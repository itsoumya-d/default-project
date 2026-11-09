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

**Do not read this as 63 equal repositories.** The eleven elevated repositories
are where the evidence is. The rest are range evidence.

**Inventory correction (2026-11-04):** live GitHub profile shows **61 public
repositories** (page 1 = 30, page 2 = 30, page 3 = 1 `craveai-privacy-policy`),
not 30. The prior baseline counted only page 1. A follow-up unauthenticated
GitHub API read the same day reports `public_repos: 63`; the two repositories
visible via API but not in the browser count are `dotnet-enterprise-api` and
`default-project` (both public, both pushed 2026-11-04). The current count used
in this workspace is therefore **63**. The `FREED`, `ridge_shade`,
`developer-utilities`, `getsmscode-test` rows from that baseline no longer
appear on pages 1–3 and are treated as renamed, archived, or private until
confirmed. Newly inventoried repos (page 1: `loanflow`, `image2code-bench`,
`full-stack-open-nextjs`; page 2: `allrtc`, `syncforge`, `ContentForge-AI`,
`mobile-native-design-system`, `flux-social`, `aeo_geo`, `hostshift`,
`swarmcompute`, `vulnhunter`, `meshauth`, `pulsenet`, `greybox-codebase-single-file`,
`syncplay`, `fieldlens__`, `zeroq`, `cybermentor`, `EcoSphere`, `simbook`,
`govpass`, `waitless`, `motion-mcp`, `surface-karya`, `trimium`,
`awesome-zero-server-saas`, `afeedi`, `Nest`, `GRC-Tools`,
`awesome-security-GRC`, `awesome-compliance`, `vc_idias`; page 3:
`craveai-privacy-policy`) are metadata [P] estimates only.

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
| peervault | 17 | 12 | 14 | 13 | 9 | 7 | 8 | 4 | **84** | [V]/[D] |
| HEROS | 16 | 12 | 13 | 14 | 8 | 7 | 7 | 4 | **81** | [V] |
| HEROS-Firewall | 14 | 10 | 12 | 13 | 8 | 6 | 6 | 3 | **72** | [V]/[D] |
| HEROS-RL | 15 | 11 | 13 | 12 | 8 | 5 | 8 | 3 | **75** | [V] |
| edgeinfer | 14 | 10 | 13 | 13 | 7 | 5 | 7 | 3 | **72** | [V] |
| RouteLLM-Gateway | 13 | 9 | 11 | 11 | 8 | 5 | 6 | 3 | **66** | [V]/[D] |
| Reflexion-SWE | 11 | 9 | 11 | 10 | 8 | 4 | 8 | 3 | **64** | [V]/[D] |
| GraphRAG-CodeAudit | 12 | 9 | 10 | 10 | 8 | 4 | 7 | 3 | **63** | [V]/[D] |
| Anthropic-PerfBench | 12 | 8 | 10 | 7 | 6 | 4 | 7 | 2 | **56** | [D] |
| HEROS-Cloud-SaaS | 10 | 8 | 8 | 8 | 7 | 3 | 4 | 2 | **50** | [V]/[D] |
| Mobbin-UI-Compiler | 9 | 8 | 8 | 8 | 7 | 3 | 3 | 2 | **48** | [V]/[D] |

Elevated-set average: **(84+81+72+75+72+66+64+63+56+50+48) / 11 = 66.5** (was
stated as 61.8; that figure did not match the table — the pre-change sum was
711/11 = **64.6**; verified rescoring of peervault 83→84 (Windows bench merged),
RouteLLM 62→66, GraphRAG 59→63, Reflexion 61→64, HEROS-Firewall 70→72,
HEROS-Cloud-SaaS 47→50, and Mobbin-UI-Compiler 45→48 brings it to **66.5**).

### Per-repository detail

#### peervault — 84 [V]/[D]
- **Evidence [V]:** ML-KEM-768 implementation with 100/100 NIST KAT vectors;
  hybrid P-256 + HKDF-SHA256; 7-layer NTT/invNTT; OPFS/File System sink; AAD
  framing documented; PR #14 (`7025352`, merged) fixed the three README
  contradictions found by the audit. CI 3/3 green.
- **Evidence [D]:** README benchmark claims (p50 0.836 ms handshake; 3.02 MB RSS
  on a synthetic 1 GB stream) were not re-measured in this workspace.
- **Windows 11 local run (2026-11-04):** `bench-pqc.mjs` (Node 22.18.0,
  wasm 49,446 bytes restored from the checked-in base64; p50 **2.221 ms**,
  p95 **2.668 ms**; KEM ~0.085 ms/op) and `bench-streaming-memory.mjs`
  (sender delta **39.45 MB**, receiver delta **16.09 MB**; sparse-file /
  discarding-sink, not WebRTC). Raw JSON committed in PR #15
  (`bc12ede`): `sdk/bench-pqc.local.json`, `sdk/bench-memory.local.json`;
  `docs/pqc-validation.md` now carries a Windows 11 subsection. **PR #15 was
  merged on 2026-11-04 at 12:25 UTC** (merge commit `e22fb7f`, 6/6 checks
  green: SDK Node 22/24, Go relay, build, deploy). KATs not re-run (no cargo);
  `npm test` is 11 pass / 9 fail here from a Windows ESM import quirk.
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

#### HEROS-Firewall — 72 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Node 22.18.0):** `npm test` =
  **16/16 pass**; `npm run redteam` reproduced **FNR 0/1,000** and
  **FPR 0/200** exactly, policy p99 **0.230 ms** (macOS reference 0.103 ms;
  machine difference) and 27.68 ms wall time. Raw output committed as
  `results/redteam-windows.json` on branch `docs/windows-redteam-run`,
  commit **`e0e8579`** (not pushed); `RESULTS.md` gains a Windows section.
- **Evidence [D]:** the p99 is policy-engine time only; process spawning,
  downstream MCP, and network latency are excluded.
- **Overlap warning:** largely superseded by HEROS `packages/agentic` +
  the 500-case corpus; treat as the predecessor, not a separate flagship.
- **Priority:** medium. **Effort:** small (link README to HEROS, mark status).

#### edgeinfer — 72 [V] (re-scored 2026-11-04; was 69 on 2026-11-03)
- **Evidence [V]:** honest README (paged KV documented as not implemented in
  the SDK path; kernel is an opt-in building block); PR #15 (`088c217`) added
  the WGSL design note with explicit acceptance gates; PR #16 (`0d17672`,
  merged, CI 4/4) added the float32 CPU reference, deterministic parity
  harness, and 8 Python tests; PR #17 (`8d9e5cc`) fixed Windows test imports
  via `pathToFileURL` (Node suite 113/113); PR #18 (`a501d55`) added GQA head
  mapping in the reference and dense baseline; PR #19 (`96574e7`) added the
  20-prompt SmolLM2-135M-Instruct ORT baseline (FP16 ONNX via `onnxruntime-web`
  CPU, `past_key_values.*`/`present.*` across 30 layers, 542 generated tokens
  recorded); PR #20 (`31a2e77`) added the f32 WGSL paged-attention kernel
  (one workgroup per query head, 64 invocations, online softmax, GQA mapping,
  block table, host-reset status word) with browser result 20/20 synthetic
  cases, max abs 8.43e-8 on Chrome 156 / NVIDIA Turing (RTX 2060); PR #21
  (`1b00c0a`) moved KV storage to f16 with f32 accumulation (browser result
  20/20, max abs 4.79e-8, 40/40 KV buffer creations without `COPY_SRC`/
  `MAP_READ`); local `adb3cb9` (`feat/p06-wgsl-parity`) adds real-geometry
  parity (9 query heads, 3 KV heads, head_dim 64, real ORT `present.*`
  tensors, CPU oracle) with 20/20 cases, max abs 3.53e-8 on RTX 2060, and KV
  memory accounting at **0.033%** overhead (2,949,120 analytic vs 2,950,080
  total; 5% gate passes). Verified 2026-11-04 in this workspace: `npm test`
  **113/113 pass** (9536 ms), Python suite **14/14 pass** (0.105 s), oracle
  re-run writes 20 reference rows.
- **PR #22** (https://github.com/itsoumya-d/edgeinfer/pull/22, head
  `adb3cb9`, +560/−6): CI run 41776945114 **Success, 28 s** — "Paged
  attention reference" (4 s), "Build & test (Node 22.x)", "Build & test
  (Node 24.x)" (matrix: 2 jobs). PR page: "All checks have passed — 4
  successful checks", no conflicts with base, mergeable automatically. Merge
  awaits owner approval.
- **Strongest achievement:** a real f16 WGSL paged-attention kernel validated
  against both synthetic and real-geometry fixtures on owner's GPU hardware,
  with deterministic CPU reference + parity harness + memory accounting.
- **Still missing:** full SmolLM2 token/logit decode parity (attention-geometry
  parity is proven, not end-to-end decode); validation-layer `mapAsync` trace
  (zero-readback is a runtime buffer-usage check, 40/40 clean); two-device
  p50/p95; Firefox; fallback flag wiring into the SDK; no speedup claimed.
- **Priority:** high (Project 06). **Effort:** large (decode parity + trace +
  two-device bench).
- **Hiring relevance:** inference-engineering signal; kernel + harness +
  honest negative gates (no speedup claim before measurement).

#### RouteLLM-Gateway — 66 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Node 22.18.0):** `npm test` = **19/19
  pass** (16 before the local canonical-JSON test); `npm run evaluate`
  reproduced the committed table exactly — always-strong 98.80% at $0.5000,
  always-weak 86.80% at $0.0500, router 97.20% at $0.1868, router+cache 97.20%
  at $0.1530 with a **13.6%** cache hit; threshold 0.74, retention 98.38%,
  cost reduction **69.40%**.
- **Evidence [D]:** the providers are deterministic mocks; this is not
  MMLU-Pro/GSM8K or RouterBench. No real API credentials were used.
- **Prepared locally (not pushed):** branch `feat/reproducible-pareto`,
  commit **`d86f178`**. Adds `src/canonical.js` (rounds non-integer floats to
  12 decimals before writing `results/pareto.json`) plus 3 tests. Motivation:
  the committed artifact went dirty after every local run from IEEE-754
  last-digit drift (`0.07750784705788455` vs `...52`); two consecutive runs now
  produce the same SHA-256. `RESULTS.md` gains a Windows reproduction section;
  README test count 16 → 19.
- **Missing:** K>4 meta-router, ONNX export, real-benchmark calibration
  (RouterBench). Project 05.
- **Priority:** medium. **Effort:** medium.

#### Reflexion-SWE — 64 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Python 3.11.13):** `pytest` =
  **37 passed, 3 skipped** (skips are Rust sandbox tests; `rustc` is not
  installed) = 40 total, matching `RESULTS.md`; `python
  scripts/run_ablation.py` reproduced the full mechanism table exactly
  (base/no_testgen 0.000 pass@1; no_reflection 3.00 mean attempts; full and
  tf_grpo 1.000 pass@1; 6 priors from 24 rollouts). The committed
  `experiments/toy_ablation.json` was already byte-stable — no code change was
  needed, so no branch was prepared.
- **Evidence [D]:** toy deterministic fixtures only; no SWE-bench Lite or
  HumanEval Rust run; no LLM judge or model-dependent Pass@1.
- **Missing:** the entire Project 03 model-dependent scope. Note the
  dependency: a real Lite-50 run needs Docker infra and owner time.
- **Priority:** medium. **Effort:** large.

#### GraphRAG-CodeAudit — 63 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Python 3.11.13):** `pytest` =
  **24/24 pass** (22 before the local label fix, including the new
  TypeScript/JavaScript tree-sitter suite); `python scripts/evaluate.py`
  reproduced the committed table exactly — GraphRAG average **7.58** vs flat
  **7.07**, comprehensiveness 8.58/8.58, diversity 10.00/10.00, empowerment
  4.01/2.28, directness 7.72/7.40, head-to-head **64/100 (64.0%)**.
- **Evidence [D]:** the judge is a deterministic rubric, not an LLM; the corpus
  is a 5-file synthetic repo. Leiden is not installed (`louvain-fallback`).
- **Prepared locally (not pushed):** branch `fix/reproducible-eval-label`,
  commit **`c9b51e7`**. The committed artifact embedded the author's absolute
  macOS path, so any run elsewhere dirtied `experiments/eval_results.json`;
  the harness now records `data/sample_repo` relative to the project root and
  two runs are byte-identical. 2 new tests; `RESULTS.md` gains a Windows
  reproduction section.
- **Missing:** AST extraction for more languages (Tree-sitter now covers
  TS/JS), incremental git-diff update, 1,000-query real benchmark. Project 07.
- **Priority:** low-medium. **Effort:** large.

#### Anthropic-PerfBench — 56 [D]
- **Evidence [D]:** measured NEON results on Apple Silicon (66.31 GB/s memcpy);
  WGSL shaders provided but never executed; 1 C test file.
- **Could not be re-run here (2026-11-04):** no C compiler (`cc`/`gcc`/`clang`),
  no `make`, and no `cargo`/`rustc` on this Windows host. The native NEON
  results are ARM-only and the WASM path needs the Rust toolchain. The score is
  unchanged and the native/WASM numbers remain `[D]`.
- **Missing:** Triton/SAE work (Project 08); any RTX 2060 kernel result.
- **Priority:** medium. **Effort:** medium-large.

#### HEROS-Cloud-SaaS — 50 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Python 3.11.13):** `pytest` =
  **6/6 pass**; `python scripts/evaluate.py` reproduced completion
  **0.7000 → 1.0000** (+30.00 pp), receipt coverage 1.0/1.0, policy
  applications 0/20, 4 drafts, 4 approved. Only millisecond timings differ
  (0.038/0.032 vs 0.030/0.017).
- **Prepared locally (not pushed):** branch `docs/windows-eval-run`, commit
  **`0096a7d`** — adds `results/eval-windows.json` and a Windows section to
  `RESULTS.md`; the macOS artifact is left intact.
- **Evidence [D]:** deterministic PLLB simulation with receipts; explicitly not
  a customer deployment; no multi-tenancy, billing, or GitHub App.
- **Priority:** low. **Effort:** large. **Do not** lead with this.

#### Mobbin-UI-Compiler — 48 [V]/[D]
- **Evidence [V] (2026-11-04, Windows 11 / Node 22.18.0):** `npm test` =
  **10/10 pass**; `node bin/mobbin-compile.mjs --surface all` regenerated all
  five surfaces, and every generated file is **byte-identical to HEAD**
  (verified by SHA-256 and `git cat-file`). The regenerated count and app list
  match `RESULTS.md`: KYC 2 refs (Revolut, Monzo), paywall 2 (Stripe, Revolut),
  dashboard 5 (Linear, Stripe, Notion, Perplexity), chat 2 (Claude,
  Perplexity), billing 1 (Stripe).
- **Evidence [D]:** fixture Mobbin adapter only; no live Mobbin MCP exists in
  this environment; no VLM/Playwright/axe loop.
- **Priority:** low. **Effort:** large.

## 2b. Verified deep-dives outside the elevated eleven

Not promoted into §2 (that set is deliberately stable), but no longer [P]
metadata rows. Evidence collected 2026-11-04 by shallow-cloning the public
repos and running their suites locally. Subjective categories remain [P].

| Repository | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | Total | Mark |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| autopilot-fde | 18 | 13 | 14 | 15 | 9 | 7 | 4 | 4 | **84** | [V] tests/CI; [P] subjective |
| llm-control-plane | 16 | 12 | 12 | 13 | 8 | 6 | 4 | 4 | **75** | [V] tests/CI; [P] subjective |

### llm-control-plane — 75

- **Evidence [V]:** 54 tests before the local change, **61 after**; statement
  coverage 94% → **95%** against a 90% CI gate; `ruff check` clean; CI matrix
  Python 3.9/3.11/3.12 plus a package-build job. Core is dependency-free;
  FastAPI is an optional extra.
- **Strongest:** idempotent per tenant/trace requests, hash-chained verifiable
  audit log, deterministic routing/failover, PII redaction, versioned evals.
- **Weakest:** in-memory only (no durable audit store), no committed benchmark
  log, no distributed tracing, no multi-process or crash-recovery test.
- **Prepared locally (not pushed):** branch `feat/metrics-label-escaping`,
  commit **`8d958c7`**. Escapes Prometheus label values (`\`, `"`, `\n`) and
  validates metric/label names; before the fix a tenant id containing `"` or a
  newline could corrupt `/metrics` or inject samples. Seven new tests.
- **Next upgrade:** durable audit store (SQLite) + committed p50/p95
  gateway-overhead log + crash-recovery test.

### autopilot-fde — 84

- **Evidence [V]:** **436 passed, 1 skipped, 154 subtests** (11.45 s) on the
  backend suite after the local fix; **100% statement coverage** of `backend`
  (3,473 statements) against a CI gate of 100%; `ruff check backend/ tests/
  scripts/` clean; CI adds Python 3.12/3.13/3.14, a real-LangGraph runtime job,
  and frontend lint/vitest/typecheck/build. 34 backend test files plus 19
  frontend test files.
- **Strongest:** unusually broad verified surface for a prototype — ingestion
  connectors, deterministic discovery/OCPM export, APS scoring with Monte Carlo,
  approval-gated code generation, MCP HTTP surface, cost attribution, PII
  scrubbing, Docker, and a paper draft with formal definitions.
- **Weakest:** the paper presented fixture-based results as an "empirical
  evaluation across 8 enterprise departments and 158 traces" while the README
  correctly calls the scenarios fictional; the table itself lists 7 processes /
  36 traces. That inconsistency is a credibility risk under ADR-006, so research
  credibility is scored 4/10 pending correction.
- **Prepared locally (not pushed):** branch `fix/paper-synthetic-claims`,
  commit **`265c25e`**. Renames the section to "Synthetic Benchmark
  Evaluation", adds a no-customer-data statement, removes the unsupported
  "first system"/"158 traces"/"verified" language, and softens the conclusion.
  Research score rises to ~6 once merged.
- **Also prepared:** branch `fix/windows-portability`, commit **`bccb8c3`**.
  Two Windows-only failures fixed: a path assertion using `str(path)` instead
  of `as_posix()`, and a POSIX-shell + `jq` test that now skips on Windows
  instead of failing. Suite before: 2 failed; after: 436 pass, 1 skip.
- **Note:** the README's apparent `�` characters are a Windows console
  rendering artifact, not file corruption. Direct byte inspection shows valid
  UTF-8 with `·` and `×`; no README edit was made.

## 3. Scores — the remaining repositories (estimates [P])

These were inventoried (language, one-line role) but not deep-dived. Scores are
conservative planning estimates, **not measurements**, and are shown only for
completeness and ranking. Each must be verified before being quoted. Live
inventory: 63 public repos = 11 elevated (§2) + 2 verified deep-dives (§2b) + 50
below (metadata only or [P] estimates).

| Repository | Lang | Est. | One-line role | Action |
|---|---|---:|---|---|
| go-ledger | Go | 52 | Idempotent double-entry ledger | Supporting; verify tests |
| llm-control-plane | Python | 75 [V] tests/CI | Provider-agnostic gateway, hash-chained audit, evals | **Deep-dived (§2b)**; local metrics-escaping fix `8d958c7` awaits approval |
| colpali-edge | Python | 38 | ColPali/edge experiment | Keep as experiment |
| certiflow-ai | TypeScript | 35 | Compliance automation | No action |
| autopilot-fde | Python/TS | 84 [V] tests/CI | FDE workflow discovery, APS scoring, approval-gated agents | **Deep-dived (§2b)**; local paper-scope `265c25e` and portability `bccb8c3` await approval |
| ghostsearch | HTML | 32 | Client-side retrieval | No action |
| HEROS-Publication | HTML | 30 | HF publication package | Supporting; cross-link HF |
| complaintgraph | Python | 30 | Review mining | No action |
| dotnet-enterprise-api | C# | 30 | ASP.NET orders API | No action |
| compose-cognitive-intervention-engine | Kotlin | 28 | Android reference | No action |
| default-project | — | 25 | This workspace | Keep |
| PlotLLM | Python | 25 | Streamlit plot generator | No action |
| factory-monitor | Rust | 20 | Unlabelled | Needs README or archive (approval) |
| itsoumya-d | — | 20 | Profile README | Improve (see NEXT_ACTIONS) |
| Yc_ai | TypeScript | 15 | Unlabelled | Needs README or archive (approval) |
| loanflow | PHP | — [P] | Clean-room regulated lending platform (Laravel 13/PHP 8.x, OAuth 2.0, Keap, WordPress, BigQuery, GTM) | Metadata only; candidate for deep-dive if flagged |
| image2code-bench | Python | — [P] | Reference-image → HTML/CSS/SVG reconstruction with pixel/edge/palette metrics | Metadata only; P04-adjacent |
| full-stack-open-nextjs | TypeScript | — [P] | Full Stack Open (U Helsinki) Next.js course solutions | Keep as study record |
| mscp-game | Dart | — [P] | Unlabelled (Dart) | No action |
| allrtc | HTML | — [P] | P2P WebRTC live streaming and transport telemetry | Metadata only |
| syncforge | HTML | — [P] | CRDT local-first state and continual agent memory sync engine | Metadata only; P-memory adjacent |
| ContentForge-AI | TypeScript | — [P] | Document parsing and structured content analysis pipeline | Metadata only; now public (was "not present" in prior audit) |
| mobile-native-design-system | Python | — [P] | Flutter-first native mobile design/motion/token/audit plugin for Codex | Metadata only; now public; P04-adjacent |
| flux-social | TypeScript | — [P] | Unlabelled (TypeScript) | Needs README or archive (approval) |
| aeo_geo | TypeScript | — [P] | Unlabelled (TypeScript) | Needs README or archive (approval) |
| hostshift | Python | — [P] | Cross-platform multi-host UI evaluation harness for computer-use agents; 142/142 CI tests claimed | Metadata only; computer-use eval adjacent |
| swarmcompute | HTML | — [P] | Browser WASM decentralized low-communication ML compute mesh | Metadata only; now public (prior "confirm" gate is moot) |
| vulnhunter | Python | — [P] | AI-powered OWASP security scanner for public GitHub repos | Metadata only |
| meshauth | HTML | — [P] | WebAuthn/Passkey passwordless auth and cryptographic source signatures | Metadata only |
| pulsenet | HTML | — [P] | Privacy-first client-side analytics with bounded delivery recovery | Metadata only; now public |
| greybox-codebase-single-file | TypeScript | — [P] | Single-file snapshot of the Greybox workspace | No action |
| syncplay | HTML | — [P] | P2P real-time multiplayer game state engine | No action |
| fieldlens__ | TypeScript | — [P] | FieldLens AI coaching app for tradespeople (Expo React Native) | No action |
| zeroq | HTML | — [P] | Serverless P2P message queue (pub/sub + work queues) | Metadata only |
| cybermentor | HTML | — [P] | AI-powered OWASP security learning platform (hackathon) | No action |
| EcoSphere | Dart | — [P] | Unlabelled (Dart) | Now public; needs README or archive (approval) |
| simbook | Dart | — [P] | Unlabelled (Dart) | Needs README or archive (approval) |
| govpass | TypeScript | — [P] | Government forms navigator and auto-fill assistant (React Native + Expo) | No action |
| waitless | Dart | — [P] | Unlabelled (Dart) | Needs README or archive (approval) |
| motion-mcp | TypeScript | — [P] | AI-native codebase-aware motion generation MCP server | Metadata only; MCP-adjacent |
| surface-karya | — | — [P] | Cross-platform Generative UI + HITL agent runtime build plan | Metadata only |
| trimium | — | — [P] | Unlabelled | Needs README or archive (approval) |
| awesome-zero-server-saas | — | — [P] | Curated zero-server/privacy-first SaaS alternatives list | No action |
| afeedi | Dart | — [P] | Unlabelled (Dart) | Needs README or archive (approval) |
| Nest | Python | — [P] | OWASP gateway/discovery project | No action |
| GRC-Tools | — | — [P] | Curated GRC tools list | No action |
| awesome-security-GRC | — | — [P] | Curated security GRC resources | No action |
| awesome-compliance | Astro | — [P] | Curated IT compliance tools/resources | No action |
| vc_idias | — | — [P] | Unlabelled | Needs README or archive (approval) |
| craveai-privacy-policy | HTML | — [P] | Unlabelled privacy policy (2025-06) | No action |

Prior baseline rows `FREED`, `ridge_shade`, `developer-utilities`,
`getsmscode-test` are **not on pages 1–3** in the 2026-11-04 inventory.
Treat as renamed/archived/private until confirmed; do not quote those scores.

Estimated average of the original nineteen (excluding the four vanished rows,
which are held pending confirmation): **32.1 [P]** — previously stated 30.3
included the four now-unverifiable rows. The 31 newly inventoried repos have
no numeric estimate; metadata only.

## 4. Portfolio-level metrics

| Metric | Value | Mark |
|---|---|---|
| Public repositories | 63 | [V] 2026-11-04 GitHub API (30 at the 2026-11-02 audit; 61 at the 2026-11-04 browser count) |
| Elevated (flagship-relevant) | 11 | [V] |
| Verified deep-dives outside the elevated set | 2 (`autopilot-fde` 84, `llm-control-plane` 75) | [V] tests/CI; [P] subjective |
| Elevated-set average RSI | 66.5 | [V]/[D] mixed (seven verified rescoring changes; the prior 61.8 did not match the table — pre-change sum was 64.6) |
| All-63 average (est.) | not meaningful | metadata [P] only; 32 repos have no numeric estimate |
| Repositories technically improved in this program | 6 (HEROS, HEROS-RL, peervault, edgeinfer, HEROS-Firewall n/a, HEROS-Cloud-SaaS n/a → HEROS ×19 PRs, peervault #14, edgeinfer #15–#21, #16–#21, plus local adb3cb9 unmerged) | [V] |
| Public model artifacts | 0 | [V] |
| Merged PRs in program | #101–#120, #14, #15, #16–#21, plus local edgeinfer adb3cb9 (real-geometry parity, unmerged) | [V] |
| npm releases published | 0 (agentic 0.3.0 packed, not published) | [V] |

## 5. Improvement ranking (by expected RSI gain per effort)

1. **HEROS** — publish `agentic@0.3.0` (needs owner approval): +2 presentation,
   real artifact gate G4. Small effort, blocked.
2. **HEROS-RL / P01** — HF upload of SFT adapter + card (needs token/approval):
   +3–4 production/artifact. Small effort, blocked.
3. **edgeinfer / P06** — WGSL kernel behind the parity harness: +6–8 on
   technical depth/testing once gates pass. Large effort, not blocked.
4. **peervault** — committed benchmark log (handshake + RSS): **DONE locally**
   (Windows 11 numbers in PR #15 `bc12ede`; 4/4 checks green). Merge blocked on
   owner approval.
5. **Reflexion-SWE / P03** — mutation-adequacy gate + Lite-50 pilot: +8 if it
   works. Large, infra-blocked.
6. **RouteLLM-Gateway / P05** — RouterBench calibration: +5. Medium.
7. **Anthropic-PerfBench / P08** — Triton SAE with measured bandwidth: +6.
   Medium-large.
8. **Mobbin-UI-Compiler** — do not invest until a real Mobbin MCP or fixture
   improvement is approved; fixture-only gains cap at +2.
9. **The 50 non-flagship repos** — at most README/metadata fixes; do not
   deep-dive. Twelve unlabelled repos need a README or an owner decision:
   `Yc_ai`, `factory-monitor`, `flux-social`, `aeo_geo`, `EcoSphere`,
   `simbook`, `waitless`, `trimium`, `afeedi`, `vc_idias`, `mscp-game`, and
   (private/renamed) `FREED`, `ridge_shade`, `developer-utilities`,
   `getsmscode-test` pending confirmation. The previously flagged
   `ContentForge-AI`, `EcoSphere`, `hostshift`, `swarmcompute`,
   `mobile-native-design-system`, `pulseNet` are now public — the "confirm
   before touching" gate is moot; treat as metadata [P] rows.

## 6. Re-scoring protocol

- A score moves only when the corresponding evidence is committed and CI/tests
  are green (or a benchmark log exists).
- After every merged PR, update the affected row and this file's averages.
- Never raise a score for documentation alone; docs cap at +1 per category.
- The honesty gate (G7) applies: any number without a log stays [D] or [P].
