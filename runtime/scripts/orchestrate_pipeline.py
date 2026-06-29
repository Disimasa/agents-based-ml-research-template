"""Research pipeline orchestrator CLI — status, gate, approve, advance."""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime

import yaml

from runtime.utils.integrity import (
    GATE_PROFILES,
    autonomous_preflight,
    can_advance,
    gate_modes_for_phase,
    load_research_state,
    next_phase,
    run_integrity_check,
)
from runtime.utils.pipeline import (
    PASSPORT_PATH,
    STATE_PATH,
    apply_pipeline_profile,
    list_pipeline_profile_names,
)
from runtime.utils.validate import validate_research

PHASE_SKILLS = {
    "bootstrap": "new-project",
    "discover": "literature-survey",
    "ideate": "hypothesis-ideation",
    "plan": "research-plan",
    "execute": "orchestra-routing → run-experiment / autonomous-loop",
    "analyze": "orchestra-routing → analyze-results",
    "synthesize": "log-decision + integrity-check",
    "write": "manuscript-draft",
    "integrity_pre_review": "integrity-check (gate 2.5)",
    "review": "peer-review",
    "revise": "revision-coaching",
    "re_review": "peer-review (re-review)",
    "integrity_final": "integrity-check (gate 4.5)",
    "finalize": "manuscript-finalize",
}

PHASE_AGENTS = {
    "bootstrap": "intake_agent",
    "discover": "literature_scout",
    "ideate": "hypothesis_generator",
    "plan": "methodology_critic",
    "execute": "experiment_runner",
    "analyze": "results_analyst",
    "synthesize": "integrity_auditor",
    "write": "manuscript_writer",
    "integrity_pre_review": "integrity_auditor",
    "review": "editor_in_chief",
    "revise": "revision_coach",
    "re_review": "editor_in_chief",
    "integrity_final": "integrity_auditor",
    "finalize": "manuscript_writer",
}

GATE_LABELS = {
    "integrity_pre_review": "ARS gate 2.5 (pre-review)",
    "integrity_final": "ARS gate 4.5 (pre-finalize)",
}


def _write_state(state: dict) -> None:
    with STATE_PATH.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(state, handle, sort_keys=False, allow_unicode=True)


def cmd_status() -> int:
    state = load_research_state()
    current = state.get("current_phase")
    nxt = next_phase(state)
    profile_name, modes = gate_modes_for_phase(current)
    print(f"mode: {state.get('mode')}")
    print(f"pipeline_profile: {state.get('pipeline_profile')}")
    print(f"current_phase: {current}")
    print(f"phases_enabled: {state.get('phases_enabled')}")
    print(f"pending_approval: {state.get('pending_approval')}")
    print(f"approved_by: {state.get('approved_by')}")
    print(f"gate_profile: {profile_name} ({', '.join(modes)})")
    if current in GATE_LABELS:
        print(f"gate_label: {GATE_LABELS[current]}")
    if nxt:
        print(f"next_phase: {nxt}")
        print(f"next_skill: {PHASE_SKILLS.get(nxt)}")
        print(f"next_agent: {PHASE_AGENTS.get(nxt)}")
    else:
        print("next_phase: <none> (complete or blocked)")
    return 0


def cmd_gate() -> int:
    schema_failures = validate_research()
    if schema_failures:
        for message in schema_failures:
            print(message, file=sys.stderr)
        return 1

    state = load_research_state()
    current = state.get("current_phase")
    profile_name, _ = gate_modes_for_phase(current)
    report = run_integrity_check(phase=current)

    if current in GATE_LABELS:
        print(f"gate: {GATE_LABELS[current]}")
    print(f"profile: {profile_name}")

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.mode}: {status}")
        for finding in result.findings:
            print(f"  - {finding}")

    ok, reasons = can_advance(state, report)
    preflight = autonomous_preflight(state)
    if preflight:
        print("autonomous preflight:", file=sys.stderr)
        for finding in preflight:
            print(f"  - {finding}", file=sys.stderr)
    if ok:
        print("GATE: PASS — safe to advance")
        return 0

    print("GATE: BLOCKED", file=sys.stderr)
    for reason in reasons:
        print(f"  - {reason}", file=sys.stderr)
    return 1


def cmd_approve(by: str) -> int:
    if by not in {"human", "ai"}:
        print("approved_by must be human or ai", file=sys.stderr)
        return 1
    state = load_research_state()
    if state.get("mode") == "hitl" and by != "human":
        print("hitl mode requires --by human", file=sys.stderr)
        return 1
    state["pending_approval"] = False
    state["approved_by"] = by
    state["approved_at"] = datetime.now(UTC).isoformat()
    _write_state(state)
    print(f"OK: approved_by={by}")
    return 0


def cmd_advance() -> int:
    schema_failures = validate_research()
    if schema_failures:
        for message in schema_failures:
            print(message, file=sys.stderr)
        return 1

    state = load_research_state()
    current = state.get("current_phase")
    report = run_integrity_check(phase=current)
    ok, reasons = can_advance(state, report)
    if not ok:
        for reason in reasons:
            print(reason, file=sys.stderr)
        return 1

    nxt = next_phase(state)
    if nxt is None:
        print("No next phase.", file=sys.stderr)
        return 1

    state["current_phase"] = nxt
    state["pending_approval"] = state.get("mode") == "hitl"
    state["approved_by"] = None
    state["approved_at"] = None
    _write_state(state)

    if PASSPORT_PATH.exists():
        passport = yaml.safe_load(PASSPORT_PATH.read_text(encoding="utf-8")) or {}
        passport["phase"] = nxt
        with PASSPORT_PATH.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(passport, handle, sort_keys=False, allow_unicode=True)

    print(f"OK: advanced to phase={nxt}")
    print(f"invoke skill: {PHASE_SKILLS.get(nxt)}")
    print(f"invoke agent: {PHASE_AGENTS.get(nxt)}")
    return 0


def cmd_profiles() -> int:
    print("Gate profiles:")
    for name, modes in GATE_PROFILES.items():
        print(f"  {name}: {', '.join(modes)}")
    return 0


def cmd_pipeline_profiles() -> int:
    print("Pipeline profiles (runtime/state/pipeline_profiles.yaml):")
    for name in list_pipeline_profile_names():
        print(f"  {name}")
    return 0


def cmd_apply_profile(name: str) -> int:
    try:
        result = apply_pipeline_profile(name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"OK: applied profile={result['profile']}")
    print(f"mode: {result['mode']}")
    print(f"current_phase: {result['current_phase']}")
    print(f"phases_enabled: {result['phases_enabled']}")
    skill = PHASE_SKILLS.get(result["current_phase"])
    agent = PHASE_AGENTS.get(result["current_phase"])
    if skill:
        print(f"invoke skill: {skill}")
    if agent:
        print(f"invoke agent: {agent}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Research pipeline orchestrator")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("status", help="Show current pipeline state")
    sub.add_parser("gate", help="Schema + phase-aware integrity gate")
    sub.add_parser("profiles", help="List integrity gate profiles (2.5 / 4.5 / default)")
    sub.add_parser("pipeline-profiles", help="List pipeline presets from pipeline_profiles.yaml")
    apply_prof = sub.add_parser("apply-profile", help="Apply a pipeline profile to research_state")
    apply_prof.add_argument("--name", required=True, help="Profile name, e.g. full-hitl")
    approve = sub.add_parser("approve", help="Record phase approval")
    approve.add_argument("--by", choices=["human", "ai"], required=True)
    sub.add_parser("advance", help="Advance to next enabled phase")

    args = parser.parse_args()
    if args.command == "status":
        return cmd_status()
    if args.command == "gate":
        return cmd_gate()
    if args.command == "profiles":
        return cmd_profiles()
    if args.command == "pipeline-profiles":
        return cmd_pipeline_profiles()
    if args.command == "apply-profile":
        return cmd_apply_profile(args.name)
    if args.command == "approve":
        return cmd_approve(args.by)
    if args.command == "advance":
        return cmd_advance()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
