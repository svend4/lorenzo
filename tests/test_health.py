"""
Тесты для scripts/improve_health.py.

Покрытие:
  - count_files()    — количество .md файлов и суммарных слов
  - read_metric()    — извлечение метрики из файла по regex
  - score_to_emoji() — цветной индикатор по баллу
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_health")

# ── count_files ───────────────────────────────────────────────────────────────

def test_count_files_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_files()
    assert isinstance(result, dict)


def test_count_files_has_required_keys(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_files()
    assert "total_files" in result
    assert "total_words" in result
    assert "sections" in result


def test_count_files_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.count_files()
    assert result["total_files"] == 0
    assert result["total_words"] == 0


def test_count_files_counts_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "a.md").write_text("# Title\n\nContent.", encoding="utf-8")
    (tmp_path / "b.md").write_text("# Other\n\nMore.", encoding="utf-8")
    result = mod.count_files()
    assert result["total_files"] == 2


def test_count_files_groups_by_section(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    sec = tmp_path / "01-svyazi"
    sec.mkdir()
    (sec / "test.md").write_text("# Test", encoding="utf-8")
    (tmp_path / "root.md").write_text("# Root", encoding="utf-8")
    result = mod.count_files()
    sections = result["sections"]
    assert "01-svyazi" in sections
    assert "root" in sections


# ── read_metric ───────────────────────────────────────────────────────────────

def test_read_metric_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("HEALTH.md", r'(\d+)', "?")
    assert isinstance(result, str)


def test_read_metric_extracts_value(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "HEALTH.md").write_text("Score: 87/100\n", encoding="utf-8")
    result = mod.read_metric("HEALTH.md", r'(\d+)', "?")
    assert result == "87"


def test_read_metric_default_for_missing(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.read_metric("NONEXISTENT.md", r'(\d+)', "99")
    assert result == "99"


def test_read_metric_default_for_no_match(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    (tmp_path / "METRICS.md").write_text("No numbers here.", encoding="utf-8")
    result = mod.read_metric("METRICS.md", r'Score: (\d+)', "0")
    assert result == "0"


# ── score_to_emoji ────────────────────────────────────────────────────────────

def test_score_to_emoji_returns_string():
    assert isinstance(mod.score_to_emoji(80), str)


def test_score_to_emoji_green_at_90():
    assert mod.score_to_emoji(90) == "🟢"


def test_score_to_emoji_green_at_100():
    assert mod.score_to_emoji(100) == "🟢"


def test_score_to_emoji_yellow_at_70():
    assert mod.score_to_emoji(70) == "🟡"


def test_score_to_emoji_yellow_at_89():
    assert mod.score_to_emoji(89) == "🟡"


def test_score_to_emoji_orange_at_50():
    assert mod.score_to_emoji(50) == "🟠"


def test_score_to_emoji_orange_at_69():
    assert mod.score_to_emoji(69) == "🟠"


def test_score_to_emoji_red_at_49():
    assert mod.score_to_emoji(49) == "🔴"


def test_score_to_emoji_red_at_0():
    assert mod.score_to_emoji(0) == "🔴"
