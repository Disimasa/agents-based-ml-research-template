"""Validate runtime/state/benchmarks/*.json."""

from __future__ import annotations

import json
import sys

import jsonschema

from runtime.utils.paths import BENCHMARKS_DIR, SCHEMA_DIR


def main() -> int:
    schema_path = SCHEMA_DIR / "benchmark_report.schema.json"
    if not schema_path.exists():
        print(f"missing schema: {schema_path}", file=sys.stderr)
        return 1

    reports = sorted(BENCHMARKS_DIR.glob("*.json"))
    if not reports:
        print("OK: no benchmark reports to validate")
        return 0

    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    failures: list[str] = []

    for report_path in reports:
        data = json.loads(report_path.read_text(encoding="utf-8"))
        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
        failures.extend(f"{report_path.name}: {error.message}" for error in errors)

    if failures:
        for message in failures:
            print(message, file=sys.stderr)
        return 1

    print(f"OK: validated {len(reports)} benchmark report(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
