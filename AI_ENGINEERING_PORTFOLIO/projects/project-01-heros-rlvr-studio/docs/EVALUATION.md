# Held-out evaluation protocol — Project 01

**Status:** pre-registered before the 500-step run finished. Results are appended
only after `checkpoint-450` exists.

## Split

- Training rows used through `checkpoint-450`: rows 1–450 of
  `heros_migration_500.jsonl`.
- Held-out rows for this evaluation: **rows 451–500 (50 tasks)**.
- `checkpoint-450` has not seen rows 451–500.
- The final 500-step adapter has seen rows 451–500, so it is **not** used for the
  held-out claim. It may be reported separately as a training-set number.

This is a time-based split within one generated dataset, not an independent
human-labeled benchmark. It measures whether the checkpoint transfers to later
schema cases, not real-world generalization.

## Models compared

1. **A0 base**: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit, no adapter.
2. **A3 checkpoint-450**: the same base with the LoRA adapter saved at step 450
   of the single-arm Dr.GRPO/DAPO run.

Both use the same prompt builder, chat template, tokenizer, and decoding settings.

## Decoding

- Greedy (`do_sample=False`)
- `max_new_tokens=128`
- prompt truncated at 768 tokens
- left padding

## Metrics

- Mean verifier reward (max 2.0)
- `OK` rate (all blocks parsed and SQL executed)
- Risk-tier calibration rate (`risk_calibration_reward == 0.5`)
- Observed row-loss rate
- Error-code distribution
- Per-hazard reward breakdown
- Peak VRAM

## What this can support

- A statement that the adapter changes held-out reward relative to the base on
  this split.
- Error analysis by hazard and error code.
- A reproducible artifact with per-task completions.

## What this cannot support

- A claim of general model quality, PostgreSQL correctness, or production safety.
- A claim that Dr.GRPO/DAPO is better than another objective: there is no A1/A2
  arm.
- A claim of statistical significance with 50 tasks and one seed.
- A claim about requirement satisfaction: the verifier still only checks row
  loss and calibration.

## Command

```powershell
$env:PYTHONPATH = "rlvr/src"
python $env:TEMP\eval_450.py `
  "AI_ENGINEERING_PORTFOLIO\projects\project-01-heros-rlvr-studio\runs\2026-11-02-a3-500-qwen1.5b" `
  checkpoint-450
```

Outputs:

- `eval_450/base.jsonl` and `base_summary.json`
- `eval_450/adapter450.jsonl` and `adapter450_summary.json`
