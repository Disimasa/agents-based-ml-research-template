"""Validate research YAML against runtime/schemas/."""

from __future__ import annotations

import sys

from runtime.utils.validate import STATE_FILES, validate_research


def main() -> int:
    failures = validate_research(STATE_FILES)
    if failures:
        for message in failures:
            print(message, file=sys.stderr)
        return 1
    print(f"OK: validated {len(STATE_FILES)} state files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
