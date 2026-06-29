---
name: peer-review
description: Review and re_review phases — R1–R3 peer review + EIC decision
---

# Peer review

**Phases:** `review`, `re_review` | **Agents:** `peer_reviewer_r1`, `peer_reviewer_r2`, `peer_reviewer_r3`, `editor_in_chief`

## Prerequisites

- Gate 2.5 PASS (`integrity_pre_review` complete)
- `research/manuscript/draft.md`

## Steps

### Round 1 (`review`)

1. **EIC** dispatches three parallel reviews:
   - R1: methods / reproducibility (M4, M5)
   - R2: experiments / benchmarks (M6)
   - R3: significance / literature (M1)
2. Each reviewer appends to `runtime/state/manuscript_reviews.yaml`:

```yaml
reviews:
  - round: 1
    reviewer_id: R1
    role: peer_reviewer_r1
    recommendation: major_revision
    summary: "..."
    major_points: ["..."]
    minor_points: ["..."]
```

3. **EIC** sets `editorial_decision` with `decision`, `round`, `decided_by: editor_in_chief`.
4. HITL: human confirms editorial decision.

### Round 2+ (`re_review`)

- After `revise` + `runtime/state/manuscript_revision_log.md` updates
- R1–R3 check only prior major points
- EIC updates decision; accept → `integrity_final`

## Anti-patterns

- Accept with open M6/M7 failures
- Reviews without reading `research/manuscript/draft.md` and provenance

## Handoff

accept → `integrity_final` (gate 4.5) | major/minor → `revision-coaching`
