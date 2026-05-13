"""Tests for scripts/improve_dependency_map.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_dependency_map")


def test_dependency_map_is_dict():
    assert hasattr(mod, "DEPENDENCY_MAP")
    assert isinstance(mod.DEPENDENCY_MAP, dict)


def test_dependency_map_not_empty():
    assert len(mod.DEPENDENCY_MAP) > 0


def test_dependency_map_entries_have_2_elements():
    for script, entry in mod.DEPENDENCY_MAP.items():
        assert len(entry) == 2, f"Entry for {script} must have (outputs, inputs)"


def test_dependency_map_outputs_are_lists():
    for script, (outputs, inputs) in mod.DEPENDENCY_MAP.items():
        assert isinstance(outputs, list), f"{script} outputs must be list"


def test_dependency_map_inputs_are_lists():
    for script, (outputs, inputs) in mod.DEPENDENCY_MAP.items():
        assert isinstance(inputs, list), f"{script} inputs must be list"


def test_dependency_map_has_search_index():
    assert "improve_search_index.py" in mod.DEPENDENCY_MAP


def test_dependency_map_has_health():
    assert "improve_health.py" in mod.DEPENDENCY_MAP


def test_dependency_map_search_index_output():
    outputs, inputs = mod.DEPENDENCY_MAP["improve_search_index.py"]
    assert any("search_index.json" in o for o in outputs)


def test_dependency_map_health_depends_on_metrics():
    _, inputs = mod.DEPENDENCY_MAP["improve_health.py"]
    assert any("METRICS" in i for i in inputs)


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_dependency_map_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DEPENDENCY_MAP.md").exists()


def test_main_dependency_map_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DEPENDENCY_MAP.md").read_text(encoding="utf-8")
    assert "improve_" in text
    assert "search_index" in text.lower() or "DEPENDENCY" in text


def test_main_dependency_map_is_markdown(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DEPENDENCY_MAP.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
