"""Tests for scripts/improve_vocabulary_richness.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_vocabulary_richness")


def test_ttr_returns_float():
    result = mod._ttr(["hello", "world", "hello"])
    assert isinstance(result, float)


def test_ttr_empty():
    result = mod._ttr([])
    assert result == 0.0


def test_ttr_all_unique():
    result = mod._ttr(["a", "b", "c", "d"])
    assert result == 1.0


def test_ttr_all_same():
    result = mod._ttr(["hello", "hello", "hello"])
    assert abs(result - 1/3) < 0.01


def test_sttr_returns_float():
    tokens = ["word"] * 200
    result = mod._sttr(tokens, window=100)
    assert isinstance(result, float)


def test_sttr_short_falls_back_to_ttr():
    tokens = ["hello", "world", "test"]
    result = mod._sttr(tokens, window=100)
    assert result == mod._ttr(tokens)


def test_hapax_counts_once():
    tokens = ["unique", "repeated", "repeated", "also_unique"]
    result = mod._hapax(tokens)
    assert result == 2


def test_hapax_empty():
    result = mod._hapax([])
    assert result == 0


def test_avg_word_len_returns_float():
    result = mod._avg_word_len(["hello", "world"])
    assert isinstance(result, float)


def test_avg_word_len_empty():
    result = mod._avg_word_len([])
    assert result == 0.0


def test_avg_word_len_correct():
    result = mod._avg_word_len(["abc", "de"])
    # (3+2)/2 = 2.5
    assert abs(result - 2.5) < 0.01


def test_unique_per_1000_returns_float():
    tokens = ["hello", "world", "hello", "test"]
    result = mod._unique_per_1000(tokens)
    assert isinstance(result, float)


def test_unique_per_1000_empty():
    result = mod._unique_per_1000([])
    assert result == 0.0


def test_all_tokens_returns_list():
    result = mod._all_tokens("Hello world привет мир")
    assert isinstance(result, list)


def test_all_tokens_lowercased():
    result = mod._all_tokens("HELLO WORLD")
    assert all(t == t.lower() for t in result)


def test_all_tokens_min_length_2():
    result = mod._all_tokens("I am in it at")
    for t in result:
        assert len(t) >= 2


def test_content_tokens_removes_stopwords():
    tokens = ["the", "for", "and", "agent", "memory"]
    result = mod._content_tokens(tokens)
    assert "the" not in result
    assert "agent" in result


def test_content_tokens_min_length_3():
    tokens = ["ok", "test", "data"]
    result = mod._content_tokens(tokens)
    for t in result:
        assert len(t) >= 3


def test_grade_returns_string():
    result = mod._grade(0.75)
    assert isinstance(result, str)


def test_grade_high_is_rich():
    result = mod._grade(0.80)
    assert "Богатый" in result


def test_grade_low_is_poor():
    result = mod._grade(0.30)
    assert "бедный" in result.lower()
