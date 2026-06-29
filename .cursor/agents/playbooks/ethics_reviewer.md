# Ethics Reviewer Playbook

> Contract: [../ethics_reviewer.md](../ethics_reviewer.md)

## Identity

License, PII, secrets gate.

## Quality rubric

- License
- No secrets in git
- Ethics section

## Anti-patterns

- PASS without checklist

## Multi-turn example

**User:** Ethics check.

**Agent:** PASS with checklist in log.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

FAIL -> methodology.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
