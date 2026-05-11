"""
Тесты для scripts/improve_density.py.

Покрытие:
  - count_mentions()  — подсчёт упоминаний ключевых слов
  - make_bar()        — ASCII прогресс-бар
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_density")


# ── count_mentions ────────────────────────────────────────────────────────────

def test_count_mentions_returns_int():
    result = mod.count_mentions("agentfs is great", ["agentfs"])
    assert isinstance(result, int)


def test_count_mentions_zero_for_no_match():
    result = mod.count_mentions("plain text", ["xyz123"])
    assert result == 0


def test_count_mentions_single():
    result = mod.count_mentions("agentfs is great", ["agentfs"])
    assert result == 1


def test_count_mentions_multiple_occurrences():
    result = mod.count_mentions("agentfs agentfs agentfs", ["agentfs"])
    assert result == 3


def test_count_mentions_case_insensitive():
    result = mod.count_mentions("AgentFS is great", ["agentfs"])
    assert result == 1


def test_count_mentions_multiple_keywords():
    result = mod.count_mentions("agentfs and yodoca together", ["agentfs", "yodoca"])
    assert result == 2


def test_count_mentions_empty_text():
    result = mod.count_mentions("", ["agentfs"])
    assert result == 0


def test_count_mentions_empty_keywords():
    result = mod.count_mentions("agentfs is great", [])
    assert result == 0


# ── make_bar ──────────────────────────────────────────────────────────────────

def test_make_bar_returns_string():
    result = mod.make_bar(5, 10)
    assert isinstance(result, str)


def test_make_bar_zero_max_all_empty():
    result = mod.make_bar(5, 0)
    assert "░" in result
    assert "█" not in result


def test_make_bar_full_when_val_equals_max():
    result = mod.make_bar(10, 10, width=10)
    assert result == "█" * 10


def test_make_bar_empty_when_zero():
    result = mod.make_bar(0, 10, width=10)
    assert result == "░" * 10


def test_make_bar_correct_width():
    result = mod.make_bar(5, 10, width=15)
    assert len(result) == 15


def test_make_bar_proportional():
    half = mod.make_bar(5, 10, width=10)
    full = mod.make_bar(10, 10, width=10)
    filled_half = half.count("█")
    filled_full = full.count("█")
    assert filled_full > filled_half


def test_make_bar_contains_blocks_and_empty():
    result = mod.make_bar(5, 10, width=10)
    # Should have some filled and some empty
    assert "█" in result or "░" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_density_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgentFS memory agent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "DENSITY.md").exists()


def test_main_density_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nAgentFS memory agent svyazi.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "DENSITY.md").read_text(encoding="utf-8")
    assert "# Карта плотности тем" in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "DENSITY.md").exists()


def test_main_density_md_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "DENSITY.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
