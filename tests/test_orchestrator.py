"""Tests for orchestrator CLI helpers."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from src.utils.integrity import can_advance, next_phase, run_integrity_check
from src.utils.pipeline import apply_pipeline_profile


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
    research = tmp_path / "research"
    research.mkdir()
    profiles_src = Path("research/pipeline_profiles.yaml").read_text(encoding="utf-8")
    (research / "pipeline_profiles.yaml").write_text(profiles_src, encoding="utf-8")
    (research / "research_state.yaml").write_text(
        yaml.safe_dump({"current_phase": "discover"}), encoding="utf-8"
    )
    (research / "pipeline.yaml").write_text("profile: x\n", encoding="utf-8")
    (research / "passport.yaml").write_text(
        yaml.safe_dump(
            {
                "research_question": None,
                "phase": "discover",
                "experiment_intake_declaration": "no_experiments_declared",
            }
        ),
        encoding="utf-8",
    )
    for name in (
        "hypotheses.yaml",
        "experiment_provenance.yaml",
    ):
        src = Path("research") / name
        if src.exists():
            (research / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    monkeypatch.setattr("src.utils.pipeline.RESEARCH_DIR", research)
    monkeypatch.setattr("src.utils.pipeline.STATE_PATH", research / "research_state.yaml")
    monkeypatch.setattr("src.utils.pipeline.PIPELINE_CONFIG_PATH", research / "pipeline.yaml")
    monkeypatch.setattr("src.utils.pipeline.PASSPORT_PATH", research / "passport.yaml")
    monkeypatch.setattr("src.utils.integrity.RESEARCH_DIR", research)

    result = apply_pipeline_profile("full-hitl")
    assert result["current_phase"] == "bootstrap"
