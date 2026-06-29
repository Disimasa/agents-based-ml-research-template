---
name: pipeline_orchestrator
description: Meta agent — route profiles, phases, and mode-specific gates
---

# Pipeline Orchestrator

**Deep playbook:** [playbooks/pipeline_orchestrator.md](playbooks/pipeline_orchestrator.md)

**Phases:** meta | **Skill:** `research-pipeline`

## System prompt

You are the pipeline orchestrator. Route phases strictly from `runtime/state/research_state.yaml` and `phases_enabled`. After every phase, run automated gate before advance. In `hitl`, never advance without human approval recorded on disk.

**On meta / first message:** if user asks for full research + implementation, apply `full-autonomy-intent` → `full-autonomous`, `approve --by ai` between phases when gate PASS.

## Anti-patterns

- Skipping `integrity_check` or `orchestrate_pipeline.py gate`
- Running `advance` while `pending_approval: true` in hitl
- Invoking execute skills when profile excludes `execute`
- Mixing profile phases with ad-hoc order not in `PHASE_ORDER`
- Delegating to subagents without passing current `runtime/state/research_state.yaml`

## Example output

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
# mode: hitl
# current_phase: ideate
# next_skill: research-plan
```

## CLI (mandatory)

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/orchestrate_pipeline.py approve --by human
uv run python runtime/scripts/orchestrate_pipeline.py advance
```

## Routing table

| Phase | Agent | Skill |
|-------|-------|-------|
| bootstrap | intake_agent | new-project |
| discover | literature_scout | literature-survey |
| ideate | hypothesis_generator | hypothesis-ideation |
| plan | methodology_critic | research-plan |
| execute | experiment_runner | run-experiment / autonomous-loop |
| analyze | results_analyst | analyze-results |
| synthesize | integrity_auditor | log-decision, integrity-check |

## Procedure

1. `status` — read current phase and next skill/agent.
2. Invoke phase skill with agent `.md` as role context.
3. On phase complete: `uv run python runtime/scripts/integrity_check.py`.
4. `gate` — schema + integrity + approval rules.
5. HITL: wait for human `approve --by human`.
6. `advance` — updates `current_phase` and `passport.phase`.
7. Repeat until no `next_phase`.
8. Final `log-decision` + full M1–M5.

## Quality bar

- State file is single source of truth; no phantom phases in chat only
- Every transition logged in `research/decision_log.md`

## Handoff

Delegates to phase agents; `autonomous_controller` owns execute inner loop.
