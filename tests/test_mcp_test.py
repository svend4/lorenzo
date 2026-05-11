"""Tests for scripts/improve_mcp_test.py."""

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_mcp_test")


def test_servers_is_list():
    assert hasattr(mod, "SERVERS")
    assert isinstance(mod.SERVERS, list)


def test_servers_not_empty():
    assert len(mod.SERVERS) > 0


def test_servers_entries_are_tuples():
    for entry in mod.SERVERS:
        assert isinstance(entry, tuple)
        assert len(entry) == 2


def test_servers_module_names_are_strings():
    for module_name, tests in mod.SERVERS:
        assert isinstance(module_name, str)


def test_servers_tests_are_lists():
    for module_name, tests in mod.SERVERS:
        assert isinstance(tests, list)


def test_servers_include_mcp_search():
    names = [name for name, _ in mod.SERVERS]
    assert "mcp_search_server" in names


def test_servers_include_mcp_contacts():
    names = [name for name, _ in mod.SERVERS]
    assert "mcp_contacts_server" in names


def test_servers_test_tuples_have_tool_and_args():
    for module_name, tests in mod.SERVERS:
        for test in tests:
            assert isinstance(test, tuple)
            assert len(test) == 2
            tool, args = test
            assert isinstance(tool, str)
            assert isinstance(args, dict)


def test_import_function_exists():
    assert hasattr(mod, "_import")
    assert callable(mod._import)


def test_import_nonexistent_module_raises():
    with pytest.raises(Exception):
        mod._import("nonexistent_module_xyz_abc")


def test_scripts_path_attribute():
    assert hasattr(mod, "SCRIPTS")
    assert isinstance(mod.SCRIPTS, Path)


def test_root_path_attribute():
    assert hasattr(mod, "ROOT")
    assert isinstance(mod.ROOT, Path)


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_no_crash_empty_servers(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SERVERS", [])
    mod.main()


def test_main_failed_import_counts(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(mod, "SERVERS", [("nonexistent_mcp_module", [("tool", {})])])
    mod.main()
    out = capsys.readouterr().out
    assert "import" in out.lower() or "❌" in out
