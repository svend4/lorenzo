"""Tests for scripts/part2_split_md.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part2_split_md")


# ── split_by_h2 ───────────────────────────────────────────────────────────────

def test_split_by_h2_returns_list():
    result = mod.split_by_h2("# Title\n\n## Section\n\nBody.")
    assert isinstance(result, list)


def test_split_by_h2_no_h2_returns_single():
    result = mod.split_by_h2("# Title\n\nSome content.")
    assert len(result) == 1
    heading, body = result[0]
    assert heading == ""


def test_split_by_h2_finds_sections():
    text = "# Title\n\n## Section One\n\nBody one.\n\n## Section Two\n\nBody two."
    result = mod.split_by_h2(text)
    headings = [h for h, _ in result]
    assert "Section One" in headings
    assert "Section Two" in headings


def test_split_by_h2_preamble_empty_heading():
    text = "# Title\n\nPreamble text.\n\n## Section One\n\nBody."
    result = mod.split_by_h2(text)
    first_heading, first_body = result[0]
    assert first_heading == ""
    assert "Preamble text." in first_body


def test_split_by_h2_body_contains_content():
    text = "## My Section\n\nSection content here."
    result = mod.split_by_h2(text)
    section = next((b for h, b in result if h == "My Section"), None)
    assert section is not None
    assert "Section content here." in section


def test_split_by_h2_three_sections():
    text = "## A\n\nAA.\n\n## B\n\nBB.\n\n## C\n\nCC."
    result = mod.split_by_h2(text)
    headings = [h for h, _ in result]
    assert "A" in headings
    assert "B" in headings
    assert "C" in headings


def test_split_by_h2_no_preamble_if_starts_with_h2():
    text = "## First\n\nContent."
    result = mod.split_by_h2(text)
    # No empty-heading preamble since text starts with ##
    headings = [h for h, _ in result]
    assert "" not in headings or all(b.strip() for h, b in result if h == "")


def test_split_by_h2_empty_string():
    result = mod.split_by_h2("")
    assert isinstance(result, list)


def test_split_by_h2_tuples():
    result = mod.split_by_h2("## Section\n\nBody.")
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)


# ── slug ──────────────────────────────────────────────────────────────────────

def test_slug_returns_string():
    result = mod.slug("My Title")
    assert isinstance(result, str)


def test_slug_lowercases():
    result = mod.slug("My Title")
    assert result == result.lower()


def test_slug_replaces_spaces():
    result = mod.slug("My Title Here")
    assert " " not in result


def test_slug_uses_hyphens():
    result = mod.slug("My Title Here")
    assert "-" in result


def test_slug_strips_trailing_hyphens():
    result = mod.slug("Title---")
    assert not result.endswith("-")


def test_slug_truncates_to_60():
    long_title = "A" * 100
    result = mod.slug(long_title)
    assert len(result) <= 60


def test_slug_empty_returns_section():
    result = mod.slug("")
    assert result == "section"


def test_slug_cyrillic():
    result = mod.slug("Архитектура системы")
    assert isinstance(result, str)
    assert len(result) > 0
