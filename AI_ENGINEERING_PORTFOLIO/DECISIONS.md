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

## D-2026-11-09-001 — Keep Dr.GRPO+DAPO, fix reward content before scaling RL steps

**Status:** Accepted
**Date:** 2026-11-09

**Context.** P01's 100-step RL-from-base run already used Dr.GRPO centered
advantages + DAPO asymmetric clipping (0.28/0.20) + k3 KL 0.01, and still
failed: held-out ok_rate 0.20 (same as base), risk_accuracy 0.10. The
literature review (`research/literature_reviews/length-difficulty-bias-rlvr.md`)
shows the estimator corrections are necessary but not sufficient; the failure
histogram (REQUIREMENT_MISS 33/50, SQL_EXEC_ERROR 7/50) proves reward content,
not the estimator, is the binding constraint.

**Decision.** Continue Dr.GRPO + DAPO + k3 KL. Freeze step-count scaling until
a risk-calibration-weighted + requirement-weighted reward rerun (>250 steps,
held-out 50 unchanged) beats base on risk_accuracy (gate: >0.20). Do not adopt
U-statistic/learnable-length advantage variants until that gate is met.

**Consequences.** The next GPU job is a reward-shaping rerun, not more steps of
the current reward. The `rlvr-bias-probe` CPU experiment (this session)
verifies the estimator half of the claim (length-bias removal) independently of
the reward-content half.

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
as #103 against `main` after #101 was squash-merged; #103 merged at `d3588ca`. The dataset bridge accepts the
five forge tiers (`SAFE`, `NOTABLE`, `MEDIUM`, `HIGH`, `CRITICAL`); the first
dry-run exposed an initial three-tier assumption and the full 500-row mapping is
now a required check.

**Consequences.** The orchestration can be reviewed and trusted before a GPU
exists. A real run still needs owner hardware, the `train` extra, and a 10-step
smoke before the 500-step ablation. No adapter, loss curve, or throughput number
may be claimed until then. If the HF adapter fails on GPU, the tested protocol
layer remains valid and the fix is localized.

---

## ADR-013 - Execution reward requires target-schema satisfaction

**Status:** Accepted
**Date:** 2026-11-02

**Context.** The 500-step adapter raised held-out mean reward from 0.71 to 1.465
while risk accuracy fell from 0.16 to 0.02. It had learned to emit a safe
`ALTER TABLE ... ADD COLUMN note` for every task, including `drop_column` and
`drop_table` tasks. The verifier awarded `+0.75` for "SQL executed" without
checking whether the requested change happened.

**Decision.** When a `MigrationTask` supplies `target_schema`, compare the final
SQLite schema to it after the migration:

- table set;
- column names;
- SQLite type affinity;
- `NOT NULL` (including primary-key implication);
- primary-key flags.

A matching schema earns `+0.75`. A valid migration that does not match gets
`-0.75` and `REQUIREMENT_MISS`. Tasks without a target schema keep the old
behavior for backward compatibility; every row in the 500-case dataset supplies
one.

**Consequences.** The old 500-step adapter is invalid under the corrected reward
and must not be presented as a migration model. New training runs will be harder
and may expose that 1.5B cannot satisfy many target schemas. That is the correct
failure: the previous reward measured format compliance, not migration skill.
The new gate is schema-level, not data-content-level; row hashing and PostgreSQL
parity remain future work.

---

## ADR-014 - Measure policy latency separately from Merkle append cost

**Status:** Accepted
**Date:** 2026-11-03

**Context.** The first p99 benchmark wrapped the receipt store in
`createMerkleReceiptStore` and measured 33.8 ms p99 at 5000 samples. That number
looks like a policy-gate failure, but the wrapper recomputes the Merkle root over
every leaf on each append, so the benchmark was measuring O(n) log maintenance,
not validation or authorization.

**Decision.** `npm run bench:policy` measures the in-process policy path with the
O(1) memory receipt store: schema validation, authorization, handler execution,
and receipt append. The signed Merkle wrapper is excluded and its cost is
reported separately. The threshold remains p99 <4.5 ms for the policy path.

**Consequences.** The policy path passes at **0.245 ms p99** over 5000 samples.
The 33.8 ms Merkle figure is retained as a known scalability limit, not hidden.
An incremental Merkle tree is required before the signed log can be claimed as
high-throughput; until then, benchmark claims must name which path they cover.

---

## ADR-015 - Scope the idempotency lock to one process

**Status:** Superseded by ADR-016
**Date:** 2026-11-03

**Context.** `AgenticApp.execute` checked the receipt store for an idempotency
key and then ran the handler. Two concurrent callers could both observe "no
receipt", both execute, and both append. PR #114 adds an in-flight promise map
so only the leader executes and followers replay the recorded response.

**Decision.** Ship the in-process lock now and test 64 concurrent calls: one
handler invocation, one receipt, 63 `_idempotent: true` responses. Do not claim
cross-process idempotency from this test. The file store's flock/WAL behavior and
a 64-worker cross-process torture test remain a separate deliverable.

**Consequences.** The P02 gate's 64-way idempotency item is satisfied at the
in-process level only. A multi-worker deployment still depends on the receipt
store's locking and on a future cross-process test.

---

## ADR-016 - Host-local cross-process idempotency locks

**Status:** Accepted
**Date:** 2026-11-03

**Context.** ADR-015 shipped an in-process promise map and explicitly did not
claim cross-process idempotency. The P02 gate asks for 64 parallel replays.
The file store also rewrote its whole JSON state from a per-process queue, so
two processes could lose each other's receipts.

**Decision.** Add a cooperative lock-file layer to `packages/agentic`:

- `withFileLock` acquires an exclusive lock with `open(path, "wx")`, retries
  with jitter for up to 30 s, and removes locks older than 120 s.
- File receipt and approval stores hold a global `<path>.lock` around every
  read-modify-write.
- The receipt store exposes `withIdempotencyLock(key, fn)` using a lock file
  named from the SHA-256 of the key. `AgenticApp` holds it across
  check-execute-record, so a follower re-checks and replays.
- The Merkle wrapper delegates the key lock to its backing store.

PR #115 adds a 64-process test: one handler execution, one receipt, one
idempotency record, 63 `_idempotent: true` responses. It passed 8/8 local stress
runs after transient Windows `EPERM`/`EACCES` retries were added.

**Consequences.** The gate's 64-way idempotency item is met **on one host**.
This is still not a distributed lock: NFS/SMB, multi-host writers, and handlers
longer than 120 s are out of scope. The threat model records these residual
risks, including the crash window between receipt append and idempotency record.

---

## ADR-017 - Maintain an incremental Merkle frontier

**Status:** Accepted
**Date:** 2026-11-03

**Context.** ADR-014 kept the policy benchmark separate from the Merkle wrapper
because the wrapper recomputed the root over every leaf on each append. That
was honest but left a real scalability limit: p99 33.8 ms at 5000 receipts.

**Decision.** Keep a Merkle frontier (one perfect-subtree root per level) inside
`createMerkleReceiptStore`. Appending a leaf carries it upward, and the root is
the fold of the remaining peaks from low to high. This is the same root as
`merkleRoot()`, including odd-node promotion, but costs O(log n) instead of
O(n). Appends are serialized through a promise chain so concurrent calls cannot
reuse a frontier.

Tests assert parity at all 96 sizes, after reload, and under 32 concurrent
appends. `npm run bench:merkle` measured p99 **0.62 ms** at 5200 signed receipts
with an in-memory store.

**Consequences.** Root updates are no longer the bottleneck. The file store
still rewrites its whole JSON file, `verify()` still recomputes every leaf, and
inclusion proofs are still O(n) to generate. Those limits stay in the threat
model; no persistent or distributed incremental tree is claimed.

---

## ADR-018 - Generate the public corpus from the executable tests

**Status:** Accepted
**Date:** 2026-11-03

**Context.** The P02 corpus existed only as test code. Hand-writing 500 JSON
records would duplicate the cases and drift from the assertions. A static
snapshot with no link to the tests would be hard to trust.

**Decision.** Record cases from inside the existing test loops. When
`HEROS_CORPUS_DIR` is set, `recorder.mjs` writes one JSONL file per worker; the
normal test run leaves it as a no-op. `build.mjs` runs the two suites, validates
13 group counts and 500 unique IDs, sorts the records, and writes
`corpus.jsonl` plus `manifest.json` with a SHA-256. `npm run corpus:check`
rebuilds and compares the committed files, and a dedicated CI job enforces it.

Approval nonces are random in the live harness, so the dataset records
`{"$runtime":"approval_nonce"}` with a `setup` object instead of pretending the
token is fixed. Other JSON-lossy values use `$undefined` and `$number` markers.

**Consequences.** The dataset is deterministic (same SHA-256 across rebuilds) and
the tests remain authoritative. It captures inputs and expected verdicts, not
observed responses; approval cases are scenarios that need the documented
setup. Publishing to Hugging Face or npm still requires separate owner approval.

---

## ADR-019 - Release agentic 0.3.0 with the threat model in the tarball

**Status:** Accepted
**Date:** 2026-11-03

**Context.** `@soumyadebnath1619/agentic@0.2.0` is already published, but the
repository has since added Ed25519 signing, cross-process idempotency locks,
the incremental Merkle root, and a threat model. Publishing the current tree as
0.2.0 would fail, and the 0.2.0 tarball did not include the new security
documentation.

**Decision.** Bump to **0.3.0**, add `THREAT_MODEL.md` and `CHANGELOG.md` to the
package `files` list, and inspect `npm pack --dry-run`. Do not create a tag or
publish. The existing `agentic-v*` workflow remains the only publish path and
requires owner approval.

**Consequences.** The release candidate is 9 files, 22.3 kB packed (82.9 kB
unpacked), with shasum `e36f6e8233ef9d0aa340e4a289cca1b1a50ca509`. The version is
still unpublished; a tag would trigger provenance publishing. P02 remains
"complete locally, publish pending" until the owner approves.


---

## ADR-020 - Do not force a 500-step RL-from-SFT run after zero-variance probes

**Status:** Accepted
**Date:** 2026-11-03

**Context.** PR #119 added `RunnerConfig.adapter_path`, so the RL runner can
start from the SFT adapter. Three GPU probes were run on the first 10 training
tasks: 2 steps at temperature 1.0/group 2, 10 steps at 1.2/group 4, and 10 steps
at 1.5/group 4. Every group was skipped with `zero_variance_group`. The SFT
policy scored 2.0 on nine tasks and a constant 1.0 on the type_narrowing task.
Sampling was not frozen: temperature 1.5 produced 4/8 unique completions and
2.0 produced 8/8, but the deterministic reward did not separate them.

**Decision.** Do not run a 500-step RL-from-SFT job that would be almost
entirely no-ops. Record the probe as a negative result in
`projects/project-01-heros-rlvr-studio/RL_FROM_SFT.md`. Keep the SFT adapter as
the accepted P01 result. The next RL experiment starts from the base model with
the corrected requirement-check reward, where the base's low held-out score
should create variance.

**Consequences.** No RL-from-SFT adapter exists and no improvement is claimed.
The four-arm ablation remains incomplete. GPU time is redirected to the
base-model RL arm and, if needed, a harder task distribution. The negative
result is itself evidence: a deterministic, coarse verifier can saturate after
SFT and remove the learning signal.


---

## ADR-021 - Treat the 100-step RL-from-base pilot as weak, not a win

**Status:** Accepted
**Date:** 2026-11-03

**Context.** The RL-from-SFT path had no learning signal (ADR-020). A 100-step
RL-from-base run with the corrected reward was then executed on the first 450
rows: 91/100 groups completed, training mean reward improved from -0.656 (first
10) to -0.044 (last 10). Held-out greedy evaluation on rows 451-500 gave mean
reward 0.13 for the final adapter and 0.165 for checkpoint-50, versus base 0.02
and SFT 1.90. Risk accuracy was 0.10-0.20 versus 0.20 base and 0.90 SFT;
REQUIREMENT_MISS rose to 32-33/50 versus 23 base.

**Decision.** Report the run as a weak positive over base but not as an RL gain
over SFT, and do not publish the RL adapter. Keep the SFT adapter as the accepted
P01 result. Do not run a 500-step version unless a specific question justifies
the compute; a longer run without a reward or task redesign is unlikely to close
a 1.77-point reward gap.

**Consequences.** P01 has a real SFT result, two documented RL negatives/weak
results, and no four-arm ablation. The honest headline is that SFT dominates
this deterministic-reward setup; RL needs a harder task distribution or finer
partial credit before it can be claimed as an improvement.


---

## ADR-022 - Keep the Bash bridges but make their coverage explicit

**Status:** Accepted
**Date:** 2026-11-03

**Context.** P02 listed 11 shell scripts (about 3,175 lines) as a maintenance
risk. Two scripts were not in the CI shellcheck list, and there was no written
policy for when a bridge should be ported or deleted.

**Decision.** Keep the Bash bridges for Linux/WSL while Zero lacks stdin, but:

- run `shellcheck -S warning` on all 11 scripts in CI;
- document the inventory, controls, known gaps, change policy, and migration
  order in `docs/shell-maintenance.md`;
- state that the Node MCP package is the cross-platform path and the Bash
  bridges are not macOS/native-Windows targets.

**Consequences.** All 11 scripts are syntax/lint-covered and the duplication,
encoding, and Bash-level test gaps are explicit. No bridge logic changed. P02's
only remaining item is the npm publication, which needs owner approval.


---

## ADR-023 - Build the paged-attention CPU reference before any WGSL

**Status:** Accepted
**Date:** 2026-11-03

**Context.** EdgeInfer cannot pin `past_key_values` in a `GPUBuffer` behind
`onnxruntime-web`; the design note requires owning the attention computation.
A WGSL kernel without a reference would be unverifiable and would invite a
speedup claim without evidence.

**Decision.** Implement a Python float32 reference for the documented cache
layout (`KV[block_id][slot][kv_head][head_dim]`, `block_size=16`) with online
softmax and a logical-to-physical block table. Add a parity harness that
compares a candidate output with `atol=2e-3`, `rtol=2e-2`, and a unittest suite
covering block boundaries, table permutation, and out-of-range slots. MHA only;
GQA is a follow-up.

PR #16 adds the reference, harness, 8 passing tests, and a dedicated CI job. It
does **not** add WGSL, model-level parity, a zero-readback trace, or a
benchmark.

**Consequences.** The next WGSL PR can be rejected by the harness. The P06 gate
remains open: parity on 20 prompts, 0 KV `mapAsync`, memory within 5%, and
two-device latency. JavaScript dependencies are installed only in CI; the local
Node suite was not used as evidence for this change.


---

## ADR-024 - Record P06 #16 verification; Mobbin MCP and UI Skills are absent here

**Status:** Accepted
**Date:** 2026-11-03

**Context.** PR #16 (`0d17672`, merged; CI 4/4) added the paged-attention CPU
reference, parity harness, and 8 tests, with ADR-023 recording the decision.
However `PROGRESS_LOG.md` had no entry for it and two required documents were
missing: `REPOSITORY_STRENGTH_INDEX.md` and `NEXT_ACTIONS.md`. Separately, the
mission brief asks for the Mobbin MCP and UI Skills to be discovered and used.

**Decision.**

1. Verify, do not re-implement: re-ran `python -m unittest test_paged_attention`
   (8/8 pass, 0.102 s) and a harness round-trip (generate 20 synthetic cases ->
   reference-as-candidate -> `check` returns `ok: true`, 20/20 compared, 0
   failures). These verify the harness end-to-end; they are **not** a WGSL,
   SmolLM2, or speedup claim.
2. Create the two missing documents. `REPOSITORY_STRENGTH_INDEX.md` scores all
   30 public repositories on the brief's eight-category rubric; the eleven
   elevated repositories carry evidence-based scores, the remaining nineteen
   are marked `[P]` estimates and must not be quoted as measurements.
   `NEXT_ACTIONS.md` ranks the next work and lists the owner-approval blockers.
3. Mobbin MCP: **not installed** in this environment (no `mobbin` tools in the
   tool catalogue; `list_mcp_resources` returns empty). No UI Skill exists
   either (available skills: browser, kimi-webbridge, opencode, report).
   Therefore Mobbin-based pattern research cannot be performed here; any UI
   work must either use the owner's Mobbin access in a later session or proceed
   from first principles with the `browser` skill for reference reading.
   `Mobbin-UI-Compiler` remains fixture-only; do not invest until that changes.
4. The Kimi WebBridge daemon had exited uncleanly; it was restarted on
   127.0.0.1:10086 (v2.0.26; v2.0.32 available, upgrade is user-initiated).
   GitHub PR #16 was verified live in the authenticated session: merged,
   "4 / 4 checks OK".

**Consequences.** The required document set is now complete (14/14). The P06
gate is still open and is the next engineering task: WGSL kernel, browser
parity on 20 prompts, zero-readback trace, memory within 5%, two-device p50/p95.
No claim may exceed that evidence. The absence of Mobbin MCP is recorded so
future sessions do not assume it exists.

---

## ADR-024 - Ship an f32 correctness kernel before the f16 paged cache

**Status:** Accepted
**Date:** 2026-11-03

**Context.** The design note targets an f16 KV cache, but the first WGSL kernel
had to be inspectable and comparable to the Python float32 reference. Implementing
f16 storage and conversion before proving the addressing and online-softmax
recurrence would mix two failure modes.

**Decision.** Ship the first kernel with f32 storage, the same
`KV[block][slot][kv_head][head_dim]` layout, online softmax, GQA head mapping,
and a host-side status reset. Validate it in a real browser against the 20-case
synthetic fixture from the Python reference. Defer f16 storage and the memory
gate to the next iteration.

The browser run passed **20/20** cases with max absolute error **8.43e-8** on
Chrome 156 / NVIDIA Turing (RTX 2060), including MHA and GQA cases. The runtime
capability check found no KV-sized buffer created with `COPY_SRC` or `MAP_READ`
across 40 KV buffer creations; this is not a validation-layer `mapAsync` trace.

**Consequences.** Addressing, GQA, block-table traversal, and online softmax are
now covered by a real GPU test. The kernel is not wired into
`EdgeInfer.generate()` and does not meet the memory gate; f16 storage, ORT
prompt/logit parity, a validation-layer trace, two-device timing, Firefox, and
a fallback flag remain open.


---

## ADR-025 - Move the WGSL cache to f16 with f32 accumulation

**Status:** Accepted
**Date:** 2026-11-03

**Context.** The first WGSL kernel used f32 KV storage to isolate addressing and
online-softmax bugs. The design target is f16 storage, and the memory gate cannot
be evaluated with f32.

**Decision.** Convert the KV storage buffers to `array<f16>` and keep f32
accumulation. The host converts `Float32Array` inputs to IEEE-754 half bits and
requires the `shader-f16` device feature, raising `WEBGPU_UNAVAILABLE` when it is
missing. The 20-case fixture is generated from the same f16-rounded K/V values
as the Python reference.

**Consequences.** The kernel now matches the intended storage format. Chrome 156
on the RTX 2060 passes **20/20** synthetic cases with max abs **4.79e-8** and
still reports **40/40** KV buffer creations without `COPY_SRC`/`MAP_READ`.
Peak-memory accounting, validation-layer trace, ORT token parity, two-device
benchmark, Firefox, and a fallback flag remain open.

