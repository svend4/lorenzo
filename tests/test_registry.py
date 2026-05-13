"""
Тесты для scripts/improve_registry.py.

Покрытие:
  - collect_scripts()    — читает scripts_catalog.json
  - collect_templates()  — читает JSON-схемы из _schemas/
  - collect_skills()     — читает .claude/skills/*.md
  - collect_mcp_servers()— читает .claude/mcp.json
  - collect_tasks()      — читает tasks/_generated/*.json
  - collect_contacts()   — читает docs/contacts/*.md
"""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_registry")

# ── collect_scripts ───────────────────────────────────────────────────────────

def test_collect_scripts_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.collect_scripts()
    assert isinstance(result, list)


def test_collect_scripts_empty_when_no_catalog(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    result = mod.collect_scripts()
    assert result == []


def test_collect_scripts_reads_catalog(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    catalog = [{"name": "improve_foo.py", "group": "reports"}]
    (tmp_path / "scripts_catalog.json").write_text(json.dumps(catalog), encoding="utf-8")
    result = mod.collect_scripts()
    assert len(result) == 1
    assert result[0]["name"] == "improve_foo.py"


# ── collect_templates ─────────────────────────────────────────────────────────

def test_collect_templates_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCHEMAS", tmp_path)
    result = mod.collect_templates()
    assert isinstance(result, list)


def test_collect_templates_empty_when_no_schemas_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCHEMAS", tmp_path / "nonexistent")
    result = mod.collect_templates()
    assert result == []


def test_collect_templates_reads_schema(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCHEMAS", tmp_path)
    schema = {"description": "Test schema", "required": ["title"], "required_sections": ["## Overview"]}
    (tmp_path / "project.json").write_text(json.dumps(schema), encoding="utf-8")
    result = mod.collect_templates()
    assert len(result) == 1
    assert result[0]["name"] == "project"
    assert result[0]["description"] == "Test schema"


def test_collect_templates_invalid_json_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCHEMAS", tmp_path)
    (tmp_path / "bad.json").write_text("not json", encoding="utf-8")
    result = mod.collect_templates()
    assert result == []


def test_collect_templates_has_required_fields_key(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCHEMAS", tmp_path)
    schema = {"required": ["title", "author"]}
    (tmp_path / "card.json").write_text(json.dumps(schema), encoding="utf-8")
    result = mod.collect_templates()
    assert "required_fields" in result[0]
    assert result[0]["required_fields"] == ["title", "author"]


# ── collect_skills ────────────────────────────────────────────────────────────

def test_collect_skills_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SKILLS", tmp_path)
    result = mod.collect_skills()
    assert isinstance(result, list)


def test_collect_skills_empty_when_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SKILLS", tmp_path / "nonexistent")
    result = mod.collect_skills()
    assert result == []


def test_collect_skills_reads_skill_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SKILLS", tmp_path)
    skill = tmp_path / "analyze-project.md"
    skill.write_text("# Analyze Project\n\nDescribes how to analyze a project.", encoding="utf-8")
    result = mod.collect_skills()
    assert len(result) == 1
    assert result[0]["name"] == "analyze-project"


def test_collect_skills_extracts_description(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SKILLS", tmp_path)
    skill = tmp_path / "my-skill.md"
    skill.write_text("# My Skill\n\nThis is the skill description.", encoding="utf-8")
    result = mod.collect_skills()
    assert "description" in result[0]
    assert result[0]["description"]  # non-empty


# ── collect_mcp_servers ───────────────────────────────────────────────────────

def test_collect_mcp_servers_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "MCP_CONFIG", tmp_path / "nonexistent.json")
    result = mod.collect_mcp_servers()
    assert isinstance(result, list)


def test_collect_mcp_servers_empty_when_no_config(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "MCP_CONFIG", tmp_path / "mcp.json")
    result = mod.collect_mcp_servers()
    assert result == []


def test_collect_mcp_servers_reads_config(tmp_path, monkeypatch):
    config_file = tmp_path / "mcp.json"
    config = {"mcpServers": {"my-server": {"command": "python", "args": ["server.py"], "description": "Test"}}}
    config_file.write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.setattr(mod, "MCP_CONFIG", config_file)
    result = mod.collect_mcp_servers()
    assert len(result) == 1
    assert result[0]["name"] == "my-server"
    assert result[0]["command"] == "python"


# ── collect_tasks ─────────────────────────────────────────────────────────────

def test_collect_tasks_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path / "nonexistent")
    result = mod.collect_tasks()
    assert isinstance(result, list)


def test_collect_tasks_empty_when_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path / "nonexistent")
    result = mod.collect_tasks()
    assert result == []


def test_collect_tasks_reads_json_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path)
    task = {"id": "task-001", "description": "Build index", "mcp_server": "my-server", "mcp_tool": "build", "template": "card"}
    (tmp_path / "task-001.json").write_text(json.dumps(task), encoding="utf-8")
    result = mod.collect_tasks()
    assert len(result) == 1
    assert result[0]["id"] == "task-001"


def test_collect_tasks_invalid_json_skipped(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path)
    (tmp_path / "bad.json").write_text("not json", encoding="utf-8")
    result = mod.collect_tasks()
    assert result == []


# ── collect_contacts ──────────────────────────────────────────────────────────

def test_collect_contacts_returns_list(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path / "nonexistent")
    result = mod.collect_contacts()
    assert isinstance(result, list)


def test_collect_contacts_empty_when_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path / "nonexistent")
    result = mod.collect_contacts()
    assert result == []


def test_collect_contacts_reads_contact_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path)
    contact = tmp_path / "kksudo.md"
    contact.write_text('---\nauthor: "kksudo"\nstatus: studied\n---\n# kksudo', encoding="utf-8")
    result = mod.collect_contacts()
    assert len(result) == 1
    assert result[0]["author"] == "kksudo"


def test_collect_contacts_skips_readme(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path)
    (tmp_path / "README.md").write_text("# Contacts index", encoding="utf-8")
    result = mod.collect_contacts()
    assert result == []


def test_collect_contacts_extracts_status(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path)
    contact = tmp_path / "author.md"
    contact.write_text('---\nauthor: testuser\nstatus: messaged\n---\n', encoding="utf-8")
    result = mod.collect_contacts()
    assert result[0]["status"] == "messaged"


def test_collect_contacts_uses_stem_when_no_frontmatter(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "CONTACTS", tmp_path)
    contact = tmp_path / "someone.md"
    contact.write_text("# Contact\nNo frontmatter here.", encoding="utf-8")
    result = mod.collect_contacts()
    assert result[0]["author"] == "someone"


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_creates_registry_md(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT", tmp_path / "REGISTRY.md")
    monkeypatch.setattr(mod, "SCRIPTS_DIR", tmp_path / "scripts")
    monkeypatch.setattr(mod, "TEMPLATES", tmp_path / "templates")
    monkeypatch.setattr(mod, "SKILLS", tmp_path / ".claude" / "skills")
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path / "tasks" / "_generated")
    monkeypatch.setattr(mod, "MCP_CONFIG", tmp_path / "mcp.json")
    monkeypatch.setattr(mod, "CONTACTS", tmp_path / "contacts")
    mod.main()
    assert (tmp_path / "REGISTRY.md").exists()


def test_main_registry_has_content(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "OUT", tmp_path / "REGISTRY.md")
    monkeypatch.setattr(mod, "SCRIPTS_DIR", tmp_path / "scripts")
    monkeypatch.setattr(mod, "TEMPLATES", tmp_path / "templates")
    monkeypatch.setattr(mod, "SKILLS", tmp_path / ".claude" / "skills")
    monkeypatch.setattr(mod, "TASKS_GEN", tmp_path / "tasks" / "_generated")
    monkeypatch.setattr(mod, "MCP_CONFIG", tmp_path / "mcp.json")
    monkeypatch.setattr(mod, "CONTACTS", tmp_path / "contacts")
    mod.main()
    text = (tmp_path / "REGISTRY.md").read_text(encoding="utf-8")
    assert "# " in text
