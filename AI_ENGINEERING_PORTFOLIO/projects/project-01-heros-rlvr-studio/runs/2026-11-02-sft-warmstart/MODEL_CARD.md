# Qwen2.5-Coder-1.5B — HEROS SFT warm start

**Status:** local experiment; **not uploaded**. Supervised warm start, not an RL
result and not a production migration model.

## Model

- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`
- Adapter: LoRA, `r=16`, `alpha=32`
- Quantization: NF4 4-bit
- License: Apache-2.0 (base model)
- Adapter: `final/`

## Training

- Targets: deterministic schema-diff SQL from `heros_rlvr.sft_data`
- Examples: 405 (first 450 rows; 50 type_narrowing rows excluded)
- Steps: 500
- Max sequence length: 1024
- Learning rate: 0.0002
- Loss: 1.529914 -> 0.00003130; mean 0.012084
- Wall clock: 496.24 s
- Peak VRAM: 3142.9 MB
- Code: `c32614f3b01be16354352d4527a2545ba3a27dff`

Loss near zero indicates fitting the training examples. It is not evidence of
generalization.

## Held-out evaluation

Base vs SFT adapter on rows 451-500 under the #107 requirement-check reward.
The held-out slice includes 5 type_narrowing rows that were excluded from SFT
because SQLite cannot distinguish their types.

| Model | Mean reward | OK rate | Risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base | 0.02 | 0.2 | 0.1957 | 0.0 |
| SFT adapter | 1.9 | 1.0 | 0.9 | 0.1 |

These are 50-task, single-seed numbers. They are not a significance test.

Per-task breakdown:

- 45/50 tasks score **2.0**.
- 5/50 tasks score **1.0**; all five are `type_narrowing`, which was excluded
  from SFT because SQLite cannot distinguish `bigint` from `int`.
- Manifest accuracy: risk **0.90**, data loss **0.90**, approval **0.90**.
- All 50 completions parse and execute (`OK` rate 1.0).
- The 0.10 row-loss rate is the five `drop_table` tasks, where losing rows is
  expected by the task label.

## Intended use

Research on verifier-driven migration post-training. The adapter must be
compared with `forge` and a larger held-out set before any production use.

## Limitations

- The SFT targets are programmatically generated, not human demonstrations.
- 50 type_narrowing rows are excluded from training; SQLite cannot verify them.
- The held-out result can be depressed by those unlearnable rows; report the
  per-hazard split.
- No RL yet; no four-arm ablation; no model-quality claim.
- The adapter is local and unpublished; no external review.
