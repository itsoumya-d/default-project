# Project 06 — EdgeInfer-WGSL-v3

**Rank:** 3 (score 96 **[P]**) · **Execution order:** 3 · **Window:** weeks 6–7
**Status:** README is honest about the missing paged KV; PR #3 adds a design
note only. No shader, no parity harness, no benchmark.

## Problem

`edgeinfer` cannot pin `past_key_values` in a `GPUBuffer` without a custom
kernel; every decode step round-trips KV through the CPU. That is the difference
between a browser demo and a usable local inference runtime.

## Next action

Write the CPU reference for paged attention (`block_size=16`, online softmax)
and a parity harness. The WGSL kernel is not allowed to land before the harness
can prove it wrong.

## Deliverables

- CPU reference and parity harness (20 prompts).
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
