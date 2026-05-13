"""Tests for scripts/improve_template_integrity.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_template_integrity")


def test_pollution_patterns_is_list():
    assert hasattr(mod, "POLLUTION_PATTERNS")
    assert isinstance(mod.POLLUTION_PATTERNS, list)
    assert len(mod.POLLUTION_PATTERNS) > 0


def test_find_pollutions_returns_list():
    result = mod.find_pollutions("# Clean document\n\nNo pollution here.\n")
    assert isinstance(result, list)


def test_find_pollutions_clean_text():
    result = mod.find_pollutions("# Title\n\n## Section\n\nContent here.\n")
    assert result == []


def test_find_pollutions_detects_alert_added():
    text = "# Title\n<!-- alert-added -->\n\nContent.\n"
    result = mod.find_pollutions(text)
    assert len(result) >= 1
    assert any("alert-added" in desc for desc, _ in result)


def test_find_pollutions_returns_position():
    text = "# Title\n<!-- alert-added -->\n\nContent.\n"
    result = mod.find_pollutions(text)
    for desc, pos in result:
        assert isinstance(pos, int)
        assert pos >= 0


def test_clean_pollutions_returns_tuple():
    result = mod.clean_pollutions("# Title\n\nContent.\n")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_clean_pollutions_clean_text():
    text = "# Title\n\nContent.\n"
    new_text, count = mod.clean_pollutions(text)
    assert count == 0
    assert new_text == text


def test_clean_pollutions_removes_alert_added():
    text = "# Title\n<!-- alert-added -->\n\nContent.\n"
    new_text, count = mod.clean_pollutions(text)
    assert count > 0
    assert "<!-- alert-added -->" not in new_text


def test_check_frontmatter_unique_returns_list():
    text = "# Title\n\nContent without frontmatter.\n"
    result = mod.check_frontmatter_unique(text)
    assert isinstance(result, list)


def test_check_frontmatter_unique_valid():
    text = "---\ntitle: Test\ndate: 2024-01-01\n---\n\n# Test\n\nContent.\n"
    result = mod.check_frontmatter_unique(text)
    assert isinstance(result, list)


def test_check_title_match_returns_list():
    text = "---\ntitle: My Title\n---\n\n# My Title\n\nContent.\n"
    result = mod.check_title_match(text)
    assert isinstance(result, list)


def test_check_title_match_no_frontmatter():
    text = "# Title\n\nContent without frontmatter.\n"
    result = mod.check_title_match(text)
    assert result == []


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_templates_dir_returns_one(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES", tmp_path / "nonexistent-templates")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = mod.main()
    assert result == 1


def test_main_empty_templates_no_crash(tmp_path, monkeypatch):
    templates = tmp_path / "templates"
    templates.mkdir()
    monkeypatch.setattr(mod, "TEMPLATES", templates)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    result = mod.main()
    assert result is None or result == 0


def test_main_with_clean_template(tmp_path, monkeypatch):
    templates = tmp_path / "templates"
    templates.mkdir()
    f = templates / "note.md"
    f.write_text("---\ntitle: Note\n---\n\n# Note\n\nContent.\n", encoding="utf-8")
    monkeypatch.setattr(mod, "TEMPLATES", templates)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()
