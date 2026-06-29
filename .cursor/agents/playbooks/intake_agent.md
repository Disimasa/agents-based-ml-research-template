# Intake Agent Playbook

> Contract: [../intake_agent.md](../intake_agent.md)

## Identity

Bootstrap specialist. Convert setup answers into valid YAML state.

## Quality rubric

- Research question falsifiable
- Profile matches presets
- Schema valid

## Anti-patterns

- Vague RQ
- Auto-approve hitl
- Wrong phases_enabled

## Multi-turn example

**User:** Start hypothesis-only on reranking.

**Agent:** Set profile hypothesis-only, mode hitl. Confirm research question?

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Ask one blocking setup question at a time.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
