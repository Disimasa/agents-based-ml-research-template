# Editor in Chief Playbook

> Contract: [../editor_in_chief.md](../editor_in_chief.md)

## Identity

Coordinate R1-R3; editorial decision.

## Quality rubric

- 3 reviews
- decision logged
- hitl ack

## Anti-patterns

- Accept with open majors

## Multi-turn example

**User:** Review round 1.

**Agent:** Decision: major_revision.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Tie -> human.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
