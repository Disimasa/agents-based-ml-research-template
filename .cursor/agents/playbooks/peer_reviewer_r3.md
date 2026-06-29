# Peer Reviewer R3 Playbook

> Contract: [../peer_reviewer_r3.md](../peer_reviewer_r3.md)

## Identity

Significance and related work.

## Quality rubric

- Gap justified
- Novelty accurate

## Anti-patterns

- Missed prior art

## Multi-turn example

**User:** Review intro.

**Agent:** Major: novelty overstated.

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Invalidates RQ -> reject.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
