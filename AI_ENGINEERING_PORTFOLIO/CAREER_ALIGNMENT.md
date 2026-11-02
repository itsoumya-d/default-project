# Career Alignment — Roles, Proof, and Compensation

Goal: convert artifacts into interviews, and interviews into an offer that
matches the evidence. The portfolio is the evidence layer; this document maps it
to roles and money without inflating either.

**Current truthful position (2026-11-02):** strong agent-infrastructure and
systems hygiene; no published model weights, no GPU training curve, no merged
upstream PR, no external adopters. That profile is competitive for agent
infrastructure and full-stack AI roles now. It is **not yet** competitive for a
frontier post-training research role, regardless of the audit score.

---

## 1. Role archetypes

| Role | Companies | What the loop actually tests | Current proof | Gap to close |
|---|---|---|---|---|
| **Post-training / RL / alignment engineer** | OpenAI, Anthropic, DeepMind, DeepSeek, Mistral, xAI | PyTorch distributed training; RLHF/RLVR (PPO/DPO/GRPO); reward modeling; debugging instability | 49 rlvr tests; Dr.GRPO/DAPO loss; toy ablation; 500-case reward stack | One real QLoRA run + MATH-500 curve + adapter card |
| **Agent systems / safeguards engineer** | Anthropic (Claude Code/MCP), OpenAI Agents, Scale AI, Cognition, Perplexity | Tool contracts; sandboxing; SWE-bench; adversarial red-teaming; deterministic recovery | 289 adversarial MCP cases; Merkle receipts; shadow gates; 16 firewall tests | Public 500-case bench; containerized SWE-bench Lite-50 |
| **Inference / kernel engineer** | NVIDIA, Fireworks, Together, HF, Chrome WebML, Apple | Triton/CUDA/WGSL fusion; PagedAttention; KV quantization; speculative decoding; roofline | ONNX wrapper; Matryoshka retrieval; NEON kernels; WGSL design note | One real kernel with parity + measured speedup |
| **Staff full-stack AI / developer infra** | Vercel, Stripe, Databricks, Supabase, Cloudflare, AWS Bedrock | TypeScript/Rust/WASM; low-latency gateways; telemetry; privacy-preserving edge; UX polish | peervault PQC/WASM; 11 running Spaces; MCP SDK; UI compiler | One commercial-grade control plane (P10) |
| **Research engineer / applied scientist** | Google Research, Microsoft Research, Meta AI, HF | Paper reproduction; ablations; statistical rigor; writing | Research library; honest failure notes | A workshop paper with a real result |

---

## 2. Proof map (what to show, what to fix)

### Post-training

**Show:** `HEROS-RL`'s 500-case dataset and toy group-size ablation; `HEROS/rlvr`
78 tests; the shadow verifier and QLoRA runner; a run log with reward/KL/length.
The run log is still the missing piece.

**Fix:** the 1.5B run. Without it, the story is "I implemented the loss"; with it,
the story is "I trained, measured, and debugged a policy."

**Interview answer to prepare:** "Why does Dr.GRPO remove length bias, and what
did you observe in your own length curve?" Have the actual curve.

### Agent systems

**Show:** the 289-case corpus (60 malformed JSON-RPC, 78 schema, 31 auth, 60
hostile forge, 30 malformed shadow, 30 approval replay); the Merkle receipt
design; the SQLite shadow gate.

**Fix:** publish the 500-case OWASP bench and run SWE-bench Lite-50 with receipts.

**Interview answer:** "Design a multi-tenant code-execution agent that resists
prompt-injected container escape, infinite retries, and non-idempotent side
effects." Whiteboard the capability boundary, the idempotency key, and the
rollback.

### Kernels

**Show:** the NEON results (66.31 GB/s memcpy), the WGSL design note, the
Matryoshka two-stage retrieval.

**Fix:** one kernel with parity and a measured speedup. A design note is a
starting point, not a kernel portfolio.

**Interview answer:** "Compute the arithmetic intensity of paged decode at
batch 1; where does it sit on the roofline; what would you fuse first?"

### Full-stack / product

**Show:** 11 running Spaces, the PQC transfer, the UI compiler, the P25 npm
packages.

**Fix:** one control plane with a real approval workflow and a tamper-proof
receipt UI.

**Interview answer:** "Design a <10 ms routing gateway at 10k RPS with fallback
and cache invalidation."

---

## 3. Interview preparation plan

| Track | Weekly drill | Artifact |
|---|---|---|
| Coding | 2 medium problems + 1 ML implementation from scratch (attention, LayerNorm, GRPO loss, Top-K SAE) | A `scratch/` repo with tests |
| Systems design | 1 mock per week: agent sandbox, router, KV cache, receipt store | A one-page design doc |
| Research | 1 paper deep-read + 1 reproduction attempt per two weeks | A literature note in `research/` |
| Behavioral | STAR stories for failure, conflict, and a shipped artifact | 6 stories, each with a metric |
| Upstream | 1 issue triage + 1 small PR attempt per month | A merged PR or a public review |

**Coding interview rule:** implement the math, not the framework. If asked for
GRPO, write the advantage and the clipped objective, then explain the reduction.

---

## 4. Compensation bands (planning, not promises)

| Pathway | Level / profile | Base | Bonus | Equity / SaaS | Total | Prerequisites and caveats |
|---|---|---:|---:|---:|---:|---|
| US Tier-1 big tech (Google/Meta/AWS/Microsoft/NVIDIA; SF/Seattle/NYC) | L4–L5 ML/systems SWE | $160k–$215k | $24k–$40k | $50k–$140k RSU | **$234k–$395k+** | US work authorization (OPT/H-1B/L-1/O-1A). Equity vests over 4 years; first-year value is not cash. |
| Frontier lab (OpenAI/Anthropic/xAI/DeepMind/Perplexity) | Member of Technical Staff | $210k–$300k | $0–$50k | $150k–$400k+ PPU/equity | **$360k–$750k+** | Extremely high bar; needs standout empirical repos, merged PRs, or papers. Equity is illiquid until a tender/IPO. |
| Global remote (US/EU Series A–C, HF, PostHog, Martian) | Senior/staff remote from India | $130k–$185k | $10k–$25k | $25k–$60k options | **$165k–$270k** | No visa; requires an asynchronous OSS track record and published packages. Some companies use local-market bands. |
| India top-tier MNC + micro-SaaS | Senior AI engineer (₹65L–₹1.2Cr) + 120–200 SaaS customers | $78k–$145k | included | $110k–$180k net SaaS | **$188k–$325k+** | Highest-probability location-independent path, but SaaS revenue is not guaranteed and requires sales/support. |

**Honest caveats.**

- The top bands assume a top-tier offer, not a portfolio score. A 98/100 planning
  score does not create an OpenAI offer.
- RSU/PPU values fluctuate; do not budget rent against unvested equity.
- A solo B2B SaaS at 250 customers is a real business with churn, support, and
  SOC2 costs; the 95% gross margin in the brief ignores founder time.
- Indian domestic compensation is usually quoted in INR; the USD figure moves
  with the exchange rate.

---

## 5. B2B SaaS economics (open-core first)

Build the product as an open-core flagship; activate Stripe only after the
validation gate. The brief's ARPA of $79/mo is a hypothesis; validate it with
design partners before forecasting.

| Product | Customer / pain | Open-core artifact | Validation gate before billing |
|---|---|---|---|
| **A. HEROS Forge & Ledger Cloud** (P10) | FinTech/HealthTech CTOs deploying coding agents; one destructive migration is an outage/SOC2 incident | GitHub App + shadow gate + Merkle receipts | 500+ stars, 100+ Action installs, 10 design partners asking for hosted retention |
| **B. MetaRoute FinOps Proxy** (P05) | Series A–C AI startups spending $10k–$100k/mo; 65% of prompts can go to a cheaper model | INT8 ONNX router + Pareto simulator | 1,000+ downloads; ≥45% bill reduction across 5 beta companies |
| **C. AST-GraphRAG Security Auditor** (P07) | AppSec teams needing blast-radius/taint analysis beyond regex SAST | PR check + 1,000-query benchmark | 50+ repos running the check; <5% developer dismissal |

### Unit economics at the brief's $79 ARPA

| Customers | MRR | ARR | Infra + Stripe / mo | Gross margin | Pre-tax operating profit / yr |
|---:|---:|---:|---:|---:|---:|
| 0 | $0 | $0 | ~$0 | n/a | $0 |
| 100 | $7,900 | $94,800 | ~$340 | 95.7% | ~$90,720 |
| 250 | $19,750 | $237,000 | ~$820 | 95.8% | ~$227,160 |
| 500 | $39,500 | $474,000 | ~$1,650 | 95.8% | ~$454,200 |
| 1,000 | $79,000 | $948,000 | ~$3,400 | 95.7% | ~$907,200 |

**What the table omits:** founder time, support, SOC2 Type II (~$20k–$50k),
legal, refunds, failed payments, and churn. A 95% gross margin is plausible for
software; a 95% net margin is not. Treat the table as a gross-margin model, not a
salary.

### Commercial sequence

1. **Open-core, no billing.** Ship the GitHub Action and the benchmark. Collect
   stars, installs, and design-partner interviews.
2. **Hosted waitlist.** A static page and a form; no infrastructure until 20
   qualified requests.
3. **Paid pilot.** A single-tenant deployment for 3–5 design partners; invoice
   manually; measure retention and time-to-value.
4. **Self-serve.** Only after the pilot proves the onboarding is <10 minutes and
   support <1 hour/customer/month.
5. **SOC2.** Only when a customer requires it and pays for it.

---

## 6. 12-month job-search plan

| Month | Action | Success metric |
|---|---|---|
| 1 | Merge PR #1–#3; publish the P01 adapter; update resume with [V] claims | 1 model artifact; 3 PRs |
| 2 | P06 parity + P02 500-case bench; one blog post | 1 kernel result; 1 public bench |
| 3 | P08 SAE; apply to 10 agent-infra roles | 10 applications; 3 referrals |
| 4 | P03 Lite-50; one upstream PR to TRL or MCP SDK | 1 merged/under-review PR |
| 5 | P05 ONNX router; 10 more applications | 5 interviews |
| 6 | P07 codebench; mock interviews weekly | 2 onsite loops |
| 7–9 | Convert interviews; negotiate with the bands above | 1 offer |
| 10–12 | If no offer, ship P09/P10 and reapply with new evidence | Bigger artifact, not more applications |

**Referral strategy:** contribute to the repo first, then ask for a referral with
the PR link. A cold application with a 289-case test suite is stronger than a
resume alone, but a referral is stronger than both.

---

## 7. What not to claim

- "Trained Qwen2.5 on GPUs" before the run exists.
- "100/100 KAT" without linking the test command and the vector file.
- "Replaces OpenAI/AWS/WeTransfer."
- "95% Python" or any skill percentage.
- "Merged upstream" before the merge.
- "250 customers" or "$200k ARR" before the first invoice.

The fastest way to lose a frontier-lab interview is an unverifiable number. The
second fastest is being unable to explain the number you did put down.
