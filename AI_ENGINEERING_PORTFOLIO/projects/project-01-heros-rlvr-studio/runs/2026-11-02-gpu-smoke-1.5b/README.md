# GPU smoke — Qwen2.5-Coder-1.5B-Instruct, 4-bit

**Date:** 2026-11-02
**Status:** 10-step smoke with the corrected prompt; **7 optimizer steps occurred**.
This is not a 500-step run, an ablation, or a model-quality claim.

## Hardware and stack

| Item | Value |
|---|---|
| GPU | NVIDIA GeForce RTX 2060, 6 GB |
| PyTorch | 2.14.1+cu130 |
| Transformers | 5.22.1 |
| PEFT | 0.21.2 |
| bitsandbytes | 0.50.2, NF4 4-bit |
| Python | 3.11.13 |
| Prompt code | `d38a603` (literal tag exemplar) |

## Configuration

- model: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- quantization: NF4 4-bit, fp16 compute
- LoRA: `r=16`, `alpha=32`
- group size: 2
- max prompt tokens: 768
- max completion tokens: 128
- steps: 10
- learning rate: `1e-5`
- gradient accumulation: 1
- seed: 42
- temperature: 0.7

## Result

| Metric | Value |
|---|---|
| Steps | 10 |
| Completed optimizer steps | **7** |
| Skipped groups | **3** (`zero_variance_group`) |
| Mean reward (completed) | **0.3393** |
| Reward range | `-0.75` to `1.75` |
| Wall clock | 185.0 s |
| Peak allocated VRAM | 4,154.6 MB |

The first three steps and steps 7-10 produced finite losses and varied rewards.
The prompt exemplar fixed the format failure: the 1.5B model now emits literal
`<think>`, `<sql_migration>`, and `<forge_manifest>` blocks.

The 10-step adapter was saved to the run's temp directory (`final/`), but it is
a smoke artifact only and is not published or presented as trained.

## What this proves

- The full runner works on the actual 1.5B model: 4-bit load, generation,
  verifier rewards, informative-group filter, loss, backward, optimizer,
  checkpoint, and recorder.
- The GPU fit: 4.15 GB peak on a 6 GB card with two 4-bit models.
- The corrected prompt produces a usable training signal on this task set.

## What this does not prove

- No 500-step run has completed at the time this file was written.
- No reward improvement, held-out score, or model quality.
- No multi-seed or four-arm ablation.
- No HF upload or model card.

## Files

- `run.json` — config and environment
- `steps.jsonl` — per-step reward, loss, KL, clip fraction, error codes
- `summary.json` — 10 steps, 7 completed, 3 skipped
