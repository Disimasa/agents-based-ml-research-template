"""Tests for pipeline profile application."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from src.utils.integrity import PHASE_ORDER
from src.utils.pipeline import (
    apply_pipeline_profile,
    first_enabled_phase,
    list_pipeline_profile_names,
)


def test_first_enabled_phase_respects_order() -> None:
    assert first_enabled_phase(["synthesize", "discover", "ideate"]) == "discover"
    assert first_enabled_phase(["finalize", "write"]) == "write"


def test_list_pipeline_profile_names() -> None:
    names = list_pipeline_profile_names()
    assert "hypothesis-only" in names
    assert "full-publication" in names


def test_apply_profile_hypothesis_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    research = tmp_path / "research"
    research.mkdir()
    profiles = {
        "profiles": {
            "hypothesis-only": {
                "mode": "hitl",
                "phases": ["discover", "ideate", "synthesize"],
            }
        }
    }
    (research / "pipeline_profiles.yaml").write_text(
        yaml.safe_dump(profiles), encoding="utf-8"
    )
    (research / "research_state.yaml").write_text(
        yaml.safe_dump({"current_phase": "bootstrap"}), encoding="utf-8"
    )
    (research / "pipeline.yaml").write_text("profile: old\n", encoding="utf-8")
    (research / "passport.yaml").write_text(
        yaml.safe_dump({"phase": "bootstrap", "research_question": None}), encoding="utf-8"
    )

    monkeypatch.setattr("src.utils.pipeline.RESEARCH_DIR", research)
    monkeypatch.setattr("src.utils.pipeline.STATE_PATH", research / "research_state.yaml")
    monkeypatch.setattr("src.utils.pipeline.PIPELINE_CONFIG_PATH", research / "pipeline.yaml")
    monkeypatch.setattr("src.utils.pipeline.PASSPORT_PATH", research / "passport.yaml")
    monkeypatch.setattr("src.utils.integrity.RESEARCH_DIR", research)

    result = apply_pipeline_profile("hypothesis-only")
    assert result["current_phase"] == "discover"
    state = yaml.safe_load((research / "research_state.yaml").read_text(encoding="utf-8"))
    assert state["pipeline_profile"] == "hypothesis-only"
    assert state["phases_enabled"] == ["discover", "ideate", "synthesize"]
    passport = yaml.safe_load((research / "passport.yaml").read_text(encoding="utf-8"))
    assert passport["phase"] == "discover"


def test_apply_unknown_profile_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    research = tmp_path / "research"
    research.mkdir()
    (research / "pipeline_profiles.yaml").write_text("profiles: {}\n", encoding="utf-8")
    (research / "research_state.yaml").write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr("src.utils.pipeline.RESEARCH_DIR", research)
    monkeypatch.setattr("src.utils.pipeline.STATE_PATH", research / "research_state.yaml")
    monkeypatch.setattr("src.utils.pipeline.PIPELINE_CONFIG_PATH", research / "pipeline.yaml")
    monkeypatch.setattr("src.utils.integrity.RESEARCH_DIR", research)
    with pytest.raises(ValueError, match="unknown profile"):
        apply_pipeline_profile("nope")


def test_phase_order_has_discover_before_synthesize() -> None:
    assert PHASE_ORDER.index("discover") < PHASE_ORDER.index("synthesize")


def test_benchmark_schema_accepts_canonical_example() -> None:
    schema_path = Path("shared/schemas/benchmark_report.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    example = {
        "experiment_id": "exp_001",
        "hypothesis_id": "hyp_001",
        "primary_metric": {"name": "accuracy", "value": None, "status": "not_executed"},
        "baselines": [],
        "limitations": ["Stub run — no metrics."],
        "negative_results": [],
    }
    import jsonschema

    jsonschema.Draft202012Validator(schema).validate(example)
