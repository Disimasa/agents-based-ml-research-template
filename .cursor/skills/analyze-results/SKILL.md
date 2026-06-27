---
name: analyze-results
description: Analyze phase — aggregate runs into benchmark JSON and update provenance
---

# Analyze results

**Phase:** `analyze`  
**Agent:** `results_analyst`

## When to use

- After one or more experiments in provenance
- Phase `analyze` enabled

## Prerequisites

- `research/experiment_provenance.yaml`
- Run artifacts in `outputs/` or W&B
- `shared/schemas/benchmark_report.schema.json`
- **`orchestra-routing`** for `analyze` / `eval` (see SKILLS_MAP)

## Steps

### 0. Route (Orchestra or template)

```bash
uv run python scripts/orchestra_route.py resolve analyze eval
```

### 1. Collect metrics

- Read only from logs, W&B, or csv in `outputs/` — **never invent**
- If `status: blocked_stub`, report `not_executed` honestly

### 2. Write `reports/benchmarks/{experiment_id}.json`

Minimum fields per schema:

```json
{
  "experiment_id": "exp_001",
  "hypothesis_id": "hyp_001",
  "primary_metric": { "name": "...", "value": null, "status": "not_executed" },
  "baselines": [],
  "limitations": [],
  "negative_results": []
}
```

### 3. Update provenance

- Fill `negative_results`, `known_limitations`
- Set hypothesis `status: tested` when appropriate

### 4. Update passport claims

Only claims with `experiment_id` reference:

```yaml
claims:
  - statement: "..."
    experiment_id: exp_001
    evidence: reports/benchmarks/exp_001.json
```

### 5. Gate

- `integrity-check` M2, M4
- HITL: present benchmark table for human review

## Handoff

→ `synthesize` via `log-decision` + `integrity-check`
