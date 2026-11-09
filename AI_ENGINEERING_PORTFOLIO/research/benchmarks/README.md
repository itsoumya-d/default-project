# Benchmarks

Measurement protocols and result snapshots. The per-project protocols live with
the projects; this directory is for cross-project comparisons.

**Status:** 2026-11-09 benchmark run. See `RESULTS_2026-11-09.md` and
`results/cross-bench.json` (15 suites: 11 green, 4 with local-env-only
missing-dep failures, 1 GPU-dependent). Runner: `run_cross_project_bench.py`.

Rules:

- Every result records hardware, software versions, seed, sample size, and the
  exact command.
- A number without a log is deleted, not footnoted.
- Negative and null results are kept.
