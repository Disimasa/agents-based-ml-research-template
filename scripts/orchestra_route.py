"""CLI: resolve Orchestra routing from .cursor/orchestra/SKILLS_MAP.yaml."""

from __future__ import annotations

import argparse
import json
import sys

from src.utils.orchestra_route import (
    installed_orchestra_skills,
    list_routes,
    load_skills_map,
    resolve_route,
)


def cmd_list() -> int:
    data = load_skills_map()
    install_dir = (data.get("install") or {}).get("install_dir", ".cursor/skills/orchestra")
    installed = installed_orchestra_skills(install_dir)
    print(f"install_dir: {install_dir}")
    print(f"installed ({len(installed)}): {', '.join(installed) if installed else '<none>'}")
    print()
    for row in list_routes(map_data=data):
        print(
            f"{row['phase']}.{row['task']}: "
            f"orchestra=[{row['orchestra_matched']}] "
            f"fallback={row['fallback_skill']} ({row['fallback_agent']})"
        )
    return 0


def cmd_resolve(phase: str, task: str, as_json: bool) -> int:
    result = resolve_route(phase, task)
    if as_json:
        print(json.dumps(result, indent=2))
    else:
        if result.get("error"):
            print(f"ERROR: {result['error']}", file=sys.stderr)
            return 1
        if result["orchestra_available"]:
            print(f"route: orchestra/{result['use_orchestra_skill']}")
        else:
            fb = result["template_fallback"]
            print(f"route: template/{fb.get('skill')} (agent: {fb.get('agent')})")
        if result.get("external_bridge"):
            print(f"external_bridge: {result['external_bridge']} (opt-in)")
        if result.get("notes"):
            print(f"notes: {result['notes']}")
    return 0 if not result.get("error") else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Orchestra skill routing")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="List all routes and install status")
    resolve = sub.add_parser("resolve", help="Resolve route for phase + task")
    resolve.add_argument("phase", help="e.g. execute, analyze")
    resolve.add_argument("task", help="e.g. train, eval")
    resolve.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.command == "list":
        return cmd_list()
    if args.command == "resolve":
        return cmd_resolve(args.phase, args.task, args.json)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
