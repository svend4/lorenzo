"""Tests for scripts/improve_llm_gaps.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_gaps")


def test_get_doc_index_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\nThis is a test document with some content.", encoding="utf-8")
    result = mod.get_doc_index()
    assert isinstance(result, str)


def test_get_doc_index_includes_file(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# AgentFS\n\nThis is the AgentFS project description.", encoding="utf-8")
    result = mod.get_doc_index()
    assert "project.md" in result


def test_get_doc_index_skips_headings(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title (skip this)\n\nThis line should appear.", encoding="utf-8")
    result = mod.get_doc_index()
    assert "Title (skip this)" not in result
    assert "This line should appear" in result


def test_get_doc_index_empty_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.get_doc_index()
    assert isinstance(result, str)
    assert result == ""


def test_get_arch_summary_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_arch_summary()
    assert isinstance(result, str)


def test_get_arch_summary_empty_when_no_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.get_arch_summary()
    assert result == ""


def test_get_arch_summary_includes_existing_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    section_dir = tmp_path / "01-svyazi"
    section_dir.mkdir()
    f = section_dir / "09-architectural-gaps.md"
    f.write_text("# Architectural Gaps\n\nThese are the gaps.", encoding="utf-8")
    result = mod.get_arch_summary()
    assert "09-architectural-gaps.md" in result
    assert "gaps" in result.lower()


def test_docs_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


def test_root_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_llm_gaps_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "call_claude_gaps", lambda *a: None)
    mod.main()
    assert (tmp_path / "LLM_GAPS.md").exists()


def test_main_with_api_response(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "call_claude_gaps", lambda *a: "## Gaps\n- gap 1")
    mod.main()
    content = (tmp_path / "LLM_GAPS.md").read_text(encoding="utf-8")
    assert "gap 1" in content


def test_main_no_api_fallback(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "call_claude_gaps", lambda *a: None)
    mod.main()
    content = (tmp_path / "LLM_GAPS.md").read_text(encoding="utf-8")
    assert "API" in content
