# AI Engineering Portfolio — Execution Workspace

Owner: **Soumya Debnath** (`itsoumya-d` on GitHub, `itssoumyad` on Hugging Face)
Audit date: **2026-11-02**
Status: **Stage 9 — requirement check works; old adapter invalid; SFT/target-diff
warm start is next**

This directory is the operating system for the portfolio transformation: the
audit, the research map, the ten-project scorecard, the platform strategy, the
infrastructure constraints, and the execution log. It is deliberately kept
separate from the repositories it changes, so a lost session can resume from
`PROGRESS_LOG.md` and `DECISIONS.md` without re-deriving context.

---

## 1. What is actually true right now

The supplied brief described an 11-repository, 13-artifact estate. Live
inspection on 2026-11-02 found a larger and newer estate, and several brief
claims that are already stale. The numbers below are the ones to use.

| Fact | Verified state | Evidence |
|---|---|---|
| Public GitHub repositories | **30** | GitHub profile, 2026-11-02 |
| Repositories audited in depth | **11** | shallow clones + test runs |
| Hugging Face Spaces | **11** | `huggingface.co/itssoumyad` |
| Hugging Face datasets | **2** (`graphrag-questions-100`, `heros-migration-500`) | HF profile |
| Hugging Face public models | **0** | HF profile |
| HF collection | 1 (`HEROS AI Systems Portfolio`) | HF profile |
| HEROS MCP tests | **46 test functions pass; 289 adversarial cases** | `npm run test:mcp` |
| HEROS `rlvr` tests | **93 total: 93 pass with torch; 80 pass + 13 skip without** | `unittest`, `main` at `c32614f` |
| HEROS-RL tests | **40 pass, 5 skipped** | `unittest` |
| GPU smoke run | **10 steps, 7 optimizer steps, mean reward 0.339, 4.15 GB peak** | RTX 2060, `runs/2026-11-02-gpu-smoke-1.5b/` |
| 500-step run | **500 steps, 209 optimizer steps, mean reward 1.0203, 4.16 GB peak** | `runs/2026-11-02-a3-500-qwen1.5b/` |
| Held-out eval | **base 0.71 vs adapter 1.465; risk 0.16 vs 0.02; 36/50 no-op migrations** | `eval_450/` |
| Corrected reward | old adapter re-scores at 0.265, 40/50 `REQUIREMENT_MISS`; smoke has 9/20 misses | `runs/.../MODEL_CARD.md` |
| Published model weights | **0** | no HF upload |
| Upstream PRs merged | **0** | no evidence in the audited repos |

The most important correction: **`HEROS-RL` already exists** and contains a
critic-free GRPO engine, a 500-case migration dataset, a toy ablation, and
TRL/Unsloth training entry points. Project 01 must not rebuild it. The work is
to add the missing deterministic SQLite shadow verifier, wire the GPU run, and
publish evidence.

The second correction: the brief's claims that `peervault` still denies its PQC
implementation and that `edgeinfer` says "Replaces OpenAI API" are **not true of
the current READMEs**. Both have been rewritten honestly. `peervault` still has
two narrow documentation contradictions (resume and OPFS), and `edgeinfer` still
lacks the paged kernel. The staged PRs target those real gaps.

---

## 2. Evidence policy

Every claim in this workspace carries one of these markers:

| Marker | Meaning |
|---|---|
| **[V]** | Verified in this session by a command, test run, or live page. |
| **[D]** | Documented upstream (README, CI, model card) but not independently reproduced here. |
| **[P]** | Planning estimate from the supplied brief; not an empirical measurement. |
| **[X]** | Contradicted by live inspection; do not repeat. |

The audit scores in `PORTFOLIO_AUDIT.md` are marked **[P]**. They are useful for
ranking work, not for a resume or a funding deck. A score becomes **[V]** only
after the rubric evidence exists in a repository and a command reproduces it.

---

## 3. Workspace map

```
AI_ENGINEERING_PORTFOLIO/
├── README.md                     # this file
├── MASTER_ROADMAP.md             # 14-week execution plan and gates
├── PORTFOLIO_AUDIT.md            # live baseline, corrections, gap matrix
├── FUTURE_AI_SKILLS_MAP.md       # six durable skill domains
├── SKILLS_ROADMAP.md             # four-stage dependency graph
├── PLATFORM_STRATEGY.md          # GitHub / HF / site / W&B / arXiv / Colab / writing
├── CAREER_ALIGNMENT.md           # roles, proof, compensation bands
├── INFRASTRUCTURE_STRATEGY.md    # RTX 2060 / MacBook / Kaggle / free-tier limits
├── RESEARCH_LIBRARY.md           # nine papers, math, limitations, targets
├── PROJECT_SCORECARD.md          # ten projects, ranking, specs, acceptance gates
├── DECISIONS.md                  # ADR-001 … ADR-012
├── PROGRESS_LOG.md               # append-only session log
├── research/
│   ├── papers/                   # citation cards and reading queue
│   ├── literature_reviews/
│   ├── benchmarks/
│   └── market_research/
├── projects/
│   ├── project-01-heros-rlvr-studio/   # verifier + runner + PR packets
│   └── project-02 … project-10/        # specifications only
├── infrastructure/
├── learning/
├── open_source/
│   └── patches/                  # four git-format-patch files
└── portfolio_website/
```

---

## 4. Merged pull requests

| Live PR | Repository | Head commit | Merge commit | Result |
|---|---|---|---|---|
| [#101](https://github.com/itsoumya-d/HEROS/pull/101) | `itsoumya-d/HEROS` | `f49a6c1` | `8a7951d` | merged; 18/18 green |
| [#103](https://github.com/itsoumya-d/HEROS/pull/103) | `itsoumya-d/HEROS` | `0ac89ff` | `d3588ca` | merged; 18/18 green |
| [#104](https://github.com/itsoumya-d/HEROS/pull/104) | `itsoumya-d/HEROS` | `52fd18b` | `d38a603` | merged; 18/18 green |
| [#105](https://github.com/itsoumya-d/HEROS/pull/105) | `itsoumya-d/HEROS` | `af79d28` | `a8451f6` | merged; 18/18 green |
| [#106](https://github.com/itsoumya-d/HEROS/pull/106) | `itsoumya-d/HEROS` | `e608a36` | `83a1b96` | merged; 18/18 green |
| [#107](https://github.com/itsoumya-d/HEROS/pull/107) | `itsoumya-d/HEROS` | `57fb564` | `f0e22d6` | merged; 18/18 green |
| [#108](https://github.com/itsoumya-d/HEROS/pull/108) | `itsoumya-d/HEROS` | `8f747ae` | `c32614f` | merged; 18/18 green |
| [#14](https://github.com/itsoumya-d/peervault/pull/14) | `itsoumya-d/peervault` | `4ad241e` | `7025352` | merged; 3/3 green |
| [#15](https://github.com/itsoumya-d/edgeinfer/pull/15) | `itsoumya-d/edgeinfer` | `2dd3bc0` | `088c217` | merged; 2/2 green |

#101 added `gpu_trainer.py` (shadow verifier + Dr.GRPO/DAPO loss), 17 tests, a
CPU-torch CI job, a benchmark protocol, and documentation. The PyTorch path
delegates to the existing CPU references where possible; two parity tests pin the
tensor advantage and loss implementations. #103 added the QLoRA runner: strict
Forge-schema → SQLite bridge, 27 tests, a fake-policy rollout loop, a run
recorder, a dry-run CLI, and the `HFPolicy` adapter. #104 added a literal tag
exemplar after a GPU smoke exposed Markdown-vs-tag format failures. #105
recorded the GPU smoke, #106 added held-out evaluation, and #107 added a
target-schema requirement check that rejects no-op migrations. #14 fixed the two
real README contradictions. #15 added a design-only WGSL paged-attention note;
it does not claim a kernel or a speedup.

The post-merge `main` commit is `c32614f` (the 500-step run used `d38a603`); the
full `rlvr` suite was re-run at 93 pass with torch and 80 pass + 13 skip without. A 10-step 1.5B GPU smoke then
completed 7 optimizer steps at 4.15 GB peak. The 500-step single-arm run then
finished 500 steps with 209 optimizer steps, mean reward 1.0203, and 4.16 GB
peak. The 50-task held-out evaluation found base 0.71 vs adapter 1.465, but risk
accuracy fell from 0.16 to 0.02; 36/50 adapter completions were safe no-op
`ADD COLUMN` migrations. This is a reward-hacking negative, not a success. The
#107 requirement check re-scores the old adapter at 0.265 (40/50 requirement
misses), and a 10-step corrected-reward smoke still had 9/20 misses. The next
work is SFT/target-diff prompting, not another long RL run. Merged remote
branches were deleted.

Review packets live in `projects/project-01-heros-rlvr-studio/PR_DESCRIPTION.md`,
`PR_DESCRIPTION_P5.md`, and the two repository README sections. The PRs were
opened and merged after explicit owner approval. No npm publish, HF upload, or
deployment occurred. The local patches remain in `open_source/patches/` for
offline review.

---

## 5. Resume protocol

1. Read `PROGRESS_LOG.md`, then `DECISIONS.md`.
2. Run `git -C repos/<name> status` and `git -C repos/<name> branch --show-current`.
3. Re-run the last verified command from the log.
4. Continue at the first unchecked item in `MASTER_ROADMAP.md`.
5. Never re-do a committed PR branch; rebase it on `origin/main` if upstream moved.

Environment used in this session:

```powershell
# PyTorch CPU venv (outside the workspace; the .venv inside the workspace hit
# a Windows ACL error)
$env:TEMP\opencode\heros-venv\Scripts\python.exe

# HEROS test command
$env:PYTHONPATH="rlvr/src"
& "$env:TEMP\opencode\heros-venv\Scripts\python.exe" -m unittest discover -s rlvr/tests -v
```

---

## 6. Immediate next actions

1. **Build an SFT/target-diff warm start.** The base 1.5B cannot satisfy most
   target schemas; RL alone is training on failures. Supervise correct
   expand-and-contract examples first.
2. **Do not publish the old adapter.** It is invalid under #107. Keep the model
   card local and negative.
3. **Run a new held-out evaluation after the warm start**, then the four-arm
   ablation. Do not compare arms before requirement satisfaction is learnable.
4. **Open one upstream PR** (TRL Dr.GRPO toggle is the smallest credible one)
   after the reward and warm start work.
5. **Start P06/P02** on CPU while the SFT pipeline is built.

---

## 7. Non-goals and guardrails

- No fabricated benchmark numbers, stars, downloads, or user counts.
- No "Replaces OpenAI/AWS" language.
- No public deployment without explicit approval.
- No secrets in Markdown, notebooks, or commits.
- No direct commits to `main`.
- No claims of GPU training until a run log and checkpoint exist.
