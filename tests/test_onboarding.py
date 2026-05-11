"""
Тесты для scripts/improve_onboarding.py.

Покрытие:
  - count_section()   — количество файлов и слов в разделе
  - get_scoring()     — чтение % из SCORING.md
  - get_script_count() — количество improve_*.py
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_onboarding")

# ── count_section ─────────────────────────────────────────────────────────────

def test_count_section_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_section("01-svyazi")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_count_section_empty_folder(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "01-svyazi").mkdir()
    files, words = mod.count_section("01-svyazi")
    assert files == 0
    assert words == 0


def test_count_section_nonexistent_returns_zeros(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    files, words = mod.count_section("nonexistent-section")
    assert files == 0
    assert words == 0


def test_count_section_counts_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    sec = tmp_path / "01-svyazi"
    sec.mkdir()
    (sec / "a.md").write_text("# A\n\nContent.", encoding="utf-8")
    (sec / "b.md").write_text("# B\n\nContent.", encoding="utf-8")
    files, _ = mod.count_section("01-svyazi")
    assert files == 2


def test_count_section_sums_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    sec = tmp_path / "01-svyazi"
    sec.mkdir()
    (sec / "a.md").write_text("one two three", encoding="utf-8")
    (sec / "b.md").write_text("four five", encoding="utf-8")
    _, words = mod.count_section("01-svyazi")
    assert words == 5


def test_count_section_returns_ints(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    files, words = mod.count_section("01-svyazi")
    assert isinstance(files, int)
    assert isinstance(words, int)


# ── get_scoring ───────────────────────────────────────────────────────────────

def test_get_scoring_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_scoring()
    assert isinstance(result, str)


def test_get_scoring_reads_from_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "SCORING.md").write_text("Итог: 96% — GO\n", encoding="utf-8")
    result = mod.get_scoring()
    assert result == "96%"


def test_get_scoring_default_when_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_scoring()
    assert result == "96%"


def test_get_scoring_contains_percent():
    result = mod.get_scoring()
    assert "%" in result


# ── get_script_count ──────────────────────────────────────────────────────────

def test_get_script_count_returns_int():
    result = mod.get_script_count()
    assert isinstance(result, int)


def test_get_script_count_positive():
    result = mod.get_script_count()
    assert result > 0


def test_get_script_count_with_mock(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "improve_a.py").write_text("", encoding="utf-8")
    (scripts / "improve_b.py").write_text("", encoding="utf-8")
    (scripts / "other.py").write_text("", encoding="utf-8")
    result = mod.get_script_count()
    assert result == 2


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_onboarding_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "SCORING.md").write_text("Балл: **96**/100", encoding="utf-8")
    mod.main()
    assert (tmp_path / "ONBOARDING.md").exists()


def test_main_onboarding_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "ONBOARDING.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "ONBOARDING.md").exists()


def test_main_onboarding_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "ONBOARDING.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
