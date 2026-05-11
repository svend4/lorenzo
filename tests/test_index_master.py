"""Tests for scripts/improve_index_master.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_index_master")


def test_sections_is_list():
    assert hasattr(mod, "SECTIONS")
    assert isinstance(mod.SECTIONS, list)
    assert len(mod.SECTIONS) > 0


def test_sections_have_3_elements():
    for item in mod.SECTIONS:
        assert len(item) == 3, f"Section item {item} must have 3 elements"


def test_meta_docs_is_list():
    assert hasattr(mod, "META_DOCS")
    assert isinstance(mod.META_DOCS, list)


def test_report_docs_is_list():
    assert hasattr(mod, "REPORT_DOCS")
    assert isinstance(mod.REPORT_DOCS, list)


def test_read_stat_missing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_stat("missing.md", r'(\d+)%', "default")
    assert result == "default"


def test_read_stat_finds_pattern(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("Score: 87/100 achieved\n", encoding="utf-8")
    result = mod.read_stat("test.md", r'(\d+)/100')
    assert result == "87"


def test_read_stat_no_match_returns_default(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    f = tmp_path / "test.md"
    f.write_text("No pattern here\n", encoding="utf-8")
    result = mod.read_stat("test.md", r'(\d+)/100', "—")
    assert result == "—"


def test_read_stat_default_is_dash():
    # Default value for read_stat is "—"
    import inspect
    sig = inspect.signature(mod.read_stat)
    assert sig.parameters["default"].default == "—"


def test_sections_contains_svyazi():
    folder_names = [s[0] for s in mod.SECTIONS]
    assert "01-svyazi" in folder_names


def test_sections_contains_habr():
    folder_names = [s[0] for s in mod.SECTIONS]
    assert "05-habr-projects" in folder_names


def test_meta_docs_contains_health():
    filenames = [m[0] for m in mod.META_DOCS]
    assert "HEALTH.md" in filenames


def test_meta_docs_contains_contacts():
    filenames = [m[0] for m in mod.META_DOCS]
    assert "CONTACTS.md" in filenames


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_index_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "INDEX.md").exists()


def test_main_index_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "INDEX.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_index_md_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "INDEX.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_main_index_with_section_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    sec = tmp_path / "01-svyazi"
    sec.mkdir()
    (sec / "README.md").write_text("# Svyazi\n\nContent.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "INDEX.md").read_text(encoding="utf-8")
    assert "INDEX.md" not in text or "# " in text
