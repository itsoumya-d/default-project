# GPU smoke — Qwen2.5-Coder-0.5B-Instruct

**Date:** 2026-11-02
**Status:** infrastructure smoke only; **no optimizer step occurred**. This is not
a training result and the saved adapter is not a trained artifact.

## Hardware and stack

| Item | Value |
|---|---|
| GPU | NVIDIA GeForce RTX 2060, 6 GB |
| Driver | 610.88, CUDA UMD 13.3 |
| PyTorch | 2.14.1+cu130 |
| Transformers | 5.22.1 |
| PEFT | 0.21.2 |
| bitsandbytes | 0.50.2 (installed; 4-bit not used in this run) |
| Python | 3.11.13 |
| SQLite | 3.50.4 |

## Configuration

- model: `Qwen/Qwen2.5-Coder-0.5B-Instruct`
- precision: fp16, no 4-bit quantization
- LoRA: `r=16`, `alpha=32`
- group size: 2
- max prompt tokens: 768
- max completion tokens: 96
- steps: 10
- learning rate: `1e-5`
- gradient accumulation: 1
- seed: 42

## Result

| Metric | Value |
|---|---|
| Steps | 10 |
| Completed optimizer steps | **0** |
| Skipped groups | **10** (`zero_variance_group`) |
| Mean reward per step | `-1.0` |
| Error code | `MISSING_BLOCKS` for both rollouts |
| Wall clock | 224.92 s |
| Peak allocated VRAM | 1,971.5 MB |

Every group was zero-variance, so DAPO dynamic sampling skipped it before the
loss and optimizer. The model did not emit the required
`think`/`sql_migration`/`forge_manifest` blocks.

## What this proves

- CUDA torch, `HFPolicy.load`, tokenizer/chat-template generation, the SQLite
  verifier, and `RunRecorder` work together on the RTX 2060.
- The runner correctly refuses to train on a zero-variance group.
- A 0.5B model at this prompt is not a viable training base without a stronger
  format-following prompt or a larger model.

## What this does not prove

- No loss curve, no reward improvement, no learned adapter, no pass@1.
- No 500-step run.
- No model-card or HF upload claim.

## Files

- `run.json` — config and environment
- `steps.jsonl` — per-step rewards, skip reasons, error codes
- `summary.json` — 10 steps, 0 completed, 10 skipped
