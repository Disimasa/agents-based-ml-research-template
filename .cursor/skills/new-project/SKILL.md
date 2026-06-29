---
name: new-project
description: Bootstrap phase — initialize research state; maps full-autonomy user intent to full-autonomous profile
---

# New project (bootstrap)

**Phase:** `bootstrap`  
**Agent:** `intake_agent`

## When to use

- Fresh fork of the template
- User says "start research", "new project", or completes `setup.md`
- User asks for **full end-to-end research + implementation** → see rule `full-autonomy-intent` → `full-autonomous` (skip asking profile)
- Profile includes `bootstrap` phase

## Intent → profile (before step 1)

| User intent | Profile | Mode |
|-------------|---------|------|
| End-to-end + develop / train / implement | `full-autonomous` | `autonomous` |
| Research track, human approves each phase | `full-hitl` | `hitl` |
| Hypotheses only, no code | `hypothesis-only` | `hitl` |
| Manuscript only | `publication-only` | `hitl` |
| Research + paper | `full-publication` | `hitl` |

If triggers match `full-autonomy-intent`, run `apply-profile --name full-autonomous` and set `mode: autonomous` without prompting.

## Steps

**Prerequisites:** `setup.md`, `runtime/state/pipeline_profiles.yaml`, `runtime/schemas/passport.schema.json`.

1. **Detect intent** (rule `full-autonomy-intent`). If full end-to-end + code → `apply-profile --name full-autonomous`, `mode: autonomous`, skip profile question.
2. **Collect inputs** (from user message or `setup.md`):
   - Working title / research question
   - `mode`: `hitl` | `autonomous`
   - `pipeline_profile`: e.g. `hypothesis-only`, `full-hitl`, `full-autonomous`, `custom`
   - Primary metric, logger preference, DVC yes/no

3. **Resolve profile** — prefer CLI when intent is clear:
   ```bash
   uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-autonomous
   ```
   Or copy `mode` and `phases` into `runtime/state/pipeline.yaml` and `phases_enabled` in `runtime/state/research_state.yaml`.

3. **Write `runtime/state/passport.yaml`:**
   ```yaml
   research_question: "<one sentence>"
   phase: bootstrap
   claims: []
   planned_experiment_ids: []
   experiment_intake_declaration: no_experiments_declared
   ```

4. **Write `runtime/state/research_state.yaml`:**
   ```yaml
   mode: hitl  # or autonomous
   pipeline_profile: <profile>
   phases_enabled: [...]
   current_phase: bootstrap
   pending_approval: true
   approved_by: null
   approved_at: null
   autonomous:
     max_iterations: 20
     max_wall_time_hours: 8
     metric_primary: null
     stop_on_plateau: 3
   ```

5. **Log** in `research/decision_log.md` with `source: user|ai`.

6. **Gate:**
   - HITL: stop; ask human to confirm passport → set `approved_by: human`, `pending_approval: false`
   - Autonomous: set `approved_by: ai`, advance `current_phase` to first enabled phase

7. **Handoff** to `research-pipeline` or `literature-survey` / next phase skill.

## Do not

- Run experiments in bootstrap
- Commit secrets or fill fake metrics
