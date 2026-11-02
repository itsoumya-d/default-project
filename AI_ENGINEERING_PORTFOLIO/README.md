# AI Engineering Portfolio — Execution Workspace

Owner: **Soumya Debnath** (`itsoumya-d` on GitHub, `itssoumyad` on Hugging Face)
Audit date: **2026-11-02**
Status: **Stage 3 — Project 01 verifier + runner and docs complete; four PR
branches staged locally**

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
| HEROS `rlvr` tests | **78 total: 78 pass with torch; 65 pass + 13 skip without** | `unittest`, stacked runner branch |
| HEROS-RL tests | **40 pass, 5 skipped** | `unittest` |
| GPU training runs producing weights | **0** | no model artifacts on HF |
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

## 4. Staged work (awaiting approval; nothing pushed)

| PR | Repository | Branch | Local commit | Patch |
|---|---|---|---|---|
| #1 | `itsoumya-d/HEROS` | `feat/rlvr-dr-grpo-gpu-trainer` | `f49a6c1` | `open_source/patches/0001-feat-rlvr-add-deterministic-SQLite-shadow-verifier-a.patch` |
| #2 | `itsoumya-d/peervault` | `docs/peervault-sync-limitations` | `4ad241e` | `open_source/patches/0001-docs-synchronize-resume-and-OPFS-limitations-with-th.patch` |
| #3 | `itsoumya-d/edgeinfer` | `docs/edgeinfer-reconcile-readme` | `2dd3bc0` | `open_source/patches/0001-docs-add-WGSL-paged-attention-design-note-and-link-i.patch` |
| #4 (stacked on #1) | `itsoumya-d/HEROS` | `feat/rlvr-qlora-runner` | `b1d3010` | `open_source/patches/0004-feat-rlvr-add-QLoRA-rollout-runner-and-dataset-bridg.patch` |

PR #1 adds `gpu_trainer.py` (shadow verifier + Dr.GRPO/DAPO loss), 17 tests, a
CPU-torch CI job, a benchmark protocol, and documentation. The PyTorch path
delegates to the existing CPU references where possible; two parity tests pin the
tensor advantage and loss implementations. PR #4 stacks the QLoRA runner on PR #1:
strict Forge-schema → SQLite bridge, 27 tests, a fake-policy rollout loop, a
run recorder, a dry-run CLI, and a thin untested `HFPolicy` adapter. It has no GPU
run. PR #2 fixes the two real README contradictions. PR #3 adds a design-only
WGSL paged-attention note; it does not claim a kernel or a speedup.

Review packets live in `projects/project-01-heros-rlvr-studio/PR_DESCRIPTION.md`,
`PR_DESCRIPTION_P5.md`, and the two repository README sections. No remote was
written. No `git push`, no `gh pr create`, no npm publish, no HF upload happened.

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

1. **Approve or reject PR #1–#4.** Nothing moves without approval. Merge #1
   before #4; #4 is stacked.
2. **Install `gh`** (or authenticate git) so a PR can be opened without the
   browser; currently `gh` is not on `PATH`.
3. **Run the 500-step GPU ablation** for Project 01 on Kaggle 2×T4 or the local
   RTX 2060, checkpointing to HF every 50 steps.
4. **Publish one real model artifact.** Until a checkpoint exists, the HF
   profile remains a demos-only profile.
5. **Open one upstream PR** (TRL Dr.GRPO toggle is the smallest credible one)
   after the local test log is ready.

---

## 7. Non-goals and guardrails

- No fabricated benchmark numbers, stars, downloads, or user counts.
- No "Replaces OpenAI/AWS" language.
- No public deployment without explicit approval.
- No secrets in Markdown, notebooks, or commits.
- No direct commits to `main`.
- No claims of GPU training until a run log and checkpoint exist.
