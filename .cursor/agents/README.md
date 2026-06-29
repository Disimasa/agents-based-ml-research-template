# Agent roles

Role definitions for the modular research pipeline. **Contracts** in this folder; **deep playbooks** in [playbooks/](playbooks/).

**Orchestrator:** `pipeline_orchestrator.md` + `research-pipeline` + `runtime/scripts/orchestrate_pipeline.py`  
**Integrity:** M1–M7, gates **2.5** (`integrity_pre_review`) and **4.5** (`integrity_final`)

## Roster (21 agents)

| Agent | Phases | Playbook |
|-------|--------|----------|
| intake_agent | bootstrap | [playbooks/intake_agent.md](playbooks/intake_agent.md) |
| literature_scout | discover | [playbooks/literature_scout.md](playbooks/literature_scout.md) |
| source_verifier | discover | [playbooks/source_verifier.md](playbooks/source_verifier.md) |
| synthesis_agent | discover, synthesize | [playbooks/synthesis_agent.md](playbooks/synthesis_agent.md) |
| hypothesis_generator | ideate | [playbooks/hypothesis_generator.md](playbooks/hypothesis_generator.md) |
| devils_advocate | ideate, plan | [playbooks/devils_advocate.md](playbooks/devils_advocate.md) |
| methodology_critic | plan | [playbooks/methodology_critic.md](playbooks/methodology_critic.md) |
| ethics_reviewer | plan | [playbooks/ethics_reviewer.md](playbooks/ethics_reviewer.md) |
| experiment_runner | execute | [playbooks/experiment_runner.md](playbooks/experiment_runner.md) |
| implementation_reviewer | execute | [playbooks/implementation_reviewer.md](playbooks/implementation_reviewer.md) |
| results_analyst | analyze | [playbooks/results_analyst.md](playbooks/results_analyst.md) |
| integrity_auditor | gates, synthesize | [playbooks/integrity_auditor.md](playbooks/integrity_auditor.md) |
| research_manager | all | [playbooks/research_manager.md](playbooks/research_manager.md) |
| pipeline_orchestrator | meta | [playbooks/pipeline_orchestrator.md](playbooks/pipeline_orchestrator.md) |
| autonomous_controller | execute (autonomous) | [playbooks/autonomous_controller.md](playbooks/autonomous_controller.md) |
| manuscript_writer | write, finalize | [playbooks/manuscript_writer.md](playbooks/manuscript_writer.md) |
| editor_in_chief | review, re_review | [playbooks/editor_in_chief.md](playbooks/editor_in_chief.md) |
| peer_reviewer_r1 | review, re_review | [playbooks/peer_reviewer_r1.md](playbooks/peer_reviewer_r1.md) |
| peer_reviewer_r2 | review, re_review | [playbooks/peer_reviewer_r2.md](playbooks/peer_reviewer_r2.md) |
| peer_reviewer_r3 | review, re_review | [playbooks/peer_reviewer_r3.md](playbooks/peer_reviewer_r3.md) |
| revision_coach | revise | [playbooks/revision_coach.md](playbooks/revision_coach.md) |

## Skills (16)

Research: `new-project`, `literature-survey`, `hypothesis-ideation`, `research-plan`, `run-experiment`, `autonomous-loop`, `analyze-results`, `log-decision`, `integrity-check`, `research-pipeline`

Orchestra bridge: `orchestra-routing` (map: `.cursor/orchestra/SKILLS_MAP.yaml`)

Publication: `manuscript-draft`, `peer-review`, `revision-coaching`, `manuscript-finalize`

## CLI

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/orchestrate_pipeline.py profiles
uv run python runtime/scripts/orchestra_route.py list
uv run python runtime/scripts/integrity_check.py --phase integrity_pre_review
```

Regenerate playbooks after template edits: `python runtime/tools/generate_playbooks.py`
