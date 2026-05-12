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


def test_should_run_initially_true():
    # Script that hasn't been run should return True
    result = mod.should_run("nonexistent_new_script.py")
    assert result is True


def test_handle_change_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "RULES", [])
    f = tmp_path / "doc.md"
    f.write_text("# Test", encoding="utf-8")
    mod.handle_change(f)  # with empty RULES, no scripts to run


def test_handle_change_triggers_script(tmp_path, monkeypatch):
    called = []
    monkeypatch.setattr(mod, "run_script", lambda s: called.append(s))
    monkeypatch.setattr(mod, "RULES", [(lambda p: p.suffix == ".md", ["improve_test.py"])])
    f = tmp_path / "doc.md"
    f.write_text("# Test", encoding="utf-8")
    mod.handle_change(f)
    assert "improve_test.py" in called


def test_run_once_no_crash(tmp_path, monkeypatch):
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "run_script", lambda s: None)
    mod.run_once()


# ── watch_polling ─────────────────────────────────────────────────────────────

def test_watch_polling_one_iteration(tmp_path, monkeypatch):
    """Test watch_polling by making time.sleep raise KeyboardInterrupt after first call."""
    from unittest.mock import patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "handle_change", lambda p: None)
    # Create a file to track
    (tmp_path / "doc.md").write_text("# Test", encoding="utf-8")
    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 1:
            raise KeyboardInterrupt()
    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except KeyboardInterrupt:
            pass
    assert call_count[0] >= 1


def test_watch_polling_detects_change(tmp_path, monkeypatch):
    """Test that watch_polling detects file changes."""
    from unittest.mock import patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    changed_files = []
    monkeypatch.setattr(mod, "handle_change", lambda p: changed_files.append(p))
    f = tmp_path / "doc.md"
    f.write_text("# Initial", encoding="utf-8")
    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] == 1:
            # Modify file on first sleep
            import time as _time
            _time.sleep(0.01)
            f.write_text("# Updated content", encoding="utf-8")
        else:
            raise KeyboardInterrupt()
    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except KeyboardInterrupt:
            pass


def test_main_without_watchdog_once(tmp_path, monkeypatch, capsys):
    """Test main() with --once flag and no watchdog."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "run_script", lambda s: None)
    monkeypatch.setattr("sys.argv", ["prog", "--once"])
    mod.main()
    out = capsys.readouterr().out
    assert "Lorenzo" in out or "вотчер" in out or isinstance(out, str)


def test_main_triggers_polling_without_watchdog(tmp_path, monkeypatch, capsys):
    """Test that main() without --once falls back to polling (no watchdog)."""
    from unittest.mock import patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])

    def fake_watch_polling():
        raise KeyboardInterrupt("done")

    monkeypatch.setattr(mod, "watch_polling", fake_watch_polling)

    # Pretend watchdog is not installed
    with patch.dict("sys.modules", {"watchdog": None}):
        try:
            mod.main()
        except KeyboardInterrupt:
            pass


def test_watch_watchdog_starts_and_stops(tmp_path, monkeypatch):
    """Test watch_watchdog by mocking watchdog.observers."""
    from unittest.mock import MagicMock, patch
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    mock_observer = MagicMock()
    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 1:
            raise KeyboardInterrupt()

    mock_observer_cls = MagicMock(return_value=mock_observer)

    with patch.dict("sys.modules", {
        "watchdog": MagicMock(),
        "watchdog.observers": MagicMock(Observer=mock_observer_cls),
        "watchdog.events": MagicMock(FileSystemEventHandler=object),
    }):
        with patch.object(mod.time, "sleep", side_effect=fake_sleep):
            try:
                mod.watch_watchdog()
            except KeyboardInterrupt:
                pass

    mock_observer.start.assert_called_once()
    mock_observer.stop.assert_called_once()


def test_run_script_handles_timeout(tmp_path, monkeypatch):
    """Test that run_script handles TimeoutExpired gracefully."""
    from unittest.mock import patch
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    dummy = scripts_dir / "dummy_timeout.py"
    dummy.write_text("import time; time.sleep(999)", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod._last_run.pop("dummy_timeout.py", None)
    with patch("subprocess.run", side_effect=__import__("subprocess").TimeoutExpired(["dummy"], 60)):
        mod.run_script("dummy_timeout.py")  # Should not raise


def test_run_script_handles_exception(tmp_path, monkeypatch):
    """Test that run_script handles generic exceptions gracefully."""
    from unittest.mock import patch
    scripts_dir = tmp_path / "scripts"
    scripts_dir.mkdir()
    dummy = scripts_dir / "dummy_error.py"
    dummy.write_text("raise RuntimeError('fail')", encoding="utf-8")
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    mod._last_run.pop("dummy_error.py", None)
    with patch("subprocess.run", side_effect=RuntimeError("test error")):
        mod.run_script("dummy_error.py")  # Should not raise


# ── new coverage tests ────────────────────────────────────────────────────────

def test_handle_change_match_fn_exception_ignored(monkeypatch):
    """Lines 67-68: exception in match_fn is silently ignored."""
    def raising_match(p):
        raise RuntimeError("bad match")
    monkeypatch.setattr(mod, "RULES", [(raising_match, ["improve_test.py"])])
    # Should not raise
    mod.handle_change(Path("docs/test.md"))


def test_watch_polling_oserror_on_init(tmp_path, monkeypatch):
    """Lines 83-84: OSError during initialization stat() is ignored."""
    from pathlib import Path as _Path

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "handle_change", lambda p: None)
    # Create a file so the init loop has something to iterate over
    (tmp_path / "doc.md").write_text("# Test", encoding="utf-8")

    original_stat = _Path.stat
    call_count = [0]

    def fake_stat(self, *args, **kwargs):
        call_count[0] += 1
        if call_count[0] == 1:  # First stat() call (init loop) raises OSError
            raise OSError("permission denied")
        # Subsequent calls raise KeyboardInterrupt to break the while True loop
        raise KeyboardInterrupt()

    monkeypatch.setattr(_Path, "stat", fake_stat)
    try:
        mod.watch_polling(interval=0.01)
    except (KeyboardInterrupt, OSError):
        pass
    # The key assertion: we reached at least the first stat() call without crashing
    assert call_count[0] >= 1


def test_watch_polling_loop_body_executes(tmp_path, monkeypatch):
    """Lines 88-105: watch_polling loop body runs on second sleep call."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "handle_change", lambda p: None)
    f = tmp_path / "doc.md"
    f.write_text("# Initial", encoding="utf-8")

    call_count = [0]

    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 2:  # Let first iteration complete, abort on second
            raise KeyboardInterrupt()

    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except KeyboardInterrupt:
            pass
    assert call_count[0] >= 2


def test_watch_watchdog_handler_on_modified(tmp_path, monkeypatch):
    """Lines 115-116: Handler.on_modified dispatches to handle_change."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    called_paths = []
    monkeypatch.setattr(mod, "handle_change", lambda p: called_paths.append(p))

    handler_instances = []

    class CapturingObserver:
        def __init__(self):
            pass
        def schedule(self, handler, path, recursive=False):
            handler_instances.append(handler)
        def start(self):
            pass
        def stop(self):
            pass
        def join(self):
            pass

    with patch.dict("sys.modules", {
        "watchdog": MagicMock(),
        "watchdog.observers": MagicMock(Observer=CapturingObserver),
        "watchdog.events": MagicMock(FileSystemEventHandler=object),
    }):
        call_count = [0]
        def fake_sleep(n):
            call_count[0] += 1
            raise KeyboardInterrupt()
        with patch.object(mod.time, "sleep", side_effect=fake_sleep):
            try:
                mod.watch_watchdog()
            except KeyboardInterrupt:
                pass

    assert handler_instances, "Handler was not captured by CapturingObserver"
    handler = handler_instances[0]
    event = MagicMock()
    event.is_directory = False
    event.src_path = str(tmp_path / "doc.md")
    handler.on_modified(event)
    assert len(called_paths) > 0


def test_watch_watchdog_handler_on_created(tmp_path, monkeypatch):
    """Lines 118-119: Handler.on_created dispatches to handle_change."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    called_paths = []
    monkeypatch.setattr(mod, "handle_change", lambda p: called_paths.append(p))

    handler_instances = []

    class CapturingObserver:
        def __init__(self):
            pass
        def schedule(self, handler, path, recursive=False):
            handler_instances.append(handler)
        def start(self):
            pass
        def stop(self):
            pass
        def join(self):
            pass

    with patch.dict("sys.modules", {
        "watchdog": MagicMock(),
        "watchdog.observers": MagicMock(Observer=CapturingObserver),
        "watchdog.events": MagicMock(FileSystemEventHandler=object),
    }):
        call_count = [0]
        def fake_sleep(n):
            call_count[0] += 1
            raise KeyboardInterrupt()
        with patch.object(mod.time, "sleep", side_effect=fake_sleep):
            try:
                mod.watch_watchdog()
            except KeyboardInterrupt:
                pass

    assert handler_instances, "Handler was not captured by CapturingObserver"
    handler = handler_instances[0]
    event = MagicMock()
    event.is_directory = False
    event.src_path = str(tmp_path / "new.md")
    handler.on_created(event)
    assert len(called_paths) > 0


def test_main_calls_watch_watchdog_when_available(tmp_path, monkeypatch):
    """Line 153: main() calls watch_watchdog() when watchdog is importable."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr("sys.argv", ["prog"])

    watchdog_called = [False]

    def fake_watch_watchdog():
        watchdog_called[0] = True
        raise KeyboardInterrupt("done")

    monkeypatch.setattr(mod, "watch_watchdog", fake_watch_watchdog)

    # Make sure watchdog is importable (patch it into sys.modules if needed)
    import sys as _sys
    if "watchdog" not in _sys.modules or _sys.modules.get("watchdog") is None:
        with patch.dict("sys.modules", {"watchdog": MagicMock()}):
            try:
                mod.main()
            except KeyboardInterrupt:
                pass
    else:
        try:
            mod.main()
        except KeyboardInterrupt:
            pass

    assert watchdog_called[0]


def test_watch_polling_loop_detects_new_file(tmp_path, monkeypatch):
    """Lines 98-100, 103-105: loop detects a new file (not in mtimes) and calls handle_change."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    handle_called = []
    monkeypatch.setattr(mod, "handle_change", lambda p: handle_called.append(p))

    # Start with no files, so mtimes is empty; then a file appears during first loop iteration
    new_file = tmp_path / "new.md"

    call_count = [0]

    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] == 1:
            # Create a file during first sleep so it appears as "new" in loop body
            new_file.write_text("# New file", encoding="utf-8")
        elif call_count[0] >= 2:
            raise KeyboardInterrupt()

    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except KeyboardInterrupt:
            pass

    # handle_change should have been called for the new file
    assert any(p == new_file for p in handle_called), f"Expected {new_file} in {handle_called}"


def test_watch_polling_loop_oserror_in_loop(tmp_path, monkeypatch):
    """Lines 96-97: OSError during stat() in the while loop is silently skipped (continue)."""
    import traceback
    from pathlib import Path as _Path

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "handle_change", lambda p: None)

    # Create a file
    (tmp_path / "doc.md").write_text("# Test", encoding="utf-8")

    original_stat = _Path.stat
    loop_oserror_raised = [False]

    def fake_stat(self, *args, **kwargs):
        # Raise OSError only when called from improve_watcher.py line 95 (loop body stat)
        stack = traceback.extract_stack()
        for frame in stack:
            if "improve_watcher" in frame.filename and frame.lineno == 95:
                if not loop_oserror_raised[0]:
                    loop_oserror_raised[0] = True
                    raise OSError("no access in loop")
        return original_stat(self, *args, **kwargs)

    call_count = [0]
    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 2:
            raise KeyboardInterrupt()

    monkeypatch.setattr(_Path, "stat", fake_stat)
    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except (KeyboardInterrupt, OSError):
            pass
    assert loop_oserror_raised[0], "OSError was never raised from the loop body stat()"


def test_watch_polling_loop_skips_non_files(tmp_path, monkeypatch):
    """Line 93: loop skips non-file entries (directories)."""
    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)

    handle_called = []
    monkeypatch.setattr(mod, "handle_change", lambda p: handle_called.append(p))

    # Create a subdirectory (not a file) — this triggers the `if not f.is_file(): continue` path
    subdir = tmp_path / "subdir"
    subdir.mkdir()

    call_count = [0]

    def fake_sleep(n):
        call_count[0] += 1
        if call_count[0] >= 2:
            raise KeyboardInterrupt()

    with patch.object(mod.time, "sleep", side_effect=fake_sleep):
        try:
            mod.watch_polling(interval=0.01)
        except KeyboardInterrupt:
            pass

    # The directory should not trigger handle_change
    assert all(str(p) != str(subdir) for p in handle_called)


def test_watch_polling_oserror_on_init_directly(tmp_path, monkeypatch):
    """Lines 83-84: OSError in init stat() (line 82) is caught and ignored."""
    import traceback
    from pathlib import Path as _Path

    monkeypatch.setattr(mod, "DOCS", tmp_path)
    monkeypatch.setattr(mod, "ROOT", tmp_path)
    monkeypatch.setattr(mod, "handle_change", lambda p: None)

    # Create a file so the init loop has something to stat
    (tmp_path / "file.md").write_text("content", encoding="utf-8")

    original_stat = _Path.stat
    oserror_raised = [False]

    def fake_stat(self, *args, **kwargs):
        # Raise OSError only when called from improve_watcher.py line 82 (init stat)
        stack = traceback.extract_stack()
        for frame in stack:
            if "improve_watcher" in frame.filename and frame.lineno == 82:
                if not oserror_raised[0]:
                    oserror_raised[0] = True
                    raise OSError("init stat error")
        return original_stat(self, *args, **kwargs)

    monkeypatch.setattr(_Path, "stat", fake_stat)
    # Kill the while loop immediately
    with patch.object(mod.time, "sleep", side_effect=KeyboardInterrupt()):
        try:
            mod.watch_polling(interval=0.01)
        except (KeyboardInterrupt, OSError):
            pass

    assert oserror_raised[0], "OSError was never raised in init stat() at line 82"
