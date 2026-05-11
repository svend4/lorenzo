"""
Тесты для scripts/improve_similar.py.

Покрытие:
  - tokenize()  — токенизация текста с фильтром стоп-слов
  - jaccard()   — сходство Жаккара двух множеств
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_similar")


# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_set():
    result = mod.tokenize("agent memory architecture")
    assert isinstance(result, set)


def test_tokenize_lowercases():
    result = mod.tokenize("AGENT Memory")
    assert "agent" in result
    assert "memory" in result


def test_tokenize_min_length_4():
    result = mod.tokenize("аб абв агент памят архитектур")
    for t in result:
        assert len(t) >= 4


def test_tokenize_filters_stopwords():
    result = mod.tokenize("и в не на что с по это как из")
    assert len(result) == 0


def test_tokenize_strips_code_blocks():
    result_with_code = mod.tokenize("```\nagent memory\n```")
    result_clean = mod.tokenize("agent memory")
    assert result_with_code != result_clean or len(result_with_code) == 0


def test_tokenize_empty():
    result = mod.tokenize("")
    assert result == set()


def test_tokenize_keeps_real_words():
    result = mod.tokenize("архитектура системы поиск память агент")
    assert len(result) > 0


# ── jaccard ───────────────────────────────────────────────────────────────────

def test_jaccard_returns_float():
    result = mod.jaccard({"a", "b"}, {"b", "c"})
    assert isinstance(result, float)


def test_jaccard_identical_sets():
    s = {"agent", "memory", "search"}
    result = mod.jaccard(s, s)
    assert result == 1.0


def test_jaccard_disjoint_sets():
    result = mod.jaccard({"agent"}, {"memory"})
    assert result == 0.0


def test_jaccard_empty_sets():
    result = mod.jaccard(set(), set())
    assert result == 0.0


def test_jaccard_one_empty():
    result = mod.jaccard({"agent"}, set())
    assert result == 0.0


def test_jaccard_symmetric():
    a = {"agent", "memory"}
    b = {"memory", "search"}
    assert mod.jaccard(a, b) == mod.jaccard(b, a)


def test_jaccard_range():
    a = {"agent", "memory", "search"}
    b = {"memory", "search", "graph"}
    result = mod.jaccard(a, b)
    assert 0.0 <= result <= 1.0


def test_jaccard_partial_overlap():
    a = {"agent", "memory"}
    b = {"agent", "search"}
    result = mod.jaccard(a, b)
    # intersection = {agent}, union = {agent, memory, search}
    assert abs(result - 1/3) < 1e-9
