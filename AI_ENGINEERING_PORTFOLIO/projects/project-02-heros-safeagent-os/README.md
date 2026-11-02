# Project 02 — HEROS-SafeAgent-OS

**Rank:** 2 (score 97 **[P]**) · **Execution order:** 2 · **Window:** weeks 4–5
**Status:** closest project to done; 289 adversarial cases verified, public
500-case corpus and signed proofs missing.

## Problem

An agent runtime needs a tamper-evident audit trail and a hard gate before
destructive actions. HEROS already has Merkle receipts, SQLite shadow gates, and
289 adversarial cases. It does not have Ed25519-signed sparse Merkle inclusion
proofs, a public 500-case corpus, or a maintenance story for the 11 shell
scripts (36.5% of code bytes).

## Next action

Map the existing 289 cases to OWASP ASI01–ASI10, then add 211 deterministic
cases. Do this before touching the signature code; the corpus is the asset.

## Deliverables

- `packages/mcp/src/merkle.ts`: domain-separated leaves, Ed25519 sign/verify.
- 500-case corpus with expected verdicts and seeds.
- 64-worker flock/WAL replay torture test.
- Threat model and npm README that match the tests.

## Gate

500 cases; 0 unapproved destructive migrations; p99 policy latency <4.5 ms; 100%
idempotency under 64 parallel replays; proof verifies in a browser.

## Dependencies and risks

None for the corpus. Signature work depends on a stable receipt schema. npm
publication needs explicit owner approval. If signatures slip, ship the corpus
and unsigned proofs rather than delaying the whole project.
