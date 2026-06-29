---
name: run-experiment
description: Execute phase (HITL) — single Hydra experiment with provenance logging
---

# Run experiment

**Phase:** `execute`  
**Agents:** `experiment_runner`, `implementation_reviewer`  
**Mode:** primarily `hitl` (one run per approval)

## When to use

- Human-approved experiment from `methodology.md`
- Phase `execute` enabled, `mode: hitl`

## Prerequisites

- `research/methodology.md` with `experiment_id`
- Matching `configs/experiment/<name>.yaml`
- `uv sync --extra torch` (or `--extra ml` for W&B)
- Run **`orchestra-routing`** first (see `.cursor/orchestra/SKILLS_MAP.yaml`)

## Steps

### 0. Route (Orchestra or template)

```bash
uv run python runtime/scripts/orchestra_route.py resolve execute train
```

- If Orchestra skill available → follow `.cursor/skills/orchestra/<name>/SKILL.md`
- Else → continue with template steps below

### 1. Pre-flight

- Confirm `experiment_intake_declaration: experiments_declared`
- Confirm hypothesis `status: selected`
- If `src/train.py` is stub: log blocker in provenance — **do not fabricate metrics**

### 2. Run

```bash
uv run python src/train.py experiment=<name> logger=csv
# W&B: uv sync --extra wandb && logger=wandb
```

Hydra outputs → `outputs/` (gitignored).

### 3. Record provenance

Append to `runtime/state/experiment_provenance.yaml`:

```yaml
experiments:
  - experiment_id: exp_001
    hydra_config: configs/experiment/<name>.yaml
    wandb_run_id: null
    repro_lock:
      paths: ["outputs/..."]
    planned_vs_executed:
      - planned: exp_001
        executed: true
    negative_results: []
    known_limitations: []
    status: completed  # planned | running | completed | failed | blocked_stub | not_executed
    verification_status: analyzed  # planned | analyzed | verified (integrity / implementation_reviewer)
```

### 4. Implementation review

`implementation_reviewer` checklist: seeds, metric match, no leakage.

### 5. Gate

- HITL: one run per approval; update `pending_approval` between runs
- Log via `research_manager` → `research/decision_log.md`

## Handoff

→ `analyze-results`
