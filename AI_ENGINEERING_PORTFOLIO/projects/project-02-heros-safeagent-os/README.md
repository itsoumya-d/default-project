# Project 02 — HEROS-SafeAgent-OS

**Rank:** 2 (score 97 **[P]**) · **Execution order:** 2 · **Window:** weeks 4–5
**Status:** 500 adversarial cases implemented
([PR #111](https://github.com/itsoumya-d/HEROS/pull/111), merged at `7875f3a`).
Ed25519 root/proof signing and a browser verifier are merged in
[PR #112](https://github.com/itsoumya-d/HEROS/pull/112) (`d0e523f`); the browser
accepted the signed proof and rejected a tampered signature. p99 policy latency
is **0.245 ms** over 5000 samples ([PR #113](https://github.com/itsoumya-d/HEROS/pull/113)),
and the in-process 64-way idempotency lock is merged in
[PR #114](https://github.com/itsoumya-d/HEROS/pull/114). Cross-process 64-worker
replay and the public corpus package remain.

## Problem

An agent runtime needs a tamper-evident audit trail and a hard gate before
destructive actions. HEROS now has a 500-case adversarial corpus, Ed25519-signed
Merkle receipts, a browser proof verifier, a measured p99 policy path, and an
in-process idempotency lock. It still lacks cross-process 64-worker replay, a
standalone public corpus package, and a maintenance story for the 11 shell
scripts (36.5% of code bytes).

## Next action

Package the 500 cases as a standalone dataset with expected verdicts and seeds,
then run the 64-worker cross-process replay torture test against the file
receipt store. Keep the O(n) Merkle-root cost visible: p99 was **33.8 ms** at
5000 receipts with the signed wrapper versus **0.245 ms** for the policy path
alone.

## Deliverables

- `packages/agentic/src/merkle.js`: domain-separated Ed25519 sign/verify.
- 500-case corpus with expected verdicts and seeds (merged; standalone package
  still pending).
- 64-worker cross-process flock/WAL replay torture test (in-process 64-way lock
  merged; cross-process pending).
- Threat model and npm README that match the tests.

## Gate

500 cases; 0 unapproved destructive migrations; p99 policy latency <4.5 ms
(**0.245 ms measured**); 64-way idempotency consistency (**in-process: 1 handler
call, 1 receipt**; cross-process pending); signed proof verifies in a browser
(**PASS**, tampered signature **FAIL**).

## Dependencies and risks

None for the corpus. Signature work depends on a stable receipt schema. npm
publication needs explicit owner approval. If signatures slip, ship the corpus
and unsigned proofs rather than delaying the whole project.
