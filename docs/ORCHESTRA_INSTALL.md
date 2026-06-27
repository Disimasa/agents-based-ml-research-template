# Orchestra skills — opt-in install

Agent routing map lives in **`.cursor/orchestra/SKILLS_MAP.yaml`** (not in this doc).

## Quick install

```bash
# 1. Clone Orchestra repo next to your project (or anywhere)
git clone https://github.com/Orchestra-Research/AI-Research-SKILLs.git ../AI-Research-SKILLs

# 2. Symlink selected skills into template install dir
mkdir -p .cursor/skills/orchestra

# Windows (PowerShell, admin may be required for symlinks)
New-Item -ItemType SymbolicLink -Path ".cursor/skills/orchestra/wandb" -Target "..\..\..\AI-Research-SKILLs\wandb"

# Linux / macOS
ln -s ../../../AI-Research-SKILLs/wandb .cursor/skills/orchestra/wandb
```

Repeat for skills listed in `SKILLS_MAP.yaml` (start with **wandb**, **lm-eval**, **peft**).

## Verify

```bash
uv run python scripts/orchestra_route.py list
uv run python scripts/orchestra_route.py resolve execute train
```

Expected when installed: `route: orchestra/wandb` (or first matched skill).  
When not installed: `route: template/run-experiment (agent: experiment_runner)`.

## Agent workflow

1. Skill **`orchestra-routing`** — read map, run CLI, delegate to Orchestra or fallback.
2. After run — `experiment_provenance.yaml`, `integrity_check`, `orchestrate_pipeline.py gate`.

## experiment-agent (optional, CC BY-NC)

Separate from Orchestra MIT skills. See [experiment-agent](https://github.com/Imbad0202/experiment-agent).

```bash
git clone https://github.com/Imbad0202/experiment-agent.git ../experiment-agent
```

Use template skill **`experiment-agent-bridge`** — config in `.cursor/orchestra/EXTERNAL_SKILLS.yaml`.

## Do not

- Commit cloned Orchestra or experiment-agent repos into ml-research-template
- Copy their SKILL.md into this repository (license + maintenance)

## See also

- [.cursor/orchestra/README.md](../.cursor/orchestra/README.md)
- [REFERENCES.md](REFERENCES.md)
- [NOTICE.md](../NOTICE.md)
