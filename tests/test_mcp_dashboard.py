"""Tests for scripts/improve_mcp_dashboard.py."""

import importlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_mcp_dashboard")


def test_main_no_log_creates_output(tmp_path, monkeypatch):
    log = tmp_path / ".claude" / "mcp_calls.jsonl"
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    assert out.exists()
    assert "MCP Dashboard" in out.read_text(encoding="utf-8")


def test_main_no_log_message(tmp_path, monkeypatch):
    log = tmp_path / ".claude" / "mcp_calls.jsonl"
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = out.read_text(encoding="utf-8")
    assert "отсутствуют" in text


def test_main_empty_log(tmp_path, monkeypatch):
    log_dir = tmp_path / ".claude"
    log_dir.mkdir(parents=True)
    log = log_dir / "mcp_calls.jsonl"
    log.write_text("", encoding="utf-8")
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = out.read_text(encoding="utf-8")
    assert "пуст" in text


def test_main_with_entries(tmp_path, monkeypatch):
    log_dir = tmp_path / ".claude"
    log_dir.mkdir(parents=True)
    log = log_dir / "mcp_calls.jsonl"
    entries = [
        {"server": "srv1", "tool": "search", "duration_ms": 120, "ts": "2025-01-01T10:00:00", "status": "ok"},
        {"server": "srv1", "tool": "search", "duration_ms": 80, "ts": "2025-01-01T10:01:00", "status": "ok"},
        {"server": "srv2", "tool": "read", "duration_ms": 50, "ts": "2025-01-01T10:02:00", "status": "error"},
    ]
    log.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = out.read_text(encoding="utf-8")
    assert "srv1" in text
    assert "srv2" in text
    assert "search" in text


def test_main_with_entries_counts(tmp_path, monkeypatch):
    log_dir = tmp_path / ".claude"
    log_dir.mkdir(parents=True)
    log = log_dir / "mcp_calls.jsonl"
    entries = [
        {"server": "srv1", "tool": "search", "duration_ms": 100, "ts": "T1", "status": "ok"},
        {"server": "srv1", "tool": "search", "duration_ms": 200, "ts": "T2", "status": "ok"},
    ]
    log.write_text("\n".join(json.dumps(e) for e in entries), encoding="utf-8")
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = out.read_text(encoding="utf-8")
    assert "2" in text  # total calls


def test_main_returns_zero(tmp_path, monkeypatch):
    log = tmp_path / ".claude" / "mcp_calls.jsonl"
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    result = mod.main()
    assert result == 0


def test_main_skips_invalid_json_lines(tmp_path, monkeypatch):
    log_dir = tmp_path / ".claude"
    log_dir.mkdir(parents=True)
    log = log_dir / "mcp_calls.jsonl"
    valid_entry = {"server": "srv1", "tool": "search", "duration_ms": 100, "ts": "T1", "status": "ok"}
    log.write_text("not valid json\n" + json.dumps(valid_entry) + "\n", encoding="utf-8")
    out = tmp_path / "docs" / "MCP_DASHBOARD.md"
    out.parent.mkdir(parents=True)
    monkeypatch.setattr(mod, "LOG_PATH", log)
    monkeypatch.setattr(mod, "OUT_PATH", out)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod.main()
    text = out.read_text(encoding="utf-8")
    assert "srv1" in text
