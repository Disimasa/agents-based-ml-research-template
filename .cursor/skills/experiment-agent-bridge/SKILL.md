---
name: experiment-agent-bridge
description: Optional bridge to experiment-agent (CC BY-NC) for run/validate modes
---

# Experiment-agent bridge

**Config:** `.cursor/orchestra/EXTERNAL_SKILLS.yaml` → `experiment_agent`  
**Upstream:** [experiment-agent](https://github.com/Imbad0202/experiment-agent) (CC BY-NC 4.0 — **opt-in only**, not bundled)

## When to use

- User explicitly installed experiment-agent (separate clone)
- Phase `execute` or `analyze`, task `reproducibility` / validation
- Modes: `plan`, `run`, `manage`, `validate` per upstream skill

## When NOT to use

- Default template workflow — use `run-experiment` + `analyze-results`
- User has not accepted NC license or cloned the repo

## Procedure

1. Confirm user opt-in (decision_log entry).
2. Read inputs from template:
   - `research/methodology.md`
   - `research/passport.yaml`
   - `research/experiment_provenance.yaml`
3. **plan** — delegate experiment design; merge with template `research-plan` if needed.
4. **run** — user-specified commands only (upstream safety rule); monitor; no auto-retry.
5. **validate** — statistical interpretation + reproducibility re-run; output `verification_status`:
   - `planned` | `analyzed` | `verified`
6. Write results to `research/experiment_provenance.yaml`:

```yaml
experiments:
  - experiment_id: exp_001
    status: completed
    verification_status: verified
    repro_lock:
      paths: ["outputs/..."]
    known_limitations: []
```

7. Run template gates: `integrity_check` M2 M4 M6; `orchestrate_pipeline.py gate`.

## Template fallback (no experiment-agent)

| Mode | Template skill |
|------|----------------|
| plan | `research-plan` |
| run | `run-experiment` |
| validate | `analyze-results` + `implementation_reviewer` |

## ARS position

Upstream fits between ARS Stage 1 and Stage 2. In this template: **execute → analyze** before `synthesize` / `write`.
