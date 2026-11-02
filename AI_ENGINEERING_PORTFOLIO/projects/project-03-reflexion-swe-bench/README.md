# Project 03 — Reflexion-SWE-Bench

**Rank:** 4 (score 93 **[P]**) · **Execution order:** 5 · **Window:** weeks 12–13
**Status:** actor/evaluator/reflection loop and a toy evaluation exist; no
mutation gate, no persistent skill library, no Lite-50 run.

## Problem

Reflexion regresses on MBPP (77.1 vs 80.1) because self-generated tests have
false positives, and the Ω=3 memory forgets cross-task lessons. A repair loop
that grades itself with its own bad tests is worse than no loop.

## Next action

Implement the mutation-adequacy gate: generate AST mutants, require a generated
test suite to kill at least 80% before it may grade a patch. Measure the
false-positive rate on a 20-issue pilot before paying for Lite-50.

## Deliverables

- Tree-sitter mutant generator + kill-rate gate.
- Persistent Matryoshka skill library replacing the sliding window.
- SWE-bench Lite-50 repair run with tokens per resolved issue.
- Inspector UI with the four required states.

## Gate

MBPP regression eliminated; false-positive test rate <2%; Lite-50 resolution
rate reported with mean tokens per resolved issue; no repository corruption.

## Dependencies and risks

Needs P01's policy and P02's receipts for the sandbox, plus Docker images and
time. If Lite-50 infrastructure is not ready by week 12, run P05 instead. Do not
claim a resolution rate from a subset without labeling it.
