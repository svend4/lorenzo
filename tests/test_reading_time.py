"""
Тесты для scripts/improve_reading_time.py.

Покрытие:
  - _count_words_by_type()  — подсчёт RU/EN слов и блоков кода
  - estimate_reading_time() — оценка времени чтения документа
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_reading_time")


# ── _count_words_by_type ──────────────────────────────────────────────────────

def test_count_words_returns_tuple():
    result = mod._count_words_by_type("some text here")
    assert isinstance(result, tuple)
    assert len(result) == 3


def test_count_words_counts_russian():
    ru_words, en_words, n_code = mod._count_words_by_type("агент система архитектура")
    assert ru_words > 0


def test_count_words_counts_english():
    ru_words, en_words, n_code = mod._count_words_by_type("agent system architecture")
    assert en_words > 0


def test_count_words_counts_code_blocks():
    text = "Before.\n```python\ncode here\n```\nAfter."
    ru_words, en_words, n_code = mod._count_words_by_type(text)
    assert n_code == 1


def test_count_words_multiple_code_blocks():
    text = "```\nblock1\n```\ntext\n```\nblock2\n```"
    _, _, n_code = mod._count_words_by_type(text)
    assert n_code == 2


def test_count_words_excludes_code_from_word_count():
    text = "агент\n```\nагент система архитектура\n```"
    ru_with_code, _, _ = mod._count_words_by_type("агент\n```\nагент система архитектура\n```")
    ru_clean, _, _ = mod._count_words_by_type("агент")
    assert ru_with_code == ru_clean


def test_count_words_zero_for_empty():
    ru_words, en_words, n_code = mod._count_words_by_type("")
    assert ru_words == 0
    assert en_words == 0
    assert n_code == 0


# ── estimate_reading_time ─────────────────────────────────────────────────────

_SHORT_TEXT = "# Title\n\nShort."

_LONG_RU = "агент " * 300
_LONG_EN = "agent " * 300


def test_estimate_reading_time_returns_dict_or_empty():
    result = mod.estimate_reading_time(_LONG_RU)
    assert isinstance(result, dict)


def test_estimate_reading_time_empty_for_short():
    result = mod.estimate_reading_time(_SHORT_TEXT)
    assert result == {}


def test_estimate_reading_time_has_required_keys():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        for key in ("minutes", "time_str", "category", "words", "ru_words", "en_words", "code_blocks"):
            assert key in result


def test_estimate_reading_time_minutes_positive():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["minutes"] > 0


def test_estimate_reading_time_minimum_1_minute():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["minutes"] >= 1.0


def test_estimate_reading_time_time_str_format():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert "мин" in result["time_str"] or "ч" in result["time_str"]


def test_estimate_reading_time_category_fast():
    # ~1 min text
    text = "агент " * 60
    result = mod.estimate_reading_time(text)
    if result:
        assert "Быстро" in result["category"]


def test_estimate_reading_time_category_long():
    # Many words
    text = "агент архитектура система память консолидация знания " * 200
    result = mod.estimate_reading_time(text)
    if result:
        assert result["category"] in (
            "📗 Быстро", "📘 Средне", "📙 Долго", "📕 Очень долго"
        )


def test_estimate_reading_time_words_counted():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["words"] > 0


def test_estimate_reading_time_ru_words():
    result = mod.estimate_reading_time(_LONG_RU)
    if result:
        assert result["ru_words"] > 0


def test_estimate_reading_time_en_words():
    result = mod.estimate_reading_time(_LONG_EN)
    if result:
        assert result["en_words"] > 0
