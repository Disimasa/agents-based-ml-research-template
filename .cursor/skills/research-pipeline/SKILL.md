---
name: research-pipeline
description: Meta orchestrator — route modular phases by profile and mode (hitl or autonomous)
---

# Research pipeline (orchestrator)

**Phase:** meta  
**Agent:** `pipeline_orchestrator`

## When to use

- User invokes `/research-pipeline` or asks to run full/partial research workflow
- User asks to **do everything / develop solution / full research with code** → rule `full-autonomy-intent` → `full-autonomous` + autonomous (apply immediately)
- Need to switch profile or resume from `current_phase`

## Full autonomy (no profile question)

If the user message matches `full-autonomy-intent` (see `.cursor/rules/full-autonomy-intent.mdc`):

```bash
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-autonomous
```

Set `mode: autonomous`, fill `research_question` and `autonomous.metric_primary`, then run phases until synthesize. On execute use `autonomous-loop`. Log to `research/to_human/summary.md`.

## Invocation

```text
/research-pipeline --profile hypothesis-only
/research-pipeline --profile full-hitl
/research-pipeline --profile full-autonomous --mode autonomous
/research-pipeline --profile full-publication
/research-pipeline --profile publication-only

## Startup

1. Read `runtime/state/research_state.yaml`, `runtime/state/pipeline.yaml`, `runtime/state/pipeline_profiles.yaml`
2. Run `uv run python runtime/scripts/orchestrate_pipeline.py status`
3. Resolve profile → `phases_enabled[]`
4. Confirm `mode` (`hitl` | `autonomous`)
5. Find `current_phase` in enabled list

## Orchestrator CLI

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status    # where am I?
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-hitl
uv run python runtime/scripts/orchestrate_pipeline.py pipeline-profiles
uv run python runtime/scripts/orchestrate_pipeline.py gate      # schema + phase-aware M1–M7
uv run python runtime/scripts/orchestrate_pipeline.py approve --by human
uv run python runtime/scripts/orchestrate_pipeline.py advance   # next phase (after gate PASS)
```

After `advance`, invoke the printed skill + agent for the new phase.

## Phase router

| Order | Phase | Skill | Lead agent |
|-------|-------|-------|------------|
| 0 | bootstrap | new-project | intake_agent |
| 1 | discover | literature-survey | literature_scout |
| 2 | ideate | hypothesis-ideation | hypothesis_generator |
| 3 | plan | research-plan | methodology_critic |
| 4 | execute | orchestra-routing → run-experiment **or** autonomous-loop | experiment_runner / autonomous_controller |
| 5 | analyze | orchestra-routing → analyze-results | results_analyst |
| 6 | synthesize | log-decision + integrity-check | integrity_auditor |
| 7 | write | manuscript-draft | manuscript_writer |
| 8 | integrity_pre_review | integrity-check (**gate 2.5**, M1–M7) | integrity_auditor |
| 9 | review | peer-review | editor_in_chief + R1–R3 |
| 10 | revise | revision-coaching | revision_coach |
| 11 | re_review | peer-review | editor_in_chief |
| 12 | integrity_final | integrity-check (**gate 4.5**, M1–M7) | integrity_auditor |
| 13 | finalize | manuscript-finalize | manuscript_writer |

Skip phases not in `phases_enabled`.

## Orchestra routing (execute / analyze)

Before invoking phase skill for **execute** or **analyze**:

1. Skill **`orchestra-routing`** (read `.cursor/orchestra/SKILLS_MAP.yaml`).
2. `uv run python runtime/scripts/orchestra_route.py resolve <phase> <task>`  
   - execute → `train` or `train_autonomous`  
   - analyze → `eval`
3. Use resolved Orchestra skill or `template_fallback` from the map.

## Advance protocol

After each phase:

1. Run `integrity-check` (micro-gate)
2. **HITL** (`pipeline-mode` rule):
   - Set `pending_approval: true`
   - **STOP** — do not call next phase skill until `approved_by: human` in `runtime/state/research_state.yaml`
3. **Autonomous**:
   - If gate PASS: `approved_by: ai`, `pending_approval: false`, advance
   - On execute: delegate to `autonomous-loop` until stop conditions

## State updates

```yaml
# runtime/state/research_state.yaml
current_phase: ideate
pending_approval: true
approved_by: null
approved_at: null
```

On approval:

```yaml
pending_approval: false
approved_by: human  # or ai
approved_at: "2026-06-27T12:00:00Z"
current_phase: plan  # next enabled phase
```

Sync `runtime/state/passport.yaml` → `phase: <current_phase>`.

## Profile quick reference

| Profile | Phases | Mode |
|---------|--------|------|
| literature-only | discover | hitl |
| hypothesis-only | discover → ideate → synthesize | hitl |
| plan-only | discover → ideate → plan | hitl |
| execute-only | execute → analyze | hitl |
| research-no-code | bootstrap → discover → ideate → plan → synthesize | hitl |
| full-hitl | research track (through synthesize) | hitl |
| full-autonomous | research track | autonomous |
| full-publication | research + publication (through finalize) | hitl |
| publication-only | write → finalize only | hitl |
| custom | `phases_enabled: [...]` | either |

## Delegation

Use Cursor **Task** tool with subagent when a phase needs deep work:

- discover → explore/literature agent
- ideate → generalPurpose + hypothesis_generator context
- execute → shell agent for `uv run` (when code exists)

Pass each subagent: current `runtime/state/research_state.yaml`, phase skill path, relevant agent `.md`.

## Logging

Every phase transition → `research_manager` entry in `research/decision_log.md`.

## Do not

- Auto-advance in HITL without `approved_by: human`
- Skip integrity gate
- Auto-commit (any mode)
