# Qwen2.5-Coder-1.5B HEROS migration adapter

**Status:** local experiment; **not uploaded**. This is a single-arm
Dr.GRPO/DAPO run, not a benchmark or a claim of model quality.

## Model

- Base: [`Qwen/Qwen2.5-Coder-1.5B-Instruct`](https://huggingface.co/Qwen/Qwen2.5-Coder-1.5B-Instruct)
- Adapter: LoRA, `r=16`, `alpha=32`, dropout 0.05
- Quantization: NF4 4-bit base, fp16 compute
- License: Apache-2.0 (inherited from the base model)
- Adapter files: `final/` in this run directory

## Training

- Dataset: HEROS `heros_migration_500.jsonl`
- SHA-256: `f1fa58dae90c561ed806af6b89b600c5c784514b1ce05269d640a076fc7e2243`
- Examples: 500
- Reward: deterministic SQLite shadow gate + risk/data-loss/approval calibration
  (maximum 2.0)
- Objective: Dr.GRPO centered advantages, DAPO asymmetric clipping, k3 KL
- Group size: 2
- Max prompt/completion tokens: 768 / 128
- Learning rate: 1e-05
- Gradient accumulation: 1
- Temperature/top-p: 0.7 / 0.95
- Seed: 42
- Steps: 500
- Code commit in `run.json`: `d38a603bbb9ba51b90a2d697af5ebd43a229fe6a`

## Hardware

- GPU: NVIDIA GeForce RTX 2060
- PyTorch: 2.14.1+cu130
- Python: 3.11.13
- SQLite: 3.50.4
- Platform: Windows-10-10.0.21996-SP0

## Measured training metrics

| Metric | Value |
|---|---:|
| Steps | 500 |
| Completed optimizer steps | 209 |
| Skipped groups | 291 |
| Mean reward (completed) | 1.0203 |
| Reward std | 0.6931 |
| Reward, first 50 completed | 0.4975 |
| Reward, last 50 completed | 1.31 |
| Mean loss | 0.015926 |
| Mean KL | 0.02115225 |
| Mean clip fraction | 0.0 |
| Reward range | -0.75 to 1.875 |
| Wall clock | 23541.51 s |
| Peak allocated VRAM | 4158.9 MB |
| Skip reasons | `{"zero_variance_group": 291}` |
| Error codes | `{"MISSING_BLOCKS": 36, "OK": 830, "SQL_EXEC_ERROR": 134}` |

These are **training-set** numbers. There is no MATH-500/GSM8K score.

## Held-out evaluation

`checkpoint-450` evaluated on rows 451-500, which it had not seen. The final
500-step adapter is not used for this table because it later trained on those
rows.

| Model | Mean reward | OK rate | Risk accuracy | Row-loss rate |
|---|---:|---:|---:|---:|
| Base | 0.71 | 0.66 | 0.16 | 0.0 |
| A3 checkpoint-450 | 1.465 | 1.0 | 0.02 | 0.0 |


These are 50-task, single-seed numbers. They are not a significance test and the
split is time-based within one generated dataset.

### Interpretation: the reward increase is mostly format compliance

The adapter is **not** solving the requested migrations. On the 50 held-out
tasks:

- 50/50 completions parsed and executed (`OK` rate 1.0).
- 36/50 added a generic `note` column instead of performing the requested
  change.
- 0/50 contained destructive SQL.
- All 50 predicted `has_data_loss: false` and `decision_required: false`.
- Risk-tier accuracy fell from **0.16** (base) to **0.02** (adapter).

Example `heros-mig-0451`: the task is a `drop_column` with expected tier
`CRITICAL`; the adapter added `note TEXT`, predicted `NOTABLE`, and received
`1.0`. The base model did the same with `SAFE`. This is the documented no-op
loophole, not evidence of migration competence.

The mean reward rose from 0.71 to 1.465 because the adapter learned the tag
format and executable additive SQL. It did not learn requirement satisfaction
or risk calibration. A task-satisfaction checker is required before this reward
can be trusted as a training objective.

## Intended use

Research on verifier-driven post-training for database migration rewrites. The
adapter should be evaluated against `forge` and a held-out schema set before any
production use.

## Limitations

- The reward checks row counts, not full requirement satisfaction. A no-op can
  score on a safe task; delete-and-reinsert with the same count is invisible.
- The shadow gate executes SQLite, not PostgreSQL. Production parity is unproven.
- Single seed, single arm, no A0/A1/A2 comparison. Do not claim Dr.GRPO "helps"
  from this run.
- 4-bit NF4 training is not bitwise reproducible; report variance.
- The 500 prompts are also the training set, so the metrics are not a
  generalization measure.
- The adapter was not uploaded and has no external review.

## Loading

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    load_in_4bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(base, "final")
tokenizer = AutoTokenizer.from_pretrained("final")
```
