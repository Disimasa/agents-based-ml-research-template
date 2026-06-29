"""Add playbook links to agent contract files."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AGENTS = ROOT / ".cursor" / "agents"


def main() -> None:
    for path in sorted(AGENTS.glob("*.md")):
        if path.name == "README.md":
            continue
        text = path.read_text(encoding="utf-8")
        name = path.stem
        link = f"**Deep playbook:** [playbooks/{name}.md](playbooks/{name}.md)"
        if link in text:
            continue
        lines = text.splitlines()
        out: list[str] = []
        inserted = False
        for index, line in enumerate(lines):
            out.append(line)
            if not inserted and line.startswith("# ") and index > 2:
                out.append("")
                out.append(link)
                inserted = True
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"updated {path.name}")


if __name__ == "__main__":
    main()
