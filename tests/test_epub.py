"""Tests for scripts/improve_epub.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_epub")


def test_check_pandoc_returns_bool():
    result = mod._check_pandoc()
    assert isinstance(result, bool)


def test_clean_for_epub_removes_html_comments():
    text = "Before <!-- comment --> After"
    result = mod._clean_for_epub(text)
    assert "comment" not in result
    assert "Before" in result
    assert "After" in result


def test_clean_for_epub_removes_multiline_comments():
    text = "Start\n<!-- \nmulti\nline\ncomment\n-->\nEnd"
    result = mod._clean_for_epub(text)
    assert "multi" not in result
    assert "Start" in result
    assert "End" in result


def test_clean_for_epub_removes_shields():
    text = "See ![badge](https://img.shields.io/badge/test-pass-green) for status."
    result = mod._clean_for_epub(text)
    assert "shields.io" not in result
    assert "status" in result


def test_clean_for_epub_preserves_regular_links():
    text = "[GitHub](https://github.com/user/repo)"
    result = mod._clean_for_epub(text)
    assert "GitHub" in result


def test_clean_for_epub_returns_string():
    result = mod._clean_for_epub("# Title\n\nContent.")
    assert isinstance(result, str)


def test_skip_files_constant():
    assert hasattr(mod, "SKIP_FILES")
    assert isinstance(mod.SKIP_FILES, set)
    assert "SEARCH.md" in mod.SKIP_FILES


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_today_attribute():
    assert hasattr(mod, "TODAY")
    assert isinstance(mod.TODAY, str)
    assert len(mod.TODAY) == 10  # YYYY-MM-DD


def test_title_attribute():
    assert hasattr(mod, "TITLE")
    assert isinstance(mod.TITLE, str)
    assert len(mod.TITLE) > 0
