# Paper note — Reflexion (Shinn et al.)

**Claim.** A language-enhanced agent can improve task performance by verbal
reflection on failure traces, without weight updates: actor → evaluator →
self-reflection → short-term memory (last `Ic` trials) → retry.

**Equation.** Not an optimization equation — a stochastic fixed-point: each
retry conditions on `reflection_1..t`, so success probability grows by
accumulated feedback, capped by evaluator accuracy.

**Experiment (this portfolio).** `Reflexion-SWE` implements the loop with a
SQLite shadow-exec evaluator and a "training-free GRPO" variant
(`reflexion_swe/tf_grpo.py`). Toy ablation is committed
(`experiments/toy_ablation.json`): memory ablation (`Ic=3`) vs baseline.
Verified locally this session: `pytest tests` → **40 passed**. No Lite-50
SWE-bench run exists; `prepare_swebench_lite.py` only fetches tasks.

**Limitation (from the paper's own ablation, and local relevance).** Reflexion
regresses on MBPP (77.1 vs 80.1) because self-generated tests have false
positives — a repair loop that grades itself with its own bad tests is worse
than none. `Ic=3` forgets cross-task lessons; no persistent skill library.

**Reproduction task.** Run a Lite-50 subset through the existing loop with the
shadow evaluator (not self-grading), report resolved rate + reflection-token
overhead vs baseline. Deferred to a GPU session; spec in `project-03` README.
