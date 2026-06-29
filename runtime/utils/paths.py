"""Repository path constants."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATE_DIR = ROOT / "runtime" / "state"
RESEARCH_DIR = ROOT / "research"
SCHEMA_DIR = ROOT / "runtime" / "schemas"
TEMPLATES_DIR = ROOT / "runtime" / "templates"
BENCHMARKS_DIR = STATE_DIR / "benchmarks"
LITERATURE_STATE_DIR = STATE_DIR / "literature"
MANUSCRIPT_REVISION_LOG_PATH = STATE_DIR / "manuscript_revision_log.md"
REPORTS_DIR = ROOT / "reports"
