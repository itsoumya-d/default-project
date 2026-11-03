# Repository Strength Index (RSI)

Owner: Soumya Debnath (`itsoumya-d`)
Baseline date: 2026-11-03
Rubric: the eight-category 100-point scale from the mission brief.
Method: evidence from the live audit (`PORTFOLIO_AUDIT.md`), local clones under
`repos/`, executed test suites, CI logs, and merged PRs. Scores marked **[V]**
are backed by executed checks or merged CI. Scores marked **[D]** rest on
documented claims not re-measured here. Scores marked **[P]** are planning
estimates for repositories that were not deep-dived and must not be quoted as
measurements.

**Do not read this as 30 equal repositories.** The eleven elevated repositories
are where the evidence is. The rest are range evidence.

## 1. Rubric

| # | Category | Points |
|---|---|---:|
| 1 | Technical depth and implementation quality | 20 |
| 2 | Architecture and code maintainability | 15 |
| 3 | Originality and problem significance | 15 |
| 4 | Testing and evaluation | 15 |
| 5 | Documentation and reproducibility | 10 |
| 6 | Production readiness and reliability | 10 |
| 7 | Research foundation and technical credibility | 10 |
| 8 | Presentation and discoverability | 5 |

## 2. Scores — the eleven elevated repositories

| Repository | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Total | Mark |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| peervault | 17 | 12 | 14 | 13 | 8 | 7 | 8 | 4 | **83** | [V]/[D] |
| HEROS | 16 | 12 | 13 | 14 | 8 | 7 | 7 | 4 | **81** | [V] |
| HEROS-Firewall | 14 | 10 | 12 | 12 | 7 | 6 | 6 | 3 | **70** | [D] |
| HEROS-RL | 15 | 11 | 13 | 12 | 8 | 5 | 8 | 3 | **75** | [V] |
| edgeinfer | 13 | 10 | 13 | 11 | 7 | 5 | 7 | 3 | **69** | [V] |
| RouteLLM-Gateway | 12 | 9 | 11 | 9 | 7 | 5 | 6 | 3 | **62** | [D] |
| Reflexion-SWE | 11 | 9 | 11 | 8 | 7 | 4 | 8 | 3 | **61** | [D] |
| GraphRAG-CodeAudit | 11 | 9 | 10 | 8 | 7 | 4 | 7 | 3 | **59** | [D] |
| Anthropic-PerfBench | 12 | 8 | 10 | 7 | 6 | 4 | 7 | 2 | **56** | [D] |
| HEROS-Cloud-SaaS | 10 | 8 | 8 | 6 | 6 | 3 | 4 | 2 | **47** | [D] |
| Mobbin-UI-Compiler | 9 | 8 | 8 | 6 | 6 | 3 | 3 | 2 | **45** | [D] |

Elevated-set average: **(83+81+70+75+69+62+61+59+56+47+45) / 11 = 61.6**

### Per-repository detail

#### peervault — 83 [V]/[D]
- **Evidence [V]:** ML-KEM-768 implementation with 100/100 NIST KAT vectors;
  hybrid P-256 + HKDF-SHA256; 7-layer NTT/invNTT; OPFS/File System sink; AAD
  framing documented; PR #14 (`7025352`, merged) fixed the three README
  contradictions found by the audit. CI 3/3 green.
- **Evidence [D]:** README benchmark claims (p50 0.836 ms handshake; 3.02 MB RSS
  on a synthetic 1 GB stream) were not re-measured in this workspace.
- **Strongest achievement:** a genuinely implemented lattice KEM with KATs, not
  a wrapper around a hosted API.
- **Weakest area:** no independent throughput/RSS reproduction; no external
  adopters; resume claims depend on unverified hardware numbers.
- **Missing:** reproducible benchmark script + logged run; signed release.
- **Priority:** high. **Effort:** small (benchmark script + log).
- **Hiring relevance:** strong for security/protocol roles; distinctive for a
  solo portfolio.

#### HEROS — 81 [V]
- **Evidence [V]:** `npm run test:mcp` 53→54 tests pass; 500 adversarial cases
  (289 pre-existing + 211 added in #111); Ed25519-signed Merkle inclusion
  proofs with a WebCrypto browser verifier (#112); p99 policy latency 0.245 ms
  and p99 signed-Merkle append 0.62 ms measured (#113/#116); 64-process
  cross-process idempotency via exclusive lock file, 8/8 stress runs (#115);
  incremental perfect-subtree frontier removing O(n) root recompute (#116);
  standalone 500-record corpus package with SHA-256 manifest and CI drift
  check (#117); `@soumyadebnath1619/agentic@0.3.0` release candidate packed and
  inspected, **not published** (#118); `rlvr` suite 95 tests; SFT adapter held
  out at **1.90** vs base 0.02 (rows 451–500, #107–#110); threat model with 10
  rows; shell maintenance policy, all 11 scripts shellcheck-clean (#120).
- **Strongest achievement:** the adversarial-corpus + signed-receipt story is
  real, executed, and CI-enforced.
- **Weakest area:** zero external adopters; npm 0.3.0 unpublished (owner
  approval); no cross-language fuzz against a real MCP client; O(n) `verify()`.
- **Missing:** upstream adoption; published release; independent review.
- **Priority:** highest. **Effort:** blocked on owner approval for npm publish.
- **Hiring relevance:** directly on-target for agent-infrastructure and
  AI-safety engineering roles.

#### HEROS-RL — 75 [V]
- **Evidence [V]:** critic-free GRPO engine; 500-case migration dataset; 40
  base tests pass (5 skip); CPU-torch CI; the GPU campaign ran through HEROS
  `rlvr`: SFT warm start (405 examples, 500 steps, loss 1.53→3.1e-5) reached
  **1.90 held-out** (45/50 at 2.0; five `type_narrowing` excluded from SFT);
  RL-from-base 100-step pilot scored 0.13; RL-from-SFT probes had 0/10
  variance groups; old 500-step RL adapter invalid under the #107 requirement
  check and **not published**.
- **Weakness:** the dataset is generated, not human-labeled; no public model
  artifact (no HF token); results live in local run logs.
- **Priority:** high. **Effort:** medium (HF upload blocked on token).
- **Hiring relevance:** strongest single training artifact; publish after
  owner approval with the honest card.

#### HEROS-Firewall — 70 [D]
- **Evidence [D]:** README documents 16 tests, 1,000 adversarial + 200 benign
  payloads, measured FNR/FPR/p99; committed red-team p99 note. Not re-run here.
- **Overlap warning:** largely superseded by HEROS `packages/agentic` +
  the 500-case corpus; treat as the predecessor, not a separate flagship.
- **Priority:** medium. **Effort:** small (link README to HEROS, mark status).

#### edgeinfer — 69 [V]
- **Evidence [V]:** honest README (paged KV documented as not implemented);
  PR #15 (`088c217`) added the WGSL design note with explicit acceptance gates;
  PR #16 (`0d17672`, merged, CI 4/4) added the float32 CPU reference,
  deterministic parity harness, and 8 Python tests (block boundaries, block
  table permutation, out-of-range slots, round-trip); harness round-trips
  20/20 self-check locally; CI job added.
- **Still missing:** the WGSL kernel itself; SmolLM2 token parity; zero-readback
  trace; two-device benchmark; GQA. No speedup claimed.
- **Priority:** high (Project 06). **Effort:** large (kernel + browser bench).
- **Hiring relevance:** inference-engineering signal once the kernel lands.

#### RouteLLM-Gateway — 62 [D]
- **Evidence [D]:** synthetic mock-provider benchmark, 69.40% cost reduction vs
  always-strong, with p50/p95 and cache hit rate; explicitly not MMLU-Pro/GSM8K.
- **Missing:** K>4 meta-router, ONNX export, real-benchmark calibration
  (RouterBench). Project 05.
- **Priority:** medium. **Effort:** medium.

#### Reflexion-SWE — 61 [D]
- **Evidence [D]:** toy deterministic fixtures only; honest labelling; no
  SWE-bench Lite run; no mutation-adequacy gate; no persistent skill library.
- **Missing:** the entire Project 03 scope. Note the dependency: a real
  Lite-50 run needs Docker infra and owner time.
- **Priority:** medium. **Effort:** large.

#### GraphRAG-CodeAudit — 59 [D]
- **Evidence [D]:** local/global search with flat-RAG baseline; Louvain
  default, Leiden optional; synthetic-repo evaluation only.
- **Missing:** AST extraction (Tree-sitter), incremental git-diff update,
  1,000-query real benchmark. Project 07.
- **Priority:** low-medium. **Effort:** large.

#### Anthropic-PerfBench — 56 [D]
- **Evidence [D]:** measured NEON results on Apple Silicon (66.31 GB/s memcpy);
  WGSL shaders provided but never executed; 1 C test file.
- **Missing:** Triton/SAE work (Project 08); any RTX 2060 kernel result.
- **Priority:** medium. **Effort:** medium-large.

#### HEROS-Cloud-SaaS — 47 [D]
- **Evidence [D]:** deterministic PLLB simulation with receipts; explicitly not
  a customer deployment; no multi-tenancy, billing, or GitHub App.
- **Priority:** low. **Effort:** large. **Do not** lead with this.

#### Mobbin-UI-Compiler — 45 [D]
- **Evidence [D]:** fixture Mobbin adapter only; no live Mobbin MCP exists in
  this environment (verified 2026-11-03: no Mobbin MCP tools or resources are
  installed); README says 10 tests; no VLM/Playwright/axe loop.
- **Priority:** low. **Effort:** large.

## 3. Scores — the remaining nineteen repositories (estimates [P])

These were inventoried (language, one-line role) but not deep-dived. Scores are
conservative planning estimates, **not measurements**, and are shown only for
completeness and ranking. Each must be verified before being quoted.

| Repository | Lang | Est. | One-line role | Action |
|---|---|---:|---|---|
| go-ledger | Go | 52 | Idempotent double-entry ledger | Supporting; verify tests |
| llm-control-plane | Python | 45 | Provider-agnostic gateway | Supporting; overlap w/ RouteLLM |
| colpali-edge | Python | 38 | ColPali/edge experiment | Keep as experiment |
| FREED | TypeScript | 35 | App source | No action |
| certiflow-ai | TypeScript | 35 | Compliance automation | No action |
| autopilot-fde | Python | 35 | Forward-deployed agents | No action |
| ghostsearch | HTML | 32 | Client-side retrieval | No action |
| HEROS-Publication | HTML | 30 | HF publication package | Supporting; cross-link HF |
| complaintgraph | Python | 30 | Review mining | No action |
| dotnet-enterprise-api | C# | 30 | ASP.NET orders API | No action |
| compose-cognitive-intervention-engine | Kotlin | 28 | Android reference | No action |
| default-project | — | 25 | This workspace | Keep |
| PlotLLM | Python | 25 | Streamlit plot generator | No action |
| developer-utilities | JavaScript | 20 | Automation scripts | No action |
| factory-monitor | Rust | 20 | Unlabelled | Needs README or archive (approval) |
| itsoumya-d | — | 20 | Profile README | Improve (see NEXT_ACTIONS) |
| ridge_shade | Dart | 18 | Mobile game | No action |
| Yc_ai | TypeScript | 15 | Unlabelled | Needs README or archive (approval) |
| getsmscode-test | JavaScript | 15 | API integration tests | No action |

Estimated average of the nineteen: **30.3 [P]**

## 4. Portfolio-level metrics

| Metric | Value | Mark |
|---|---|---|
| Public repositories | 30 | [V] |
| Elevated (flagship-relevant) | 11 | [V] |
| Elevated-set average RSI | 61.6 | [V]/[D] mixed |
| All-thirty average (est.) | 45.7 | mixed |
| Repositories technically improved in this program | 6 (HEROS, HEROS-RL, peervault, edgeinfer, HEROS-Firewall n/a, HEROS-Cloud-SaaS n/a → HEROS ×19 PRs, peervault #14, edgeinfer #15/#16) | [V] |
| Public model artifacts | 0 | [V] |
| Merged PRs in program | #101–#120, #14, #15, #16 | [V] |
| npm releases published | 0 (agentic 0.3.0 packed, not published) | [V] |

## 5. Improvement ranking (by expected RSI gain per effort)

1. **HEROS** — publish `agentic@0.3.0` (needs owner approval): +2 presentation,
   real artifact gate G4. Small effort, blocked.
2. **HEROS-RL / P01** — HF upload of SFT adapter + card (needs token/approval):
   +3–4 production/artifact. Small effort, blocked.
3. **edgeinfer / P06** — WGSL kernel behind the parity harness: +6–8 on
   technical depth/testing once gates pass. Large effort, not blocked.
4. **peervault** — committed benchmark log (handshake + RSS): +2. Small, not
   blocked.
5. **Reflexion-SWE / P03** — mutation-adequacy gate + Lite-50 pilot: +8 if it
   works. Large, infra-blocked.
6. **RouteLLM-Gateway / P05** — RouterBench calibration: +5. Medium.
7. **Anthropic-PerfBench / P08** — Triton SAE with measured bandwidth: +6.
   Medium-large.
8. **Mobbin-UI-Compiler** — do not invest until a real Mobbin MCP or fixture
   improvement is approved; fixture-only gains cap at +2.
9. **The 19 non-flagship repos** — at most README/metadata fixes; do not
   deep-dive. Two unlabelled repos need a README or an owner decision.

## 6. Re-scoring protocol

- A score moves only when the corresponding evidence is committed and CI/tests
  are green (or a benchmark log exists).
- After every merged PR, update the affected row and this file's averages.
- Never raise a score for documentation alone; docs cap at +1 per category.
- The honesty gate (G7) applies: any number without a log stays [D] or [P].
