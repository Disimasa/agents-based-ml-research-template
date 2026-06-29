"""Validate pipeline.yaml and research_state.yaml."""

from __future__ import annotations

import sys

from runtime.utils.validate import validate_research

TARGETS = {
    "pipeline.yaml": "pipeline.schema.json",
    "research_state.yaml": "research_state.schema.json",
}


def main() -> int:
    failures = validate_research(TARGETS)
    if failures:
        for message in failures:
            print(message, file=sys.stderr)
        return 1
    print(f"OK: validated {len(TARGETS)} pipeline files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
