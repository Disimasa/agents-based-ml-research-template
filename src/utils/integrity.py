"""Automated integrity checks M1–M7 (ARS-inspired)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import jsonschema

from src.utils.validate import load_yaml

ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "research"
REPORTS_DIR = ROOT / "reports" / "benchmarks"
MANUSCRIPT_DIR = RESEARCH_DIR / "manuscript"
BENCHMARK_SCHEMA_PATH = ROOT / "shared" / "schemas" / "benchmark_report.schema.json"

PHASE_ORDER = [
    "bootstrap",
    "discover",
    "ideate",
    "plan",
    "execute",
    "analyze",
    "synthesize",
    "write",
    "integrity_pre_review",
    "review",
    "revise",
    "re_review",
    "integrity_final",
    "finalize",
]

# ARS-style gate profiles: 2.5 (pre-review) and 4.5 (pre-finalize) use full M1–M7.
GATE_PROFILES: dict[str, list[str]] = {
    "research_default": ["M1", "M2", "M3", "M4", "M5"],
    "gate_2_5_pre_review": ["M1", "M2", "M3", "M4", "M5", "M6", "M7"],
    "gate_4_5_final": ["M1", "M2", "M3", "M4", "M5", "M6", "M7"],
    "publication_light": ["M4", "M6", "M7"],
}

PHASE_GATE_PROFILE: dict[str, str] = {
    "integrity_pre_review": "gate_2_5_pre_review",
    "integrity_final": "gate_4_5_final",
    "review": "publication_light",
    "re_review": "publication_light",
    "finalize": "publication_light",
}

METRIC_PATTERN = re.compile(
    r"\b(\d+\.\d+|\d+%|accuracy|f1|auc|mse|loss|bleu|rouge)\b",
    re.IGNORECASE,
)
EXPERIMENT_CLAIM_PATTERN = re.compile(
    r"\b(we (achieved|obtained|trained|ran)|results show|outperforms|beats baseline)\b",
    re.IGNORECASE,
)


@dataclass
class ModeResult:
    mode: str
    passed: bool
    findings: list[str] = field(default_factory=list)


@dataclass
class IntegrityReport:
    results: list[ModeResult] = field(default_factory=list)
    gate_profile: str = "research_default"

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    def failures(self) -> list[str]:
        messages: list[str] = []
        for result in self.results:
            if not result.passed:
                for finding in result.findings:
                    messages.append(f"{result.mode}: {finding}")
        return messages


def gate_modes_for_phase(phase: str | None) -> tuple[str, list[str]]:
    profile_name = PHASE_GATE_PROFILE.get(phase or "", "research_default")
    modes = GATE_PROFILES[profile_name]
    return profile_name, modes


def _literature_dirs() -> list[Path]:
    literature_root = RESEARCH_DIR / "literature"
    if not literature_root.exists():
        return []
    return [path for path in literature_root.iterdir() if path.is_dir() and path.name != "_example"]


def _load_verified_source_ids() -> set[str]:
    ids: set[str] = set()
    for topic_dir in _literature_dirs():
        results_dir = topic_dir / "results"
        if not results_dir.exists():
            continue
        for json_path in results_dir.glob("*.json"):
            try:
                payload = json.loads(json_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            entries = payload if isinstance(payload, list) else [payload]
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                if entry.get("verified") is True and entry.get("id"):
                    ids.add(str(entry["id"]))
    return ids


def check_m1_source_traceability() -> ModeResult:
    findings: list[str] = []
    passport = load_yaml(RESEARCH_DIR / "passport.yaml")
    verified_ids = _load_verified_source_ids()
    claims = passport.get("claims") or []

    for index, claim in enumerate(claims):
        if not isinstance(claim, dict):
            continue
        source_id = claim.get("source_id") or claim.get("literature_id")
        if source_id and str(source_id) not in verified_ids:
            findings.append(
                f"claim[{index}] references unverified or missing source_id={source_id}"
            )

    if claims and not verified_ids and _literature_dirs():
        findings.append("claims present but no verified literature results/*.json entries")

    return ModeResult("M1", not findings, findings)


def check_m2_no_fabricated_metrics() -> ModeResult:
    findings: list[str] = []
    provenance = load_yaml(RESEARCH_DIR / "experiment_provenance.yaml")
    experiment_ids = {
        str(item.get("experiment_id"))
        for item in (provenance.get("experiments") or [])
        if isinstance(item, dict) and item.get("experiment_id")
    }

    scan_paths = list(RESEARCH_DIR.rglob("*.md")) + list(RESEARCH_DIR.rglob("*.yaml"))
    scan_paths.extend(REPORTS_DIR.glob("*.json") if REPORTS_DIR.exists() else [])

    for path in scan_paths:
        if path.name in {"pipeline_profiles.yaml", "reviews.yaml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if not METRIC_PATTERN.search(text):
            continue
        if EXPERIMENT_CLAIM_PATTERN.search(text):
            rel = path.relative_to(ROOT)
            if "experiment_id" not in text and not any(exp_id in text for exp_id in experiment_ids):
                findings.append(
                    f"possible fabricated metric in {rel} without experiment_id linkage"
                )

    return ModeResult("M2", not findings, findings)


def check_m3_falsifiable_hypotheses() -> ModeResult:
    findings: list[str] = []
    data = load_yaml(RESEARCH_DIR / "hypotheses.yaml")
    for hypothesis in data.get("hypotheses") or []:
        if not isinstance(hypothesis, dict):
            continue
        if hypothesis.get("status") == "rejected":
            continue
        criteria = str(hypothesis.get("falsification_criteria") or "").strip()
        if len(criteria) < 12:
            hyp_id = hypothesis.get("id", "?")
            findings.append(f"{hyp_id}: falsification_criteria missing or too vague")
        vague = {"if it fails", "if it doesn't work", "if not better", "tbd", "n/a"}
        if criteria.lower() in vague:
            hyp_id = hypothesis.get("id", "?")
            findings.append(f"{hyp_id}: falsification_criteria is not measurable")
    return ModeResult("M3", not findings, findings)


def check_m4_provenance_linkage() -> ModeResult:
    findings: list[str] = []
    passport = load_yaml(RESEARCH_DIR / "passport.yaml")
    provenance = load_yaml(RESEARCH_DIR / "experiment_provenance.yaml")
    experiment_ids = {
        str(item.get("experiment_id"))
        for item in (provenance.get("experiments") or [])
        if isinstance(item, dict) and item.get("experiment_id")
    }

    for index, claim in enumerate(passport.get("claims") or []):
        if not isinstance(claim, dict):
            continue
        statement = str(claim.get("statement") or "")
        if not EXPERIMENT_CLAIM_PATTERN.search(statement):
            continue
        exp_id = claim.get("experiment_id")
        if not exp_id or str(exp_id) not in experiment_ids:
            findings.append(
                f"claim[{index}] implies experimental result but lacks provenance experiment_id"
            )

    return ModeResult("M4", not findings, findings)


def check_m5_paper_code_consistency() -> ModeResult:
    findings: list[str] = []
    methodology = RESEARCH_DIR / "methodology.md"
    train_py = ROOT / "src" / "train.py"
    train_is_stub = train_py.read_text(encoding="utf-8").strip().count("\n") < 5

    if methodology.exists():
        text = methodology.read_text(encoding="utf-8", errors="ignore")
        if train_is_stub and EXPERIMENT_CLAIM_PATTERN.search(text):
            findings.append("methodology.md claims execution but src/train.py is still a stub")
        if "configs/model/" in text or "configs/experiment/" in text:
            for match in re.findall(r"configs/(model|experiment)/([\w_-]+)", text):
                group, name = match
                config_path = ROOT / "configs" / group / f"{name}.yaml"
                if not config_path.exists():
                    findings.append(
                        f"methodology references missing config: configs/{group}/{name}.yaml"
                    )

    state = load_research_state()
    execute_phases = {"execute", "analyze", "synthesize"}
    if (
        list((ROOT / "configs" / "model").glob("*.yaml"))
        and train_is_stub
        and state.get("current_phase") in execute_phases
    ):
        findings.append(
            "training entry point is stub during execute — use status blocked_stub in provenance"
        )

    return ModeResult("M5", not findings, findings)


def check_m6_benchmark_honesty() -> ModeResult:
    findings: list[str] = []
    if not REPORTS_DIR.exists():
        return ModeResult("M6", True, [])

    reports = list(REPORTS_DIR.glob("*.json"))
    if not reports:
        return ModeResult("M6", True, [])

    schema = json.loads(BENCHMARK_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    provenance = load_yaml(RESEARCH_DIR / "experiment_provenance.yaml")
    provenance_ids = {
        str(item.get("experiment_id"))
        for item in (provenance.get("experiments") or [])
        if isinstance(item, dict) and item.get("experiment_id")
    }

    for report_path in reports:
        try:
            data = json.loads(report_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            findings.append(f"{report_path.name}: invalid JSON")
            continue
        errors = list(validator.iter_errors(data))
        if errors:
            findings.append(f"{report_path.name}: schema — {errors[0].message}")
        exp_id = str(data.get("experiment_id", ""))
        if exp_id and exp_id not in provenance_ids:
            findings.append(f"{report_path.name}: experiment_id not in provenance")
        notes = str(data.get("honest_comparison_notes") or data.get("limitations") or "").strip()
        if not notes:
            findings.append(f"{report_path.name}: missing honest_comparison_notes or limitations")

    return ModeResult("M6", not findings, findings)


def check_m7_manuscript_state_consistency() -> ModeResult:
    findings: list[str] = []
    draft_path = MANUSCRIPT_DIR / "draft.md"
    state = load_research_state()
    publication_phases = {
        "write",
        "integrity_pre_review",
        "review",
        "revise",
        "re_review",
        "integrity_final",
        "finalize",
    }
    current = state.get("current_phase")
    enabled = set(state.get("phases_enabled") or [])
    publication_active = bool(enabled & publication_phases)

    if publication_active and current in publication_phases and not draft_path.exists():
        findings.append("publication phase active but research/manuscript/draft.md missing")
        return ModeResult("M7", False, findings)

    if not draft_path.exists():
        return ModeResult("M7", True, [])

    draft_text = draft_path.read_text(encoding="utf-8", errors="ignore")
    passport = load_yaml(RESEARCH_DIR / "passport.yaml")
    provenance = load_yaml(RESEARCH_DIR / "experiment_provenance.yaml")
    experiment_ids = {
        str(item.get("experiment_id"))
        for item in (provenance.get("experiments") or [])
        if isinstance(item, dict) and item.get("experiment_id")
    }

    if EXPERIMENT_CLAIM_PATTERN.search(draft_text):
        if not any(exp_id in draft_text for exp_id in experiment_ids):
            if "experiment_id:" not in draft_text and "[uncertain]" not in draft_text:
                findings.append(
                    "manuscript draft contains experimental claims without experiment_id tags"
                )

    for index, claim in enumerate(passport.get("claims") or []):
        if not isinstance(claim, dict):
            continue
        statement = str(claim.get("statement") or "")
        if len(statement) < 20:
            continue
        snippet = statement[:40]
        if snippet in draft_text:
            exp_id = claim.get("experiment_id")
            if claim.get("source_id") is None and exp_id and str(exp_id) not in draft_text:
                findings.append(
                    f"passport claim[{index}] in draft but missing experiment_id {exp_id} nearby"
                )

    return ModeResult("M7", not findings, findings)


def run_integrity_check(
    modes: list[str] | None = None,
    *,
    phase: str | None = None,
) -> IntegrityReport:
    profile_name, profile_modes = gate_modes_for_phase(phase)
    selected = modes or profile_modes
    all_checks = {
        "M1": check_m1_source_traceability,
        "M2": check_m2_no_fabricated_metrics,
        "M3": check_m3_falsifiable_hypotheses,
        "M4": check_m4_provenance_linkage,
        "M5": check_m5_paper_code_consistency,
        "M6": check_m6_benchmark_honesty,
        "M7": check_m7_manuscript_state_consistency,
    }
    report = IntegrityReport(gate_profile=profile_name)
    for mode in selected:
        if mode in all_checks:
            report.results.append(all_checks[mode]())
    return report


def load_research_state() -> dict[str, Any]:
    return load_yaml(RESEARCH_DIR / "research_state.yaml")


def load_pipeline_profiles() -> dict[str, Any]:
    return load_yaml(RESEARCH_DIR / "pipeline_profiles.yaml")


def next_phase(state: dict[str, Any]) -> str | None:
    enabled = state.get("phases_enabled") or []
    current = state.get("current_phase")
    if current not in PHASE_ORDER:
        return enabled[0] if enabled else None
    current_index = PHASE_ORDER.index(current)
    for phase in PHASE_ORDER[current_index + 1 :]:
        if phase in enabled:
            return phase
    return None


def can_advance(state: dict[str, Any], integrity: IntegrityReport) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if not integrity.passed:
        reasons.extend(integrity.failures())
    reasons.extend(autonomous_preflight(state))
    if state.get("pending_approval"):
        reasons.append("pending_approval is true — approve before advance")
    mode = state.get("mode", "hitl")
    approved_by = state.get("approved_by")
    if mode == "hitl" and approved_by != "human":
        reasons.append("hitl mode requires approved_by: human")
    if mode == "autonomous" and approved_by not in {"human", "ai"}:
        reasons.append("autonomous mode requires approved_by: human or ai")
    nxt = next_phase(state)
    if nxt is None:
        reasons.append("no next phase in phases_enabled — pipeline may be complete")
    return (len(reasons) == 0, reasons)


def autonomous_preflight(state: dict[str, Any]) -> list[str]:
    """Guardrails when mode is autonomous."""
    if state.get("mode") != "autonomous":
        return []

    findings: list[str] = []
    autonomous = state.get("autonomous")
    if not isinstance(autonomous, dict):
        findings.append("autonomous mode requires autonomous: {} block in research_state.yaml")
        return findings

    for key in ("max_iterations", "max_wall_time_hours", "stop_on_plateau"):
        if key not in autonomous:
            findings.append(f"autonomous.{key} is required in autonomous mode")

    phases_enabled = state.get("phases_enabled") or []
    current = state.get("current_phase")
    execute_track = "execute" in phases_enabled

    passport = load_yaml(RESEARCH_DIR / "passport.yaml")
    question = passport.get("research_question")
    if current != "bootstrap" and not (isinstance(question, str) and question.strip()):
        findings.append("autonomous mode requires non-empty passport.research_question")

    if execute_track and current in {"execute", "analyze", "synthesize"}:
        metric = autonomous.get("metric_primary")
        if not (isinstance(metric, str) and metric.strip()):
            findings.append(
                "autonomous mode with execute phase requires autonomous.metric_primary "
                "before execute/analyze"
            )

    return findings
