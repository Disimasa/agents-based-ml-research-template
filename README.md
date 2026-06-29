# ml-research-template

CCDS + Hydra + modular AI research pipeline for Cursor.

- **AI entry:** [AGENTS.md](AGENTS.md)
- **Research state:** [research/README.md](research/README.md)
- **Optional Orchestra skills:** [docs/ORCHESTRA_INSTALL.md](docs/ORCHESTRA_INSTALL.md)
- **Template runtime:** [runtime/README.md](runtime/README.md) — orchestrator, schemas, validation (internal)

## Quick start

```bash
uv sync
uv sync --group dev   # ruff, pytest, validate
```

### 1. Bootstrap research

1. Fill [setup.md](setup.md) (research question, profile, mode).
2. In Cursor: ask the agent to run skill **`new-project`**, or apply a profile directly:

```bash
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name hypothesis-only
uv run python runtime/scripts/orchestrate_pipeline.py status
```

### 2. Run the pipeline

```bash
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/orchestrate_pipeline.py approve --by human
uv run python runtime/scripts/orchestrate_pipeline.py advance
```

After `advance`, invoke the printed skill + agent for the new phase (or ask the AI: `/research-pipeline`).

### 3. Profiles

```bash
uv run python runtime/scripts/orchestrate_pipeline.py pipeline-profiles
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-hitl
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-publication
```

Presets live in `runtime/state/pipeline_profiles.yaml`.

### One-shot full research (autonomous)

In Cursor you can say:

> Full research on [topic]. Develop and validate the best solution.

The agent applies rule `full-autonomy-intent` → profile `full-autonomous`, mode `autonomous` — no need to name the profile. See [AGENTS.md](AGENTS.md).

## Training code (user / agent)

`src/train.py` and `src/modeling/` are **scaffolds** — you (or your agent) implement training on the **execute** phase.

- Hydra configs: `configs/train.yaml`, `configs/experiment/*.yaml`
- Skill: `.cursor/skills/run-experiment/SKILL.md`
- If code is not ready: log `status: blocked_stub` in `runtime/state/experiment_provenance.yaml` — never fabricate metrics

Optional ML stack:

```bash
uv sync --extra torch
uv sync --extra ml          # torch + wandb
uv sync --extra mlflow
```

## Orchestra (optional)

External MIT skills for W&B, PEFT, lm-eval, etc. — not bundled. Install **per task** when the agent needs them; see [docs/ORCHESTRA_INSTALL.md](docs/ORCHESTRA_INSTALL.md).

```bash
uv run python runtime/scripts/orchestra_route.py list
```

## Validate & integrity

```bash
uv run python runtime/scripts/validate_research.py
uv run python runtime/scripts/integrity_check.py --phase integrity_pre_review
uv run ruff check src tests runtime
uv run pytest tests -q
```

## License

MIT — [LICENSE](LICENSE). Third-party attributions: [docs/REFERENCES.md](docs/REFERENCES.md).
