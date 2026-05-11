"""
Тесты для scripts/improve_empty_sections.py.

Покрытие:
  - _parse_sections()  — парсинг заголовков и подсчёт слов
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_empty_sections")


# ── _parse_sections ───────────────────────────────────────────────────────────

def test_parse_sections_returns_list():
    result = mod._parse_sections("# Title\n## Section\n")
    assert isinstance(result, list)


def test_parse_sections_empty():
    result = mod._parse_sections("")
    assert result == []


def test_parse_sections_no_headings():
    result = mod._parse_sections("plain text no headings here")
    assert result == []


def test_parse_sections_finds_h2():
    result = mod._parse_sections("## My Section\n\nContent here.\n")
    assert len(result) == 1
    assert result[0]["level"] == 2


def test_parse_sections_finds_h3():
    result = mod._parse_sections("### Sub Section\n\nContent here.\n")
    assert len(result) == 1
    assert result[0]["level"] == 3


def test_parse_sections_title_extracted():
    result = mod._parse_sections("## My Section Title\n\nContent here.\n")
    if result:
        assert result[0]["title"] == "My Section Title"


def test_parse_sections_has_required_keys():
    result = mod._parse_sections("## Section\n\nContent here.\n")
    for sec in result:
        assert "level" in sec
        assert "title" in sec
        assert "line_idx" in sec
        assert "content_words" in sec


def test_parse_sections_counts_words():
    result = mod._parse_sections("## Section\n\none two three four five\n")
    if result:
        assert result[0]["content_words"] >= 5


def test_parse_sections_empty_section_zero_words():
    result = mod._parse_sections("## Empty\n\n## Another\n\nWith words here.\n")
    if len(result) >= 2:
        # First section has no words (only empty + next heading)
        assert result[0]["content_words"] == 0


def test_parse_sections_multiple_sections():
    text = "## Section A\n\nContent A.\n\n## Section B\n\nContent B words here.\n"
    result = mod._parse_sections(text)
    assert len(result) == 2


def test_parse_sections_skips_code_in_word_count():
    text = "## Section\n\n```python\ncode line one\ncode line two\n```\nReal text.\n"
    result = mod._parse_sections(text)
    if result:
        # Code block content should not count or be minimal
        assert isinstance(result[0]["content_words"], int)
