# Architectural Decision Log

Format: context → decision → consequences. Status is one of **Accepted**,
**Superseded**, or **Proposed**. ADRs are append-only; corrections supersede
rather than rewrite.

---

## ADR-001 — Repository disposition

**Status:** Accepted (archive actions require user approval)
**Date:** 2026-11-02

**Context.** Live inspection found 30 public repositories. The brief listed 11 and
proposed archiving `ContentForge-AI`, `EcoSphere`, and `x`. Those three names do
**not** appear on the live profile; the profile contains `FREED`, `colpali-edge`,
`certiflow-ai`, `PlotLLM`, `ridge_shade`, and other repos not in the brief. We
must not archive by a stale list.

**Decision.**

- Elevate: `HEROS`, `HEROS-RL`, `peervault`, `edgeinfer`, `Reflexion-SWE`,
  `RouteLLM-Gateway`, `GraphRAG-CodeAudit`, `Anthropic-PerfBench`.
- Merge `swarmcompute` into `peervault` **only if** that repository is confirmed
  to exist at execution time; it is not on the live profile today.
- Archive nothing automatically. Before archiving, capture the exact repo name,
  last commit, and a one-line reason in `PROGRESS_LOG.md`, then ask for approval.
- Synchronize documentation via PRs, never by force-pushing `main`.

**Consequences.** The audit is grounded in the live 30-repo estate. Any archive
is reversible for 90 days on GitHub and is gated on explicit approval.

---

## ADR-002 — Project 01 is the first execution target

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The largest hiring gap is empirical post-training: zero public model
weights, zero GPU run logs, and no MATH-500/GSM8K curves. The brief proposed
building a GPU trainer inside `HEROS/rlvr`. Live inspection found that
`HEROS-RL` already implements a critic-free GRPO engine, a 500-case dataset,
reward diagnostics, and TRL/Unsloth entry points.

**Decision.** Execute Project 01 as an **integration and evidence** project, not
a rewrite:

1. Add the deterministic SQLite shadow verifier and Dr.GRPO/DAPO loss to
   `HEROS/rlvr` (#101).
2. Reuse `HEROS-RL`'s reward stack and dataset instead of duplicating them.
3. Run the 500-step QLoRA ablation on the RTX 2060 / Kaggle T4 and publish the
   adapter plus a W&B report.
4. Only then add MATH-500/GSM8K evaluation.

**Consequences.** Avoids two competing GRPO implementations. The published
artifact must cite both repositories and pin the exact commit SHAs.

---

## ADR-003 — 6 GB VRAM training strategy

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The local GPU is an RTX 2060 (6 GB, Turing SM 7.5, no native bf16).
Full fine-tuning of a 1.5B model is impossible; even LoRA at 16-bit exceeds the
budget once activations and optimizer state are included.

**Decision.** Use 4-bit NF4 QLoRA (`r=16`, `alpha=32`, dropout 0.05), gradient
checkpointing, `paged_adamw_8bit`, micro-batch 1 with gradient accumulation, and
fp16 autocast. Dr.GRPO removes the value critic, so the policy + reference +
adapter + 4-bit base must fit under ~4.5 GB for `G=4` at 512 tokens. Burst to
Kaggle 2×T4 (32 GB total) for `G=8` on the 3B model. Checkpoint the adapter to
HF every 50 steps.

**Consequences.** If the local run OOMs, reduce `max_length` to 384 before
reducing the group size below 4; `G=1` has no learning signal. Never claim bf16
on Turing; use fp16.

---

## ADR-004 — Orchestration: direct APIs + MCP + stateful graphs

**Status:** Accepted
**Date:** 2026-11-02

**Context.** Legacy LangChain-style prompt chains hide state, retries, and tool
contracts. The portfolio already has MCP bridges, SQLite shadow gates, and
Merkle receipts.

**Decision.** Build agents as explicit state machines: direct model APIs, MCP
2025-11-25 tool contracts with `--describe`, a SQLite-WAL or LangGraph
checkpointed state graph, typed error codes, idempotency keys, and human approval
gates. LangChain may be used only as an adapter, never as the source of truth.

**Consequences.** More up-front schema work; far better debuggability and
replayability. Every agent project must ship a state-transition diagram.

---

## ADR-005 — Zero-cost, local-first persistence

**Status:** Accepted
**Date:** 2026-11-02

**Context.** Free-tier VMs are reclaimed or cut without notice. The brief notes
Oracle's June 2026 reduction of Always Free ARM to 2 OCPU / 12 GB and idle
reclamation. Any always-on server is a single point of failure for a portfolio
demo.

**Decision.** Default to browser OPFS/IndexedDB, SQLite WAL, and DuckDB. Use
static hosting (GitHub Pages, Cloudflare Pages) and stateless HF Spaces. Treat
Neon/Postgres as an optional commercial layer, not a demo dependency. Every demo
must work offline or from a pre-computed artifact.

**Consequences.** Some multi-user features (live collaboration, hosted approval
inbox) move to Project 10. Demo cold starts stay under 5 seconds.

---

## ADR-006 — Evidence-gated claims

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The supplied brief contains claims that are already stale
(`peervault` PQC disclaimer, `edgeinfer` tagline, 72.8% shell, 13 HF artifacts).
Publishing unverified numbers would damage credibility more than a smaller,
honest portfolio.

**Decision.** Every public claim is tagged in the workspace as **[V]** verified,
**[D]** documented, **[P]** planned, or **[X]** contradicted. Resume bullets and
README claims may use only **[V]** and **[D]** items, with the evidence link.
Audit scores remain planning estimates until the rubric evidence exists.

**Consequences.** Slower publishing, but no retractions. The first public model
card will say "adapter trained for 500 steps; no benchmark gain claimed" until
the evaluation is complete.

---

## ADR-007 — No fake kernels or placeholder benchmarks

**Status:** Accepted
**Date:** 2026-11-02

**Context.** Project 06 asks for WGSL paged-attention shaders and Project 08 for
Triton SAE kernels. A stub shader that compiles but does not attend would be
worse than no shader, because it creates a false claim.

**Decision.** For Project 06, ship a design note and a CPU reference first; the
WGSL kernel lands only with parity and zero-readback evidence (PR #3 does the
design-note step). For Project 08, ship the eager PyTorch SAE and a roofline
baseline before the fused Triton kernel. Benchmarks must include hardware,
driver/browser version, batch size, sequence length, and a correctness check.

**Consequences.** Project 06's headline metric moves later. The repository stays
honest, and the design note is still a useful hiring artifact.

---

## ADR-008 — Pull-request workflow and approval gate

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The brief requires PRs for every change and explicit approval before
pushing. `gh` is not installed in this environment, and no remote credentials
were used.

**Decision.** Work on a feature branch in a local clone; run the full test suite;
commit with a conventional message; export a `git format-patch` artifact to
`open_source/patches/`; write a PR description with problem, changes, test log,
and benchmark delta. **Never** push, open a PR, comment upstream, publish to
npm, or upload to HF without explicit approval. Upstream contributions follow the
same rule, with an additional "no unsolicited comments" rule.

**Consequences.** The user can review a complete patch offline. The local commit
hash is the resume point. If upstream moves, rebase before pushing.

---

## ADR-009 — Documentation corrections are scoped to observed contradictions

**Status:** Accepted
**Date:** 2026-11-02

**Context.** PR #2 was specified as "remove the false PQC/disclaimer text". Live
inspection showed the PQC text is already correct. The actual contradictions are
the FAQ's "no streaming-to-disk path" and the comparison table's "Resumable
transfers: No".

**Decision.** Fix only what is demonstrably wrong: the FAQ size answer, the
tab-closed answer, and the resume row. Add a one-paragraph note that resume is
manual. Do not rewrite the security architecture or inflate the claims.

**Consequences.** A small, reviewable PR. The README stays consistent with
`docs/pqc-validation.md` and the shipped `createOpfsSink()`.

---

## ADR-010 — The tensor layer delegates to the CPU reference

**Status:** Accepted
**Date:** 2026-11-02

**Context.** #101 added `gpu_trainer.py` with its own advantage centering,
zero-variance filter, and loss reduction. The package already had
`advantages.dr_grpo_advantages`, `sampling.has_learning_signal`, and
`losses.grpo_loss`. Three duplicate definitions would drift.

**Decision.** `DapoDynamicSampler` delegates to the existing advantage and
sampling functions. The tensor loss remains separate because `grpo_loss` is pure
Python and cannot backpropagate, but two parity tests pin it to the CPU
reference. The README explains that the CPU `none` reduction divides by `G`
(equal per-token weight, scale grows with tokens) while the tensor loss uses the
paper's constant horizon `G * L_max`.

**Consequences.** One definition for advantages and sampling; a documented,
tested scale difference for the loss. If the CPU reference changes, CI fails
until both paths agree.

---

## ADR-011 — Five flagships in 14 weeks, four deferred

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The scorecard ranks ten projects, but the owner has ~15 h/week and
one 6 GB GPU. Attempting ten shallow projects would produce ten demos and no
measured result.

**Decision.** Execute P01, P02, P06, P08, and P03 in that order; use P05 as the
week-13 substitute if P03's Docker infrastructure is not ready. Defer P04, P07,
P09, and P10 to maintenance and documentation. Insert a buffer week at week 8.

**Consequences.** The portfolio has five deep case studies instead of ten thin
ones. A project that misses its gate ships a smaller honest artifact or stops;
it does not get a fabricated number to keep the schedule.

---

## ADR-012 — QLoRA runner is protocol-first; the HF adapter stays thin

**Status:** Accepted
**Date:** 2026-11-02

**Context.** Project 01 P5 needs a runner that can sample a policy, score the
group with the deterministic verifier, apply the Dr.GRPO/DAPO loss, and write an
auditable run. The agent environment has CPU torch but no transformers, PEFT,
bitsandbytes, or GPU. A runner that could only be exercised by downloading a
1.5B model would be unverified code with an attractive name.

**Decision.** Split the runner into a tested protocol layer and a thin model
adapter. `QLoRARunner` depends only on `generate`, `token_logprobs`, and `save`.
The tests use a fake differentiable policy and the real SQLite verifier. The
schema bridge, prompt, tier validation, recorder, zero-variance skip, and
gradient-accumulation scaling are all tested on CPU. `HFPolicy` is a lazy
Transformers/PEFT/bitsandbytes adapter; it is explicitly marked untested and is
not part of the default CI gate.

The runner was opened as #102 against the #101 branch, then rebased and reopened
as #103 against `main` after #101 was squash-merged. The dataset bridge accepts the
five forge tiers (`SAFE`, `NOTABLE`, `MEDIUM`, `HIGH`, `CRITICAL`); the first
dry-run exposed an initial three-tier assumption and the full 500-row mapping is
now a required check.

**Consequences.** The orchestration can be reviewed and trusted before a GPU
exists. A real run still needs owner hardware, the `train` extra, and a 10-step
smoke before the 500-step ablation. No adapter, loss curve, or throughput number
may be claimed until then. If the HF adapter fails on GPU, the tested protocol
layer remains valid and the fix is localized.
