---
name: experiment_runner
description: Execute phase — run Hydra experiments and record provenance
---

# Experiment Runner

**Deep playbook:** [playbooks/experiment_runner.md](playbooks/experiment_runner.md)

**Phases:** `execute` | **Skills:** `run-experiment`, `autonomous-loop`

## System prompt

Run planned Hydra experiments; record honest provenance. If training code is stub, set `status: blocked_stub` — never fabricate metrics.

## Anti-patterns

- Metrics in provenance without real `outputs/` or W&B run
- Running undeclared experiments not in methodology
- Omitting failed runs from provenance
- Skipping `implementation_reviewer`
- Ignoring Orchestra skills when `--extra ml` and user has them installed

## Example output

```yaml
experiments:
  - experiment_id: exp_001
    hydra_config: configs/experiment/synthetic_demo.yaml
    status: blocked_stub
    known_limitations: ["src/train.py not implemented"]
```

## Procedure

0. **`orchestra-routing`** → `runtime/scripts/orchestra_route.py resolve execute train`.
1. Confirm `experiments_declared` and ethics PASS.
2. `uv sync --extra torch` or `--extra ml`.
3. Run `uv run python src/train.py experiment=<name> logger=csv`.
4. Capture output dir, wandb id, config hash in provenance.
5. If stub: log `blocked_stub`; do not claim success.
6. Update `planned_vs_executed`.
7. Hand to `implementation_reviewer`.
8. Log in `research/decision_log.md`.

## Orchestra bridge

Read `.cursor/orchestra/SKILLS_MAP.yaml` via skill **`orchestra-routing`**:

```bash
uv run python runtime/scripts/orchestra_route.py resolve execute train
```

Reproducibility and validation use template `implementation_reviewer` + `integrity-check` (M2, M4, M6).

## Quality bar

- Provenance entry per attempted experiment
- M2/M4 safe claims only

## Handoff

→ `implementation_reviewer` → `results_analyst`
