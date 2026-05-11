"""Tests for scripts/improve_named_entity_index.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_named_entity_index")


def test_clean_returns_string():
    result = mod._clean("some text here")
    assert isinstance(result, str)


def test_clean_removes_code():
    result = mod._clean("Before\n```python\ncode here\n```\nAfter")
    assert "code here" not in result


def test_extract_entities_returns_dict(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("kksudo created AgentFS.", f)
    assert isinstance(result, dict)


def test_extract_entities_has_required_keys(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("some text here", f)
    for key in ("people", "projects", "tech", "orgs", "dates"):
        assert key in result


def test_extract_entities_finds_known_person(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("kksudo created AgentFS project.", f)
    assert "kksudo" in result["people"]


def test_extract_entities_finds_known_project(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("Using AgentFS for knowledge storage.", f)
    assert "agentfs" in result["projects"]


def test_extract_entities_finds_tech(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("Using MCP and RAG architecture.", f)
    assert "mcp" in result["tech"] or "rag" in result["tech"]


def test_extract_entities_finds_date(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("Released in 2024-03 by the team.", f)
    assert len(result["dates"]) >= 1


def test_extract_entities_deduplicates(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("kksudo and kksudo are the same person.", f)
    assert result["people"].count("kksudo") == 1


def test_extract_entities_github_url(tmp_path):
    f = tmp_path / "test.md"
    result = mod._extract_entities("See github.com/kksudo/agentfs for source.", f)
    combined = result["people"] + result["projects"]
    assert len(combined) > 0


def test_known_people_list_exists():
    assert hasattr(mod, "KNOWN_PEOPLE")
    assert len(mod.KNOWN_PEOPLE) > 0


def test_known_projects_list_exists():
    assert hasattr(mod, "KNOWN_PROJECTS")
    assert len(mod.KNOWN_PROJECTS) > 0
