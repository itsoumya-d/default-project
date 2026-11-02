# Infrastructure Strategy — Zero-Cost, Local-First

Constraint: every demo must work without a paid server, and every training run
must fit a 6 GB RTX 2060 or a free Kaggle/Colab session. Quotas change without
notice; the values below are a planning baseline, not a contract. Re-check the
provider console before a run.

**Verified in this session:** local Python 3.11.13, Node 22.18.0, PyTorch
2.15.0+cpu in a temp venv, no GPU exposed to the agent. The RTX 2060 and MacBook
Air are the owner's hardware, not the agent's.

---

## 1. Hardware matrix

| Resource | Verified / planned specs | Assigned work | Guardrail |
|---|---|---|---|
| **RTX 2060 (local)** | 6 GB GDDR6, 1,920 CUDA cores, 240 Tensor cores, ~336 GB/s, Turing SM 7.5, fp16/int8/int4, **no native bf16** | 4-bit QLoRA SFT + Dr.GRPO on 0.5B–1.5B (`G=4`, 512 tokens); Triton SAE; Ollama/Qwen2.5-Coder-3B-Q4; WebGPU Vulkan/D3D12 benchmarks | Gradient checkpointing, `paged_adamw_8bit`, micro-batch 1 + accumulation, fp16. If OOM: 384 tokens before `G<4`. |
| **MacBook Air** | Unified memory, Metal/WebGPU, ARM CPU | TypeScript/Next.js; Rust→WASM; Zero builds; Tree-sitter/Leiden | Offload CUDA/Triton/Docker-heavy jobs to the RTX 2060 or Kaggle. |
| **Kaggle** | ~30 h/week free GPU; 2×T4 16 GB = 32 GB VRAM (or P100 16 GB) | `G=8` on Qwen2.5-Coder-3B; MATH-500/RouterBench batches; one-click notebooks | Checkpoint the adapter to HF every 50 steps; sessions time out. |
| **Colab** | Dynamic free T4 16 GB | Notebook reproduction; small evals | Do not depend on it for a deadline. |
| **Oracle Always Free** | Reported June 2026 cut to 2 OCPU / 12 GB ARM, 200 GB block storage; idle instances reclaimed | Optional Docker/SWE-bench Lite host | Never make a demo depend on an always-on VM. |
| **HF Spaces** | CPU Basic 2 vCPU / 16 GB; free | 11 demo Spaces | Stateless startup <5 s; pre-compute artifacts. |
| **Cloudflare Pages/Workers** | 100k req/day free (verify current) | Portfolio site; router proxy | Static export first; Workers only for a webhook. |
| **Neon Postgres** | 0.5 GB free | Project 10 commercial layer only | SQLite/DuckDB is the default demo path. |

---

## 2. VRAM budget for Project 01

A 1.5B model in 4-bit NF4 is roughly:

```text
weights   ≈ 1.5e9 × 0.5 bytes  ≈ 0.75 GB
adapters  ≈ 2 × r × d × layers ≈ 0.03 GB (r=16)
optimizer ≈ paged 8-bit AdamW  ≈ 0.06 GB (adapter params only)
activations (grad checkpointing, B=1, L=512) ≈ 1.2–2.0 GB
logits / temp buffers ≈ 0.3 GB
KV / rollout cache for G=4 ≈ 0.4–0.8 GB
------------------------------------------------
total ≈ 2.7–4.0 GB, leaving headroom under 6 GB
```

This is a budget, not a measurement. The run log must record
`torch.cuda.max_memory_allocated()` and the actual batch/sequence settings. If
the measured peak exceeds 5.4 GB, reduce sequence length first.

**Turing note:** use fp16 autocast, not bf16. `torch.cuda.is_bf16_supported()`
returns False on SM 7.5. QLoRA's NF4 compute dtype should be fp16.

---

## 3. Free-tier API limits (planning baseline)

| API tier | RPM | TPM | RPD | Notes |
|---|---:|---:|---:|---|
| Gemini Flash free (AI Studio, no billing) | 15 | 1,000,000 | 1,500 | **Verify in the console.** Limits are enforced independently; any one triggers HTTP 429. |
| Gemini Pro free | 2 | 32,000 | 50 | Input/output token caps vary by snapshot. |
| Gemini 2.5 Pro free | 5 | — | 25 | Reported; verify. |
| Local Ollama / llama.cpp | unlimited | — | — | Default for private code; no data leaves the machine. |

**Privacy rule:** the free AI Studio tier may log inputs/outputs for training.
Never send private keys, proprietary code, or customer data. Use local models for
anything sensitive.

**Implementation rule:** wrap every hosted call in a token bucket and exponential
backoff with jitter. Do not retry a 429 immediately; that deepens the throttle.

```python
import random
import threading
import time


class TokenBucket:
    """Thread-safe token bucket for RPM/TPM-style limits."""

    def __init__(self, rate: float, capacity: float):
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.updated = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self, amount: float = 1.0) -> None:
        while True:
            with self.lock:
                now = time.monotonic()
                self.tokens = min(
                    self.capacity, self.tokens + (now - self.updated) * self.rate
                )
                self.updated = now
                if self.tokens >= amount:
                    self.tokens -= amount
                    return
                wait = (amount - self.tokens) / self.rate
            time.sleep(wait)


def backoff(attempt: int, base: float = 1.0, cap: float = 60.0) -> float:
    """Exponential backoff with full jitter."""
    return min(cap, random.uniform(0, base * (2 ** attempt)))
```

For a 15 RPM limit, use `rate=15/60` and `capacity=15`; acquire one token per
request. For TPM, acquire `(input_tokens + output_tokens)` with
`capacity=1_000_000`. Never run both buckets in parallel without a shared lock if
the provider counts them together.

---

## 4. Four deployment topologies

### Topology 1 — completely local-first (default)

Browser WebGPU + WASM + IndexedDB/OPFS; Node 22 + Zero binaries + SQLite WAL.
Used by edgeinfer, peervault, pulsenet (if confirmed), and the HEROS CLI. Works
offline, no recurring cost, no data egress.

### Topology 2 — serverless/static edge

GitHub Pages (static), Cloudflare Pages/Workers (proxy), HF CPU Spaces (demos),
Neon (optional commercial DB). Used by the portfolio site, the ten Spaces, the
MetaRoute ONNX proxy, and the HEROS Cloud webhook. Design for <5 s cold start and
bundle pre-computed JSON/DuckDB artifacts.

### Topology 3 — ephemeral GPU

Kaggle/Colab for training and batch eval; checkpoint to HF every 50 steps. Never
store the only copy of a result on an ephemeral disk. The RTX 2060 is the
persistent local trainer for small runs.

### Topology 4 — hybrid cascade

Local Qwen2.5-Coder-3B handles routine code/AST queries; escalate complex
multi-file synthesis to Gemini Flash inside a token bucket; fall back to local
Ollama if the quota is exhausted. The router must expose the fallback reason in
response metadata.

---

## 5. Reproducibility contract

Every benchmark artifact includes:

```yaml
hardware: "NVIDIA RTX 2060 6GB / Apple M2 / Kaggle T4x2"
os: "Windows 11 / macOS 15 / Ubuntu 22.04"
driver: "NVIDIA 5xx.xx / Metal 3"
runtime: "Python 3.11.13, torch 2.15.0+cu..., CUDA 12.x"
model: "Qwen/Qwen2.5-Coder-1.5B-Instruct @ <sha>"
dataset: "itssoumyad/heros-migration-500 @ <sha>"
seed: 42
batch: 1
grad_accum: 8
max_length: 512
group_size: 4
command: "python -m heros_rlvr.train ..."
peak_vram_gb: 4.1
wall_clock_min: 37
```

No artifact without this block. Synthetic results say "synthetic" in the title.

---

## 6. Secrets and access

- No tokens in Markdown, notebooks, or git history.
- Use `HF_TOKEN`, `WANDB_API_KEY`, `OPENAI_API_KEY` from the environment; provide
  `.env.example` with empty values.
- The agent never asks for a password. A login/2FA/CAPTCHA gate is reported to
  the user with the exact URL and state, and only that browser action pauses.
- Browser sessions are user-owned; do not export cookies or credentials.

---

## 7. Cost guardrails

| Guardrail | Rule |
|---|---|
| Training | Stop if projected wall-clock > 6 h on a free GPU or peak VRAM > 5.4 GB. |
| API | Hard cap per run; token bucket + daily budget; log every call's tokens. |
| Storage | HF datasets <5 GB per artifact; prune checkpoints older than the best two. |
| Demos | No always-on VM; no paid DB for a demo; static or CPU Space only. |
| Commercial | Stripe only after the validation gates in `CAREER_ALIGNMENT.md` §4. |
