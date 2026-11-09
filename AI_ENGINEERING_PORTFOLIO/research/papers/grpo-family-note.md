# Paper note — GRPO family (GRPO / Dr. GRPO / DAPO)

**Claim.** Group-relative policy optimization trains reasoning models from
verifiable rewards without a critic network; Dr. GRPO removes GRPO's length
and difficulty biases; DAPO fixes entropy collapse with asymmetric clipping.

**Equation.** Standard: `A_i = (r_i − mean(r)) / std(r)`, broadcast to all
tokens of completion `o_i`. Dr. GRPO: mean-center only, normalize by a constant.
DAPO: clip ratios with `[1 − ε_low, 1 + ε_high]`, `ε_high > ε_low`.

**Experiment (this portfolio).** P01 100-step RL-from-base
(`runs/2026-11-03-rl-base-100-corrected`, Qwen2.5-Coder-1.5B, LoRA r16, group 4,
temp 1.0, RTX 2060): 91/100 completed steps, mean reward first-10 −0.66 →
last-10 −0.04; 50-task held-out: ok_rate 0.20 (base 0.20), risk_accuracy 0.10.
Full synthesis in `literature_reviews/length-difficulty-bias-rlvr.md`.

**Limitation.** The correction is necessary but not sufficient — when reward
content under-pays requirement checks and risk calibration, a bias-free
estimator still cannot learn the right behavior.

**Reproduction task.** `rlvr-bias-probe` (CPU): simulate length-correlated
spurious reward, compare GRPO vs Dr.GRPO length drift / solve rate with fixed
seeds. See package README.
