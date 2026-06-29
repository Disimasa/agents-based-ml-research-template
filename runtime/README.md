# Runtime

Internal template machinery. Users normally do not edit this tree.

| Path | Purpose |
|------|---------|
| `state/` | Agent pipeline state (YAML, benchmark JSON, literature outlines, revision log) |
| `state/benchmarks/` | Structured benchmark reports (M6) |
| `state/literature/{topic}/` | Literature search outline + fields (agent) |
| `schemas/` | JSON schemas for state files |
| `templates/` | Starters for literature, manuscript, summaries |
| `utils/` | Validation, integrity, pipeline, orchestra routing |
| `scripts/` | CLI (orchestrator, validate, integrity) |
| `tools/` | Maintainer utilities |

User-facing artifacts: `research/`, `src/`, `configs/`, `scripts/`, `reports/`.

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/validate_research.py
```
