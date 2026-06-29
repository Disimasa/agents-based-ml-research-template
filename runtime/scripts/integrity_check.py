"""CLI: automated integrity checks M1–M7."""

from __future__ import annotations

import argparse
import sys

from runtime.utils.integrity import run_integrity_check


def main() -> int:
    parser = argparse.ArgumentParser(description="Run research integrity checks M1–M7")
    parser.add_argument(
        "--modes",
        nargs="+",
        choices=["M1", "M2", "M3", "M4", "M5", "M6", "M7"],
        help="Subset of modes (overrides --phase profile)",
    )
    parser.add_argument(
        "--phase",
        help="Use gate profile for pipeline phase (e.g. integrity_pre_review for gate 2.5)",
    )
    args = parser.parse_args()

    report = run_integrity_check(modes=args.modes, phase=args.phase)
    if args.phase:
        print(f"gate_profile: {report.gate_profile}")

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"
        print(f"{result.mode}: {status}")
        for finding in result.findings:
            print(f"  - {finding}")

    if report.passed:
        print("OK: integrity checks passed")
        return 0

    print("FAIL: integrity checks failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
