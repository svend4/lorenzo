"""Tests for scripts/mcp_skills_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_skills_server")


# ── _parse_skill ──────────────────────────────────────────────────────────────

def test_parse_skill_returns_dict():
    text = "# My Skill\n\nDescription of the skill.\n\n## Когда использовать\n\n- \"trigger phrase\"\n"
    result = mod._parse_skill("my-skill", text)
    assert isinstance(result, dict)


def test_parse_skill_has_name():
    text = "# My Skill\n\nDescription.\n"
    result = mod._parse_skill("my-skill", text)
    assert result.get("name") == "my-skill"


def test_parse_skill_extracts_description():
    text = "# My Skill\n\nThis is the description.\n"
    result = mod._parse_skill("my-skill", text)
    assert "description" in result
    assert "This is the description." in result["description"]


def test_parse_skill_extracts_triggers():
    text = (
        "# My Skill\n\nDescription.\n\n"
        "## Когда использовать\n\n"
        '- "анализ проекта"\n'
        '- "review docs"\n'
    )
    result = mod._parse_skill("my-skill", text)
    triggers = result.get("triggers", [])
    assert isinstance(triggers, list)
    assert len(triggers) >= 1


def test_parse_skill_empty_triggers_when_no_section():
    text = "# My Skill\n\nDescription without triggers section.\n"
    result = mod._parse_skill("my-skill", text)
    assert result.get("triggers", []) == []


# ── tool_list_skills ──────────────────────────────────────────────────────────

def test_tool_list_skills_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SKILLS_DIR", tmp_path)
    result = mod.tool_list_skills()
    assert isinstance(result, str)


def test_tool_list_skills_with_files(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (skills_dir / "analyze-project.md").write_text("# Analyze Project\n\nAnalyze.", encoding="utf-8")
    result = mod.tool_list_skills()
    assert isinstance(result, str)
    assert "analyze-project" in result


def test_tool_list_skills_empty_dir(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.tool_list_skills()
    assert isinstance(result, str)


def test_tool_list_skills_no_dir(tmp_path, monkeypatch):
    nonexistent = tmp_path / "no_skills"
    monkeypatch.setattr(mod, "SKILLS_DIR", nonexistent)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.tool_list_skills()
    assert isinstance(result, str)


# ── tool_get_skill ────────────────────────────────────────────────────────────

def test_tool_get_skill_not_found(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.tool_get_skill("nonexistent-skill")
    assert isinstance(result, str)
    assert "не найден" in result.lower() or "❌" in result


def test_tool_get_skill_found(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (skills_dir / "analyze-project.md").write_text("# Analyze Project\n\nContent here.", encoding="utf-8")
    result = mod.tool_get_skill("analyze-project")
    assert isinstance(result, str)
    assert "Analyze Project" in result or "analyze-project" in result


# ── tool_match_skill ──────────────────────────────────────────────────────────

def test_tool_match_skill_empty_query(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.tool_match_skill("")
    assert isinstance(result, str)


def test_tool_match_skill_returns_string(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    (skills_dir / "analyze-project.md").write_text(
        "# Analyze Project\n\nDescription.\n\n## Когда использовать\n\n- \"analyze\"\n",
        encoding="utf-8"
    )
    result = mod.tool_match_skill("analyze project")
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_list_skills(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.dispatch("list_skills", {})
    assert isinstance(result, str)


def test_dispatch_get_skill(tmp_path, monkeypatch):
    skills_dir = tmp_path / "skills"
    skills_dir.mkdir()
    monkeypatch.setattr(mod, "SKILLS_DIR", skills_dir)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.dispatch("get_skill", {"name": "nonexistent"})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_skills_dir_attribute():
    assert hasattr(mod, "SKILLS_DIR")
    assert isinstance(mod.SKILLS_DIR, Path)
