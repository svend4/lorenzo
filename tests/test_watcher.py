"""
Тесты для scripts/improve_watcher.py.

Покрытие:
  - should_run()      — cooldown-логика
  - handle_change()   — применение правил RULES к пути файла
  - run_script()      — не запускает при cooldown, не падает для несуществующего
"""

import importlib
import sys
import time
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("improve_watcher")

# ── should_run ────────────────────────────────────────────────────────────────

def test_should_run_true_when_never_run():
    mod._last_run.clear()
    assert mod.should_run("improve_metrics.py") is True


def test_should_run_false_immediately_after_run():
    mod._last_run["improve_metrics.py"] = time.time()
    assert mod.should_run("improve_metrics.py") is False


def test_should_run_true_after_cooldown(monkeypatch):
    # Simulate old timestamp beyond COOLDOWN
    mod._last_run["improve_metrics.py"] = time.time() - mod.COOLDOWN - 1
    assert mod.should_run("improve_metrics.py") is True


def test_should_run_different_scripts_independent():
    mod._last_run.clear()
    mod._last_run["improve_metrics.py"] = time.time()
    # A different script should still be runnable
    assert mod.should_run("improve_health.py") is True


def test_should_run_returns_bool():
    mod._last_run.clear()
    result = mod.should_run("any_script.py")
    assert isinstance(result, bool)

# ── handle_change ─────────────────────────────────────────────────────────────

def test_handle_change_md_file_triggers_index_update():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        mod.handle_change(Path("docs/01-svyazi/README.md"))
    assert "improve_index_update.py" in called


def test_handle_change_contacts_triggers_entities():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        mod.handle_change(Path("docs/CONTACTS.md"))
    assert "improve_entities.py" in called


def test_handle_change_readme_triggers_sitemap():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        mod.handle_change(Path("docs/README.md"))
    assert "improve_sitemap.py" in called


def test_handle_change_svyazi_triggers_stats():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        mod.handle_change(Path("docs/01-svyazi/component.md"))
    assert "improve_stats.py" in called


def test_handle_change_py_script_triggers_report():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        mod.handle_change(Path("scripts/improve_metrics.py"))
    assert "improve_report.py" in called


def test_handle_change_no_duplicates():
    mod._last_run.clear()
    called = []
    with patch.object(mod, "run_script", side_effect=lambda s: called.append(s)):
        # CONTACTS.md matches both .md rule and CONTACTS.md rule
        mod.handle_change(Path("docs/CONTACTS.md"))
    # Each script should appear at most once
    assert len(called) == len(set(called))


def test_handle_change_unknown_file_no_crash():
    mod._last_run.clear()
    # A file that matches no rule should not crash
    mod.handle_change(Path("docs/some_random.xyz"))


def test_handle_change_returns_none():
    mod._last_run.clear()
    with patch.object(mod, "run_script"):
        result = mod.handle_change(Path("docs/test.md"))
    assert result is None

# ── run_script ────────────────────────────────────────────────────────────────

def test_run_script_skips_nonexistent_file(monkeypatch):
    mod._last_run.clear()
    ran = []
    monkeypatch.setattr(mod, "ROOT", ROOT)
    # Script that definitely doesn't exist
    with patch("subprocess.run") as mock_run:
        mod.run_script("nonexistent_script_xyz.py")
        mock_run.assert_not_called()


def test_run_script_respects_cooldown():
    mod._last_run["improve_metrics.py"] = time.time()
    with patch("subprocess.run") as mock_run:
        mod.run_script("improve_metrics.py")
        mock_run.assert_not_called()


def test_run_script_updates_last_run(tmp_path, monkeypatch):
    # Script must be at ROOT / "scripts" / name
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    dummy = scripts_dir / "dummy_test_script.py"
    dummy.write_text("print('ok')", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod._last_run.pop("dummy_test_script.py", None)

    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        mod.run_script("dummy_test_script.py")
        assert "dummy_test_script.py" in mod._last_run


# ── main ──────────────────────────────────────────────────────────────────────

def test_main_once_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "run_script", lambda script: None)
    monkeypatch.setattr("sys.argv", ["prog", "--once"])
    mod.main()


def test_main_once_calls_run_script(tmp_path, monkeypatch):
    called = []
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "run_script", lambda s: called.append(s))
    monkeypatch.setattr("sys.argv", ["prog", "--once"])
    mod.main()
    assert len(called) > 0
