# Autonomous Controller Playbook

> Contract: [../autonomous_controller.md](../autonomous_controller.md)

## Identity

Inner loop under budget.

## Quality rubric

- .lab log
- stop documented

## Anti-patterns

- Infinite loop
- auto-commit

## Multi-turn example

**User:** Autonomous execute.

**Agent:** Stop: plateau x3.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

integrity FAIL x3 -> hitl.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
