# Corrected-reward smoke

**Status:** 10-step smoke with the #107 target-schema check. The check works, but
the base model mostly fails requirement satisfaction. No adapter was saved.

## Configuration

- Base: `Qwen/Qwen2.5-Coder-1.5B-Instruct`, NF4 4-bit
- LoRA: `r=16`, `alpha=32`
- Group size: 2
- Max prompt/completion: 768 / 128
- Seed: 42, temperature 0.7
- Steps: 10
- Code: `f0e22d6` (requirement check merged)

## Result

| Metric | Value |
|---|---:|
| Steps | 10 |
| Optimizer steps | 7 |
| Zero-variance skips | 3 |
| Mean per-step reward | -0.2375 |
| Error codes | 9 `REQUIREMENT_MISS`, 5 `MISSING_BLOCKS`, 4 `SQL_EXEC_ERROR`, 2 `OK` |
| Wall clock | 174.11 s |
| Peak VRAM | 4,154.6 MB |

The no-op loophole is closed: valid but unrelated SQL now loses the execution
reward. The remaining problem is capability, not reward leakage. The base model
does not reliably produce the requested target schema, so another 500-step run
on this prompt would mostly train on negative/zero-variance groups.

## Next step

Build a supervised warm-start or a target-diff prompt that shows the exact
requested change before another RL run. The existing 500-step adapter is invalid
under #107 and must not be published.
