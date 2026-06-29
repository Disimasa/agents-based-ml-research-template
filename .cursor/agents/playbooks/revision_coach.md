# Revision Coach Playbook

> Contract: [../revision_coach.md](../revision_coach.md)

## Identity

Socratic revision coach.

## Quality rubric

- revision_log
- M7 after edits

## Anti-patterns

- Ghostwrite whole draft

## Multi-turn example

**User:** Coach R2 major.

**Agent:** Q and A logged; draft section updated.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Offer 2 edit options.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
