"""
Тесты для scripts/improve_validate.py.

Покрытие:
  - check_section_readmes()    — наличие README.md в разделах
  - check_meta_files()         — наличие обязательных мета-файлов
  - check_empty_files()        — файлы < 30 слов
  - check_naming()             — длинные кириллические имена
  - check_h1_titles()          — наличие заголовка H1
  - check_broken_internal()    — сломанные внутренние ссылки
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_validate")

# ── check_section_readmes ─────────────────────────────────────────────────────

def test_check_section_readmes_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_SECTIONS", [])
    result = mod.check_section_readmes()
    assert isinstance(result, list)


def test_check_section_readmes_missing_readme_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_SECTIONS", ["01-test"])
    (tmp_path / "01-test").mkdir()
    # No README.md created
    result = mod.check_section_readmes()
    assert len(result) == 1
    assert "01-test" in result[0]


def test_check_section_readmes_existing_readme_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_SECTIONS", ["01-test"])
    section = tmp_path / "01-test"
    section.mkdir()
    # Long enough README (>20 words)
    (section / "README.md").write_text("# Title\n\n" + "word " * 25, encoding="utf-8")
    result = mod.check_section_readmes()
    assert result == []


def test_check_section_readmes_short_readme_warned(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_SECTIONS", ["01-test"])
    section = tmp_path / "01-test"
    section.mkdir()
    (section / "README.md").write_text("# Short", encoding="utf-8")  # only 2 words
    result = mod.check_section_readmes()
    assert len(result) == 1


# ── check_meta_files ──────────────────────────────────────────────────────────

def test_check_meta_files_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_META_FILES", [])
    result = mod.check_meta_files()
    assert isinstance(result, list)


def test_check_meta_files_missing_file_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_META_FILES", ["README.md"])
    result = mod.check_meta_files()
    assert len(result) == 1
    assert "README.md" in result[0]


def test_check_meta_files_existing_file_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_META_FILES", ["README.md"])
    (tmp_path / "README.md").write_text("# Docs", encoding="utf-8")
    result = mod.check_meta_files()
    assert result == []


def test_check_meta_files_multiple_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "REQUIRED_META_FILES", ["README.md", "HEALTH.md"])
    result = mod.check_meta_files()
    assert len(result) == 2


# ── check_empty_files ─────────────────────────────────────────────────────────

def test_check_empty_files_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.check_empty_files()
    assert isinstance(result, list)


def test_check_empty_files_short_file_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    short_file = tmp_path / "short.md"
    short_file.write_text("# Title\n\nJust a few words.", encoding="utf-8")
    result = mod.check_empty_files()
    assert len(result) >= 1


def test_check_empty_files_long_file_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "long.md").write_text("# Title\n\n" + "word " * 50, encoding="utf-8")
    result = mod.check_empty_files()
    assert result == []


def test_check_empty_files_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.check_empty_files()
    assert result == []


# ── check_naming ──────────────────────────────────────────────────────────────

def test_check_naming_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.check_naming()
    assert isinstance(result, list)


def test_check_naming_normal_names_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    (tmp_path / "agent-memory.md").write_text("# Title", encoding="utf-8")
    result = mod.check_naming()
    assert result == []


def test_check_naming_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.check_naming()
    assert result == []


# ── check_h1_titles ───────────────────────────────────────────────────────────

def test_check_h1_titles_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.check_h1_titles()
    assert isinstance(result, list)


def test_check_h1_titles_file_without_h1_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "noh1.md"
    f.write_text("## Section\n\n" + "word " * 40, encoding="utf-8")
    result = mod.check_h1_titles()
    assert len(result) >= 1
    assert "noh1" in result[0]


def test_check_h1_titles_file_with_h1_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "withh1.md"
    f.write_text("# Title\n\n" + "word " * 40, encoding="utf-8")
    result = mod.check_h1_titles()
    assert result == []


def test_check_h1_titles_skips_short_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "tiny.md"
    f.write_text("## No H1 but very short", encoding="utf-8")
    result = mod.check_h1_titles()
    assert result == []


# ── check_broken_internal ─────────────────────────────────────────────────────

def test_check_broken_internal_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.check_broken_internal()
    assert isinstance(result, list)


def test_check_broken_internal_broken_link_detected(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "source.md"
    f.write_text("See [Missing](nonexistent.md) for details.", encoding="utf-8")
    result = mod.check_broken_internal()
    assert len(result) >= 1
    assert "nonexistent.md" in result[0]


def test_check_broken_internal_valid_link_no_issue(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    target = tmp_path / "target.md"
    target.write_text("# Target", encoding="utf-8")
    source = tmp_path / "source.md"
    source.write_text("See [Target](target.md) for details.", encoding="utf-8")
    result = mod.check_broken_internal()
    assert result == []


def test_check_broken_internal_http_links_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    f = tmp_path / "source.md"
    f.write_text("See [External](https://example.com) here.", encoding="utf-8")
    result = mod.check_broken_internal()
    assert result == []


def test_check_broken_internal_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path.parent)
    result = mod.check_broken_internal()
    assert result == []
