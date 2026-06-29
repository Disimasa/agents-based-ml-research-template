"""Tests for orchestrator CLI helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from runtime.utils.integrity import (
    autonomous_preflight,
    can_advance,
    next_phase,
    run_integrity_check,
)
from runtime.utils.pipeline import apply_pipeline_profile


def _patch_state_dir(monkeypatch: pytest.MonkeyPatch, state_dir: Path) -> None:
    monkeypatch.setattr("runtime.utils.integrity.STATE_DIR", state_dir)
    monkeypatch.setattr("runtime.utils.pipeline.STATE_PATH", state_dir / "research_state.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PIPELINE_CONFIG_PATH", state_dir / "pipeline.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PASSPORT_PATH", state_dir / "passport.yaml")


def test_next_phase_from_discover() -> None:
    state = {
        "phases_enabled": ["discover", "ideate", "synthesize"],
        "current_phase": "discover",
    }
    assert next_phase(state) == "ideate"


def test_can_advance_blocked_without_approval() -> None:
    state = {
        "mode": "hitl",
        "phases_enabled": ["discover", "ideate"],
        "current_phase": "discover",
        "pending_approval": True,
        "approved_by": None,
    }
    report = run_integrity_check(phase="discover")
    ok, reasons = can_advance(state, report)
    assert not ok
    assert any("pending_approval" in reason for reason in reasons)


def test_can_advance_hitl_after_human_approve() -> None:
    state = {
        "mode": "hitl",
        "phases_enabled": ["discover", "ideate"],
        "current_phase": "discover",
        "pending_approval": False,
        "approved_by": "human",
    }
    report = run_integrity_check(phase="discover")
    ok, reasons = can_advance(state, report)
    assert ok, reasons


def test_apply_full_hitl_starts_bootstrap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    profiles_src = Path("runtime/state/pipeline_profiles.yaml").read_text(encoding="utf-8")
    (state_dir / "pipeline_profiles.yaml").write_text(profiles_src, encoding="utf-8")
    (state_dir / "research_state.yaml").write_text(
        yaml.safe_dump({"current_phase": "discover"}), encoding="utf-8"
    )
    (state_dir / "pipeline.yaml").write_text("profile: x\n", encoding="utf-8")
    (state_dir / "passport.yaml").write_text(
        yaml.safe_dump(
            {
                "research_question": None,
                "phase": "discover",
                "experiment_intake_declaration": "no_experiments_declared",
            }
        ),
        encoding="utf-8",
    )
    for name in ("hypotheses.yaml", "experiment_provenance.yaml"):
        src = Path("runtime/state") / name
        if src.exists():
            (state_dir / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    _patch_state_dir(monkeypatch, state_dir)

    result = apply_pipeline_profile("full-hitl")
    assert result["current_phase"] == "bootstrap"


def test_autonomous_preflight_requires_research_question() -> None:
    state = {
        "mode": "autonomous",
        "current_phase": "discover",
        "phases_enabled": ["discover", "ideate"],
        "autonomous": {
            "max_iterations": 20,
            "max_wall_time_hours": 8,
            "stop_on_plateau": 3,
            "metric_primary": None,
        },
    }
    findings = autonomous_preflight(state)
    assert any("research_question" in item for item in findings)


def test_autonomous_preflight_requires_metric_on_execute(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "passport.yaml").write_text(
        yaml.safe_dump({"research_question": "Does X improve Y?"}), encoding="utf-8"
    )
    monkeypatch.setattr("runtime.utils.integrity.STATE_DIR", state_dir)

    state = {
        "mode": "autonomous",
        "current_phase": "execute",
        "phases_enabled": ["execute", "analyze"],
        "autonomous": {
            "max_iterations": 20,
            "max_wall_time_hours": 8,
            "stop_on_plateau": 3,
            "metric_primary": None,
        },
    }
    findings = autonomous_preflight(state)
    assert any("metric_primary" in item for item in findings)
