# References

Upstream patterns and optional MIT skill installs by pipeline phase.

## Layout and training

- [cookiecutter-data-science](https://github.com/drivendata/cookiecutter-data-science) — CCDS layout
- [lightning-hydra-template](https://github.com/ashleve/lightning-hydra-template) — Hydra structure
- [Hydra docs](https://hydra.cc/docs/intro/)
- [uv docs](https://docs.astral.sh/uv/)

## Agent architecture (inspiration only)

Multi-agent roles, playbooks, and publication workflow in this template were **inspired by** (not copied from):

- [experiment-agent](https://github.com/Imbad0202/experiment-agent)
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills)

All agents and skills in `.cursor/` are **original MIT** implementations. No code from these projects is bundled or required.

## Optional installs by phase

Template ships **own** `.cursor/agents/` + `.cursor/skills/` (MIT). External repos below are optional accelerators for engineering tasks (train, eval, literature search).

**Agent routing map (Orchestra):** [`.cursor/orchestra/SKILLS_MAP.yaml`](../.cursor/orchestra/SKILLS_MAP.yaml)  
**Human install guide:** [ORCHESTRA_INSTALL.md](ORCHESTRA_INSTALL.md) (agent installs per task)

| Phase | Template skill | Optional external (license) |
|-------|----------------|----------------------------|
| bootstrap | `new-project` | — |
| discover | `literature-survey` | Orchestra paper-search (MIT); [Deep-Research-skills](https://github.com/Weizhena/Deep-Research-skills); K-Dense (MIT) |
| ideate | `hypothesis-ideation` | Orchestra hypothesis-generation (MIT) |
| plan | `research-plan` | K-Dense scientific brainstorming (MIT) |
| execute | `orchestra-routing` → `run-experiment`, `autonomous-loop` | [Orchestra AI-Research-SKILLs](https://github.com/Orchestra-research/AI-Research-SKILLs) — PEFT, TRL, W&B (MIT) |
| analyze | `orchestra-routing` → `analyze-results` | Orchestra lm-eval, wandb (MIT) |
| synthesize | `log-decision`, `integrity-check` | — |
| write | `manuscript-draft` | — |
| review / revise | `peer-review`, `revision-coaching` | — |
| finalize | `manuscript-finalize` | — |

## Orchestra bridge (execute / analyze)

1. Skill **`orchestra-routing`** reads `.cursor/orchestra/SKILLS_MAP.yaml`.
2. `uv run python runtime/scripts/orchestra_route.py resolve execute train`
3. If Orchestra skill installed in `.cursor/skills/orchestra/` → use it; else template `run-experiment`.
4. Always: provenance + `integrity-check` + HITL gates.

## K-Dense bridge (domain)

For bio/chem/domain libs, discover skills from [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) — no bundled orchestrator; `research-pipeline` skill composes the chain.

## Licensing

Template agents and skills in this repo are **MIT**. Optional Orchestra / K-Dense / Weizhena installs are **not bundled** — see table above and [ORCHESTRA_INSTALL.md](ORCHESTRA_INSTALL.md). No third-party code is copied into this repository.
