---
name: orchestra-routing
description: Route execute/analyze engineering to installed Orchestra skills or template fallbacks
---

# Orchestra routing

**Map:** `.cursor/orchestra/SKILLS_MAP.yaml`  
**External:** `.cursor/orchestra/EXTERNAL_SKILLS.yaml`

## When to use

- Before `run-experiment`, `autonomous-loop`, or `analyze-results`
- User has or wants optional [Orchestra AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) installed
- Phase `execute` or `analyze` (or autonomous train loop)

## Procedure

1. Read `.cursor/orchestra/SKILLS_MAP.yaml`.
2. Resolve route:

```bash
uv run python scripts/orchestra_route.py resolve <phase> <task>
# e.g. resolve execute train
```

3. **If `orchestra_available`** — open installed skill at `.cursor/skills/orchestra/<name>/SKILL.md` and follow it for the engineering subtask.
4. **If `orchestra_available: false`** — use `template_fallback.skill` and `template_fallback.agent` from the map (e.g. `run-experiment` + `experiment_runner`). If the user wants Orchestra: clone [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) and symlink **only** the skill(s) from `orchestra_candidates` for this task (see [docs/ORCHESTRA_INSTALL.md](../../docs/ORCHESTRA_INSTALL.md)); re-run `orchestra_route.py resolve`.
5. For **validate / reproducibility** — check `experiment-agent-bridge` if user opted into [experiment-agent](https://github.com/Imbad0202/experiment-agent) (CC BY-NC).
6. After any run:
   - Update `research/experiment_provenance.yaml` (`status`, `verification_status` if validated)
   - `uv run python scripts/integrity_check.py --modes M2 M4 M6`
   - `uv run python scripts/orchestrate_pipeline.py gate`
7. Log routing decision in `research/decision_log.md`:

```markdown
- **routing:** orchestra: wandb | fallback: run-experiment
- **source:** ai
```

## Install (on demand)

Only when user agrees and a route needs Orchestra. Install **one skill at a time** per [docs/ORCHESTRA_INSTALL.md](../../docs/ORCHESTRA_INSTALL.md). Never bulk-install or copy SKILL.md into this repo.

## Rules

- Never assume Orchestra skills are installed — always run `orchestra_route.py` or check `install_dir`.
- Template integrity gates always apply; Orchestra does not replace `integrity-check`.
- Do not copy Orchestra SKILL.md into this repo.

## Related template skills

| Task | Fallback skill |
|------|----------------|
| train | `run-experiment` |
| train_autonomous | `autonomous-loop` |
| eval | `analyze-results` |
| literature_search | `literature-survey` |
| hypothesis_generation | `hypothesis-ideation` |
