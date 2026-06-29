---
name: integrity-check
description: Micro-gate — 7-mode integrity verification (M1–M7) with ARS gates 2.5 and 4.5
---

# Integrity check

**Phase:** gate (after every phase; required before advance)  
**Agent:** `integrity_auditor`  
**Playbook:** `.cursor/agents/playbooks/integrity_auditor.md`

## When to use

- Before `pipeline_orchestrator` advances `current_phase`
- At **`integrity_pre_review`** (ARS gate **2.5**) — full M1–M7
- At **`integrity_final`** (ARS gate **4.5**) — full M1–M7
- After `analyze` or before `synthesize` — default M1–M5

## Automated execution (required)

```bash
uv run python runtime/scripts/validate_research.py
uv run python runtime/scripts/integrity_check.py --phase integrity_pre_review  # gate 2.5
uv run python runtime/scripts/integrity_check.py --phase integrity_final       # gate 4.5
uv run python runtime/scripts/orchestrate_pipeline.py gate
```

Default research phases: `uv run python runtime/scripts/integrity_check.py` (M1–M5 via profile).

## Seven modes

| Mode | Check |
|------|--------|
| M1 | Literature claims → verified `results/*.json` |
| M2 | No fabricated metrics |
| M3 | Falsifiable hypotheses |
| M4 | Results claims → `runtime/state/experiment_provenance.yaml` |
| M5 | Methodology ↔ `configs/` ↔ `src/` |
| M6 | `runtime/state/benchmarks/*.json` schema + honest_comparison_notes |
| M7 | `research/manuscript/draft.md` ↔ passport + provenance |

## Gate profiles

| Profile | Phases | Modes |
|---------|--------|-------|
| `research_default` | bootstrap…synthesize | M1–M5 |
| `gate_2_5_pre_review` | `integrity_pre_review` | M1–M7 |
| `gate_4_5_final` | `integrity_final` | M1–M7 |
| `publication_light` | review, re_review, finalize | M4, M6, M7 |

List profiles: `uv run python runtime/scripts/orchestrate_pipeline.py profiles`

## Retry policy

- HITL: max 3 FAIL retries per phase; human override in `research/decision_log.md`
- Autonomous: one auto-fix; then `research/to_human/integrity_fail.md`

## Handoff

PASS → `orchestrate_pipeline.py advance` | FAIL → phase owner
