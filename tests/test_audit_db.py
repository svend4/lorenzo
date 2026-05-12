"""Tests for scripts/improve_audit_db.py."""

import importlib
import json
import sqlite3
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_audit_db")


def test_schema_is_string():
    assert hasattr(mod, "SCHEMA")
    assert isinstance(mod.SCHEMA, str)


def test_schema_has_mcp_calls_table():
    assert "mcp_calls" in mod.SCHEMA


def test_schema_has_workflow_runs_table():
    assert "workflow_runs" in mod.SCHEMA


def test_schema_has_skill_metrics_table():
    assert "skill_metrics" in mod.SCHEMA


def test_get_db_returns_connection(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "test.sqlite")
    conn = mod.get_db()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_get_db_creates_tables(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "test.sqlite")
    conn = mod.get_db()
    tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
    conn.close()
    assert "mcp_calls" in tables
    assert "workflow_runs" in tables
    assert "skill_metrics" in tables


def test_rebuild_creates_db(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "audit.sqlite")
    monkeypatch.setattr(mod, "CLAUDE_DIR", tmp_path)
    mod.rebuild()
    assert (tmp_path / "audit.sqlite").exists()


def test_rebuild_with_mcp_log(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "audit.sqlite")
    monkeypatch.setattr(mod, "CLAUDE_DIR", tmp_path)
    log = tmp_path / "mcp_calls.jsonl"
    entry = {"ts": "2024-01-01T10:00:00", "server": "test-server", "tool": "search", "duration_ms": 50, "status": "ok"}
    log.write_text(json.dumps(entry), encoding="utf-8")
    mod.rebuild()
    conn = sqlite3.connect(str(tmp_path / "audit.sqlite"))
    count = conn.execute("SELECT COUNT(*) FROM mcp_calls").fetchone()[0]
    conn.close()
    assert count == 1


def test_rebuild_with_skill_metrics_log(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "audit.sqlite")
    monkeypatch.setattr(mod, "CLAUDE_DIR", tmp_path)
    log = tmp_path / "skill_metrics.jsonl"
    entry = {"ts": "2024-01-01T10:00:00", "skill": "analyze", "scores": {"helpful": 4, "complete": 5}}
    log.write_text(json.dumps(entry), encoding="utf-8")
    mod.rebuild()
    conn = sqlite3.connect(str(tmp_path / "audit.sqlite"))
    count = conn.execute("SELECT COUNT(*) FROM skill_metrics").fetchone()[0]
    conn.close()
    assert count == 1


def test_cmd_query_returns_zero_on_success(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "audit.sqlite")
    conn = mod.get_db()
    conn.close()
    result = mod.cmd_query("SELECT 1 AS val")
    assert result == 0


def test_cmd_query_returns_one_on_error(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "DB_PATH", tmp_path / "audit.sqlite")
    conn = mod.get_db()
    conn.close()
    result = mod.cmd_query("SELECT * FROM nonexistent_table_xyz")
    assert result == 1


def test_db_path_attribute():
    assert hasattr(mod, "DB_PATH")
    assert isinstance(mod.DB_PATH, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_rebuild_no_crash(tmp_path, monkeypatch):
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLAUDE_DIR", claude_dir)
    monkeypatch.setattr(mod, "DB_PATH", claude_dir / "audit.sqlite")
    monkeypatch.setattr("sys.argv", ["prog", "--rebuild"])
    result = mod.main()
    assert result == 0


def test_main_default_no_crash(tmp_path, monkeypatch):
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLAUDE_DIR", claude_dir)
    monkeypatch.setattr(mod, "DB_PATH", claude_dir / "audit.sqlite")
    monkeypatch.setattr("sys.argv", ["prog"])
    mod.main()  # must not raise


def test_main_top_tools_no_crash(tmp_path, monkeypatch):
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLAUDE_DIR", claude_dir)
    monkeypatch.setattr(mod, "DB_PATH", claude_dir / "audit.sqlite")
    monkeypatch.setattr("sys.argv", ["prog", "--top-tools", "3"])
    mod.main()  # must not raise


def _setup_audit(tmp_path, monkeypatch):
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir()
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "CLAUDE_DIR", claude_dir)
    monkeypatch.setattr(mod, "DB_PATH", claude_dir / "audit.sqlite")
    return claude_dir


def test_main_rebuild_no_crash(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--rebuild"])
    result = mod.main()
    assert result == 0


def test_main_query_no_crash(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--query", "SELECT 1"])
    mod.main()


def test_main_slow_calls_no_crash(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--slow-calls", "50"])
    mod.main()


def test_main_recent_no_crash(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--recent", "5"])
    mod.main()


def test_main_workflow_stats_no_crash(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    monkeypatch.setattr("sys.argv", ["prog", "--workflow-stats"])
    mod.main()


def test_rebuild_with_mcp_log(tmp_path, monkeypatch):
    import json as _json
    claude_dir = _setup_audit(tmp_path, monkeypatch)
    mcp_log = claude_dir / "mcp_calls.jsonl"
    mcp_log.write_text(
        _json.dumps({"ts": "2026-01-01T10:00:00", "server": "test",
                     "tool": "search", "args": {}, "duration_ms": 50, "status": "ok"}) + "\n",
        encoding="utf-8"
    )
    monkeypatch.setattr("sys.argv", ["prog", "--rebuild"])
    mod.main()


def test_get_db_creates_db(tmp_path, monkeypatch):
    _setup_audit(tmp_path, monkeypatch)
    conn = mod.get_db()
    conn.close()
    claude_dir = tmp_path / ".claude"
    assert (claude_dir / "audit.sqlite").exists()
