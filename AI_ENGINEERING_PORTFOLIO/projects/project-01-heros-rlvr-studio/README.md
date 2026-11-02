# Project 01 — HEROS-RLVR-Studio

**Status:** code slice implemented and tested; PR #1 staged locally; **no GPU run
yet**.
**Repository of record:** `itsoumya-d/HEROS`, branch
`feat/rlvr-dr-grpo-gpu-trainer`, commit `b59f47e`.
**Workspace copy:** `AI_ENGINEERING_PORTFOLIO/projects/project-01-heros-rlvr-studio/`
(verifier, tests, and the documents in `docs/`).

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
| Test suite | `tests/test_gpu_rlvr_pipeline.py` | 17 tests |
| CPU-torch CI job | `.github/workflows/rlvr.yml` (PR #1) | Added |
| `gpu` dependency extra | `rlvr/pyproject.toml` (PR #1) | Added |
| QLoRA runner | — | **Not implemented** (Phase P5) |
| 500-step ablation | — | **Not run** |
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
| PyTorch 2.15.0+cpu, Python 3.11.13, Windows | **51 tests pass, 0 fail** | **[V]** |
| No PyTorch, Python 3.11.13, Windows | **51 tests, 44 pass, 7 skip** | **[V]** |

The seven skips are the tensor tests: advantages, the CPU/tensor parity checks,
loss bias, horizon scaling, shape validation, and invalid horizon. They skip by
design rather than failing the stdlib-only job.

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

What the tests do **not** prove: model quality, training stability, throughput,
or benchmark improvement. Those require the GPU run.

---

## 5. Quick start

```bash
# From the HEROS repository root
cd rlvr
python -m pip install -e ".[gpu]"      # torch is optional for the verifier
python -m unittest discover -s tests -v
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
├── BENCHMARKS.md             # measurement protocol; results pending
├── PR_DESCRIPTION.md         # review packet for PR #1
├── docs/
│   ├── REWARD_SPEC.md        # reward contract and edge cases
│   └── ARCHITECTURE.md       # data flow, threat model, GPU budget
├── src/heros_rlvr/
│   └── gpu_trainer.py        # verifier + sampler + loss
└── tests/
    └── test_gpu_rlvr_pipeline.py
```

The files are copied into `HEROS/rlvr/` on the PR branch. This directory is the
portfolio-side source of truth for the design documents; the code of record is the
PR branch. The mirror intentionally omits the pre-existing `advantages.py`,
`sampling.py`, and `losses.py` modules, so run the tests from the HEROS checkout,
not from this directory.

---

## 7. Roadmap inside the project

| Phase | Deliverable | State |
|---|---|---|
| P1 | Reward specification | **Done** |
| P2 | Architecture and threat model | **Done** |
| P3 | Dependency extras | **Partial** (`gpu` extra; runner deps pending) |
| P4 | Verifier + loss engine | **Done** (PR #1) |
| P5 | `qlora_runner.py` for Qwen2.5-Coder-1.5B-Instruct | **Next** |
| P6 | 75+ tests | 51 now |
| P7 | 500-step four-arm ablation | Not started |
| P8 | Parallel shadow workers >1.8× step throughput | Not started |
| P9 | Kaggle/Colab notebook | Not started |
| P10 | HF adapter + model card | Not started |

P5 is blocked on nothing but implementation time. P7 is blocked on GPU access and
owner approval. P10 is blocked on P7.

---

## 8. Limitations and non-claims

- **No model was trained for this project yet.** There is no adapter, no loss
  curve, no pass@1 number, and no throughput number.
- The shadow verifier checks **row counts**, not row contents. A migration that
  deletes and reinserts the same number of different rows is not flagged. A
  table rename is flagged as loss even when data is preserved.
- A no-op migration can score `2.0` on a safe task. The verifier rewards safety
  and calibration, not requirement satisfaction. A requirement-satisfaction check
  is future work.
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
