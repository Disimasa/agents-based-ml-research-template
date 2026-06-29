---
name: manuscript-draft
description: Write phase — build manuscript draft from research artifacts
---

# Manuscript draft

**Phase:** `write` | **Agent:** `manuscript_writer`

## Prerequisites

- `synthesize` complete; M1–M5 PASS on research track
- `runtime/state/passport.yaml` `claims`, `research/methodology.md`, `runtime/state/benchmarks/`

## Steps

1. Copy `runtime/templates/manuscript_draft.template.md` → `research/manuscript/draft.md`.
2. Fill sections from `runtime/state/passport.yaml` and `research/methodology.md` only.
3. Results: copy metrics from benchmark JSON; tag `<!-- experiment_id: exp_XXX -->`.
4. If no run: state `[not executed]` — do not invent numbers.
5. Set `runtime/state/passport.yaml` → `write_status: draft`.
6. `uv run python runtime/scripts/integrity_check.py --modes M7`.
7. HITL: human approves draft → advance to `integrity_pre_review`.

## Gate 2.5

At `integrity_pre_review`:

```bash
uv run python runtime/scripts/orchestrate_pipeline.py gate
# profile: gate_2_5_pre_review — M1–M7
```

## Handoff

→ `peer-review` after gate PASS + human ack
