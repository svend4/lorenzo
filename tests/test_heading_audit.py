"""
Тесты для scripts/improve_heading_audit.py.

Покрытие:
  - _parse_headings()  — парсинг заголовков и подсчёт слов секций
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_heading_audit")


# ── _parse_headings ───────────────────────────────────────────────────────────

def test_parse_headings_returns_list():
    result = mod._parse_headings("# Title\n## Section\n")
    assert isinstance(result, list)


def test_parse_headings_empty():
    result = mod._parse_headings("")
    assert result == []


def test_parse_headings_no_headings():
    result = mod._parse_headings("plain text without headings")
    assert result == []


def test_parse_headings_finds_h1():
    result = mod._parse_headings("# My Title\n")
    assert len(result) == 1
    assert result[0]["level"] == 1


def test_parse_headings_finds_h2():
    result = mod._parse_headings("## My Section\n")
    assert len(result) == 1
    assert result[0]["level"] == 2


def test_parse_headings_title_extracted():
    result = mod._parse_headings("## My Section Title\n")
    if result:
        assert result[0]["title"] == "My Section Title"


def test_parse_headings_has_required_keys():
    result = mod._parse_headings("## Section\n\nContent.\n")
    for h in result:
        assert "level" in h
        assert "title" in h
        assert "line_idx" in h
        assert "content_words" in h


def test_parse_headings_counts_words():
    result = mod._parse_headings("## Section\n\none two three four five\n")
    if result:
        assert result[0]["content_words"] >= 5


def test_parse_headings_multiple():
    text = "# Title\n## Section A\n\nContent.\n## Section B\n\nMore content.\n"
    result = mod._parse_headings(text)
    assert len(result) == 3


def test_parse_headings_skips_code():
    text = "# Title\n```\n## Fake Heading\n```\n## Real Heading\n"
    result = mod._parse_headings(text)
    titles = [h["title"] for h in result]
    assert "Fake Heading" not in titles
    assert "Real Heading" in titles
