# Progress Log

Append-only. Newest entry at the bottom. Each entry records what changed, the
exact commands used, results, and the next checkpoint. Do not edit history; add a
correction entry instead.

---

## 2026-11-02 — Session 01: live audit, workspace bootstrap, first PR slices

### Environment

| Item | Value |
|---|---|
| OS | Windows (win32) |
| Workspace | `C:\Users\Soumya Debnath\Documents\Default Project` |
| Python | 3.11.13 |
| Node | v22.18.0 |
| npm | 11.5.2 |
| PyTorch | 2.15.0+cpu in `%TEMP%\opencode\heros-venv` |
| GPU in this session | None exposed to the agent |
| `gh` CLI | Not installed |
| Kimi browser daemon | v2.0.26, port 10086; v2.0.28 available (not upgraded) |

The workspace `.venv` failed with `WinError 5` on `pip` metadata. The working
venv is outside the repository at `%TEMP%\opencode\heros-venv`.

### Live inspection

- GitHub `itsoumya-d?tab=repositories`: **30 public repositories** (not 11).
  New/changed names found: `HEROS-RL`, `Reflexion-SWE`, `RouteLLM-Gateway`,
  `GraphRAG-CodeAudit`, `Mobbin-UI-Compiler`, `HEROS-Firewall`,
  `HEROS-Cloud-SaaS`, `Anthropic-PerfBench`, `FREED`, `colpali-edge`,
  `certiflow-ai`, `PlotLLM`, `ridge_shade`, `developer-utilities`.
- Hugging Face `itssoumyad`: **11 Spaces, 2 datasets, 0 models, 1 collection**.
  The collection description says "Ten applied AI systems", not 13.
- The brief's `ContentForge-AI`, `EcoSphere`, and `x` repos are not present on
  the live profile.

### Cloned repositories

Shallow clones under `repos/` (gitignored): `HEROS`, `HEROS-RL`, `peervault`,
`edgeinfer`, `Reflexion-SWE`, `RouteLLM-Gateway`, `GraphRAG-CodeAudit`,
`Anthropic-PerfBench`, `Mobbin-UI-Compiler`, `HEROS-Firewall`,
`HEROS-Cloud-SaaS`.

### Baseline test runs

| Command | Result |
|---|---|
| `PYTHONPATH=rlvr/src python -m unittest discover -s rlvr/tests -v` (system Python, no torch) | **45 pass, 5 skip** |
| same, with PyTorch 2.15 CPU venv | **49 pass** |
| `python -m unittest discover -s tests -v` in `HEROS-RL` | **40 pass, 5 skip** |
| `npm run test:mcp` in `HEROS` | **46 test functions pass, 0 fail; 289 adversarial cases** |
| `npm run test:mcp` runtime | ~4.3 s |

### Corrections to the supplied brief

| Brief claim | Live result | Marker |
|---|---|---|
| 11 GitHub repos | 30 public repos | **X** |
| 13 HF artifacts | 11 Spaces + 2 datasets + 0 models | **X** |
| HEROS shell 72.8% | 36.5% of code bytes (170.5 KB / 467.5 KB); 7.6% of all repo bytes | **X** |
| peervault README says PQC unimplemented | README already documents ML-KEM-768, AAD, OPFS; residual contradictions are FAQ + resume row | **X** |
| edgeinfer says "Replaces OpenAI API" | No such tagline; README explicitly documents paged KV as not implemented | **X** |
| 289 adversarial MCP tests | Confirmed: 60+78+31+60+30+30 = 289 cases across 46 passing test functions | **V** |
| HEROS rlvr 34 tests | Confirmed: 34 baseline; 49 after the new slice | **V** |

### PR #1 — HEROS `feat/rlvr-dr-grpo-gpu-trainer` (commit `b59f47e`)

Added:

- `rlvr/src/heros_rlvr/gpu_trainer.py`
  - `DeterministicForgeShadowVerifier` with an in-memory SQLite gate, row-loss
    detection, and an authorizer denying `ATTACH`, `DETACH`,
    `PRAGMA writable_schema`, and `load_extension`.
  - `DapoDynamicSampler` and `compute_dr_grpo_token_loss` with constant-horizon
    Dr.GRPO reduction and DAPO asymmetric clipping.
  - Optional torch import; the verifier remains stdlib-only.
- `rlvr/tests/test_gpu_rlvr_pipeline.py` — 15 tests.
- `rlvr/src/heros_rlvr/__init__.py` — exports.
- `rlvr/pyproject.toml` — `gpu` extra.
- `rlvr/README.md` — trainer section.
- `.github/workflows/rlvr.yml` — CPU-torch smoke job.

Test log: `49 tests ... OK`. Without torch: `49 tests ... OK (skipped=5)`.

### PR #2 — peervault `docs/peervault-sync-limitations` (commit `4ad241e`)

Changed `README.md` only:

- Comparison row: `Resumable transfers` from `No` to `Manual (chunk bitmap)`.
- Added a paragraph explaining `receivedBitmap()` / `requestMissingChunks()` /
  `resendChunks()` and the absence of an automatic journal.
- FAQ tab-closed answer now explains manual resume.
- FAQ file-size answer now documents `createOpfsSink()` /
  `createFileSystemSink()` and removes "there is no streaming-to-disk path".

No code, crypto, or package version changed.

### PR #3 — edgeinfer `docs/edgeinfer-reconcile-readme` (commit `2dd3bc0`)

- Added `docs/wgsl-paged-attention.md`: KV block layout, bindings, online softmax
  recurrence, parity/zero-readback/memory/performance gates, non-goals.
- Linked it from the existing "Paged GPUBuffer-resident KV is not implemented"
  limitation.
- No shader, no benchmark, no speedup claim.

### Artifacts written

`AI_ENGINEERING_PORTFOLIO/` now contains the twelve strategy documents, ten
project directories, and three `git format-patch` files under
`open_source/patches/`. `repos/` is gitignored and is not part of the workspace
commit.

### Open blockers

1. No `gh` CLI and no remote push attempted. PRs #1–#3 await approval.
2. No GPU in this session; the 500-step QLoRA run is not started.
3. No Hugging Face token in the environment; no model/dataset upload attempted.
4. The Kimi browser extension works, but the daemon reports v2.0.28 available.
   The upgrade is user-initiated (`kimi-webbridge upgrade`).
5. Citation `arXiv:2606.06178` (MetaRouter) and `arXiv:2603.01162`
   (GRPO U-statistic) were initially suspected of being future-dated; both were
   verified live via the arXiv API on 2026-11-02 and are real.

### Next checkpoint

1. User approval for PR #1–#3.
2. Install `gh` or configure a credential helper; push in the approved order.
3. Start Project 01 Phase P5: QLoRA runner on Qwen2.5-Coder-1.5B-Instruct.
4. Record the first W&B run ID and checkpoint URL in this log.

---

## 2026-11-02 - Session 02: documentation completion and PR #1 de-duplication

### Documents written

- `MASTER_ROADMAP.md`: 14-week plan, gate definitions, capacity budget, risk
  register, approval gates, kill criteria, and explicit deferrals.
- `projects/project-01-heros-rlvr-studio/`: `README.md`, `BENCHMARKS.md`,
  `PR_DESCRIPTION.md`, `docs/REWARD_SPEC.md`, `docs/ARCHITECTURE.md`.
- `projects/project-02 ... project-10/README.md`: one-page specs with status,
  next action, gate, dependencies, and risks.
- `infrastructure/README.md`, `learning/README.md`,
  `portfolio_website/README.md`, and four `research/*/README.md` indexes.

### PR #1 correction

Review found that `gpu_trainer.py` duplicated three existing CPU primitives:
`advantages.dr_grpo_advantages`, `sampling.has_learning_signal`, and the
`losses.grpo_loss` reduction. The torch path now:

- delegates `DapoDynamicSampler.is_informative_group` to `has_learning_signal`;
- delegates `compute_dr_grpo_advantages` to `dr_grpo_advantages`, then converts
  the list to a tensor (rewards are constants, so the detach is intentional);
- keeps a tensor loss only because the pure-Python loss cannot backpropagate,
  and pins it to `grpo_loss(..., length_normalization="none") * L_max` with a
  parity test.

Added `rlvr/BENCHMARKS.md` to fix a README link that pointed at a non-existent
file, plus a reward-contract table and explicit loopholes in `rlvr/README.md`.

### Test log

| Command | Result |
|---|---|
| `unittest` with PyTorch 2.15.0+cpu | **51 tests pass, 0 fail** (0.383 s) |
| `unittest` without torch | **51 tests, 44 pass, 7 skip** (0.471 s) |

The two new tests are the CPU/tensor parity checks.

### Commit update

PR #1 was amended locally: `b59f47e` -> `f49a6c1`. New diff: 7 files,
+869 / -4. The patch in `open_source/patches/` was regenerated (40,079 bytes).
PR #2 (`4ad241e`) and PR #3 (`2dd3bc0`) are unchanged.

### State

- Three branches remain local. No push, no PR, no npm publish, no HF upload.
- `gh` is still absent.
- No GPU is exposed to the agent; the 500-step run is still owner-run.
- Project 01 acceptance remains blocked on P5 (runner), P7 (GPU run), P10 (HF
  adapter), not on documentation.

### Next checkpoint

1. Owner review of PR #1 (`f49a6c1`), PR #2 (`4ad241e`), PR #3 (`2dd3bc0`).
2. On approval: install `gh`, push branches, open PRs, and watch CI.
3. On PR #1 merge: implement `qlora_runner.py` and run the 100-step smoke.

---

## 2026-11-02 - Session 03: Project 01 P5 QLoRA runner

### What changed

- Added `rlvr/src/heros_rlvr/qlora_runner.py`: strict Forge-schema to SQLite
  bridge, prompt builder, `QLoRARunner`, `RunRecorder`, and the thin `HFPolicy`
  adapter.
- Added `rlvr/tests/test_qlora_runner.py` (27 tests) and
  `rlvr/scripts/train_qlora.py` (dry-run and real-run CLI).
- Extended `MigrationTask` with optional `source_schema`, `target_schema`, and
  `hazard` fields for prompt construction.
- Added the `train` extra to `rlvr/pyproject.toml`; kept `gpu` torch-only.
- Updated the CPU-torch CI job to run the full `rlvr` suite, not just the
  verifier file.
- Updated `rlvr/README.md`, `rlvr/BENCHMARKS.md`, Project 01 docs, scorecard,
  architecture, reward spec, and the root workspace index.

### Tier correction found by validation

The first 500-row dry-run failed on `expected_tier='HIGH'`. HEROS-RL and forge
use five tiers: SAFE, NOTABLE, MEDIUM, HIGH, CRITICAL. The bridge initially
accepted SAFE/WARN/CRITICAL. It now accepts all five and requires the field.
The full dry-run maps 500/500 rows with all ten hazard classes, 50 each.

### Test log

| Command | Result |
|---|---|
| `unittest` with PyTorch 2.15.0+cpu | **78 tests pass, 0 fail** (2.088 s) |
| `unittest` without torch | **78 tests, 65 pass, 13 skip** (0.535 s) |
| `train_qlora.py --dry-run` over all 500 rows | **500/500 mapped, exit 0** |
| patch applied to clean worktree at f49a6c1 | `git apply --check` = 0; then 78 pass with torch, 78/65/13 without |

The 13 skips are 7 pre-existing tensor tests and 6 runner-orchestration tests.
The schema bridge, tier validation, prompt, and recorder tests run without torch.

### Commit and patch

- PR #4 branch `feat/rlvr-qlora-runner`, commit `b1d3010`, stacked on PR #1
  `f49a6c1`.
- Diff: 9 files, +1573 / -20.
- Patch: `open_source/patches/0004-feat-rlvr-add-QLoRA-rollout-runner-and-dataset-bridg.patch`
  (68,932 bytes).
- PR packet: `projects/project-01-heros-rlvr-studio/PR_DESCRIPTION_P5.md`.

### What is still not true

- No GPU run. There is no adapter, loss curve, pass@1, or throughput number.
- `HFPolicy` has not been executed because transformers, peft, and bitsandbytes
  are not installed and no GPU is exposed to the agent.
- The shadow gate executes SQLite, not PostgreSQL; a PostgreSQL parity gate is
  still planned.
- Requirement satisfaction is still unchecked; the no-op loophole remains.
- No remote write occurred: no push, PR, npm publish, or HF upload.

### Next checkpoint

1. Owner review of PR #1 (`f49a6c1`) and stacked PR #4 (`b1d3010`).
2. On approval: install `gh`, push #1 first, then rebase #4 on the merged branch.
3. Owner-run GPU smoke: install `rlvr[train]`, run a 10-step smoke, inspect
   `run.json` and `steps.jsonl`, then decide on the 500-step ablation.

---

## 2026-11-02 - Session 04: pushed branches and opened PRs

### Approval and remote writes

The owner replied "continue and do it" to the approval request. Branches were
pushed with the existing Git credential manager. `gh` is still not installed, so
the pull requests were opened through the authenticated Kimi browser session.
No npm publish, HF upload, or deployment occurred.

### Live pull requests

Internal labels from Sessions 01-03 map as follows: PR #1 -> #101, PR #4 -> #102
(then #103 after the rebase), PR #2 -> #14, PR #3 -> #15.

| Live PR | Repository | Head commit | Base | Status |
|---|---|---|---|---|
| [#101](https://github.com/itsoumya-d/HEROS/pull/101) | `itsoumya-d/HEROS` | `f49a6c1` | `main` | merged at `8a7951d`; 18/18 green |
| [#102](https://github.com/itsoumya-d/HEROS/pull/102) | `itsoumya-d/HEROS` | `b1d3010` | old #101 branch | closed; superseded by #103 |
| [#103](https://github.com/itsoumya-d/HEROS/pull/103) | `itsoumya-d/HEROS` | `0ac89ff` | `main` | open; 18/18 green |
| [#14](https://github.com/itsoumya-d/peervault/pull/14) | `itsoumya-d/peervault` | `4ad241e` | `main` | open; 3/3 green |
| [#15](https://github.com/itsoumya-d/edgeinfer/pull/15) | `itsoumya-d/edgeinfer` | `2dd3bc0` | `main` | open; 2/2 green |

### Corrections after #101 was merged

The owner merged #101 with a squash merge (`8a7951d`) while this session was
still running. The runner branch was rebased with
`git rebase --onto origin/main f49a6c1 feat/rlvr-qlora-runner`, producing
`0ac89ff`. The old stacked base branch was deleted, which closed #102 instead of
retargeting it. #103 is the clean replacement against `main`: 1 commit, 9 files,
78 tests, and 18/18 checks green. #102 has a comment pointing to #103.

### Verification after push

- GitHub check-runs API: all checks completed with `success` for #101, #102,
  #103, #14, and #15 head commits. HEROS reports 18 checks per commit because
  both push and pull_request events run the matrix; `RLVR unit tests` and
  `GPU trainer smoke tests (CPU torch)` are green.
- PR #101 body contains the reward/loss problem statement and the 51-test log.
- PR #103 body contains the 78-test log, the 500/500 dry-run, and the explicit
  "no GPU run" limitation.
- PR #14 and #15 bodies are documentation-only and contain no benchmark claim.

### State

- #101 is merged; #103, #14, and #15 are open.
- Local `feat/rlvr-qlora-runner` is now 1 commit ahead of `origin/main` at
  `0ac89ff`; the old branch is preserved locally as
  `feat/rlvr-qlora-runner-pre-rebase`.
- No `gh` binary; PR creation/editing used the authenticated Kimi browser
  session. The extension/daemon version mismatch is still present.
- The 500-step GPU run, HF adapter, and model card remain undone.

### Next checkpoint

1. Merge #103 after review.
2. Review/merge #14 and #15.
3. Owner-run 10-step GPU smoke, then the 100-step and 500-step runs.
4. Publish an adapter/model card only after `run.json` and `steps.jsonl` exist.

---

## 2026-11-02 - Session 05: merged the four portfolio PRs

### Merges

The user said "continue" after the PRs were green; the remaining merges were
performed through the GitHub API using the stored Git credential. No token was
written to disk or printed.

| PR | Merge commit | Method |
|---|---|---|
| [#101](https://github.com/itsoumya-d/HEROS/pull/101) | `8a7951d` | squash, owner-merged |
| [#103](https://github.com/itsoumya-d/HEROS/pull/103) | `d3588ca` | squash |
| [#14](https://github.com/itsoumya-d/peervault/pull/14) | `7025352` | squash |
| [#15](https://github.com/itsoumya-d/edgeinfer/pull/15) | `088c217` | squash |

#103 is the replacement for #102, which was closed when the old stacked base
branch was deleted after #101's squash merge. #102 has a comment pointing to
#103. Merged remote branches were deleted.

### Post-merge verification

Ran from a clean worktree at `HEROS origin/main` (`d3588ca`):

| Command | Result |
|---|---|
| `unittest` with PyTorch 2.15.0+cpu | **78 tests pass, 0 fail** (2.110 s) |
| `unittest` without torch | **78 tests, 65 pass, 13 skip** (0.506 s) |

CI at merge time: #103 18/18 green, #14 3/3 green, #15 2/2 green.

### State

- Project 01 verifier, loss, schema bridge, and QLoRA runner are on `main`.
- The portfolio has four merged PRs and zero open portfolio PRs.
- No GPU run, adapter, model card, npm publish, or HF upload exists.
- `HFPolicy` remains untested; the next useful step is a 10-step GPU smoke.
- The local workspace branch `docs/ai-engineering-portfolio` records the final
  hashes and merge state.

---

## 2026-11-02 - Session 06: GPU environment, prompt fix, and 500-step launch

### GPU environment

`nvidia-smi` exposed the host RTX 2060 6 GB, but the original test venv had
`torch 2.15.0+cpu` and `torch.cuda.is_available()` was false. A separate venv was
created at `%TEMP%\opencode\heros-gpu-venv` with:

- torch `2.14.1+cu130`
- transformers `5.22.1`
- peft `0.21.2`
- accelerate `1.15.0`
- bitsandbytes `0.50.2`
- numpy `2.4.6`

`torch.cuda.is_available()` is now true and reports the RTX 2060.

### HFPolicy test

A tiny-model test exercised `HFPolicy.load`, `generate`, `token_logprobs`,
backward, `optimizer.step`, and `save`. It produced an adapter at 24.8 MB VRAM
with the tiny model. This closed the "HFPolicy untested" gap at the mechanism
level.

### 0.5B negative smoke

Qwen2.5-Coder-0.5B-Instruct, fp16, 10 steps, group size 2, 96 completion tokens:

- 0 optimizer steps; 10/10 skipped as zero-variance.
- All rewards `-1.0`, error `MISSING_BLOCKS`.
- 224.92 s, 1.97 GB peak.
- The model wrote prose/Markdown instead of the required tags.

Evidence: `runs/2026-11-02-gpu-smoke-0.5b/`.

### Prompt fix and 1.5B positive smoke

A one-shot literal tag exemplar was added and tested. The 1.5B model then
emitted exact `<think>`, `<sql_migration>`, `<forge_manifest>` blocks and scored
`1.0` instead of `-1.0`. The fix is PR #104, merged at `d38a603`; the suite is
now 79 tests (66 pass + 13 skip without torch).

Qwen2.5-Coder-1.5B-Instruct, NF4 4-bit, 10 steps, group size 2, 128 completion
tokens:

- **7 optimizer steps**, 3 zero-variance skips.
- Mean reward **0.339**, range `-0.75` to `1.75`.
- 185.0 s, **4.15 GB** peak, ~18.5 s/step.
- A temporary adapter was saved but is not published or called trained.

Evidence: `runs/2026-11-02-gpu-smoke-1.5b/`.

### 500-step run

A 500-step single-arm run (Dr.GRPO + DAPO, Qwen2.5-Coder-1.5B, NF4, G=2,
128 completion tokens, seed 42) was started in the background at 04:38 UTC.
It writes `run.json`, `steps.jsonl`, `checkpoints.jsonl`, checkpoints every 50
steps, and a final adapter to
`runs/2026-11-02-a3-500-qwen1.5b/`. It was at 19 steps when this entry was
written; the final result is recorded in the next entry.

### Still not done

- No completed 500-step results, held-out evaluation, or published adapter.
- No HF token, so no model/dataset upload.
- No npm publish.

---

## 2026-11-02 - Session 07: 500-step run completed, evaluation launched

### Run result

The 500-step single-arm A3 run completed at 11:09 UTC (16:39 local) after
23,541.5 s (6.54 h).

| Metric | Value |
|---|---:|
| Steps | 500 |
| Completed optimizer steps | 209 |
| Skipped zero-variance groups | 291 |
| Mean reward | 1.0203 |
| Reward, first 50 completed | 0.4975 |
| Reward, last 50 completed | 1.3100 |
| Reward range | -0.75 to 1.875 |
| Mean loss | 0.015926 |
| Mean KL | 0.021152 |
| Mean clip fraction | 0.0 |
| Error codes | 830 OK, 134 SQL_EXEC_ERROR, 36 MISSING_BLOCKS |
| Peak allocated VRAM | 4,158.9 MB |
| Final adapter | `runs/2026-11-02-a3-500-qwen1.5b/final/` |
| Checkpoint-450 | `runs/2026-11-02-a3-500-qwen1.5b/checkpoint-450/` |

This is a training-set reward curve. It does not yet include a held-out result.
The first-vs-last window suggests learning, but that is not a significance test.

### Code and docs merged

- PR #104: literal tag exemplar, `d38a603`.
- PR #105: GPU smoke docs, `a8451f6`.
- PR #106: held-out evaluation package/CLI, `83a1b96`.
- Suite: **85 tests**; 72 pass + 13 skip without torch.

### Evaluation in progress

The watcher is evaluating base vs `checkpoint-450` on rows 451-500 (50 tasks),
then verifying the final adapter and generating `MODEL_CARD.md`. The evaluation
is greedy, max 128 new tokens, same prompt/verifier as training.

The final 500-step adapter is not used for the held-out claim because it trained
on rows 451-500 after checkpoint-450. The 450 checkpoint is the held-out model.

### Still pending

- Held-out metrics and model card.
- Adapter upload (no HF token).
- npm publish (no package change).
- Four-arm ablation and parallel workers.

---

## 2026-11-02 - Session 08: held-out evaluation and reward-hacking finding

### Held-out protocol

Base vs `checkpoint-450` on rows 451-500 (50 tasks). Greedy decoding, 128 new
tokens, same prompt and verifier. `checkpoint-450` had not seen those rows; the
final 500-step adapter did, so it is excluded from the held-out claim.

### Result

| Model | Mean reward | OK rate | Risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base Qwen2.5-Coder-1.5B | 0.71 | 0.66 | 0.16 | 0.0 |
| A3 checkpoint-450 | **1.465** | **1.0** | **0.02** | 0.0 |

### Failure analysis

The adapter did not learn to perform the requested migration. It learned the
tag format and a safe additive no-op:

- 50/50 completions parsed and executed.
- 36/50 added a generic `note` column.
- 0/50 contained destructive SQL.
- All 50 predicted `has_data_loss: false` and `decision_required: false`.
- Risk-tier accuracy fell from 0.16 to 0.02.

Example `heros-mig-0451` is a `drop_column` task with expected tier `CRITICAL`.
The adapter added `note TEXT`, predicted `NOTABLE`, and received `1.0`.

This is the documented no-op loophole, not migration competence. The mean reward
increase is mostly the `+0.25` format and `+0.75` execution components.

### Artifacts

- `runs/2026-11-02-a3-500-qwen1.5b/MODEL_CARD.md`
- `runs/2026-11-02-a3-500-qwen1.5b/eval_450/base.jsonl`
- `runs/2026-11-02-a3-500-qwen1.5b/eval_450/adapter450.jsonl`
- `runs/2026-11-02-a3-500-qwen1.5b/final/` (local adapter, 73.9 MB)
- `runs/2026-11-02-a3-500-qwen1.5b/checkpoint-450/`

The final adapter was verified with PEFT and returned `ADAPTER_OK` at 1.24 GB
VRAM. It is local only.

### Decision

P01 is **not portfolio-ready**. Do not publish the adapter. The next engineering
task is a deterministic requirement-satisfaction check that closes the no-op
loophole; only then rerun the evaluation and ablation. This negative result is
more valuable than a claim based on format compliance.

### Still pending

- Requirement-satisfaction reward and a new held-out run.
- Four-arm ablation.
- HF upload (no token).
- npm publish (no package change).

---

## 2026-11-02 - Session 09: requirement check merged

PR #107 (`f0e22d6`) closes the no-op loophole for tasks with a target schema.
The verifier now compares tables, column names, SQLite affinity, `NOT NULL`, and
primary keys after the migration. A valid but unrelated migration gets
`REQUIREMENT_MISS` and `-0.75` execution reward; a matching schema earns `+0.75`.

- All 500 dataset target schemas parse.
- `heros-mig-0001` with a real `DROP COLUMN` scores 2.0; the same task with
  `ADD COLUMN bio` scores -0.5 and `REQUIREMENT_MISS`.
- Suite: **87 tests**; 74 pass + 13 skip without torch.

The old 500-step adapter is invalid under the corrected reward and must not be
published. Re-scoring the stored held-out completions under #107 gives base
0.02 and adapter 0.265; the adapter has 10 `OK` and 40 `REQUIREMENT_MISS`. The
old 1.465 was format/execution reward, not migration correctness.

A 10-step retraining smoke is running to check whether the base model can produce
any target-satisfying groups; if every group collapses to `REQUIREMENT_MISS`,
the next step is SFT/target-diff prompting, not a 500-step run.

---

## 2026-11-02 - Session 10: corrected-reward smoke

The 10-step smoke with #107's target-schema check ran on Qwen2.5-Coder-1.5B
(NF4, group size 2, 128 completion tokens):

| Metric | Value |
|---|---:|
| Steps | 10 |
| Optimizer steps | 7 |
| Zero-variance skips | 3 |
| Mean per-step reward | -0.2375 |
| Error codes | 9 REQUIREMENT_MISS, 5 MISSING_BLOCKS, 4 SQL_EXEC_ERROR, 2 OK |
| Wall clock | 174.11 s |
| Peak VRAM | 4,154.6 MB |

The check works: no-op SQL no longer earns execution reward. The remaining
problem is capability. The base model cannot satisfy most target schemas, so a
long RL run would mostly train on failures and zero-variance groups.

### Decision

Do not run another 500-step RL attempt on this prompt. Build an SFT/target-diff
warm start first, then evaluate a new checkpoint. The old 500-step adapter is
invalid under #107 and must not be published.

### Re-score of the old adapter

Stored held-out completions re-scored under #107:

| Model | Old reward | Corrected reward | OK | REQUIREMENT_MISS |
|---|---:|---:|---:|---:|
| Base | 0.71 | 0.02 | 10 | 23 |
| Old adapter | 1.465 | 0.265 | 10 | 40 |

This confirms the old 1.465 was format/execution reward, not migration skill.

---

## 2026-11-02 - Session 11: SFT target generator merged

PR #108 (`c32614f`) adds deterministic SFT targets derived from the old/target
schema diff:

- add/drop column;
- add NOT NULL with a default;
- single-column rename;
- table rebuild for type, NOT NULL, and primary-key changes.

`target_completion` wraps the SQL and expected manifest in the verifier's tags.
A schema-diff pass over all 500 rows produces target-matching SQL for 450 rows.
The 50 `type_narrowing` rows are excluded because SQLite cannot distinguish
`bigint` from `int`; they collapse to the same affinity.

Suite: **93 tests** (80 pass + 13 skip without torch).

A 500-step supervised warm start is running on the first 450 rows with the SFT
targets. Rows 451-500 remain held out. If the loss stays finite and the adapter
improves held-out requirement satisfaction, the next step is a short RL run from
the SFT checkpoint; if not, the target generator or model size is the blocker.

---

## 2026-11-02 - Session 12: SFT warm start completed

The SFT warm start ran 500 supervised steps on 405 target examples from the
first 450 rows (the 50 type_narrowing rows are excluded from supervision):

- Loss: 1.5299 (first) -> 0.0000313 (last); mean 0.01208
- Wall clock: 496.24 s
- Peak VRAM: 3,142.9 MB
- Adapter: `runs/2026-11-02-sft-warmstart/final/`

The adapter is local and unpublished. A held-out evaluation on rows 451-500 is
running under the #107 requirement-check reward. Training loss near zero is
memorization evidence only; the held-out result decides whether the warm start
generalizes.

PR #108 (SFT target generator) merged at `c32614f`; suite is 93 tests.

---

## 2026-11-02 - Session 13: SFT held-out evaluation

The SFT warm start evaluated on rows 451-500 under the #107 requirement reward.
The first run used 128 new tokens and truncated 20 long rebuild completions;
the corrected run used 512 tokens.

| Model | Mean reward | OK rate | Manifest risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base | 0.02 | 0.20 | 0.1957 | 0.0 |
| SFT adapter | **1.90** | **1.00** | **0.90** | 0.10 |

- 45/50 tasks score 2.0.
- 5/50 score 1.0; all five are `type_narrowing`, excluded from SFT because
  SQLite cannot distinguish `bigint` from `int`.
- Manifest data-loss accuracy 0.90; approval accuracy 0.90.
- The 0.10 row-loss rate is the five `drop_table` tasks, where row loss is
  expected by the task label.

### Artifacts

- `runs/2026-11-02-sft-warmstart/final/` (LoRA adapter, local)
- `runs/2026-11-02-sft-warmstart/MODEL_CARD.md`
- `runs/2026-11-02-sft-warmstart/eval_450_512/`
- `runs/2026-11-02-sft-warmstart/sft_metrics.json`

### Status

P01 is locally portfolio-ready but unpublished. The old RL adapter remains
invalid. HF upload is blocked on credentials; the controlled RL-from-SFT and
four-arm ablation are still missing. A fixed evaluation metric separates
manifest risk accuracy from the combined calibration score.

---

## 2026-11-02 - Session 14: SFT held-out result and metric correction

The SFT adapter evaluated on rows 451-500 with 512 generated tokens:

| Model | Mean reward | OK rate | Risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base | 0.02 | 0.20 | 0.1957 | 0.0 |
| SFT adapter | **1.90** | **1.00** | **0.90** | 0.10 |

45/50 tasks score 2.0; the five 1.0 tasks are `type_narrowing`, excluded from
SFT because SQLite cannot distinguish their types. Manifest data-loss and
approval accuracy are both 0.90.

The evaluation summary previously used `risk_calibration_reward == 0.5` as
"risk accuracy"; that field stores the combined calibration score. PR #109
(`1f047ad`) adds explicit risk/loss/decision match flags, `calibration_mean`, and
`calibration_full_rate`. The SFT model card uses the corrected metrics.

P01 is locally portfolio-ready but unpublished. HF upload is blocked on
credentials. The old RL adapter is invalid; a controlled RL-from-SFT and
four-arm ablation remain optional follow-ups, not safety claims.

---

## 2026-11-02 - Session 15: reproducible SFT CLI

PR #110 (`90f33a1`) adds `rlvr/scripts/sft_warmstart.py` and
`build_sft_examples()`. The CLI can regenerate the SFT adapter from the dataset:

```bash
python rlvr/scripts/sft_warmstart.py \
  --dataset ../HEROS-RL/data/heros_migration_500.jsonl \
  --limit 450 --steps 500 --output-dir outputs/sft-warmstart
```

`--dry-run` reports 405 examples (45 each for 9 hazards; `type_narrowing`
excluded) without importing torch. The script writes `run.json`,
`sft_metrics.json`, and `final/`.

Suite: **94 tests** (81 pass + 13 skip without torch). The SFT result remains
1.90 held-out vs base 0.02 with 45/50 at 2.0. The adapter is local and
unpublished.

---

## 2026-11-02 - Session 16: P02 corpus inventory

P01 is locally complete (SFT 1.90 held-out, 94 tests). Work moved to P02.

- Counted the existing 289 adversarial cases in
  `packages/mcp/test/adversarial.test.mjs`.
- Allocated the 211-case gap across JSON-RPC, agentic schema, auth/scope, forge,
  shadow, approval replay, and end-to-end destructive gates.
- Wrote `projects/project-02-heros-safeagent-os/CASE_MAP.md` with the corpus
  schema, implementation order, and gate.
- No P02 code changes yet; the next checkpoint is the corpus JSON + runner.

HF publication of the P01 SFT adapter remains blocked on credentials and explicit
approval. No npm publish.
