"""Tests for docstoolkit.file_watcher_sim (E146)."""

from __future__ import annotations

import hashlib
import threading

import pytest

from docstoolkit.file_watcher_sim import (
    ChangeKind,
    FileChange,
    FileWatcherSim,
    WatchSnapshot,
)


def _h(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------------------
# ChangeKind
# ---------------------------------------------------------------------------


class TestChangeKind:
    def test_added_value(self) -> None:
        assert ChangeKind.ADDED.value == "ADDED"

    def test_modified_value(self) -> None:
        assert ChangeKind.MODIFIED.value == "MODIFIED"

    def test_removed_value(self) -> None:
        assert ChangeKind.REMOVED.value == "REMOVED"

    def test_unchanged_value(self) -> None:
        assert ChangeKind.UNCHANGED.value == "UNCHANGED"

    def test_members_count(self) -> None:
        assert len(list(ChangeKind)) == 4


# ---------------------------------------------------------------------------
# FileChange
# ---------------------------------------------------------------------------


class TestFileChange:
    def test_construct(self) -> None:
        c = FileChange(
            path="a.md",
            kind=ChangeKind.ADDED,
            old_hash=None,
            new_hash="abc",
            timestamp=1.0,
        )
        assert c.path == "a.md"
        assert c.kind == ChangeKind.ADDED
        assert c.old_hash is None
        assert c.new_hash == "abc"
        assert c.timestamp == 1.0

    def test_equality(self) -> None:
        a = FileChange("p", ChangeKind.MODIFIED, "x", "y", 2.0)
        b = FileChange("p", ChangeKind.MODIFIED, "x", "y", 2.0)
        assert a == b

    def test_inequality(self) -> None:
        a = FileChange("p", ChangeKind.MODIFIED, "x", "y", 2.0)
        b = FileChange("p", ChangeKind.MODIFIED, "x", "z", 2.0)
        assert a != b


# ---------------------------------------------------------------------------
# WatchSnapshot
# ---------------------------------------------------------------------------


class TestWatchSnapshot:
    def test_default_empty(self) -> None:
        s = WatchSnapshot()
        assert s.files == {}
        assert s.timestamp == 0.0
        assert s.file_count == 0

    def test_file_count_nonzero(self) -> None:
        s = WatchSnapshot(files={"a": "h1", "b": "h2"}, timestamp=5.0)
        assert s.file_count == 2
        assert s.timestamp == 5.0

    def test_file_count_large(self) -> None:
        files = {f"f{i}.md": f"h{i}" for i in range(100)}
        s = WatchSnapshot(files=files, timestamp=1.0)
        assert s.file_count == 100


# ---------------------------------------------------------------------------
# register
# ---------------------------------------------------------------------------


class TestRegister:
    def test_register_adds_file(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "hello", now=1.0)
        assert "a.md" in w.tracked_paths
        assert w.file_count == 1

    def test_register_stores_hash(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "hello", now=1.0)
        snap = w.snapshot()
        assert snap.files["a.md"] == _h("hello")

    def test_register_does_not_emit_event(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "hello", now=1.0)
        assert w.changes_since(0.0) == []

    def test_register_does_not_fire_subscribers(self) -> None:
        w = FileWatcherSim()
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.register("a.md", "x", now=1.0)
        assert received == []

    def test_register_overwrite(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        w.register("a.md", "v2", now=2.0)
        assert w.snapshot().files["a.md"] == _h("v2")


# ---------------------------------------------------------------------------
# register_batch
# ---------------------------------------------------------------------------


class TestRegisterBatch:
    def test_register_multiple(self) -> None:
        w = FileWatcherSim()
        w.register_batch({"a": "1", "b": "2", "c": "3"}, now=1.0)
        assert w.file_count == 3
        assert set(w.tracked_paths) == {"a", "b", "c"}

    def test_register_batch_empty(self) -> None:
        w = FileWatcherSim()
        w.register_batch({}, now=1.0)
        assert w.file_count == 0

    def test_register_batch_hashes(self) -> None:
        w = FileWatcherSim()
        w.register_batch({"a": "alpha", "b": "beta"}, now=1.0)
        snap = w.snapshot()
        assert snap.files["a"] == _h("alpha")
        assert snap.files["b"] == _h("beta")

    def test_register_batch_no_events(self) -> None:
        w = FileWatcherSim()
        w.register_batch({"a": "1", "b": "2"}, now=1.0)
        assert w.changes_since(0.0) == []


# ---------------------------------------------------------------------------
# update — MODIFIED
# ---------------------------------------------------------------------------


class TestUpdate:
    def test_modified_kind(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v2", now=2.0)
        assert change.kind == ChangeKind.MODIFIED

    def test_modified_hashes(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v2", now=2.0)
        assert change.old_hash == _h("v1")
        assert change.new_hash == _h("v2")

    def test_modified_path(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v2", now=2.0)
        assert change.path == "a.md"

    def test_modified_timestamp(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v2", now=42.5)
        assert change.timestamp == 42.5

    def test_modified_updates_state(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        w.update("a.md", "v2", now=2.0)
        snap = w.snapshot()
        assert snap.files["a.md"] == _h("v2")


# ---------------------------------------------------------------------------
# update — UNCHANGED
# ---------------------------------------------------------------------------


class TestUpdateNoChange:
    def test_unchanged_kind(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v1", now=2.0)
        assert change.kind == ChangeKind.UNCHANGED

    def test_unchanged_same_hash(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.update("a.md", "v1", now=2.0)
        assert change.old_hash == change.new_hash == _h("v1")

    def test_unchanged_no_subscriber_fire(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.update("a.md", "v1", now=2.0)
        assert received == []


# ---------------------------------------------------------------------------
# update — ADDED (when not registered)
# ---------------------------------------------------------------------------


class TestUpdateNewFile:
    def test_added_kind(self) -> None:
        w = FileWatcherSim()
        change = w.update("new.md", "content", now=1.0)
        assert change.kind == ChangeKind.ADDED

    def test_added_old_hash_none(self) -> None:
        w = FileWatcherSim()
        change = w.update("new.md", "content", now=1.0)
        assert change.old_hash is None
        assert change.new_hash == _h("content")

    def test_added_tracked(self) -> None:
        w = FileWatcherSim()
        w.update("new.md", "content", now=1.0)
        assert "new.md" in w.tracked_paths

    def test_added_fires_subscriber(self) -> None:
        w = FileWatcherSim()
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.update("new.md", "content", now=1.0)
        assert len(received) == 1
        assert received[0].kind == ChangeKind.ADDED


# ---------------------------------------------------------------------------
# remove
# ---------------------------------------------------------------------------


class TestRemove:
    def test_remove_returns_change(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.remove("a.md", now=2.0)
        assert change is not None
        assert change.kind == ChangeKind.REMOVED

    def test_remove_hashes(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.remove("a.md", now=2.0)
        assert change.old_hash == _h("v1")
        assert change.new_hash is None

    def test_remove_path(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.remove("a.md", now=2.0)
        assert change.path == "a.md"

    def test_remove_timestamp(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        change = w.remove("a.md", now=7.0)
        assert change.timestamp == 7.0

    def test_remove_untracks(self) -> None:
        w = FileWatcherSim()
        w.register("a.md", "v1", now=1.0)
        w.remove("a.md", now=2.0)
        assert "a.md" not in w.tracked_paths
        assert w.file_count == 0


# ---------------------------------------------------------------------------
# remove — non-existent
# ---------------------------------------------------------------------------


class TestRemoveNonExistent:
    def test_returns_none(self) -> None:
        w = FileWatcherSim()
        assert w.remove("missing.md", now=1.0) is None

    def test_no_event_logged(self) -> None:
        w = FileWatcherSim()
        w.remove("missing.md", now=1.0)
        assert w.changes_since(0.0) == []

    def test_no_subscriber_fire(self) -> None:
        w = FileWatcherSim()
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.remove("missing.md", now=1.0)
        assert received == []


# ---------------------------------------------------------------------------
# snapshot
# ---------------------------------------------------------------------------


class TestSnapshot:
    def test_empty(self) -> None:
        w = FileWatcherSim()
        snap = w.snapshot()
        assert snap.file_count == 0
        assert snap.files == {}

    def test_after_register(self) -> None:
        w = FileWatcherSim()
        w.register("a", "x", now=1.0)
        w.register("b", "y", now=2.0)
        snap = w.snapshot()
        assert snap.file_count == 2
        assert snap.files["a"] == _h("x")
        assert snap.files["b"] == _h("y")

    def test_snapshot_is_independent(self) -> None:
        w = FileWatcherSim()
        w.register("a", "x", now=1.0)
        snap = w.snapshot()
        w.update("a", "y", now=2.0)
        # The original snapshot must not change.
        assert snap.files["a"] == _h("x")

    def test_snapshot_timestamp(self) -> None:
        w = FileWatcherSim()
        w.register("a", "x", now=1.0)
        w.register("b", "y", now=5.0)
        snap = w.snapshot()
        assert snap.timestamp == 5.0


# ---------------------------------------------------------------------------
# diff
# ---------------------------------------------------------------------------


class TestDiff:
    def test_no_changes(self) -> None:
        w = FileWatcherSim()
        w.register("a", "1", now=1.0)
        s1 = w.snapshot()
        s2 = w.snapshot()
        assert w.diff(s1, s2) == []

    def test_added(self) -> None:
        w = FileWatcherSim()
        s1 = w.snapshot()
        w.register("a", "1", now=1.0)
        s2 = w.snapshot()
        d = w.diff(s1, s2)
        assert len(d) == 1
        assert d[0].kind == ChangeKind.ADDED
        assert d[0].path == "a"
        assert d[0].new_hash == _h("1")
        assert d[0].old_hash is None

    def test_removed(self) -> None:
        w = FileWatcherSim()
        w.register("a", "1", now=1.0)
        s1 = w.snapshot()
        w.remove("a", now=2.0)
        s2 = w.snapshot()
        d = w.diff(s1, s2)
        assert len(d) == 1
        assert d[0].kind == ChangeKind.REMOVED
        assert d[0].path == "a"
        assert d[0].old_hash == _h("1")
        assert d[0].new_hash is None

    def test_modified(self) -> None:
        w = FileWatcherSim()
        w.register("a", "1", now=1.0)
        s1 = w.snapshot()
        w.update("a", "2", now=2.0)
        s2 = w.snapshot()
        d = w.diff(s1, s2)
        assert len(d) == 1
        assert d[0].kind == ChangeKind.MODIFIED
        assert d[0].old_hash == _h("1")
        assert d[0].new_hash == _h("2")

    def test_mixed(self) -> None:
        w = FileWatcherSim()
        w.register_batch({"keep": "k", "mod": "old", "gone": "g"}, now=1.0)
        s1 = w.snapshot()
        w.update("mod", "new", now=2.0)
        w.remove("gone", now=2.0)
        w.update("added", "a", now=2.0)
        s2 = w.snapshot()
        d = w.diff(s1, s2)
        kinds = {c.path: c.kind for c in d}
        assert kinds == {
            "added": ChangeKind.ADDED,
            "mod": ChangeKind.MODIFIED,
            "gone": ChangeKind.REMOVED,
        }


# ---------------------------------------------------------------------------
# changes_since
# ---------------------------------------------------------------------------


class TestChangesSince:
    def test_empty(self) -> None:
        w = FileWatcherSim()
        assert w.changes_since(0.0) == []

    def test_filters_by_timestamp(self) -> None:
        w = FileWatcherSim()
        w.update("a", "1", now=1.0)
        w.update("a", "2", now=2.0)
        w.update("a", "3", now=3.0)
        results = w.changes_since(1.5)
        assert [c.timestamp for c in results] == [2.0, 3.0]

    def test_zero_returns_all(self) -> None:
        w = FileWatcherSim()
        w.update("a", "1", now=1.0)
        w.update("b", "2", now=2.0)
        assert len(w.changes_since(0.0)) == 2

    def test_future_returns_none(self) -> None:
        w = FileWatcherSim()
        w.update("a", "1", now=1.0)
        assert w.changes_since(100.0) == []

    def test_includes_unchanged(self) -> None:
        w = FileWatcherSim()
        w.register("a", "v", now=1.0)
        w.update("a", "v", now=2.0)
        events = w.changes_since(0.0)
        assert len(events) == 1
        assert events[0].kind == ChangeKind.UNCHANGED


# ---------------------------------------------------------------------------
# subscribe
# ---------------------------------------------------------------------------


class TestSubscribe:
    def test_returns_int_id(self) -> None:
        w = FileWatcherSim()
        sub_id = w.subscribe(lambda c: None)
        assert isinstance(sub_id, int)

    def test_unique_ids(self) -> None:
        w = FileWatcherSim()
        a = w.subscribe(lambda c: None)
        b = w.subscribe(lambda c: None)
        assert a != b

    def test_callback_fires_on_update(self) -> None:
        w = FileWatcherSim()
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.update("a", "1", now=1.0)
        assert len(received) == 1
        assert received[0].path == "a"
        assert received[0].kind == ChangeKind.ADDED

    def test_callback_fires_on_modify(self) -> None:
        w = FileWatcherSim()
        w.register("a", "v1", now=1.0)
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.update("a", "v2", now=2.0)
        assert len(received) == 1
        assert received[0].kind == ChangeKind.MODIFIED

    def test_callback_fires_on_remove(self) -> None:
        w = FileWatcherSim()
        w.register("a", "v1", now=1.0)
        received: list[FileChange] = []
        w.subscribe(received.append)
        w.remove("a", now=2.0)
        assert len(received) == 1
        assert received[0].kind == ChangeKind.REMOVED


# ---------------------------------------------------------------------------
# unsubscribe
# ---------------------------------------------------------------------------


class TestUnsubscribe:
    def test_returns_true_when_removed(self) -> None:
        w = FileWatcherSim()
        sub_id = w.subscribe(lambda c: None)
        assert w.unsubscribe(sub_id) is True

    def test_returns_false_for_unknown(self) -> None:
        w = FileWatcherSim()
        assert w.unsubscribe(9999) is False

    def test_stops_receiving(self) -> None:
        w = FileWatcherSim()
        received: list[FileChange] = []
        sub_id = w.subscribe(received.append)
        w.unsubscribe(sub_id)
        w.update("a", "1", now=1.0)
        assert received == []

    def test_double_unsubscribe(self) -> None:
        w = FileWatcherSim()
        sub_id = w.subscribe(lambda c: None)
        assert w.unsubscribe(sub_id) is True
        assert w.unsubscribe(sub_id) is False


# ---------------------------------------------------------------------------
# multiple subscribers
# ---------------------------------------------------------------------------


class TestMultipleSubscribers:
    def test_all_receive(self) -> None:
        w = FileWatcherSim()
        a: list[FileChange] = []
        b: list[FileChange] = []
        w.subscribe(a.append)
        w.subscribe(b.append)
        w.update("p", "x", now=1.0)
        assert len(a) == 1
        assert len(b) == 1

    def test_one_unsubscribed_other_remains(self) -> None:
        w = FileWatcherSim()
        a: list[FileChange] = []
        b: list[FileChange] = []
        sa = w.subscribe(a.append)
        w.subscribe(b.append)
        w.unsubscribe(sa)
        w.update("p", "x", now=1.0)
        assert a == []
        assert len(b) == 1

    def test_thread_safe_subscribers(self) -> None:
        w = FileWatcherSim()
        counter = {"n": 0}
        lock = threading.Lock()

        def cb(_c: FileChange) -> None:
            with lock:
                counter["n"] += 1

        w.subscribe(cb)

        def worker(i: int) -> None:
            w.update(f"p{i}", str(i), now=float(i))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert counter["n"] == 20


# ---------------------------------------------------------------------------
# edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_state_snapshot(self) -> None:
        w = FileWatcherSim()
        s = w.snapshot()
        assert s.file_count == 0
        assert s.timestamp == 0.0

    def test_empty_state_tracked_paths(self) -> None:
        w = FileWatcherSim()
        assert w.tracked_paths == []

    def test_register_same_path_twice(self) -> None:
        w = FileWatcherSim()
        w.register("a", "v1", now=1.0)
        w.register("a", "v2", now=2.0)
        assert w.file_count == 1
        assert w.snapshot().files["a"] == _h("v2")

    def test_register_same_path_twice_no_event(self) -> None:
        w = FileWatcherSim()
        w.register("a", "v1", now=1.0)
        w.register("a", "v2", now=2.0)
        assert w.changes_since(0.0) == []

    def test_diff_with_empty_snapshots(self) -> None:
        w = FileWatcherSim()
        s1 = WatchSnapshot()
        s2 = WatchSnapshot()
        assert w.diff(s1, s2) == []

    def test_empty_content_hash(self) -> None:
        w = FileWatcherSim()
        change = w.update("a", "", now=1.0)
        assert change.new_hash == _h("")
        assert change.kind == ChangeKind.ADDED

    def test_unicode_content(self) -> None:
        w = FileWatcherSim()
        content = "Привет мир \U0001f600"
        change = w.update("a", content, now=1.0)
        assert change.new_hash == _h(content)

    def test_diff_order_added_modified_removed(self) -> None:
        w = FileWatcherSim()
        w.register_batch({"m": "old", "r": "x"}, now=1.0)
        s1 = w.snapshot()
        w.update("m", "new", now=2.0)
        w.remove("r", now=2.0)
        w.update("a", "v", now=2.0)
        s2 = w.snapshot()
        d = w.diff(s1, s2)
        kinds = [c.kind for c in d]
        # ADDED first, then MODIFIED, then REMOVED.
        assert kinds.index(ChangeKind.ADDED) < kinds.index(ChangeKind.MODIFIED)
        assert kinds.index(ChangeKind.MODIFIED) < kinds.index(ChangeKind.REMOVED)

    def test_subscriber_callback_called_after_state_updated(self) -> None:
        """When subscriber fires, state should already reflect the change."""
        w = FileWatcherSim()
        observed: list[int] = []

        def cb(change: FileChange) -> None:
            observed.append(w.file_count)

        w.subscribe(cb)
        w.update("a", "1", now=1.0)
        w.update("b", "2", now=2.0)
        assert observed == [1, 2]
