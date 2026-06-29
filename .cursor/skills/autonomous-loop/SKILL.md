---
name: autonomous-loop
description: Execute phase (autonomous) — inner optimization loop with stop conditions
---

# Autonomous loop

**Phase:** `execute`  
**Agents:** `autonomous_controller`, `experiment_runner`, `implementation_reviewer`, `results_analyst`  
**Mode:** `autonomous` only

## When to use

- `runtime/state/research_state.yaml` → `mode: autonomous`
- Profile `full-autonomous` or custom with execute + autonomous settings

## Prerequisites

- Approved plan (autonomous may auto-approve if integrity PASS)
- `autonomous.max_iterations`, `metric_primary` set in `runtime/state/research_state.yaml`
- **`orchestra-routing`** for `execute` / `train_autonomous` (see SKILLS_MAP)

## Stop conditions

Stop when any:

1. `max_iterations` exhausted
2. `max_wall_time_hours` exceeded
3. `stop_on_plateau` runs without improvement on `metric_primary`
4. Integrity FAIL × 3 on same phase
5. User sets `mode: hitl` or `force_hitl: true`

## Inner loop

```
while not stopped:
  0. orchestra-routing → execute/train_autonomous
  1. autonomous_controller selects active hypothesis
  2. experiment_runner → Hydra run (or log blocked_stub)
  3. implementation_reviewer → PASS/FAIL
  4. results_analyst → metric vs baseline
  5. if improved: keep, log to .lab/
     else: revert, pivot hypothesis or call devils_advocate
  6. append research/to_human/summary.md every N iterations
```

## `.lab/` (opt-in, gitignored)

Create `.lab/research-log.md`:

```markdown
## Iteration N
- hypothesis: hyp_001
- experiment: exp_00X
- metric: ...
- decision: keep|revert|pivot
```

## Constraints

- **No auto-commit** (see `git-safety` rule)
- **No blocking AskUser** unless `force_hitl: true`
- Log every iteration via `research_manager`

## Handoff

On stop → `analyze-results` → `log-decision` / `integrity-check` → `research/to_human/summary.md`
