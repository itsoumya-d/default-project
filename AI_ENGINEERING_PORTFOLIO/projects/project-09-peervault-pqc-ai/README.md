# Project 09 — PeerVault-PQC-AI

**Rank:** 8 (score 91 **[P]**) · **Execution order:** 8 · **Window:** deferred
**Status:** PQC channel, OPFS sink, and manual chunk bitmap exist. PR #2 fixes
the two README contradictions. No automatic journal, no cross-reload resume, no
model-shard streaming.

## Problem

Browser transfers fail on tab reload; OPFS resume is manual; model artifacts are
too large for chat apps. The crypto is already documented and tested; the gap is
durability and the AI artifact path.

## Next action

Implement the persistent `ChunkBitmap` journal and a cross-reload resume test
before touching model shards. Durability is the user-visible failure.

## Deliverables

- Persistent chunk journal in OPFS/IndexedDB.
- Cross-reload resume with a checksum-verified final artifact.
- Encrypted `.safetensors` / `.onnx` shard streaming into
  `EdgeInfer.fromBuffer()`.
- 100/100 KAT and a <64 MB receiver RSS measurement on a 500 MB transfer.
- npm package.

## Gate

100/100 KAT; <64 MB RSS on 500 MB; a real cross-reload resume test; npm release.
Do not merge or cite `swarmcompute` until the owner confirms it is public.

## Dependencies and risks

Needs P06's `fromBuffer()` path and P02's receipts. Deferred in the 14-week plan.
The security architecture is already strong; do not rewrite it to chase a
headline.
