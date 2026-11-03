# Project 06 — EdgeInfer-WGSL-v3

**Rank:** 3 (score 96 **[P]**) · **Execution order:** 3 · **Window:** weeks 6–7
**Status:** CPU reference and harness
([PR #16](https://github.com/itsoumya-d/edgeinfer/pull/16), `0d17672`), GQA
support ([PR #18](https://github.com/itsoumya-d/edgeinfer/pull/18), `a501d55`),
the 20-prompt ORT baseline
([PR #19](https://github.com/itsoumya-d/edgeinfer/pull/19), `96574e7`), the first
WGSL kernel ([PR #20](https://github.com/itsoumya-d/edgeinfer/pull/20),
`31a2e77`), and the f16 KV cache
([PR #21](https://github.com/itsoumya-d/edgeinfer/pull/21), `1b00c0a`) are
merged. The kernel passes **20/20 synthetic cases** on Chrome 156 / NVIDIA
Turing with max absolute error **4.79e-8**; **40/40 KV buffer creates** pass the
runtime zero-readback capability check. The Node suite is **113/113** and the
Python suite is **14 tests**. No SmolLM2 token parity, validation-layer trace,
memory-within-5% measurement, or benchmark exists.

## Problem

`edgeinfer` cannot pin `past_key_values` in a `GPUBuffer` without a custom
kernel; every decode step round-trips KV through the CPU. That is the difference
between a browser demo and a usable local inference runtime.

## Next action

Wire the kernel into a paged decode path that can be compared token-for-token
with the 20-prompt ORT baseline, and add a validation-layer `mapAsync` trace plus
peak-KV memory accounting. Keep the ORT path as default until those gates pass.

## Deliverables

- CPU reference and parity harness (20 deterministic cases; PRs #16/#18).
- 20-prompt ORT baseline fixture (PR #19; 542 generated tokens).
- WGSL paged-decode kernel (f16 KV, f32 accumulation; PRs #20/#21).
- Zero-readback runtime capability check (40/40 clean; validation-layer trace
  still pending).
- p50/p95 on two devices with browser and driver versions.
- Peak KV memory within 5% of the analytic size.

## Gate

Synthetic tensor parity is **20/20** with f16 storage. The full gate remains
open: ORT parity on 20 prompts, 0 KV `mapAsync` in a validation trace, peak
memory within 5%, two-device benchmark, and fallback behavior. No "10×" claim
before the measurement.

## Dependencies and risks

CPU work is unblocked. GPU browser access is the risk. If parity fails after
three kernel iterations, publish the CPU reference and the negative result. Do
not ship a shader that does not attend.
