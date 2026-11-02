# A3 single-arm 500-step run

**Status:** training complete; held-out evaluation running.

## Configuration

- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- Quantization: NF4 4-bit, fp16 compute
- LoRA: `r=16`, `alpha=32`
- Objective: Dr.GRPO centered advantages + DAPO asymmetric clipping + k3 KL
- Group size: 2
- Max prompt / completion tokens: 768 / 128
- Learning rate: `1e-5`
- Gradient accumulation: 1
- Temperature / top-p: 0.7 / 0.95
- Seed: 42
- Steps: 500
- Hardware: RTX 2060 6 GB
- Code commit: `d38a603`
- Wall clock: 23,541.5 s (6.54 h)
- Peak allocated VRAM: 4,158.9 MB

## Training result

| Metric | Value |
|---|---:|
| Steps | 500 |
| Optimizer steps | 209 |
| Zero-variance skips | 291 |
| Mean reward | 1.0203 |
| Reward, first 50 completed | 0.4975 |
| Reward, last 50 completed | 1.3100 |
| Reward range | -0.75 to 1.875 |
| Mean loss | 0.015926 |
| Mean KL | 0.021152 |
| Mean clip fraction | 0.0 |
| Error codes | 830 OK, 134 SQL_EXEC_ERROR, 36 MISSING_BLOCKS |

The reward curve rises on the training set. This is not a held-out result and
not a significance test. The held-out evaluation uses `checkpoint-450` on rows
451-500, which that checkpoint has not seen; the final adapter trained on those
rows afterward.

## Artifacts

- `checkpoint-450/` — held-out evaluation checkpoint
- `final/` — final LoRA adapter and tokenizer (local, not uploaded)
- `eval_450/` — held-out base vs adapter outputs (when complete)
- `MODEL_CARD.md` — generated from final metrics and held-out results (when complete)
- `run.json`, `steps.jsonl`, `summary.json`, `final_metrics.json`
