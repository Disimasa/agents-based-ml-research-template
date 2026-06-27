# AGENTS.md

Точка входа для AI-ассистентов: карта репозитория, pipeline, агенты. Правила — `.cursor/rules/`, сценарии — `.cursor/skills/`, роли — `.cursor/agents/` (+ [playbooks](.cursor/agents/playbooks/)).

## Layout

| Path | Purpose |
|------|---------|
| `configs/` | Hydra configs |
| `src/modeling/` | Training code (stub until Wave A) |
| `research/manuscript/` | Publication track (draft, reviews, revision) |
| `research/` | Pipeline state — [research/README.md](research/README.md) |
| `.cursor/rules/` | 12 governance rules |
| `.cursor/skills/` | 16 skills (research + publication + orchestra bridge) |
| `.cursor/orchestra/` | SKILLS_MAP + EXTERNAL_SKILLS (Orchestra opt-in routing) |
| `.cursor/agents/` | 21 agent contracts + playbooks |
| `scripts/` | `orchestrate_pipeline.py`, `orchestra_route.py`, `integrity_check.py`, validate |
| `shared/schemas/` | JSON schemas |

## Research + publication pipeline

### Режимы

| Mode | Поведение |
|------|-----------|
| `hitl` | `pending_approval` + `approved_by: human` между фазами |
| `autonomous` | auto-advance при PASS gate; inner loop на execute |

### Фазы (14)

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

| Mode | Смысл |
|------|--------|
| M1–M5 | Research track (sources, metrics, hypotheses, provenance, code) |
| M6 | Benchmark honesty (`reports/benchmarks/`) |
| M7 | Manuscript ↔ passport/provenance |

### Профили

| Profile | Срез |
|---------|------|
| `hypothesis-only` | discover → ideate → synthesize |
| `full-hitl` | research track |
| `full-publication` | research + publication → finalize |
| `publication-only` | write → finalize |

Полный список: `research/pipeline_profiles.yaml`

### Orchestrator

```bash
uv run python scripts/orchestrate_pipeline.py status
uv run python scripts/orchestrate_pipeline.py gate
uv run python scripts/orchestrate_pipeline.py profiles
uv run python scripts/orchestrate_pipeline.py approve --by human
uv run python scripts/orchestrate_pipeline.py advance
```

```text
/research-pipeline --profile full-publication
```

Skill: `.cursor/skills/research-pipeline/SKILL.md`  
Playbooks: `.cursor/agents/playbooks/*.md`

## Orchestra bridge (execute / analyze)

Карта маршрутизации: `.cursor/orchestra/SKILLS_MAP.yaml` (не в `docs/`).

```bash
uv run python scripts/orchestra_route.py list
uv run python scripts/orchestra_route.py resolve execute train
```

1. Skill **`orchestra-routing`** — Orchestra skill из `.cursor/skills/orchestra/` или template fallback.
2. Опционально **`experiment-agent-bridge`** (CC BY-NC) — см. `EXTERNAL_SKILLS.yaml`.
3. Установка: [docs/ORCHESTRA_INSTALL.md](docs/ORCHESTRA_INSTALL.md).

## Commands

```bash
uv sync --group dev
uv run ruff check src tests scripts
uv run pytest tests -q
uv run python scripts/validate_research.py
uv run python scripts/orchestra_route.py resolve execute train
uv run python scripts/integrity_check.py --phase integrity_pre_review
```

## External optional

[docs/REFERENCES.md](docs/REFERENCES.md) — Orchestra/K-Dense/ARS opt-in (не bundle).
