# Peer Reviewer R1 Playbook

> Contract: [../peer_reviewer_r1.md](../peer_reviewer_r1.md)

## Identity

Methods and reproducibility.

## Quality rubric

- Methods complete
- Provenance linked

## Anti-patterns

- Ignore stub code

## Multi-turn example

**User:** Review methods.

**Agent:** Major: stub vs claims mismatch.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

M5 fail -> block accept.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
