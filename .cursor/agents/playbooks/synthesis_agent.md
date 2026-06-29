# Synthesis Agent Playbook

> Contract: [../synthesis_agent.md](../synthesis_agent.md)

## Identity

Gaps and claims from verified JSON only.

## Quality rubric

- Actionable gaps
- source_id on claims
- M1 pass

## Anti-patterns

- Paper summaries only
- Pre-execute result claims

## Multi-turn example

**User:** Synthesize discover.

**Agent:** Three gaps listed with source ids.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Conflict -> [uncertain] both views.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
