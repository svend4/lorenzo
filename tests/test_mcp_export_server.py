"""Tests for scripts/mcp_export_server.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("mcp_export_server")


# ── dispatch ──────────────────────────────────────────────────────────────────

def test_dispatch_export_rss_returns_string():
    result = mod.dispatch("export_rss", {"days": 7})
    assert isinstance(result, str)


def test_dispatch_list_formats_returns_string():
    result = mod.dispatch("list_formats", {})
    assert isinstance(result, str)


def test_dispatch_export_csv_returns_string():
    result = mod.dispatch("export_csv", {})
    assert isinstance(result, str)


def test_dispatch_unknown_tool():
    result = mod.dispatch("unknown_xyz", {})
    assert "unknown_xyz" in result or "Неизвестный" in result


def test_dispatch_export_obsidian_dry_run():
    result = mod.dispatch("export_obsidian", {"section": ""})
    assert isinstance(result, str)


def test_dispatch_export_report():
    result = mod.dispatch("export_report", {})
    assert isinstance(result, str)


# ── TOOLS ─────────────────────────────────────────────────────────────────────

def test_tools_is_list():
    assert isinstance(mod.TOOLS, list)
    assert len(mod.TOOLS) > 0


def test_root_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)
