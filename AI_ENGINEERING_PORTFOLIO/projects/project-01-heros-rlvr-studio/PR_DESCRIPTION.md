# PR #101 — feat(rlvr): deterministic SQLite shadow verifier + Dr.GRPO/DAPO loss engine

**Status:** **merged** into `main` at `8a7951d` (squash merge); CI was 18/18 green.
**Live PR:** https://github.com/itsoumya-d/HEROS/pull/101
**Repository:** `itsoumya-d/HEROS`
**Base:** `main` at `5b8536b`
**Branch:** `feat/rlvr-dr-grpo-gpu-trainer` (deleted after merge)
**Commit:** `f49a6c1`
**Patch:** `AI_ENGINEERING_PORTFOLIO/open_source/patches/0001-feat-rlvr-add-deterministic-SQLite-shadow-verifier-a.patch`
**Diff size:** 7 files, +869 / −4

**Follow-up:** the P5 QLoRA runner merged as
[#103](https://github.com/itsoumya-d/HEROS/pull/103) at `d3588ca` (head
`0ac89ff`). See [`PR_DESCRIPTION_P5.md`](PR_DESCRIPTION_P5.md). This packet's
51-test log is the #101 commit; the runner merge has 78 tests.

---

## 1. Problem

HEROS-RL already has a critic-free GRPO engine, a 500-case migration dataset, and
TRL/Unsloth entry points. HEROS `rlvr` already has pure-Python advantages, losses,
dynamic sampling, and a `CommandVerifier` adapter. What is missing is the piece
that makes migration training *verifiable*:

- a reward that executes the proposed migration against seeded rows and measures
  data loss, instead of asking a text judge;
- a differentiable Dr.GRPO + DAPO loss that the QLoRA runner can call;
- a CPU CI job that exercises the reward and loss on every push.

This PR adds that slice. It does **not** add a QLoRA runner, a training run, a
checkpoint, or a benchmark number.

---

## 2. Changes

| File | Change | Why |
|---|---|---|
| `rlvr/src/heros_rlvr/gpu_trainer.py` | New: `MigrationTask`, `VerificationReceipt`, `DeterministicForgeShadowVerifier`, `DapoDynamicSampler`, `compute_dr_grpo_token_loss` | The reward and loss core |
| `rlvr/tests/test_gpu_rlvr_pipeline.py` | New: 17 tests | Pin the reward contract, authorizer, tensor math, and CPU/tensor parity |
| `rlvr/src/heros_rlvr/__init__.py` | Exports the new symbols | Public API |
| `rlvr/pyproject.toml` | `gpu = ["torch>=2.4"]` extra | Torch stays optional |
| `.github/workflows/rlvr.yml` | New `gpu-trainer-cpu` job | Runs the new tests with CPU torch |
| `rlvr/README.md` | Reward table, delegation note, limitations, benchmark link | Reviewer-facing contract |
| `rlvr/BENCHMARKS.md` | New: measurement protocol and gates | Fixes the README's previously broken link; no results claimed |

### 2.1 Verifier behavior

A completion must contain `<think>`, `<sql_migration>`, and
`<forge_manifest>`. The verifier:

1. Parses the three blocks and fails closed if any is missing.
2. Rejects a manifest that is not a JSON object before executing SQL.
3. Opens a fresh `:memory:` SQLite connection with an authorizer that denies
   `ATTACH`, `DETACH`, `PRAGMA writable_schema`, and `load_extension`.
4. Applies the task DDL and seed rows.
5. Snapshots table counts, applies the migration, snapshots again.
6. Scores format (`0.25`), execution (`0.75`), and calibration (`1.00`).
7. Applies a `0.40` miracle-step penalty for destructive claims with fewer than
   20 characters of reasoning.
8. Returns an immutable `VerificationReceipt` with `shadow_row_loss_detected` and
   an error code.

Maximum reward is `2.00`. Missing blocks return `-1.00`; invalid JSON or a SQL
error returns `-0.50`.

### 2.2 Loss behavior

`compute_dr_grpo_token_loss` implements:

- centered advantages with no standard-deviation division (Dr.GRPO);
- DAPO asymmetric clipping at `0.2` / `0.28`;
- the k3 KL estimator `exp(ref − policy) − (ref − policy) − 1`;
- the constant-horizon reduction `sum(tokens) / (G * L_max)`.

### 2.3 De-duplication

`DapoDynamicSampler` delegates to the existing
`sampling.has_learning_signal` and `advantages.dr_grpo_advantages` functions
rather than reimplementing them. Two new parity tests pin the tensor
advantage path to `dr_grpo_advantages` and the tensor loss to `grpo_loss`
(`length_normalization="none"`, scaled by `L_max`). This answers the obvious
review question: why are there two implementations?

The pure-Python functions remain the reference for CPU analysis. The tensor
functions exist because `grpo_loss` cannot backpropagate. The parity tests make
drift a CI failure.

---

## 3. Test plan

```powershell
# From the HEROS repository root
$env:PYTHONPATH = "rlvr/src"

# With CPU torch
& "$env:TEMP\opencode\heros-venv\Scripts\python.exe" -m unittest discover -s rlvr/tests -v

# Without torch (system Python)
python -m unittest discover -s rlvr/tests
```

### Result with torch

```text
Ran 51 tests in 0.383s
OK
```

### Result without torch

```text
Ran 51 tests in 0.471s
OK (skipped=7)
```

The seven skips are tensor-only: advantages, two parity checks, length bias,
constant horizon, shape validation, and invalid horizon.

### What the tests cover

| Area | Cases |
|---|---|
| Shadow verifier | safe max reward, destructive loss + penalty, missing blocks, invalid JSON, non-object manifest, broken SQL, denied `ATTACH`, understated manifest |
| Dynamic sampling | zero-variance rejection, mixed group, zero-mean advantages, CPU/tensor parity |
| Loss | length-bias equality at `kl_beta=0`, constant-horizon scaling, CPU/tensor parity, shape mismatch, invalid horizon |

No test asserts model quality. No test requires a GPU.

---

## 4. Benchmark delta

**None.** This PR does not claim a training result, a speedup, or an accuracy
change. `rlvr/BENCHMARKS.md` defines the four-arm ablation and the metadata that
a future result must include. A run without `run.json` is not a result.

---

## 5. Security review

| Concern | Control |
|---|---|
| Model-authored `ATTACH` / file access | authorizer denies `ATTACH` and `DETACH` |
| Schema corruption | authorizer denies `PRAGMA writable_schema` |
| Native extension loading | authorizer denies `load_extension` |
| State leakage between rollouts | fresh `:memory:` database per call |
| Partial migration on error | ephemeral DB is closed; no reuse |
| Malformed manifest probing SQL | JSON object validated before execution |

Residual risks, documented in the README and code:

- No statement timeout or memory cap. A recursive CTE can stall a worker.
- Row counts only; delete-and-reinsert with the same count is invisible.
- A table rename is a false-positive loss.
- A no-op migration can score `2.00` on a safe task; requirement satisfaction is
  not checked.
- The authorizer is a guardrail, not a sandbox. Production use needs process
  isolation.

The PR does not claim otherwise.

---

## 6. Compatibility and risk

- **Torch is optional.** The package imports without torch; the verifier is
  stdlib-only. The `gpu` extra is additive.
- **No existing API changed.** The new symbols are additive exports.
- **No dependency version bump** beyond the optional `torch>=2.4`.
- **CI cost:** the new job installs CPU torch on `ubuntu-22.04`, timeout 20
  minutes. It runs only the new test file.
- **Windows/Linux:** tests pass on Windows Python 3.11.13 and are written for
  POSIX CI. The SQLite authorizer constants exist in Python 3.11+.
- **Rollback:** revert the commit; no data or schema migration is involved.

---

## 7. Reviewer guide

Start with:

1. `rlvr/src/heros_rlvr/gpu_trainer.py` — `_run_sqlite_shadow_gate` and
   `compute_dr_grpo_token_loss`.
2. `rlvr/tests/test_gpu_rlvr_pipeline.py` — the reward examples and parity tests.
3. `rlvr/README.md` — the reward table and limitations.
4. `rlvr/BENCHMARKS.md` — what is deliberately not claimed.

Questions worth asking:

- Is `expected_data_loss OR observed_row_loss` the right calibration target?
- Should the miracle penalty use reasoning length at all?
- Is count-based row loss enough for a first reward, or should v1 hash rows?
- Should the tensor loss live in `losses.py` as an optional torch backend instead
  of a separate module?

---

## 8. Checklist

- [x] Feature branch, no commit to `main`
- [x] Conventional commit message
- [x] Full `rlvr` suite run with and without torch
- [x] New tests for every reward branch and failure floor
- [x] CPU/tensor parity tests
- [x] No secrets, tokens, or local paths in the diff
- [x] Limitations documented
- [x] Patch exported for offline review
- [x] Push approved by owner
- [x] PR opened: #101
- [x] CI green on GitHub (18/18 checks)
- [x] Merged into `main` at `8a7951d`

---

## 9. Follow-ups (not in this PR)

1. ~~`qlora_runner.py`: model load, rollout loop, optimizer, checkpointing.~~
   Merged as #103 at `d3588ca`; still needs a real GPU run.
2. Requirement-satisfaction check to close the no-op loophole.
3. Process-isolated shadow worker with CPU/memory limits.
4. Held-out shadow set and a forge-parity evaluation.
5. 500-step four-arm ablation and an HF adapter with a model card.

---

## 10. Next step

#101 and #103 are merged. Run the GPU smoke next. Merging #101 does not approve
an npm publish or an HF upload.
