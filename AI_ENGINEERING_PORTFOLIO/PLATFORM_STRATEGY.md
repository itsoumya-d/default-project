# Platform Strategy — Hub-and-Spoke Technical Identity

The hub is the GitHub repository; the spokes are Hugging Face, the portfolio
site, W&B, papers, notebooks, and writing. Every spoke must point back to a
reproducible artifact, and every artifact must have exactly one canonical home.

**Current state (2026-11-02):** 30 GitHub repos, 11 HF Spaces, 2 datasets,
0 public models, 1 collection, no personal site content verified, no public W&B
reports, no arXiv submission. The immediate job is not more platforms; it is one
real model artifact and a curated GitHub surface.

---

## 1. Platform matrix

| Platform | Tier / priority | Publish exactly | Never publish | Integration mechanism | Discovery vector | Free-plan verdict |
|---|---|---|---|---|---|---|
| **GitHub** (`itsoumya-d`) | **Tier 1 — mandatory** | 6 pinned repos: HEROS, HEROS-RL, peervault, edgeinfer, Reflexion-SWE, HEROS-Firewall. CI badges, reproducible benchmarks, clean commits. | Unmodified scaffolds; "Replaces OpenAI/AWS"; unverified numbers; stale limitation sections. | Actions build/test/release; npm publish from tags; Space sync workflow. | Every hiring engineer's first click; code search for Triton/GRPO/MCP/WebGPU. | 100% free (public repos + 2,000 CI min/mo). **Highest ROI.** |
| **Hugging Face** (`itssoumyad`) | **Tier 1 — mandatory** | QLoRA/RLVR adapters, 1k–5k-row datasets with cards, live Spaces, paper links in YAML. | Static HTML placeholders with no inference; toy datasets without cards; demo claims without telemetry. | Link `arxiv:2406.18665`, `arxiv:2303.11366`, `arxiv:2404.16130` in model/dataset YAML; Space README links the repo. | HF paper pages and dataset search; researchers inspecting citations. | 100% free (public models/datasets + CPU Spaces). **Highest ROI.** |
| **Portfolio site** (`itsoumya-d.github.io`) | **Tier 1 — executive hub** | 10 case studies with diagrams, benchmark tables, failure post-mortems, live WebGPU/WASM demos, verified links. | Skill percentage bars, fake testimonials, generic chatbot widgets, unbuilt demos. | GitHub Pages action; pull release tags via GitHub API; embed HF Spaces. | Resume header, LinkedIn featured, 60-second recruiter triage. | Free via GitHub/Cloudflare Pages. **High ROI.** |
| **W&B / MLflow** | **Tier 2 — empirical proof** | Public reports for P01 (reward/KL/length curves) and P08 (SAE reconstruction); exported SVG charts. | Unlabelled scratch runs; crashed sweeps; cherry-picked single points. | Embed read-only report links and SVGs in GitHub `RESULTS.md` and HF cards. | ML interviewers verifying a real training run. | Free personal/academic tier; MLflow local. **High ROI.** |
| **arXiv / OpenReview / Papers with Code** | **Tier 2 — research credibility** | 6–8 page LaTeX reports for `hostshift` (if confirmed), HEROS-RLVR, AST-GraphRAG; reproducible tables. | Blog posts dressed as preprints; no baselines; no variance. | Link GitHub + HF artifacts from the paper; submit to a workshop before a main track. | Semantic Scholar, Google Scholar, alphaXiv. | Free. **High ROI for research roles**, slow for product roles. |
| **Colab / Kaggle** | **Tier 2 — reproducibility engine** | One-click notebooks for P01 Dr.GRPO, P05 routing calibration, P08 Triton kernels. | Hardcoded local paths; unpinned deps; notebook-only code. | `notebooks/` in each repo; badge in README; Kaggle dataset mirror. | Hiring engineers click the badge to see if the code runs. | Free (Kaggle ~30 h/wk T4×2; Colab T4). **Essential.** |
| **LinkedIn / Hashnode / Dev.to** | **Tier 3 — distribution** | 10 post-mortems, one per flagship, each with a specific failure and a measured fix. | "Top 10 AI tools"; daily hype; reposted press releases. | Canonical Markdown in `blog/`, cross-posted with a canonical link. | Sourcer keyword search: Triton, GRPO, MCP, WebGPU, Rust WASM, vLLM. | Free. **Moderate ROI**, capped at one article per completed project. |

---

## 2. GitHub curation

### Pin six, not thirty

The profile currently shows 30 repos. A recruiter will not scroll. Pin:

1. `HEROS` — agent runtime, 289 adversarial cases, npm packages.
2. `HEROS-RL` — GRPO engine, 500-case dataset, training scripts.
3. `peervault` — Rust WASM ML-KEM-768, OPFS streaming.
4. `edgeinfer` — WebGPU/ONNX inference, Matryoshka retrieval.
5. `Reflexion-SWE` — code repair with verbal RL.
6. `HEROS-Firewall` — MCP security proxy with Merkle receipts.

Everything else stays public but unpinned. No archive without approval
(ADR-001).

### Repo README contract

Every pinned repo must answer, above the fold:

1. What problem does it solve?
2. What is the one command that proves it?
3. What is measured, on what hardware, and what is **not** implemented?
4. Where is the package/model/dataset?
5. What is the license?

### Commit hygiene

- Conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`).
- No commits directly to `main`; PR branches only.
- No generated artifacts committed unless they are the benchmark evidence.
- No secrets; `.env.example` only.

---

## 3. Hugging Face execution

### The missing model

The profile has 0 public models. The first upload should be the Project 01
adapter:

```
itssoumyad/heros-qwen2.5-coder-1.5b-rlvr
```

The card must state: base model, dataset, 500-step run, hardware, seed, loss/KL/
length curves, evaluation command, and the exact limitations. If the run is not
complete, do not upload a placeholder.

### Dataset cards

`heros-migration-500` and `graphrag-questions-100` need:

- YAML `language`, `license`, `task_categories`, `size_categories`;
- provenance and generation script;
- a "not human-verified" line if true;
- a baseline table and a known failure mode.

### Space hygiene

All 11 Spaces currently show "Running". Each Space README must include:

- a one-click "Load sample" button for the empty state;
- a visible hardware badge (CPU / GPU / WebGPU);
- a machine-readable error code on failure;
- a link to the GitHub source and the exact commit.

---

## 4. Portfolio site specification

Stack: Next.js with `output: 'export'`, Tailwind, static assets, no server.

**Hero badges (only if clickable to CI/test logs):**

- 289 adversarial MCP cases passing.
- 100/100 NIST ML-KEM-768 KAT vectors (link the test).
- 49 KB zero-dependency Rust WASM PQC core (link the build).
- 7–35 KiB Zero static binaries (link the release).

**Case study template:** problem → constraint → architecture diagram → benchmark
table → failure post-mortem → what I would do next → repo/paper links.

**Demos:** EdgeInfer Matryoshka scan and PeerVault ML-KEM encapsulation run
client-side. If WebGPU is unavailable, show a deterministic WASM fallback and a
badge, not a blank canvas.

**Never:** skill bars, "95% Python", fake testimonials, a generic chatbot, or a
public deploy without approval.

---

## 5. 30 / 60 / 90-day cadence

| Window | GitHub | HF | Writing | Measurement |
|---|---|---|---|---|
| **0–30 days** | #101/#103/#104/#105/#106/#14/#15 merged; pin six; add CI badges | Publish P01 adapter + model card | One post: "What a deterministic shadow verifier catches that a reward model misses" | 93 tests; first W&B run |
| **31–60 days** | P06 design → parity; P02 public 500-case bench | Upload `owasp-agentic-bench-500`; update Spaces | One post: "Zero-readback KV in WebGPU: the parity harness" | 0 KV readback; 500 cases |
| **61–90 days** | P08 SAE weights; P05 ONNX router | Upload SAE weights + routing benchmark | One post: "Top-K SAE on a 6 GB Turing card" | R²>0.92; p99 <6 ms |

The cadence is intentionally output-based, not activity-based. A week without a
merged artifact is a signal to cut scope, not to add a platform.

---

## 6. Cross-linking matrix

| From | To | Mechanism |
|---|---|---|
| GitHub README | HF model/dataset | Badge + direct link + commit SHA |
| HF model card | GitHub repo + W&B report | YAML `source` + links |
| Portfolio site | GitHub, HF, paper, W&B | Case-study footer |
| Paper | GitHub + HF + benchmark | Reproducibility appendix |
| W&B report | GitHub `RESULTS.md` | Public read-only link |
| LinkedIn post | Portfolio case study | Canonical URL |

One canonical URL per artifact. Mirrors are allowed; conflicting numbers are not.
