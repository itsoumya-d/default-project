# Research Library — Verified Papers and Reproduction Targets

Citation verification: every arXiv ID below was queried against the live arXiv
API on **2026-11-02**. All returned a matching title. This matters because the
portfolio cites 2025–2026 work, and a single fabricated citation would be fatal
in a research interview.

Status markers: **[V]** citation verified live; **[D]** result documented in the
paper but not reproduced here; **[P]** planned target.

---

## 1. Reproduction baselines (do not copy blindly)

| Paper / benchmark | Reported baseline vs. intervention | Reported metric | What it actually teaches | Status |
|---|---|---|---|---|
| Reflexion — HumanEval Python | GPT-4 single sample 80.1% → Reflexion 91.0% | pass@1 | Verbal critique over unit-test feedback helps when the tests are accurate. | **[D]** |
| Reflexion — MBPP Python | GPT-4 80.1% → Reflexion 77.1% | pass@1 | Self-generated tests produce false positives; the agent locks in buggy code. | **[D]** |
| Reflexion — HumanEval Rust (50 hardest) | Full 0.68 vs. no critique 0.60 vs. no test execution 0.52 | pass@1 | Critique and execution are synergistic; neither alone is enough. | **[D]** |
| RouteLLM — MT-Bench | GPT-4 baseline vs. preference router (GPT-4 + Mixtral 8×7B) | ~3.7× cost reduction at comparable quality | Preference data transfers across model pairs; ~1,500 domain samples can be enough. | **[D]** |
| RouteLLM — MMLU / GSM8K | Random router vs. augmented preference router | >2× savings; >40% cheaper than commercial routers | Chatbot Arena data alone can underperform random routing until golden-label or judge augmentation is added. | **[D]** |

**Rule for this portfolio:** reproduce the *direction* and the *failure mode*
first, then report the absolute number with the exact model, prompt, harness,
decoding settings, and hardware. A 2-point gain on a 164-problem HumanEval split
is within noise; do not headline it without a confidence interval.

---

## 2. Paper cards

### 2.1 RouteLLM and MetaRouter — cost-quality routing

**RouteLLM: Learning to Route LLMs with Preference Data** — Ong, Almahairi, Wu,
Chiang, Wu, Gonzalez, Kadous, Stoica. ICLR 2025. arXiv:2406.18665. **[V]**

**Learning to Route LLMs from Implicit Cost-Performance Preferences via
Meta-Learning (MetaRouter)** — Jiahao Zeng, Ming Tang, Ningning Ding. IJCAI 2026,
pp. 6045–6053. arXiv:2606.06178. **[V]**

**Mechanism.** A router estimates the probability that the strong model beats the
weak model for a query, using a Bradley-Terry model:

```text
P(win_strong | q) = σ(s(q, M_strong) − s(q, M_weak))
```

`s` can be a matrix-factorization scorer, a BERT classifier, a causal-LM
likelihood, or a kNN score. Training uses human preference battles, optionally
augmented with golden-label or LLM-judge data. MetaRouter adds a latent
preference context encoder `z = E_φ(c_1:N)` inferred from a few pairwise
feedback events, then routes across K ≥ 4 models under a cost-performance
preference.

**Documented limitations.** Binary strong-vs-weak routing does not handle K ≥ 4
specialized models of equal size. Arena data alone can underperform random
routing on MMLU/GSM8K until domain augmentation is added. Preference drift and
provider price changes invalidate a frozen router.

**Dependencies / data / hardware.** PyTorch, HF Transformers, scikit-learn;
Chatbot Arena (~80k battles), MT-Bench, MMLU, GSM8K, RouterBench (405k+
outcomes). A router fits in <4 GB VRAM; the RTX 2060 is sufficient.

**Portfolio target (Project 05).** Upgrade `RouteLLM-Gateway` to K ≥ 4 with a
latent context encoder, export to INT8 ONNX (<15 MB), and report APGR, CPT-95,
and p99 routing latency. **Metric:** >2.5× cost reduction on MMLU/GSM8K at
≤1 point quality loss; p99 < 6 ms.

---

### 2.2 Reflexion — verbal reinforcement learning

**Reflexion: Language Agents with Verbal Reinforcement Learning** — Shinn,
Cassano, Berman, Gopinath, Narasimhan, Yao. NeurIPS 2023. arXiv:2303.11366. **[V]**

**Mechanism.** The policy is parameterized by an actor `M_a` and an episodic
memory, not by updated weights:

```text
θ = {M_a, mem}
sr_k = M_sr(τ_k, r_k, mem_k)          # verbal self-reflection
mem_{k+1} = bounded(mem_k ∪ {sr_k}, Ω) # Ω ∈ [1, 3]
```

The actor retries the task with the reflection in context. No gradient step is
taken. The paper's coding results use unit-test feedback as the reward signal.

**Documented limitations.** MBPP regresses because self-generated tests have
false positives. A sliding window `Ω=3` discards cross-task lessons. WebShop
stagnates after ~4 trials. The method depends on a reliable evaluator; with a
weak evaluator it reinforces wrong behavior.

**Dependencies / data / hardware.** HumanEval (Python/Rust), MBPP, HotPotQA,
ALFWorld. A 3B QLoRA local model or a hosted API is enough; no GPU training is
required for the Reflexion loop itself.

**Portfolio target (Project 03).** Add a Hypothesis property-based + AST mutation
adequacy gate: a self-generated test suite must kill ≥80% of synthetic mutants
before it can grade a patch. Add a persistent Matryoshka skill library
(`d=64→768`) instead of the Ω=3 window. **Metric:** eliminate the MBPP
regression, report HumanEval/SWE-bench Lite-50 pass@1 and false-positive test
rate (<2%).

---

### 2.3 GraphRAG — local-to-global retrieval over a graph

**From Local to Global: A Graph RAG Approach to Query-Focused Summarization** —
Edge, Trinh, Cheng, Bradley, Chao, Mody, Truitt, Metropolitansky, Ness, Larson.
Microsoft Research, 2024. arXiv:2404.16130. **[V]**

**Mechanism.** Build an entity-relationship graph `G=(V,E,W)`, partition it into
hierarchical communities with Leiden, and pre-generate community summaries. A
global query is answered by map-reduce over the summaries.

```text
Q = (1/2m) Σ_ij (A_ij − γ k_i k_j / 2m) δ(c_i, c_j)
```

Leiden maximizes modularity `Q` with a resolution parameter `γ`. Local search
fans out from entities; global search summarizes communities.

**Documented limitations.** LLM-based entity extraction over every chunk costs
10–50× the tokens of flat RAG and hallucinates edges. Community summaries drift
when the corpus changes; incremental updates are not free. The paper evaluates
query-focused summarization, not code navigation.

**Dependencies / data / hardware.** `microsoft/graphrag`, Tree-sitter, igraph,
leidenalg, DuckDB. CPU-only AST parsing is sufficient for a 1M-token corpus.

**Portfolio target (Project 07).** Replace LLM extraction with deterministic
Tree-sitter AST + taint edges; add incremental git-diff Leiden updates; curate
`ast-graphrag-codebench-1000` across 10 real repos. **Metric:** Recall@10 >0.88
on multi-hop dependency queries, ≥90% indexing-token reduction vs. LLM-GraphRAG,
<800 ms incremental update.

---

### 2.4 SWE-bench — repository-level repair

**SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** — Jimenez,
Yang, Wettig, Yao, Pei, Press, Narasimhan. ICLR 2024. arXiv:2310.06770. **[V]**

**Mechanism.** 2,294 issues from 12 Python repositories. The agent receives a
codebase and an issue, edits the repo, and is graded by tests: every
`FAIL_TO_PASS` test must pass and every `PASS_TO_PASS` test must stay green.
Predictions are git diffs evaluated in isolated Docker containers.

**Documented limitations.** The full suite needs >120 GB of Docker storage and
long wall-clock time. Agents corrupt repos, loop forever, or overfit to the
issue text. Test coverage is incomplete; a patch can pass while being wrong.
SWE-bench Lite (300 instances) is the practical subset.

**Dependencies / data / hardware.** `swe-bench/SWE-bench`, `docker-py`,
`princeton-nlp/SWE-bench_Lite`. A local Docker host or an Oracle Always Free ARM
VM with 200 GB disk is enough for Lite-50.

**Portfolio target (Project 03).** Run Lite-50 with HEROS Merkle receipts and a
deterministic rollback gate. **Metric:** % resolved, mean tokens per resolved
issue, and zero corrupted-container states.

---

### 2.5 GRPO → Dr.GRPO → DAPO — verifiable RL post-training

**DeepSeekMath** — Shao et al., 2024. arXiv:2402.03300. **[V]**
**DeepSeek-R1** — Guo et al., 2025. arXiv:2501.12948. **[D]**
**Understanding R1-Zero-Like Training (Dr.GRPO)** — Liu et al., 2025.
arXiv:2503.20783. **[V]**
**DAPO** — Yu et al., 2025. arXiv:2503.14476. **[V]**
**Demystifying GRPO: its policy gradient is a U-statistic** — Zhou et al., 2026.
arXiv:2603.01162. **[V]**

**GRPO objective.** Sample `G` completions per prompt, compute a group-relative
advantage, and skip the value critic:

```text
r_{i,t}(θ) = π_θ(o_{i,t} | q, o_{i,<t}) / π_{old}(o_{i,t} | q, o_{i,<t})
Â_i = (R_i − mean(R)) / (std(R) + ε)

J_GRPO = E[ (1/G) Σ_i (1/|o_i|) Σ_t
          min(r_{i,t} Â_i, clip(r_{i,t}, 1−ε, 1+ε) Â_i)
          − β D_KL^{(i,t)} ]
```

The k3 KL estimator is:

```text
ρ = log π_ref(o_t) − log π_θ(o_t)
D_KL = exp(ρ) − ρ − 1        # always ≥ 0
```

**Dr.GRPO correction.** GRPO's `1/|o_i|` and `1/std(R)` introduce a length and
difficulty bias. Dr.GRPO removes both and uses a constant horizon `L_max`:

```text
L_Dr.GRPO = −(1/G) Σ_i (1/L_max) Σ_t
            [ min(r_{i,t} Â_i, clip(...) Â_i) − β D_KL ]
```

**DAPO corrections.** Token-level normalization `1/Σ_i|o_i|`, decoupled clipping
`[ε_low, ε_high] = [0.2, 0.28]`, dynamic sampling that drops groups with accuracy
0 or 1, and overlong-reward shaping.

**Documented limitations.** Requires a verifiable reward (math answer, compiler,
schema gate). KL can collapse the policy; too little KL allows reward hacking.
Group size controls variance; `G=1` has no learning signal. A U-statistic view
gives a finite-sample error bound and a scaling law for choosing `G`.

**Dependencies / data / hardware.** PyTorch, HF Transformers, PEFT, TRL,
bitsandbytes; `b-mc2/sql-create-context`, `xlangai/spider`,
`HuggingFaceH4/MATH-500`. RTX 2060 6 GB for 4-bit QLoRA `G=4` on 1.5B; Kaggle
2×T4 32 GB for `G=8` on 3B.

**Portfolio target (Project 01).** Wire the SQLite shadow verifier into the
reward, run 500 steps, publish the adapter, and report MATH-500 pass@1, response
length stability, KL, clip fraction, and reward variance. **Metric:** no claim
until the run exists; target a measurable calibration gain, not a fabricated
+18%.

---

### 2.6 Matryoshka, PagedAttention, FlashAttention — retrieval and decoding

**Matryoshka Representation Learning** — Kusupati et al., NeurIPS 2022.
arXiv:2205.13147. **[V]**
**PagedAttention / vLLM** — Kwon et al., SOSP 2023. arXiv:2309.06180. **[V]**
**FlashAttention-2** — Dao, ICLR 2024. arXiv:2307.08691. **[V]**

**MRL.** Optimize nested prefixes simultaneously:

```text
L_MRL = Σ_{m ∈ M} c_m · L(z_{1:m}, y),   M = {64, 128, 256, 768}
```

The same embedding supports a coarse INT8 scan at `d=64` and a fine FP32 rerank
at `d=768`; no separate model is needed.

**PagedAttention.** Partition the KV cache into fixed-size blocks
(`block_size=16`), map logical blocks through a block table, and allocate
physical blocks on demand. This removes external fragmentation and enables
prefix sharing. vLLM reports 2–4× throughput at the same latency.

**FlashAttention-2.** Tile Q/K/V in SRAM and compute attention with an online
softmax, never materializing the N×N matrix:

```text
m_new = max(m_old, m_block)
α = exp(m_old − m_new)
l = l·α + Σ exp(s − m_new)
acc = acc·α + Σ exp(s − m_new)·v
```

**Documented limitations.** Browser ONNX wrappers cannot pin `past_key_values`
in a `GPUBuffer` without a custom kernel; MRL truncation changes the embedding
norm and needs re-normalization; PagedAttention assumes a serving engine that
owns the KV cache.

**Dependencies / data / hardware.** `onnxruntime-web ≥1.21.0`, WebGPU, WGSL;
SmolLM2-135M/360M ONNX; `mteb/scifact`; RTX 2060 and Apple Silicon WebGPU.

**Portfolio target (Project 06).** Implement `paged_flash_decoding.wgsl` and
`matryoshka_int8_scan.wgsl`, prove zero CPU KV readback, and measure an INT8 scan
speedup. **Metric:** parity with the ORT baseline, 0 `mapAsync` on KV buffers,
and a documented p50/p95 on two devices. No speedup claim before parity.

---

### 2.7 Sparse autoencoders and Triton kernels

**Towards Monosemanticity** — Bricken et al., 2023. **[D]**
**Scaling Monosemanticity** — Templeton et al., 2024. **[D]**
**Scaling and evaluating sparse autoencoders (Top-K SAE)** — Gao et al., 2024.
arXiv:2406.04093. **[V]**
**Triton** — Tillet et al., MAPL 2019. **[D]**

**Mechanism.** Decompose a residual-stream activation `x ∈ R^d` into an
overcomplete sparse feature basis:

```text
z = TopK(W_enc (x − b_dec) + b_enc, k)
x̂ = W_dec z + b_dec
L = ||x − x̂||²  (+ optional auxiliary dead-latent loss)
```

With `d_model=1536`, a 16× SAE has `d_sae=24,576`; `k=64` controls the L0 norm.
A feature can be clamped or steered at inference to suppress a behavior.

**Documented limitations.** Dead latents, feature splitting, and imperfect
reconstruction (`R² < 1`). A causal claim requires activation patching, not
correlation. Eager training is HBM-bound because the encoder, TopK, and decoder
round-trip large buffers.

**Dependencies / data / hardware.** PyTorch 2.4+, Triton, safetensors;
`bigcode/the-stack-smol`, `CyberNative/Code_Vulnerability_Security_DPO`. RTX 2060
6 GB (Turing SM 7.5) can train a 24k-feature SAE in fp16 in a few hours if the
activation buffer is streamed.

**Portfolio target (Project 08).** Fuse centering + projection + TopK in Triton;
train on Qwen2.5-Coder-1.5B layer 14; clamp insecure-code features. **Metric:**
>2.4× kernel speedup, `R²>0.92`, CWE suppression without pass@1 regression.

---

### 2.8 FIPS 203 ML-KEM-768 and hybrid channels

**NIST FIPS 203, Module-Lattice-Based Key-Encapsulation Mechanism Standard**
(2024). **[D]** (standard; not an arXiv paper)

**Mechanism.** ML-KEM works over the ring:

```text
R_q = Z_q[X]/(X^256 + 1),  q = 3329
```

Key generation, encapsulation, and decapsulation use a 7-layer NTT/invNTT with
Montgomery reduction, SHAKE256-based sampling, and centered binomial
distribution noise (`η=2`). ML-KEM-768 uses `k=3`, a 1,184-byte encapsulation
key, and a 1,088-byte ciphertext. The hybrid channel concatenates the ML-KEM and
P-256 ECDH secrets and runs HKDF-SHA256:

```text
session = HKDF(ECDH_secret || ML-KEM_secret, salt=transcript_hash)
file_key = HKDF(share_link_key || session, salt=transcript_hash)
```

AES-256-GCM encrypts each 64 KB chunk with a fresh 96-bit IV and the full 21-byte
header as AAD.

**Documented limitations.** Not independently audited; side-channel resistance
depends on a constant-time implementation; browser WebRTC still needs a TURN
relay behind symmetric NAT; OPFS quotas vary by browser.

**Dependencies / data / hardware.** Rust `wasm32-unknown-unknown`, Web Crypto,
WebRTC, OPFS; 100 NIST KAT vectors. Runs on a laptop; <64 MB receiver RSS with
an OPFS sink is the target.

**Portfolio target (Project 09).** Add persistent OPFS `ChunkBitmap` resume,
merge the WASM worker mesh if `swarmcompute` is confirmed, and stream encrypted
LoRA/ONNX shards into `EdgeInfer.fromBuffer()`. **Metric:** 100/100 KAT, <64 MB
receiver RSS on a 500 MB transfer, and a real cross-reload resume test.

---

### 2.9 Design2Code — screenshot-to-code evaluation

**Design2Code: Benchmarking Multimodal Code Generation for Automated Front-End
Engineering** — Chenglei Si, Yanzhe Zhang, Ryan Li, Zhengyuan Yang, Ruibo Liu,
Diyi Yang. NAACL 2025. arXiv:2403.03163. **[V]**

**Mechanism.** 484 real webpages. A model receives a screenshot and generates
HTML/CSS. Automatic metrics include bounding-box overlap, CLIP similarity, and
normalized tree edit distance; human evaluation validates the ranking.

**Documented limitations.** The benchmark measures visual similarity, not
accessibility or maintainability. Generated code can look right and be
unusable. Layout recall is the weakest dimension for frontier models.

**Portfolio target (Project 04).** Add Playwright rendering, bounding-box IoU,
axe-core WCAG 2.2 AA checks, and a VLM repair loop. **Metric:** 100% AA pass on
the generated set, IoU improvement over the one-shot baseline, and a documented
human review sample.

---

## 3. Implementation map

| Project | Papers | First measurable gate |
|---|---|---|
| 01 HEROS-RLVR-Studio | GRPO, Dr.GRPO, DAPO, U-statistic | 500-step run + adapter + reward/KL/length logs |
| 02 HEROS-SafeAgent-OS | MCP spec, Merkle, OWASP ASI | 500-case adversarial corpus, 0 unapproved destructive migrations |
| 03 Reflexion-SWE-Bench | Reflexion, SWE-bench | MBPP regression eliminated; Lite-50 resolution rate |
| 04 Mobbin-UI-Compiler-VLM | Design2Code, MRL | WCAG 2.2 AA pass rate; IoU vs one-shot |
| 05 MetaRoute-Gateway | RouteLLM, MetaRouter | APGR, CPT-95, p99 <6 ms |
| 06 EdgeInfer-WGSL-v3 | MRL, PagedAttention, FlashAttention-2 | 0 KV readback, parity, p50/p95 |
| 07 AST-GraphRAG-CodeAudit | GraphRAG, Leiden | Recall@10 >0.88, ≥90% token reduction |
| 08 Triton-SAE-Safety | Top-K SAE, Triton | >2.4× kernel speedup, R²>0.92 |
| 09 PeerVault-PQC-AI | FIPS 203, MRL | 100/100 KAT, <64 MB RSS, resume test |
| 10 HEROS-Cloud-Control | MCP, Merkle, RouteLLM | 100% tamper detection, Lighthouse ≥98 |

---

## 4. Citation hygiene

- Cite the **paper version** you actually read (v1 vs v2 can change numbers).
- Link the arXiv abstract, not a PDF mirror.
- For 2026 papers (MetaRouter, GRPO U-statistic), include the venue and DOI when
  available; both were verified live.
- Never cite a paper as proof of your implementation. Cite it as the method, then
  link your own run log.
- If a number is from a synthetic fixture, label it "synthetic" in the same
  sentence. The portfolio's credibility depends on this.
