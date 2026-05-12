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


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "confluence")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()


def test_main_creates_confluence_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "confluence")
    (tmp_path / "doc.md").write_text("# Title\n\nContent.", encoding="utf-8")
    mod.main()
    assert (tmp_path / "confluence").exists()


def test_main_empty_docs_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "confluence")
    mod.main()


# ── arg parsing ────────────────────────────────────────────────────────────────

def test_section_arg_parsing():
    """Lines 32-34: --section sets SECTION_FILTER."""
    orig = sys.argv[:]
    try:
        sys.argv = ["prog", "--section", "01-svyazi"]
        importlib.reload(mod)
        assert mod.SECTION_FILTER is not None
    finally:
        sys.argv = orig
        importlib.reload(mod)


# ── md_to_confluence: blockquote line ────────────────────────────────────────

def test_md_to_confluence_blockquote(tmp_path, monkeypatch):
    """Line 111: line starts with '> ' → {quote}...{quote}."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    source = tmp_path / "test.md"
    source.write_text("", encoding="utf-8")
    text = "> This is a blockquote.\n"
    result = mod.md_to_confluence(text, source)
    assert "{quote}" in result


# ── main: DRY_RUN=False writes files, exception handling ─────────────────────

def test_main_write_exception_handled(tmp_path, monkeypatch, capsys):
    """Lines 155-156: exception in processing → error printed."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", False)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    out_dir = tmp_path / "confluence"
    monkeypatch.setattr(mod, "OUT_DIR", out_dir)
    f = tmp_path / "bad.md"
    f.write_text("# Title\n\nContent.\n", encoding="utf-8")
    # Mock md_to_confluence to raise
    monkeypatch.setattr(mod, "md_to_confluence", lambda text, source: (_ for _ in ()).throw(ValueError("mock")))
    mod.main()
    out = capsys.readouterr().out
    assert "❌" in out or "bad.md" in out


# ── __main__ block ─────────────────────────────────────────────────────────────

def test_main_block_via_runpy(tmp_path, monkeypatch):
    """Line 165: __main__ block."""
    import runpy
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "OUT_DIR", tmp_path / "confluence")
    runpy.run_path(str(ROOT / "scripts" / "improve_confluence.py"), run_name="__main__")
