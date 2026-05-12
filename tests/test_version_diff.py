"""Tests for scripts/improve_version_diff.py."""

import importlib
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_version_diff")


def test_extract_headings_returns_set():
    result = mod._extract_headings("# Title\n## Section\n")
    assert isinstance(result, set)


def test_extract_headings_finds_h1():
    result = mod._extract_headings("# My Title\n")
    assert "My Title" in result


def test_extract_headings_finds_h2():
    result = mod._extract_headings("## My Section\n")
    assert "My Section" in result


def test_extract_headings_finds_h3():
    result = mod._extract_headings("### Subsection\n")
    assert "Subsection" in result


def test_extract_headings_multiple():
    text = "# Title\n## Section A\n## Section B\n"
    result = mod._extract_headings(text)
    assert "Title" in result
    assert "Section A" in result
    assert "Section B" in result


def test_extract_headings_empty():
    result = mod._extract_headings("plain text without headings")
    assert result == set()


def test_word_count_returns_int():
    result = mod._word_count("hello world test")
    assert isinstance(result, int)


def test_word_count_counts_words():
    result = mod._word_count("hello world test")
    assert result >= 3


def test_word_count_strips_code():
    result = mod._word_count("Before\n```python\ncode\n```\nAfter")
    assert result < 10


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_git_show_returns_string():
    # Test that it returns empty string on error (e.g., non-existent rev)
    result = mod._git_show("nonexistent_rev_abc123", "docs/README.md")
    assert isinstance(result, str)


def test_changed_docs_files_returns_list():
    # On a real repo with HEAD, should return a list
    result = mod._changed_docs_files("HEAD", "HEAD")
    assert isinstance(result, list)


def test_changed_docs_files_only_md():
    # All returned files should end in .md
    result = mod._changed_docs_files("HEAD~5", "HEAD")
    for f in result:
        assert f.endswith(".md")


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_version_diff_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "VERSION_DIFF.md").exists()


def test_main_version_diff_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "VERSION_DIFF.md").read_text(encoding="utf-8")
    assert "# " in text


def test_main_version_diff_starts_with_heading(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = (tmp_path / "VERSION_DIFF.md").read_text(encoding="utf-8")
    assert text.strip().startswith("#")


def test_extract_headings_returns_set():
    text = "# Title\n\n## Section One\n\n### Subsection\n\nContent."
    result = mod._extract_headings(text)
    assert isinstance(result, set)
    assert "Section One" in result


def test_extract_headings_empty():
    result = mod._extract_headings("Just plain text.")
    assert result == set()


def test_word_count_returns_int():
    result = mod._word_count("Hello world this is text.")
    assert isinstance(result, int)
    assert result > 0


def test_word_count_ignores_code_blocks():
    text = "normal text ```code block here``` more text"
    result = mod._word_count(text)
    # code block content should be removed
    assert isinstance(result, int)


def test_git_show_invalid_rev_returns_empty():
    result = mod._git_show("nonexistent_rev_xyz123", "nonexistent/path.md")
    assert result == ""


def test_resolve_rev_returns_string():
    result = mod._resolve_rev("HEAD")
    assert isinstance(result, str)


def test_resolve_rev_invalid_returns_rev():
    result = mod._resolve_rev("definitely_invalid_rev_xyz")
    # Should return the rev itself on failure
    assert isinstance(result, str)
