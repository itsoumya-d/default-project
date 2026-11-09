# rlvr-bias-probe

CPU-only, deterministic experiment comparing the **GRPO advantage estimator**
vs **Dr. GRPO** in a synthetic verifiable-reward environment with a spurious
verbosity bonus (reward pays for length, not for solving). Implements the
reproduction task from
`AI_ENGINEERING_PORTFOLIO/research/literature_reviews/length-difficulty-bias-rlvr.md`.

## Question

Does the standard GRPO advantage (`(r − mean) / std`, broadcast to all tokens)
harvest reward from completion *length* in a way Dr. GRPO (mean-centered only)
does not?

## The environment

One simulated prompt per group. A completion is `(solved, length)`.
`reward = 1.0·[solved] + verbosity_bonus·(length / max_len)` — the second term
is spurious: a good policy must raise solve rate, not length. Two arms start at
the same `(skill, verbosity)` and share identical sampled batches; each arm
updates with its own estimator. Deterministic given `--seed`.

## Methods

- N groups × G completions per group; bandit-style policy gradient on
  skill/verbosity (skill: Bernoulli solve margin; verbosity: normalized length).
- GRPO: `A_i = (r_i − mean(r)) / std(r)`. Dr.GRPO: `A_i = r_i − mean(r)`.
- Metrics: mean length, length drift vs group 0, advantage–length Pearson
  correlation, solve rate, mean reward.
- No LLM, no GPU, no network. `random.Random(seed·10000+g)` per group.

## Run

```bash
.venv\Scripts\python.exe -m pytest tests -q
python scripts/run_probe.py --groups 300 --group-size 8 --seed 42 --verbosity-bonus 0.3
```

## Results (2026-11-09, Windows 10, Python 3.11, seeds stamped)

| Metric | GRPO | Dr.GRPO |
|---|---:|---:|
| Mean length | 88.6 | 88.6 |
| Length drift vs group 0 | +12.0 | +12.0 |
| Advantage–length correlation | **0.50** | **0.07** |
| Solve rate | 0.83 | 0.83 |
| Mean reward | 0.96 | 0.96 |
| Final verbosity | 0.77 | 0.51 |

## Interpretation (measured, not claimed beyond the sim)

- Under a spurious length bonus, the standard GRPO advantage **carries a 0.50
  correlation with length** — it attributes reward to long completions as if
  length were skill. Dr.GRPO removes that channel (correlation 0.07).
- Dr.GRPO's verbosity stays at init (0.51) — it does not chase length at all —
  while GRPO inflates it to 0.77. The residual length drift comes from the
  shared batch sampling (both arms are scored on identical rollouts), not from
  the estimator difference; the estimators differ in *attribution*, which is
  exactly the bias the literature names.
- Both arms solve equally well here (0.83) because the task is a bandit with
  no length penalty — the experiment isolates the bias term, not task mastery.
  This matches the P01 finding: a bias-free estimator cannot fix reward content
  that under-pays risk calibration (see `DECISIONS.md` D-2026-11-09-001).

## Limits

Synthetic bandit, not an LLM. Verifies the estimator's attribution behavior,
not end-task gains. The GPU half of the claim (250-step risk-weighted rerun)
is specified in `DECISIONS.md` and remains unrun.

## Files

- `rlvr_bias_probe/__init__.py` — estimators + `run_experiment`
- `tests/test_estimators.py` — 6 tests (determinism, schema, bonus response)
- `scripts/run_probe.py` — runner, writes seed-stamped JSON
- `results/bias-probe.json` — this run's output
