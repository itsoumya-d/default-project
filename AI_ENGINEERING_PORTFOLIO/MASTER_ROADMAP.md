# Master Roadmap — 14 Weeks, Five Flagships, One Evidence Standard

Window: **2026-11-02 → 2027-02-07** (14 weeks).
Owner: Soumya Debnath.
Execution model: agent prepares code, tests, docs, and review packets; the owner
runs GPU jobs and approves every remote write.

This is a dependency-aware plan, not a promise. A week can slip; a gate cannot be
faked. If a gate fails, the project ships a smaller honest artifact or stops.

---

## 1. Position at the start

| Item | State on 2026-11-02 | Marker |
|---|---|---|
| Live audit | 30 GitHub repos, 11 HF Spaces, 2 datasets, 0 models | **[V]** |
| Strategy workspace | 12 documents, 10 project directories | **[V]** |
| Project 01 code slice | verifier + Dr.GRPO/DAPO loss + QLoRA runner, 44 new tests | **[V]** |
| HEROS `rlvr` suite | 94 pass with torch; 81 pass + 13 skip without | **[V]** |
| Live PRs | [#101](https://github.com/itsoumya-d/HEROS/pull/101), [#103](https://github.com/itsoumya-d/HEROS/pull/103), [#104](https://github.com/itsoumya-d/HEROS/pull/104), [#105](https://github.com/itsoumya-d/HEROS/pull/105), [#106](https://github.com/itsoumya-d/HEROS/pull/106), [#107](https://github.com/itsoumya-d/HEROS/pull/107), [#108](https://github.com/itsoumya-d/HEROS/pull/108), [#109](https://github.com/itsoumya-d/HEROS/pull/109), [#110](https://github.com/itsoumya-d/HEROS/pull/110), [#111](https://github.com/itsoumya-d/HEROS/pull/111), [#112](https://github.com/itsoumya-d/HEROS/pull/112), [#113](https://github.com/itsoumya-d/HEROS/pull/113), [#114](https://github.com/itsoumya-d/HEROS/pull/114), [#115](https://github.com/itsoumya-d/HEROS/pull/115), [#116](https://github.com/itsoumya-d/HEROS/pull/116), [#117](https://github.com/itsoumya-d/HEROS/pull/117), [#118](https://github.com/itsoumya-d/HEROS/pull/118), [#119](https://github.com/itsoumya-d/HEROS/pull/119), [#14](https://github.com/itsoumya-d/peervault/pull/14), [#15](https://github.com/itsoumya-d/edgeinfer/pull/15) all merged; CI green | **[V]** |
| GPU runs | RL 500 steps found reward hacking; SFT warm start scores 1.90 held-out vs base 0.02; RL-from-SFT probe had 0/10 variance groups | **[V]** |
| Public model artifacts | none | **[V]** |
| `gh` CLI | not installed | **[V]** |

The first two weeks are therefore about **converting local commits into reviewed
upstream work** and **converting tests into a reproducible GPU run**. Everything
else waits.

---

## 2. Capacity and constraints

| Resource | Budget | Consequence |
|---|---|---|
| Owner time | ~15 h/week, 14 weeks ≈ 210 h **[P]** | Five flagships is already aggressive; no sixth. |
| Agent time | session-based, no GPU | Code, tests, docs, CI, review packets. |
| RTX 2060 | 6 GB, no bf16 | 1.5B QLoRA at `G=4`, 512 tokens, fp16. |
| Kaggle | ~30 GPU h/week, 2×T4 16 GB | 3B runs and the 500-step ablation if local OOMs. |
| HF | free, no token in this environment | Owner uploads adapters and cards. |
| CI | GitHub free 2,000 min/month | CPU tests only; no GPU runner. |
| Paid services | **zero** | SQLite/DuckDB/local models are the default path. |

**Hard rule:** the agent never claims a GPU result. A run is real only when a
`run.json`, a W&B link, and a checkpoint exist.

---

## 3. Gate definitions

Every project exits through the same seven gates (from `PROJECT_SCORECARD.md`):

| Gate | Question | Minimum evidence |
|---|---|---|
| G1 Build | Does a clean checkout run? | One documented command; pinned deps; no hidden local path. |
| G2 Test | Do unit, integration, and adversarial tests pass? | CI log with counts and runtime. |
| G3 Benchmark | Is the headline number measured? | Hardware, versions, seeds, baseline, correctness check, variance. |
| G4 Artifact | Is there something to inspect? | HF model/dataset card, npm package, or signed release. |
| G5 Docs | Do limitations match the code? | README + failure section + threat model where relevant. |
| G6 Review | Can a reviewer reconstruct the work? | PR with problem, diff, test log, benchmark delta. |
| G7 Honesty | Is every claim tagged? | `[V]` / `[D]` / `[P]` / `[X]` on quantitative claims. |

A project may be portfolio-ready at G1–G7 without being commercially viable.
Commercial work is a separate track and is out of scope for this window.

---

## 4. Timeline

| Week | Dates | Primary deliverable | Exit gate | Fallback if blocked |
|---:|---|---|---|---|
| 1 | Nov 2-8 | PRs #101–#119 merged; P01 QLoRA + SFT + P02 corpus/package | P01 SFT 1.90 held-out; 54 MCP tests; P02 500 records | Start P02 signed proofs |
| 2 | Nov 9–15 | P01 SFT + controlled RL-from-SFT | SFT 1.90 held-out; RL-from-SFT probe **negative** (0/10 variance groups) | RL from base with corrected reward |
| 3 | Nov 16–22 | P01 RL from base + ablation (Base, SFT, GRPO, Dr.GRPO+DAPO); MATH-500; HF adapter; W&B report | G3 + G4 for P01 | Ship 100-step negative result + protocol |
| 4 | Nov 23–29 | **Delivered early:** P02 corpus 289 → 500 cases; Ed25519 signing; browser verifier; standalone JSONL package | 500 records + manifest; browser PASS; CI drift check | Ship corpus only |
| 5 | Nov 30-Dec 6 | **Delivered early:** P02 p99 latency; host-local 64-process idempotency; incremental Merkle root; threat model | p99 0.245 ms policy; 0.62 ms signed Merkle; 64-process replay 1 handler/1 receipt | Prepare npm release candidate; defer multi-host lock |
| 6 | Dec 7–13 | P06 CPU reference + parity harness; WGSL paged-decode draft | Parity harness green on CPU | Keep design note only |
| 7 | Dec 14–20 | P06 WGSL kernel; zero-readback trace; two-device benchmark | G3 for P06 | Ship CPU reference + negative result |
| 8 | Dec 21–27 | **Buffer / documentation debt**; portfolio site scaffold; no new flagship | Site builds; docs current | Rest — burnout is a risk |
| 9 | Dec 28–Jan 3 | P08 eager SAE + roofline baseline | Reconstruction `R²` measured | Delay P08 to week 10 |
| 10 | Jan 4–10 | P08 fused Triton Top-K SAE; achieved bandwidth | Kernel parity + speedup measured | Ship eager SAE only |
| 11 | Jan 11–17 | P08 steering eval; HF weights; report | G3 + G4 for P08 | Ship SAE weights without steering claim |
| 12 | Jan 18–24 | P03 mutation-adequacy gate; Lite-50 run | False-positive rate measured | Ship gate + 20-issue pilot |
| 13 | Jan 25–31 | P03 finish **or** P05 routing if P03 blocked; site case studies | G2 + G3 for chosen project | Finish site only |
| 14 | Feb 1–7 | Freeze, retro, applications, next-quarter plan | All public claims audited | — |

**Total flagship count:** five deep (P01, P02, P06, P08, P03), with P05 as a
conditional substitute. P04, P07, P09, and P10 are explicitly deferred; they
receive maintenance only.

---

## 5. Phase detail

### Weeks 1–3 — Project 01: HEROS-RLVR-Studio

**Outcome:** one public adapter trained with a deterministic verifier, plus a
reproducible four-arm ablation.

| Step | Owner | Deliverable | Done when |
|---|---|---|---|
| Resolve #101 | owner + agent | merge or review comments | branch merged or revised |
| `qlora_runner.py` | agent | 4-bit Qwen2.5-Coder-1.5B load, rollout loop, reward call | loads on CPU; unit tests mock the model |
| Shadow-worker pool | agent | process/thread pool around SQLite verifier | throughput test at 1/2/4 workers |
| 100-step smoke | owner | run log | loss finite; peak VRAM recorded |
| 500-step ablation | owner | 4 arms × 500 steps | same seed/data/eval; `run.json` per arm |
| MATH-500 eval | owner | pass@1 with 95% CI | 4 arms, same decoding params |
| HF adapter | owner | model card + adapter | card links repo, run log, limitations |
| W&B report | owner | public read-only report | reward/KL/length/clip curves |
| PR #2 (runner) | agent | code + tests + docs | 75+ tests in CI |

**Decision point (end of week 2):** if the 1.5B model cannot complete a 100-step
smoke under 5.4 GB peak on the RTX 2060, switch the local claim to 0.5B and run
1.5B on Kaggle only. Do not silently change the model in the results table.

**Kill criterion:** if no GPU run is possible by 2026-11-22, Project 01 ships as a
verified CPU library plus a runnable notebook, and the roadmap advances to P02.
The README must say "no training run" in the first paragraph.

### Weeks 4–5 — Project 02: HEROS-SafeAgent-OS

**Outcome:** a 500-case public adversarial corpus and Ed25519-signed sparse Merkle
inclusion proofs.

| Step | Deliverable | Done when |
|---|---|---|
| Corpus audit | map 289 existing cases to OWASP ASI01–ASI10 | coverage table has no empty category |
| New cases | +211 cases, deterministic seeds | 500 total, each with expected verdict |
| Package | JSONL corpus + manifest + CI drift check | 500 records, deterministic SHA-256 |
| Merkle | `packages/agentic/src/merkle.js` with domain-separated leaves | frontier root matches `merkleRoot` at every size; p99 0.62 ms signed append |
| Signatures | Ed25519 sign/verify via `node:crypto` | browser verify path works |
| Torture | 64-worker flock/WAL replay | host-local 64-process: 1 handler, 1 receipt; multi-host pending |
| Docs | threat model + npm README | limitations match tests |
| Release | npm package (approval required) | `0.3.0` dry-run inspected: 9 files, 22.3 kB, provenance workflow ready |

**Decision point:** if signature work exceeds week 5, ship the corpus and unsigned
proofs, and keep the npm package at release-candidate status.

### Weeks 6–7 — Project 06: EdgeInfer-WGSL-v3

**Outcome:** paged KV decode in a `GPUBuffer` with zero KV readback, or a
documented negative result.

| Step | Deliverable | Done when |
|---|---|---|
| CPU reference | paged attention with `block_size=16` | matches dense attention on 20 prompts |
| WGSL kernel | decode kernel + bindings | compiles in Chrome and Firefox |
| Parity | max abs error vs ORT | within tolerance on 20 prompts |
| Zero readback | trace of `mapAsync` calls | zero calls on KV buffers |
| Memory | analytic vs measured | within 5% |
| Benchmark | p50/p95 on two devices | device + driver recorded |
| Fallback | feature flag | dense path still works |

**Kill criterion:** if parity fails after three kernel iterations, publish the CPU
reference, the parity harness, and the negative result. Do not ship a shader that
does not attend.

### Week 8 — Buffer

No new flagship. Close documentation debt, run the portfolio site build, audit all
public claims, and take at least two days off. This week exists so weeks 9–14 do
not inherit a burnout debt.

### Weeks 9–11 — Project 08: Triton-SAE-Safety

**Outcome:** a fused Top-K SAE kernel with a measured speedup and an honest
safety-steering evaluation.

| Step | Deliverable | Done when |
|---|---|---|
| Eager SAE | PyTorch baseline on layer 14 | `R² > 0.92` on held-out activations |
| Roofline | achieved vs theoretical bandwidth | chart with hardware counters |
| Triton kernel | fused centering + encoder + Top-K | parity with eager within 1e-3 |
| Speedup | same batch/shape, warmup, 100 iters | median + IQR reported |
| Steering | CWE suppression eval | pass@1 regression reported |
| Artifact | safetensors + model card | weights load in a clean env |

**Kill criterion:** if the fused kernel is slower than eager after two tuning
rounds, publish the roofline analysis as the result. A negative kernel result is
still a kernel result.

### Weeks 12–13 — Project 03: Reflexion-SWE-Bench

**Outcome:** a mutation-adequacy gate that prevents self-generated tests from
grading themselves, evaluated on SWE-bench Lite-50.

| Step | Deliverable | Done when |
|---|---|---|
| Mutation gate | AST mutant generator + kill-rate threshold | ≥80% kill required before grading |
| Memory | persistent skill library | cross-task retrieval measured |
| Lite-50 | repair run | resolution rate + tokens/issue |
| Regression | MBPP false-positive rate | <2% |

**Conditional:** if Lite-50 infrastructure (Docker, images, time) is not ready by
week 12, run P05 instead: K≥4 router, INT8 ONNX, APGR/CPT-95 on RouterBench.

### Week 14 — Freeze

- Audit every public number against a log or artifact.
- Remove or qualify any claim that lost its evidence.
- Update the six pinned repos and the HF collection.
- Write the retro: what shipped, what slipped, what was killed.
- Draft the next-quarter plan; do not start it.

---

## 6. Weekly cadence

| Day | Action |
|---|---|
| Monday | Pick the week's single primary deliverable; write it at the top of `PROGRESS_LOG.md`. |
| Tuesday–Thursday | Code/test. One commit per logical change on a feature branch. |
| Friday | Run the full suite; record counts and runtime; update the PR packet. |
| Saturday | Owner GPU run or benchmark; capture `run.json` and W&B link. |
| Sunday | Append to `PROGRESS_LOG.md`; update `DECISIONS.md` if a decision changed; stop. |

**WIP limit:** one flagship in code, one in review, zero in "almost done".

---

## 7. Risk register

| Risk | Likelihood | Impact | Mitigation | Trigger |
|---|---|---|---|---|
| No GPU access in agent session | certain | high | owner runs; agent supplies scripts and checks logs | already true |
| RTX 2060 OOM at 1.5B | medium | high | 0.5B local, 1.5B Kaggle; 384 tokens before `G<4` | smoke test fails |
| Kaggle quota or timeout | medium | medium | checkpoint every 50 steps; resumable runs | session dies |
| HF token absent | certain until owner acts | medium | prepare card + files; owner uploads | upload step |
| Upstream drift in HEROS/HEROS-RL | medium | medium | rebase before push; small PRs | `git fetch` shows movement |
| TRL/Unsloth API change | medium | medium | pin versions; adapter layer | import error |
| Benchmark variance | high | medium | 3 seeds; report median + IQR; no single-run claim | first run |
| Scope creep (new project) | high | high | WIP limit; deferred list is explicit | new idea mid-week |
| Reviewer fatigue | medium | medium | PRs under 700 lines; one purpose each | PR > 1,000 lines |
| Windows path/ACL issues | medium | low | temp venv outside workspace; POSIX CI | local install fails |
| Claim drift in docs | medium | high | G7 audit at every gate and week 14 | number without log |

---

## 8. Approval gates

Nothing is pushed, published, or uploaded without an explicit "approve" from the
owner. The agent presents, for each PR:

1. The branch and commit hash.
2. `git show --stat`.
3. The full test command and result.
4. The patch file path.
5. Known limitations and rollback.

Approval is per action: merging #101 does not authorize an HF upload, and
approving an HF upload does not authorize an npm publish.

| Action | Needs approval | Artifact prepared |
|---|---|---|
| `git push` a feature branch | yes | patch + test log |
| Open a PR | yes | `PR_DESCRIPTION.md` |
| Merge a PR | yes | review response |
| npm publish | yes | `npm pack` output + provenance |
| HF model/dataset upload | yes | card + file list + checksum |
| Public deployment | yes | threat model + rollback |
| Upstream comment/PR | yes | draft text, no unsolicited pings |

---

## 9. Definition of done for the 14 weeks

The window succeeds if **three** of these are true:

- [ ] One adapter on HF with a run log and an honest card.
- [ ] One 500-case public corpus with signed receipts.
- [ ] One WGSL kernel with parity and zero-readback evidence.
- [ ] One Triton kernel with a measured speedup and roofline.
- [ ] One portfolio site with five case studies and no unsupported numbers.
- [ ] One upstream PR merged (TRL Dr.GRPO toggle is the smallest credible one).

It fails if any public claim is contradicted by its own artifact. Shipping four
projects honestly beats shipping ten with one inflated number.

---

## 10. Explicitly out of scope

- P04 UI compiler, P07 AST-GraphRAG, P09 PeerVault-PQC-AI, P10 Cloud Control as
  primary projects. Maintenance and documentation only.
- Paid infrastructure, always-on servers, and any "production SLA" language.
- arXiv main-track submission. A workshop draft is allowed after P01's run.
- Hiring claims that depend on unmeasured numbers.
- Rewriting existing repositories that are already honest (see ADR-009).

---

## 11. Change control

This roadmap changes only by appending a dated entry to `DECISIONS.md` with the
reason, the old plan, and the new plan. Silent reordering is not allowed. If a
week slips, record the slip in `PROGRESS_LOG.md` and adjust the next week, not the
gate.
