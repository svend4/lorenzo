"""
Тесты для scripts/improve_sentiment.py.

Покрытие:
  - count_words()  — подсчёт слов из списка
  - tone_label()   — определение тональности
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_sentiment")


# ── count_words ───────────────────────────────────────────────────────────────

def test_count_words_returns_int():
    result = mod.count_words("some text", ["some"])
    assert isinstance(result, int)


def test_count_words_zero_for_no_match():
    result = mod.count_words("plain text here", ["excellent", "optimal"])
    assert result == 0


def test_count_words_finds_single():
    result = mod.count_words("This is excellent work here.", ["excellent"])
    assert result == 1


def test_count_words_finds_multiple_occurrences():
    result = mod.count_words("риск риск риск", ["риск"])
    assert result == 3


def test_count_words_case_insensitive():
    result = mod.count_words("EXCELLENT quality here", ["excellent"])
    assert result == 1


def test_count_words_multiple_words():
    result = mod.count_words("excellent optimal performance", ["excellent", "optimal"])
    assert result == 2


def test_count_words_empty_text():
    result = mod.count_words("", ["excellent"])
    assert result == 0


def test_count_words_empty_list():
    result = mod.count_words("some text", [])
    assert result == 0


# ── tone_label ────────────────────────────────────────────────────────────────

def test_tone_label_returns_string():
    result = mod.tone_label(5, 2, 1, 1, 100)
    assert isinstance(result, str)


def test_tone_label_neutral_zero_total():
    result = mod.tone_label(0, 0, 0, 0, 0)
    assert result == "нейтральный"


def test_tone_label_optimistic():
    # pos > neg*2 and pos > urg
    result = mod.tone_label(10, 4, 3, 1, 100)
    assert "оптимистичный" in result


def test_tone_label_skeptical():
    # neg > pos*1.5
    result = mod.tone_label(2, 10, 1, 1, 100)
    assert "скептичный" in result


def test_tone_label_urgent():
    # urg > pos and urg > neg
    result = mod.tone_label(1, 1, 8, 0, 100)
    assert "срочный" in result


def test_tone_label_uncertain():
    # unc > pos and unc > neg
    result = mod.tone_label(1, 1, 0, 8, 100)
    assert "неопределённый" in result


def test_tone_label_neutral_balanced():
    # None of the above conditions
    result = mod.tone_label(3, 3, 3, 3, 100)
    assert "нейтральный" in result


def test_tone_label_optimistic_equal():
    # Exactly pos == neg*2 + 1
    result = mod.tone_label(11, 5, 2, 1, 100)
    assert "оптимистичный" in result


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_sentiment_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nОтличная архитектура! Быстрый поиск.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "SENTIMENT.md").exists()


def test_main_sentiment_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nПроблема памяти решена.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "SENTIMENT.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "SENTIMENT.md").exists()


def test_main_sentiment_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "SENTIMENT.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")
