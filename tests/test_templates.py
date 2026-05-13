"""Tests for scripts/improve_templates.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_templates")


def test_templates_is_dict():
    assert hasattr(mod, "TEMPLATES")
    assert isinstance(mod.TEMPLATES, dict)


def test_templates_not_empty():
    assert len(mod.TEMPLATES) > 0


def test_templates_keys_are_strings():
    for key in mod.TEMPLATES:
        assert isinstance(key, str)


def test_templates_values_are_strings():
    for key, val in mod.TEMPLATES.items():
        assert isinstance(val, str), f"Template {key} value should be string"


def test_templates_have_md_extension():
    for key in mod.TEMPLATES:
        assert key.endswith(".md"), f"Template key {key} should end with .md"


def test_templates_have_h1():
    for key, val in mod.TEMPLATES.items():
        assert "# " in val, f"Template {key} should have H1 heading"


def test_templates_project_component_exists():
    assert "project-component.md" in mod.TEMPLATES


def test_templates_ensemble_exists():
    assert "ensemble.md" in mod.TEMPLATES


def test_templates_research_note_exists():
    assert "research-note.md" in mod.TEMPLATES


def test_templates_have_today_placeholder():
    for key, val in mod.TEMPLATES.items():
        assert "{today}" in val, f"Template {key} should have {{today}} placeholder"


def test_tmpl_path_attribute():
    assert hasattr(mod, "TMPL")
    assert isinstance(mod.TMPL, Path)


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_main_creates_templates(tmp_path, monkeypatch):
    tmpl_dir = tmp_path / "templates"
    monkeypatch.setattr(mod, "TMPL", tmpl_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TODAY", "2025-01-01")
    mod.main()
    assert tmpl_dir.exists()
    assert any(tmpl_dir.iterdir())


def test_main_creates_all_template_files(tmp_path, monkeypatch):
    tmpl_dir = tmp_path / "templates"
    monkeypatch.setattr(mod, "TMPL", tmpl_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TODAY", "2025-01-01")
    mod.main()
    created = {f.name for f in tmpl_dir.iterdir()}
    for key in mod.TEMPLATES:
        assert key in created, f"Template file {key} not created"


def test_main_fills_today(tmp_path, monkeypatch):
    tmpl_dir = tmp_path / "templates"
    monkeypatch.setattr(mod, "TMPL", tmpl_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "TODAY", "2025-01-01")
    mod.main()
    for key in mod.TEMPLATES:
        f = tmpl_dir / key
        text = f.read_text(encoding="utf-8")
        assert "{today}" not in text, f"Template {key} should have {{today}} filled"
        assert "2025-01-01" in text
