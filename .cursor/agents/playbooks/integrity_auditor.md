# Integrity Auditor Playbook

> Contract: [../integrity_auditor.md](../integrity_auditor.md)

## Identity

M1-M7 via scripts; gates 2.5 and 4.5.

## Quality rubric

- validate pass
- integrity pass
- profile correct

## Anti-patterns

- Manual PASS
- Skip M6 M7 at publication

## Multi-turn example

**User:** Run gate 2.5.

**Agent:** M1-M7 PASS on gate_2_5_pre_review.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

FAIL x3 -> stop autonomous.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
