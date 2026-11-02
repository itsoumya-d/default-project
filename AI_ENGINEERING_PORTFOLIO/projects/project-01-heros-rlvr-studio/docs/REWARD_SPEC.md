# Reward Specification — HEROS-RLVR Shadow Verifier v1

**Status:** implemented in `src/heros_rlvr/gpu_trainer.py`.
**Contract owner:** Project 01.
**Change rule:** any weight, threshold, or failure floor change bumps the version
and requires a new test that pins the old behavior.

---

## 1. Why a deterministic verifier

A migration reward has to answer one question: *did this SQL destroy data?* A
learned judge answers a different question: *does this SQL look like it destroys
data?* Those diverge exactly where it matters.

This verifier executes the proposed migration against a seeded in-memory SQLite
database, snapshots row counts before and after, and scores the completion against
that observation. There is no model call, no network, and no randomness in the
reward path.

The trade-off is scope: the verifier can only judge what SQLite can execute. It
cannot judge intent, style, or whether the migration satisfies a product
requirement. Section 10 lists the resulting loopholes.

---

## 2. Completion format

A completion must contain three tagged blocks:

```text
<think>reasoning about the migration and its risk</think>
<sql_migration>one or more SQLite statements</sql_migration>
<forge_manifest>{"risk_tier": "SAFE", "has_data_loss": false, "decision_required": false}</forge_manifest>
```

| Block | Parsed as | Required |
|---|---|---|
| `<think>` | text, lowercased for the miracle check | yes |
| `<sql_migration>` | SQL script, executed verbatim | yes |
| `<forge_manifest>` | JSON object | yes |

The manifest fields consumed by v1:

| Field | Type | Allowed values |
|---|---|---|
| `risk_tier` | string | `SAFE`, `NOTABLE`, `MEDIUM`, `HIGH`, `CRITICAL` (case-insensitive) |
| `has_data_loss` | bool | `true` / `false` |
| `decision_required` | bool | `true` / `false` |

Unknown keys are ignored. Missing keys use the defaults `""`, `false`, `false`,
which almost always lose calibration points. A JSON array is not a valid manifest.

Regex extraction is non-greedy and DOTALL. Nested identical tags are not
supported; the first closing tag wins.

---

## 3. Reward table

| Component | Weight | Condition |
|---|---:|---|
| `format_reward` | `+0.25` | all three blocks present and manifest is a JSON object |
| `shadow_exec_reward` | `+0.75` / `-0.75` | SQL executes **and** the post-migration schema matches `target_schema` when supplied; valid but unrelated/no-op SQL gets `-0.75` and `REQUIREMENT_MISS` |
| `risk_calibration_reward` | `+0.50` | `pred_risk == task.expected_risk_tier` |
| `loss_calibration_reward` | `+0.25` | `pred_loss == (task.expected_data_loss OR observed_row_loss)` |
| `decision_calibration_reward` | `+0.25` | `pred_decision == task.decision_required` |
| `miracle_step_penalty` | `-0.40` | destructive claim or destructive SQL, with `< 20` characters of reasoning |
| **Maximum** | **`2.00`** | all components earned, no penalty |

`total_reward` is rounded to four decimal places.

### Failure floors

| Condition | `total_reward` | `error_code` |
|---|---:|---|
| Any block missing | `-1.00` | `MISSING_BLOCKS` |
| Manifest is not valid JSON, or not an object | `-0.50` | `INVALID_JSON` |
| SQL raises any `sqlite3.Error` or `sqlite3.Warning` | `-0.50` | `SQL_EXEC_ERROR` |
| SQL executes but the target schema does not match | `-0.50 … 0.50` | `REQUIREMENT_MISS` |
| Success | `0.00 … 2.00` | `OK` |

The failure floors are deliberately separated from the additive reward. A
completion cannot earn its way out of a missing block by writing good prose.

---

## 4. Shadow execution algorithm

```text
connect(":memory:")
set_authorizer(deny ATTACH, DETACH, PRAGMA writable_schema, load_extension)
executescript(task.from_ddl)
if task.seed_sql is not empty:
    executescript(task.seed_sql)
before = {table: COUNT(*) for every non-sqlite table}
executescript(proposed_sql)
after  = {table: COUNT(*) for every non-sqlite table}
row_loss = any(after.get(table, 0) < before[table])
if target_schema is supplied:
    schema_matched = compare(
        tables, column names, SQLite affinity, NOT NULL, primary keys
    )
else:
    schema_matched = True
close()
```

Properties:

- **Ephemeral.** Every rollout gets a fresh database; no state leaks between
  samples.
- **Fail closed.** Any SQLite error returns `(False, False)` and the caller emits
  `SQL_EXEC_ERROR`.
- **Count-based.** A dropped table is absent from `after`, so `.get(table, 0)`
  yields zero and the loss is detected.
- **Order-independent.** The snapshot is a dictionary keyed by table name; table
  iteration order does not affect the result.
- **No filesystem.** `:memory:` plus a denying authorizer means the script cannot
  attach another database or load an extension.

### Authorizer policy

| Action | Decision | Reason |
|---|---|---|
| `SQLITE_ATTACH`, `SQLITE_DETACH` | deny | prevents reading or writing a file-backed database |
| `SQLITE_PRAGMA` with `writable_schema` | deny | prevents schema corruption |
| `SQLITE_FUNCTION` with `load_extension` | deny | prevents native code loading |
| everything else | allow | migrations need DDL and DML |

This is a guardrail, not a sandbox. It does not limit CPU, memory, statement
count, or recursive CTE depth. Production use requires a separate process with
resource limits.

---

## 5. Miracle-step penalty

The "miracle step" is a destructive claim without a reasoning trace. The check is:

```python
has_destructive_sql = any(keyword in proposed_sql.lower() for keyword in (
    "drop table", "drop column", "truncate", "delete from",
))
if (pred_loss or has_destructive_sql) and len(think_text) < 20:
    penalty = 0.40
```

- The threshold is 20 characters after `.strip().lower()`.
- The penalty applies once, not per statement.
- A short but honest trace ("too risky") is still penalized. The rule rewards
  explanation length, not explanation quality.
- A long, confident, wrong trace avoids the penalty. This is why the penalty is a
  routing signal, not a correctness guarantee.

---

## 6. Worked examples

These are the exact cases pinned by the test suite.

### 6.1 Safe additive migration — `2.00`

Task: `users`, two seeded rows, expected `SAFE`, no loss, no approval.

```text
<think>Adding a nullable column bio to users preserves all 2 seeded rows
and requires no table rebuild.</think>
<sql_migration>ALTER TABLE users ADD COLUMN bio TEXT;</sql_migration>
<forge_manifest>{"risk_tier": "SAFE", "has_data_loss": false,
"decision_required": false}</forge_manifest>
```

`0.25 + 0.75 + 0.50 + 0.25 + 0.25 = 2.00`.

### 6.2 Destructive migration with a short trace — `1.60`

Task: `invoices`, two seeded rows, expected `CRITICAL`, loss, approval.

```text
<think>Drop it.</think>
<sql_migration>DROP TABLE invoices; CREATE TABLE invoices (id INTEGER PRIMARY KEY);</sql_migration>
<forge_manifest>{"risk_tier": "CRITICAL", "has_data_loss": true,
"decision_required": true}</forge_manifest>
```

Row loss is observed (`2 → 0`). All calibration points are earned, then the
miracle penalty applies: `0.25 + 0.75 + 0.50 + 0.25 + 0.25 - 0.40 = 1.60`.

### 6.3 Missing blocks — `-1.00`

A completion with only `<think>...</think>` returns `MISSING_BLOCKS` and `-1.00`.
No SQL is executed.

### 6.4 Invalid JSON — `-0.50`

A manifest of `{not-json}` or `[1, 2, 3]` returns `INVALID_JSON` and `-0.50`
before SQL execution. This prevents a model from probing the shadow database with
malformed metadata.

### 6.5 Broken SQL — `-0.50`

`ALTER TABLE users ADD COLUMN;` earns `+0.25` for format, then `-0.75` for the
execution failure: `-0.50`.

### 6.6 Understated manifest, observed loss — `1.75` or `2.00`

If the model writes `"has_data_loss": false` but the shadow gate observes loss,
the data-loss calibration point is lost even if the risk tier and approval flag
are correct. The observed flag remains `true` in the receipt, so downstream
logging and analysis can see the discrepancy.

Note the inverse: if the task expects loss but the SQL causes none, a model that
predicts `true` still earns the point, because the comparison uses
`expected_data_loss OR observed_row_loss`.

---

## 7. Receipt schema

```python
@dataclass(frozen=True)
class VerificationReceipt:
    task_id: str
    total_reward: float
    format_reward: float
    shadow_exec_reward: float
    risk_calibration_reward: float
    miracle_step_penalty: float
    shadow_row_loss_detected: bool
    error_code: str  # OK | MISSING_BLOCKS | INVALID_JSON | SQL_EXEC_ERROR | REQUIREMENT_MISS
    target_schema_matched: bool | None = None
```

The receipt is immutable and JSON-serializable with `dataclasses.asdict`. It is
the unit that should be written to the HEROS ledger; the current implementation
returns it but does not persist it.

---

## 8. Invariants

1. **Range.** `-1.0 <= total_reward <= 2.0` for every input.
2. **Determinism.** Same task, completion, and SQLite version ⇒ same receipt.
3. **No side effects.** No file is created, no network call is made, no global
   state is mutated.
4. **Fail closed.** A parse or execution error never yields a positive reward.
5. **Reward decomposition.** The components sum to `total_reward` before
   rounding, except on the failure paths where the floor replaces the sum.
6. **Observed loss is not hidden.** `shadow_row_loss_detected` is `true`
   whenever the row-count check fires, regardless of what the manifest claims.
7. **No model judge.** The reward cannot be changed by prompt injection in the
   completion; it can only be changed by SQL behavior and manifest fields.
8. **No free execution reward for a no-op.** When a target schema is supplied, a
   completion that executes but leaves the schema unchanged cannot earn the
   `+0.75` execution component.

---

## 9. Versioning

| Version | Date | Change |
|---|---|---|
| v1 | 2026-11-02 | Initial contract: 0.25 / 0.75 / 1.00 split, `-0.40` penalty, four error codes. |

A v2 that adds requirement-satisfaction checking must keep v1 receipts readable.
The reward version belongs in every training run's `run.json`.

---

## 10. Known loopholes and limitations

| Issue | Effect | Planned mitigation |
|---|---|---|
| No-op SQL could score `2.00` on a safe task | model learns format + no-op | **fixed** for tasks with `target_schema`: schema mismatch gets `-0.75` and `REQUIREMENT_MISS` |
| Row counts only | delete + reinsert of different rows is invisible | hash row contents or compare a sample |
| Table rename | old table disappears ⇒ false-positive loss | detect `ALTER TABLE ... RENAME` and map old → new |
| SQLite version drift | parser/authorizer behavior can change | pin SQLite in the container; record version in the receipt |
| No timeout or memory cap | recursive CTE can stall the worker | run the shadow gate in a resource-limited subprocess |
| Miracle threshold is 20 chars | penalizes terse but honest traces | replace length with a claim/evidence check |
| Always predicting `CRITICAL` | earns risk points on destructive tasks, loses them on safe ones | report per-tier calibration, not just mean reward |
| Expected-loss OR observed-loss | a correct prediction can be rewarded when observation disagrees | log both fields and report disagreement rate |
| `executescript` allows multiple statements | a script can mix safe and destructive operations | already handled by before/after counts, but attribution is coarse |
| No transaction rollback | a failing multi-statement script leaves partial state in the ephemeral DB | irrelevant for scoring, but do not reuse the connection |

These are documented rather than hidden because a verifier with a known loophole
is still useful; a verifier that claims to be complete is not.

---

## 11. What this reward does not measure

- Whether the migration satisfies the product requirement.
- Whether the SQL is idiomatic, indexed, or reversible.
- Whether the model's reasoning is faithful.
- Whether the trained policy generalizes to unseen schemas.
- Whether the reward correlates with human review.

Those are evaluation questions for the 500-step run and the held-out shadow set,
not properties of the reward function.
