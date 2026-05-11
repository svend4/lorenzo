"""
Тесты для scripts/improve_word_freq.py.

Покрытие:
  - tokenize()  — токенизация с удалением стопслов и кода
  - top_words() — топ-N слов по частоте
  - make_bar()  — текстовая полоса прогресса
"""

import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_word_freq")

# ── tokenize ──────────────────────────────────────────────────────────────────

def test_tokenize_returns_list():
    assert isinstance(mod.tokenize("some text here"), list)


def test_tokenize_lowercases():
    result = mod.tokenize("AgentFS Memory Consolidation")
    assert all(t == t.lower() for t in result)


def test_tokenize_removes_stopwords():
    result = mod.tokenize("и в на что как это для или но the a an")
    assert result == []


def test_tokenize_keeps_content_words():
    result = mod.tokenize("агент память консолидация yodoca agentfs")
    assert "агент" in result
    assert "память" in result


def test_tokenize_min_length_3():
    result = mod.tokenize("ab abc abcd")
    assert "ab" not in result
    assert "abc" in result


def test_tokenize_removes_code_blocks():
    text = "text\n```python\nprint('hello')\n```\nmore text"
    result = mod.tokenize(text)
    assert "print" not in result


def test_tokenize_removes_urls():
    result = mod.tokenize("see https://github.com/user/repo here")
    assert not any("http" in t for t in result)


def test_tokenize_empty_text():
    assert mod.tokenize("") == []


# ── top_words ─────────────────────────────────────────────────────────────────

def test_top_words_returns_list():
    result = mod.top_words(["агент", "память", "агент"])
    assert isinstance(result, list)


def test_top_words_returns_tuples():
    result = mod.top_words(["агент", "память", "агент"])
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2


def test_top_words_respects_n():
    words = ["a", "b", "c", "d", "e"] * 5
    result = mod.top_words(words, n=3)
    assert len(result) == 3


def test_top_words_sorted_by_frequency():
    words = ["агент"] * 5 + ["память"] * 3 + ["граф"] * 1
    result = mod.top_words(words, n=3)
    counts = [r[1] for r in result]
    assert counts == sorted(counts, reverse=True)


def test_top_words_most_frequent_first():
    words = ["агент"] * 10 + ["память"] * 3
    result = mod.top_words(words, n=2)
    assert result[0][0] == "агент"
    assert result[0][1] == 10


def test_top_words_empty_list():
    result = mod.top_words([])
    assert result == []


# ── make_bar ──────────────────────────────────────────────────────────────────

def test_make_bar_returns_string():
    result = mod.make_bar(5, 10)
    assert isinstance(result, str)


def test_make_bar_correct_length():
    result = mod.make_bar(5, 10, width=20)
    assert len(result) == 20


def test_make_bar_full_bar():
    result = mod.make_bar(10, 10, width=10)
    assert result == "█" * 10


def test_make_bar_empty_bar():
    result = mod.make_bar(0, 10, width=10)
    assert result == "░" * 10


def test_make_bar_half_filled():
    result = mod.make_bar(5, 10, width=10)
    filled = result.count("█")
    empty = result.count("░")
    assert filled == 5
    assert empty == 5


def test_make_bar_proportional():
    short = mod.make_bar(2, 10, width=20)
    long_ = mod.make_bar(8, 10, width=20)
    assert short.count("█") < long_.count("█")
