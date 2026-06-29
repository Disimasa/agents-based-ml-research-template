"""Tests for pipeline profile application."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from runtime.utils.integrity import PHASE_ORDER
from runtime.utils.pipeline import (
    apply_pipeline_profile,
    first_enabled_phase,
    list_pipeline_profile_names,
    validate_profile_phases,
)


def test_first_enabled_phase_respects_order() -> None:
    assert first_enabled_phase(["synthesize", "discover", "ideate"]) == "discover"
    assert first_enabled_phase(["finalize", "write"]) == "write"


def test_list_pipeline_profile_names() -> None:
    names = list_pipeline_profile_names()
    assert "hypothesis-only" in names
    assert "full-publication" in names


def test_apply_profile_hypothesis_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    profiles = {
        "profiles": {
            "hypothesis-only": {
                "mode": "hitl",
                "phases": ["discover", "ideate", "synthesize"],
            }
        }
    }
    (state_dir / "pipeline_profiles.yaml").write_text(
        yaml.safe_dump(profiles), encoding="utf-8"
    )
    (state_dir / "research_state.yaml").write_text(
        yaml.safe_dump({"current_phase": "bootstrap"}), encoding="utf-8"
    )
    (state_dir / "pipeline.yaml").write_text("profile: old\n", encoding="utf-8")
    (state_dir / "passport.yaml").write_text(
        yaml.safe_dump({"phase": "bootstrap", "research_question": None}), encoding="utf-8"
    )

    monkeypatch.setattr("runtime.utils.integrity.STATE_DIR", state_dir)
    monkeypatch.setattr("runtime.utils.pipeline.STATE_PATH", state_dir / "research_state.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PIPELINE_CONFIG_PATH", state_dir / "pipeline.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PASSPORT_PATH", state_dir / "passport.yaml")

    result = apply_pipeline_profile("hypothesis-only")
    assert result["current_phase"] == "discover"
    state = yaml.safe_load((state_dir / "research_state.yaml").read_text(encoding="utf-8"))
    assert state["pipeline_profile"] == "hypothesis-only"
    assert state["phases_enabled"] == ["discover", "ideate", "synthesize"]
    passport = yaml.safe_load((state_dir / "passport.yaml").read_text(encoding="utf-8"))
    assert passport["phase"] == "discover"


def test_apply_unknown_profile_raises(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    (state_dir / "pipeline_profiles.yaml").write_text("profiles: {}\n", encoding="utf-8")
    (state_dir / "research_state.yaml").write_text("{}\n", encoding="utf-8")
    monkeypatch.setattr("runtime.utils.integrity.STATE_DIR", state_dir)
    monkeypatch.setattr("runtime.utils.pipeline.STATE_PATH", state_dir / "research_state.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PIPELINE_CONFIG_PATH", state_dir / "pipeline.yaml")
    with pytest.raises(ValueError, match="unknown profile"):
        apply_pipeline_profile("nope")


def test_phase_order_has_discover_before_synthesize() -> None:
    assert PHASE_ORDER.index("discover") < PHASE_ORDER.index("synthesize")


def test_benchmark_schema_accepts_canonical_example() -> None:
    schema_path = Path("runtime/schemas/benchmark_report.schema.json")
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


def test_experiment_provenance_schema_planned_vs_executed() -> None:
    schema_path = Path("runtime/schemas/experiment_provenance.schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    import jsonschema

    example = {
        "experiments": [
            {
                "experiment_id": "exp_001",
                "planned_vs_executed": [{"planned": "exp_001", "executed": True}],
            }
        ]
    }
    jsonschema.Draft202012Validator(schema).validate(example)


def test_validate_profile_phases_rejects_unknown() -> None:
    with pytest.raises(ValueError, match="unknown phase"):
        validate_profile_phases(["discover", "not-a-phase"])


def test_apply_profile_rejects_invalid_phase(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    state_dir = tmp_path / "state"
    state_dir.mkdir()
    profiles = {
        "profiles": {
            "bad": {"mode": "hitl", "phases": ["discover", "typo-phase"]},
        }
    }
    (state_dir / "pipeline_profiles.yaml").write_text(
        yaml.safe_dump(profiles), encoding="utf-8"
    )
    (state_dir / "research_state.yaml").write_text("{}", encoding="utf-8")
    monkeypatch.setattr("runtime.utils.integrity.STATE_DIR", state_dir)
    monkeypatch.setattr("runtime.utils.pipeline.STATE_PATH", state_dir / "research_state.yaml")
    monkeypatch.setattr("runtime.utils.pipeline.PIPELINE_CONFIG_PATH", state_dir / "pipeline.yaml")
    with pytest.raises(ValueError, match="unknown phase"):
        apply_pipeline_profile("bad")
