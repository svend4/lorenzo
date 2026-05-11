"""Tests for scripts/improve_text_segmenter.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_text_segmenter")


def test_word_count_returns_int():
    result = mod._word_count("hello world test")
    assert isinstance(result, int)


def test_word_count_counts_words():
    result = mod._word_count("one two three four five")
    assert result == 5


def test_word_count_empty():
    result = mod._word_count("")
    assert result == 0


def test_extract_title_returns_string(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert isinstance(result, str)


def test_extract_title_finds_h1(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_title("# My Title\nContent here.", f)
    assert result == "My Title"


def test_extract_title_fallback(tmp_path):
    f = tmp_path / "my-test-file.md"
    result = mod._extract_title("no heading", f)
    assert len(result) > 0


def test_split_into_segments_returns_list():
    text = "# Title\n\nContent here.\n\n## Section\n\nMore content.\n"
    result = mod._split_into_segments(text, target_size=100)
    assert isinstance(result, list)


def test_split_into_segments_has_content():
    text = "# Title\n\nSome content here.\n\n## Section A\n\nSection A content.\n\n## Section B\n\nSection B content.\n"
    result = mod._split_into_segments(text, target_size=50)
    assert len(result) >= 1


def test_split_into_segments_entry_keys():
    text = "## Section\n\nSome content goes here for testing purposes.\n"
    result = mod._split_into_segments(text, target_size=100)
    for seg in result:
        assert "heading" in seg
        assert "content" in seg
        assert "word_count" in seg


def test_split_into_segments_word_counts():
    text = "## Section\n\nSome content goes here for testing purposes.\n"
    result = mod._split_into_segments(text, target_size=100)
    for seg in result:
        assert isinstance(seg["word_count"], int)
        assert seg["word_count"] >= 0


def test_split_into_segments_no_headings():
    text = "First paragraph of content here.\n\n\nSecond paragraph of content here.\n"
    result = mod._split_into_segments(text, target_size=100)
    assert len(result) >= 1


def test_split_into_segments_respects_target():
    # With small target_size, should split into multiple segments
    text = "## Section\n\n" + ("word " * 100) + "\n\n## Other\n\n" + ("word " * 100)
    result = mod._split_into_segments(text, target_size=20)
    assert len(result) >= 2
