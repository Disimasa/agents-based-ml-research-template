# Project bootstrap

Answer these when starting a new project from this template. Results feed `research/passport.yaml` and `research/research_state.yaml`.

## Research

1. Working title / topic:
2. Research question (one sentence):
3. Domain (ML / NLP / CV / other):

## Pipeline

4. Default mode: `hitl` | `autonomous`
5. Initial profile (pick one):

| Profile | Phases |
|---------|--------|
| `literature-only` | discover |
| `hypothesis-only` | discover → ideate → synthesize |
| `plan-only` | discover → ideate → plan |
| `execute-only` | execute → analyze |
| `research-no-code` | bootstrap → discover → ideate → plan → synthesize |
| `full-hitl` | full research track (through synthesize) |
| `full-autonomous` | same as full-hitl, autonomous mode |
| `full-publication` | research + manuscript → finalize |
| `publication-only` | write → finalize |
| `custom` | set `phases_enabled` manually |

6. Phases to enable (only if `custom`):

## Execution

7. Primary metric:
8. Logger: `wandb` | `csv` | `mlflow`
9. Use DVC for data? yes | no
10. Use Orchestra skills for execute/analyze? yes | no — if yes, agent installs only needed skills per [docs/ORCHESTRA_INSTALL.md](docs/ORCHESTRA_INSTALL.md)

**Shortcut:** If you want the agent to do everything including code, say so in one message (e.g. "full end-to-end research on topic X — develop and validate the best solution") — the agent applies `full-autonomous` automatically (see `.cursor/rules/full-autonomy-intent.mdc`).

---

## Apply profile (CLI)

After filling in, run:

```bash
uv run python scripts/orchestrate_pipeline.py apply-profile --name <profile>
uv run python scripts/orchestrate_pipeline.py status
```

Or ask the agent to run skill **`new-project`** (updates passport + state from your answers).

## Training code

Template does **not** ship a full training loop. On phase **execute**, you or your agent implement `src/train.py` and `src/modeling/`. Until then, experiments are logged as `blocked_stub` in provenance.
