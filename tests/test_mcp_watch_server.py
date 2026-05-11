"""Tests for scripts/mcp_watch_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_watch_server")


# ── tool_recent_changes ───────────────────────────────────────────────────────

def test_tool_recent_changes_returns_string():
    result = mod.tool_recent_changes(hours=24)
    assert isinstance(result, str)


def test_tool_recent_changes_default_hours():
    result = mod.tool_recent_changes()
    assert isinstance(result, str)


# ── tool_pending_actions ──────────────────────────────────────────────────────

def test_tool_pending_actions_returns_string():
    result = mod.tool_pending_actions()
    assert isinstance(result, str)


# ── tool_watch_status ─────────────────────────────────────────────────────────

def test_tool_watch_status_returns_string():
    result = mod.tool_watch_status()
    assert isinstance(result, str)


# ── tool_trigger_recompute ────────────────────────────────────────────────────

def test_tool_trigger_recompute_empty_section():
    result = mod.tool_trigger_recompute("")
    assert isinstance(result, str)


def test_tool_trigger_recompute_returns_string():
    result = mod.tool_trigger_recompute("01-svyazi")
    assert isinstance(result, str)


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_recent_changes():
    result = mod.dispatch("recent_changes", {"hours": 1})
    assert isinstance(result, str)


def test_dispatch_watch_status():
    result = mod.dispatch("watch_status", {})
    assert isinstance(result, str)


def test_dispatch_pending_actions():
    result = mod.dispatch("pending_actions", {})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0
