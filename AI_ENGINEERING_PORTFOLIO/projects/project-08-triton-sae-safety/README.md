# Project 08 — Triton-SAE-Safety

**Rank:** 6 (score 95 **[P]**, which is actually fourth by score) ·
**Execution order:** 4 · **Window:** weeks 9–11
**Status:** `Anthropic-PerfBench` has NEON kernels; no Triton, no SAE, no RTX
2060 run.

## Problem

Eager SAE training is HBM-bound, and interpretability work that cannot train at
scale stays a notebook. The safety question is concrete: can activation steering
suppress insecure code without hurting pass@1?

## Next action

Train an eager Top-K SAE on Qwen2.5-Coder-1.5B layer 14 and measure `R²` before
writing a kernel. A fused kernel for a bad SAE is wasted work.

## Deliverables

- Eager PyTorch SAE with `R² > 0.92` on held-out activations.
- Roofline chart with achieved vs theoretical bandwidth.
- Fused centering + encoder + Top-K Triton kernel, parity within 1e-3.
- Activation-steering evaluation against `Code_Vulnerability_Security_DPO`.
- safetensors weights and a model card.

## Gate

>2.4× kernel speedup with a measured baseline; `R² > 0.92`; CWE suppression with
no pass@1 regression; weights on HF.

## Dependencies and risks

Shares the RTX 2060 with P06. Kernel tuning can eat a week with no result; the
kill criterion is two tuning rounds, then publish the roofline and the negative
result. Do not claim a speedup from a different batch or sequence shape.
