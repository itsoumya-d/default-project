# Pre-registration — P01 risk-weighted rerun (2026-11-09)

**Decision:** D-2026-11-09-001 (continue Dr.GRPO + DAPO + k3 KL; change reward
content, not the estimator).

## Question

Does doubling the risk-calibration and requirement (shadow/schema-match) terms
improve risk calibration from base, as the reward-content hypothesis predicts?

## Setup (frozen before the run)

- Code: `repos/HEROS/rlvr/scripts/train_qlora.py` @ `461880a`
  (weights added in this commit; defaults 1.0 preserve the spec).
- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit.
- Policy: fresh LoRA r=16, alpha=32, dropout 0.05.
- Training data: first 450 rows of `heros_migration_500.jsonl`.
- Held-out: rows 451–500 (50 tasks) — the same slice as all prior runs.
- Objective: Dr.GRPO centered advantages, DAPO asymmetric clipping (0.28/0.20),
  k3 KL 0.01.
- **Reward change:** `risk_calibration_weight=2.0`, `requirement_weight=2.0`
  (total max 3.75 vs spec 2.0; components raw in receipts, weighting in total).
- Group size 4, temperature 1.0, top-p 0.95, max prompt/completion 1024/128,
  learning rate 1e-5, gradient accumulation 1, seed 42.
- Requested steps: **250** (prior: 100).
- Hardware: RTX 2060 6 GB, torch 2.14.1+cu130, transformers 5.22.2, peft 0.21.2.

## Gate

Held-out 50 (greedy, spec-weighted eval via
`evaluate_heldout.py --start 450 --limit 50`): **risk_accuracy > 0.20** (base)
before any further step scaling. Report ok_rate, risk_accuracy,
decision_accuracy, mean reward, error-code histogram regardless of outcome.

## Run

- `runs/2026-11-09-risk-weighted-250/` (pending)
- Smoke: `runs/2026-11-09-risk-weighted-smoke2` (5 steps, 3 completed — weights
  recorded in run.json; step-1 KL/STD match the unweighted run's trajectory).
- Restart note: first launch reached step 77 (+ `checkpoint-50`) before a
  server restart killed the process. The run was relaunched from step 0 with
  the same seed, so the trajectory is expected to reproduce exactly.

## Expected time

~85 min wall (100-step run was 34 min).
