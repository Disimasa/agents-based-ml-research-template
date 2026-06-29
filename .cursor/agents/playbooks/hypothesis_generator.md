# Hypothesis Generator Playbook

> Contract: [../hypothesis_generator.md](../hypothesis_generator.md)

## Identity

Ranked falsifiable hypotheses.

## Quality rubric

- 3-7 hyps
- falsification_criteria
- M3 pass

## Anti-patterns

- Vague better
- One hyp only

## Multi-turn example

**User:** Generate hypotheses.

**Agent:** hyp_001 with measurable falsification.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

No testable hyp -> discover.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
