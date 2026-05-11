"""Tests for scripts/improve_export_html.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_export_html")


def test_md_to_html_returns_string():
    result = mod.md_to_html("# Hello\n\nWorld.")
    assert isinstance(result, str)


def test_md_to_html_converts_h1():
    result = mod.md_to_html("# Title")
    assert "<h1>" in result
    assert "Title" in result


def test_md_to_html_converts_h2():
    result = mod.md_to_html("## Section")
    assert "<h2>" in result
    assert "Section" in result


def test_md_to_html_converts_h3():
    result = mod.md_to_html("### Subsection")
    assert "<h3>" in result
    assert "Subsection" in result


def test_md_to_html_converts_bold():
    result = mod.md_to_html("This is **bold** text.")
    assert "<strong>" in result
    assert "bold" in result


def test_md_to_html_converts_code_inline():
    result = mod.md_to_html("Use `print()` function.")
    assert "<code>" in result
    assert "print()" in result


def test_md_to_html_converts_links():
    result = mod.md_to_html("[GitHub](https://github.com)")
    assert '<a href="https://github.com">' in result
    assert "GitHub" in result


def test_md_to_html_converts_blockquote():
    result = mod.md_to_html("> Note: something important.")
    assert "<blockquote>" in result
    assert "Note" in result


def test_md_to_html_converts_list_item():
    result = mod.md_to_html("- Item one")
    assert "<li>" in result
    assert "Item one" in result


def test_md_to_html_converts_code_block():
    result = mod.md_to_html("```python\nprint('hello')\n```")
    assert "<pre>" in result
    assert "<code" in result


def test_md_to_html_escapes_code_block_html():
    result = mod.md_to_html("```\n<script>evil()</script>\n```")
    assert "<script>" not in result
    assert "&lt;script&gt;" in result


def test_md_to_html_removes_comments():
    result = mod.md_to_html("<!-- hidden --> visible")
    assert "hidden" not in result
    assert "visible" in result


def test_md_to_html_converts_table():
    table = "| A | B |\n|---|---|\n| 1 | 2 |"
    result = mod.md_to_html(table)
    assert "<table>" in result
    assert "<th>" in result


def test_md_to_html_hr():
    result = mod.md_to_html("---")
    assert "<hr>" in result


def test_build_nav_returns_string():
    sections = {"01-docs": [("01-docs/file.md", "File Title")]}
    result = mod.build_nav(sections)
    assert isinstance(result, str)


def test_build_nav_contains_section():
    sections = {"01-docs": [("01-docs/file.md", "File Title")]}
    result = mod.build_nav(sections)
    assert "01-docs" in result


def test_build_nav_contains_file_link():
    sections = {"01-docs": [("01-docs/file.md", "File Title")]}
    result = mod.build_nav(sections)
    assert "File Title" in result


def test_build_nav_creates_nav_tag():
    sections = {}
    result = mod.build_nav(sections)
    assert "<nav>" in result
    assert "</nav>" in result


def test_build_nav_multiple_sections():
    sections = {
        "01-svyazi": [("01-svyazi/intro.md", "Introduction")],
        "02-projects": [("02-projects/agentfs.md", "AgentFS")],
    }
    result = mod.build_nav(sections)
    assert "01-svyazi" in result
    assert "02-projects" in result


def test_css_constant():
    assert hasattr(mod, "CSS")
    assert isinstance(mod.CSS, str)
    assert "font-family" in mod.CSS


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_index_html(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "index.html").exists()


def test_main_html_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (tmp_path / "doc.md").write_text("# AgentFS\n\nContent here.", encoding="utf-8")
    mod.main()
    text = (tmp_path / "index.html").read_text(encoding="utf-8")
    assert "<html" in text or "<!DOCTYPE" in text or "AgentFS" in text


def test_main_empty_docs(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert (tmp_path / "index.html").exists()
