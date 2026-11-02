# Project 10 — HEROS-Cloud-Control

**Rank:** 10 (score 90 **[P]**) · **Execution order:** 10 · **Window:** deferred
**Status:** `HEROS-Cloud-SaaS` is a deterministic PLLB simulation, not a
multi-tenant product. No GitHub App, no hosted sandbox, no billing.

## Problem

Teams deploying coding agents need a migration gate and a SOC2-grade receipt
trail. A simulation demonstrates the workflow; it does not demonstrate tenancy,
authorization, or durability.

## Next action

Build the GitHub App/Action dry-run path against 250 real migrations. Do not add
billing or multi-tenancy until the gate is trusted.

## Deliverables

- GitHub App/Action that dry-runs a migration and posts a receipt.
- Signed human approval for `has_data_loss: true`.
- Tamper-evident receipt viewer.
- Hosted sandbox demo with a rollback plan.
- Lighthouse ≥98 and Playwright E2E.

## Gate

250 dry-runs; 100% tamper detection; signed approval enforced; Lighthouse ≥98;
E2E green. A public deployment needs separate approval and a threat model.

## Dependencies and risks

Commercial layer; needs P02 and P07 as the trust substrate. Deferred. Do not
describe the simulation as a product or imply SOC2 compliance.
