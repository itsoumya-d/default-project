# Project 01 — HEROS-RLVR-Studio

**Status:** verifier/loss, runner, requirement check, and SFT warm start are
merged. The old RL adapter failed requirement satisfaction and is invalid. The
SFT warm start scores **1.90 held-out reward** vs base **0.02**, with 45/50 tasks
at the maximum 2.0 and manifest risk accuracy 0.90. The adapter and model card
are local only; HF publication remains. RL-from-SFT was probed and produced
zero-variance groups; a 100-step RL-from-base pilot reached only **0.13**
held-out reward (0.165 at checkpoint-50) versus SFT **1.90**. **No RL gain is
claimed.** See [`RL_FROM_SFT.md`](RL_FROM_SFT.md) and
[`RL_BASE_100.md`](RL_BASE_100.md).
**Repository of record:** `itsoumya-d/HEROS`. The verifier/loss PR is
[#101](https://github.com/itsoumya-d/HEROS/pull/101), merged at `8a7951d`; the P5
runner is [#103](https://github.com/itsoumya-d/HEROS/pull/103), merged at
`d3588ca`; the prompt exemplar is
[#104](https://github.com/itsoumya-d/HEROS/pull/104), merged at `d38a603`; the
GPU-smoke documentation is
[#105](https://github.com/itsoumya-d/HEROS/pull/105), merged at `a8451f6`; the
held-out evaluation CLI is
[#106](https://github.com/itsoumya-d/HEROS/pull/106), merged at `83a1b96`; the
requirement check is
[#107](https://github.com/itsoumya-d/HEROS/pull/107), merged at `f0e22d6`; the
SFT target generator is
[#108](https://github.com/itsoumya-d/HEROS/pull/108), merged at `c32614f`; the
evaluation metric fix is
[#109](https://github.com/itsoumya-d/HEROS/pull/109), merged at `1f047ad`; the
reproducible SFT CLI is
[#110](https://github.com/itsoumya-d/HEROS/pull/110), merged at `90f33a1`; the
adapter-init path is
[#119](https://github.com/itsoumya-d/HEROS/pull/119), merged at `e4cfed4`.
**Workspace copy:** `AI_ENGINEERING_PORTFOLIO/projects/project-01-heros-rlvr-studio/`
(verifier, runner, tests, and the documents in `docs/`).

---

## 1. The problem

Small code models fail at schema migrations in a specific, expensive way: they
emit a plausible `ALTER TABLE` or `DROP COLUMN` that destroys rows, then describe
it as safe. A text-only reward model cannot reliably catch this, because the
failure is not in the prose; it is in what the SQL does to data.

HEROS already has the right primitive: `forge` is a deterministic schema-risk
oracle. HEROS-RL already has a critic-free GRPO engine and a 500-case migration
dataset. What was missing was the bridge:

1. Execute the model's migration against seeded rows in a disposable database.
2. Measure row loss instead of asking a judge.
3. Turn the result into a scalar reward with a stable contract.
4. Optimize it with Dr.GRPO reductions and DAPO clipping.

This project builds that bridge and then measures whether it trains.

---

## 2. What is new here

| Component | File | State |
|---|---|---|
| Deterministic SQLite shadow verifier | `src/heros_rlvr/gpu_trainer.py` | Implemented, 8 tests |
| DAPO dynamic sampler | same | Implemented, 4 tests; delegates to existing CPU references |
| Dr.GRPO advantage + DAPO token loss | same | Implemented, 5 tests; parity-pinned to `grpo_loss` |
| Test suite, verifier/loss | `tests/test_gpu_rlvr_pipeline.py` | 17 tests |
| QLoRA rollout runner | `src/heros_rlvr/qlora_runner.py` | Implemented, 27 tests |
| Runner CLI | `scripts/train_qlora.py` | Implemented; dry-run over 500 rows |
| Runner test suite | `tests/test_qlora_runner.py` | Schema bridge, recorder, fake-policy orchestration |
| CPU-torch CI job | `.github/workflows/rlvr.yml` (#101) | Added |
| `gpu` / `train` dependency extras | `rlvr/pyproject.toml` (#101 / #103) | Added |
| 500-step ablation | `RL_FROM_SFT.md`, `RL_BASE_100.md` | **SFT 1.90; RL-from-SFT 0/10 variance groups; RL-base 100-step 0.13 (0.165 at 50); no four-arm ablation** |
| HF adapter | — | **Not uploaded** |

The verifier is stdlib-only. PyTorch is imported lazily, so the default suite
stays lightweight and the reward path can run in a process without CUDA.

---

## 3. Reward in one table

| Term | Value | Source |
|---|---:|---|
| Format | `+0.25` | all three blocks present and manifest is a JSON object |
| Shadow execution | `+0.75` | migration executed successfully in SQLite |
| Risk calibration | `+0.50` | predicted tier equals expected tier |
| Data-loss calibration | `+0.25` | predicted flag equals `expected_data_loss OR observed_row_loss` |
| Approval calibration | `+0.25` | predicted `decision_required` equals task |
| Miracle-step penalty | `-0.40` | destructive claim/SQL with fewer than 20 characters of reasoning |
| **Maximum** | **`2.00`** | |

Failure floors are separate: `-1.00` for missing blocks, `-0.50` for invalid JSON
or SQL execution error. The full contract, including edge cases and loopholes, is
in [`docs/REWARD_SPEC.md`](docs/REWARD_SPEC.md).

The design is deliberately not a learned reward model. The same completion and
the same seed produce the same reward on every machine with the same SQLite
version.

---

## 4. Test evidence

Command, from the HEROS repository root with the `gpu` extra installed:

```powershell
$env:PYTHONPATH = "rlvr/src"
python -m unittest discover -s rlvr/tests -v
```

| Environment | Result | Marker |
|---|---|---|
| PyTorch 2.15.0+cpu, Python 3.11.13, Windows | **94 tests pass, 0 fail** | **[V]** |
| No PyTorch, Python 3.11.13, Windows | **94 tests, 81 pass, 13 skip** | **[V]** |
| 500-row dataset dry-run, no torch | **500/500 rows mapped, 10 hazard classes** | **[V]** |
| 10-step 1.5B GPU smoke | **7 completed, 3 skipped, mean reward 0.339, 4.15 GB peak** | **[V]** |
| 500-step single-arm run | **500 steps, 209 optimizer steps, reward 1.0203, 4.16 GB** | **[V]** |
| Held-out eval, old reward | base 0.71 vs checkpoint-450 1.465; risk 0.16 vs 0.02 | **[V]** |
| Held-out re-score, #107 reward | base 0.02 vs adapter 0.265; adapter 40/50 `REQUIREMENT_MISS` | **[V]** |
| SFT warm start, #107 reward | base 0.02 vs SFT adapter **1.90**; 45/50 at 2.0; risk 0.90 | **[V]** |

The thirteen skips are tensor tests: seven pre-existing loss/advantage cases and
six runner-orchestration cases. They skip by design rather than failing the
stdlib-only job. The verifier, schema bridge, prompt builder, and recorder tests
run without torch.

What the tests prove:

- A safe `ALTER TABLE ... ADD COLUMN` scores `2.0`.
- A destructive `DROP TABLE` is detected by row-count loss and scores `1.6` with
  the miracle penalty.
- Missing blocks fail closed at `-1.0`.
- Invalid JSON fails before SQL execution at `-0.5`.
- `ATTACH DATABASE` is denied by the SQLite authorizer.
- A manifest that understates row loss cannot hide the observed loss.
- Dr.GRPO advantages are zero-mean; the length-bias test gets equal per-token
  gradients for a 10-token and a 100-token completion at `kl_beta=0`.
- The constant-horizon loss scales inversely with `L_max`.
- The tensor advantage and loss paths match their pure-Python references, so the
  CPU and GPU implementations cannot drift silently.
- A Forge schema row converts to SQLite DDL plus deterministic seed rows, and the
  seed executes in an in-memory database.
- All five forge tiers (`SAFE`, `NOTABLE`, `MEDIUM`, `HIGH`, `CRITICAL`) are
  accepted; an unknown tier fails before training.
- The prompt shows the hazard and schemas but not the expected labels, and now
  includes a literal tag exemplar with no task-label leakage.
- A zero-variance group skips the optimizer step and is logged as skipped.
- Gradient accumulation divides the loss, so two half-sized micro-batches match
  one full batch rather than doubling the update.
- `run.json`, `steps.jsonl`, and `summary.json` are written, and a restart
  truncates stale step logs instead of appending to them.

The separate 10-step GPU smoke exercised `HFPolicy` on the RTX 2060: 4-bit load,
generation, literal tag parsing, 7 optimizer steps, and adapter save at 4.15 GB
peak. What the tests and smoke do **not** prove: model quality, training
stability, throughput, or benchmark improvement. Those require the completed
500-step run and a held-out evaluation.

---

## 5. Quick start

```bash
# From the HEROS repository root
cd rlvr
python -m pip install -e ".[gpu]"      # verifier/loss/CPU runner tests
python -m unittest discover -s tests -v

# The HF adapter and a real run need the train extra
python -m pip install -e ".[train]"
python scripts/train_qlora.py \
  --dataset ../../HEROS-RL/data/heros_migration_500.jsonl --dry-run
```

Minimal verifier call:

```python
from heros_rlvr.gpu_trainer import DeterministicForgeShadowVerifier, MigrationTask

task = MigrationTask(
    task_id="mig-001",
    from_ddl="CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL);",
    seed_sql="INSERT INTO users (id, email) VALUES (1, 'a@b.com');",
    requirement="Add an optional bio column without losing rows.",
    expected_risk_tier="SAFE",
    expected_data_loss=False,
    decision_required=False,
)

completion = (
    "<think>Adding a nullable column preserves the seeded row.</think>"
    "<sql_migration>ALTER TABLE users ADD COLUMN bio TEXT;</sql_migration>"
    '<forge_manifest>{"risk_tier": "SAFE", "has_data_loss": false, '
    '"decision_required": false}</forge_manifest>'
)

receipt = DeterministicForgeShadowVerifier().verify_rollout(task, completion)
print(receipt.total_reward, receipt.error_code)  # 2.0 OK
```

---

## 6. Layout

```text
project-01-heros-rlvr-studio/
├── README.md                 # this file
├── BENCHMARKS.md             # measurement protocol + smoke evidence
├── PR_DESCRIPTION.md         # review packet for #101
├── PR_DESCRIPTION_P5.md      # review packet for #103
├── runs/
│   ├── 2026-11-02-gpu-smoke-0.5b/
│   ├── 2026-11-02-gpu-smoke-1.5b/
│   └── 2026-11-02-a3-500-qwen1.5b/   # in progress
├── docs/
│   ├── REWARD_SPEC.md        # reward contract and edge cases
│   ├── ARCHITECTURE.md       # data flow, threat model, GPU budget
│   └── EVALUATION.md         # pre-registered held-out protocol
├── src/heros_rlvr/
│   ├── gpu_trainer.py        # verifier + sampler + loss
│   └── qlora_runner.py       # schema bridge, rollout loop, recorder, HF adapter
├── scripts/
│   └── train_qlora.py        # dry-run and real-run CLI
└── tests/
    ├── test_gpu_rlvr_pipeline.py
    └── test_qlora_runner.py
```

The files are copied into `HEROS/rlvr/` on the merged branches. This directory
is the portfolio-side source of truth for the design documents; the code of
record is `main` at `90f33a1`. The mirror intentionally omits the pre-existing
`advantages.py`, `sampling.py`, `losses.py`, and package metadata, so run the
tests from the HEROS checkout, not from this directory.

---

## 7. Roadmap inside the project

| Phase | Deliverable | State |
|---|---|---|
| P1 | Reward specification | **Done** |
| P2 | Architecture and threat model | **Done** |
| P3 | Dependency extras | **Done** (`gpu` and `train` extras) |
| P4 | Verifier + loss engine | **Done** ([#101](https://github.com/itsoumya-d/HEROS/pull/101)) |
| P5 | `qlora_runner.py` for Qwen2.5-Coder-1.5B-Instruct | **Merged** ([#103](https://github.com/itsoumya-d/HEROS/pull/103)); GPU-smoked |
| P6 | 75+ tests | **94 now** |
| P7 | 500-step four-arm ablation | **RL arm negative; SFT warm start 1.90 held-out; RL-from-SFT and A0/A1/A2 pending** |
| P8 | Parallel shadow workers >1.8× step throughput | Not started |
| P9 | Kaggle/Colab notebook | Not started |
| P10 | HF adapter + model card | SFT model card local; HF upload blocked on credentials |

P7 now has a GPU path and an SFT result: RTX 2060, 4-bit 1.5B, 3.14 GB SFT peak.
The four-arm ablation is still missing; the SFT arm is not a controlled RL
comparison. P10 has a local model card but is blocked on the absent HF token. P8
can start from the measured 500-step RL throughput.

### Acceptance evidence

| Gate | Requirement | Evidence | Status |
|---|---|---|---|
| Tests | 75+ green | 94 tests with torch; 81 pass + 13 skip without | **[V]** |
| GPU path | 4-bit 1.5B fits 6 GB | 4.15 GB peak in the 10-step smoke | **[V]** |
| Training signal | Informative reward groups | 7/10 optimizer steps in the smoke | **[V]** |
| 500-step run | 500 steps, finite loss | 500 steps, 209 optimizer steps, mean reward 1.0203 | **[V]** |
| Held-out eval, old RL reward | Unseen migration rows | base 0.71 vs old adapter 1.465; risk 0.16 vs 0.02 | **[V]** |
| Held-out eval, corrected reward | Unseen migration rows | base 0.02 vs old adapter 0.265; old adapter 40/50 `REQUIREMENT_MISS` | **[V]** |
| SFT warm start | 500 supervised steps | loss 1.53 -> 3.1e-5; adapter saved locally | **[V]** |
| SFT held-out eval | base vs SFT on rows 451-500 | **SFT 1.90 vs base 0.02; 45/50 at 2.0; risk 0.90** | **[V]** |
| Model card | Honest metrics + limits | SFT `MODEL_CARD.md` generated | **[V]** |
| Requirement satisfaction | Requested change actually performed | SFT 45/50 at 2.0; 5 `type_narrowing` at 1.0 | **[V]** |
| HF upload | Public artifact | blocked: no HF token | **[X]** |
| RL from SFT | RL rerun on the warm start | not started | **[X]** |
| Four-arm ablation | A0/A1/A2/A3 | no controlled comparison | **[X]** |
| Parallel workers | >1.8× at 4 workers | not started | **[X]** |

P01 is **locally portfolio-ready but not published**. The SFT adapter is a strong
held-out result under the corrected reward. It is not a controlled RL result, has
no HF artifact, and has not been tested against PostgreSQL. Do not present the
old 500-step RL adapter as a migration model.

---

## 8. Limitations and non-claims

- **The old RL result was negative.** The 500-step RL adapter raised mean reward
  from 0.71 to 1.465 but risk accuracy fell from 0.16 to 0.02; 36/50 completions
  were no-op `ADD COLUMN` migrations. Under the corrected reward it scores 0.265
  with 40/50 requirement misses. It is invalid and must not be published.
- **The SFT result is positive but narrow.** The SFT adapter scores **1.90** on
  50 held-out rows (base 0.02), with 45/50 at 2.0 and manifest risk accuracy
  0.90. The 5 failures are all `type_narrowing`, which SQLite cannot verify.
  This is supervised warm start, not RL; there is no controlled A0/A1/A2/A3
  comparison.
- **The shadow gate executes SQLite, not PostgreSQL.** The runner prompts for
  SQLite-compatible SQL so training and verification agree. PostgreSQL syntax
  parity is a separate evaluation gate; the production migration target remains
  PostgreSQL.
- The shadow verifier checks **row counts**, not row contents. A migration that
  deletes and reinserts the same number of different rows is not flagged. A
  table rename is flagged as loss even when data is preserved.
- **Requirement checking is schema-level.** A no-op is now rejected when a
  target schema is supplied, but row contents are still not hashed; a
  delete-and-reinsert with the same count is invisible.
- **`type_narrowing` is unrepresentable in SQLite.** `bigint` and `int` collapse
  to the same affinity; the 50 such rows are excluded from SFT and score 1.0,
  not 2.0, in the held-out set.
- The SQLite authorizer is a narrow escape guard, not a sandbox. There is no
  statement timeout or memory cap; untrusted SQL still needs process isolation
  for production use.
- The verifier is deterministic for a fixed SQLite version. A SQLite upgrade can
  change parser or authorizer behavior; pin the version in CI if exact
  reproducibility matters.
- The miracle-step detector is a heuristic. It routes suspicious samples for
  review; it is not a faithfulness proof.
- No comparison to OpenAI, Anthropic, or any hosted RLHF service is made or
  implied.

---

## 9. References

- Dr.GRPO: Liu et al., *Understanding R1-Zero-Like Training: A Critical
  Perspective*, arXiv:2503.20783.
- DAPO: Yu et al., *DAPO: An Open-Source LLM Reinforcement Learning System at
  Scale*, arXiv:2503.14476.
- GRPO: Shao et al., *DeepSeekMath*, arXiv:2402.03300.
- QLoRA: Dettmers et al., arXiv:2305.14314.
- HEROS `forge` and the parent repository: `itsoumya-d/HEROS`.
- HEROS-RL engine and dataset: `itsoumya-d/HEROS-RL`.
