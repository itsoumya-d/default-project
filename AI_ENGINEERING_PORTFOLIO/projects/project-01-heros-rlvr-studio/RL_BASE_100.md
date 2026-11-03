# RL from base with the corrected reward — 100-step pilot

**Status:** local experiment, 2026-11-03. **Weak positive over base; not
competitive with SFT. No model-quality claim.**

## Question

Can Dr.GRPO/DAPO from the base model learn real migrations under the corrected
requirement-check reward, without the reward hacking that invalidated the old
500-step adapter?

## Setup

- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit.
- Policy: fresh LoRA, r=16, alpha=32, dropout 0.05.
- Training data: first 450 rows of `heros_migration_500.jsonl`.
- Held-out: rows 451–500, the same 50-task slice used for the SFT result.
- Objective: Dr.GRPO centered advantages, DAPO asymmetric clipping, k3 KL.
- Group size 4, temperature 1.0, top-p 0.95.
- Max prompt/completion tokens: 1024 / 128.
- Learning rate 1e-5, gradient accumulation 1, seed 42.
- Hardware: RTX 2060 6 GB, torch 2.14.1+cu130, transformers 5.22.1, peft
  0.21.2.
- Code: `e4cfed4`; runner support for sampling controls in #119.

## Training

| Metric | Value |
|---|---:|
| Requested steps | 100 |
| Completed optimizer steps | **91** |
| Skipped groups | 9 |
| Mean reward, completed | **-0.2328** |
| Mean reward, first 10 | -0.6562 |
| Mean reward, last 10 | **-0.0437** |
| Mean loss | 0.025862 |
| Max mean KL | 0.04435 |
| Max reward std | 1.1924 |
| OK completions | 21 / 400 |
| Error codes | 70 REQUIREMENT_MISS, 66 SQL_EXEC_ERROR, 47 MISSING_BLOCKS, 21 OK |

Training reward improved, but it is still negative. Format errors decreased
during the run; requirement satisfaction is the remaining bottleneck.

## Held-out evaluation

Greedy decoding on rows 451–500. Both adapters were evaluated against the same
base run in the same script.

| Model | Mean reward | OK rate | Risk accuracy | Loss accuracy | REQUIREMENT_MISS | SQL_EXEC_ERROR | MISSING_BLOCKS |
|---|---:|---:|---:|---:|---:|---:|---:|
| Base | 0.02 | 0.20 | 0.20 | 0.60 | 23 | 12 | 5 |
| RL base, checkpoint-50 | **0.165** | 0.20 | 0.20 | 0.64 | 32 | 8 | 0 |
| RL base, final (100) | **0.13** | 0.20 | **0.10** | **0.72** | 33 | 7 | 0 |
| SFT warm start | **1.90** | 1.00 | **0.90** | **0.90** | 0 | 0 | 0 |

The RL arm removes the base model's missing-block failures and slightly reduces
SQL execution errors, but it produces more requirement misses than the base and
far more than SFT. Going from 50 to 100 steps did not improve mean reward or
risk accuracy; it only improved loss calibration.

## Interpretation

- The corrected reward **does provide a learning signal from base**: 91/100
  groups had variance and the final training reward is less negative than the
  start.
- The signal is weak: 100 steps move held-out reward from 0.02 to 0.13–0.165,
  while SFT reaches 1.90 with no RL.
- The adapter is not competitive, and the checkpoint trend is non-monotonic.
  There is no basis for claiming an RL gain over SFT, a four-arm ablation, or a
  production migration model.
- The result is consistent with the earlier finding that the deterministic,
  coarse verifier is easy to satisfy partially but hard to optimize from a weak
  base in 100 steps.

## Decision

Keep the SFT adapter as the accepted P01 result. Do not publish the RL adapter.
The next useful experiment is a longer, better-shaped run only if it can answer
a specific question; otherwise the honest portfolio result is the negative
RL-from-SFT probe plus this weak base-model pilot.

## Evidence

- `runs/2026-11-03-rl-base-probe/` — 10-step probe, 8/10 completed.
- `runs/2026-11-03-rl-base-100-corrected/` — training artifacts,
  `checkpoint-50`, `checkpoint-100`, `final`.
- `runs/2026-11-03-rl-base-100-corrected/eval_checkpoint-50/`
- `runs/2026-11-03-rl-base-100-corrected/eval_final/`

Adapter weights are gitignored. The background shell reported exit code 1 after
printing `completed 91/100`; `run.json`, `steps.jsonl`, `summary.json`, both
checkpoints, and `final` are present and were used for evaluation.

## Limitations

- 100 steps, one seed, one Windows host, 50 held-out tasks.
- No significance test and no hyperparameter sweep.
- The base and SFT evaluations were run at different times but use the same
  deterministic verifier and held-out rows.
- The RL adapters were not uploaded or published.
