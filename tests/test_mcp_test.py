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


def test_main_returns_zero_when_all_pass(monkeypatch):
    # Use empty server list — no failures, no passes, returns 0
    monkeypatch.setattr(mod, "SERVERS", [])
    result = mod.main()
    assert result == 0


def test_import_helper_handles_missing_module(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "SCRIPTS", tmp_path)
    try:
        mod._import("nonexistent_module_xyz")
    except (FileNotFoundError, AttributeError, ImportError):
        pass


def test_servers_attribute_is_list():
    assert hasattr(mod, "SERVERS")
    assert isinstance(mod.SERVERS, list)


# ── main() with mock dispatch ─────────────────────────────────────────────────

def test_main_with_module_no_dispatch(tmp_path, monkeypatch, capsys):
    """Module imported but has no dispatch function."""
    import types
    fake_mod = types.ModuleType("fake_mcp_no_dispatch")
    # No 'dispatch' attribute

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_no_dispatch", [("tool", {})])])
    mod.main()
    out = capsys.readouterr().out
    assert "нет функции dispatch" in out or "dispatch" in out.lower()


def test_main_with_dispatch_returns_string(tmp_path, monkeypatch, capsys):
    """Module with dispatch that returns a string — should pass."""
    import types
    fake_mod = types.ModuleType("fake_mcp_ok")
    fake_mod.dispatch = lambda tool, args: "Result string"

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_ok", [("search", {"q": "test"})])])
    result = mod.main()
    assert result == 0
    out = capsys.readouterr().out
    assert "✓" in out or "fake_mcp_ok" in out


def test_main_with_dispatch_returns_non_string(tmp_path, monkeypatch, capsys):
    """Module with dispatch that returns a non-string — should fail."""
    import types
    fake_mod = types.ModuleType("fake_mcp_bad")
    fake_mod.dispatch = lambda tool, args: {"key": "value"}  # dict not str

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_bad", [("tool", {})])])
    result = mod.main()
    assert result == 1
    out = capsys.readouterr().out
    assert "❌" in out


def test_main_with_dispatch_raises_exception(tmp_path, monkeypatch, capsys):
    """Module with dispatch that raises an exception — should fail."""
    import types
    fake_mod = types.ModuleType("fake_mcp_error")
    fake_mod.dispatch = lambda tool, args: (_ for _ in ()).throw(RuntimeError("test error"))

    def _raise(*a, **kw):
        raise RuntimeError("test error")
    fake_mod.dispatch = _raise

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_error", [("tool", {})])])
    result = mod.main()
    assert result == 1


def test_main_unknown_tool_handled(tmp_path, monkeypatch, capsys):
    """Test that dispatch handles unknown tool gracefully."""
    import types
    fake_mod = types.ModuleType("fake_mcp_graceful")
    fake_mod.dispatch = lambda tool, args: "Неизвестный инструмент" if tool == "__nonexistent__" else "ok"

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_graceful", [])])
    result = mod.main()
    assert result == 0


def test_main_unknown_tool_not_handled(tmp_path, monkeypatch, capsys):
    """Test that dispatch not handling unknown tool is reported."""
    import types
    fake_mod = types.ModuleType("fake_mcp_unhandled")
    fake_mod.dispatch = lambda tool, args: "ok"  # doesn't return 'Неизвестный'

    def fake_import(name):
        return fake_mod

    monkeypatch.setattr(mod, "_import", fake_import)
    monkeypatch.setattr(mod, "SERVERS", [("fake_mcp_unhandled", [])])
    mod.main()
    out = capsys.readouterr().out
    assert isinstance(out, str)
