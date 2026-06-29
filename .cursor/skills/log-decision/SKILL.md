---
name: log-decision
description: Synthesize phase — decision log and passport sync
---

# Log decision

**Phase:** `synthesize`  
**Agents:** `integrity_auditor`, `synthesis_agent`, `research_manager`

## When to use

- End of a phase or full pipeline
- After analyze or hypothesis-only profiles that end at synthesize

## Prerequisites

- Phase artifacts for completed phases
- `research/decision_log.md` (append-only)

## Steps

### 1. Summarize outcomes

For each completed phase, append:

```markdown
## YYYY-MM-DD — synthesize

- **profile:** hypothesis-only
- **phases completed:** discover, ideate, synthesize
- **selected hypothesis:** hyp_001 | none
- **experiments:** none | exp_001 ...
- **integrity:** PASS | FAIL (modes: ...)
- **next steps:** ...
- **source:** ai
```

### 2. Sync passport

- `passport.phase: synthesize` (or final phase)
- Reconcile `claims[]` with literature + provenance
- Set `experiment_intake_declaration` accurately

### 3. Autonomous human digest

If `mode: autonomous`, write `research/to_human/summary.md`:

```markdown
# Research summary

## Question
...

## Key decisions
...

## Results (honest)
...

## Open risks
...
```

### 4. Final gate

- Run full `integrity-check` (M1–M5)
- HITL: `pending_approval: true` until human closes pipeline
- Autonomous: mark pipeline done in `runtime/state/research_state.yaml` (`current_phase: done` — use comment in state if schema lacks field)

## Handoff

Pipeline complete → user review. Optional Phase 7 `write` deferred (external ARS).
