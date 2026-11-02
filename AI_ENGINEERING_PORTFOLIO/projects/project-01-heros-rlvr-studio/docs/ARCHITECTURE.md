# Architecture — Project 01

**Scope:** the verifier/loss slice, the QLoRA runner that now exists on the
stacked branch, and the boundaries between them.
**Rule:** anything marked *planned* is not implemented and must not be described
as working. Anything marked *implemented, untested on GPU* has CPU tests but no
real-model evidence.

---

## 1. Context

HEROS is a deterministic agent runtime: `forge` analyzes schema migrations,
`ledger` records receipts, and the MCP server exposes both to agents. HEROS-RL is
a separate training repository with a critic-free GRPO engine, a 500-case
migration dataset, and TRL/Unsloth entry points.

Project 01 connects them:

```text
                    ┌─────────────────────────────┐
                    │  HEROS-RL dataset + engine  │
                    │  500 migrations, GRPO core  │
                    └──────────────┬──────────────┘
                                   │ prompts
                                   ▼
┌──────────────┐        ┌──────────────────────┐
│ QLoRA policy │───────▶│  rollout generator   │
│ 1.5B / 0.5B   │        │  G samples per task  │
└──────────────┘        └──────────┬───────────┘
                                   │ completions
                                   ▼
                    ┌─────────────────────────────┐
                    │ DeterministicForgeShadow    │
                    │ Verifier (this PR)          │
                    │  SQLite shadow + manifest   │
                    └──────────────┬──────────────┘
                                   │ rewards + receipts
                                   ▼
                    ┌─────────────────────────────┐
                    │ DAPO sampler + Dr.GRPO loss │
                    │ (this PR)                   │
                    └──────────────┬──────────────┘
                                   │ gradients
                                   ▼
                    ┌─────────────────────────────┐
                    │ optimizer / checkpoint      │
                    │ (QLoRARunner, this PR)      │
                    └─────────────────────────────┘
```

The verifier and loss are pure functions with respect to their inputs. The runner
owns all state: model weights, optimizer, RNG, and checkpointing.

---

## 2. Components

| Component | Responsibility | State | Depends on |
|---|---|---|---|
| `MigrationTask` | immutable task record: DDL, seed data, expectation | implemented | stdlib |
| `DeterministicForgeShadowVerifier` | parse completion, run SQL, emit receipt | implemented | stdlib + SQLite |
| `DapoDynamicSampler` | zero-variance detection, Dr.GRPO advantages | implemented | torch for advantages |
| `compute_dr_grpo_token_loss` | clipped policy gradient + KL | implemented | torch |
| `QLoRARunner` | rollout, reward filter, loss, optimizer, checkpoint | implemented, fake-policy tests | torch |
| `HFPolicy` | 4-bit model load, generate, token log-probs, adapter save | implemented, **untested on GPU** | transformers, peft, bitsandbytes |
| `RunRecorder` | `run.json`, `steps.jsonl`, `checkpoints.jsonl`, summary | implemented, tested | stdlib |
| `ShadowWorkerPool` | parallel verifier execution | **planned** | multiprocessing |
| `HFEvaluator` | MATH-500 pass@1 with CI | **planned** | transformers, datasets |

### 2.1 Verifier

Entry point: `verify_rollout(task, completion) -> VerificationReceipt`.

Stages:

1. Regex-extract `<think>`, `<sql_migration>`, `<forge_manifest>`.
2. Fail closed on missing blocks.
3. Parse the manifest; fail closed on non-object JSON.
4. Open a fresh `:memory:` SQLite connection and install the authorizer.
5. Apply `from_ddl`, then `seed_sql`.
6. Snapshot table counts.
7. Apply the migration.
8. Snapshot again; compute row loss.
9. If `target_schema` is supplied, compare the final SQLite schema (tables,
   columns, affinity, `NOT NULL`, primary keys) to it. A mismatch earns
   `REQUIREMENT_MISS` and loses the execution reward.
10. Score format, execution, and three calibration checks.
11. Apply the miracle penalty.
12. Return an immutable receipt.

The verifier has no `async`, no I/O, and no global mutable state. It is safe to
run in a thread or a process, provided each call gets its own connection (it
does).

### 2.2 Loss engine

Inputs are tensors shaped `(G, L)` plus rewards shaped `(G,)`:

```text
advantages = rewards - mean(rewards)                 # Dr.GRPO, no std division
ratio      = exp(policy_logprobs - old_logprobs)      # old is detached
surr1      = ratio * advantages
surr2      = clamp(ratio, 1-0.20, 1+0.28) * advantages
objective  = min(surr1, surr2)                        # DAPO asymmetric clip
kl         = exp(ref - policy) - (ref - policy) - 1   # k3 estimator
loss       = -sum((objective - beta * kl) * mask) / (G * L_max)
```

The denominator is `G * L_max`, not `G * sum(sequence_lengths)`. That is the
Dr.GRPO constant-horizon reduction: a token in a short completion and a token in a
long completion receive the same weight. The consequence is intentional and
documented in `docs/REWARD_SPEC.md` §10: long incorrect completions can dominate
unless `L_max` and the verifier are controlled.

`completion_mask` is applied per token. `valid_tokens` is clamped to at least 1
for metric division, so an all-zero mask produces finite metrics rather than NaN.
The loss itself is zero in that case.

### 2.3 Runner

`qlora_runner.py` implements the orchestration. It is split into a tested
protocol layer and a thin model adapter:

| Piece | Behavior | Tested? |
|---|---|---|
| `parse_forge_schema` / `build_sqlite_ddl` / `build_seed_sql` | strict Forge-schema → SQLite fixture; two seed rows per table | yes |
| `dataset_row_to_task` | validate five forge tiers and map a JSONL row | yes, including all 500 rows |
| `build_prompt` | hazard + current/target schema; no expected labels | yes |
| `QLoRARunner.train_step` | `G` rollouts → verifier → zero-variance filter → token log-probs → loss → optimizer | yes, fake policy |
| `QLoRARunner.run` | steps, checkpoint cadence, final adapter, recorder | yes, fake policy |
| `RunRecorder` | `run.json`, `steps.jsonl`, `checkpoints.jsonl`, `summary.json`; truncates stale logs on restart | yes |
| `HFPolicy` | chat template, 4-bit NF4 load, LoRA, generate, token log-probs, save | **no**; requires GPU stack |

The runner is the only component allowed to touch the GPU. It processes one
prompt group at a time (`B=1`) and accumulates gradients across
`gradient_accumulation` groups. Loss is divided by the accumulation count so the
effective gradient scale does not grow with it. A zero-variance group skips the
optimizer and is recorded as `skipped`; a non-finite loss clears accumulated
gradients and is recorded the same way.

`HFPolicy` applies the tokenizer's chat template to the plain prompt, uses left
padding for generation, and computes completion log-probs by concatenating
prompt ids with completion ids tokenized without added special tokens. It saves
the PEFT adapter and tokenizer, not a merged base model.

No real-model run is claimed. The adapter has not been executed on a GPU in this
session, and no loss curve exists.

---

## 3. Data flow and shapes

| Artifact | Shape / type | Notes |
|---|---|---|
| prompt batch | `(B,)` strings, `B=1` | `HFPolicy` applies the chat template |
| completion batch | `(B, G)` strings | `G` rollouts per prompt |
| token ids | `(B*G, L)` | left-padded for generation |
| `policy_logprobs` | `(G, L)` per prompt | current policy |
| `old_logprobs` | `(G, L)` | detached at rollout time |
| `ref_logprobs` | `(G, L)` | frozen reference model |
| `completion_mask` | `(G, L)` | 1 for generated tokens |
| `rewards` | `(G,)` | verifier output |
| `loss` | scalar | backpropagated |

For memory reasons the runner may process one prompt group at a time (`B=1`)
with gradient accumulation, rather than materializing `B*G` sequences. The loss
function is written for a single group; batching across prompts is a runner
concern.

---

## 4. Determinism and reproducibility

| Source of nondeterminism | Control |
|---|---|
| SQLite version | record `sqlite3.sqlite_version` in `run.json` |
| Python hash seed | set `PYTHONHASHSEED=0` in the run script |
| Torch RNG | `torch.manual_seed`, `torch.cuda.manual_seed_all` |
| cuDNN | `torch.backends.cudnn.deterministic = True` where supported |
| Data order | fixed seed + saved sampler state |
| Generation | greedy for eval; fixed temperature/top-p for rollouts |
| Floating point | fp16 training is not bitwise reproducible; report variance |

The verifier itself is deterministic. The training run is *reproducible within
floating-point tolerance*, not bitwise identical. The model card must say which
claim it makes.

---

## 5. GPU memory budget

This is a **budget**, not a measurement. The run log must replace it with
`torch.cuda.max_memory_allocated()`.

```text
Qwen2.5-Coder-1.5B, 4-bit NF4, r=16, alpha=32, L=512, G=4, B=1

weights (NF4)                     ~0.75 GB
adapters + optimizer state        ~0.09 GB
activations (grad checkpointing)  ~1.20–2.00 GB
logits / temp buffers             ~0.30 GB
rollout KV cache                  ~0.40–0.80 GB
------------------------------------------------
budget                            ~2.74–3.94 GB
RTX 2060 available                6.00 GB
headroom                          2.06–3.26 GB
```

Rules:

- Use fp16 autocast, not bf16 (`torch.cuda.is_bf16_supported()` is false on SM
  7.5).
- Use `paged_adamw_8bit`; the adapter optimizer state is small but paging avoids
  spikes.
- If peak exceeds 5.4 GB, reduce `L` to 384 before reducing `G` below 4.
- If 1.5B still OOMs, switch the local run to 0.5B and move 1.5B to Kaggle. Record
  the switch; do not silently change the model in the results table.

---

## 6. Security and threat model

### 6.1 Assets

- The host filesystem and any database outside the shadow.
- The training process and its GPU memory.
- The integrity of the reward signal.
- The receipt log used for audit.

### 6.2 Adversaries

| Adversary | Capability | Goal |
|---|---|---|
| Model policy | controls the completion text and SQL | escape the shadow, fake safety, maximize reward |
| Prompt injector | controls task text or seed data | alter verifier behavior |
| Corrupted dataset | controls DDL/seed SQL | execute unexpected statements during setup |
| Insider | controls the runner | tamper with rewards or receipts |

### 6.3 Controls

| Threat | Control | Residual risk |
|---|---|---|
| `ATTACH` a file DB | authorizer denies `ATTACH`/`DETACH` | none observed in tests |
| `PRAGMA writable_schema` | authorizer denies | none observed |
| `load_extension` | authorizer denies the function | SQLite build may expose other entry points |
| Multi-statement script | before/after counts catch row loss | attribution is coarse |
| Recursive CTE DoS | none | worker can stall; process isolation planned |
| Memory exhaustion | none | large result sets can OOM the worker |
| Reward tampering | verifier is pure; receipt is immutable | runner can still discard receipts |
| Seed SQL injection | `executescript` runs it as trusted setup | dataset must be curated |
| Prompt injection in task text | task text is not executed | model may be confused, reward unaffected |

### 6.4 Non-goals

- A general-purpose SQL sandbox.
- Protection against a malicious dataset author.
- Network egress control (the verifier makes no network calls).
- Side-channel resistance.

The authorizer is a narrow guard against the obvious escapes. It is not a
container, seccomp profile, or VM. A production trainer should run the shadow gate
in a subprocess with `RLIMIT_AS`, `RLIMIT_CPU`, and no network namespace.

---

## 7. Integration with HEROS

The intended receipt mapping:

| Verifier field | HEROS ledger field | Notes |
|---|---|---|
| `task_id` | `task_id` | join key |
| `total_reward` | `score` | float |
| `error_code` | `status` | `OK` maps to `verified` |
| `shadow_row_loss_detected` | `has_data_loss` | observed, not predicted |
| `risk_calibration_reward` | `risk_score` | partial credit |
| `miracle_step_penalty` | `flags[]` | append `miracle_step` when > 0 |

The current PR does **not** write to the ledger. The mapping is a design contract
for the runner integration; it must be tested against the real ledger schema
before it is claimed.

`forge` remains the production oracle. The SQLite shadow is the training-time
oracle. They must agree on a shared evaluation set before the trained policy is
described as "forge-aligned"; that agreement test is part of P7.

---

## 8. Scaling the verifier

The verifier is CPU-bound and short-lived. A single SQLite connection per rollout
is cheap, but Python-level regex and JSON parsing dominate for short scripts.

Planned `ShadowWorkerPool`:

```text
main process
  ├── worker 0: N prompts -> verifier -> receipts
  ├── worker 1: ...
  └── worker k: ...
        └── results merged in prompt order
```

Design constraints:

- One process per worker, not one thread, to bypass the GIL for parsing.
- Each worker owns its connections; no shared SQLite handle.
- Results are merged by `(prompt_id, rollout_index)` to preserve determinism.
- Backpressure: the pool accepts at most `2 * workers` pending groups.
- Failure policy: a worker crash fails the group, not the run; the run records
  the failure count.

Target: **>1.8× step throughput at 4 workers** versus serial. This is a target,
not a measurement. If the target is not met, report the measured curve and keep
the serial path as the default.

---

## 9. Failure modes

| Failure | Symptom | Response |
|---|---|---|
| Model emits no tags | `MISSING_BLOCKS`, `-1.0` | expected early in training; monitor rate |
| Manifest JSON truncated | `INVALID_JSON`, `-0.5` | cap completion length; add stop tokens |
| SQL references unknown table | `SQL_EXEC_ERROR`, `-0.5` | expected; include schema in prompt |
| All rewards identical | sampler drops every group | raise temperature or check verifier |
| Reward mean rises but eval falls | reward hacking | inspect per-tier calibration and no-op rate |
| Peak VRAM > 5.4 GB | OOM risk | reduce `L`, then `G` |
| Loss NaN | fp16 overflow | lower LR, check mask, use fp32 loss accumulation |
| Verifier slower than generation | GPU idle | increase workers or batch prompts |

---

## 10. Open design questions

1. **Requirement satisfaction.** The verifier rewards safety, not correctness. A
   no-op scores `2.0` on a safe task. v2 needs a schema-diff check.
2. **Row identity.** Counts miss delete-and-reinsert. Hashing a sample of rows is
   cheap but not free.
3. **Ledger coupling.** Should the training receipt be the same object the
   production ledger stores, or a projection?
4. **Forge parity.** Which oracle is authoritative when SQLite and `forge`
   disagree?
5. **Process isolation.** Is a subprocess per group affordable at 500 steps, or
   does the pool need a long-lived sandbox?
6. **Evaluation contamination.** The 500-case dataset is also the training set.
   A held-out shadow set is required before any generalization claim.

None of these blocks the current code slice. All of them block a production claim.
