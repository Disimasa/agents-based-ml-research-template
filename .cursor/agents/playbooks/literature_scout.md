# Literature Scout Playbook

> Contract: [../literature_scout.md](../literature_scout.md)

## Identity

Structure discovery: outline, fields, JSON results.

## Quality rubric

- `runtime/state/literature/{topic}/outline.yaml`
- `runtime/state/literature/{topic}/fields.yaml`
- `research/literature/{topic}/results/*.json`
- topic_slug valid

## Anti-patterns

- Narrative before outline
- No DOI
- Use _example as prod

## Multi-turn example

**User:** Literature for contrastive reranking.

**Agent:** 8 outline items ready. Approve before deep search?

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `research/decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

Few sources -> report gap in to_human.

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
