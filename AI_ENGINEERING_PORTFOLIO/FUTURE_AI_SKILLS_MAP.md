# Future AI Skills Map

Purpose: decide what to learn deeply, what to use as a tool, and what to stop
investing in. The map is organized by durable capability, not by framework. A
framework is a temporary interface; the underlying math, memory model, and
verification loop are the transferable asset.

**Core architectural position (ADR-004):** direct model APIs + MCP 2025-11-25 +
stateful graph orchestration (LangGraph or a SQLite-WAL finite-state machine)
supersede brittle legacy LangChain prompt chains. Use LangChain only as an
adapter; keep state, retries, and tool contracts explicit.

---

## 1. The six domains

| Domain & competency | Classification | Demand and 10–20 year relevance | Mathematical / systems prerequisites | Core papers and primary resources | Portfolio exercise | Interview evaluation |
|---|---|---|---|---|---|---|
| **A. ML/DL: PyTorch internals, autograd, distributed tensor mechanics** | Foundational | **Critical / permanent.** Every higher-level API compiles to tensor ops, gradients, and memory movement. | Matrix calculus; Jacobian-vector products; IEEE 754 (fp32/bf16/fp16/fp8); SRAM vs HBM; coalescing; reduction order. | Paszke et al., *PyTorch* (2019); Goodfellow et al., *Deep Learning*; Karpathy, *Zero to Hero*; PyTorch `torch.compile` and autograd docs. | Implement a custom `autograd.Function` backward pass; write the Dr.GRPO token loss and verify gradients numerically; profile a fused kernel against eager PyTorch. | Live coding: multi-head attention, LayerNorm, or a custom backward pass; diagnose OOM and NaN gradients. |
| **A2. Self-supervised, representation, multimodal learning** | Foundational | **High / high.** Vision, audio, code, and action tokens converge into shared backbones; retrieval quality is a product differentiator. | InfoNCE/contrastive loss; temperature scaling; nested subspace optimization; patchification; cross-modal projection. | Kusupati et al., *Matryoshka Representation Learning* (NeurIPS 2022, arXiv:2205.13147); Radford et al., *CLIP*; Peebles & Xie, *DiT*. | Train Matryoshka heads at `d ∈ {64,128,256,768}`; evaluate Recall@10 vs full-dimension baseline; build the UI-AST compiler in Project 04. | Derive InfoNCE; explain why MRL sums cross-entropy over prefix dimensions and how truncation changes the normalization. |
| **B. LLM engineering: verifiable RL post-training (GRPO, Dr.GRPO, DAPO, DPO)** | Foundational + algorithmic | **Extreme / 15+ years.** The shift from preference imitation (RLHF) to reinforcement learning with verifiable rewards (RLVR) is the defining post-training change. | Policy gradient theorem; importance sampling; KL divergence; group-normalized advantages; Bradley-Terry; clipping; length bias. | Shao et al., *DeepSeekMath* (arXiv:2402.03300); Guo et al., *DeepSeek-R1* (arXiv:2501.12948); Liu et al., *Dr.GRPO* (arXiv:2503.20783); Yu et al., *DAPO* (arXiv:2503.14476); Rafailov et al., *DPO* (2023). | Project 01: 4-bit QLoRA Dr.GRPO on Qwen2.5-Coder-1.5B with the SQLite shadow verifier; log reward, KL, clip fraction, and response length. | Derive GRPO vs PPO and why removing the critic saves ~50% memory; explain Dr.GRPO's length-bias correction and DAPO's dynamic sampling. |
| **B2. Quantization, distillation, structured generation** | Foundational systems | **Extreme / permanent.** Edge deployment and datacenter TCO require sub-4-bit precision and guaranteed syntax. | Affine quantization `W_q = round(W/s) + z`; group-wise scales; Hessian/outlier preservation (AWQ/GPTQ); FSM/CFG logit masking. | Dettmers et al., *QLoRA* (2023); Lin et al., *AWQ* (2024); Willard & Louf, *Outlines* (2023). | Implement FSM token constraints in Project 06; compute exact KV-cache VRAM for a 7B model at batch `B`, sequence `S`, GQA groups `G`. | Calculate VRAM for weights + KV + activations; write a token-level FSM mask; explain why INT4 needs group scales. |
| **C. AI agents: sandboxing, MCP, verbal/experiential RL** | Architectural | **Extreme / 15+ years.** Autonomous software and computer-use agents require formal sandboxing, idempotency, and cross-episode memory. | POMDPs; capability-based security; Merkle trees; graph traversal; property-based testing; mutation adequacy. | Shinn et al., *Reflexion* (NeurIPS 2023, arXiv:2303.11366); Jimenez et al., *SWE-bench* (ICLR 2024, arXiv:2310.06770); Anthropic MCP 2025-11-25 spec. | Project 02 and 03: containerized repair agent, mutation-gated tests, Merkle receipts, 500-case OWASP bench. | System design: multi-tenant code-execution agent that resists prompt-injected container escape, infinite retries, and non-idempotent side effects. |
| **D. AI infrastructure: GPU kernels and serving** | Foundational systems | **Extreme / 20+ years.** Compute scales faster than memory bandwidth; kernel fusion and memory-bound optimization remain the moat. | Roofline model; SRAM tiling; coalesced HBM access; online softmax; paged virtual memory; warp divergence. | Dao, *FlashAttention-2* (arXiv:2307.08691); Kwon et al., *PagedAttention/vLLM* (SOSP 2023, arXiv:2309.06180); Zheng et al., *SGLang* (2024). | Project 06 WGSL paged decode; Project 08 fused Triton Top-K SAE; measure FLOPs/byte and achieved bandwidth. | Analyze HBM traffic; explain how online softmax avoids the N×N matrix; debug warp divergence; compute the speculative-decoding break-even. |
| **D2. Routing, graph/vector indexing, observability** | Systems architecture | **High / 15+ years.** Heterogeneous model fleets need learned routing; code and docs need hybrid graph-vector retrieval. | Contextual bandits; matrix factorization; Bradley-Terry; HNSW; Leiden modularity; OpenTelemetry spans. | Ong et al., *RouteLLM* (ICLR 2025, arXiv:2406.18665); Zeng et al., *MetaRouter* (IJCAI 2026, arXiv:2606.06178); Edge et al., *GraphRAG* (arXiv:2404.16130). | Project 05: K≥4 preference-aware router to INT8 ONNX; Project 07: AST-GraphRAG with incremental Leiden. | Design a <10 ms routing gateway at 10k RPS with fallback, drift detection, and cache invalidation. |
| **E. Full-stack local-first systems: Rust, TS, WASM, SQLite/DuckDB** | Foundational engineering | **High / permanent.** Zero-server and edge-native architectures remove hosting burn and preserve data sovereignty. | Rust ownership; WASM linear memory; WebRTC SCTP; OPFS; MVCC; WAL locking; zero-copy `ArrayBuffer` transfer. | NIST FIPS 203; WebGPU WGSL spec; DuckDB-WASM architecture; SQLite WAL docs. | Project 09: stream encrypted LoRA shards into EdgeInfer; add cross-reload OPFS resume; measure receiver RSS. | Deep-dive zero-copy across JS/WASM, OPFS locking, backpressure over WebRTC. |
| **F. Frontier: world models, mechanistic interpretability, safety** | Research frontier | **Growing / 20+ years.** Verifying internal representations and steering activations without capability loss is a safety requirement. | Sparse autoencoders; dictionary learning; L1/Top-K sparsity; activation patching; causal interventions. | Bricken et al., *Towards Monosemanticity* (2023); Templeton et al., *Scaling Monosemanticity* (2024); Gao et al., *Top-K SAE* (arXiv:2406.04093). | Project 08: 16× Top-K SAE on Qwen2.5-Coder layer 14; clamp insecure-code features; measure CWE suppression vs pass@1. | Explain polysemanticity/superposition; design a steering intervention that suppresses SQL injection without degrading pass@1. |

---

## 2. What to deprioritize

| Deprioritize | Why | Replace with |
|---|---|---|
| Framework-specific LangChain chain recipes | The abstraction hides state, retries, and tool contracts; it changes every year. | Direct APIs + MCP + explicit state machine. |
| "Prompt engineering" as a primary skill | It is a communication skill, not a moat. | Evals, structured outputs, and determinism. |
| Training from scratch on a laptop | Cost and data make it non-competitive. | QLoRA/DPO on 1.5B–3B, evaluated honestly. |
| Dashboard-only "AI product" work | No defensible systems depth. | Local-first inference, security, or evaluation infrastructure. |
| Collecting certificates | Weak signal vs. reproducible artifacts. | One merged upstream PR + one published model. |
| Unverified benchmark claims | A retraction costs more than a missing number. | Evidence-gated claims (ADR-006). |

---

## 3. The durable stack, in one page

```
Mathematics:      linear algebra → probability → policy gradients → optimization
Systems:          memory hierarchy → kernels → serving → sandboxing → auditability
Models:           transformer internals → post-training (SFT/DPO/GRPO) → quantization
Agents:           MCP contracts → state machines → retries/idempotency → evals
Data:             deterministic fixtures → real benchmarks → significance testing
Product:          local-first UX → four states (empty/loading/degraded/error) → accessibility
```

The portfolio should have **one proof per layer**, not ten proofs of the same
layer. The project scorecard is designed around that rule.

---

## 4. 12-month learning cadence

| Weeks | Focus | Output |
|---|---|---|
| 1–3 | RL post-training + deterministic gates | Project 01 runner, 87 tests, first GPU run |
| 4–6 | GPU kernels + paged attention + SAEs | Project 06 design → parity; Project 08 eager SAE |
| 7–10 | Verbal RL, mutation testing, graph theory, routing | Project 03, 05, 07 benchmarks |
| 11–14 | PQC, multimodal ASTs, multi-tenant SaaS | Project 09, 04, 10 |
| 15–26 | Upstream PRs, papers, model cards, interviews | 1 merged PR, 1 paper draft, 3 model/dataset cards |
| 27–52 | Depth: pick two domains (post-training + kernels) | One substantial result, not ten small ones |

The cadence is deliberately slower than the brief's 14-week "all ten projects"
plan. Ten shallow projects do not beat two deep ones for a research-engineer
loop; the scorecard keeps the ten as a menu, not a mandate.
