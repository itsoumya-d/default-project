# Next Actions

Owner: Soumya Debnath. Execution model: agent prepares; owner approves every
remote write (push, merge, publish, upload, deploy). Ranked by expected
portfolio value per unit of effort. Updated 2026-11-03 (Session 27).

Status legend: `[ ]` pending · `[~]` in progress · `[x]` done · `[!]` blocked on
owner.

## 0. Immediate (this session, no approval needed)

- [x] Verify edgeinfer PR #16 merged, CI 4/4 green; re-run reference tests
      (8/8 pass) and parity round-trip (20/20 pass).
- [x] Create `REPOSITORY_STRENGTH_INDEX.md` (was missing from the required
      document set).
- [x] Create this file (was missing from the required document set).
- [ ] Append Session 27 to `PROGRESS_LOG.md`; record ADR-023 in `DECISIONS.md`.
- [ ] Commit and push the workspace docs branch (agent-prepared, owner merges
      or fast-forwards as usual).

## 1. Blocked on owner approval / credentials (highest value once unblocked)

- [!] **Publish `@soumyadebnath1619/agentic@0.3.0`** (PR #118 is the release
      candidate; `npm pack` inspected: 9 files, 22.3 kB). Needs: explicit
      approval + npm OTP/token. Value: first public artifact gate (G4) for P02.
- [!] **Upload P01 SFT adapter + model card to Hugging Face**
      (`runs/2026-11-02-sft-warmstart/final/` + `MODEL_CARD.md`). Needs: HF
      token for `itssoumyad` + approval. Value: closes the 0-public-models gap;
      the single largest credibility gain available.
- [!] **Publish the 500-case corpus** (`packages/mcp/corpus/`, SHA-256
      `03f0608c…`) — either as an npm package or an HF dataset. Needs: approval
      of target + license check. Value: G4 for P02; citable artifact.
- [!] **Pin the six repositories** on the GitHub profile (HEROS, HEROS-RL,
      peervault, edgeinfer, Reflexion-SWE, HEROS-Firewall). Needs: approval
      (public presentation change). Value: presentation +2 across pinned set.
- [!] **Sync the HF collection description** ("Ten applied AI systems" →
      "Eleven Spaces + two datasets") and the `itsoumya-d` profile README with
      verified achievements. Needs: approval. Value: discoverability.
- [!] **npm/HF/GitHub release for edgeinfer** — not until the WGSL gates pass.

## 2. Next engineering work (not blocked; in roadmap order, pull forward as capacity allows)

- [ ] **P06 — WGSL paged-attention kernel** (Weeks 6–7, pull forward; CPU
      reference + harness DONE in #16). Steps:
      1. Draft `src/webgpu/kernels/paged_attention.wgsl` (MHA, f16, block=16,
         online softmax, zero readback of KV during decode).
      2. Host-side block table + pipeline setup behind a feature flag with
         `WEBGPU_UNAVAILABLE` fallback.
      3. Browser parity run vs the CPU reference on the 20 synthetic cases
         (atol 2e-3 / rtol 2e-2), then SmolLM2-135M-Instruct greedy decode for
         32 tokens × ≥20 prompts vs ORT baseline.
      4. Zero-readback trace via WebGPU validation layer; memory within 5% of
         the analytic bound; p50/p95 on two devices with browser/driver
         versions recorded.
      5. No speedup claim until step 4 passes. Kill criterion: two tuning
         rounds without beating eager → publish roofline analysis instead.
- [ ] **peervault — committed benchmark log**: script + run for handshake
      p50/p95 and 1 GB stream RSS on the owner's machine; update README with
      the log link. Small; closes the largest [D] gap in the highest-scored repo.
- [ ] **P05 — RouteLLM RouterBench calibration** (Week 13 fallback or pull
      forward): K>4 router, ONNX export, measured RouterBench numbers.
- [ ] **P08 — Triton Top-K SAE** (Weeks 9–11): eager baseline + roofline first;
      fused kernel only after eager is measured.
- [ ] **P03 — Reflexion-SWE mutation-adequacy gate** (Week 12): ≥80% mutant
      kill rate before grading; Lite-50 only if Docker infra is ready.
- [ ] **P01 — optional RL follow-ups**: do NOT run another long RL job; the
      corrected-reward pilot (0.13) and zero-variance probes are recorded.
      Next useful step is a harder task distribution, not more steps.

## 3. Documentation / workspace hygiene

- [ ] `DECISIONS.md`: add ADR-023 (P06 #16 verification; Mobbin MCP absent;
      RSI/NEXT_ACTIONS created).
- [ ] `PROGRESS_LOG.md`: Session 27 entry with exact commands and results.
- [ ] Fix the encoding artifacts (`�`) in `MASTER_ROADMAP.md` /
      `PORTFOLIO_AUDIT.md` when next edited; no content change otherwise.
- [ ] `HEROS-Firewall` and `HEROS-Cloud-SaaS`: add a "superseded by / see
      HEROS" banner to READMEs (small PR each, owner merges).
- [ ] Two unlabelled repos (`Yc_ai`, `factory-monitor`): ask owner for a
      one-line description or archive approval — do not guess.

## 4. Verification checkpoints before any "done" claim

1. Clean checkout runs (G1) — one documented command.
2. Full test suite green with counts + runtime (G2).
3. Benchmark on real hardware with versions/seeds/baseline (G3).
4. Artifact exists and is inspectable (G4).
5. Limitations match the code (G5).
6. PR reconstructable by a reviewer (G6).
7. Every public number tagged `[V]` / `[D]` / `[P]` / `[X]` (G7).

## 5. Explicitly not next

- No new flagship projects (WIP limit: one in code, one in review).
- No publishing, uploading, deploying, merging, or pinning without approval.
- No RL 500-step rerun; no four-arm ablation claim.
- No archiving of any repository without explicit owner approval.
- No work in `mercor-odin-task-nk3pabc4/` (unrelated to this program; leave
  untouched).
