"""Tests for scripts/improve_llm_enrich.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_llm_enrich")


def test_extract_facts_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# My Project\n\nSome content about the project.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert isinstance(result, dict)


def test_extract_facts_has_title(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# My Project Title\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "title" in result
    assert result["title"] == "My Project Title"


def test_extract_facts_title_fallback_to_stem(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "my-project.md"
    f.write_text("No heading here.\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["title"] == "my-project"


def test_extract_facts_has_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n<!-- tags: memory, agent, rag -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "tags" in result
    assert isinstance(result["tags"], list)
    assert "memory" in result["tags"]
    assert "agent" in result["tags"]


def test_extract_facts_empty_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent without tags.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["tags"] == []


def test_extract_facts_has_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n<!-- summary -->\n> This is the summary text.\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "summary" in result
    assert "summary text" in result["summary"]


def test_extract_facts_empty_summary(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent without summary.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert result["summary"] == ""


def test_extract_facts_has_projects(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\n**Проекты:** AgentFS, NGT Memory, Yodoca\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "projects" in result
    assert "AgentFS" in result["projects"]


def test_extract_facts_has_chunks(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.\n\n## Section\n\nMore content.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "chunks" in result
    assert isinstance(result["chunks"], list)


def test_extract_facts_has_tokens(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "tokens" in result
    assert isinstance(result["tokens"], int)


def test_extract_facts_has_path(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "project.md"
    f.write_text("# Project\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "path" in result
    assert "project.md" in result["path"]


def test_enrich_prompt_constant():
    assert hasattr(mod, "ENRICH_PROMPT")
    assert isinstance(mod.ENRICH_PROMPT, str)
    assert "{title}" in mod.ENRICH_PROMPT


def test_dry_run_attribute():
    assert hasattr(mod, "DRY_RUN")
    assert isinstance(mod.DRY_RUN, bool)


def test_sections_constant():
    assert hasattr(mod, "SECTIONS")
    assert isinstance(mod.SECTIONS, list)
    assert "05-habr-projects" in mod.SECTIONS


def test_out_dir_attribute():
    assert hasattr(mod, "OUT_DIR")
    assert isinstance(mod.OUT_DIR, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_dry_run_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_main_dry_run_with_file(tmp_path, monkeypatch):
    doc = tmp_path / "doc.md"
    doc.write_text("# AgentFS\n\nContent.", encoding="utf-8")
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", [])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", doc)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_main_dry_run_empty_sections(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DRY_RUN", True)
    monkeypatch.setattr(mod, "SECTIONS", ["nonexistent-section"])
    monkeypatch.setattr(mod, "SECTION_FILTER", None)
    monkeypatch.setattr(mod, "FILE_FILTER", None)
    monkeypatch.setattr(mod, "FORCE", False)
    mod.main()


def test_extract_facts_returns_dict(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "agentfs.md"
    f.write_text("# AgentFS\n\n<!-- tags: memory, agent -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert isinstance(result, dict)
    assert "title" in result
    assert "tags" in result
    assert result["title"] == "AgentFS"


def test_extract_facts_finds_tags(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    f = tmp_path / "doc.md"
    f.write_text("# Title\n\n<!-- tags: memory, search -->\n\nContent.", encoding="utf-8")
    result = mod.extract_facts(f)
    assert "memory" in result["tags"]
    assert "search" in result["tags"]


def test_build_enriched_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    facts = {
        "title": "AgentFS", "tags": ["memory"], "summary": "Agent filesystem.",
        "projects": "Yodoca", "path": "docs/agentfs.md",
        "chunks": [], "tokens": 100,
    }
    result = mod.build_enriched(facts, "## Content\n\nSome enriched content.")
    assert isinstance(result, str)
    assert "AgentFS" in result
