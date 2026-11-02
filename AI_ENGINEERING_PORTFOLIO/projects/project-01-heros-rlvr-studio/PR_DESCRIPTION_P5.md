# PR #103 — feat(rlvr): QLoRA rollout runner + dataset bridge

**Status:** **merged** into `main` at `d3588ca` (squash merge); CI was 18/18 green.
**Live PR:** https://github.com/itsoumya-d/HEROS/pull/103
**Supersedes:** #102 (closed when the old stacked base branch was deleted).
**Repository:** `itsoumya-d/HEROS`
**Base for this PR:** `main` at `8a7951d`
**Branch:** `feat/rlvr-qlora-runner` (deleted after merge)
**Commit:** `0ac89ff` (rebased runner commit)
**Patch:** `AI_ENGINEERING_PORTFOLIO/open_source/patches/0004-feat-rlvr-add-QLoRA-rollout-runner-and-dataset-bridg.patch`
**Diff size:** 9 files, +1573 / −20

---

## 1. Why this PR exists

#101 added the verifier and the tensor loss but stopped at a pure function. It
could not sample a model, score a group, update an adapter, or leave a run log.
This PR adds that missing orchestration layer:

```text
dataset row -> SQLite fixture -> prompt -> G rollouts
            -> shadow verifier -> zero-variance filter
            -> token log-probs -> Dr.GRPO/DAPO loss
            -> gradient accumulation -> optimizer -> checkpoint + run.json
```

It is deliberately split into a **tested protocol layer** and a **thin model
adapter**. The runner is tested on CPU with a fake policy and the real SQLite
verifier. `HFPolicy` needs Transformers, PEFT, bitsandbytes, and a GPU; it is not
covered by CI and **no GPU run is claimed**.

---

## 2. Changes

| File | Change | Why |
|---|---|---|
| `rlvr/src/heros_rlvr/qlora_runner.py` | New: schema bridge, prompt builder, `QLoRARunner`, `RunRecorder`, `HFPolicy` | The runner layer |
| `rlvr/tests/test_qlora_runner.py` | New: 27 tests | Pin the bridge and orchestration |
| `rlvr/src/heros_rlvr/gpu_trainer.py` | `MigrationTask` gains optional `source_schema`, `target_schema`, `hazard`; tier comment corrected | Prompt metadata without breaking existing callers |
| `rlvr/src/heros_rlvr/__init__.py` | Export the runner API | Public surface |
| `rlvr/pyproject.toml` | `train` extra: transformers, peft, accelerate, bitsandbytes | Keep torch-only `gpu` extra light |
| `rlvr/scripts/train_qlora.py` | CLI with `--dry-run` and real-run path | Reproducible entry point |
| `.github/workflows/rlvr.yml` | CPU-torch job runs the full suite, not only the verifier file | Runner tests do not drift out of CI |
| `rlvr/README.md` | Runner section, tier table, limitations, test counts | Reviewer-facing contract |
| `rlvr/BENCHMARKS.md` | Current CPU results and the runner's unmeasured status | No fake throughput |

### 2.1 Dataset bridge

The HEROS-RL dataset stores schemas in the Forge `TABLE`/`COLUMN` format, while
the verifier executes SQLite. The bridge is strict:

- identifiers must be simple `[A-Za-z_][A-Za-z0-9_]*`;
- column types must be in an explicit map;
- unknown types, duplicate tables/columns, a `COLUMN` before a `TABLE`, and a
  table with no columns all raise before training;
- SQLite DDL is generated with quoted identifiers;
- two deterministic seed rows are inserted per table.

**Tier correction found during validation.** The first dry-run failed on
`expected_tier="HIGH"`. The dataset uses the forge five-tier scale (`SAFE`,
`NOTABLE`, `MEDIUM`, `HIGH`, `CRITICAL`), while the initial bridge accepted
`SAFE`/`WARN`/`CRITICAL`. The bridge now accepts all five and requires the field;
a full 500-row dry-run maps every row.

### 2.2 Prompt construction

`build_prompt` includes the hazard class and the current/target schemas. It
deliberately **excludes** `expected_tier`, `data_loss`, and
`requires_expand_contract`: those are labels the model must infer. The prompt
requires SQLite-compatible SQL because the shadow gate is SQLite, not
PostgreSQL.

### 2.3 Runner behavior

- `QLoRARunner` processes one prompt group at a time (`B=1`).
- It rejects a non-informative group before computing log-probs (DAPO dynamic
  sampling).
- It computes current log-probs and a frozen reference's log-probs, then calls
  `compute_dr_grpo_token_loss`.
- Loss is divided by `gradient_accumulation`; eight micro-batches therefore have
  the same effective scale as one batch. A test compares accumulated and
  single-batch SGD updates.
- A non-finite loss clears accumulated gradients and is recorded as
  `non_finite_loss`.
- Checkpoints are written every `checkpoint_every` steps plus a `final/` adapter.
- `RunRecorder` truncates stale `steps.jsonl` on a new run, writes `run.json`
  atomically, and records environment data (Python, platform, SQLite, torch/CUDA
  when present).

### 2.4 Model adapter

`HFPolicy` is intentionally thin:

- 4-bit NF4 + fp16 on CUDA; fp32 on CPU;
- LoRA target modules for Qwen-family attention/MLP projections;
- left padding for decoder generation;
- tokenizer chat template applied consistently in generation and log-prob
  computation;
- reference policy is a second base model without the adapter;
- adapter + tokenizer saved, base model not merged.

It has not been executed on a GPU in this session. The PR does not claim that it
works end to end.

### 2.5 CLI

```bash
python rlvr/scripts/train_qlora.py \
  --dataset ../HEROS-RL/data/heros_migration_500.jsonl --dry-run
```

The dry-run imports no torch and validates every row. A real run needs
`pip install -e "rlvr[train]"` and a GPU.

---

## 3. Test plan and results

```powershell
# From the HEROS repository root
$env:PYTHONPATH = "rlvr/src"

# With CPU torch
& "$env:TEMP\opencode\heros-venv\Scripts\python.exe" -m unittest discover -s rlvr/tests -v

# Without torch
python -m unittest discover -s rlvr/tests
```

### Result with torch

```text
Ran 78 tests in 2.088s
OK
```

### Result without torch

```text
Ran 78 tests in 0.535s
OK (skipped=13)
```

The 13 skips are 7 pre-existing tensor tests and 6 runner-orchestration tests.
The schema bridge, prompt, tier validation, and recorder tests run without
torch.

### 500-row dry-run

```text
rows: 500, planned_steps: 500, group_size: 4
hazards: all 10 classes present, 50 each
```

### Patch verification

The patch was exported with `git format-patch`, applied with
`git apply --check` to a clean worktree at `f49a6c1`, and the full suite was run
from the applied worktree:

```text
APPLY_CHECK=0
Ran 78 tests ... OK
Ran 78 tests ... OK (skipped=13)
```

### What the tests cover

| Area | Cases |
|---|---|
| Schema bridge | parse, DDL, seed rows, multiple tables, unknown type, duplicate table, column-before-table |
| Dataset mapping | five tiers, missing tier, unknown tier, non-boolean flag, JSONL round-trip, empty file |
| Prompt | hazard + schemas present; expected labels absent |
| Rollout | mixed group informative; uniform group rejected |
| Runner | optimizer update, zero-variance skip, accumulation deferral, accumulation scaling, artifacts/checkpoints, empty-task rejection |
| Recorder | run metadata, step log truncation, summary counts |

No test asserts model quality or throughput. No test requires a GPU.

---

## 4. What is not claimed

- No model was trained. There is no adapter, loss curve, pass@1 number, or
  throughput number.
- `HFPolicy` is untested; the first real run may expose tokenizer, dtype, or
  device-map issues.
- The shadow gate executes SQLite, a subset of PostgreSQL. A production
  PostgreSQL parity evaluation is a separate gate.
- Requirement satisfaction is still not checked; the no-op loophole from #101
  remains.
- The runner is serial. Parallel shadow workers (P8) are not in this PR.

---

## 5. Compatibility and risk

- **Rebased after #101.** #101 is squash-merged into `main`; this branch is
  rebased onto `main` and contains only the runner commit. It is no longer
  stacked on the old base branch.
- **No existing API removed.** `MigrationTask` gains optional trailing fields;
  existing seven-argument construction still works.
- **Torch remains optional.** Importing `heros_rlvr` does not import
  transformers, peft, or bitsandbytes.
- **CI cost:** the existing CPU-torch job now runs 78 tests instead of 17; the
  measured runtime is ~2 s on this machine.
- **Windows/Linux:** tested on Windows Python 3.11.13; CI is Ubuntu Python 3.12.
- **Rollback:** revert `0ac89ff`; no data or schema migration is involved.

---

## 6. Reviewer guide

Start with:

1. `rlvr/src/heros_rlvr/qlora_runner.py` — `dataset_row_to_task`, `train_step`,
   `HFPolicy.token_logprobs`.
2. `rlvr/tests/test_qlora_runner.py` — the fake policy and the accumulation
   scaling test.
3. `rlvr/scripts/train_qlora.py` — the real-run wiring.
4. `rlvr/README.md` — limitations and test counts.

Questions worth asking:

- Is SQLite-compatible prompting the right compromise for a PostgreSQL product,
  or should the reward run a PostgreSQL container?
- Should the reference policy share the base weights with the adapter disabled
  instead of loading a second model?
- Is one optimizer step per prompt group the right unit, or should the runner
  batch multiple prompts before stepping?
- Should `HFPolicy` apply a fixed system prompt in addition to the chat template?
- Is `gradient_accumulation` the right place to normalize, or should the loss
  function take a `micro_batch_count` argument?

---

## 7. Checklist

- [x] Feature branch, no commit to `main`
- [x] Based on merged #101; targets `main` after rebase
- [x] Conventional commit message
- [x] Full suite run with and without torch
- [x] All 500 dataset rows mapped by the dry-run
- [x] Tests for every runner branch and recorder path
- [x] Patch applies cleanly to `f49a6c1`
- [x] No secrets, tokens, or local paths in the diff
- [x] GPU adapter and throughput limitations documented
- [x] Push approved by owner
- [x] PR opened: #103 (against `main`)
- [x] CI green on GitHub (18/18 checks)
- [x] Merged into `main` at `d3588ca`
- [ ] **Real GPU smoke run**

---

## 8. Next step

[#101](https://github.com/itsoumya-d/HEROS/pull/101) and
[#103](https://github.com/itsoumya-d/HEROS/pull/103) are merged into `main`. A
real GPU smoke run is still required before any training result is claimed.
Merging these PRs does not approve an npm publish or an HF upload.
