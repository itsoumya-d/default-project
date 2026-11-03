# RL from the SFT adapter — negative result

**Status:** local experiment, 2026-11-03. **No RL improvement is claimed.**
The SFT adapter remains the accepted P01 result.

## Question

Does Dr.GRPO/DAPO improve the SFT warm start when both start from the same
`Qwen2.5-Coder-1.5B-Instruct` base and use the corrected requirement-check
reward?

## Setup

- SFT adapter: `runs/2026-11-02-sft-warmstart/final` (LoRA r=16, alpha=32,
  NF4; 18,464,768 trainable parameters).
- Dataset: `heros_migration_500.jsonl`; first 450 rows, matching the SFT
  training slice. The 50-row held-out slice was not used.
- Runner: `rlvr/scripts/train_qlora.py` with the new `--adapter-path` support
  from PR #119.
- Hardware: RTX 2060 6 GB, torch 2.14.1+cu130, transformers 5.22.1, peft
  0.21.2.
- Group sampling is skipped when `reward_std == 0`; a skipped group performs no
  optimizer step.

## Results

| Run | Group | Temperature | Steps | Completed | Rewards |
|---|---:|---:|---:|---:|---|
| smoke | 2 | 1.0 | 2 | **0** | 2.0, 2.0 |
| probe | 4 | 1.2 | 10 | **0** | nine 2.0, one 1.0 |
| probe | 4 | 1.5 | 10 | **0** | nine 2.0, one 1.0 |

Every group was skipped with `skip_reason: "zero_variance_group"` and
`reward_std: 0.0`. The one 1.0 is `heros-mig-0003`, a `type_narrowing` task
where SQLite cannot verify the intended type change; all four samples landed on
the same partial reward.

Sampling itself was not frozen:

| Temperature | Unique completions (4–8 samples) |
|---:|---:|
| 1.2 | 1 |
| 1.5 | 4 of 8 |
| 2.0 | 8 of 8 |
| 2.5 | 8 of 8, with degenerate output |

At 2.5 the model produced an unrelated URL in one sample. Diversity increased,
but the deterministic reward stayed at the same value for the sampled tasks.

## Interpretation

The SFT warm start is saturated on the sampled training distribution: it emits
requirement-satisfying SQL consistently, so all group members earn 2.0. The
verifier is deliberately coarse (execute, preserve rows, match the target
schema), so different valid migrations receive the same reward. With zero
variance, DAPO has no advantage signal and the runner correctly skips the group.

This is a property of the reward/data combination, not evidence that the RL
code is broken:

- the adapter loads as trainable and generates on CUDA;
- sampling produces distinct completions at higher temperature;
- the reference model and runner complete a smoke run and write artifacts;
- the skip path is the tested `zero_variance_group` behavior.

## Decision

Do **not** run a 500-step RL-from-SFT job that would be mostly no-ops. The old
500-step RL adapter remains invalid under the corrected reward; the SFT adapter
remains the accepted result.

Next experiments, in order:

1. **RL from base with the corrected reward.** The base model has low held-out
   reward (0.02), so it should produce variance; this tests whether RL learns
   real migrations or reward-hacks.
2. **A harder task distribution** with more partial-credit cases, so the
   verifier can separate valid-but-different migrations.
3. **Finer reward granularity** only if it can be done without weakening the
   requirement check.

## Evidence

- `runs/2026-11-03-rl-sft-smoke/`
- `runs/2026-11-03-rl-sft-probe/`
- `runs/2026-11-03-rl-sft-probe-t15/`

Each directory contains `run.json`, `steps.jsonl`, `summary.json`, and
`checkpoints.jsonl`. Adapter weights are gitignored.

## Limitations

- 2- and 10-step probes, one seed, one Windows host.
- Only the first 10 training tasks were sampled.
- Temperature 1.5 changes the policy distribution; it is not the old 500-step
  recipe.
- No held-out evaluation of an RL adapter exists because no RL adapter was
  trained.
