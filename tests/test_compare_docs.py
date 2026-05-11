"""
Тесты для scripts/improve_compare_docs.py.

Покрытие:
  - _clean()          — удаление кода, URL, комментариев
  - _tokens()         — токенизация с фильтрацией стоп-слов
  - _headings()       — извлечение заголовков
  - _word_count()     — подсчёт слов
  - compare_two()     — сравнение двух файлов
  - format_comparison() — форматирование результата
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_compare_docs")


# ── _clean ────────────────────────────────────────────────────────────────────

def test_clean_returns_lowercase():
    result = mod._clean("UPPER CASE Text")
    assert result == result.lower()


def test_clean_removes_code_block():
    result = mod._clean("before\n```python\ncode here\n```\nafter")
    assert "code here" not in result


def test_clean_removes_inline_code():
    result = mod._clean("Use `function()` here.")
    assert "function()" not in result


def test_clean_removes_url():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_clean_removes_html_comments():
    result = mod._clean("before <!-- comment --> after")
    assert "comment" not in result


# ── _tokens ───────────────────────────────────────────────────────────────────

def test_tokens_returns_list():
    result = mod._tokens("агент память архитектура")
    assert isinstance(result, list)


def test_tokens_min_length_4():
    result = mod._tokens("а аб абв абвг абвгд")
    for t in result:
        assert len(t) >= 4


def test_tokens_filters_stopwords():
    result = mod._tokens("это как но или что")
    assert len(result) == 0


def test_tokens_finds_real_words():
    result = mod._tokens("архитектура системы проектирование")
    assert len(result) > 0


def test_tokens_case_insensitive():
    result = mod._tokens("Агент ПАМЯТЬ архитектура")
    assert "агент" in result
    assert "память" in result


# ── _headings ─────────────────────────────────────────────────────────────────

def test_headings_returns_list():
    result = mod._headings("# Title\n## Section\n### Sub")
    assert isinstance(result, list)


def test_headings_extracts_h1():
    result = mod._headings("# Title")
    assert "Title" in result


def test_headings_extracts_h2():
    result = mod._headings("## Section Name")
    assert "Section Name" in result


def test_headings_extracts_h3():
    result = mod._headings("### Sub Section")
    assert "Sub Section" in result


def test_headings_empty_text():
    result = mod._headings("No headings here")
    assert result == []


def test_headings_removes_formatting():
    result = mod._headings("## **Bold** Heading")
    assert "Bold" in result[0]
    assert "**" not in result[0]


# ── _word_count ───────────────────────────────────────────────────────────────

def test_word_count_returns_int():
    result = mod._word_count("one two three")
    assert isinstance(result, int)


def test_word_count_counts_correctly():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_word_count_multiline():
    result = mod._word_count("one\ntwo\nthree")
    assert result == 3


# ── compare_two ───────────────────────────────────────────────────────────────

def test_compare_two_returns_dict(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент обрабатывает информацию и отвечает на вопросы пользователя.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранит знания через архитектуру памяти агента.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert isinstance(result, dict)


def test_compare_two_has_required_keys(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент обрабатывает информацию и отвечает.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранит знания через архитектуру.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    for key in ("jaccard", "common_words", "unique_a", "unique_b",
                "common_heads", "only_heads_a", "only_heads_b",
                "words_a", "words_b", "size_ratio"):
        assert key in result, f"Missing key: {key}"


def test_compare_two_jaccard_identical(tmp_path):
    text = "# Title\n\nАгент обрабатывает информацию память архитектура.\n"
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text(text, encoding="utf-8")
    b.write_text(text, encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["jaccard"] == 1.0


def test_compare_two_jaccard_disjoint(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nархитектура система кластер граф модель байесовская\n", encoding="utf-8")
    b.write_text("# B\n\npython javascript typescript react frontend backend\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["jaccard"] < 0.5


def test_compare_two_jaccard_range(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nАгент обрабатывает информацию через архитектуру.\n", encoding="utf-8")
    b.write_text("# B\n\nСистема хранит знания через граф памяти.\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert 0.0 <= result["jaccard"] <= 1.0


def test_compare_two_paths_stored(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\ntext here\n", encoding="utf-8")
    b.write_text("# B\n\ntext here\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["path_a"] == a
    assert result["path_b"] == b


def test_compare_two_word_counts(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\none two three\n", encoding="utf-8")
    b.write_text("# B\n\none two three four five six\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert result["words_a"] < result["words_b"]


def test_compare_two_common_headings(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Title\n## Shared Section\n## Only A\n", encoding="utf-8")
    b.write_text("# Title\n## Shared Section\n## Only B\n", encoding="utf-8")
    result = mod.compare_two(a, b)
    assert "Shared Section" in result["common_heads"]


# ── format_comparison ─────────────────────────────────────────────────────────

def test_format_comparison_returns_list(tmp_path):
    monkeypatch_root = tmp_path
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# Doc A\n\nАгент архитектура память консолидация.\n", encoding="utf-8")
    b.write_text("# Doc B\n\nСистема хранения знаний через граф.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    assert isinstance(result, list)


def test_format_comparison_contains_jaccard(tmp_path):
    a = tmp_path / "a.md"
    b = tmp_path / "b.md"
    a.write_text("# A\n\nАгент архитектура память консолидация.\n", encoding="utf-8")
    b.write_text("# B\n\nАгент архитектура память консолидация.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    text = "\n".join(result)
    assert "Jaccard" in text or "jaccard" in text or "%" in text


def test_format_comparison_has_filenames(tmp_path):
    a = tmp_path / "doc_a.md"
    b = tmp_path / "doc_b.md"
    a.write_text("# A\n\nАгент архитектура память.\n", encoding="utf-8")
    b.write_text("# B\n\nСистема хранения знаний.\n", encoding="utf-8")

    original_root = mod.ROOT
    try:
        mod.ROOT = tmp_path
        r = mod.compare_two(a, b)
        result = mod.format_comparison(r)
    finally:
        mod.ROOT = original_root

    text = "\n".join(result)
    assert "doc_a.md" in text or "doc_b.md" in text
