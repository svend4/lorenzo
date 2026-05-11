"""Tests for scripts/part6_vacancies.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part6_vacancies")


def test_keywords_is_dict():
    assert isinstance(mod.KEYWORDS, dict)
    assert len(mod.KEYWORDS) > 0


def test_keywords_values_are_tuples():
    for key, val in mod.KEYWORDS.items():
        assert isinstance(val, tuple), f"Key {key!r}: value should be tuple"
        assert len(val) == 2, f"Key {key!r}: tuple should have 2 elements"


def test_keywords_filenames_are_md():
    for key, (fname, _) in mod.KEYWORDS.items():
        assert fname.endswith(".md"), f"Key {key!r}: filename {fname!r} should end with .md"


def test_keywords_has_research():
    assert any("research" in k.lower() or "Research" in k for k in mod.KEYWORDS)


def test_keywords_has_security():
    assert any("security" in k.lower() or "Security" in k for k in mod.KEYWORDS)


def test_keywords_has_finance():
    assert any("finance" in k.lower() or "Finance" in k for k in mod.KEYWORDS)


def test_mhtml_is_path():
    assert isinstance(mod.MHTML, Path)


def test_keywords_displays_are_strings():
    for key, (fname, display) in mod.KEYWORDS.items():
        assert isinstance(display, str), f"Key {key!r}: display should be string"
        assert len(display) > 0
