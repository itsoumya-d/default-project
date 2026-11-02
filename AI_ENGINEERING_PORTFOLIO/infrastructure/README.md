# Infrastructure — Runbooks and Measurement Harness

This directory holds the operational layer that keeps the portfolio projects
reproducible on free or already-owned hardware. It is not a product.

**Status:** empty scaffold. The strategy is in `../INFRASTRUCTURE_STRATEGY.md`;
nothing here has been implemented or measured yet.

## Planned contents

| Path | Purpose | State |
|---|---|---|
| `runbooks/rtx2060-qlora.md` | 1.5B NF4 environment, OOM ladder, checkpoint policy | Planned |
| `runbooks/kaggle-2xt4.md` | session bootstrap, dataset mount, resume | Planned |
| `benchmarks/` | hardware/version capture and result schema | Planned |
| `costs/` | free-tier quota table with a "verified on" date | Planned |
| `incidents/` | dated failures and fixes (ACL, OOM, CUDA, quota) | Planned |

## Rules

- Every runbook starts from a clean checkout and ends with a command that proves
  the environment works.
- Every quota number carries a verification date; provider limits change.
- No secret, token, or private path is committed. Use environment variables.
- A runbook that has not been executed is marked **draft**, not **verified**.
