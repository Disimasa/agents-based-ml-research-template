"""Tests for integrity M6/M7 and extended phase order."""

from runtime.utils.integrity import (
    GATE_PROFILES,
    PHASE_ORDER,
    check_m3_falsifiable_hypotheses,
    gate_modes_for_phase,
    next_phase,
    run_integrity_check,
)


def test_phase_order_includes_publication_track() -> None:
    assert "write" in PHASE_ORDER
    assert "integrity_pre_review" in PHASE_ORDER
    assert "finalize" in PHASE_ORDER
    assert PHASE_ORDER.index("integrity_pre_review") < PHASE_ORDER.index("review")


def test_gate_2_5_uses_m1_through_m7() -> None:
    profile, modes = gate_modes_for_phase("integrity_pre_review")
    assert profile == "gate_2_5_pre_review"
    assert modes == ["M1", "M2", "M3", "M4", "M5", "M6", "M7"]


def test_gate_4_5_profile() -> None:
    profile, modes = gate_modes_for_phase("integrity_final")
    assert profile == "gate_4_5_final"
    assert "M7" in modes


def test_m3_passes_on_empty_hypotheses() -> None:
    assert check_m3_falsifiable_hypotheses().passed


def test_next_phase_publication() -> None:
    state = {
        "phases_enabled": ["synthesize", "write", "integrity_pre_review"],
        "current_phase": "synthesize",
    }
    assert next_phase(state) == "write"


def test_integrity_report_seven_modes_when_requested() -> None:
    report = run_integrity_check(["M1", "M2", "M3", "M4", "M5", "M6", "M7"])
    assert len(report.results) == 7


def test_gate_profiles_defined() -> None:
    assert "research_default" in GATE_PROFILES
    assert len(GATE_PROFILES["gate_2_5_pre_review"]) == 7
