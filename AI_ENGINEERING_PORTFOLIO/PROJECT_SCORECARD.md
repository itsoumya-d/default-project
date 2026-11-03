# Project Scorecard — Ten Flagships, Ranked and Gated

Execution rule: **one project at a time.** A project is "done" only when its
acceptance gate passes, its tests run in CI, its artifact is published, and its
README limitation section matches the code. Ten shallow projects lose to two
deep ones in a research-engineer loop.

Scores below are the supplied planning scores **[P]**. They are useful for
ordering, not for a resume. See `PORTFOLIO_AUDIT.md` §9 for how a score becomes
verified.

---

## 1. Ranking matrix

| Brief rank | Project | Category | Hiring (20) | Research (15) | Complexity (15) | Originality (15) | Hardware (10) | Free infra (10) | Relevance (15) | Total |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | **P01 HEROS-RLVR-Studio** | Verifier-driven post-training | 20 | 15 | 14 | 15 | 9 | 10 | 15 | **98** |
| 2 | **P02 HEROS-SafeAgent-OS** | Audited MCP runtime | 19 | 13 | 15 | 15 | 10 | 10 | 15 | **97** |
| 3 | **P06 EdgeInfer-WGSL-v3** | WebGPU kernels | 19 | 14 | 15 | 14 | 10 | 10 | 14 | **96** |
| 4 | **P03 Reflexion-SWE-Bench** | Autonomous repair | 19 | 14 | 14 | 13 | 9 | 9 | 15 | **93** |
| 5 | **P05 MetaRoute-Gateway** | Cost-quality routing | 18 | 14 | 13 | 13 | 10 | 10 | 14 | **92** |
| 6 | **P08 Triton-SAE-Safety** | Kernels + interpretability | 19 | 15 | 15 | 14 | 9 | 9 | 14 | **95** |
| 7 | **P07 AST-GraphRAG-CodeAudit** | Graph retrieval | 17 | 13 | 13 | 13 | 10 | 10 | 14 | **90** |
| 8 | **P09 PeerVault-PQC-AI** | PQC + federated artifacts | 17 | 13 | 14 | 14 | 10 | 10 | 13 | **91** |
| 9 | **P04 Mobbin-UI-Compiler-VLM** | Multimodal UI compiler | 17 | 12 | 13 | 13 | 9 | 9 | 13 | **86** |
| 10 | **P10 HEROS-Cloud-Control** | Agentic governance SaaS | 18 | 11 | 14 | 13 | 10 | 10 | 14 | **90** |

**Arithmetic inconsistency in the supplied ranking:** P08 scores **95**, which is
higher than P03 (93), P05 (92), P07 (90), P09 (91), P04 (86), and P10 (90), yet
it is listed at rank 6. The table above preserves the brief's rank column for
traceability; the score column says P08 should be #4.

### Recommended execution order (dependency-aware)

| Order | Project | Why this position |
|---:|---|---|
| 1 | P01 | Closes the zero-model gap; unblocks P03 (local policy) and P05 (local model). |
| 2 | P02 | Hardens the MCP runtime that P10 sells; reuses the 289-case suite. |
| 3 | P06 | Kernel depth; unblocks P09's EdgeInfer shard streaming. |
| 4 | P08 | GPU kernel + interpretability; shares the RTX 2060 with P06. |
| 5 | P03 | Needs P01's policy and P02's receipts for the repair sandbox. |
| 6 | P05 | Needs P01's local model and a real cost baseline. |
| 7 | P07 | Independent; can run on CPU while GPU work is queued. |
| 8 | P09 | Needs P06's `fromBuffer()` path and P02's receipts. |
| 9 | P04 | Independent UI track; best after P06's browser tooling. |
| 10 | P10 | Commercial layer; needs P02 and P07 as the trust substrate. |

This order differs from the brief's rank because dependencies matter more than a
two-point score difference. If the goal is purely interview signal in the next
eight weeks, do P01 → P06 → P08 and defer the rest.

---

## 2. Project specifications

### P01 — HEROS-RLVR-Studio

**Problem.** Small code models hallucinate destructive SQL migrations
(`DROP COLUMN` without backfill) and malformed MCP manifests. `HEROS/rlvr` now
has a tested CPU runner, a GPU SFT result, and an adapter-initialization path,
but no validated RL improvement. `HEROS-RL` already has a critic-free GRPO
engine, a 500-case dataset, and TRL/Unsloth entry points, but no 1.5B result.

**Originality.** The reward is not a learned preference model; it is a
deterministic SQLite shadow gate plus forge's risk contract. A migration is
executed against seeded rows, and row loss is measured, not guessed.

**Stack.** Python 3.11, PyTorch 2.4+, Transformers, PEFT, bitsandbytes (NF4),
DuckDB, W&B, HEROS `forge`/`ledger`/MCP. This slice does not depend on TRL; the
existing HEROS-RL TRL entry point remains a separate baseline.

**Data.** `heros-migration-500` (existing) plus a curated 5,000-pair set from
`b-mc2/sql-create-context` and `xlangai/spider`; `HuggingFaceH4/MATH-500` for the
reasoning eval. Do not call the generated set human-verified.

**Compute.** RTX 2060 6 GB: 4-bit QLoRA (`r=16`, `alpha=32`), `G=4`,
`max_length=512`, `paged_adamw_8bit`, ~4.2 GB. Kaggle 2×T4 for `G=8` on 3B.

**Phases.**

| Phase | Deliverable | Status |
|---|---|---|
| P1 | `REWARD_SPEC.md` with weights and miracle penalty | **Done** in `projects/project-01-heros-rlvr-studio/docs/` |
| P2 | Architecture: rollout → shadow worker → receipt | **Done** |
| P3 | `pyproject` extras: torch, peft, bitsandbytes | **Done**: `gpu` + `train` extras |
| P4 | `gpu_trainer.py` with verifier + loss | **Done** ([#101](https://github.com/itsoumya-d/HEROS/pull/101)) |
| P5 | `qlora_runner.py` loading Qwen2.5-Coder-1.5B | **Done** ([#103](https://github.com/itsoumya-d/HEROS/pull/103)); GPU SFT + adapter-init path exercised |
| P6 | 75+ tests | **95 now** |
| P7 | 500-step ablation (Base, SFT, GRPO, Dr.GRPO+DAPO) | **SFT 1.90; RL-from-SFT 0/10 variance groups; RL-base 100-step 0.13 (0.165 at 50); no four-arm ablation** |
| P8 | Parallel shadow workers >1.8× step throughput | Not started |
| P9 | Colab/Kaggle notebook | Not started |
| P10 | PR + HF adapter | SFT model card local; adapter-init [#119](https://github.com/itsoumya-d/HEROS/pull/119) merged; HF upload blocked on credentials |

**Acceptance gate.** 75+ tests green; 500-step run with a committed `run.json`
(seed, hardware, loss curve, KL, clip fraction, reward variance, length); adapter
on HF with an honest model card; MATH-500 pass@1 with error bars; no claim of
"+18%" unless the ablation shows it.

**Hiring.** OpenAI post-training/RL infra, Anthropic alignment/tool use,
DeepSeek, Google DeepMind, Mistral.

---

### P02 — HEROS-SafeAgent-OS

**Problem.** An agent runtime needs a tamper-evident audit trail and a hard gate
before destructive actions. HEROS now has a 500-case adversarial corpus, Merkle
receipts, and SQLite shadow gates; the gaps are Ed25519-signed sparse Merkle
inclusion proofs and the shell-script maintenance surface.

**Stack.** Zero, Rust, Node 22+ ESM, TypeScript, SQLite WAL, Ed25519
(`node:crypto`), GitHub Actions.

**Phases.** Audit the 11 shell scripts (36.5% of code bytes) → implement
`packages/mcp/src/merkle.ts` with Ed25519 → migrate harnesses to `node --test` →
expand to 500 OWASP ASI01–ASI10 cases → 64-worker flock/WAL idempotency torture →
publish npm → threat model → PR → sync `HEROS-Firewall` Space.

**Acceptance gate.** 500 cases, 0 unapproved destructive migrations, p99 policy
latency <4.5 ms, 100% idempotency consistency under 64 parallel replays, signed
proof verifies in the browser.

**Current.** 500 cases implemented (289 existing + 211 in PR #111); 54 MCP
tests pass. Ed25519 root/proof signing and a browser verifier merged in PR #112
(`d0e523f`); the browser accepted the signed proof and rejected a tampered
signature. p99 policy latency is **0.245 ms** over 5000 samples (PR #113). The
host-local 64-process idempotency lock and threat model merged in PR #115
(`dc51441`): one handler call, one receipt, 63 replays. Merkle root updates are
incremental: p99 **0.62 ms** at 5200 signed receipts (PR #116, `d93e7d9`). The
500 cases are packaged as a 500-record JSONL dataset with a manifest and CI
drift check (PR #117, `2658e90`). `@soumyadebnath1619/agentic@0.3.0` is a
9-file, 22.3 kB release candidate with the threat model and changelog included
(PR #118, `cbee92a`). The 11-script maintenance policy is merged with full
shellcheck coverage (PR #120, `61f6eec`). `HEROS-Firewall` has 16 tests and a
measured red-team result. **Gate met locally; corpus packaged; release candidate
ready; shell maintenance documented.** Remaining: publish approval.

**Hiring.** Anthropic MCP/safeguards, OpenAI safety systems, Scale AI, AWS
Bedrock AgentCore.

---

### P03 — Reflexion-SWE-Bench

**Problem.** Reflexion regresses on MBPP (77.1 vs 80.1) because self-generated
tests have false positives; the Ω=3 memory forgets cross-task lessons.
`Reflexion-SWE` already has the actor/evaluator/reflection loop and an honest toy
evaluation.

**Originality.** A mutation-adequacy gate: a generated test suite must kill ≥80%
of synthetic AST mutants before it may grade a patch. A persistent Matryoshka
skill library replaces the sliding window.

**Stack.** Python 3.11, LangGraph or SQLite FSM, Tree-sitter, Hypothesis,
docker-py, FAISS, FastAPI, React/TS inspector.

**Data.** HumanEval (164), MBPP (500), SWE-bench Lite (300), Lite-50 for the
practical loop.

**Acceptance gate.** MBPP regression eliminated; false-positive test rate <2%;
Lite-50 resolution rate reported with mean tokens per resolved issue; no repo
corruption.

**Hiring.** OpenAI Codex/SWE agents, Anthropic Claude Code, Cognition, Cursor,
DeepMind.

---

### P04 — Mobbin-UI-Compiler-VLM

**Problem.** Screenshot-to-code tools produce visually plausible but
inaccessible code. `Mobbin-UI-Compiler` has a fixture adapter and five surfaces;
it needs a real VLM, a typed UI-AST, and deterministic accessibility audits.

**Stack.** TypeScript, Next.js 15, Tailwind, Flutter (if the design-system repo
is confirmed), Qwen2-VL-2B 4-bit or Gemini Flash, Playwright, axe-core, Design2Code.

**Acceptance gate.** 100% WCAG 2.2 AA on the generated benchmark, IoU improvement
over one-shot, no live-Mobbin claim without the MCP server.

**Hiring.** Vercel/v0, Anthropic Artifacts, Google Flutter/design-to-code, Meta.

---

### P05 — MetaRoute-Gateway

**Problem.** Binary strong-vs-weak routing cannot handle K≥4 specialized models,
and a frozen router drifts when prices/models change. `RouteLLM-Gateway` already
has a Bradley-Terry router and a synthetic 69.40% cost reduction.

**Stack.** Python, PyTorch, ONNX Runtime, FastAPI, DuckDB, Chatbot Arena +
RouterBench.

**Acceptance gate.** K≥4, latent preference encoder, INT8 ONNX <15 MB, p99 <6 ms,
APGR and CPT-95 reported, >2.5× cost reduction on MMLU/GSM8K at ≤1 point loss.

**Hiring.** Cloudflare AI Gateway, Databricks Mosaic, Perplexity, AWS Bedrock.

---

### P06 — EdgeInfer-WGSL-v3

**Problem.** `edgeinfer` cannot pin `past_key_values` in a `GPUBuffer` without a
custom kernel; every decode step round-trips KV through the CPU. The README is
honest about this.

**Originality.** Two WGSL kernels: paged decode (`block_size=16`, online softmax,
`ort.Tensor.fromGpuBuffer`) and Matryoshka INT8 scan (`d=64` coarse → `d=768`
FP32 rerank) with zero readback.

**Stack.** TypeScript, WGSL, onnxruntime-web ≥1.21.0, IndexedDB, Vitest,
Playwright GPU runner, SmolLM2-135M/360M.

**Phases.** Design note (PR #3, done) → CPU reference (PR #16, done) → GQA
(PR #18) → 20-prompt ORT baseline (PR #19) → f32 WGSL kernel (PR #20) → f16 KV
cache (PR #21, done) → ORT prompt parity → zero-readback trace → benchmark →
150+ tests → npm → HF Space.

**Current.** The CPU reference, GQA support, 20-prompt ORT baseline, and f16
WGSL kernel are merged. Synthetic WebGPU parity is **20/20** on Chrome 156 /
NVIDIA Turing with max abs **4.79e-8**; the runtime zero-readback capability
check passes **40/40**. Node tests are **113/113**; Python tests are **14**.
SmolLM2 token/logit parity, a validation-layer trace, peak-memory accounting,
two-device p50/p95, Firefox, and a fallback flag remain.

**Acceptance gate.** Parity with ORT on 20 prompts, 0 `mapAsync` on KV buffers,
memory within 5% of the analytic KV size, p50/p95 on two devices, fallback flag.
No "10×" claim before the measurement.

**Hiring.** Chrome WebML, Hugging Face transformers.js, NVIDIA, Apple on-device,
Fireworks.

---

### P07 — AST-GraphRAG-CodeAudit

**Problem.** Microsoft GraphRAG's LLM entity extraction is expensive and
hallucinates edges. `GraphRAG-CodeAudit` uses regex/LLM extraction and a synthetic
repo.

**Originality.** Deterministic Tree-sitter AST + taint graph, Leiden communities,
incremental git-diff invalidation. No LLM in the indexing path.

**Stack.** Python, Tree-sitter, igraph, leidenalg, DuckDB, edgeinfer embeddings,
FastAPI, Cytoscape.js.

**Acceptance gate.** `ast-graphrag-codebench-1000` (10 real repos), Recall@10
>0.88, ≥90% indexing-token reduction, <800 ms incremental update, subgraph F1
reported.

**Hiring.** Microsoft Research/GitHub Copilot, Sourcegraph, Cursor, Google Cloud.

---

### P08 — Triton-SAE-Safety

**Problem.** Eager SAE training is HBM-bound; `Anthropic-PerfBench` has NEON
kernels but no Triton, no SAE, and no RTX 2060 run.

**Originality.** Fused centering + encoder + TopK in SRAM; 16× Top-K SAE on
Qwen2.5-Coder-1.5B layer 14; activation steering against insecure code.

**Stack.** PyTorch 2.4+, Triton, safetensors, `the-stack-smol`,
`Code_Vulnerability_Security_DPO`.

**Acceptance gate.** >2.4× kernel speedup, `R²>0.92`, CWE suppression with no
pass@1 regression, roofline chart with achieved bandwidth, weights on HF.

**Hiring.** Anthropic performance/interpretability, OpenAI safety/kernels,
NVIDIA, DeepMind.

---

### P09 — PeerVault-PQC-AI

**Problem.** Browser transfers fail on tab reload; OPFS resume is manual;
model artifacts are too large for chat apps. `peervault` already has the PQC
channel and the OPFS sink.

**Originality.** A persistent `ChunkBitmap` journal, cross-reload resume, and
encrypted `.safetensors`/`.onnx` shard streaming into `EdgeInfer.fromBuffer()`.

**Stack.** Rust→WASM, TypeScript, WebRTC, OPFS, IndexedDB, Go relay.

**Acceptance gate.** 100/100 KAT, <64 MB receiver RSS on 500 MB, a real
cross-reload resume test, npm package, `swarmcompute` merge only if confirmed.

**Hiring.** Cloudflare, Apple Private Cloud Compute, Signal, Brave, Google FL.

---

### P10 — HEROS-Cloud-Control

**Problem.** Teams deploying coding agents need a migration gate and a SOC2-grade
receipt trail. `HEROS-Cloud-SaaS` is a deterministic PLLB simulation, not a
multi-tenant product.

**Stack.** Next.js 15, TypeScript, Tailwind, HEROS MCP/forge/ledger, Neon
Postgres (optional) + SQLite/DuckDB, Cloudflare Workers, Mobbin patterns.

**Acceptance gate.** GitHub App/Action dry-runs 250 migrations, 100% tamper
detection, signed human approval for `has_data_loss: true`, Lighthouse ≥98,
Playwright E2E, a hosted sandbox demo (approval required before deploy).

**Hiring.** Stripe, Vercel, Supabase, Databricks, Anthropic/OpenAI product infra,
B2B SaaS founder track.

---

## 3. Portfolio-level gates

| Gate | Requirement |
|---|---|
| G1 Build | One command installs and runs the project from a clean checkout. |
| G2 Test | Unit + integration + adversarial tests green in CI. |
| G3 Benchmark | Real hardware, seeds, hardware/software matrix, correctness check. |
| G4 Artifact | Model/dataset/npm package published with a card. |
| G5 Docs | Limitations match code; threat model where relevant; four UI states. |
| G6 Review | PR description with problem, changes, test log, benchmark delta. |
| G7 Honesty | No unverified number; every claim tagged [V]/[D]/[P]. |

A project can be "portfolio-ready" at G1–G7 without being commercially viable.
Commercial gates are separate (see `CAREER_ALIGNMENT.md` §4).
