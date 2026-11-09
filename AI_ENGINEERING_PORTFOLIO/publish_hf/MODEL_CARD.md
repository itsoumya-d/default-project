---
license: apache-2.0
base_model: Qwen/Qwen2.5-Coder-1.5B-Instruct
pipeline_tag: text-generation
tags:
- grpo
- rlvr
- drgrpo
- sql-migration
- postgresql
- peft
- lora
- arxiv:2402.03300
- arxiv:2501.12948
---

# HEROS-RLVR Qwen2.5-Coder-1.5B (RL-from-base LoRA, 100-step pilot)

**Status: research adapter. No benchmark gain is claimed.**

A LoRA adapter (`r=16`, `alpha=32`, dropout 0.05) trained from the base model
with Dr.GRPO centered advantages, DAPO asymmetric clipping (0.28/0.20), and
k3 KL (0.01) on the HEROS destructive-DDL migration task set. 100 requested
steps; 91 completed, 9 skipped groups.

## What it proves

- A corrected, reward-hacking-free verifiable pipeline runs end-to-end (SQLite
  shadow execution + requirement checker + risk calibration).
- Training improved likelihood metrics (mean reward first-10 → last-10:
  −0.66 → −0.04) without collapsing.
- The failure mode is measured, not hidden: 50-task held-out eval gives
  ok_rate **0.20 (10/50)** vs base **0.20**, risk_accuracy **0.10**,
  decision_accuracy **0.50**; errors are REQUIRED_MISSING (33/50),
  SQL_EXEC_ERROR (7/50).

## What it does not prove

- No task-capability gain over base on this pilot. The next run must change
  reward content (risk-calibration + requirement weighting) before scaling steps.

## Intended use

Research/evaluation of verifiable-reward training dynamics only. Not for
production SQL migration generation.

## Files

| File | What |
|---|---|
| `adapter_config.json` | LoRA config (r16/alpha32) |
| `adapter_model.safetensors` | adapter weights (~74 MB) |
| `tokenizer.json`, `tokenizer_config.json` | tokenizer (from base) |
| `chat_template.jinja` | chat template |
| `README.md` | this card |

## Training and evaluation

- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit; RTX 2060 6 GB.
- Data: first 450 rows of `heros_migration_500.jsonl` (HF: `itssoumyad/heros-migration-500`).
- Held-out: rows 451–500 (50 tasks), same slice as the SFT comparison.
- Code and full run manifests: `github.com/itsoumya-d/default-project`
  (`docs/ai-engineering-portfolio`), `AI_ENGINEERING_PORTFOLIO/projects/project-01-heros-rlvr-studio/`
  (`runs/2026-11-03-rl-base-100-corrected`, `RL_BASE_100.md`).
- Related experiment: `github.com/itsoumya-d/rlvr-bias-probe` (GRPO vs Dr.GRPO
  length-bias probe).

## Limitations

Single-seed pilot; 50-task eval; risk calibration is the known-weak axis
(this is the main negative result of the report). Do not cite ok_rate as a
capability claim.
