# SFT warm start — Qwen2.5-Coder-1.5B

**Status:** 500-step supervised warm start complete; held-out evaluation complete.
This is not an RL run and not a published model.

## Why

The corrected RL smoke showed that the base model rarely satisfies the target
schema (`9/20 REQUIREMENT_MISS`). RL alone would train on failures. This run
supervises deterministic target-satisfying SQL from `heros_rlvr.sft_data`.

## Data and configuration

- Training rows: first 450 of `heros_migration_500.jsonl`
- Usable examples: **405** (50 `type_narrowing` rows excluded because SQLite
  cannot represent the distinction)
- Held-out rows: 451–500
- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit
- LoRA: `r=16`, `alpha=32`
- Max sequence length: 1024
- Learning rate: `2e-4`
- Steps: 500
- Code: `c32614f` (SFT target generator)

## Result

| Metric | Value |
|---|---:|
| Steps | 500 |
| Loss, first step | 1.5299 |
| Loss, last step | 0.0000313 |
| Mean loss | 0.01208 |
| Wall clock | 496.24 s |
| Peak VRAM | 3,142.9 MB |
| Adapter | `final/` (local) |

Loss near zero indicates strong fitting to the 405 examples. The held-out
evaluation decides whether it generalizes; training loss alone is not evidence.

## Held-out result

Base vs SFT adapter on rows 451-500 under the #107 reward, 512 generated tokens:

| Model | Mean reward | OK rate | Risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base | 0.02 | 0.20 | 0.1957 | 0.0 |
| SFT adapter | **1.90** | **1.00** | **0.90** | 0.10 |

45/50 tasks score 2.0. The five 1.0 tasks are `type_narrowing`, which SQLite
cannot verify and which were excluded from SFT. The 0.10 row-loss rate is the
five `drop_table` tasks, where row loss is expected by the label.

## Artifacts

- `run.json` — config and environment
- `run.log` — step losses
- `sft_metrics.json` — aggregate loss and timing
- `final/` — LoRA adapter and tokenizer
- `eval_450/` — base vs SFT adapter on held-out rows (when complete)
