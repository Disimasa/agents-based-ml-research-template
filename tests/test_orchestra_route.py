"""Tests for Orchestra routing."""

from pathlib import Path

from src.utils.orchestra_route import load_skills_map, resolve_route


def test_skills_map_loads() -> None:
    data = load_skills_map()
    assert "routes" in data
    assert "execute" in data["routes"]


def test_resolve_execute_train_fallback() -> None:
    result = resolve_route("execute", "train")
    assert result["template_fallback"]["skill"] == "run-experiment"
    assert result["orchestra_available"] is False


def test_resolve_unknown_phase() -> None:
    result = resolve_route("nonexistent", "train")
    assert "error" in result


def test_map_file_exists() -> None:
    assert Path(".cursor/orchestra/SKILLS_MAP.yaml").exists()
