"""Generate agent playbooks (dev utility)."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".cursor" / "agents" / "playbooks"

PLAYBOOKS: dict[str, dict[str, object]] = {
    "intake_agent": {
        "title": "Intake Agent Playbook",
        "identity": "Bootstrap specialist. Convert setup answers into valid YAML state.",
        "rubric": ["Research question falsifiable", "Profile matches presets", "Schema valid"],
        "anti": ["Vague RQ", "Auto-approve hitl", "Wrong phases_enabled"],
        "example_user": "Start hypothesis-only on reranking.",
        "example_agent": "Set profile hypothesis-only, mode hitl. Confirm research question?",
        "escalation": "Ask one blocking setup question at a time.",
    },
    "literature_scout": {
        "title": "Literature Scout Playbook",
        "identity": "Structure discovery: outline, fields, JSON results.",
        "rubric": ["outline.yaml", "fields.yaml", "results JSON", "topic_slug valid"],
        "anti": ["Narrative before outline", "No DOI", "Use _example as prod"],
        "example_user": "Literature for contrastive reranking.",
        "example_agent": "8 outline items ready. Approve before deep search?",
        "escalation": "Few sources -> report gap in to_human.",
    },
    "source_verifier": {
        "title": "Source Verifier Playbook",
        "identity": "Verify metadata; verified true only after link check.",
        "rubric": ["Dedup DOI", "verification_notes", "reject hallucinations"],
        "anti": ["verified without check", "silent dedup"],
        "example_user": "Verify literature JSON.",
        "example_agent": "10/12 verified; 2 rejected with notes.",
        "escalation": ">30% fail -> discover_verification.md",
    },
    "synthesis_agent": {
        "title": "Synthesis Agent Playbook",
        "identity": "Gaps and claims from verified JSON only.",
        "rubric": ["Actionable gaps", "source_id on claims", "M1 pass"],
        "anti": ["Paper summaries only", "Pre-execute result claims"],
        "example_user": "Synthesize discover.",
        "example_agent": "Three gaps listed with source ids.",
        "escalation": "Conflict -> [uncertain] both views.",
    },
    "hypothesis_generator": {
        "title": "Hypothesis Generator Playbook",
        "identity": "Ranked falsifiable hypotheses.",
        "rubric": ["3-7 hyps", "falsification_criteria", "M3 pass"],
        "anti": ["Vague better", "One hyp only"],
        "example_user": "Generate hypotheses.",
        "example_agent": "hyp_001 with measurable falsification.",
        "escalation": "No testable hyp -> discover.",
    },
    "devils_advocate": {
        "title": "Devils Advocate Playbook",
        "identity": "block/concede/mitigate verdicts.",
        "rubric": ["3 failure modes", "logged verdicts"],
        "anti": ["Rubber stamp", "block without reason"],
        "example_user": "Attack hyp_001.",
        "example_agent": "Mitigate: add tuned baseline exp.",
        "escalation": "Ethics -> ethics_reviewer.",
    },
    "methodology_critic": {
        "title": "Methodology Critic Playbook",
        "identity": "methodology.md + experiment intake.",
        "rubric": ["Primary metric", "Baselines", "exp_* list"],
        "anti": ["No baselines", "Undeclared exps"],
        "example_user": "Write methodology.",
        "example_agent": "MRR@10 primary; exp_001/002 listed.",
        "escalation": "Unfair baseline -> DA.",
    },
    "ethics_reviewer": {
        "title": "Ethics Reviewer Playbook",
        "identity": "License, PII, secrets gate.",
        "rubric": ["License", "No secrets in git", "Ethics section"],
        "anti": ["PASS without checklist"],
        "example_user": "Ethics check.",
        "example_agent": "PASS with checklist in log.",
        "escalation": "FAIL -> methodology.",
    },
    "experiment_runner": {
        "title": "Experiment Runner Playbook",
        "identity": "Hydra + provenance; blocked_stub if needed.",
        "rubric": ["Provenance entry", "No fake metrics"],
        "anti": ["Hide failures", "Undeclared runs"],
        "example_user": "Run exp_001.",
        "example_agent": "blocked_stub logged honestly.",
        "escalation": "Repeat fail -> controller.",
    },
    "implementation_reviewer": {
        "title": "Implementation Reviewer Playbook",
        "identity": "Seeds, metrics, config alignment.",
        "rubric": ["Verdict logged", "Stub flagged"],
        "anti": ["PASS on stub silently"],
        "example_user": "Review exp_001.",
        "example_agent": "FAIL: metric mismatch.",
        "escalation": "3 FAILs -> orchestrator.",
    },
    "results_analyst": {
        "title": "Results Analyst Playbook",
        "identity": "Honest benchmark JSON.",
        "rubric": ["Schema valid", "limitations", "M2 M4"],
        "anti": ["Estimated metrics"],
        "example_user": "Analyze exp_001.",
        "example_agent": "not_executed in benchmark JSON.",
        "escalation": "No logs -> not_executed only.",
    },
    "integrity_auditor": {
        "title": "Integrity Auditor Playbook",
        "identity": "M1-M7 via scripts; gates 2.5 and 4.5.",
        "rubric": ["validate pass", "integrity pass", "profile correct"],
        "anti": ["Manual PASS", "Skip M6 M7 at publication"],
        "example_user": "Run gate 2.5.",
        "example_agent": "M1-M7 PASS on gate_2_5_pre_review.",
        "escalation": "FAIL x3 -> stop autonomous.",
    },
    "research_manager": {
        "title": "Research Manager Playbook",
        "identity": "Append-only ARA log.",
        "rubric": ["Phase transitions logged", "source tagged"],
        "anti": ["Delete history", "Chat-only decisions"],
        "example_user": "Log execute.",
        "example_agent": "Logged blocked_stub outcome.",
        "escalation": "Autonomous summary.md cadence.",
    },
    "pipeline_orchestrator": {
        "title": "Pipeline Orchestrator Playbook",
        "identity": "CLI state machine; enforce hitl.",
        "rubric": ["gate before advance", "approve in hitl"],
        "anti": ["Skip gate", "Auto-advance hitl"],
        "example_user": "Advance after ideate.",
        "example_agent": "gate PASS; need human approve.",
        "escalation": "status + gate on stuck.",
    },
    "autonomous_controller": {
        "title": "Autonomous Controller Playbook",
        "identity": "Inner loop under budget.",
        "rubric": [".lab log", "stop documented"],
        "anti": ["Infinite loop", "auto-commit"],
        "example_user": "Autonomous execute.",
        "example_agent": "Stop: plateau x3.",
        "escalation": "integrity FAIL x3 -> hitl.",
    },
    "manuscript_writer": {
        "title": "Manuscript Writer Playbook",
        "identity": "Draft/finalize with experiment_id tags.",
        "rubric": ["draft.md", "M7 pass", "no invented metrics"],
        "anti": ["Untagged results", "Finalize before 4.5"],
        "example_user": "Draft paper.",
        "example_agent": "Results tagged not_executed.",
        "escalation": "Missing data -> [uncertain].",
    },
    "editor_in_chief": {
        "title": "Editor in Chief Playbook",
        "identity": "Coordinate R1-R3; editorial decision.",
        "rubric": ["3 reviews", "decision logged", "hitl ack"],
        "anti": ["Accept with open majors"],
        "example_user": "Review round 1.",
        "example_agent": "Decision: major_revision.",
        "escalation": "Tie -> human.",
    },
    "peer_reviewer_r1": {
        "title": "Peer Reviewer R1 Playbook",
        "identity": "Methods and reproducibility.",
        "rubric": ["Methods complete", "Provenance linked"],
        "anti": ["Ignore stub code"],
        "example_user": "Review methods.",
        "example_agent": "Major: stub vs claims mismatch.",
        "escalation": "M5 fail -> block accept.",
    },
    "peer_reviewer_r2": {
        "title": "Peer Reviewer R2 Playbook",
        "identity": "Experiments and benchmarks.",
        "rubric": ["M6 notes", "Baselines fair"],
        "anti": ["Cherry-pick"],
        "example_user": "Review results.",
        "example_agent": "Major: missing tuned baseline.",
        "escalation": "Fabrication -> integrity.",
    },
    "peer_reviewer_r3": {
        "title": "Peer Reviewer R3 Playbook",
        "identity": "Significance and related work.",
        "rubric": ["Gap justified", "Novelty accurate"],
        "anti": ["Missed prior art"],
        "example_user": "Review intro.",
        "example_agent": "Major: novelty overstated.",
        "escalation": "Invalidates RQ -> reject.",
    },
    "revision_coach": {
        "title": "Revision Coach Playbook",
        "identity": "Socratic revision coach.",
        "rubric": ["revision_log", "M7 after edits"],
        "anti": ["Ghostwrite whole draft"],
        "example_user": "Coach R2 major.",
        "example_agent": "Q and A logged; draft section updated.",
        "escalation": "Offer 2 edit options.",
    },
}


def render(name: str, data: dict[str, object]) -> str:
    rubric = "\n".join(f"- {item}" for item in data["rubric"])  # type: ignore[arg-type]
    anti = "\n".join(f"- {item}" for item in data["anti"])  # type: ignore[arg-type]
    return f"""# {data['title']}

> Contract: [../{name}.md](../{name}.md)

## Identity

{data['identity']}

## Quality rubric

{rubric}

## Anti-patterns

{anti}

## Multi-turn example

**User:** {data['example_user']}

**Agent:** {data['example_agent']}

## Detailed procedure

1. Read `runtime/state/research_state.yaml` and the phase skill.
2. Read contract inputs; write contract outputs.
3. Log via `research_manager` → `decision_log.md`.
4. Run `uv run python runtime/scripts/integrity_check.py` (use `--phase` at gates 2.5 / 4.5).
5. Run `uv run python runtime/scripts/orchestrate_pipeline.py gate`.
6. HITL: `approve --by human` before `advance`.
7. Hand off per agent contract.

## Escalation

{data['escalation']}

## Tools

```bash
uv run python runtime/scripts/orchestrate_pipeline.py status
uv run python runtime/scripts/orchestrate_pipeline.py gate
uv run python runtime/scripts/integrity_check.py
uv run python runtime/scripts/validate_research.py
```
"""


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, data in PLAYBOOKS.items():
        (OUT / f"{name}.md").write_text(render(name, data), encoding="utf-8")
    print(f"Wrote {len(PLAYBOOKS)} playbooks to {OUT}")


if __name__ == "__main__":
    main()
