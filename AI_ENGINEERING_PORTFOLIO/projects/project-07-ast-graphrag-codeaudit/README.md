# Project 07 — AST-GraphRAG-CodeAudit

**Rank:** 7 (score 90 **[P]**) · **Execution order:** 7 · **Window:** deferred
**Status:** regex/LLM extraction over a synthetic repository; no deterministic
AST graph, no Leiden communities, no incremental invalidation.

## Problem

Microsoft GraphRAG's LLM entity extraction is expensive and hallucinates edges.
For code, entity extraction does not need a model: the parser already knows the
structure.

## Next action

Build the Tree-sitter AST + taint graph on one real repository and measure
Recall@10 before adding communities. The deterministic index is the contribution.

## Deliverables

- Tree-sitter AST + taint graph, no LLM in the indexing path.
- Leiden community detection with a stable seed.
- Git-diff incremental invalidation.
- `ast-graphrag-codebench-1000`: 10 real repositories, 1,000 queries.
- Cytoscape.js inspector.

## Gate

Recall@10 >0.88; ≥90% indexing-token reduction vs an LLM baseline; <800 ms
incremental update; subgraph F1 reported.

## Dependencies and risks

CPU-only and independent, so it can run while GPU work is queued. Deferred in
the 14-week plan; do not start it before P01 and P02 pass their gates.
