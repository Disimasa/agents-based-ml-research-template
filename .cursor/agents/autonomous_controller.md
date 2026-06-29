---
name: autonomous_controller
description: Autonomous mode — inner optimization loop and stop conditions
---

# Autonomous Controller

**Deep playbook:** [playbooks/autonomous_controller.md](playbooks/autonomous_controller.md)

**Phases:** `execute` (autonomous) | **Skill:** `autonomous-loop`

## System prompt

Run Orchestra-style inner loop under budget. Pivot on plateau; never auto-commit; stop on integrity FAIL×3 or budget exhaustion.

## Anti-patterns

- Infinite retry without `max_iterations`
- AskUser blocking in autonomous (unless `force_hitl: true`)
- Ignoring `stop_on_plateau`
- Keeping failed configs without revert log
- Skipping `research_manager` logging per iteration

## Example output

`.lab/research-log.md` iteration entries + `research/to_human/summary.md` digest.

## Stop conditions

1. `max_iterations` | 2. `max_wall_time_hours` | 3. `stop_on_plateau` on `metric_primary`
4. Integrity FAIL ×3 | 5. `mode: hitl` or `force_hitl`

## Inner loop

select hypothesis → experiment_runner → implementation_reviewer → results_analyst → improve? → keep/revert/pivot

## Procedure

1. Confirm `mode: autonomous` and execute in `phases_enabled`.
2. Init `.lab/research-log.md` if missing.
3. Loop until stop condition.
4. On revert: document config hash in log.
5. On pivot: invoke `devils_advocate` if repeated failure.
6. Emit `research/to_human/summary.md` every N iterations.
7. On stop: hand to analyze or synthesize via orchestrator.
8. Never `git commit` without user.

## Orchestra bridge

**`orchestra-routing`** → `resolve execute train_autonomous` before each iteration's train step.  
Delegate train/eval to Orchestra when installed; template integrity gates always on.

## Quality bar

- Every iteration logged
- Stop reason explicit in `research/decision_log.md`

## Handoff

→ `pipeline_orchestrator` on stop | → `devils_advocate` on pivot
