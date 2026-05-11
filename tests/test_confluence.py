"""Tests for scripts/improve_confluence.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_confluence")


def test_md_to_confluence_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("# Title\n\nContent here.\n", encoding="utf-8")
    result = mod.md_to_confluence("# Title\n\nContent here.\n", source)
    assert isinstance(result, str)


def test_md_to_confluence_converts_h1(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("# My Title\n", source)
    assert "h1. My Title" in result


def test_md_to_confluence_converts_h2(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("## Section Two\n", source)
    assert "h2. Section Two" in result


def test_md_to_confluence_converts_bold(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("**bold text** here\n", source)
    # Bold ** is converted; the double asterisks are removed from the output
    assert "**bold text**" not in result


def test_md_to_confluence_converts_inline_code(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("Use `python` for scripting\n", source)
    assert "{{python}}" in result


def test_md_to_confluence_converts_link(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("[GitHub](https://github.com)\n", source)
    assert "[GitHub|https://github.com]" in result


def test_md_to_confluence_converts_code_block(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("```python\ncode here\n```\n", source)
    assert "{code:language=python}" in result or "{code" in result


def test_md_to_confluence_converts_code_block_end(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("```python\ncode\n```\n", source)
    assert "{code}" in result


def test_md_to_confluence_strips_html_comments(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("Text <!-- comment --> more text\n", source)
    assert "<!--" not in result
    assert "comment" not in result


def test_md_to_confluence_converts_horizontal_rule(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("Before\n---\nAfter\n", source)
    assert "----" in result


def test_md_to_confluence_converts_table(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    text = "| Col1 | Col2 |\n|------|------|\n| A | B |\n"
    result = mod.md_to_confluence(text, source)
    assert "||" in result


def test_md_to_confluence_has_source_info(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    result = mod.md_to_confluence("# Test\n", source)
    assert "{info" in result
