"""Tests for scripts/mcp_ops_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_ops_server")


# ── tool_audit_query ──────────────────────────────────────────────────────────

def test_tool_audit_query_empty_sql():
    result = mod.tool_audit_query("")
    assert isinstance(result, str)
    assert "❌" in result or "укаж" in result.lower()


def test_tool_audit_query_non_select_rejected():
    result = mod.tool_audit_query("DROP TABLE events;")
    assert isinstance(result, str)
    assert "select" in result.lower() or "❌" in result or "только" in result.lower()


def test_tool_audit_query_valid_select_no_db():
    # When DB is not available, should return error string not raise
    result = mod.tool_audit_query("SELECT * FROM events LIMIT 5")
    assert isinstance(result, str)


# ── tool_audit_top_tools ──────────────────────────────────────────────────────

def test_tool_audit_top_tools_returns_string():
    result = mod.tool_audit_top_tools(n=5)
    assert isinstance(result, str)


# ── tool_audit_slow_calls ──────────────────────────────────────────────────────

def test_tool_audit_slow_calls_returns_string():
    result = mod.tool_audit_slow_calls(threshold_ms=100)
    assert isinstance(result, str)


# ── tool_workflow_history ─────────────────────────────────────────────────────

def test_tool_workflow_history_returns_string():
    result = mod.tool_workflow_history()
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_audit_query_empty():
    result = mod.dispatch("audit_query", {"sql": ""})
    assert isinstance(result, str)


def test_dispatch_audit_top_tools():
    result = mod.dispatch("audit_top_tools", {"n": 5})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_root_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)
