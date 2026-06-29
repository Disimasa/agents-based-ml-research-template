---
name: revision-coaching
description: Revise phase — Socratic responses to peer review
---

# Revision coaching

**Phase:** `revise` | **Agent:** `revision_coach`

## Prerequisites

- `editorial_decision.decision` is `minor_revision` or `major_revision`
- `runtime/state/manuscript_reviews.yaml` round N complete

## Socratic protocol

For each **major_point**:

1. Restate the reviewer's concern in one sentence.
2. Ask the author (human) one clarifying question.
3. Propose a concrete edit OR experiment tag fix (`experiment_id`).
4. Log in `runtime/state/manuscript_revision_log.md`:

```markdown
### Round 1 — point 1
- **reviewer:** R2
- **concern:** baseline unfair
- **coach_question:** Did we tune baseline learning rate?
- **resolution:** Added exp_002 baseline tune; tagged in draft.
```

## Steps

1. Triage major before minor points.
2. Update `research/manuscript/draft.md` section by section.
3. Re-run `uv run python runtime/scripts/integrity_check.py --modes M4 M6 M7`.
4. HITL: human approves revision batch.
5. Advance to `re_review`.

## Handoff

→ `peer-review` (`re_review`)
