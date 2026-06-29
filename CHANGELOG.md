# Changelog

All notable changes to this template. Format based on [Keep a Changelog](https://keepachangelog.com/).

## [0.2.0] - 2026-06-29

### Added

- **`runtime/` package** — orchestrator, validation, integrity, schemas, CLI, maintainer tools.
- **14-phase research + publication pipeline** with HITL and autonomous modes.
- **Orchestrator CLI** (`runtime/scripts/orchestrate_pipeline.py`): `status`, `gate`, `approve`, `advance`, `apply-profile`, `pipeline-profiles`.
- **Integrity checks M1–M7** with ARS-inspired gates 2.5 (`integrity_pre_review`) and 4.5 (`integrity_final`).
- **16 Cursor skills** and **21 agent contracts** (+ playbooks) for bootstrap → finalize.
- **Orchestra bridge** — opt-in routing via `.cursor/orchestra/SKILLS_MAP.yaml` and `runtime/scripts/orchestra_route.py`.
- **Publication track** — manuscript draft, peer review, revision coaching, finalize.
- **Profile presets** in `runtime/state/pipeline_profiles.yaml` (`hypothesis-only`, `full-hitl`, `full-autonomous`, `full-publication`, …).
- **JSON schemas** under `runtime/schemas/` for state YAML and benchmark reports.
- **Autonomous preflight** guardrails (`metric_primary`, `research_question`, iteration budgets).
- **Tests** (26) for orchestrator, pipeline profiles, integrity, orchestra routing.
- **User directories** with README stubs: `research/`, `scripts/`, `reports/`, `data/`.

### Changed

- **User vs agent split:**
  - **User-facing:** `research/` (methodology, decision log, literature results, manuscript draft, `to_human/`), `src/`, `configs/`, `scripts/`, `reports/`.
  - **Agent state:** `runtime/state/` (passport, research_state, pipeline, hypotheses, provenance, benchmarks, literature outlines, manuscript reviews, revision log).
  - **Templates:** `runtime/templates/` (literature example, manuscript draft, summary).
- **Benchmark JSON** moved from `reports/benchmarks/` to `runtime/state/benchmarks/`.
- **Literature agent files** (`outline.yaml`, `fields.yaml`) → `runtime/state/literature/{topic}/`; user keeps `research/literature/{topic}/results/`.
- **CLI entry points** live under `runtime/scripts/` (no root `scripts/` wrappers).
- **AGENTS.md**, rules, skills, and agents aligned to `runtime/state/` and `research/` paths.
- **`validate_research.py`** validates `STATE_FILES` in `runtime/state/`.
- **Third-party attributions** consolidated in `docs/REFERENCES.md` (removed redundant `NOTICE.md`).

### Removed

- Root `scripts/` compatibility wrappers (`orchestrate_pipeline`, `validate_*`, `integrity_check`, `orchestra_route`).
- `src/utils/` pipeline shims (orchestrator code lives in `runtime/utils/`).
- `shared/schemas/` (→ `runtime/schemas/`).
- Pipeline state YAML from root `research/` (→ `runtime/state/`).
- `NOTICE.md` (attributions in `docs/REFERENCES.md`).
- `experiment-agent-bridge` skill, `EXTERNAL_SKILLS.yaml`, and `execute_validate` Orchestra route (architecture credit only in REFERENCES).

## [0.1.0] - 2026-06-27

### Added

- Initial CCDS + Hydra layout (`src/`, `configs/`, `data/`).
- Research AI layer skeleton: rules, skills, agents, `research/` placeholders.
- `setup.md` bootstrap questionnaire.
- Hydra train/eval entry points (scaffold).
