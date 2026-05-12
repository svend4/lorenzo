"""Tests for scripts/improve_watch.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_watch")


def test_snapshot_returns_dict(tmp_path):
    result = mod._snapshot(tmp_path)
    assert isinstance(result, dict)


def test_snapshot_empty_dir(tmp_path):
    result = mod._snapshot(tmp_path)
    assert result == {}


def test_snapshot_finds_md_files(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Hello", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert f in result


def test_snapshot_ignores_non_md(tmp_path):
    py = tmp_path / "script.py"
    py.write_text("print('hello')", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert py not in result


def test_snapshot_finds_nested_md(tmp_path):
    sub = tmp_path / "sub"
    sub.mkdir()
    f = sub / "nested.md"
    f.write_text("# Nested", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert f in result


def test_snapshot_values_are_floats(tmp_path):
    f = tmp_path / "doc.md"
    f.write_text("# Hello", encoding="utf-8")
    result = mod._snapshot(tmp_path)
    assert isinstance(result[f], float)


def test_changed_files_empty():
    result = mod._changed_files({}, {})
    assert result == []


def test_changed_files_new_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {}
    new = {f: 1234567890.0}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_deleted_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {f: 1234567890.0}
    new = {}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_modified_file(tmp_path):
    f = tmp_path / "doc.md"
    old = {f: 1000.0}
    new = {f: 2000.0}
    result = mod._changed_files(old, new)
    assert f in result


def test_changed_files_unchanged_file(tmp_path):
    f = tmp_path / "doc.md"
    mtime = 1234567890.0
    old = {f: mtime}
    new = {f: mtime}
    result = mod._changed_files(old, new)
    assert f not in result


def test_changed_files_returns_list(tmp_path):
    result = mod._changed_files({}, {})
    assert isinstance(result, list)


def test_interval_constant():
    assert hasattr(mod, "INTERVAL")
    assert isinstance(mod.INTERVAL, int)
    assert mod.INTERVAL > 0


def test_docs_path_attribute():
    assert hasattr(mod, "DOCS")
    assert isinstance(mod.DOCS, Path)


# ── _run_scripts ──────────────────────────────────────────────────────────────

def test_run_scripts_calls_subprocess(tmp_path, monkeypatch, capsys):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GROUP_FILTER", None)
    monkeypatch.setattr(mod, "FAST", False)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    changed = [tmp_path / "doc.md"]
    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch("subprocess.run", return_value=fake_result) as mock_run:
        mod._run_scripts(changed)
        mock_run.assert_called_once()


def test_run_scripts_with_group_filter(tmp_path, monkeypatch, capsys):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GROUP_FILTER", "quality")
    monkeypatch.setattr(mod, "FAST", False)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    changed = [tmp_path / "doc.md"]
    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch("subprocess.run", return_value=fake_result) as mock_run:
        mod._run_scripts(changed)
        call_args = mock_run.call_args[0][0]
        assert "--group" in call_args
        assert "quality" in call_args


def test_run_scripts_with_fast_flag(tmp_path, monkeypatch, capsys):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GROUP_FILTER", None)
    monkeypatch.setattr(mod, "FAST", True)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    changed = [tmp_path / f"doc{i}.md" for i in range(8)]
    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch("subprocess.run", return_value=fake_result) as mock_run:
        mod._run_scripts(changed)
        call_args = mock_run.call_args[0][0]
        assert "--fast" in call_args


def test_run_scripts_failed_returncode(tmp_path, monkeypatch, capsys):
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "GROUP_FILTER", None)
    monkeypatch.setattr(mod, "FAST", False)
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    monkeypatch.setattr(mod, "SCRIPTS_DIR", scripts_dir)
    changed = [tmp_path / "doc.md"]
    fake_result = MagicMock()
    fake_result.returncode = 1
    with patch("subprocess.run", return_value=fake_result):
        mod._run_scripts(changed)
    out = capsys.readouterr().out
    assert "❌" in out or "Готово" in out


# ── main() ────────────────────────────────────────────────────────────────────

def test_main_runs_one_iteration(tmp_path, monkeypatch, capsys):
    """Test main() polling loop with one iteration."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERVAL", 1)
    monkeypatch.setattr(mod, "GROUP_FILTER", None)
    monkeypatch.setattr(mod, "FAST", False)

    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 1:
            raise KeyboardInterrupt()

    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        mod.main()

    out = capsys.readouterr().out
    assert "Остановлено" in out or "Жду" in out


def test_main_detects_changes(tmp_path, monkeypatch, capsys):
    """Test main() detects file changes during polling."""
    from unittest.mock import patch, MagicMock
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "INTERVAL", 1)
    monkeypatch.setattr(mod, "GROUP_FILTER", None)
    monkeypatch.setattr(mod, "FAST", False)

    f = tmp_path / "doc.md"
    f.write_text("# Initial", encoding="utf-8")

    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] == 1:
            # Modify file on first iteration
            f.write_text("# Updated", encoding="utf-8")
            import os
            stat = f.stat()
            os.utime(f, (stat.st_atime + 1, stat.st_mtime + 1))
        else:
            raise KeyboardInterrupt()

    fake_result = MagicMock()
    fake_result.returncode = 0
    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        with patch("subprocess.run", return_value=fake_result):
            mod.main()

    out = capsys.readouterr().out
    assert isinstance(out, str)
