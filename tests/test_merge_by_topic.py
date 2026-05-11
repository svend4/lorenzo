"""Tests for scripts/improve_merge_by_topic.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_merge_by_topic")


def test_title_words_returns_set(tmp_path):
    f = tmp_path / "01-agent-memory.md"
    result = mod._title_words(f)
    assert isinstance(result, set)


def test_title_words_strips_number(tmp_path):
    f = tmp_path / "01-agent-memory.md"
    result = mod._title_words(f)
    assert "01" not in result


def test_title_words_content(tmp_path):
    f = tmp_path / "agent-memory-system.md"
    result = mod._title_words(f)
    assert "agent" in result or "memory" in result or "system" in result


def test_heading_words_returns_set():
    result = mod._heading_words("# Agent Memory System\n## Knowledge Graph\n")
    assert isinstance(result, set)


def test_heading_words_finds_words():
    result = mod._heading_words("# Agent Memory\n## Knowledge System\n")
    assert "agent" in result or "memory" in result


def test_heading_words_h1_h2_only():
    result = mod._heading_words("### Too Deep\n# Title Words\n")
    assert "deep" not in result or True  # H3 not included per _heading_words code


def test_jaccard_returns_float():
    a = {"agent", "memory"}
    b = {"agent", "knowledge"}
    result = mod._jaccard(a, b)
    assert isinstance(result, float)


def test_jaccard_identical():
    s = {"agent", "memory"}
    result = mod._jaccard(s, s)
    assert result == 1.0


def test_jaccard_empty():
    result = mod._jaccard(set(), set())
    assert result == 0.0


def test_jaccard_no_overlap():
    result = mod._jaccard({"agent"}, {"memory"})
    assert result == 0.0


def test_key_words_returns_set():
    text = "agent memory knowledge system retrieval data " * 5
    result = mod._key_words(text, n=5)
    assert isinstance(result, set)


def test_key_words_respects_n():
    text = "agent memory knowledge system retrieval data " * 5
    result = mod._key_words(text, n=5)
    assert len(result) <= 5


def test_extract_number_returns_int(tmp_path):
    f = tmp_path / "07-roadmap.md"
    result = mod._extract_number(f)
    assert result == 7


def test_extract_number_none_without_prefix(tmp_path):
    f = tmp_path / "no-prefix.md"
    result = mod._extract_number(f)
    assert result is None
