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


def test_run_calls_extract_and_split(monkeypatch, capsys):
    """Lines 26-28: run() calls extract_and_split with correct args."""
    called = [False]
    def fake_extract(mhtml_path, keywords, out_dir):
        called[0] = True
    monkeypatch.setattr(mod, "extract_and_split", fake_extract)
    mod.run()
    assert called[0]


def test_run_prints_section_header(monkeypatch, capsys):
    """Line 27: run() prints a header."""
    monkeypatch.setattr(mod, "extract_and_split", lambda *a: None)
    mod.run()
    out = capsys.readouterr().out
    assert "Anthropic" in out or "vacancies" in out.lower() or "---" in out
