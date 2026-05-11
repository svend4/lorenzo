"""Tests for scripts/improve_duplicate_across.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_duplicate_across")


def test_tokens_returns_list():
    result = mod._tokens("agent memory knowledge system")
    assert isinstance(result, list)


def test_tokens_removes_stopwords():
    result = mod._tokens("the and for or but in on at")
    assert "the" not in result
    assert "and" not in result


def test_tokens_min_3_chars():
    result = mod._tokens("ab abc abcd")
    for t in result:
        assert len(t) >= 3


def test_shingles_returns_set():
    tokens = ["agent", "memory", "system", "knowledge", "data"]
    result = mod._shingles(tokens, n=2)
    assert isinstance(result, set)


def test_shingles_correct_size():
    tokens = ["a", "b", "c", "d"]
    result = mod._shingles(tokens, n=2)
    assert len(result) == 3  # ab, bc, cd


def test_shingles_empty_when_too_short():
    tokens = ["a", "b"]
    result = mod._shingles(tokens, n=4)
    assert result == set()


def test_jaccard_shingle_returns_float():
    s_a = {"a b", "b c", "c d"}
    s_b = {"a b", "b c", "x y"}
    result = mod._jaccard_shingle(s_a, s_b)
    assert isinstance(result, float)


def test_jaccard_shingle_identical():
    s = {"a b", "b c", "c d"}
    result = mod._jaccard_shingle(s, s)
    assert result == 1.0


def test_jaccard_shingle_empty():
    result = mod._jaccard_shingle(set(), set())
    assert result == 0.0


def test_jaccard_shingle_no_overlap():
    s_a = {"a b"}
    s_b = {"c d"}
    result = mod._jaccard_shingle(s_a, s_b)
    assert result == 0.0


def test_word_overlap_returns_float():
    tok_a = ["agent", "memory", "system"]
    tok_b = ["agent", "knowledge", "system"]
    result = mod._word_overlap(tok_a, tok_b)
    assert isinstance(result, float)


def test_word_overlap_identical():
    tokens = ["agent", "memory", "system"]
    result = mod._word_overlap(tokens, tokens)
    assert result == 1.0


def test_word_overlap_no_overlap():
    tok_a = ["agent"]
    tok_b = ["memory"]
    result = mod._word_overlap(tok_a, tok_b)
    assert result == 0.0


def test_verdict_returns_string():
    result = mod._verdict(0.7)
    assert isinstance(result, str)


def test_verdict_high_similarity():
    result = mod._verdict(0.8)
    assert "Вероятный" in result


def test_verdict_medium_similarity():
    result = mod._verdict(0.5)
    assert "Значительное" in result


def test_verdict_low_similarity():
    result = mod._verdict(0.2)
    assert "Умеренное" in result
