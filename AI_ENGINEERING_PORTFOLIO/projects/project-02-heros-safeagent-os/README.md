# Project 02 — HEROS-SafeAgent-OS

**Rank:** 2 (score 97 **[P]**) · **Execution order:** 2 · **Window:** weeks 4–5
**Status:** **Acceptance gate met locally; publication pending.** 500 adversarial
cases ([PR #111](https://github.com/itsoumya-d/HEROS/pull/111), `7875f3a`),
Ed25519 signed proofs and a browser verifier
([PR #112](https://github.com/itsoumya-d/HEROS/pull/112), `d0e523f`), p99 policy
latency **0.245 ms** ([PR #113](https://github.com/itsoumya-d/HEROS/pull/113)),
and host-local 64-process idempotency
([PR #115](https://github.com/itsoumya-d/HEROS/pull/115), `dc51441`) are merged.
The threat model is `packages/agentic/THREAT_MODEL.md`. The standalone public
corpus package and npm release remain; npm publication needs owner approval.

## Problem

An agent runtime needs a tamper-evident audit trail and a hard gate before
destructive actions. HEROS now has a 500-case adversarial corpus, Ed25519-signed
Merkle receipts, a browser proof verifier, a measured p99 policy path, and
host-local cross-process idempotency. It still lacks a standalone public corpus
package and a maintenance story for the 11 shell scripts (36.5% of code bytes).

## Next action

Package the 500 cases as a standalone dataset with expected verdicts and seeds,
and add a runner that consumes the package. Keep the O(n) Merkle-root cost
visible: p99 was **33.8 ms** at 5000 receipts with the signed wrapper versus
**0.245 ms** for the policy path alone.

## Deliverables

- `packages/agentic/src/merkle.js`: domain-separated Ed25519 sign/verify
  (merged).
- 500-case corpus with expected verdicts and seeds (merged; standalone package
  still pending).
- 64-process cross-process replay test (merged in PR #115; host-local file
  locks, not a distributed lock).
- Threat model and npm README that match the tests (threat model merged in
  PR #115; npm README updated).

## Gate

**Met locally:** 500 cases; 0 unapproved destructive migrations; p99 policy
latency **0.245 ms** (<4.5 ms); 64-process idempotency **1 handler call, 1
receipt, 63 replays**; signed proof verifies in a browser (**PASS**) and a
tampered signature fails (**FAIL**). The idempotency guarantee is host-local;
multi-host deployments still need a database-backed store.

## Dependencies and risks

None for the corpus. Signature work depends on a stable receipt schema. npm
publication needs explicit owner approval. If signatures slip, ship the corpus
and unsigned proofs rather than delaying the whole project.
