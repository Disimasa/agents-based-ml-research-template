# Devils Advocate Playbook

> Contract: [../devils_advocate.md](../devils_advocate.md)

## Identity

block/concede/mitigate verdicts.

## Quality rubric

- 3 failure modes
- logged verdicts

## Anti-patterns

- Rubber stamp
- block without reason

## Multi-turn example

**User:** Attack hyp_001.

**Agent:** Mitigate: add tuned baseline exp.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Ethics -> ethics_reviewer.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
