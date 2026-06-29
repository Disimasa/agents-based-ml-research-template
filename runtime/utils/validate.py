"""YAML/JSON validation against shared schemas."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema
import yaml

from runtime.utils.paths import SCHEMA_DIR, STATE_DIR

STATE_FILES = {
    "passport.yaml": "passport.schema.json",
    "research_state.yaml": "research_state.schema.json",
    "pipeline.yaml": "pipeline.schema.json",
    "hypotheses.yaml": "hypotheses.schema.json",
    "experiment_provenance.yaml": "experiment_provenance.schema.json",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return data if isinstance(data, dict) else {}


def validate_file(yaml_name: str, schema_name: str) -> list[str]:
    yaml_path = STATE_DIR / yaml_name
    schema_path = SCHEMA_DIR / schema_name
    if not yaml_path.exists():
        return [f"missing file: {yaml_path}"]
    if not schema_path.exists():
        return [f"missing schema: {schema_path}"]

    data = load_yaml(yaml_path)
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(data), key=lambda err: list(err.path))
    return [f"{yaml_name}: {error.message}" for error in errors]


def validate_research(files: dict[str, str] | None = None) -> list[str]:
    targets = files or STATE_FILES
    failures: list[str] = []
    for yaml_name, schema_name in targets.items():
        failures.extend(validate_file(yaml_name, schema_name))
    return failures
