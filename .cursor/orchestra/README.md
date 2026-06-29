# Orchestra routing (agent layer)

**For agents:** read `SKILLS_MAP.yaml` via skill `orchestra-routing`.

| File | Purpose |
|------|---------|
| `SKILLS_MAP.yaml` | Phase/task → Orchestra skill names + template fallback |

**Install target:** `.cursor/skills/orchestra/` (gitignored symlinks — see [docs/ORCHESTRA_INSTALL.md](../../docs/ORCHESTRA_INSTALL.md)).

**CLI:**

```bash
uv run python runtime/scripts/orchestra_route.py list
uv run python runtime/scripts/orchestra_route.py resolve execute train
```

Do not commit cloned Orchestra skills into this template repo.
