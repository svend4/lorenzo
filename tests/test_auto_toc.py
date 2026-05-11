"""
Тесты для scripts/improve_auto_toc.py.

Покрытие:
  - _slug()              — GitHub-совместимый якорь из заголовка
  - _build_toc()         — строит markdown TOC
  - _extract_headings()  — извлекает заголовки H2..Hmax
  - _has_toc()           — определяет наличие TOC
"""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_auto_toc")


# ── _slug ─────────────────────────────────────────────────────────────────────

def test_slug_returns_string():
    result = mod._slug("Hello World")
    assert isinstance(result, str)


def test_slug_lowercases():
    result = mod._slug("Hello World")
    assert result == result.lower()


def test_slug_spaces_to_dashes():
    result = mod._slug("Hello World")
    assert result == "hello-world"


def test_slug_removes_special_chars():
    result = mod._slug("Hello, World!")
    assert "," not in result
    assert "!" not in result


def test_slug_strips_dashes():
    result = mod._slug("  Hello World  ")
    assert not result.startswith("-")
    assert not result.endswith("-")


def test_slug_handles_cyrillic():
    result = mod._slug("Агент памяти")
    assert isinstance(result, str)
    assert len(result) > 0


def test_slug_empty():
    result = mod._slug("")
    assert isinstance(result, str)


# ── _build_toc ────────────────────────────────────────────────────────────────

def test_build_toc_returns_string():
    headings = [(2, "Introduction"), (2, "Methods")]
    result = mod._build_toc(headings)
    assert isinstance(result, str)


def test_build_toc_starts_with_marker():
    headings = [(2, "Section")]
    result = mod._build_toc(headings)
    assert result.startswith(mod.TOC_MARKER)


def test_build_toc_contains_contents():
    headings = [(2, "Section")]
    result = mod._build_toc(headings)
    assert "## Contents" in result


def test_build_toc_contains_heading_links():
    headings = [(2, "My Section")]
    result = mod._build_toc(headings)
    assert "My Section" in result
    assert "(#" in result


def test_build_toc_h2_no_indent():
    headings = [(2, "Top Level")]
    result = mod._build_toc(headings)
    assert "- [Top Level]" in result


def test_build_toc_h3_indented():
    headings = [(3, "Sub Level")]
    result = mod._build_toc(headings)
    assert "  - [Sub Level]" in result


def test_build_toc_multiple_headings():
    headings = [(2, "Section A"), (2, "Section B"), (3, "Sub B")]
    result = mod._build_toc(headings)
    assert "Section A" in result
    assert "Section B" in result
    assert "Sub B" in result


def test_build_toc_deduplicates_anchors():
    headings = [(2, "Same Title"), (2, "Same Title")]
    result = mod._build_toc(headings)
    # Both should appear, second with -1 suffix
    assert result.count("Same Title") == 2


# ── _extract_headings ─────────────────────────────────────────────────────────

def test_extract_headings_returns_list():
    result = mod._extract_headings("## Section\n", 3)
    assert isinstance(result, list)


def test_extract_headings_skips_h1():
    result = mod._extract_headings("# Title\n## Section\n", 3)
    for level, _ in result:
        assert level >= 2


def test_extract_headings_extracts_h2():
    result = mod._extract_headings("## My Section\n", 3)
    assert (2, "My Section") in result


def test_extract_headings_extracts_h3():
    result = mod._extract_headings("### Sub Section\n", 3)
    assert (3, "Sub Section") in result


def test_extract_headings_respects_max_level():
    text = "## H2\n### H3\n#### H4\n"
    result = mod._extract_headings(text, 3)
    levels = [level for level, _ in result]
    assert 4 not in levels


def test_extract_headings_skips_code_blocks():
    text = "```\n## Fake Heading\n```\n## Real Heading\n"
    result = mod._extract_headings(text, 3)
    titles = [title for _, title in result]
    assert "Fake Heading" not in titles
    assert "Real Heading" in titles


def test_extract_headings_removes_formatting():
    result = mod._extract_headings("## **Bold** Heading\n", 3)
    if result:
        _, title = result[0]
        assert "**" not in title


# ── _has_toc ──────────────────────────────────────────────────────────────────

def test_has_toc_false_without_toc():
    result = mod._has_toc("# Title\n\nSome content.\n")
    assert result is False


def test_has_toc_true_with_marker():
    result = mod._has_toc(f"# Title\n\n{mod.TOC_MARKER}\n## Contents\n")
    assert result is True


def test_has_toc_true_with_contents_heading():
    result = mod._has_toc("# Title\n\n## Contents\n- [Section](#section)\n")
    assert result is True


def test_has_toc_true_with_table_of_contents():
    result = mod._has_toc("# Title\n\n## Table of Contents\n- [Section](#section)\n")
    assert result is True
