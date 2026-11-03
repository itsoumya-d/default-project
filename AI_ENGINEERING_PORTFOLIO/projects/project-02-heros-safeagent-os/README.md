# Project 02 — HEROS-SafeAgent-OS

**Rank:** 2 (score 97 **[P]**) · **Execution order:** 2 · **Window:** weeks 4–5
**Status:** **P02 deliverables complete locally; npm release pending.** 500
adversarial cases ([PR #111](https://github.com/itsoumya-d/HEROS/pull/111),
`7875f3a`) are packaged as a 500-record JSONL dataset with a manifest and CI
drift check ([PR #117](https://github.com/itsoumya-d/HEROS/pull/117),
`2658e90`). Ed25519 signed proofs and a browser verifier are merged
([PR #112](https://github.com/itsoumya-d/HEROS/pull/112), `d0e523f`); policy p99
is **0.245 ms** ([PR #113](https://github.com/itsoumya-d/HEROS/pull/113)).
Host-local 64-process idempotency and the threat model are merged
([PR #115](https://github.com/itsoumya-d/HEROS/pull/115), `dc51441`). Merkle
append is incremental at p99 **0.62 ms** for 5200 signed receipts
([PR #116](https://github.com/itsoumya-d/HEROS/pull/116), `d93e7d9`).
`@soumyadebnath1619/agentic@0.3.0` is prepared as a release candidate
([PR #118](https://github.com/itsoumya-d/HEROS/pull/118), `cbee92a`): nine
tarball files including `THREAT_MODEL.md` and `CHANGELOG.md`. Publication needs
owner approval; the shell-script maintenance story remains.

## Problem

An agent runtime needs a tamper-evident audit trail and a hard gate before
destructive actions. HEROS now has a packaged 500-case adversarial corpus,
Ed25519-signed Merkle receipts, a browser proof verifier, a measured p99 policy
path, host-local cross-process idempotency, and a documented threat model. The
remaining gaps are the npm release and a maintenance story for the 11 shell
scripts (36.5% of code bytes).

## Next action

Publish `@soumyadebnath1619/agentic@0.3.0` after explicit owner approval, using
the existing `agentic-v*` tag workflow and provenance. Then write the
shell-script maintenance plan. Keep the remaining limits visible: the file store
still rewrites its whole JSON file and `verify()` is O(n), even though Merkle
root updates are O(log n).

## Deliverables

- `packages/agentic/src/merkle.js`: domain-separated Ed25519 sign/verify
  (merged).
- 500-case corpus with expected verdicts and seeds (merged; packaged as
  `packages/mcp/corpus/corpus.jsonl` in PR #117 with a manifest and CI drift
  check).
- 64-process cross-process replay test (merged in PR #115; host-local file
  locks, not a distributed lock).
- Incremental Merkle frontier: root update O(log n), p99 **0.62 ms** at 5200
  signed receipts (merged in PR #116).
- Threat model and npm README that match the tests (threat model merged in
  PR #115; npm README updated).
- `@soumyadebnath1619/agentic@0.3.0` release candidate: nine files, 22.3 kB
  tarball, `THREAT_MODEL.md` + `CHANGELOG.md` included (PR #118). Publish is
  gated on owner approval.

## Gate

**Met locally:** 500 cases; **500-record JSONL package** with expected verdicts;
0 unapproved destructive migrations; p99 policy latency **0.245 ms** (<4.5 ms);
64-process idempotency **1 handler call, 1 receipt, 63 replays**; signed proof
verifies in a browser (**PASS**) and a tampered signature fails (**FAIL**). The
idempotency guarantee is host-local; multi-host deployments still need a
database-backed store.

## Dependencies and risks

None for the corpus. Signature work depends on a stable receipt schema. npm
publication needs explicit owner approval. If signatures slip, ship the corpus
and unsigned proofs rather than delaying the whole project.
