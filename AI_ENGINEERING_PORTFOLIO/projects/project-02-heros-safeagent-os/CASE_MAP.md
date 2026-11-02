# P02 — adversarial corpus map

**Status:** inventory complete; 289/500 cases exist. This file is the
implementation checklist for the 211-case gap.

Source: `packages/mcp/test/adversarial.test.mjs` (289 counted cases) and the
MCP/agentic harnesses.

## Existing 289 cases

| Test | ASI tags | Cases | Surface |
|---|---|---:|---|
| malformed JSON-RPC never crashes | ASI05/ASI09 | 60 | `server.handleMessage` |
| agentic schema validation | ASI01/ASI02 | 78 | `createAgenticApp.execute` |
| invalid/over-scoped API keys | ASI03/ASI10 | 31 | auth session + `tools/call` |
| hostile forge schema payloads | ASI05/ASI06 | 60 | `forge_analyze` / `forge_shadow_analyze` |
| malformed shadow schemas | ASI05 | 30 | shadow gate |
| approval replay/rebinding | ASI02/ASI07 | 30 | approval tokens |

Total: **289**.

## Gap to 500: 211 cases

| Family | ASI tags | Add | Why |
|---|---|---:|---|
| JSON-RPC malformed/boundary | ASI05/09 | 40 | IDs, params, methods, oversized strings, Unicode controls, duplicate sessions |
| Agentic schema mutation | ASI01/02 | 30 | nested objects, unions, arrays, pattern/length edges, idempotency collisions |
| Auth and scope | ASI03/10 | 25 | expired, malformed, cross-org, read-only write, revoked, case variants |
| Forge payloads | ASI05/06 | 30 | parser edges, huge schemas, invalid types, contradictory target schemas |
| Shadow gate | ASI05 | 30 | multi-statement, comments, CTE, temp tables, quoted identifiers, row-count edge cases |
| Approval replay | ASI02/07 | 30 | nonce reuse, payload mutation, cross-session, expired token, concurrent use |
| End-to-end destructive gates | ASI08/09 | 26 | unapproved DROP/TRUNCATE, rollback failure, partial migration, audit gap |

## Corpus format

Each case should have:

```json
{
  "id": "asi05-jsonrpc-061",
  "asi": ["ASI05", "ASI09"],
  "surface": "jsonrpc",
  "seed": 61061,
  "input": {},
  "expected": {
    "error_code": "INVALID_REQUEST",
    "executed": false,
    "bounded": true
  }
}
```

Rules:

- deterministic seed and input;
- expected failure code or bounded success;
- no network, no filesystem, no sleeps;
- one case must not depend on another case's state;
- a case that intentionally succeeds (control group) must say so.

## Implementation order

1. `packages/mcp/test/corpus/` JSON files by surface.
2. `packages/mcp/test/corpus500.test.mjs` runner that maps each surface to the
   existing harness method.
3. Add the missing cases family by family, regenerating the count.
4. Make the runner assert `cases.length === 500` and `failures.length === 0`.
5. Add `npm run test:corpus` and wire it into CI.
6. Only then start the Ed25519 signed-proof work.

## Gate

- 500 deterministic cases.
- 0 unapproved destructive migrations.
- 0 server crashes.
- p99 policy latency < 4.5 ms on the recorded hardware.
- 100% idempotency under 64 concurrent replays.
- browser-verifiable receipt proof.

Do not claim the gate until the runner prints the counts and the browser proof
verifies.
