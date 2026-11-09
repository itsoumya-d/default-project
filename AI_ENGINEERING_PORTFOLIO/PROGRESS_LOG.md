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

---

## 2026-11-03 - Session 17: P02 500-case corpus

PR #111 (`7875f3a`) adds 211 deterministic cases to the existing 289, completing
the 500-case P02 corpus:

| Surface | New cases |
|---|---:|
| malformed JSON-RPC | 40 |
| agentic schema mutation | 30 |
| auth/scope | 25 |
| hostile forge payloads | 30 |
| malformed shadow schemas | 30 |
| approval replay/rebind | 30 |
| destructive approval gate | 26 |

`npm run test:mcp`: **53 tests pass, 0 fail**; the new test functions assert
their own counts. Existing 289 + new 211 = 500.

This closes the case-count part of the P02 gate. Still missing: Ed25519 signed
inclusion proofs, p99 policy latency, 64-worker idempotency torture, browser
proof verification, and a standalone public corpus package.

---

## 2026-11-03 - Session 18: Ed25519 signed proofs + browser verifier

PR #112 (`d0e523f`) adds Ed25519 signing to the append-only Merkle log:

- domain-separated root signatures (`HEROS-MERKLE-ROOT-v1\0`);
- `signMerkleRoot`, `verifyMerkleRoot`, `signInclusionProof`,
  `verifySignedInclusionProof`;
- `createMerkleReceiptStore` accepts a signer and stores
  `merkle_root_signature` + `signer_public_key`;
- `store.signedInclusionProof` returns a signed proof;
- `store.verify()` detects `MERKLE_ROOT_MISMATCH` and `SIGNATURE_MISMATCH`.

Browser verifier: `packages/agentic/web/verify-proof.html` uses WebCrypto
Ed25519 + SHA-256. Live browser check:

- valid signed proof: **PASS**;
- tampered signature: **FAIL** (`Merkle path: true; signature: false`).

Agentic suite: **35 tests pass**. P02 now has 500 cases + signed proofs +
browser verification. Remaining gate items: p99 policy latency <4.5 ms,
64-worker idempotency torture, and a public corpus package.

---

## 2026-11-03 - Session 19: P02 latency + idempotency

PR #113 (`58173eb`) adds `npm run bench:policy`:

| Metric | Value |
|---|---:|
| Samples | 5000 |
| p50 | 0.0364 ms |
| p95 | 0.0954 ms |
| p99 | **0.245 ms** |
| Max | 2.3768 ms |

It measures validation + authorization + handler + an O(1) memory receipt
append, and deliberately excludes the Merkle wrapper. Re-running with the
signed Merkle wrapper gave p99 **33.8 ms** at 5000 receipts because the root is
recomputed O(n) on every append. That is a real scalability limit, recorded in
ADR-014, not a policy-latency result.

PR #114 (`9ca2264`) adds an in-flight idempotency map to `AgenticApp`:

- 64 concurrent requests with one key: **1 handler invocation, 1 receipt, 63
  `_idempotent: true` responses**;
- a concurrent different payload gets `IDEMPOTENCY_CONFLICT` and does not
  execute;
- `npm run test:agentic` = **37 pass**, `npm run test:mcp` = **53 pass**.

Scope is in-process only (ADR-015). Cross-process 64-worker replay and the
standalone public corpus package remain the P02 blockers.

---

## 2026-11-03 - Session 20: P02 cross-process lock + threat model

PR #115 (`dc51441`) closes the P02 64-worker gate item at the host-local level:

- `withFileLock` uses exclusive lock-file creation with bounded retry, jitter,
  stale-lock recovery, and Windows `EPERM`/`EACCES` handling;
- file receipt and approval stores take a global lock around read-modify-write;
- `withIdempotencyLock(key, fn)` serializes one key across processes;
- `createMerkleReceiptStore` delegates the key lock;
- 64 spawned Node workers, one key: **1 handler execution, 1 receipt, 1
  idempotency record, 63 `_idempotent: true` responses**;
- 8/8 local stress runs passed after the Windows retry fix.

The same PR adds `packages/agentic/THREAT_MODEL.md` (10 threat rows) and updates
the package README so its multi-process and O(n) Merkle claims match the code.

Suites: `npm run test:agentic` = **38 pass**; `npm run test:mcp` = **53 pass**.
P02's acceptance gate is now met locally. Remaining P02 work: a standalone
public corpus package and the npm release (owner approval required).

---

## 2026-11-03 - Session 21: incremental Merkle frontier

PR #116 (`d93e7d9`) removes the O(n) Merkle root recomputation:

- `createMerkleReceiptStore` keeps one perfect-subtree root per level;
- append carries a leaf upward and folds the peaks, matching `merkleRoot`
  including odd-node promotion;
- appends serialize through a promise chain, so concurrent calls cannot share a
  stale frontier;
- tests cover 96 sequential sizes, reload parity, and 32 concurrent appends.

`npm run test:agentic` = **40 pass**; `npm run test:mcp` = **53 pass**.

`npm run bench:merkle` with Ed25519 signing and an in-memory store:

| Metric | Value |
|---|---:|
| Tree size | 5200 |
| p50 | 0.2015 ms |
| p95 | 0.3412 ms |
| p99 | **0.6226 ms** |
| Max | 5.4516 ms |

The earlier wrapper measured **33.8 ms** p99 at 5000 receipts. The file store
still rewrites the whole JSON file, `verify()` is still O(n), and proofs are
O(n) to generate; those limits are documented in the threat model.

---

## 2026-11-03 - Session 22: standalone P02 corpus package

PR #117 (`2658e90`) packages the 500 adversarial cases as a dataset:

- `packages/mcp/corpus/corpus.jsonl` â€” 500 records with input and expected
  verdict;
- `manifest.json` â€” 13 group counts, surface/ASI aggregates, source tests, and
  SHA-256 `03f0608cb9b0d9b86c4216daa9843dbad05d353986c09b4e6247bb933462ba92`;
- `recorder.mjs` â€” per-worker JSONL recorder, no-op in normal test runs;
- `build.mjs` â€” runs both suites, validates counts/IDs, writes the package;
- `corpus:build` / `corpus:check`, plus a dedicated CI drift job.

Approval nonces are recorded as a runtime marker with a setup object; two
consecutive builds produced the same SHA-256.

`npm run test:mcp` = **54 pass** (including `corpus-package.test.mjs`);
`npm run test` passed; PR #117 CI = **20/20 green**.

P02 now has 500 executable cases, a 500-record package, signed proofs, browser
verification, p99 policy latency, host-local 64-process idempotency, an
incremental Merkle root, and a threat model. Remaining: npm release (approval)
and the shell-script maintenance story.


---

## 2026-11-03 - Session 23: agentic 0.3.0 release candidate

PR #118 (`cbee92a`) prepares `@soumyadebnath1619/agentic@0.3.0` without
publishing:

- version bump from 0.2.0 (already public) to 0.3.0;
- `THREAT_MODEL.md` and `CHANGELOG.md` added to the npm tarball;
- `npm run pack:agentic` inspected: 9 files, 22.3 kB packed, 82.9 kB unpacked,
  shasum `e36f6e8233ef9d0aa340e4a289cca1b1a50ca509`;
- no tag, no registry write, no approval bypassed;
- `npm run test:agentic` = 40 pass; CI = 20/20 green.

P02 is now complete locally: 500 executable cases, 500-record dataset, signed
proofs, browser verification, p99 policy latency, 64-process idempotency,
incremental Merkle root, threat model, and a release candidate. Remaining:
owner approval to publish and the shell-script maintenance story.


---

## 2026-11-03 - Session 24: RL-from-SFT probe and adapter init

PR #119 (`e4cfed4`) adds `RunnerConfig.adapter_path`, loads an existing PEFT
adapter as trainable in `HFPolicy.load`, wires `train_qlora.py --adapter-path`,
and adds temperature/completion/gradient-accumulation CLI controls. The `rlvr`
suite is **95 pass**.

GPU probes from the SFT adapter:

| Run | Group | Temp | Steps | Completed | Reward pattern |
|---|---:|---:|---:|---:|---|
| smoke | 2 | 1.0 | 2 | 0 | 2.0, 2.0 |
| probe | 4 | 1.2 | 10 | 0 | nine 2.0, one 1.0 |
| probe | 4 | 1.5 | 10 | 0 | nine 2.0, one 1.0 |

Every group was skipped as `zero_variance_group`. Sampling diversity exists at
temperature 1.5 (4/8 unique) and 2.0 (8/8), but the deterministic reward stays
constant, so DAPO has no advantage signal. The SFT adapter remains the accepted
result; no RL improvement is claimed. Recorded in
`projects/project-01-heros-rlvr-studio/RL_FROM_SFT.md`.

Next: RL from the base model with the corrected reward, then a harder task
distribution if variance is still too low.


---

## 2026-11-03 - Session 25: 100-step RL from base

Ran a 100-step corrected-reward RL pilot from the base model on rows 1-450:

- 91/100 groups completed, 9 skipped;
- training mean reward -0.2328 overall, -0.656 first 10, -0.044 last 10;
- 21 OK completions out of 400; 70 REQUIREMENT_MISS, 66 SQL_EXEC_ERROR,
  47 MISSING_BLOCKS;
- mean loss 0.0259, max mean KL 0.0443.

Held-out rows 451-500:

| Model | Mean reward | OK | Risk acc | Loss acc | Requirement misses |
|---|---:|---:|---:|---:|---:|
| Base | 0.02 | 0.20 | 0.20 | 0.60 | 23 |
| RL checkpoint-50 | 0.165 | 0.20 | 0.20 | 0.64 | 32 |
| RL final (100) | 0.13 | 0.20 | 0.10 | 0.72 | 33 |
| SFT | 1.90 | 1.00 | 0.90 | 0.90 | 0 |

The RL arm removes missing-block failures and slightly reduces SQL execution
errors, but remains far below SFT and worsens requirement misses and risk
calibration. No RL adapter is published; the SFT adapter remains accepted.

Recorded in `projects/project-01-heros-rlvr-studio/RL_BASE_100.md`.


---

## 2026-11-03 - Session 26: shell maintenance and P01 result cleanup

PR #120 (`61f6eec`) closes the P02 shell-script maintenance gap:

- `docs/shell-maintenance.md` inventories all 11 scripts, their controls, known
  gaps, change policy, and migration order;
- `forge/eval-bridge.sh` and `zero-ecosystem/eval-harness/zeval.sh` were added
  to the CI shellcheck list;
- all 11 scripts pass `shellcheck -S warning` locally; CI is 20/20 green.

The SFT model card now explicitly separates the RL probes: RL-from-SFT had 0/10
variance groups, and RL-from-base 100 steps reached 0.13 held-out versus SFT
1.90. No RL adapter is claimed or published.

P02 is complete locally except the npm publication, which requires owner
approval. P01 has an accepted SFT result and documented RL negatives/weak
results; the four-arm ablation is not claimed.

---

## 2026-11-03 - Session 28: P06 #16 verification cross-check; required-document completion

### Context

Resumed from Session 26 (P02 complete locally; npm publish awaits approval).
Live inspection showed that **PR #16** (`0d17672`, `feat(edgeinfer): add paged
attention CPU reference`) had already been merged into `edgeinfer/main` at
14:23 +0530 on 2026-11-03 with CI green (live PR page shows 4/4 checks OK;
the parallel session's log entry records 3/3 — cosmetic discrepancy, noted).
It had no `PROGRESS_LOG.md` entry at the time; the parallel session logged it
separately as "Session 27" while this session was running, so this entry is
numbered Session 28. The required documents `REPOSITORY_STRENGTH_INDEX.md` and
`NEXT_ACTIONS.md` were missing and are created here.

### Tool discovery (Task 1, completed)

| Item | Result |
|---|---|
| Kimi WebBridge daemon | had exited uncleanly; restarted on 127.0.0.1:10086 (v2.0.26; v2.0.32 available, upgrade is user-initiated) |
| GitHub PR #16 | verified live: merged, "4 / 4 checks OK" |
| Mobbin MCP | **not installed** — no `mobbin` tools in catalogue; `list_mcp_resources` returns empty |
| UI Skills | **none** — available skills: browser, kimi-webbridge, opencode, report |
| `gh` CLI | still not installed; live checks used the authenticated Kimi session |
| GPU | RTX 2060 visible to the host (from Session 06); no GPU job run this session |

### Verification of PR #16 (no re-implementation)

| Check | Result |
|---|---|
| `python -m unittest test_paged_attention -v` (edgeinfer/scripts) | **8 tests pass, 0.102 s** |
| Parity round-trip: `generate` 20 synthetic cases, reference used as candidate, `check` | **`ok: true`, 20 compared, 0 failures** |

These verify the harness end-to-end only. **Not claimed:** WGSL kernel,
SmolLM2 token parity, zero-readback trace, memory bound, two-device latency,
any speedup. MHA only; GQA is a follow-up.

### Documents created

- `REPOSITORY_STRENGTH_INDEX.md` — all 30 public repositories scored on the
  brief's eight-category rubric. Eleven elevated repositories are evidence-based
  (`[V]`/`[D]`); the other nineteen are marked `[P]` estimates and must not be
  quoted as measurements. Elevated-set average **61.6**. Includes per-repo
  strongest achievement, weakest area, missing capabilities, priority, effort,
  hiring relevance, and a re-scoring protocol.
- `NEXT_ACTIONS.md` — ranked queue; Section 1 lists the owner-approval blockers
  (npm publish, HF adapter upload, corpus publication, profile pinning,
  collection-description sync); Section 2 is the unblocked engineering queue
  (P06 WGSL kernel first); Section 5 lists explicit non-goals.

### Decisions

- ADR-024 appended: record P06 #16 verification; Mobbin MCP / UI Skills absent;
  required document set now 14/14.

### State

- Required document set: **14/14 present** (was 12).
- P06: CPU reference + parity harness DONE and merged (#16); WGSL kernel not
  started; P06 gate remains open.
- P01: SFT adapter 1.90 held-out, local and unpublished; HF upload blocked on
  token + approval.
- P02: complete locally; `agentic@0.3.0` packed, **not published**.
- No push, publish, upload, deploy, pin, or archive action was taken this
  session. The workspace docs branch is uncommitted pending owner review.

### Next checkpoint

1. Owner reviews the workspace docs diff (RSI + NEXT_ACTIONS + ADR-024 + this
   log) and approves the commit/push of `docs/ai-engineering-portfolio`.
2. Owner decides the three release actions in NEXT_ACTIONS Section 1 (npm,
   HF adapter, corpus) — each needs explicit approval.
3. Engineering (not blocked): start the P06 WGSL kernel behind the parity
   harness on a feature branch; do not claim any speedup before the gates pass.


---

## 2026-11-03 - Session 27: P06 CPU reference and parity harness

EdgeInfer PR #16 (`0d17672`) adds the Python CPU reference required before a
WGSL paged-attention kernel:

- `scripts/paged_attention_reference.py` â€” float32 online softmax over a
  block-table KV cache (`block_size=16`);
- `scripts/paged_attention_parity.py` â€” compares a candidate output to the
  reference (`atol=2e-3`, `rtol=2e-2`), with deterministic synthetic cases;
- `scripts/test_paged_attention.py` â€” **8 tests pass**, covering block
  boundaries, block-table permutation, out-of-range slots, and tolerances;
- CI job `Paged attention reference` runs the Python tests; PR CI = 3/3 green.

This does **not** claim SmolLM2 parity, WebGPU correctness, a zero-readback
trace, memory within 5%, or a two-device speedup. The WGSL kernel remains the
next P06 step and must be gated by this harness.


---

## 2026-11-03 - Session 28: P06 CPU, baseline, and WGSL kernel

Five P06 PRs merged:

- **#16** (`0d17672`): Python float32 paged-attention reference and candidate
  comparison harness.
- **#17** (`8d9e5cc`): Windows test imports use `pathToFileURL`; Node suite
  reaches **113/113**.
- **#18** (`a501d55`): GQA head mapping in the reference and dense baseline.
- **#19** (`96574e7`): 20-prompt SmolLM2-135M-Instruct ORT baseline. The FP16
  ONNX export ran through `onnxruntime-web` CPU with `past_key_values.*` /
  `present.*` across 30 layers; the fixture records 542 generated tokens,
  chosen logits, and top-5 logits. Four validator tests.
- **#20** (`31a2e77`): f32 WGSL paged-attention kernel and browser harness.
  One workgroup per query head, 64 invocations, online softmax, GQA mapping,
  block table, host-reset status word.

Browser evidence: **20/20 synthetic cases pass**, max abs **8.43e-8** on Chrome
156 / NVIDIA Turing (RTX 2060), including MHA and GQA cases. Runtime capability
check: **40/40** KV-sized buffer creations had no `COPY_SRC` or `MAP_READ`.
This is not a validation-layer `mapAsync` trace.

Verification: `npm test` **113/113**, typecheck pass, Python reference **10/10**,
baseline validator **4/4**, `npm run pack:check` pass.

Scope: kernel is f32, opt-in, and not wired into `EdgeInfer.generate()`. No ORT
prompt/logit parity, f16 cache, validation trace, memory check, two-device
benchmark, or speedup claim. The P06 gate remains open.


---

## 2026-11-03 - Session 29: f16 paged-attention KV

PR #21 (`1b00c0a`) moves the WebGPU paged-attention kernel to f16 KV storage
with f32 accumulation:

- WGSL `enable f16`; K/V cache buffers are `array<f16>`;
- host converts `Float32Array` inputs to IEEE-754 half bits and requires
  `shader-f16`;
- fixture reference is generated from the same f16-rounded values;
- browser harness requests `shader-f16`.

Result on Chrome 156 / NVIDIA Turing (RTX 2060): **20/20** synthetic cases
(MHA + GQA), max abs **4.79e-8**, **40/40** KV buffer creations without
`COPY_SRC`/`MAP_READ`.

Verification: `npm test` **113/113**, typecheck pass, Python reference
**10/10**, `npm run pack:check` pass; PR CI 3/3 green.

Still open: SmolLM2 token/logit parity, validation-layer `mapAsync` trace, peak
memory within 5%, two-device p50/p95, Firefox, and a fallback flag. The kernel
is opt-in and not wired into `EdgeInfer.generate()`.

---

## 2026-11-04 - Session 30: live 61-repo reconciliation, real-geometry parity, PR #22

### Live inventory (Kimi browser, authenticated session)
- GitHub profile header: **61 public repositories** (was 30 on 2026-11-03).
  Page 1 = 30, page 2 = 30, page 3 = 1 (`craveai-privacy-policy`).
  Newly visible: `loanflow`, `image2code-bench`, `allrtc`, `syncforge`,
  `ContentForge-AI`, `mobile-native-design-system`, `flux-social`, `aeo_geo`,
  `hostshift`, `swarmcompute`, `vulnhunter`, `meshauth`, `pulsenet`,
  `greybox-codebase-single-file`, `syncplay`, `fieldlens__`, `zeroq`,
  `cybermentor`, `EcoSphere`, `simbook`, `govpass`, `waitless`, `motion-mcp`,
  `surface-karya`, `trimium`, `awesome-zero-server-saas`, `afeedi`, `Nest`,
  `GRC-Tools`, `awesome-security-GRC`, `awesome-compliance`, `vc_idias`.
  Missing from the old baseline: `FREED`, `ridge_shade`, `developer-utilities`,
  `getsmscode-test` (renamed/archived/private until confirmed).
- Hugging Face `itssoumyad`: 11 Spaces, 2 datasets, 0 models, 1 collection
  ("Ten applied AI systems"). Unchanged.
- Kimi bridge: running on 127.0.0.1:10086, v2.0.26 (v2.0.32 available,
  user-initiated upgrade). `gh` still not installed.

### RSI updates (`REPOSITORY_STRENGTH_INDEX.md`)
- Inventory corrected from 30 → 61 public repos; §3 expanded to the 50
  non-elevated repos with metadata [P] rows; vanished baseline rows held
  pending confirmation.
- edgeinfer re-scored **69 → 72 [V]**: evidence now covers #17 (Windows
  `pathToFileURL`, 113/113), #18 (GQA), #19 (20-prompt SmolLM2 ORT baseline),
  #20 (f32 WGSL kernel, 20/20, 8.43e-8), #21 (f16 KV, 20/20, 4.79e-8,
  40/40 buffer-usage clean), plus local `adb3cb9` real-geometry parity.
- Elevated-set average: 61.6 → **61.8**. Portfolio metrics row updated
  (61 public repos; PRs #101–#120, #14, #15, #16–#21, plus `adb3cb9`).

### P06 real-geometry parity (commit `adb3cb9`, branch `feat/p06-wgsl-parity`)
Verified independently in this workspace:
- `npm test`: **113/113 pass** (9536 ms).
- Python suite: **14/14 pass** (0.105 s).
- `node scripts/kv_memory_accounting.mjs`: analytic 2,949,120 vs total
  2,950,080; **overhead 0.033%** — passes the 5% gate.
- CPU oracle re-run: writes 20 reference rows.
- Committed browser result (2026-11-04, Chrome 156, RTX 2060 / NVIDIA
  Turing): **20/20 real-geometry cases, max abs 3.53e-8**, 40/40 KV buffer
  creations without `COPY_SRC`/`MAP_READ`.

### PR #22 — https://github.com/itsoumya-d/edgeinfer/pull/22
- Head: `adb3cb9` (`feat/p06-wgsl-parity`), base `main` (`1b00c0a`).
  8 files, +560/−6. Title: "feat(edgeinfer): add real-geometry
  paged-attention parity". Description records evidence and non-claims.
- CI run [41776945114](https://github.com/itsoumya-d/edgeinfer/actions/runs/41776945114):
  **Status Success, total duration 28 s**. Jobs: "Paged attention
  reference" (4 s), "Build & test (Node 22.x)", "Build & test (Node 24.x)"
  (matrix: 2 jobs completed). Annotations: 3 Node 20 deprecation warnings,
  3 ubuntu-latest notices.
- PR page: "All checks have passed — 4 successful checks", "No conflicts
  with base branch", mergeable automatically. Codex review failed to complete
  (usage limit); CodeRabbit notes repo has <10 stars so no automatic review.

### Still open (P06)
- Full SmolLM2 token/logit decode parity (attention-geometry parity only).
- Validation-layer `mapAsync` trace (zero-readback is a runtime buffer-usage
  check).
- Two-device p50/p95; Firefox; fallback flag wiring into the SDK.
- PR #22 merge awaits owner approval (remote write).

---

## 2026-11-04 - Session 31: peervault Windows benchmark log, PR #15

### Context
PR #22 (edgeinfer) is green and merge-ready; merge awaits owner approval.
This session advanced the next unblocked item: the committed benchmark log
for peervault, the largest `[D]` gap in the highest-scored repo (83 [V]/[D]).

### Environment
- `repos/peervault/sdk`: `npm install` (98 packages) + `npm run build`
  (tsup) — both passed. `node v22.18.0`, Windows 11 Pro, RTX 2060 host.
- `cargo` / `rustc` are **not installed** on this host. The wasm artifact
  `pqc/target/wasm32-unknown-unknown/release/peervault_mlkem768.wasm` was
  absent, so `bench-pqc.mjs` failed with `ENOENT`. It was restored from the
  checked-in base64 payload in `sdk/src/mlkem-wasm.generated.ts`
  (49,446 bytes, `\x00asm` magic; byte-identical to the vendored payload).
  No cargo was invoked.

### Benchmark runs (2026-11-04)
- `node scripts/bench-pqc.mjs` (250 KEM iterations, 50 handshakes):
  - keygen mean 0.085 ms (11,710 ops/s)
  - encapsulate mean 0.086 ms (11,612 ops/s)
  - decapsulate mean 0.083 ms (12,025 ops/s)
  - full handshake mean 2.252 ms (444 ops/s); p50 **2.221 ms**, p95 **2.668 ms**
  - wasm_bytes: 49,446 (matches the checked-in core).
  Compare Apple Silicon (same doc): handshake p50 0.836 ms, p95 1.082 ms.
- `node --expose-gc scripts/bench-streaming-memory.mjs` (sparse-file /
  discarding-sink, 1 GB, 16,384 chunks; not a real WebRTC transfer):
  - sender: baseline 28.22 MB, peak 67.67 MB, delta **39.45 MB**
  - receiver: baseline 53.36 MB, peak 69.45 MB, delta **16.09 MB**
  Compare Apple Silicon: receiver 3.02 MB, sender 77.45 MB. Both runs
  reported; no WebRTC throughput claimed.
- `npm test`: **11 pass / 9 fail** on this host due to a Windows
  `ERR_UNSUPPORTED_ESM_URL_SCHEME` import quirk (absolute paths without
  `file://`), unrelated to the benchmarks. KATs were not re-run (needs cargo).

### Commit and PR
- Branch `feat/peervault-bench-windows`, commit `bc12ede` (docs + 2 JSON
  only; no code, no crypto, no version bump). `sdk/dist/*` churn from the
  local build was discarded.
- PR [#15](https://github.com/itsoumya-d/peervault/pull/15) (opened via
  Kimi browser): "All checks have passed — 4 successful checks", no conflicts,
  mergeable. Body records the numbers, the wasm-restore note, and the
  non-claims. Codex review hit the usage limit (as on edgeinfer #22).

### Files
- `sdk/bench-pqc.local.json`, `sdk/bench-memory.local.json` (raw outputs),
  `docs/pqc-validation.md` (Windows 11 subsection).

### Still open
- PR #15 (peervault) and PR #22 (edgeinfer) merges await owner approval.
- P06 remaining gates; 0 public HF models; npm 0.3.0 publish.

---

## 2026-11-04 - Session 32: P06 failed-ACK/retry prep (unblocked)

### Context
PR #22 (edgeinfer real-geometry parity) and PR #15 (peervault Windows bench)
remain open and green; merges await explicit owner approval and are not
performed here. HF remains 0 public models (needs token + approval); npm
`agentic@0.3.0` publish awaits approval; P06 decode-parity / validation-trace
/ two-device gates need browser/GPU work not claimable from an agent run.

### What this session did (P06 prep, branch `feat/p06-decode-parity-prep`)
Worked only from the existing real-geometry harness already on
`feat/p06-decode-parity-prep`:
- `scripts/smollm2_decode_prep.mjs` (177 lines): loads the 20-prompt ORT
  baseline + real-geometry fixture + committed oracle reference; re-runs the
  CPU online-softmax recurrence over all 20 cases and checks it matches the
  committed reference within `atol=2e-3 / rtol=2e-2`; writes a prep manifest
  mapping each baseline prompt (`prompt-01` … `prompt-20`) to its oracle case
  with `pastLen`, `blockTable`, and baseline token count.
- `scripts/fixtures/smollm2-decode-prep.json` (388 lines): the manifest.
  This is **prep only** — it is not token/logit decode parity, and the kernel
  remains an opt-in building block.

### Verification (this session)
- `node scripts/smollm2_decode_prep.mjs`: `oracleCheck: { ok: true,
  failures: 0, maxAbs: 0 }`; `baseline: { cases: 20, totalTokens: 542 }`
  (matches the committed 20-prompt baseline: 542 generated tokens per
  `docs/wgsl-paged-attention.md`); 20 `promptToCase` rows (`prompt-01` →
  `pastLen 37`, blockTable `[7,6,5,4,3,2,1,0]`, baselineTokens 8).
- `npm test`: **113/113 pass** (9473 ms). Python suite: **14/14 pass**
  (0.104 s).
- Staged only the two new files on `feat/p06-decode-parity-prep`; no merge,
  no submission, no claims.

### Explicit non-claims
- No WGSL decode-parity claim. Full SmolLM2 token/logit decode parity is
  still blocked on chaining the kernel into a decoder and a browser/GPU run.
- No validation-layer `mapAsync` trace; zero-readback remains the runtime
  buffer-usage check.
- No two-device p50/p95; no Firefox; no fallback wiring; no speedup.
- No merge of PR #22/#15; no HF upload; no npm publish.

### Next checkpoint
1. Owner decides on merging PR #22 (edgeinfer) and PR #15 (peervault).
2. Owner provides HF token + approval for the P01 SFT adapter upload, and
   npm approval for `agentic@0.3.0`.
3. Decode parity proper (browser/GPU) when the owner is at the machine.

---

## 2026-11-04 - Session 33: AGENTS.md spec adoption, ledger, tooling audit

### Context
The owner supplied a workspace engineering / portfolio / global career
specification (`AGENTS.md`): public repos only (`itsoumya-d`), visa or
100%-remote-from-India gate, per-country salary floors, Gmail pre-flight
check, skill-gap prototypes, Revo CV generation, and the five-stage
sequential pipeline. Owner choices this session: (1) Gmail MCP absent →
create the ledger now, owner supplies Gmail export/connection, then source
roles; (2) keep the ADR-008 approval gate — prepare locally, no push/merge/
publish without explicit approval; (3) Global Remote first.

### Tooling audit (verified this session)
- Gmail MCP: **absent** — no Gmail tools in the catalogue, empty MCP
  resource list. The Air New Zealand Rule cannot be executed until Gmail is
  connected or the owner provides an export.
- Mobbin MCP / UI Skills: absent (already recorded in ADR-024).
- `websearch` tool: returns "No search results found" for every query this
  session (job-board sourcing via search is unavailable; browser/WebBridge
  or direct fetches are the fallback).
- `pandoc` and `revo` binaries: not on PATH (the Revo CV pipeline cannot be
  run until installed/located).
- `gh` CLI: still not installed; `git` credential flow + browser used instead
  (as before).

### Files created / updated (local only, uncommitted)
- `AI_ENGINEERING_PORTFOLIO/APPLIED_JOBS_AND_VISA_LEDGER.md` (new): the
  duplicate/rejection firewall and the seven-step pre-flight procedure,
  including the Air New Zealand entry (rejected for lacking local work
  permission — brief-sourced, not yet Gmail-verified).
- This entry; a `NEXT_ACTIONS.md` Stage-1 entry (see below).

### Live state correction (GitHub API, unauthenticated, 2026-11-04)
- `itsoumya-d` profile reports **63 public repositories** (not 61 in the
  Session 30 count, not 30 in the 2026-11-02 audit). Two new public repos
  since the RSI update: `dotnet-enterprise-api` and `default-project`.
  RSI `§1` and the `README.md` fact table still say 61/30 — flagged in
  `NEXT_ACTIONS.md` §3 for the next edit; this entry does not edit those
  numbers without a full RSI re-count.
- Newest pushed public prototypes (push order): `autopilot-fde` (2026-10-29),
  `llm-control-plane` (2026-11-04 08:58Z), `RouteLLM-Gateway`,
  `GraphRAG-CodeAudit`, `loanflow`, `edgeinfer` — all public, all cited by
  URL only. No private repo was accessed.

### Verification (this session)
- HEROS `rlvr` suite (system Python, no torch): **95 tests, 82 pass, 13
  skip** — matches the recorded `82 pass + 13 skip without torch`.
- Workspace `git status`: docs branch `docs/ai-engineering-portfolio`,
  ahead-behind clean; uncommitted diffs are the Session 30–32 RSI/PROGRESS
  edits (already on disk before this session).
- `repos/` state unchanged: HEROS clean `main`, peervault on
  `feat/peervault-bench-windows`, edgeinfer on
  `feat/p06-decode-parity-prep` with the two decode-prep files staged. No
  new remote write was made; approval gate held.

### Explicit non-claims
- No job sourced, no application made, no CV generated, no prototype pushed.
  Stage 1 (Gmail audit → role selection) is blocked on the owner's Gmail
  export/connection; Stage 2–4 cannot start without a JD to target.
- The ledger's Air New Zealand row is brief-sourced, not Gmail-verified.

### Next checkpoint
1. Owner provides Gmail access (MCP connection or an export of past
   applications) → populate the ledger, dedupe, then source Global Remote
   roles against the $65k floor.
2. Owner decides on merging edgeinfer PR #22 and peervault PR #15 (still
   green, still unmerged).
3. Owner provides HF token + approval for the P01 SFT adapter upload, and
   npm approval for `agentic@0.3.0`.

---

## 2026-11-04 - Session 34: inventory count 63, llm-control-plane deep-dive, metrics hardening

### Inventory count corrected (verified)
- Unauthenticated GitHub API `/users/itsoumya-d` on 2026-11-04:
  `public_repos: 63`, `followers: 6`. The 2026-11-04 browser count of 61
  missed `dotnet-enterprise-api` and `default-project` (both public, both
  pushed 2026-11-04).
- `README.md` fact row and `REPOSITORY_STRENGTH_INDEX.md` §1/§4 now say 63,
  with both evidence dates retained. No private repository was read or
  modified; every API/read/clone used public endpoints only.

### llm-control-plane — first deep-dive outside the elevated eleven
Public repo cloned shallowly to `repos/llm-control-plane`. Python 3.11.13;
isolated venv at `%TEMP%\opencode\llm-cp-venv` (pytest, ruff, pytest-cov,
fastapi, httpx installed with `uv pip`). Baseline:
- `pytest`: **54 passed** (3.44 s); warning: Starlette `httpx` deprecation only.
- `pytest --cov`: **94%** statements (1005 stmts, 61 missed), above the CI
  gate of 90%.
- `ruff check .`: clean.
- CI inspected: matrix 3.9/3.11/3.12, ruff, coverage gate, compileall, and a
  package-build job. Core is dependency-free; FastAPI is optional.

### Prepared change — Prometheus exposition hardening (local only)
Branch `feat/metrics-label-escaping`, commit **`8d958c7`** (not pushed):
- `llm_control_plane/metrics.py`: `_escape_label_value` escapes `\\`, `"`,
  and `\n`; `_validate_metric_name` enforces
  `[a-zA-Z_:][a-zA-Z0-9_:]*`; label keys are validated against
  `[a-zA-Z_][a-zA-Z0-9_]*`.
- `tests/test_metrics.py` (new, 7 tests): quote/backslash/newline escaping,
  injection payload stays on one line, invalid metric name, invalid label
  name, observation `_count`/`_sum`/`_p50`/`_p95`, merge semantics, empty
  registry.
- Why it matters: a tenant id or model name containing a quote/newline could
  corrupt the `/metrics` payload or inject samples. This is a real
  production-readiness defect, not a cosmetic test count.

### Verification after the change
| Command | Result |
|---|---|
| `pytest -p no:cacheprovider` | **61 passed** (2.70 s) |
| `pytest --cov=llm_control_plane` | **95%** (1018 stmts, 50 missed); metrics.py 95% |
| `ruff check .` | **All checks passed** |
| `git log -1` | `8d958c7 fix(metrics): escape Prometheus label values and validate names` |

### RSI update
- `REPOSITORY_STRENGTH_INDEX.md` gains §2b: **llm-control-plane 75** —
  [V] on tests/CI/coverage, [P] on the subjective categories. §3 row changed
  from 45 [P] to 75 [V] tests/CI with the prepared-fix note. Portfolio
  metrics now report 63 public repos, 11 elevated + 1 verified deep-dive.
- No score was raised for an unmerged change; the 75 describes the tested
  baseline, and the prepared branch is listed separately.

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy. `feat/metrics-label-escaping`
  exists only in `repos/llm-control-plane` on this machine.
- No job sourced and no application made; Gmail remains the Stage-1 blocker.
- The 75 is a rubric score, not a benchmark or an external validation.

### Next checkpoint
1. Owner reviews `8d958c7`; on approval, push the branch and open a PR.
2. Owner provides Gmail export/access → Stage 1 role sourcing.
3. Owner decides on edgeinfer PR #22 / peervault PR #15 and the HF/npm gates.

---

## 2026-11-04 - Session 35: autopilot-fde deep-dive, two prepared fixes, paper claim audit

### Environment
- Clone `repos/autopilot-fde` (public, depth 1, `main` at `72652a6`).
- Isolated venv `%TEMP%\opencode\fde-venv` (Python 3.12; backend requirements +
  pytest, pytest-cov, ruff via `uv pip`). Node 22.18.0 available; frontend
  suite not run this session.

### Baseline and findings
The repo was carried in RSI §3 as a **35 [P]** "no action" row. That estimate
was wrong by a wide margin. Verified locally:
- **436 passed, 1 skipped, 154 subtests** (11.45 s) after the portability fix;
  before it, **2 failed** on Windows.
- **100% statement coverage** of `backend` (3,473 statements) against a CI gate
  of 100%.
- `ruff check backend/ tests/ scripts/`: clean.
- CI inspected: Python 3.12/3.13/3.14, a separate real-LangGraph runtime job,
  and frontend lint/vitest/typecheck/build. 34 backend test files; 19 frontend
  test files.
- Module surface: ingestion (Slack/IMAP/WhatsApp), deterministic discovery +
  OCEL export, APS scoring with Monte Carlo, approval-gated LangGraph codegen,
  MCP HTTP/server, cost attribution, PII scrubbing, Docker.

### Prepared fix 1 — Windows portability (`fix/windows-portability`, `bccb8c3`)
- `tests/test_units.py`: `assertIn("runs/training", str(path))` →
  `path.as_posix()`. On Windows the path uses `\`, so the assertion failed.
- `tests/test_publish_workflow.py`: the test shells out to `bash`/`sh` and
  requires `jq`; it now skips unless `os.name != "nt"` and both binaries exist.
  CI (Ubuntu, jq preinstalled) still executes it. This is a skip, not a
  weakened assertion.
- Not pushed; owner approval required.

### Prepared fix 2 — paper claim scope (`fix/paper-synthetic-claims`, `265c25e`)
A credibility finding, not a code bug. `paper/main.tex` said:
- "the **first** system that **autonomously** performs the role of a Forward
  Deployed Engineer";
- "**empirical evaluation** across 8 **enterprise departments** and 158
  multi-turn interaction traces";
- "7 **verified** business processes";
- "zero unsupervised critical **safety violations**".

The README explicitly says the scenarios are fictional and the scores are model
outputs, not measured customer outcomes; `backend/demo_data.py` is fixture data
("8 business departments and 250+ events"). The table also lists 7 processes
and 36 traces, not 158. Under ADR-006 this is an unsupported claim set.

The prepared commit:
- labels the section **"Synthetic Benchmark Evaluation"** and adds a
  no-customer-data / simulator-output statement;
- removes "first", "autonomously", "verified", and the unsupported 158 count;
- scopes "zero critical violations" to "in simulation";
- softens the conclusion to a reviewable reference architecture with production
  validation as future work.

This is a **draft correction for owner review**; the paper's arguments and
formal definitions are unchanged. Research credibility is scored 4/10 until the
correction is accepted (≈6 after).

### Correction — README encoding
The README's apparent `�` characters are a **Windows console rendering
artifact**, not file corruption. Direct byte inspection (`read_bytes()` +
SHA-256 vs `git cat-file -p HEAD:README.md`) shows byte-identical valid UTF-8
containing `·` and `×`. A rewrite attempt was reverted via
`git checkout -- README.md`; no README change was committed. Workspace items
that assumed real encoding damage should verify bytes before editing.

### RSI update
- §2b now covers two verified deep-dives: **autopilot-fde 84** and
  **llm-control-plane 75**.
- §3 row changed from 35 [P] "no action" to 84 [V] tests/CI with both prepared
  branches noted.
- Portfolio metrics: 63 public repos, 11 elevated + 2 verified deep-dives.
- No score was raised for an unmerged change; the 84 reflects the tested
  baseline, with research at 4 pending the paper correction.

### Verification commands (all local)
| Command | Result |
|---|---|
| `pytest tests/ --ignore=tests/runtime` on `fix/windows-portability` (before fix) | 2 failed |
| same on `fix/windows-portability` (after fix) | **436 passed, 1 skipped, 154 subtests** |
| same on `fix/paper-synthetic-claims` | 2 failed (branch is based on `main`; it does not contain the portability fix — CI on Ubuntu is unaffected) |
| `pytest ... --cov=backend` on `fix/windows-portability` | **100%** (3,473 stmts, 0 missed) |
| `ruff check backend/ tests/ scripts/` | **All checks passed** |
| `git log -1` (portability branch) | `bccb8c3` |
| `git log -1` (paper branch) | `265c25e` |

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- The frontend lint/test/typecheck/build jobs were **not** re-run locally; the
  claim is that CI defines them, not that they passed here.
- Runtime (`tests/runtime/`) was not executed locally (needs the LangGraph
  extra).
- No judgement is made here about the paper's author affiliation or email.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner reviews `bccb8c3` and `265c25e`; on approval, push and open PRs.
2. Owner provides Gmail export/access → Stage 1 role sourcing.
3. Owner decides on edgeinfer PR #22 / peervault PR #15 and the HF/npm gates.

---

## 2026-11-04 - Session 36: RouteLLM-Gateway [D]→[V], reproducible Pareto artifact

### What was verified
`repos/RouteLLM-Gateway` fast-forwarded to `92083c8` (public `main`; PR #1,
HTTP provider). Local Windows 11 / Node 22.18.0:
- `npm test`: **16/16 pass** at baseline.
- `npm run evaluate`: reproduced the committed RESULTS table **exactly** —
  always-strong 98.80% / $0.5000; always-weak 86.80% / $0.0500; router 97.20% /
  $0.1868; router+cache 97.20% / $0.1530; cache hit 13.6%; threshold 0.74;
  retention 98.38%; cost reduction 69.40%.
- This is the first time the RouteLLM benchmark has been reproduced in this
  workspace; the repo moves from `[D]` to `[V]/[D]` (mocks, not a real-model
  benchmark) and 62 → **66**.

### Finding — committed artifact was not byte-stable
Running `npm run evaluate` left `results/pareto.json` dirty on every run:
two float values changed in the last digit (`0.07750784705788455` →
`...52`, `-0.009595645288350907` → `...893`) from platform accumulation order.
The metrics table was unaffected, but a reviewer would see an unexplained diff
after a "reproducible" run.

### Prepared change — `feat/reproducible-pareto`, `d86f178` (not pushed)
- `src/canonical.js`: `canonicalize()` recurses through arrays/objects and
  rounds non-integer finite numbers to 12 decimals; integers, booleans, null,
  and non-finite values pass through.
- `scripts/evaluate.mjs`: writes `JSON.stringify(canonicalize(result), null,
  2)` instead of the raw result.
- `test/canonical.test.mjs` (3 tests): last-digit drift collapses to one value,
  integers/non-finite/structure preserved, input not mutated.
- `RESULTS.md`: adds a Windows 11 reproduction section with the exact metrics
  and the float-drift note.
- `README.md`: test count 16 → 19 and mentions canonical JSON rounding.

### Verification
| Command | Result |
|---|---|
| `npm test` (baseline) | 16/16 pass |
| `npm test` (after change) | **19/19 pass** (298 ms) |
| `npm run evaluate` run 1 | SHA-256 `424cc3e3…` |
| `npm run evaluate` run 2 | SHA-256 `424cc3e3…` (identical) |
| `git log -1` | `d86f178` |

The two-run equality is same-host determinism. Cross-platform byte equality is
argued from the 12-decimal rounding, not measured on a second OS.

### RSI correction
While updating the RouteLLM row, the elevated-set average was found to be
wrong: the table sums to **711/11 = 64.6**, not the stated **61.8**. Corrected
to **65.0** after RouteLLM 62→66 (715/11). This is an arithmetic correction,
not a new measurement.

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- The benchmark still uses deterministic mock providers; no real model/API was
  called.
- No claim of cross-platform byte equality from measurement; only same-host
  determinism was measured.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner reviews `d86f178`; on approval, push and open a PR.
2. Owner reviews the three autopilot-fde/llm-control-plane branches.
3. Owner provides Gmail export/access → Stage 1 role sourcing.

---

## 2026-11-04 - Session 37: GraphRAG-CodeAudit [D]→[V], portable eval artifact

### What was verified
`repos/GraphRAG-CodeAudit` fast-forwarded to `f5677e3` (public `main`, new
tree-sitter TS/JS extraction and `scripts/audit_repo.py`). Local Windows 11 /
Python 3.11.13:
- Initial run without tree-sitter: 16 passed, 6 errors (the new TS suite
  requires the optional parsers). Installed
  `tree-sitter>=0.25,<0.27`, `tree-sitter-javascript`, `tree-sitter-typescript`
  into the existing venv.
- After install: **22/22 pass** (1.31 s). After the local fix: **24/24**.
- `python scripts/evaluate.py` reproduced the committed table exactly:
  GraphRAG **7.58** vs flat **7.07**, comprehension 8.58/8.58, diversity
  10.00/10.00, empowerment 4.01/2.28, directness 7.72/7.40, head-to-head
  **64/100 (64.0%)**. GraphRAG moves from `[D]` to `[V]/[D]` and 59 → **63**.

### Finding — committed artifact embedded a machine-specific path
`experiments/eval_results.json` stored
`/Users/soumyadebnath16/Developer/Shado/repos/.../data/sample_repo`, so any run
on another machine changed the file. The metrics were identical; only the path
differed.

### Prepared change — `fix/reproducible-eval-label`, `c9b51e7` (not pushed)
- `graphrag_audit/eval.py`: adds `repo_label(repo_path, root)` (POSIX relative
  label when the repo is under the project root, absolute otherwise) and
  `run_evaluation(..., label=None)` records it.
- `scripts/evaluate.py`: passes `repo_label(args.repo, ROOT)`.
- `tests/test_eval.py`: +2 tests (relative label, outside-root absolute;
  evaluation records the supplied label).
- `experiments/eval_results.json`: `repo` becomes `data/sample_repo`; two
  consecutive runs are byte-identical.
- `RESULTS.md`: tests 15 → 24 and a Windows reproduction section.

### Verification
| Command | Result |
|---|---|
| `pytest` before deps | 16 passed, 6 errors |
| `pytest` after parser install | 22 passed |
| `pytest` after fix | **24 passed** (0.16 s) |
| `python scripts/evaluate.py` | table reproduced exactly |
| `git log -1` | `c9b51e7` |
| artifact | `repo: data/sample_repo`; stable across runs |

### RSI correction
Elevated-set sum is now **719/11 = 65.4** (RouteLLM 66 + GraphRAG 63). The
pre-change table summed to 64.6, not the previously stated 61.8. This is
recorded as an arithmetic correction, not a new measurement.

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- The judge is a deterministic rubric, not an LLM; the corpus is a 5-file
  synthetic repo; Leiden is not installed (`louvain-fallback`).
- No coverage gate exists in this repo; the local 88% figure is informational.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner reviews `c9b51e7`; on approval, push and open a PR.
2. Owner reviews `d86f178`, `8d958c7`, `bccb8c3`, `265c25e`.
3. Owner provides Gmail export/access → Stage 1 role sourcing.

---

## 2026-11-04 - Session 38: Reflexion-SWE and HEROS-Firewall verified

### Reflexion-SWE — 61 [D] → 64 [V]/[D]
Public `main` was already current. Local Windows 11 / Python 3.11.13:
- `pytest`: **37 passed, 3 skipped** in 5.23 s. The 3 skips are the Rust
  sandbox tests (`rustc` is not installed); 37 + 3 = 40, matching `RESULTS.md`.
- `python scripts/run_ablation.py` reproduced the mechanism table **exactly**:
  base/no_testgen 0.000 pass@1 (1.00 attempts, 0.167 score), no_reflection
  0.000 (3.00 attempts), full 1.000 (2.00 attempts), tf_grpo 1.000 (1.00
  attempts), 6 priors from 24 rollouts.
- `experiments/toy_ablation.json` was **already byte-stable** after the run
  (`git status` clean), so no code change was needed and no branch was
  prepared. This is the first repo in the sweep with nothing to fix.

### HEROS-Firewall — 70 [D] → 72 [V]/[D]
- `npm test`: **16/16 pass** in 167 ms.
- `npm run redteam`: **FNR 0/1,000**, **FPR 0/200** exactly; policy p99
  **0.230 ms** (macOS reference 0.103 ms — machine difference), total 27.68 ms.
- The committed `results/redteam.json` changed only in `p99_ms`/`total_ms`,
  which are machine-dependent. The historical macOS artifact was left intact.

### Prepared change — `docs/windows-redteam-run`, `e0e8579` (not pushed)
- Adds `results/redteam-windows.json` (raw Windows output) rather than
  overwriting the macOS artifact.
- Adds a Windows reproduction section to `RESULTS.md` with the FNR/FPR/p99
  numbers and the same policy-layer-only caveat.

### RSI update
- Reflexion-SWE 61 → **64** (testing +2, docs +1).
- HEROS-Firewall 70 → **72** (testing +1, docs +1).
- Elevated-set average: **724/11 = 65.8** (was 65.4; the historical 61.8 was an
  arithmetic error, pre-change true sum 64.6).

### Verification commands (all local)
| Command | Result |
|---|---|
| `pytest` (Reflexion-SWE) | 37 passed, 3 skipped |
| `python scripts/run_ablation.py` | table reproduced; artifact clean |
| `npm test` (HEROS-Firewall) | 16/16 pass |
| `npm run redteam` | FNR 0, FPR 0, p99 0.230 ms |
| `git log -1` (HEROS-Firewall) | `e0e8579` |

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- Reflexion's model-dependent Pass@1 / SWE-bench Lite / HumanEval numbers are
  **not** reproduced and are not claimed.
- HEROS-Firewall p99 excludes process spawn, downstream MCP, and network time.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner reviews `e0e8579`; on approval, push and open a PR.
2. Owner reviews the five other prepared branches.
3. Owner provides Gmail export/access → Stage 1 role sourcing.

---

## 2026-11-04 - Session 39: Cloud-SaaS and Mobbin verified; PerfBench blocked by toolchain

### HEROS-Cloud-SaaS — 47 [D] → 50 [V]/[D]
- `pytest`: **6/6 pass** in 0.65 s.
- `python scripts/evaluate.py` reproduced the PLLB table exactly: completion
  **0.7000 → 1.0000** (**+30.00 pp**), receipt coverage 1.0/1.0, policy
  applications 0/20, 4 drafts, 4 approved.
- Only timings differ (`mean_ms` 0.038/0.032 vs macOS 0.030/0.017).
- **Prepared locally (not pushed):** branch `docs/windows-eval-run`, commit
  **`0096a7d`** — adds `results/eval-windows.json` and a Windows reproduction
  section; the macOS artifact stays intact.

### Mobbin-UI-Compiler — 45 [D] → 48 [V]/[D]
- `npm test`: **10/10 pass** in 137 ms.
- `node bin/mobbin-compile.mjs --surface all` regenerated all five surfaces.
  Every generated file is **byte-identical to HEAD** (SHA-256 + `git cat-file`
  comparison); the count/app list matches `RESULTS.md` (KYC 2, paywall 2,
  dashboard 5, chat 2, billing 1).
- No change needed; no branch prepared. The apparent dirty tree after
  regeneration is Git's CRLF stat cache, not content drift.

### Anthropic-PerfBench — 56 [D], not re-runnable here
- The host has **no C compiler** (`cc`/`gcc`/`clang`), **no `make`**, and
  **no `cargo`/`rustc`**.
- The native results are Apple-Silicon NEON; the WASM path needs the Rust
  toolchain. `make test`, `make bench`, and `make wasm-test` cannot run.
- Score unchanged; the native/WASM numbers remain `[D]`. This is a toolchain
  limitation, not a repo failure.

### RSI update
| Repo | Before | After |
|---|---:|---:|
| HEROS-Cloud-SaaS | 47 [D] | **50 [V]/[D]** |
| Mobbin-UI-Compiler | 45 [D] | **48 [V]/[D]** |
| Anthropic-PerfBench | 56 [D] | 56 [D] (blocked) |
| Elevated average | 65.8 | **66.4** (730/11) |

### Verification commands (all local)
| Command | Result |
|---|---|
| `pytest` (Cloud-SaaS) | 6 passed |
| `python scripts/evaluate.py` (Cloud-SaaS) | table reproduced exactly |
| `npm test` (Mobbin) | 10/10 pass |
| `node bin/mobbin-compile.mjs --surface all` | 5 surfaces; byte-identical output |
| toolchain probe | cc/gcc/clang/make/cargo/rustc all missing |

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- Anthropic-PerfBench's native and WASM numbers were **not** reproduced.
- Cloud-SaaS is still a deterministic simulation, not a customer deployment.
- Mobbin still uses the fixture adapter; no live Mobbin MCP, no browser audit.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner reviews `0096a7d`; on approval, push and open a PR.
2. Owner reviews the six other prepared branches.
3. Owner provides Gmail export/access → Stage 1 role sourcing.
4. Optional: install a C/Rust toolchain to unblock PerfBench verification.

---

## 2026-11-04 - Session 40: live PR/HF reconciliation — peervault #15 merged

### Hugging Face estate (public API)
| Kind | Count | Evidence |
|---|---:|---|
| Spaces | **11** | `huggingface.co/api/spaces?author=itssoumyad` |
| Datasets | **2** | `heros-migration-500`, `graphrag-questions-100` |
| Models | **0** | `huggingface.co/api/models?author=itssoumyad` |

Matches the recorded estate; no upload was made. The 11 Spaces are `heros-rl`,
`reflexion-swe`, `graphrag-codeaudit`, `portfolio`, `edgeinfer-v2`,
`peervault-pqc`, `heros-firewall`, `anthropic-perfbench`, `routellm-gateway`,
`mobbin-ui-compiler`, `heros-cloud-saas`.

### Pull-request state correction
The workspace still said peervault #15 awaited approval. Live GitHub API:
- **peervault #15 merged** 2026-11-04T12:25:14Z at `e22fb7f3`; 6/6 checks green
  (SDK Node 22/24, Go relay, build, deploy).
- **edgeinfer #23 merged** 2026-11-04T11:02:31Z at `89881a9` ("ci: enforce a
  coverage floor"); 6/6 checks green.
- **RouteLLM-Gateway #1 merged** 2026-11-04T10:39:45Z at `92083c8` (HTTP
  provider adapter).
- **edgeinfer #22 remains open** (`adb3cb9`); merge awaits owner approval.

### Updates
- `README.md` §4: added the three merged PRs and the note that #22 is open.
- `NEXT_ACTIONS.md`: peervault benchmark item marked done; RSI 83 → 84.
- `REPOSITORY_STRENGTH_INDEX.md`: peervault 84 (docs +1 for the merged,
  verified benchmark log); elevated average **66.5** (731/11).

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy this session.
- peervault's NIST KATs were not re-run (no `cargo` on this host); the
  `[D]` part of its score remains.
- No job sourced; Gmail remains the Stage-1 blocker.

### Next checkpoint
1. Owner decides on edgeinfer #22 (open, green).
2. Owner reviews the seven prepared local branches.
3. Owner provides Gmail export/access → Stage 1 role sourcing.

---

## 2026-11-09 - Session 41: branch/PR re-verify; no new code changes

### Prepared-branch re-verification (all local, clean)
| Repo | Branch | HEAD | Status |
|---|---|---|---|
| `llm-control-plane` | `feat/metrics-label-escaping` | `8d958c7` | clean |
| `autopilot-fde` | `fix/windows-portability` | `bccb8c3` | clean |
| `autopilot-fde` | `fix/paper-synthetic-claims` (separate, priority) | `265c25e` | clean |
| `RouteLLM-Gateway` | `feat/reproducible-pareto` | `d86f178` | clean |
| `GraphRAG-CodeAudit` | `fix/reproducible-eval-label` | `c9b51e7` | clean |
| `HEROS-Firewall` | `docs/windows-redteam-run` | `e0e8579` | clean |
| `HEROS-Cloud-SaaS` | `docs/windows-eval-run` | `0096a7d` | clean |

`autopilot-fde` is currently checked out on `fix/windows-portability`; the
paper-scope fix `265c25e` remains on its own branch from `main` (does not
include `bccb8c3`) and is the higher-priority review item.

### Live PR state (GitHub API, read-only)
- **edgeinfer #22** `feat(edgeinfer): add real-geometry paged-attention parity`
  (`adb3cb9`, base `main`): **open, not merged**, mergeable state unknown via
  API — owner decision still pending.
- Open PR search for `author:itsoumya-d` reports 434 results total; the bulk
  are `Yc_ai` bot-generated PRs unrelated to this portfolio program. Only
  edgeinfer #22 is in-scope.

### Quick re-verification
| Command | Result |
|---|---|
| `npm test` (HEROS, `main`) | **54 tests, 54 pass, 0 fail** |
| HEROS-RL `pytest` | not re-run (no `pytest` in available Python envs this session) |
| Anthropic-PerfBench | still blocked (no C compiler/make/cargo/rustc on host) |

### RSI
No score changes. Elevated average remains **66.5** (731/11); 10/11 elevated
repos have locally verified evidence.

### Explicit non-claims
- No push, PR, merge, publish, upload, or deploy.
- No job sourced/applied; Gmail MCP/export still required for Stage 1 pre-flight.
- HEROS-RL and PerfBench results are carried forward from prior evidence, not
  re-run this session.

### Next checkpoint
1. Owner decides on edgeinfer #22 (open).
2. Owner reviews the seven prepared local branches (`265c25e` paper scope first).
3. Owner provides Gmail export/access → Stage 1 Global Remote role sourcing.

