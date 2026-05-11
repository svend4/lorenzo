"""Tests for scripts/part1_utils.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("part1_utils")


# ── clean ─────────────────────────────────────────────────────────────────────

def test_clean_returns_string():
    result = mod.clean("Hello world.")
    assert isinstance(result, str)


def test_clean_removes_citeturn():
    text = "Content citeturn0search5 here."
    result = mod.clean(text)
    assert "citeturn" not in result
    assert "Content" in result
    assert "here." in result


def test_clean_removes_citeturn_various():
    text = "A citeturn1abc B citeturn99xyz C"
    result = mod.clean(text)
    assert "citeturn" not in result
    assert "A" in result
    assert "B" in result


def test_clean_collapses_many_newlines():
    text = "A\n\n\n\n\nB"
    result = mod.clean(text)
    assert "\n\n\n\n" not in result
    assert "A" in result
    assert "B" in result


def test_clean_preserves_double_newline():
    text = "A\n\nB"
    result = mod.clean(text)
    assert "A" in result
    assert "B" in result


def test_clean_strips_whitespace():
    text = "  \n\nHello\n\n  "
    result = mod.clean(text)
    assert result == result.strip()


def test_clean_empty_string():
    result = mod.clean("")
    assert result == ""


# ── write_doc ─────────────────────────────────────────────────────────────────

def test_write_doc_creates_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    dest = tmp_path / "output.md"
    mod.write_doc(dest, "# Hello")
    assert dest.exists()


def test_write_doc_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    dest = tmp_path / "output.md"
    mod.write_doc(dest, "# Hello\n\nContent.")
    text = dest.read_text(encoding="utf-8")
    assert "# Hello" in text
    assert "Content." in text


def test_write_doc_appends_newline(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    dest = tmp_path / "output.md"
    mod.write_doc(dest, "Content")
    text = dest.read_text(encoding="utf-8")
    assert text.endswith("\n")


def test_write_doc_strips_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    dest = tmp_path / "output.md"
    mod.write_doc(dest, "  Content  ")
    text = dest.read_text(encoding="utf-8")
    assert text == "Content\n"


def test_write_doc_creates_parent_dirs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    dest = tmp_path / "sub" / "deep" / "output.md"
    mod.write_doc(dest, "Content")
    assert dest.exists()


# ── module attributes ─────────────────────────────────────────────────────────

def test_root_is_path():
    assert isinstance(mod.ROOT, Path)


def test_docs_is_path():
    assert isinstance(mod.DOCS, Path)
