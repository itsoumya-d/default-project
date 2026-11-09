# Step 2 — What Anthropic, OpenAI, and Google Signal for, Mapped to This Portfolio (2026-11-09)

Web research (queries run 2026-11-09; key sources at bottom). This report turns
lab publishing + hiring practice into a feasibility map against repos that
already exist locally. No fabricated metrics: the only numbers cited are this
portfolio's own measured results or explicitly marked as external facts.

## 1. The consistent hiring signal (all three labs)

Independent, verifiable research depth beats pedigree:

- Anthropic's own guidance leads with **"independent research, a careful blog
  post, or a real open-source contribution"** (EduAv­enues summary of Anthropic's
  stated hiring stance).
- Anthropic's engineering blog (`anthropic.com/research/demystifying-evals-for-ai-agents`,
  2026 agentic-coding report) publishes **eval design methodology**, not vibes.
- Hugging Face's ICML-2026 reproduction post ("What We Learned by Reproducing
  2,200 papers from ICML") states the artifact hierarchy plainly: runnable
  reproduction > reported number.
- The recurring GitHub/HF signals that interviewers can click and run:
  1. a paper reimplementation with the equation, seed, and log present;
  2. fine-tuned weights/LoRA with a Model Card + eval table;
  3. a custom eval dataset with a Dataset Card (known failure modes included);
  4. benchmarks with hardware/seed/command stamps and negative results kept;
  5. technical reports that name what the implementation does *not* do.

**Gap this exposes (see `AUDIT_2026-11-09.md` §Quality gaps):** the portfolio
has 1+2-partial+3+4 but **zero HF model artifacts** and stub research dirs.

## 2. Papers / reports mapped to local repos

| Lab | Paper / report (2026 horizon) | Local repo | Status | Next build |
|---|---|---|---|---|
| DeepSeek | GRPO (DeepSeek-R1 family) | HEROS-RL, P01 rlvr-studio | works: P01 100-step RL-from-base, mean reward −0.23→−0.04 | bias-probe experiment (this session) |
| Dr.GRPO | length/difficulty bias critique | P01 `RL_BASE_100.md` already uses "Dr.GRPO centered advantages" | readability gap: claims correct, synthesis missing | literature review (this session) |
| DAPO | entropy collapse / asymmetric clipping | same | same | same review |
| Anthropic | Reflexion (Shinn et al., self-eval loop) | Reflexion-SWE | toy ablation only | Lite-50 run (deferred; spec'd) |
| Anthropic/OpenAI | SWE-Bench Verified | Reflexion-SWE `prepare_swebench_lite.py` exists, no Lite-50 result | **unfinished** | deferred GPU run |
| GraphRAG (Microsoft, adopted by Google/Anthropic-style RAG stacks) | local→global hierarchical summarization | GraphRAG-CodeAudit | eval committed (`results/eval_results.json`) | cross-project bench (this session) |
| Anthropic | Demystifying evals for AI agents (2026) | genai-tooling-evals, HEROS-Firewall redteam | partial | cross-project bench + results table |
| Google/DeepMind | ColPali visual document retrieval | colpali-edge | 25 unit tests pass | deeper README/results check (deferred) |
| OpenAI | image2code / SVG-UI-gen style visual evals | image2code-bench | deps missing locally; CI green | verify locally (deferred) |
| Anthropic | Anthropic-PerfBench-style kernel perf | Anthropic-PerfBench, edgeinfer | roofline committed | — (healthy) |

External anchors (for citation, not for portfolio claims): `arxiv.org/html/2606.17799v1`
(coding benchmarks misaligned with agentic SWE), `tianpan.co` SWE-bench gap post,
`featurebench` (ICLR 2026), HF "agentic-RL-2026" post ("reward directly paid for
length → model grew long for a simpler reason" — exactly the P01 failure shape).

## 3. Feasibility: what is honestly buildable on this machine

Hardware: **Windows 10, RTX 2060 6 GB, torch 2.14.1+cu130** (from prior P01 run
manifests), Python 3.11. Feasible and verifiable:

- ✅ CPU-only simulated-policy RL estimators (GRPO vs Dr.GRPO) — exact math, no
  GPU, deterministic seeds → this session's `rlvr-bias-probe`.
- ✅ Test-suite cross-project benchmark — pure pytest orchestration.
- ✅ Research writing (reviews, paper notes, reports) — zero compute.
- ✅ Profile README skin + sync script + workflow — zero compute.
- ⚠️ GPU LoRA re-training — feasible at P01's proven scale (100 steps ≈ 34 min
  wall time from the P01 manifest: 02:43→03:17 = 34 min), but any new GPU run
  this session would outrun a single turn; the prior 100-step result is what we
  report, and a 250-step `risk-calibration-weighted` rerun is specified as the
  next GPU job.
- ❌ Full SWE-Bench Lite-50 — needs ~1,000+ GPU generations + curated task
  files; spec'd, not run. Claiming it would be fabrication.

## 4. Reward-shaping conclusion from P01's own logs

The 100-step run's eval table (`eval_final`, 50 held-out tasks) shows:
REQUIREMENT_MISS 33/50, SQL_EXEC_ERROR 7/50, risk_accuracy 0.10,
decision_accuracy 0.50, ok_rate 0.20 — i.e. the policy can produce valid SQL
shape but cannot choose the *right* migration nor label its risk. Any next RL
run must up-weight `risk_calibration` + `requirement` terms and *fix risk
prediction before scaling steps*. This is the design decision recorded in
`DECISIONS.md` (D-2026-11-09-001).

## Sources (2026-11-09 queries)

- EduAv­enues, "What Anthropic and OpenAI Hire For, Beyond a Pedigree"
- Anthropic, "Demystifying evals for AI agents" (anthropic.com/research)
- Hugging Face, "What We Learned by Reproducing 2,200 papers from ICML" (2026)
- Hugging Face, "Agentic RL 2026" series; "State of Open Source on HF: Spring 2026"
- arXiv 2606.17799 (coding benchmarks vs agentic SWE); featurebench (ICLR 2026)
- tianpan.co, "Agentic Coding in Production: What SWE-bench Scores Miss" (Apr 2026)
- Interconnects, "Recent reasoning research: GRPO tweaks, base-model RL"
- Kili Technology, "GRPO Explained"; Cameron Wolfe, "GRPO++" (substack)
- OpenTrain, "GRPO for Reasoning-Model Post-Training" (verifier errors become targets)
- Unifying GRPO Frameworks (arXiv 2510.06870) — length bias: one advantage
  uniformly assigned to all tokens of a response
- swebench.com leaderboards (Verified / Lite / Multilingual / Multimodal)
