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
- [x] **Session 33:** adopt the `AGENTS.md` spec; create
      `APPLIED_JOBS_AND_VISA_LEDGER.md` (Air New Zealand Rule firewall +
      pre-flight procedure); record the Gmail/websearch/pandoc/revo
      tooling gaps in `PROGRESS_LOG.md` Session 33. HEROS `rlvr` re-verified
      locally (82 pass + 13 skip, no torch). Live public count is now **63**
      (see §3).
- [x] **Session 34:** correct the count to 63 in README/RSI; deep-dive
      `llm-control-plane` (54 → 61 tests, 95% coverage, ruff clean, RSI 75
      §2b); prepare `feat/metrics-label-escaping` commit `8d958c7`
      (Prometheus label escaping + name validation, 7 new tests). **Local
      only — not pushed.**
- [!] **Review/push `llm-control-plane` `8d958c7`** (owner approval): push
      the branch and open a PR if the fix is accepted.
- [x] **Session 35:** deep-dive `autopilot-fde` (436 passed + 1 skipped, 154
      subtests, 100% backend coverage, ruff clean, RSI 84 §2b). Prepared
      `fix/windows-portability` `bccb8c3` (2 Windows failures fixed) and
      `fix/paper-synthetic-claims` `265c25e` (paper claimed "empirical
      evaluation across 8 enterprise departments and 158 traces" on fixture
      data; now scoped to a synthetic benchmark). **Local only.**
- [!] **Review/push `autopilot-fde` `bccb8c3` and `265c25e`** (owner
      approval): the paper correction is the higher-priority of the two
      because the uncorrected claims conflict with ADR-006 and the README.
- [x] **Session 36:** verify `RouteLLM-Gateway` end-to-end on Windows
      (16/16 then 19/19 tests; benchmark table reproduced exactly); prepare
      `feat/reproducible-pareto` `d86f178` (canonical float rounding so
      `results/pareto.json` is byte-stable; 3 tests); RSI 62 [D] → 66
      [V]/[D]. Also corrected the elevated average: the table summed to
      64.6, not 61.8; now 65.0. **Local only.**
- [!] **Review/push `RouteLLM-Gateway` `d86f178`** (owner approval).
- [x] **Session 37:** verify `GraphRAG-CodeAudit` on Windows (22/22 tests after
      installing tree-sitter parsers, benchmark table reproduced exactly:
      GraphRAG 7.58 vs flat 7.07, 64/100 wins); prepare
      `fix/reproducible-eval-label` `c9b51e7` (artifact records
      `data/sample_repo` instead of an absolute macOS path; 2 tests; 24/24
      pass); RSI 59 [D] → 63 [V]/[D]; elevated average now 65.4. **Local
      only.**
- [!] **Review/push `GraphRAG-CodeAudit` `c9b51e7`** (owner approval).
- [x] **Session 38:** verify `Reflexion-SWE` (37 passed + 3 skipped; ablation
      table reproduced exactly; artifact already byte-stable — no fix needed)
      and `HEROS-Firewall` (16/16 tests; red-team FNR 0/1000, FPR 0/200, p99
      0.230 ms). Prepared `docs/windows-redteam-run` `e0e8579` (raw Windows
      output + RESULTS section). RSI: Reflexion 61→64, Firewall 70→72,
      elevated average 65.8. **Local only.**
- [!] **Review/push `HEROS-Firewall` `e0e8579`** (owner approval).
- [x] **Session 39:** verify `HEROS-Cloud-SaaS` (6/6 tests; PLLB table
      reproduced exactly) and `Mobbin-UI-Compiler` (10/10 tests; regenerated
      artifacts byte-identical). Prepared `docs/windows-eval-run` `0096a7d`
      (raw Windows eval + RESULTS section). `Anthropic-PerfBench` could not be
      run: no C compiler/make/cargo on this host — score unchanged at 56 [D].
      RSI: Cloud-SaaS 47→50, Mobbin 45→48, elevated average 66.4. **Local
      only.**
- [!] **Review/push `HEROS-Cloud-SaaS` `0096a7d`** (owner approval).
- [!] **Decide on edgeinfer #22** (open, merge-ready, `adb3cb9`): owner merges
      or closes; no agent action.
- [x] **Session 40:** live reconcile — HF has **11 Spaces / 2 datasets /
      0 models** (matches); **peervault #15 merged** (`e22fb7f`, 6/6 green),
      **edgeinfer #23 merged** (`89881a9`), **RouteLLM #1 merged** (`92083c8`);
      **edgeinfer #22 still open**. README/NEXT_ACTIONS/RSI updated; peervault
      RSI 83→84, elevated average 66.5.
- [x] **Session 41:** re-verified prepared branches (all 7 clean, including
      `autopilot-fde` `265c25e` paper-scope fix on a separate branch from
      `bccb8c3`); edgeinfer #22 still open (434 open PRs total are mostly
      `Yc_ai` bot noise — only #22 is relevant to this program); HEROS
      `npm test` re-run 54/54 pass. HEROS-RL not re-run (no pytest in available
      env); PerfBench still blocked by missing C/Rust toolchains. Stage 1
      remains blocked on Gmail access/export.
- [ ] **Verify apparent `�` characters at byte level before editing any
      workspace doc** — the autopilot-fde README proved they are a Windows
      console artifact, not corruption.
- [ ] **Stage 1 blocked:** Gmail MCP is absent (no Gmail tools, empty MCP
      catalogue). Owner to connect Gmail MCP or paste an export of past
      applications so the ledger can be populated and deduped. After that,
      source Global Remote AI/ML roles against the $65k floor (salary matrix
      at the top of `AGENTS.md`).
- [ ] Commit the workspace docs branch along with the Session 30–32 edits
      (agent-prepared, owner merges or fast-forwards as usual).

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
- [x] **peervault — committed benchmark log**: PR #15 (`bc12ede`) merged
      2026-11-04 at 12:25 UTC (`e22fb7f`, 6/6 checks green). Windows 11
      handshake p50 2.221 / p95 2.668 ms and 1 GB stream RSS committed as
      `sdk/bench-pqc.local.json` + `sdk/bench-memory.local.json`; README link
      updated. RSI 83 → 84.
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
- [ ] **Fix stale public-repo counts:** `README.md` fact table still says 30
      (2026-11-02 audit) and `REPOSITORY_STRENGTH_INDEX.md §1` says 61
      (Session 30). Live GitHub API on 2026-11-04 reports **63 public
      repositories**. Update both to 63 with the API evidence, or re-confirm
      with an authenticated session before editing — do not touch without
      that evidence.
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
