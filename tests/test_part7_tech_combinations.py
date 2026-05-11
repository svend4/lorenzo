"""Tests for scripts/part7_tech_combinations.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part7_tech_combinations")


def test_keywords_is_dict():
    assert isinstance(mod.KEYWORDS, dict)
    assert len(mod.KEYWORDS) > 0


def test_keywords_values_are_tuples():
    for key, val in mod.KEYWORDS.items():
        assert isinstance(val, tuple)
        assert len(val) == 2


def test_keywords_filenames_are_md():
    for key, (fname, _) in mod.KEYWORDS.items():
        assert fname.endswith(".md")


def test_keywords_has_agent():
    assert any("роут" in k.lower() or "agent" in k.lower() for k in mod.KEYWORDS)


def test_keywords_has_graph():
    assert any("граф" in k.lower() or "graph" in k.lower() for k in mod.KEYWORDS)


def test_keywords_has_benchmarks():
    assert any("бенчмарк" in k.lower() or "benchmark" in k.lower() for k in mod.KEYWORDS)


def test_mhtml_is_path():
    assert isinstance(mod.MHTML, Path)


def test_keywords_displays_are_strings():
    for key, (fname, display) in mod.KEYWORDS.items():
        assert isinstance(display, str)
        assert len(display) > 0
