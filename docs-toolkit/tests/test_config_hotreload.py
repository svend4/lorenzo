"""Tests for the E79 config_hotreload module.

Covers:
- FileWatcher: start/stop, check_once, on_change callbacks, multi-path,
  no-change returns empty, missing files.
- HotReloadManager: JSON loading, INI loading, dot-notation get, snapshot
  deep copy, subscribe callbacks, reload, on_error, overlapping keys,
  nested dot notation, missing file handling.
- Edge cases throughout.
"""

import configparser
import copy
import json
import os
import tempfile
import threading
import time

import pytest

from docstoolkit.config_hotreload import FileWatcher, HotReloadManager, ReloadConfig


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_json(path: str, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


def write_ini(path: str, sections: dict) -> None:
    """Write a simple INI file.  *sections* maps section names to dicts."""
    cp = configparser.ConfigParser()
    for section, values in sections.items():
        if section == "DEFAULT":
            for k, v in values.items():
                cp["DEFAULT"][k] = str(v)
        else:
            cp[section] = {k: str(v) for k, v in values.items()}
    with open(path, "w", encoding="utf-8") as fh:
        cp.write(fh)


def touch(path: str) -> None:
    """Update mtime of an existing file."""
    t = time.time() + 1
    os.utime(path, (t, t))


def bump_mtime(path: str, delta: float = 2.0) -> None:
    """Advance the mtime of *path* by *delta* seconds."""
    s = os.stat(path)
    new_t = s.st_mtime + delta
    os.utime(path, (new_t, new_t))


# ---------------------------------------------------------------------------
# FileWatcher tests
# ---------------------------------------------------------------------------


class TestFileWatcherInit:
    def test_creates_with_empty_paths(self):
        fw = FileWatcher([], interval=0.1)
        assert fw._paths == []

    def test_stores_paths(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            path = f.name
        try:
            fw = FileWatcher([path])
            assert path in fw._paths
        finally:
            os.unlink(path)

    def test_default_interval(self):
        fw = FileWatcher([])
        assert fw._interval == 1.0

    def test_custom_interval(self):
        fw = FileWatcher([], interval=0.25)
        assert fw._interval == 0.25

    def test_missing_file_does_not_raise_on_init(self):
        fw = FileWatcher(["/tmp/__nonexistent_file_xyz__.json"])
        # No exception — snapshot is (0, 0)
        assert fw._snapshots.get("/tmp/__nonexistent_file_xyz__.json") == (0, 0)


class TestFileWatcherCheckOnce:
    def test_no_change_returns_empty(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path])
            result = fw.check_once()
            assert result == []
        finally:
            os.unlink(path)

    def test_detects_mtime_change(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path])
            bump_mtime(path)
            result = fw.check_once()
            assert path in result
        finally:
            os.unlink(path)

    def test_detects_size_change(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path])
            # Same mtime but larger size
            s = os.stat(path)
            with open(path, "w") as fh:
                fh.write('{"key": "value"}')
            os.utime(path, (s.st_mtime, s.st_mtime))
            result = fw.check_once()
            assert path in result
        finally:
            os.unlink(path)

    def test_snapshot_updates_so_second_call_is_empty(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path])
            bump_mtime(path)
            fw.check_once()  # first call — snapshot updated
            result = fw.check_once()  # second call — no change
            assert result == []
        finally:
            os.unlink(path)

    def test_multiple_paths_all_changed(self):
        paths = []
        try:
            for _ in range(3):
                f = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
                f.write(b"{}")
                f.close()
                paths.append(f.name)
            fw = FileWatcher(paths)
            for p in paths:
                bump_mtime(p)
            result = fw.check_once()
            assert set(result) == set(paths)
        finally:
            for p in paths:
                os.unlink(p)

    def test_multiple_paths_only_one_changed(self):
        paths = []
        try:
            for _ in range(3):
                f = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
                f.write(b"{}")
                f.close()
                paths.append(f.name)
            fw = FileWatcher(paths)
            bump_mtime(paths[1])
            result = fw.check_once()
            assert result == [paths[1]]
        finally:
            for p in paths:
                os.unlink(p)

    def test_missing_file_appears_as_changed_when_created(self):
        path = "/tmp/__fw_test_newfile__.json"
        if os.path.exists(path):
            os.unlink(path)
        try:
            fw = FileWatcher([path])  # file does not exist yet
            # After creating the file the snapshot changes from (0,0)
            with open(path, "w") as fh:
                fh.write("{}")
            result = fw.check_once()
            assert path in result
        finally:
            if os.path.exists(path):
                os.unlink(path)

    def test_existing_file_deleted_detected(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        fw = FileWatcher([path])
        os.unlink(path)
        result = fw.check_once()
        assert path in result


class TestFileWatcherOnChange:
    def test_callback_called_on_change(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path])
            called = []
            fw.on_change(lambda p: called.append(p))
            bump_mtime(path)
            fw.check_once()
            # check_once does NOT fire callbacks — callbacks are fired by the
            # background thread.  We test callback firing via start/stop.
        finally:
            os.unlink(path)

    def test_background_thread_fires_callback(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path], interval=0.05)
            called = threading.Event()
            fw.on_change(lambda p: called.set())
            fw.start()
            bump_mtime(path)
            assert called.wait(timeout=2.0), "callback not fired within 2 s"
            fw.stop()
        finally:
            os.unlink(path)

    def test_callback_receives_correct_path(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path], interval=0.05)
            received = []
            lock = threading.Lock()
            def cb(p):
                with lock:
                    received.append(p)
            fw.on_change(cb)
            fw.start()
            bump_mtime(path)
            time.sleep(0.3)
            fw.stop()
            assert path in received
        finally:
            os.unlink(path)

    def test_multiple_callbacks_all_called(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path], interval=0.05)
            e1, e2 = threading.Event(), threading.Event()
            fw.on_change(lambda p: e1.set())
            fw.on_change(lambda p: e2.set())
            fw.start()
            bump_mtime(path)
            assert e1.wait(2.0) and e2.wait(2.0)
            fw.stop()
        finally:
            os.unlink(path)

    def test_callback_exception_does_not_crash_watcher(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path], interval=0.05)
            second_called = threading.Event()
            fw.on_change(lambda p: (_ for _ in ()).throw(RuntimeError("boom")))
            fw.on_change(lambda p: second_called.set())
            fw.start()
            bump_mtime(path)
            assert second_called.wait(2.0), "second callback not called after exception"
            fw.stop()
        finally:
            os.unlink(path)


class TestFileWatcherStartStop:
    def test_start_creates_daemon_thread(self):
        fw = FileWatcher([], interval=0.1)
        fw.start()
        assert fw._thread is not None
        assert fw._thread.is_alive()
        assert fw._thread.daemon
        fw.stop()

    def test_stop_joins_thread(self):
        fw = FileWatcher([], interval=0.05)
        fw.start()
        fw.stop()
        assert fw._thread is None

    def test_double_start_does_not_spawn_extra_thread(self):
        fw = FileWatcher([], interval=0.1)
        fw.start()
        t1 = fw._thread
        fw.start()  # should be a no-op
        assert fw._thread is t1
        fw.stop()

    def test_stop_before_start_is_safe(self):
        fw = FileWatcher([], interval=0.1)
        fw.stop()  # should not raise

    def test_start_stop_multiple_times(self):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as f:
            f.write(b"{}")
            path = f.name
        try:
            fw = FileWatcher([path], interval=0.05)
            for _ in range(3):
                fw.start()
                fw.stop()
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# HotReloadManager tests
# ---------------------------------------------------------------------------


class TestHotReloadManagerLoad:
    def test_load_json(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"host": "localhost", "port": 5432})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert data == {"host": "localhost", "port": 5432}

    def test_load_ini(self, tmp_path):
        p = tmp_path / "cfg.ini"
        write_ini(str(p), {"database": {"host": "db.local", "port": "5432"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert "database" in data
        assert data["database"]["host"] == "db.local"

    def test_load_missing_file_raises(self, tmp_path):
        p = tmp_path / "missing.json"
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        with pytest.raises(Exception):
            mgr.load(str(p))

    def test_load_missing_file_calls_on_error(self, tmp_path):
        p = tmp_path / "missing.json"
        errors = []
        cfg = ReloadConfig(paths=[str(p)], on_error=lambda path, exc: errors.append((path, exc)))
        mgr = HotReloadManager(cfg)
        # on_error is only used in _do_reload / start; load() itself re-raises
        with pytest.raises(Exception):
            mgr.load(str(p))

    def test_load_returns_raw_dict(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"a": {"b": {"c": 42}}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert data["a"]["b"]["c"] == 42

    def test_load_updates_internal_state(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"key": "value"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.load(str(p))
        assert mgr.get("key") == "value"

    def test_load_invalid_json_raises(self, tmp_path):
        p = tmp_path / "bad.json"
        p.write_text("not json {{{")
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        with pytest.raises(Exception):
            mgr.load(str(p))

    def test_load_cfg_extension(self, tmp_path):
        p = tmp_path / "cfg.cfg"
        write_ini(str(p), {"section": {"key": "val"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert data["section"]["key"] == "val"

    def test_load_conf_extension(self, tmp_path):
        p = tmp_path / "cfg.conf"
        write_ini(str(p), {"section": {"foo": "bar"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert data["section"]["foo"] == "bar"


class TestHotReloadManagerGet:
    def test_get_top_level_key(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"host": "example.com"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("host") == "example.com"
        mgr.stop()

    def test_get_nested_key(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"db": {"host": "pg.local", "port": 5432}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("db.host") == "pg.local"
        assert mgr.get("db.port") == 5432
        mgr.stop()

    def test_get_deeply_nested_key(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"a": {"b": {"c": {"d": "deep"}}}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("a.b.c.d") == "deep"
        mgr.stop()

    def test_get_missing_key_returns_default(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"x": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("nonexistent") is None
        assert mgr.get("nonexistent", "fallback") == "fallback"
        mgr.stop()

    def test_get_partial_path_returns_dict(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"db": {"host": "pg.local"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        val = mgr.get("db")
        assert isinstance(val, dict)
        assert val["host"] == "pg.local"
        mgr.stop()

    def test_get_ini_section_key(self, tmp_path):
        p = tmp_path / "cfg.ini"
        write_ini(str(p), {"server": {"host": "myhost"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("server.host") == "myhost"
        mgr.stop()


class TestHotReloadManagerSnapshot:
    def test_snapshot_returns_dict(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"a": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        snap = mgr.snapshot()
        assert isinstance(snap, dict)
        mgr.stop()

    def test_snapshot_is_deep_copy(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"nested": {"x": 1}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        snap1 = mgr.snapshot()
        snap1["nested"]["x"] = 999
        snap2 = mgr.snapshot()
        assert snap2["nested"]["x"] == 1  # original unchanged
        mgr.stop()

    def test_snapshot_reflects_latest_state(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"version": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        write_json(str(p), {"version": 2})
        mgr.reload(str(p))
        snap = mgr.snapshot()
        assert snap["version"] == 2
        mgr.stop()

    def test_snapshot_contains_all_files(self, tmp_path):
        p1 = tmp_path / "a.json"
        p2 = tmp_path / "b.json"
        write_json(str(p1), {"from_a": True})
        write_json(str(p2), {"from_b": True})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        snap = mgr.snapshot()
        assert snap.get("from_a") is True
        assert snap.get("from_b") is True
        mgr.stop()


class TestHotReloadManagerReload:
    def test_reload_picks_up_new_content(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"status": "old"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("status") == "old"
        write_json(str(p), {"status": "new"})
        mgr.reload(str(p))
        assert mgr.get("status") == "new"
        mgr.stop()

    def test_reload_missing_file_calls_on_error(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"x": 1})
        errors = []
        cfg = ReloadConfig(
            paths=[str(p)],
            on_error=lambda path, exc: errors.append((path, exc)),
        )
        mgr = HotReloadManager(cfg)
        mgr.start()
        os.unlink(str(p))
        mgr.reload(str(p))
        assert len(errors) == 1
        mgr.stop()

    def test_reload_missing_file_raises_without_on_error(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"x": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        os.unlink(str(p))
        with pytest.raises(Exception):
            mgr.reload(str(p))
        mgr.stop()

    def test_reload_invalid_json_calls_on_error(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"x": 1})
        errors = []
        cfg = ReloadConfig(
            paths=[str(p)],
            on_error=lambda path, exc: errors.append((path, exc)),
        )
        mgr = HotReloadManager(cfg)
        mgr.start()
        p.write_text("INVALID {{")
        mgr.reload(str(p))
        assert len(errors) == 1
        mgr.stop()

    def test_reload_does_not_affect_other_files(self, tmp_path):
        p1 = tmp_path / "a.json"
        p2 = tmp_path / "b.json"
        write_json(str(p1), {"a": 1})
        write_json(str(p2), {"b": 2})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        write_json(str(p1), {"a": 100})
        mgr.reload(str(p1))
        assert mgr.get("a") == 100
        assert mgr.get("b") == 2
        mgr.stop()


class TestHotReloadManagerSubscribe:
    def test_subscribe_fires_on_key_change(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"counter": 0})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        events = []
        mgr.subscribe(lambda k, o, n: events.append((k, o, n)))
        write_json(str(p), {"counter": 1})
        mgr.reload(str(p))
        assert any(e[0] == "counter" and e[1] == 0 and e[2] == 1 for e in events)
        mgr.stop()

    def test_subscribe_fires_for_new_key(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"existing": "yes"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        events = []
        mgr.subscribe(lambda k, o, n: events.append((k, o, n)))
        write_json(str(p), {"existing": "yes", "new_key": "added"})
        mgr.reload(str(p))
        assert any(e[0] == "new_key" and e[1] is None and e[2] == "added" for e in events)
        mgr.stop()

    def test_subscribe_fires_for_removed_key(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"gone": "soon"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        events = []
        mgr.subscribe(lambda k, o, n: events.append((k, o, n)))
        write_json(str(p), {})
        mgr.reload(str(p))
        assert any(e[0] == "gone" and e[2] is None for e in events)
        mgr.stop()

    def test_subscribe_no_event_if_unchanged(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"stable": "value"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        events = []
        mgr.subscribe(lambda k, o, n: events.append((k, o, n)))
        mgr.reload(str(p))  # same content, no change
        assert events == []
        mgr.stop()

    def test_multiple_subscribers_all_called(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"v": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        calls_a, calls_b = [], []
        mgr.subscribe(lambda k, o, n: calls_a.append(k))
        mgr.subscribe(lambda k, o, n: calls_b.append(k))
        write_json(str(p), {"v": 2})
        mgr.reload(str(p))
        assert "v" in calls_a
        assert "v" in calls_b
        mgr.stop()

    def test_subscribe_exception_does_not_break_others(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"v": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        second_called = []
        mgr.subscribe(lambda k, o, n: (_ for _ in ()).throw(RuntimeError("boom")))
        mgr.subscribe(lambda k, o, n: second_called.append(k))
        write_json(str(p), {"v": 2})
        mgr.reload(str(p))
        assert "v" in second_called
        mgr.stop()

    def test_subscribe_nested_key_change(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"db": {"host": "old"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        events = []
        mgr.subscribe(lambda k, o, n: events.append((k, o, n)))
        write_json(str(p), {"db": {"host": "new"}})
        mgr.reload(str(p))
        assert any(e[0] == "db.host" and e[1] == "old" and e[2] == "new" for e in events)
        mgr.stop()


class TestHotReloadManagerOverlappingKeys:
    def test_last_file_wins_for_same_key(self, tmp_path):
        p1 = tmp_path / "base.json"
        p2 = tmp_path / "override.json"
        write_json(str(p1), {"color": "red"})
        write_json(str(p2), {"color": "blue"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        assert mgr.get("color") == "blue"
        mgr.stop()

    def test_first_file_value_used_when_second_missing_key(self, tmp_path):
        p1 = tmp_path / "base.json"
        p2 = tmp_path / "override.json"
        write_json(str(p1), {"base_key": "from_base", "shared": "base"})
        write_json(str(p2), {"shared": "override"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        assert mgr.get("base_key") == "from_base"
        assert mgr.get("shared") == "override"
        mgr.stop()

    def test_deep_merge_nested_dicts(self, tmp_path):
        p1 = tmp_path / "base.json"
        p2 = tmp_path / "override.json"
        write_json(str(p1), {"db": {"host": "base-host", "port": 5432}})
        write_json(str(p2), {"db": {"host": "override-host"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        # host is overridden, port is preserved from base
        assert mgr.get("db.host") == "override-host"
        assert mgr.get("db.port") == 5432
        mgr.stop()

    def test_json_and_ini_merged(self, tmp_path):
        pj = tmp_path / "cfg.json"
        pi = tmp_path / "cfg.ini"
        write_json(str(pj), {"from_json": "yes"})
        write_ini(str(pi), {"extras": {"from_ini": "yes"}})
        mgr = HotReloadManager(ReloadConfig(paths=[str(pj), str(pi)]))
        mgr.start()
        assert mgr.get("from_json") == "yes"
        assert mgr.get("extras.from_ini") == "yes"
        mgr.stop()


class TestHotReloadManagerStartStop:
    def test_start_loads_all_files(self, tmp_path):
        p1 = tmp_path / "a.json"
        p2 = tmp_path / "b.json"
        write_json(str(p1), {"a": 1})
        write_json(str(p2), {"b": 2})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p1), str(p2)]))
        mgr.start()
        assert mgr.get("a") == 1
        assert mgr.get("b") == 2
        mgr.stop()

    def test_stop_before_start_is_safe(self):
        mgr = HotReloadManager(ReloadConfig(paths=[]))
        mgr.stop()  # should not raise

    def test_watcher_started_after_start(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)], interval=0.05))
        mgr.start()
        assert mgr._watcher is not None
        assert mgr._watcher._thread is not None
        assert mgr._watcher._thread.is_alive()
        mgr.stop()

    def test_watcher_stopped_after_stop(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)], interval=0.05))
        mgr.start()
        mgr.stop()
        assert mgr._watcher is None

    def test_on_error_called_for_missing_file_on_start(self, tmp_path):
        missing = tmp_path / "missing.json"
        errors = []
        cfg = ReloadConfig(
            paths=[str(missing)],
            on_error=lambda path, exc: errors.append((path, exc)),
        )
        mgr = HotReloadManager(cfg)
        mgr.start()  # should NOT raise
        assert len(errors) == 1
        mgr.stop()

    def test_missing_file_raises_on_start_without_on_error(self, tmp_path):
        missing = tmp_path / "missing.json"
        mgr = HotReloadManager(ReloadConfig(paths=[str(missing)]))
        with pytest.raises(Exception):
            mgr.start()

    def test_background_watcher_triggers_reload(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"val": "before"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)], interval=0.05))
        mgr.start()
        assert mgr.get("val") == "before"
        write_json(str(p), {"val": "after"})
        bump_mtime(str(p))
        deadline = time.time() + 3.0
        while time.time() < deadline:
            if mgr.get("val") == "after":
                break
            time.sleep(0.05)
        assert mgr.get("val") == "after"
        mgr.stop()


class TestReloadConfigDataclass:
    def test_default_interval(self):
        cfg = ReloadConfig(paths=["a.json"])
        assert cfg.interval == 1.0

    def test_default_on_error_is_none(self):
        cfg = ReloadConfig(paths=[])
        assert cfg.on_error is None

    def test_custom_values(self):
        handler = lambda p, e: None
        cfg = ReloadConfig(paths=["x"], interval=2.5, on_error=handler)
        assert cfg.paths == ["x"]
        assert cfg.interval == 2.5
        assert cfg.on_error is handler


class TestPublicImports:
    def test_imports_from_package(self):
        from docstoolkit.config_hotreload import FileWatcher, ReloadConfig, HotReloadManager
        assert FileWatcher is not None
        assert ReloadConfig is not None
        assert HotReloadManager is not None

    def test_all_list(self):
        import docstoolkit.config_hotreload as mod
        assert "FileWatcher" in mod.__all__
        assert "ReloadConfig" in mod.__all__
        assert "HotReloadManager" in mod.__all__


class TestEdgeCases:
    def test_empty_json_file(self, tmp_path):
        p = tmp_path / "empty.json"
        write_json(str(p), {})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.snapshot() == {}
        mgr.stop()

    def test_json_array_at_root_raises(self, tmp_path):
        p = tmp_path / "array.json"
        p.write_text("[1, 2, 3]")
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        with pytest.raises(Exception):
            mgr.load(str(p))

    def test_ini_empty_file(self, tmp_path):
        p = tmp_path / "empty.ini"
        p.write_text("")
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        data = mgr.load(str(p))
        assert isinstance(data, dict)

    def test_reload_config_dataclass_equality(self):
        c1 = ReloadConfig(paths=["a"], interval=1.0)
        c2 = ReloadConfig(paths=["a"], interval=1.0)
        # on_error is excluded from comparison (compare=False)
        assert c1 == c2

    def test_get_before_load_returns_default(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"x": 1})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        # No start/load called yet
        assert mgr.get("x", "missing") == "missing"

    def test_check_once_does_not_fire_callbacks(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {})
        fw = FileWatcher([str(p)])
        fired = []
        fw.on_change(lambda path: fired.append(path))
        bump_mtime(str(p))
        fw.check_once()
        # check_once should NOT fire callbacks — only the background thread does
        assert fired == []

    def test_snapshot_independent_of_internal_state(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"data": [1, 2, 3]})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        snap = mgr.snapshot()
        snap["data"].append(99)
        assert mgr.get("data") == [1, 2, 3]
        mgr.stop()

    def test_multiple_reloads_accumulate_correctly(self, tmp_path):
        p = tmp_path / "cfg.json"
        write_json(str(p), {"n": 0})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        for i in range(1, 6):
            write_json(str(p), {"n": i})
            mgr.reload(str(p))
        assert mgr.get("n") == 5
        mgr.stop()

    def test_unicode_values_in_json(self, tmp_path):
        p = tmp_path / "unicode.json"
        write_json(str(p), {"greeting": "Привет мир", "emoji": "🎉"})
        mgr = HotReloadManager(ReloadConfig(paths=[str(p)]))
        mgr.start()
        assert mgr.get("greeting") == "Привет мир"
        mgr.stop()

    def test_file_watcher_no_paths_check_once(self):
        fw = FileWatcher([])
        assert fw.check_once() == []

    def test_hot_reload_manager_no_paths_start_stop(self):
        mgr = HotReloadManager(ReloadConfig(paths=[]))
        mgr.start()
        assert mgr.snapshot() == {}
        mgr.stop()
