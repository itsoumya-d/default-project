# Project 05 — MetaRoute-Gateway

**Rank:** 5 (score 92 **[P]**) · **Execution order:** 6 · **Window:** conditional
**Status:** Bradley-Terry router and a synthetic 69.40% cost reduction exist;
no K≥4 latent router, no INT8 ONNX export, no measured cost-quality curve.

## Problem

Binary strong-vs-weak routing cannot handle four or more specialized models, and
a frozen router drifts when prices or model versions change. The existing
69.40% figure is synthetic and must not be quoted as a production result.

## Next action

Build the K≥4 offline evaluation on RouterBench before training anything. A
router that cannot be evaluated is a demo, not a system.

## Deliverables

- Latent preference encoder over K≥4 models.
- INT8 ONNX export under 15 MB.
- APGR and CPT-95 on RouterBench and a Chatbot Arena slice.
- FastAPI gateway with a deterministic fallback.

## Gate

K≥4; p99 <6 ms; APGR and CPT-95 reported; >2.5× cost reduction on MMLU/GSM8K at
≤1 point loss; price table versioned in the report.

## Dependencies and risks

Needs P01's local model and a real price baseline. This is the fallback if P03's
Docker infrastructure is not ready in week 12. Do not compare against a stale
price table without a date.
