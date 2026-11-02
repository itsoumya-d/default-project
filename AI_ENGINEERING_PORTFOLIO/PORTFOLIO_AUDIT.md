# Portfolio Audit — Verified Baseline

Owner: **Soumya Debnath** (`itsoumya-d`, `itssoumyad`)
Audit date: **2026-11-02**
Method: live Kimi browser inspection of GitHub and Hugging Face, shallow git
clones, byte/test inventories, and local test execution.

**Read this first.** The audit scores below are **planning estimates [P]**, not
measurements. The previous brief's 100-point scores were supplied without a
reproducible rubric calculation. This document keeps them where they are useful
for ranking, adds the live evidence, and marks every claim that is already
contradicted. A score becomes **[V]** only when the rubric evidence exists and a
command reproduces it.

---

## 1. Executive summary

1. **The estate is larger than the brief.** The public GitHub profile has **30
   repositories**, not 11. Eleven are materially relevant to this portfolio; the
   rest are unrelated utilities, games, or older experiments.
2. **`HEROS-RL` already exists and is the real Project 01 base.** It contains a
   critic-free GRPO engine, a 500-case migration dataset, a toy group-size
   ablation, and TRL/Unsloth training scripts. It has **40 passing tests (5
   skipped)** and a CPU-torch CI job. It does **not** contain a 1.5B training
   result. Rebuilding it would be waste; wiring it to the shadow verifier and
   running the GPU job is the work.
3. **The strongest verified engineering asset is HEROS.** `npm run test:mcp`
   passes **46 test functions** containing **289 adversarial cases**
   (60 + 78 + 31 + 60 + 30 + 30). The `rlvr` package passes **34 baseline tests**
   and **78 tests** after the verifier + runner slice.
4. **Three brief claims are stale.** `peervault` already documents its PQC and
   OPFS implementation; `edgeinfer` does not say "Replaces OpenAI API"; and the
   HEROS shell ratio is **36.5% of code bytes** (7.6% of all repo bytes), not
   72.8%. The real peervault issues are two narrow README contradictions, and
   the real edgeinfer gap is the missing paged kernel.
5. **The frontier gap is empirical, not architectural.** There are **0 public
   model weights** and **0 GPU training logs**. Ten HF Spaces and two datasets
   demonstrate systems, but no trained artifact. Project 01 is the shortest path
   to closing that gap.

---

## 2. Scoring rubric (100 points)

| Dimension | Points | What earns the points | What does not |
|---|---:|---|---|
| Architectural originality and problem complexity | 25 | First-principles systems/math; a real constraint the design resolves | Tutorial wrappers; API-call chains |
| Code quality, memory/concurrency safety, maintainability | 20 | Typing, modular isolation, atomic writes/locking, no `eval`, documented failure boundaries | Single-file demos; unbounded memory |
| Verification, adversarial testing, CI rigor | 20 | Unit + adversarial corpora, KATs, deterministic fixtures, CI on multiple OS/runtimes | Tests that only assert a mock was called |
| Empirical benchmarking and reproducibility | 20 | Real hardware logs, ablations, published checkpoints, seeds, variance | Synthetic fixtures presented as model results |
| Documentation honesty and production packaging | 15 | Self-describing schemas, threat models, synchronized limitations, installable artifacts | Hyperbole; stale limitations; unpinned deps |

---

## 3. Live inventory — the eleven relevant repositories

Test-file counts are **[V]** from the filesystem. "Documented tests" are **[D]**
from each README and were not all re-run in this session.

| # | Repository | Stack | What it actually is | Last commit | Test evidence | Brief score | Live band | Disposition |
|---:|---|---|---|---|---|---:|---:|---|
| 1 | `HEROS` | JS/Node 22, Python, Zero, Shell | MCP 2025-11-25 runtime, forge/ledger, agentic SDK, rlvr | 2026-10-31 | 16 test files; 46 MCP test functions pass; 289 adversarial cases; 34→78 rlvr tests | 82 | 82–86 | **Elevate.** #101 adds the GPU-trainer slice; #102 adds the runner. |
| 2 | `HEROS-RL` | Python | Critic-free GRPO for zero-downtime Postgres migrations; 500-case dataset | 2026-11-01 | 6 test files; **40 pass, 5 skip**; CPU-torch CI | not in brief | 78–84 | **Elevate as Project 01 base.** Run the 1.5B job. |
| 3 | `peervault` | TypeScript, Rust→WASM, Go relay | Zero-server WebRTC E2EE transfer; ML-KEM-768 + P-256 hybrid; OPFS sink | 2026-10-31 | 11 test files; README claims 89/89 SDK tests, 100/100 KATs | 78 | 78–84 | **Elevate.** #14 fixes two doc contradictions. |
| 4 | `edgeinfer` | TypeScript, WebGPU, ONNX | Browser inference, Matryoshka two-stage retrieval, γ=5 speculative decoding | 2026-10-31 | 10 test files; README claims 106 tests | 75 | 74–80 | **Elevate.** #15 adds the WGSL design note. |
| 5 | `Reflexion-SWE` | Python | Actor/Evaluator/Reflection code-repair agent; toy-fixture evaluation | 2026-10-31 | 7 test files; measured toy results, not HumanEval/SWE-bench | — | 72–78 | **Project 03 base.** Add mutation gate + real benchmark. |
| 6 | `RouteLLM-Gateway` | JS/Python | Bradley-Terry router, semantic cache, schema fallback | 2026-10-31 | 6 test files; synthetic 69.40% cost reduction vs always-strong | — | 72–78 | **Project 05 base.** Add multi-model + ONNX. |
| 7 | `GraphRAG-CodeAudit` | Python | Local/global GraphRAG for code; Louvain default, Leiden optional | 2026-10-31 | 6 test files; synthetic-repo evaluation | — | 70–76 | **Project 07 base.** Replace regex/LLM extraction with AST. |
| 8 | `Anthropic-PerfBench` | C/NEON, WGSL | Three transformer kernels × three iterations; ARM64 measured | 2026-10-31 | 1 C test file; NEON results, **WGSL not executed** | — | 68–74 | **Project 08 base.** Add Triton + SAE. |
| 9 | `Mobbin-UI-Compiler` | JS/TS, React 19 | Reference-driven UI compiler; fixture Mobbin adapter | 2026-10-31 | 1 test file; README says 10 tests | — | 64–72 | **Project 04 base.** Add VLM + Playwright/axe loop. |
| 10 | `HEROS-Firewall` | Node/JS | OWASP ASI01–ASI10 proxy, HMAC approvals, Merkle receipts | 2026-10-31 | 5 test files; README says 16 tests, 1,000 adversarial + 200 benign | — | 76–82 | **Project 02/10 base.** Add Ed25519 + 500-case bench. |
| 11 | `HEROS-Cloud-SaaS` | Python | PLLB-governed workflow studio; deterministic simulation | 2026-10-31 | 3 test files; README says 6 tests | — | 62–70 | **Project 10 base.** Add multi-tenant + GitHub App. |

**Live band** is a range, not a precise score. It reflects the evidence in this
audit: verified tests and honest docs raise the floor; missing GPU runs and
missing upstream adoption cap the ceiling.

---

## 4. Brief assets that are not publicly visible

The following names appear in the supplied brief but **not** in the live public
profile. They may be private, renamed, or deleted. Do not cite or archive them
until the owner confirms.

| Brief asset | Live status | Action |
|---|---|---|
| `itsoumya-d/hostshift` (ICLR 2027 LENS) | Not on the public profile | Confirm private/public status before using as a research artifact. |
| `itsoumya-d/pulsenet` | Not on the public profile | Do not include in the pinned set until confirmed. |
| `itsoumya-d/mobile-native-design-system` | Not on the public profile | Project 04 can proceed from `Mobbin-UI-Compiler`; merge only if confirmed. |
| `itsoumya-d/swarmcompute` | Not on the public profile | ADR-001 defers the merge. |
| `itsoumya-d/x` / `EcoSphere` / `ContentForge-AI` | Not on the public profile | **Do not archive.** The archive request targets names that do not exist live. |

This is a safety correction, not a criticism: archiving by a stale list is
irreversible for the wrong repository.

---

## 5. The other public repositories

The remaining 19 repos are not in the flagship set. They are useful as range
evidence but should not be pinned above the eleven above.

| Repository | Language | One-line role | Flagship? |
|---|---|---|---|
| `FREED` | TypeScript | App source | No |
| `colpali-edge` | Python | ColPali/edge experiment | No |
| `itsoumya-d` | — | Profile README | No |
| `HEROS-Publication` | HTML | HF publication package | Supporting |
| `compose-cognitive-intervention-engine` | Kotlin | Android Compose reference | No |
| `ghostsearch` | HTML | Client-side document retrieval | No |
| `llm-control-plane` | Python | Provider-agnostic gateway | Supporting |
| `certiflow-ai` | TypeScript | Compliance automation | No |
| `go-ledger` | Go | Idempotent double-entry ledger | Supporting |
| `complaintgraph` | Python | Review mining | No |
| `Yc_ai` | TypeScript | Unlabelled | No |
| `autopilot-fde` | Python | Forward-deployed engineer agents | No |
| `factory-monitor` | Rust | Unlabelled | No |
| `dotnet-enterprise-api` | C# | ASP.NET orders API | No |
| `default-project` | — | This workspace | No |
| `PlotLLM` | Python | Streamlit plot generator | No |
| `developer-utilities` | JavaScript | Automation scripts | No |
| `ridge_shade` | Dart | Mobile game | No |
| `getsmscode-test` | JavaScript | API integration tests | No |

The range is broad. The portfolio signal is diluted by unpinned, unrelated
repos; the fix is curation (pin six, archive nothing without approval), not
deletion.

---

## 6. Hugging Face inventory

Live at `huggingface.co/itssoumyad` on 2026-11-02:

| Category | Count | Names / notes |
|---|---:|---|
| Spaces | **11** | `portfolio`, `heros-rl`, `reflexion-swe`, `graphrag-codeaudit`, `edgeinfer-v2`, `peervault-pqc`, `heros-firewall`, `anthropic-perfbench`, `routellm-gateway`, `mobbin-ui-compiler`, `heros-cloud-saas` |
| Datasets | **2** | `heros-migration-500` (500 rows), `graphrag-questions-100` (100 rows) |
| Public models | **0** | None public yet |
| Collection | **1** | `HEROS AI Systems Portfolio`, **13 items** = 11 Spaces + 2 datasets |

All 11 Spaces showed **Running** and were updated two days before the audit. The
collection description says "Ten applied AI systems", but the collection itself
contains 13 items; the copy should be synchronized to "Eleven Spaces + two
datasets" in a later PR.

**The critical gap:** 0 public models. The HF profile currently proves that demos
run, not that a model was trained. Project 01's model card and adapter are the
first fix.

---

## 7. Deep dives

### 7.1 HEROS — the strongest verified systems artifact

**Verified.**

- 152 tracked files, ~2.25 MB, 4 CI workflows.
- `npm run test:mcp`: **46 tests pass, 0 fail**, 4.3 s. Six data-driven
  adversarial functions cover **289 cases** across ASI01–ASI10.
- `rlvr` baseline: **34 tests pass** in 0.49 s. After #101 and the stacked
  runner PR: **78 pass** (with torch) / **65 pass + 13 skip** (without torch).
  The runner is CPU-tested with a fake policy; no GPU run exists.
- Packages: `@soumyadebnath1619/mcp` v0.3.0, `@soumyadebnath1619/agentic`
  v0.2.0, `forge` v0.1.4, `ledger` v0.1.11.
- Language mix: `.sh` = 170.5 KB of 467.5 KB of code bytes (**36.5%**), not
  72.8%. Shell is 7.6% of all tracked bytes because docs and images dominate.

**Gaps.**

- No GPU training job and no model checkpoint.
- The shell scripts are still a maintenance surface; the 36.5% code-byte share
  is high for a "Node/Zero" project.
- The MCP test count is strong, but the suite is JS-only; there is no
  cross-language fuzz harness against a real MCP client.
- No external adopters or upstream review history.

**Disposition.** Retain and elevate. #101 is the first slice. A follow-up
"shell-to-Node" PR should target the installer and demo scripts, not the Zero
binaries.

### 7.2 HEROS-RL — the real Project 01 base

**Verified.**

- 32 files, ~788 KB, 6 test files.
- `python -m unittest discover -s tests -v`: **40 pass, 5 skip**.
- 500-case dataset `data/heros_migration_500.jsonl` with 10 families.
- Toy GRPO ablation: `G=1` fails (0.500 accuracy), `G=4+` solves the toy task
  (1.000). This is a **toy contextual bandit**, not an LLM result.
- CI has a dedicated CPU-torch job for `test_grpo_loss.py`.
- `RESULTS.md` explicitly says the 1.5B empirical run was **not run**.

**Gaps.**

- No QLoRA/GPU run, no MATH-500 or GSM8K curve, no published adapter.
- The reward stack is static SQL analysis plus optional `forge`; the SQLite
  shadow database is not yet wired in.
- The dataset is generated, not independently labeled; its "500 cases" are a
  deterministic fixture, not a human-verified benchmark.

**Disposition.** Elevate. #101 adds the missing shadow verifier and loss; #102 adds the runner; the
next step is the 500-step run and an honest model card.

### 7.3 peervault — already synchronized, two narrow contradictions

**Verified.**

- 77 files, ~8.9 MB (demo media dominates), 11 test files.
- README documents ML-KEM-768 over `R_q = Z_3329[X]/(X^256+1)`, 7-layer
  NTT/invNTT, 100/100 NIST KAT vectors, hybrid P-256 + HKDF-SHA256, 21-byte AAD
  framing, and `createOpfsSink()`.
- README claims 89/89 SDK tests, 100/100 KATs, p50 0.836 ms / p95 1.082 ms
  handshake on Apple Silicon, and 3.02 MB receiver RSS on a synthetic 1 GB
  stream (**[D]**, not reproduced here).
- The README already contains an explicit retraction of the old "no lattice
  arithmetic" text.

**Gaps found (the real ones).**

- FAQ: "there is no streaming-to-disk path" contradicts the OPFS sink section.
- Comparison table: "Resumable transfers: No" contradicts the shipped
  `receivedBitmap()` / `requestMissingChunks()` / `resendChunks()` primitives.
- FAQ: "the transfer fails" after tab close omits the manual-resume path.

**Disposition.** PR #2 fixes exactly these three statements. It does not touch
the crypto or the package version.

### 7.4 edgeinfer — honest docs, missing kernel

**Verified.**

- 48 files, ~325 KB, 10 test files.
- README claims 106 tests (**[D]**).
- README explicitly states: pre-release, not on npm, paged GPUBuffer KV **not
  implemented**, bundle size claim corrected to ~24 KB, "Replaces OpenAI API"
  absent.
- The speculative decoding and Matryoshka claims are documented, but the
  WebGPU numbers were removed because WebGPU is unavailable in Node CI.

**Gap.** The core technical differentiator — zero-readback paged KV — is still
missing. PR #3 adds a design note with parity and zero-readback gates; it does
not pretend a kernel exists.

**Disposition.** Elevate, but the headline metric waits for Project 06.

### 7.5 Reflexion-SWE — honest toy result, not a benchmark

- 29 files, 7 test files.
- README says the measurements are on deterministic toy fixtures, not HumanEval
  Rust or SWE-bench Lite. That honesty is an asset.
- Gap: no real SWE-bench Lite run, no mutation-adequacy gate, no persistent skill
  library. Project 03.

### 7.6 RouteLLM-Gateway — synthetic cost result

- 26 files, 6 test files.
- Measured synthetic mock-provider benchmark: 69.40% cost reduction vs
  always-strong, with p50/p95 and cache hit rate. Explicitly not MMLU-Pro/GSM8K.
- Gap: binary strong/weak only; no K≥4 meta-learned router; no ONNX export.
  Project 05.

### 7.7 GraphRAG-CodeAudit — synthetic repo, Louvain default

- 33 files, 6 test files.
- Local/global search with a flat RAG baseline; Louvain default, Leiden optional.
- Gap: regex/LLM extraction, no Tree-sitter AST, no incremental git-diff update,
  no 1,000-query real-repo benchmark. Project 07.

### 7.8 Anthropic-PerfBench — real NEON, unexecuted WGSL

- 19 files, 1 C test file.
- Measured NEON results on Apple Silicon; 66.31 GB/s memcpy. WGSL shaders are
  provided but **not executed**; no WebGPU numbers claimed.
- Gap: no Triton, no SAE, no RTX 2060 kernel. Project 08.

### 7.9 Mobbin-UI-Compiler — fixture adapter only

- 35 files, 1 test file; README says 10 tests.
- Explicit environment boundary: no live Mobbin MCP; fixture metadata only.
- Gap: no VLM, no Playwright render, no axe-core loop. Project 04.

### 7.10 HEROS-Firewall — strong security surface

- 21 files, 5 test files; README says 16 tests, 1,000 adversarial + 200 benign,
  FNR/FPR/p99 measured.
- Gap: HMAC approvals are symmetric; Ed25519-signed Sparse Merkle proofs and a
  published 500-case OWASP bench remain. Project 02.

### 7.11 HEROS-Cloud-SaaS — deterministic simulation

- 19 files, 3 test files; README says 6 tests.
- PLLB loop with a deterministic engine and receipts; explicitly "not a customer
  deployment or ARR result."
- Gap: no multi-tenancy, billing, GitHub App, or tamper-proof receipt UI.
  Project 10.

---

## 8. Portfolio gap analysis

| Dimension | Verified evidence | Missing frontier capability | Hiring perception |
|---|---|---|---|
| ML/DL | Pure-Python GRPO/DAPO equations; toy bandit ablation; Matryoshka retrieval | Zero PyTorch/JAX GPU training runs; no mixed precision; no published weights | Strong software engineer who reads papers; no empirical neural-network proof |
| LLM post-training | 49 CPU tests; Dr.GRPO/DAPO loss; deterministic rewards | No SFT/QLoRA/DPO/GRPO run on a real model; no MATH-500/GSM8K curve | Passes a loss-function screen; fails a research deep-dive on evidence |
| Systems/inference | Zero binaries; Rust WASM ML-KEM; ONNX wrapper | No custom WGSL/Triton/CUDA kernel; no paged KV; no KV quantization | High systems hygiene; needs kernel depth for inference roles |
| Agents/security | 289 adversarial MCP cases; Merkle receipts; shadow gates | No containerized SWE-bench pass@1; no 500-case public bench | Immediately competitive for agent infrastructure/safety |
| Data/eval | 500-row migration set; 100-row GraphRAG set | No 1k–5k real-repo set; no significance testing | Dataset scale reads as a fixture, not a benchmark |
| OSS signal | Solo repos; npm packages published | Zero merged upstream PRs; zero external adopters | Needs collaborative review history |

---

## 9. Re-baseline protocol

Run this after each merged PR:

1. **Code quality:** `ruff check`, `mypy --strict` where configured, package
   build, `npm pack --dry-run`.
2. **Verification:** full unit suite, adversarial corpus, KATs, and a
   deterministic seed replay.
3. **Empirical:** one real hardware log with device, driver, batch size, sequence
   length, and a correctness check. No synthetic result may be labeled a model
   result.
4. **Docs:** diff the README "Known Limitations" against the shipped code; every
   limitation needs a test or an explicit "not implemented" line.
5. **Artifact:** publish the model/dataset/npm package and link it from the
   README and HF card.

Scores move only when the corresponding evidence is committed. Until then the
band in §3 stands.

---

## 10. Disposition summary

| Action | Repositories | Gate |
|---|---|---|
| Elevate and pin | HEROS, HEROS-RL, peervault, edgeinfer, Reflexion-SWE, HEROS-Firewall | #101/#102 + #14/#15 + one GPU run |
| Elevate after Project 05/07/08 | RouteLLM-Gateway, GraphRAG-CodeAudit, Anthropic-PerfBench | Real benchmark + artifact |
| Keep as supporting | Mobbin-UI-Compiler, HEROS-Cloud-SaaS | Project 04/10 |
| Confirm before touching | hostshift, pulsenet, mobile-native-design-system, swarmcompute | Owner confirmation |
| Do not archive by stale list | x, EcoSphere, ContentForge-AI | Names not live |
