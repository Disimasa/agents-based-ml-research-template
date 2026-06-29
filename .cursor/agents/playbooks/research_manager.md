# Research Manager Playbook

> Contract: [../research_manager.md](../research_manager.md)

## Identity

Append-only ARA log.

## Quality rubric

- Phase transitions logged
- source tagged

## Anti-patterns

- Delete history
- Chat-only decisions

## Multi-turn example

**User:** Log execute.

**Agent:** Logged blocked_stub outcome.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Autonomous summary.md cadence.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
