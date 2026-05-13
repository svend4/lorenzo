"""Tests for scripts/mcp_templates_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_templates_server")


# ── tool_list_templates ───────────────────────────────────────────────────────

def test_tool_list_templates_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path / "no_templates")
    result = mod.tool_list_templates()
    assert isinstance(result, str)
    assert "не найден" in result.lower() or "templates" in result.lower()


def test_tool_list_templates_with_files(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path)
    schemas = tmp_path / "_schemas"
    schemas.mkdir()
    (tmp_path / "project.md").write_text("# Project Template\n\n{name}", encoding="utf-8")
    result = mod.tool_list_templates()
    assert isinstance(result, str)
    assert "project" in result


def test_tool_list_templates_skips_readme(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path)
    (tmp_path / "README.md").write_text("# README", encoding="utf-8")
    (tmp_path / "contact.md").write_text("# Contact", encoding="utf-8")
    result = mod.tool_list_templates()
    assert "README" not in result
    assert "contact" in result


# ── tool_show_template ────────────────────────────────────────────────────────

def test_tool_show_template_not_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path)
    result = mod.tool_show_template("nonexistent_template")
    assert isinstance(result, str)
    assert "❌" in result or "не найден" in result.lower()


def test_tool_show_template_found(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path)
    (tmp_path / "project.md").write_text("# Project\n\n{name}", encoding="utf-8")
    result = mod.tool_show_template("project")
    assert isinstance(result, str)
    assert "Project" in result


# ── tool_init_doc ─────────────────────────────────────────────────────────────

def test_tool_init_doc_missing_args():
    result = mod.tool_init_doc("", "", {})
    assert isinstance(result, str)
    assert "❌" in result or "укаж" in result.lower()


def test_tool_init_doc_empty_template():
    result = mod.tool_init_doc("", "my-slug", {})
    assert isinstance(result, str)
    assert "❌" in result


def test_tool_validate_doc_missing_path():
    result = mod.tool_validate_doc("")
    assert isinstance(result, str)
    assert "❌" in result or "укаж" in result.lower()


# ── tool_list_tasks ───────────────────────────────────────────────────────────

def test_tool_list_tasks_returns_string(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_DIR", tmp_path)
    result = mod.tool_list_tasks()
    assert isinstance(result, str)


def test_tool_list_tasks_no_dir(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TASKS_DIR", tmp_path / "no_tasks")
    result = mod.tool_list_tasks()
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_list_templates(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path / "no_templates")
    result = mod.dispatch("list_templates", {})
    assert isinstance(result, str)


def test_dispatch_show_template(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "TEMPLATES_DIR", tmp_path)
    result = mod.dispatch("show_template", {"name": "nonexistent"})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_templates_dir_attribute():
    assert hasattr(mod, "TEMPLATES_DIR")
    assert isinstance(mod.TEMPLATES_DIR, Path)
