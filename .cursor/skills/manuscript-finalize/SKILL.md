---
name: manuscript-finalize
description: Finalize phase — submission-ready package after gate 4.5
---

# Manuscript finalize

**Phase:** `finalize` | **Agent:** `manuscript_writer`

## Prerequisites

- Gate 4.5 PASS (`integrity_final` — M1–M7)
- `editorial_decision.decision: accept` (or human override logged)

## Steps

1. Confirm gate:

```bash
uv run python runtime/scripts/orchestrate_pipeline.py gate
# gate: ARS gate 4.5 (pre-finalize)
```

2. Polish `research/manuscript/draft.md`: abstract, limitations, consistency pass.
3. Export checklist to `research/to_human/finalize_checklist.md`:
   - all claims tagged
   - benchmarks linked
   - `runtime/state/manuscript_reviews.yaml` complete
4. Set `passport.write_status: finalized`.
5. Log in `research/decision_log.md`; pipeline complete.

## Optional

- LaTeX / PDF — external tool or optional ARS install (see REFERENCES)
- Do not bundle NC ARS skills in template

## Handoff

Pipeline complete → human submission
