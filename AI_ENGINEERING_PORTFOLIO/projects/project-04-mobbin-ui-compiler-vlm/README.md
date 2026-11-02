# Project 04 — Mobbin-UI-Compiler-VLM

**Rank:** 9 (score 86 **[P]**) · **Execution order:** 9 · **Window:** deferred
**Status:** fixture adapter and five surfaces exist; no real VLM, no typed
UI-AST, no deterministic accessibility audit.

## Problem

Screenshot-to-code tools produce visually plausible but inaccessible code.
Without a typed intermediate representation and an automated audit, "it looks
right" is the only quality signal.

## Next action

Define the typed UI-AST and a fixture-based converter before adding a VLM. The
AST is the part that survives a model swap.

## Deliverables

- Typed UI-AST with a JSON schema.
- Qwen2-VL-2B 4-bit or Gemini Flash adapter behind a flag.
- Playwright + axe-core audit harness.
- Design2Code benchmark slice with an IoU baseline.

## Gate

100% WCAG 2.2 AA on the generated benchmark; IoU improvement over one-shot; no
live-Mobbin claim unless the MCP server is actually connected.

## Dependencies and risks

Best after P06's browser tooling. VLM hosting is the main cost risk; use a local
2B model for the demo and a hosted model only for a labeled comparison. Deferred
until the GPU flagships ship.
