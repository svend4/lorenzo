"""Tests for scripts/mcp_runner_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_runner_server")


# ── tool_list_scripts ─────────────────────────────────────────────────────────

def test_tool_list_scripts_returns_string():
    result = mod.tool_list_scripts()
    assert isinstance(result, str)


def test_tool_list_scripts_mentions_scripts():
    result = mod.tool_list_scripts()
    assert "improve_" in result or "скрипт" in result.lower()


def test_tool_list_scripts_group_filter():
    result = mod.tool_list_scripts(group="reports")
    assert isinstance(result, str)


# ── tool_describe_script ──────────────────────────────────────────────────────

def test_tool_describe_script_not_in_catalog():
    result = mod.tool_describe_script("improve_nonexistent_xyz.py")
    assert isinstance(result, str)
    assert "не найден" in result.lower() or "❌" in result


def test_tool_describe_script_adds_py_extension():
    result = mod.tool_describe_script("improve_nonexistent_xyz")
    assert isinstance(result, str)


# ── tool_run_improve ──────────────────────────────────────────────────────────

def test_tool_run_improve_empty_script():
    result = mod.tool_run_improve("")
    assert isinstance(result, str)
    assert "❌" in result or "укаж" in result.lower()


def test_tool_run_improve_non_improve_script():
    result = mod.tool_run_improve("gateway.py")
    assert isinstance(result, str)
    assert "❌" in result
    assert "improve_" in result


def test_tool_run_improve_nonexistent():
    result = mod.tool_run_improve("improve_nonexistent_xyz_script.py")
    assert isinstance(result, str)
    assert "❌" in result or "не найден" in result.lower()


# ── tool_run_group ────────────────────────────────────────────────────────────

def test_tool_run_group_empty():
    result = mod.tool_run_group("")
    assert isinstance(result, str)
    assert "❌" in result or "укаж" in result.lower()


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_list_scripts():
    result = mod.dispatch("list_scripts", {"group": "all"})
    assert isinstance(result, str)


def test_dispatch_describe_script():
    result = mod.dispatch("describe_script", {"name": "improve_nonexistent.py"})
    assert isinstance(result, str)


def test_dispatch_run_improve_empty():
    result = mod.dispatch("run_improve", {"script": "", "dry_run": True})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0
