# AGENTS.md

Entry point for AI assistants: repository map, pipeline, agents. Rules — `.cursor/rules/`, workflows — `.cursor/skills/`, roles — `.cursor/agents/` (+ [playbooks](.cursor/agents/playbooks/)).

## Layout

| Path | Purpose |
|------|---------|
| `research/` | Your research artifacts — [research/README.md](research/README.md) |
| `scripts/` | Your helper scripts (data prep, batch runs) |
| `configs/` | Hydra configs |
| `src/modeling/` | Training code (stub until user/agent implements on execute) |
| `runtime/state/` | Agent pipeline state (YAML — not user-facing) |
| `runtime/templates/` | Starters for literature, manuscript, summaries |
| `runtime/schemas/` | JSON schemas for state YAML |
| `runtime/scripts/` | Orchestrator CLI, integrity, validate, orchestra route |
| `runtime/tools/` | Maintainer utilities (playbook generator) |
| `runtime/utils/` | Shared runtime libraries |
| `.cursor/rules/` | 13 governance rules (incl. `full-autonomy-intent`) |
| `.cursor/skills/` | 16 skills (research + publication + orchestra bridge) |
| `.cursor/orchestra/` | SKILLS_MAP + EXTERNAL_SKILLS (Orchestra opt-in routing) |
| `.cursor/agents/` | 21 agent contracts + playbooks |

## Research + publication pipeline

### Modes

| Mode | Behavior |
|------|----------|
| `hitl` | `pending_approval` + `approved_by: human` between phases |
| `autonomous` | auto-advance on PASS gate; inner loop on execute; preflight guardrails |

### Full autonomy intent ("do everything + develop")

Rule **`.cursor/rules/full-autonomy-intent.mdc`** (always on): agent **does not ask for profile** — sets `full-autonomous` + `mode: autonomous`, writes code on execute, logs to `research/to_human/summary.md`. Exception: paper only without code → `publication-only` / `full-publication` (hitl at review).

### Phases (14)

| Phase | Skill | Agent(s) |
|-------|-------|----------|
| bootstrap | new-project | intake_agent |
| discover | literature-survey | literature_scout |
| ideate | hypothesis-ideation | hypothesis_generator |
| plan | research-plan | methodology_critic |
| execute | **orchestra-routing** → run-experiment / autonomous-loop | experiment_runner |
| analyze | **orchestra-routing** → analyze-results | results_analyst |
| synthesize | log-decision, integrity-check | integrity_auditor |
| write | manuscript-draft | manuscript_writer |
| integrity_pre_review | integrity-check | integrity_auditor (**gate 2.5**, M1–M7) |
| review | peer-review | editor_in_chief, R1–R3 |
| revise | revision-coaching | revision_coach |
| re_review | peer-review | editor_in_chief |
| integrity_final | integrity-check | integrity_auditor (**gate 4.5**, M1–M7) |
| finalize | manuscript-finalize | manuscript_writer |

### Integrity M1–M7

| Mode | Meaning |
|------|---------|
| M1–M5 | Research track (sources, metrics, hypotheses, provenance, code) |
| M6 | Benchmark honesty (`runtime/state/benchmarks/`) |
| M7 | Manuscript ↔ passport/provenance |

### Profiles

| Profile | Scope |
|---------|-------|
| `hypothesis-only` | discover → ideate → synthesize |
| `full-hitl` | full research track |
| `full-autonomous` | full research track, autonomous mode |
| `full-publication` | research + publication → finalize |
| `publication-only` | write → finalize |

Full list: `runtime/state/pipeline_profiles.yaml`

### Orchestrator

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name full-hitl
uv run python runtime/scripts/orchestrate_pipeline.py pipeline-profiles
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/orchestrate_pipeline.py profiles
uv run python runtime/scripts/orchestrate_pipeline.py approve --by human
uv run python runtime/scripts/orchestrate_pipeline.py advance
```

```text
/research-pipeline --profile full-publication
```

Skill: `.cursor/skills/research-pipeline/SKILL.md`  
Playbooks: `.cursor/agents/playbooks/*.md`

## Orchestra bridge (execute / analyze)

Routing map: `.cursor/orchestra/SKILLS_MAP.yaml` (not in `docs/`).

```bash
uv run python runtime/scripts/orchestra_route.py list
uv run python runtime/scripts/orchestra_route.py resolve execute train
```

1. Skill **`orchestra-routing`** — Orchestra skill from `.cursor/skills/orchestra/` or template fallback.
2. Optional **`experiment-agent-bridge`** (CC BY-NC) — see `EXTERNAL_SKILLS.yaml`.
3. Per-task install: [docs/ORCHESTRA_INSTALL.md](docs/ORCHESTRA_INSTALL.md).

## Commands

```bash
uv sync --group dev
uv run ruff check src tests runtime
uv run pytest tests -q
uv run python runtime/scripts/validate_research.py
uv run python runtime/scripts/orchestrate_pipeline.py apply-profile --name hypothesis-only
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/orchestra_route.py resolve execute train
```

## External optional

[docs/REFERENCES.md](docs/REFERENCES.md) — Orchestra/K-Dense/ARS opt-in (not bundled).
