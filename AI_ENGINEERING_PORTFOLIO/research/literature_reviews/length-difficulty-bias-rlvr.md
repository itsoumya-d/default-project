# Literature review — Length and difficulty bias in verifiable RL (GRPO, Dr.GRPO, DAPO, U-statistic critiques)

**Status:** complete synthesis with design decision (see `DECISIONS.md` D-2026-11-09-001).
**Sources:** GRPO (DeepSeek-R1 lineage), Dr. GRPO (Liu et al.), DAPO (ByteDance Seed,
Yu et al.), "Unifying the GRPO Frameworks with Learnable Token-Level Length" (arXiv 2510.06870),
HF agentic-RL-2026 post, OpenTrain GRPO post-training guide, Interconnects GRPO-tweaks roundup,
Kili "GRPO Explained", XLANG/various "From REINFORCE to Dr. GRPO" survey notes.

## Design question

Should the portfolio's verifiable-reward training (P01 HEROS-RLVR studio) use the
standard GRPO advantage estimator, or an estimator corrected for length and
difficulty bias — and with what clipping/KL settings?

## 1. Standard GRPO and where its bias lives

For a prompt `q`, sample a group of `G` completions `{o_i}` with rewards `r_i`.
The GRPO advantage:

```
A_i = (r_i − mean(r)) / std(r)      # applied uniformly to every token of o_i
```

Two documented biases follow from this definition:

1. **Length bias.** The same scalar advantage is broadcast to every token of a
   response. A long incorrect completion dilutes its own per-token signal;
   updates across different lengths are not commensurable. The HF 2026 agentic-RL
   post gives the empirical version: "its reward directly paid for length; the run
   grew long for a simpler reason." The P01 run shows the shadow of this failure:
   completions improved in shape/reward while *risk accuracy stayed at 0.10* —
   the token-broadcast advantage rewards "more plausible text" without teaching
   response-level decisions (risk tier, data-loss flag).
2. **Difficulty bias.** Dividing by `std(r)` amplifies easy-group residuals and
   shrinks hard-group ones. When the whole group fails (all `r_i ≈ 0`, P01's
   REQUIREMENT_MISS regime) or all succeed, advantages collapse or explode
   independent of learning value, and groups that teach the most (mixed
   success) get systematically *lower* weight than easy groups whose variance
   is mostly stylistic.

## 2. The corrections

- **Dr. GRPO** — removes both bias terms: no `std(r)` division, and a
  token-level loss normalized by a constant (sequence-matched) instead of by
  per-response length. Advantages become mean-centered only; the optimizer can
  no longer harvest reward from length or from low-variance easy groups.
- **DAPO** — asymmetric clipping (`clip_eps_high > clip_eps_low`, e.g. 0.28/0.20
  in P01's config) to fight entropy collapse, plus decoupled clipping so
  exploration increases where the group is uncertain.
- **U-statistic / learnable-length variants (arXiv 2510.06870)** — replace the
  uniform broadcast with a learned, token-aware advantage; principled but adds
  hyperparameter surface and wants a bigger N to distinguish from noise.
- **k3 KL estimator** — keep a small KL anchor to the SFT/reference policy
  (P01: `kl_beta=0.01`) to keep reward chasing from drifting into invalid SQL.

## 3. What the evidence says for *this* portfolio

- P01's run (`runs/2026-11-03-rl-base-100-corrected`, Qwen2.5-Coder-1.5B, LoRA
  r16, RTX 2060) used Dr.GRPO+DAPO *already* (manifest config: `clip_eps_high
  0.28`, `clip_eps_low 0.2`, `kl_beta 0.01`, group 4, temp 1.0). Result:
  ok_rate 0.20 → 0.20 vs base; mean reward 0.02 → 0.13 after checkpoint-50 eval.
  So the estimator was not the binding constraint — **reward content was**.
- The failure histogram proves it: REQUIREMENT_MISS 33/50, SQL_EXEC_ERROR 7/50,
  risk_accuracy 0.10. No advantage estimator fixes a reward that under-pays
  correct risk calibration and requirement satisfaction.
- Conclusion: keep Dr.GRPO+DAPO (cheap, correct), but stop scaling steps until
  the reward pays for the failure modes. Length/difficulty corrections are
  *necessary, not sufficient*.

## 4. Reproduction task (tied to a portfolio project)

- **Task (runnable now, CPU):** implement the estimator comparison as a
  simulated-policy experiment — `rlvr-bias-probe` (this session): a synthetic
  environment where completion length correlates with reward for spurious
  reasons; run GRPO vs Dr.GRPO advantage estimators for N=200 groups × G=8,
  fixed seeds, and report (a) mean length drift under each estimator, (b)
  advantage–length correlation, (c) solve rate. Deterministic, ~seconds on CPU.
- **Task (GPU, next):** 250-step rerun of P01 with
  `risk_calibration_weight ×2` and `requirement_weight ×2` on the corrected
  reward, held-out 50 unchanged, report ok_rate/risk_accuracy/decision_accuracy.
  Gate: risk_accuracy must exceed base 0.20 before any further scaling.

## 5. Design decision (recorded in DECISIONS.md)

D-2026-11-09-001: Continue Dr.GRPO (mean-centered, no std division) + DAPO
asymmetric clip (0.28/0.20) + k3 KL 0.01. Do not adopt U-statistic variants
until the risk-weighted reward rerun beats base on risk_accuracy. Freeze step
count until reward content changes land.
