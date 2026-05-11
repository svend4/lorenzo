"""Tests for scripts/improve_digest_auto.py."""

import importlib
import sys
from collections import Counter
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_digest_auto")


def test_tokenize_diff_returns_tuple():
    diff = "+agent memory system\n-old data removed\n"
    result = mod._tokenize_diff(diff)
    assert isinstance(result, tuple)
    assert len(result) == 2


def test_tokenize_diff_added_tokens():
    diff = "+agent memory knowledge system retrieval\n"
    added, removed = mod._tokenize_diff(diff)
    assert isinstance(added, Counter)
    assert len(added) > 0


def test_tokenize_diff_removed_tokens():
    diff = "-agent memory knowledge system\n"
    added, removed = mod._tokenize_diff(diff)
    assert isinstance(removed, Counter)
    assert len(removed) > 0


def test_tokenize_diff_skips_markers():
    diff = "--- old file\n+++ new file\n+actual content added\n"
    added, removed = mod._tokenize_diff(diff)
    assert "file" not in added
    assert "file" not in removed


def test_tokenize_diff_min_4_chars():
    diff = "+ab abc abcd abcde\n"
    added, removed = mod._tokenize_diff(diff)
    for token in added:
        assert len(token) >= 4


def test_section_of_docs_file():
    result = mod._section_of("docs/01-svyazi/file.md")
    assert result == "01-svyazi"


def test_section_of_scripts():
    result = mod._section_of("scripts/improve_test.py")
    assert result == "scripts"


def test_section_of_root():
    result = mod._section_of("README.md")
    assert result == "root"


def test_section_of_nested_docs():
    result = mod._section_of("docs/05-habr-projects/memory/yodoca.md")
    assert result == "05-habr-projects"
