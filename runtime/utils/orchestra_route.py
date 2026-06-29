"""Resolve Orchestra vs template fallback from .cursor/orchestra/SKILLS_MAP.yaml."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = ROOT / ".cursor" / "orchestra" / "SKILLS_MAP.yaml"


def load_skills_map(path: Path | None = None) -> dict[str, Any]:
    map_path = path or MAP_PATH
    if not map_path.exists():
        raise FileNotFoundError(f"Skills map not found: {map_path}")
    data = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def installed_orchestra_skills(install_dir: str | Path) -> list[str]:
    directory = ROOT / install_dir if not Path(install_dir).is_absolute() else Path(install_dir)
    if not directory.exists():
        return []
    return sorted(
        item.name
        for item in directory.iterdir()
        if item.is_dir() and (item / "SKILL.md").exists()
    )


def resolve_route(
    phase: str,
    task: str,
    *,
    map_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    data = map_data or load_skills_map()
    routes = data.get("routes") or {}
    phase_routes = routes.get(phase)
    if not phase_routes:
        return {
            "phase": phase,
            "task": task,
            "error": f"unknown phase: {phase}",
            "orchestra_available": False,
        }

    task_config = phase_routes.get(task)
    if not task_config:
        return {
            "phase": phase,
            "task": task,
            "error": f"unknown task {task} for phase {phase}",
            "orchestra_available": False,
        }

    install_dir = (data.get("install") or {}).get("install_dir", ".cursor/skills/orchestra")
    installed = set(installed_orchestra_skills(install_dir))
    candidates = task_config.get("orchestra_skills") or []
    matched = [name for name in candidates if name in installed]

    fallback = task_config.get("template_fallback") or {}
    return {
        "phase": phase,
        "task": task,
        "install_dir": install_dir,
        "orchestra_candidates": candidates,
        "orchestra_matched": matched,
        "orchestra_available": bool(matched),
        "use_orchestra_skill": matched[0] if matched else None,
        "template_fallback": fallback,
        "external_bridge": task_config.get("external_bridge"),
        "notes": task_config.get("notes"),
    }


def list_routes(*, map_data: dict[str, Any] | None = None) -> list[dict[str, str]]:
    data = map_data or load_skills_map()
    install_dir = (data.get("install") or {}).get("install_dir", ".cursor/skills/orchestra")
    installed = installed_orchestra_skills(install_dir)
    rows: list[dict[str, str]] = []
    for phase, tasks in (data.get("routes") or {}).items():
        if not isinstance(tasks, dict):
            continue
        for task, config in tasks.items():
            if not isinstance(config, dict):
                continue
            candidates = config.get("orchestra_skills") or []
            matched = [name for name in candidates if name in installed]
            fb = config.get("template_fallback") or {}
            rows.append(
                {
                    "phase": str(phase),
                    "task": str(task),
                    "orchestra_matched": ",".join(matched) if matched else "-",
                    "fallback_skill": str(fb.get("skill", "")),
                    "fallback_agent": str(fb.get("agent", "")),
                }
            )
    return rows
