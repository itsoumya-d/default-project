# Project 06 — EdgeInfer-WGSL-v3

**Rank:** 3 (score 96 **[P]**) · **Execution order:** 3 · **Window:** weeks 6–7
**Status:** The CPU reference and parity harness are merged in
[PR #16](https://github.com/itsoumya-d/edgeinfer/pull/16) (`0d17672`). No WGSL
kernel, no SmolLM2 parity, no zero-readback trace, and no benchmark exist yet.

## Problem

`edgeinfer` cannot pin `past_key_values` in a `GPUBuffer` without a custom
kernel; every decode step round-trips KV through the CPU. That is the difference
between a browser demo and a usable local inference runtime.

## Next action

Implement the WGSL paged-decode kernel behind a feature flag only after the
reference can catch it. Start with a single-layer MHA path, keep the existing
ORT path as fallback, and run the parity harness before adding any performance
claim.

## Deliverables

- CPU reference and parity harness (20 deterministic cases; PR #16).
- WGSL paged-decode kernel with a dense fallback flag.
- Zero-readback trace: no `mapAsync` on KV buffers.
- p50/p95 on two devices with browser and driver versions.
- Memory within 5% of the analytic KV size.

## Gate

Parity with ORT on 20 prompts; 0 KV `mapAsync`; memory within 5%; two-device
benchmark; fallback works. No "10×" claim before the measurement.

## Dependencies and risks

CPU work is unblocked. GPU browser access is the risk. If parity fails after
three kernel iterations, publish the CPU reference and the negative result. Do
not ship a shader that does not attend.
