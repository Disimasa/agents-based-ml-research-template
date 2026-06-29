---
name: hypothesis-ideation
description: Ideate phase — ranked falsifiable hypotheses with devil's advocate review
---

# Hypothesis ideation

**Phase:** `ideate`  
**Agents:** `hypothesis_generator`, `devils_advocate`

## When to use

- Phase `ideate` enabled
- After discover (or standalone if profile skips discover but has ideate — use passport question only)

## Prerequisites

- `runtime/state/passport.yaml`
- Literature artifacts (if discover ran)
- `runtime/schemas/hypotheses.schema.json`

## Steps

### 1. Generate (`hypothesis_generator`)

Edit `runtime/state/hypotheses.yaml`:

```yaml
hypotheses:
  - id: hyp_001
    statement: "Adding X improves Y on Z under condition C"
    falsification_criteria: "No significant improvement (p>0.05) on primary metric M"
    priority: 1
    status: proposed  # proposed | selected | rejected | tested
    source: ai
```

Produce 3–7 hypotheses mapped to literature gaps or novel extensions.

### 2. Ideation lenses (Orchestra-inspired)

Apply at least two:

- **Baseline gap** — beats obvious baseline?
- **Ablation** — which component matters?
- **Scale/data** — holds across scale?
- **Failure mode** — when does it break?

### 3. Devil's advocate (`devils_advocate`)

For each `proposed` hypothesis:

- List confounders, leakage risks, vague metrics
- Set `status: rejected` or add mitigation to `research/decision_log.md`
- **Block** if falsification criteria are not measurable

### 4. Selection

- **HITL:** human sets one hypothesis to `status: selected`
- **Autonomous:** select lowest `priority` number that passed DA

### 5. Update passport

- Sketch `planned_experiment_ids: [exp_001, ...]` (not executed yet)

### 6. Gate

- `integrity-check` M3
- HITL: `pending_approval: true` until selection confirmed

## Handoff

→ `research-plan` (plan) or back to ideate on autonomous pivot
