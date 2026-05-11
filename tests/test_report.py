"""
Тесты для scripts/improve_report.py.

Покрытие:
  - read_metric()       — извлечение метрики из файла по regex
  - count_files()       — количество .md файлов и суммарные слова
  - get_section_counts()— количество файлов в каждом разделе
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_report")

# ── read_metric ───────────────────────────────────────────────────────────────

def test_read_metric_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("HEALTH.md", r'(\d+)', default="?")
    assert isinstance(result, str)


def test_read_metric_extracts_value(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "HEALTH.md").write_text("Score: **87/100**\n", encoding="utf-8")
    result = mod.read_metric("HEALTH.md", r'\*\*(\d+)/100\*\*', default="?")
    assert result == "87"


def test_read_metric_returns_default_for_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("NONEXISTENT.md", r'(\d+)', default="42")
    assert result == "42"


def test_read_metric_returns_default_for_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "METRICS.md").write_text("No matching content here.", encoding="utf-8")
    result = mod.read_metric("METRICS.md", r'Score: (\d+)', default="0")
    assert result == "0"


def test_read_metric_first_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "KPI.md").write_text("Count: 100\nAnother: 200\n", encoding="utf-8")
    result = mod.read_metric("KPI.md", r'(\d+)', default="?")
    assert result == "100"


# ── count_files ───────────────────────────────────────────────────────────────

def test_count_files_returns_tuple(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_files()
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_count_files_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    count, words = mod.count_files()
    assert count == 0
    assert words == 0


def test_count_files_counts_md_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("# Title\n\nContent.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Another\n\nMore content.", encoding="utf-8")
    count, words = mod.count_files()
    assert count == 2


def test_count_files_sums_words(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("one two three", encoding="utf-8")
    (tmp_path / "b.md").write_text("four five", encoding="utf-8")
    _, words = mod.count_files()
    assert words == 5


def test_count_files_returns_ints(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    count, words = mod.count_files()
    assert isinstance(count, int)
    assert isinstance(words, int)


# ── get_section_counts ────────────────────────────────────────────────────────

def test_get_section_counts_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_section_counts()
    assert isinstance(result, dict)


def test_get_section_counts_empty_when_no_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_section_counts()
    assert result == {}


def test_get_section_counts_counts_md_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    sec = tmp_path / "01-svyazi"
    sec.mkdir()
    (sec / "a.md").write_text("# A", encoding="utf-8")
    (sec / "b.md").write_text("# B", encoding="utf-8")
    result = mod.get_section_counts()
    assert result.get("01-svyazi") == 2


def test_get_section_counts_skips_nonexistent_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    # Only create one section
    (tmp_path / "01-svyazi").mkdir()
    (tmp_path / "01-svyazi" / "test.md").write_text("# T", encoding="utf-8")
    result = mod.get_section_counts()
    assert "02-anthropic-vacancies" not in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_report_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "REPORT.md").exists()


def test_main_report_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "REPORT.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "REPORT.md").exists()


def test_main_report_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "REPORT.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
