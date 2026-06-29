"""Pipeline profile application and phase helpers."""

from __future__ import annotations

from typing import Any

import yaml

from src.utils.integrity import PHASE_ORDER, load_pipeline_profiles, load_research_state
from src.utils.validate import RESEARCH_DIR, load_yaml

PIPELINE_CONFIG_PATH = RESEARCH_DIR / "pipeline.yaml"
STATE_PATH = RESEARCH_DIR / "research_state.yaml"
PASSPORT_PATH = RESEARCH_DIR / "passport.yaml"


def first_enabled_phase(phases_enabled: list[str]) -> str | None:
    enabled = set(phases_enabled)
    for phase in PHASE_ORDER:
        if phase in enabled:
            return phase
    return phases_enabled[0] if phases_enabled else None


def list_pipeline_profile_names() -> list[str]:
    data = load_pipeline_profiles()
    profiles = data.get("profiles") or {}
    return sorted(profiles.keys())


def validate_profile_phases(phases: list[str]) -> None:
    unknown = [phase for phase in phases if phase not in PHASE_ORDER]
    if unknown:
        known = ", ".join(PHASE_ORDER)
        raise ValueError(f"unknown phase(s) in profile: {', '.join(unknown)} (known: {known})")


def apply_pipeline_profile(profile_name: str) -> dict[str, Any]:
    data = load_pipeline_profiles()
    profiles = data.get("profiles") or {}
    if profile_name not in profiles:
        known = ", ".join(sorted(profiles.keys()))
        raise ValueError(f"unknown profile: {profile_name} (known: {known})")

    profile = profiles[profile_name]
    mode = profile.get("mode", "hitl")
    phases = list(profile.get("phases") or [])
    if not phases:
        raise ValueError(f"profile {profile_name} has no phases")

    validate_profile_phases(phases)

    first = first_enabled_phase(phases)
    if first is None:
        raise ValueError(f"profile {profile_name} has no valid phases")

    state = load_research_state()
    state["mode"] = mode
    state["pipeline_profile"] = profile_name
    state["phases_enabled"] = phases
    state["current_phase"] = first
    state["pending_approval"] = False
    state["approved_by"] = None
    state["approved_at"] = None

    with STATE_PATH.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(state, handle, sort_keys=False, allow_unicode=True)

    pipeline_config = {"profile": profile_name, "mode": mode, "phases": phases}
    with PIPELINE_CONFIG_PATH.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(pipeline_config, handle, sort_keys=False, allow_unicode=True)

    if PASSPORT_PATH.exists():
        passport = load_yaml(PASSPORT_PATH)
        passport["phase"] = first
        with PASSPORT_PATH.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(passport, handle, sort_keys=False, allow_unicode=True)

    return {
        "profile": profile_name,
        "mode": mode,
        "phases_enabled": phases,
        "current_phase": first,
    }
