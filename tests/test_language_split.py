"""Tests for scripts/improve_language_split.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_language_split")


def test_clean_for_lang_returns_string():
    result = mod._clean_for_lang("some text")
    assert isinstance(result, str)


def test_clean_for_lang_removes_code():
    result = mod._clean_for_lang("Before\n```python\ncode\n```\nAfter")
    assert "code" not in result


def test_clean_for_lang_removes_urls():
    result = mod._clean_for_lang("See https://example.com for details.")
    assert "https" not in result


def test_lang_stats_returns_dict():
    result = mod._lang_stats("Hello world test")
    assert isinstance(result, dict)


def test_lang_stats_required_keys():
    result = mod._lang_stats("Hello world")
    for key in ("ru", "en", "total", "ru_ratio", "en_ratio", "label"):
        assert key in result


def test_lang_stats_empty():
    result = mod._lang_stats("")
    assert result["total"] == 0
    assert result["label"] == "empty"


def test_lang_stats_russian_text():
    result = mod._lang_stats("Привет мир тест данных проекта системы")
    assert result["label"] == "RU"
    assert result["ru_ratio"] > 0.7


def test_lang_stats_english_text():
    result = mod._lang_stats("Hello world test data project system analysis")
    assert result["label"] == "EN"
    assert result["en_ratio"] > 0.7


def test_lang_stats_mixed_text():
    ru_words = "Привет мир тест " * 5
    en_words = "Hello world test " * 5
    result = mod._lang_stats(ru_words + en_words)
    assert result["label"] == "MIX"


def test_lang_stats_counts_words():
    result = mod._lang_stats("hello world test")
    assert result["total"] >= 3
    assert result["en"] >= 3


def test_split_paragraphs_returns_tuple():
    result = mod._split_paragraphs_by_lang("Some text here")
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_split_paragraphs_russian_stays_in_ru():
    ru_text = "Привет мир тест данных проекта системы анализа"
    ru_out, en_out = mod._split_paragraphs_by_lang(ru_text)
    assert len(ru_out) > 0


def test_split_paragraphs_english_goes_to_en():
    en_text = "Hello world this is English text and data"
    ru_out, en_out = mod._split_paragraphs_by_lang(en_text)
    assert len(en_out) > 0


def test_lang_stats_ratios_sum_to_at_most_one():
    result = mod._lang_stats("Mixed текст with some английские words")
    assert result["ru_ratio"] + result["en_ratio"] <= 1.0 + 0.01
