# Paper note — GraphRAG (local→global hierarchical retrieval)

**Claim.** Standard vector RAG fails on sensemaking questions ("summarize the
whole codebase", "what changed across modules?"). GraphRAG extracts entities
and relations, builds a knowledge graph, detects communities, and pre-summarizes
each community to answer global questions (local→global hierarchy).

**Equation.** Retrieval is graph-conditioned: `context = TextUnitRetriever
(local query) ∪ CommunitySummaries(graph-level query)`. No single equation —
the contribution is the data structure (entity graph + hierarchical summaries).

**Experiment (this portfolio).** `GraphRAG-CodeAudit` implements extraction
(Python + tree-sitter TypeScript/JavaScript), community detection (Leiden),
and local/global query. 100 sensemaking questions are published to HF as
`itssoumyad/graphrag-questions-100`; eval results committed in
`experiments/eval_results.json`. Verified this session: 18 Python tests pass;
6 TS-extraction tests error without tree-sitter grammars (CI installs them).

**Limitation.** Extraction quality caps everything downstream — the TS adapter
requires tree-sitter + grammars and is not exercised in minimal environments;
community summarization cost grows with repo size; judge-based eval
(`judge.py`) is heuristic, not exact-match.

**Reproduction task.** Re-run `scripts/evaluate.py` on the committed 100-question
set, join results to the HF dataset card, and record precision@k growth under
community-size sweeps. CPU-feasible.
