# Experiment Runner Playbook

> Contract: [../experiment_runner.md](../experiment_runner.md)

## Identity

Hydra + provenance; blocked_stub if needed.

## Quality rubric

- Provenance entry
- No fake metrics

## Anti-patterns

- Hide failures
- Undeclared runs

## Multi-turn example

**User:** Run exp_001.

**Agent:** blocked_stub logged honestly.

## Detailed procedure

0. **`orchestra-routing`:** `uv run python scripts/orchestra_route.py resolve execute train`.
1. Read `research/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `decision_log.md`.
4. Run `uv run python scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Repeat fail -> controller.

## Tools

```bash
uv run python scripts/orchestra_route.py resolve execute train
uv run python scripts/orchestrate_pipeline.py status
uv run python scripts/orchestrate_pipeline.py gate
uv run python scripts/integrity_check.py
uv run python scripts/validate_research.py
```
