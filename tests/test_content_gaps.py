"""
Тесты для scripts/improve_content_gaps.py.

Покрытие:
  - _clean()              — очистка markdown-разметки
  - _extract_concepts()   — извлечение концептов из текста
  - _suggest_location()   — предложение папки для нового файла
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_content_gaps")


# ── _clean ────────────────────────────────────────────────────────────────────

def test_clean_returns_string():
    result = mod._clean("some text")
    assert isinstance(result, str)


def test_clean_removes_code_blocks():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_clean_removes_inline_code():
    result = mod._clean("Use `function()` here.")
    assert "function()" not in result


def test_clean_removes_url():
    result = mod._clean("See https://example.com for more.")
    assert "https" not in result


def test_clean_removes_html_comments():
    result = mod._clean("Before <!-- comment --> after")
    assert "comment" not in result


def test_clean_empty():
    result = mod._clean("")
    assert result == ""


# ── _extract_concepts ─────────────────────────────────────────────────────────

def test_extract_concepts_returns_list():
    result = mod._extract_concepts("plain text")
    assert isinstance(result, list)


def test_extract_concepts_empty():
    result = mod._extract_concepts("")
    assert result == []


def test_extract_concepts_min_length_3():
    result = mod._extract_concepts("АБ ABC test")
    for c in result:
        assert len(c.lower().strip()) >= 3


def test_extract_concepts_max_length_50():
    result = mod._extract_concepts("# Title\n\nSome text here.")
    for c in result:
        assert len(c.lower().strip()) <= 50


def test_extract_concepts_no_pure_numbers():
    result = mod._extract_concepts("12345 and 678 in the text.")
    for c in result:
        assert not c.strip().isdigit()


# ── _suggest_location ─────────────────────────────────────────────────────────

def test_suggest_location_returns_string():
    result = mod._suggest_location("test term", [])
    assert isinstance(result, str)


def test_suggest_location_default_docs():
    result = mod._suggest_location("test term", [])
    assert "docs" in result


def test_suggest_location_uses_source_folder():
    sources = ["docs/05-habr-projects/memory/file.md",
               "docs/05-habr-projects/memory/other.md"]
    result = mod._suggest_location("memory term", sources)
    assert "docs/" in result


def test_suggest_location_most_common_folder():
    sources = [
        "docs/05-habr-projects/a.md",
        "docs/05-habr-projects/b.md",
        "docs/01-svyazi/c.md",
    ]
    result = mod._suggest_location("term", sources)
    assert "05-habr-projects" in result
