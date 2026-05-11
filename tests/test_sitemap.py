"""
Тесты для scripts/improve_sitemap.py.

Покрытие:
  - get_title()       — извлечение H1-заголовка из файла
  - get_word_count()  — подсчёт слов в файле
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_sitemap")


# ── get_title ─────────────────────────────────────────────────────────────────

def test_get_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# My Title\n\nContent here.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert isinstance(result, str)


def test_get_title_extracts_h1(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# My Document Title\n\nContent here.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert result == "My Document Title"


def test_get_title_strips_whitespace(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("#  Spaced Title  \n\nContent.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert result == "Spaced Title"


def test_get_title_truncates_at_60(tmp_path):
    f = tmp_path / "test.md"
    long_title = "A" * 100
    f.write_text(f"# {long_title}\n\nContent.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert len(result) <= 60


def test_get_title_fallback_to_stem(tmp_path):
    f = tmp_path / "my_document.md"
    f.write_text("No heading here, just content.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert result == "my_document"


def test_get_title_missing_file_returns_stem(tmp_path):
    f = tmp_path / "nonexistent_doc.md"
    result = mod.get_title(f)
    assert result == "nonexistent_doc"


def test_get_title_empty_file_returns_stem(tmp_path):
    f = tmp_path / "empty_file.md"
    f.write_text("", encoding="utf-8")
    result = mod.get_title(f)
    assert result == "empty_file"


def test_get_title_finds_first_h1(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("## Not H1\n# First H1\n# Second H1\n\nContent.\n", encoding="utf-8")
    result = mod.get_title(f)
    assert result == "First H1"


def test_get_title_h2_not_returned_as_h1(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("## Section Title\n\nContent without H1.\n", encoding="utf-8")
    result = mod.get_title(f)
    # No H1 found, should return stem
    assert result == "test"


# ── get_word_count ────────────────────────────────────────────────────────────

def test_get_word_count_returns_int(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one two three\n", encoding="utf-8")
    result = mod.get_word_count(f)
    assert isinstance(result, int)


def test_get_word_count_counts_words(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one two three four five\n", encoding="utf-8")
    result = mod.get_word_count(f)
    assert result == 5


def test_get_word_count_empty_file(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("", encoding="utf-8")
    result = mod.get_word_count(f)
    assert result == 0


def test_get_word_count_multiline(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("one\ntwo\nthree\n", encoding="utf-8")
    result = mod.get_word_count(f)
    assert result == 3


def test_get_word_count_missing_file_returns_zero(tmp_path):
    f = tmp_path / "nonexistent.md"
    result = mod.get_word_count(f)
    assert result == 0
