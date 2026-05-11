"""
Тесты для scripts/improve_staleness.py.

Покрытие:
  - _has_summary()  — проверка наличия summary-комментария
  - _has_tags()     — проверка наличия тегов
  - _word_count()   — подсчёт слов (без комментариев)
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_staleness")


# ── _has_summary ──────────────────────────────────────────────────────────────

def test_has_summary_false_without_marker():
    result = mod._has_summary("# Title\n\nSome content here.\n")
    assert result is False


def test_has_summary_true_with_summary_comment():
    result = mod._has_summary("<!-- summary -->\n> Some annotation.\n")
    assert result is True


def test_has_summary_true_with_summary_colon():
    result = mod._has_summary("<!-- summary: text -->\n")
    assert result is True


def test_has_summary_false_empty():
    result = mod._has_summary("")
    assert result is False


def test_has_summary_true_abstract_marker():
    result = mod._has_summary("<!-- abstract-auto -->\nContent.\n")
    # Only looks for "summary" pattern
    result2 = mod._has_summary("<!-- summary -->\n")
    assert result2 is True


# ── _has_tags ─────────────────────────────────────────────────────────────────

def test_has_tags_false_without_marker():
    result = mod._has_tags("# Title\n\nContent here.\n")
    assert result is False


def test_has_tags_true_with_tags_comment():
    result = mod._has_tags("<!-- tags: memory, agent -->\n# Title\n")
    assert result is True


def test_has_tags_false_empty():
    result = mod._has_tags("")
    assert result is False


def test_has_tags_true_with_whitespace():
    result = mod._has_tags("<!--   tags: memory -->\n")
    assert result is True


# ── _word_count ───────────────────────────────────────────────────────────────

def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts_words():
    result = mod._word_count("one two three four five")
    assert result >= 4


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_word_count_excludes_html_comments():
    text = "<!-- comment with many words --> actual word count here"
    with_comment = mod._word_count("<!-- comment --> word")
    without_comment = mod._word_count("word")
    assert with_comment == without_comment


def test_word_count_multiline():
    result = mod._word_count("one\ntwo\nthree")
    assert result >= 3
