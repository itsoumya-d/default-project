# Project 01 runs

| Run | Model | Steps | Optimizer steps | Status | Evidence |
|---|---|---:|---:|---|---|
| `2026-11-02-gpu-smoke-0.5b` | Qwen2.5-Coder-0.5B-Instruct, fp16 | 10 | 0 | negative smoke | all groups zero-variance, `MISSING_BLOCKS` |
| `2026-11-02-gpu-smoke-1.5b` | Qwen2.5-Coder-1.5B-Instruct, NF4 | 10 | 7 | positive smoke | mean reward 0.339, 4.15 GB peak, 185 s |
| `2026-11-02-a3-500-qwen1.5b` | Qwen2.5-Coder-1.5B-Instruct, NF4 | 500 | in progress | running | `run.json`, `steps.jsonl`, checkpoints every 50 |

The 1.5B smoke uses the #104 prompt exemplar. The 500-step run is a single arm
(Dr.GRPO + DAPO), not the four-arm ablation. No run has a held-out evaluation or
a published adapter.
