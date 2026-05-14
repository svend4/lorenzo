"""Tests for E361 DocReplayLog."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_replay_log import (
    Checkpoint,
    DocReplayLog,
    ReplayEvent,
    ReplayStats,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestReplayEventDataclass:
    def test_construct_with_required_fields(self):
        ev = ReplayEvent(event_id=1, stream_id="s1", event_type="created")
        assert ev.event_id == 1
        assert ev.stream_id == "s1"
        assert ev.event_type == "created"

    def test_default_payload_is_empty_dict(self):
        ev = ReplayEvent(event_id=1, stream_id="s", event_type="t")
        assert ev.payload == {}

    def test_default_recorded_at_is_zero(self):
        ev = ReplayEvent(event_id=1, stream_id="s", event_type="t")
        assert ev.recorded_at == 0.0

    def test_payload_is_independent_per_instance(self):
        a = ReplayEvent(event_id=1, stream_id="s", event_type="t")
        b = ReplayEvent(event_id=2, stream_id="s", event_type="t")
        a.payload["k"] = "v"
        assert b.payload == {}

    def test_explicit_payload_kept(self):
        ev = ReplayEvent(
            event_id=5, stream_id="x", event_type="y", payload={"a": 1}, recorded_at=12.5
        )
        assert ev.payload == {"a": 1}
        assert ev.recorded_at == 12.5


class TestCheckpointDataclass:
    def test_construct(self):
        cp = Checkpoint(name="v1", event_id=10)
        assert cp.name == "v1"
        assert cp.event_id == 10
        assert cp.created_at == 0.0

    def test_with_created_at(self):
        cp = Checkpoint(name="x", event_id=0, created_at=99.0)
        assert cp.created_at == 99.0

    def test_equality(self):
        a = Checkpoint(name="v1", event_id=5, created_at=1.0)
        b = Checkpoint(name="v1", event_id=5, created_at=1.0)
        assert a == b


class TestReplayStatsDataclass:
    def test_construct(self):
        s = ReplayStats(
            total_events=3,
            unique_streams=2,
            unique_event_types=2,
            checkpoint_count=1,
        )
        assert s.total_events == 3
        assert s.unique_streams == 2
        assert s.unique_event_types == 2
        assert s.checkpoint_count == 1


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_default_empty(self):
        log = DocReplayLog()
        assert log.stats().total_events == 0

    def test_no_checkpoints_initially(self):
        log = DocReplayLog()
        assert log.list_checkpoints() == []

    def test_independent_instances(self):
        a = DocReplayLog()
        b = DocReplayLog()
        a.append("s", "t")
        assert b.stats().total_events == 0


# ---------------------------------------------------------------------------
# Append
# ---------------------------------------------------------------------------
class TestAppend:
    def test_append_returns_event(self):
        log = DocReplayLog()
        ev = log.append("s1", "created")
        assert isinstance(ev, ReplayEvent)
        assert ev.event_id == 1

    def test_append_increments_id(self):
        log = DocReplayLog()
        a = log.append("s", "t")
        b = log.append("s", "t")
        c = log.append("s", "t")
        assert (a.event_id, b.event_id, c.event_id) == (1, 2, 3)

    def test_append_with_payload(self):
        log = DocReplayLog()
        ev = log.append("s", "t", payload={"k": "v"})
        assert ev.payload == {"k": "v"}

    def test_append_default_payload_empty(self):
        log = DocReplayLog()
        ev = log.append("s", "t")
        assert ev.payload == {}

    def test_append_with_explicit_now(self):
        log = DocReplayLog()
        ev = log.append("s", "t", now=123.5)
        assert ev.recorded_at == 123.5

    def test_payload_is_copied(self):
        log = DocReplayLog()
        p = {"k": "v"}
        ev = log.append("s", "t", payload=p)
        p["new"] = 1
        assert "new" not in ev.payload

    def test_empty_stream_id_rejected(self):
        log = DocReplayLog()
        with pytest.raises(ValueError):
            log.append("", "t")

    def test_empty_event_type_rejected(self):
        log = DocReplayLog()
        with pytest.raises(ValueError):
            log.append("s", "")

    def test_non_dict_payload_rejected(self):
        log = DocReplayLog()
        with pytest.raises(TypeError):
            log.append("s", "t", payload="not-a-dict")  # type: ignore[arg-type]

    def test_recorded_at_auto(self):
        log = DocReplayLog()
        ev = log.append("s", "t")
        assert ev.recorded_at > 0


# ---------------------------------------------------------------------------
# get_event
# ---------------------------------------------------------------------------
class TestGetEvent:
    def test_get_existing(self):
        log = DocReplayLog()
        log.append("s", "t")
        ev2 = log.append("s", "t")
        got = log.get_event(2)
        assert got is not None
        assert got.event_id == ev2.event_id

    def test_get_missing(self):
        log = DocReplayLog()
        assert log.get_event(99) is None

    def test_get_after_truncate(self):
        log = DocReplayLog()
        log.append("s", "t")
        log.append("s", "t")
        log.truncate_before(2)
        assert log.get_event(1) is None
        assert log.get_event(2) is not None


# ---------------------------------------------------------------------------
# replay_stream
# ---------------------------------------------------------------------------
class TestReplayStream:
    def test_empty_stream(self):
        log = DocReplayLog()
        assert log.replay_stream("missing") == []

    def test_basic_replay(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "b")
        log.append("s1", "c")
        evs = log.replay_stream("s1")
        assert [e.event_type for e in evs] == ["a", "c"]

    def test_from_event_id(self):
        log = DocReplayLog()
        log.append("s1", "a")  # id=1
        log.append("s1", "b")  # id=2
        log.append("s1", "c")  # id=3
        evs = log.replay_stream("s1", from_event_id=2)
        assert [e.event_id for e in evs] == [2, 3]

    def test_limit(self):
        log = DocReplayLog()
        for i in range(5):
            log.append("s", f"t{i}")
        evs = log.replay_stream("s", limit=3)
        assert len(evs) == 3
        assert [e.event_id for e in evs] == [1, 2, 3]

    def test_sorted_ascending(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.append("s", "c")
        evs = log.replay_stream("s")
        ids = [e.event_id for e in evs]
        assert ids == sorted(ids)

    def test_filters_other_streams(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "b")
        log.append("s1", "c")
        log.append("s2", "d")
        evs = log.replay_stream("s2")
        assert [e.event_type for e in evs] == ["b", "d"]


# ---------------------------------------------------------------------------
# replay_all
# ---------------------------------------------------------------------------
class TestReplayAll:
    def test_empty(self):
        log = DocReplayLog()
        assert log.replay_all() == []

    def test_returns_all(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "b")
        log.append("s1", "c")
        assert len(log.replay_all()) == 3

    def test_from_event_id(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.append("s", "c")
        evs = log.replay_all(from_event_id=2)
        assert [e.event_id for e in evs] == [2, 3]

    def test_limit(self):
        log = DocReplayLog()
        for _ in range(10):
            log.append("s", "t")
        assert len(log.replay_all(limit=4)) == 4

    def test_sorted_asc(self):
        log = DocReplayLog()
        log.append("s2", "a")
        log.append("s1", "b")
        log.append("s3", "c")
        ids = [e.event_id for e in log.replay_all()]
        assert ids == sorted(ids)


# ---------------------------------------------------------------------------
# replay_to
# ---------------------------------------------------------------------------
class TestReplayTo:
    def test_callback_invoked_per_event(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        seen = []
        n = log.replay_to(seen.append)
        assert n == 2
        assert [e.event_type for e in seen] == ["a", "b"]

    def test_callback_with_stream_filter(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "b")
        log.append("s1", "c")
        seen = []
        n = log.replay_to(seen.append, stream_id="s1")
        assert n == 2
        assert all(e.stream_id == "s1" for e in seen)

    def test_from_event_id(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.append("s", "c")
        seen = []
        n = log.replay_to(seen.append, from_event_id=2)
        assert n == 2
        assert [e.event_id for e in seen] == [2, 3]

    def test_until_event_id(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.append("s", "c")
        seen = []
        n = log.replay_to(seen.append, until_event_id=2)
        assert n == 2
        assert [e.event_id for e in seen] == [1, 2]

    def test_non_callable_rejected(self):
        log = DocReplayLog()
        with pytest.raises(TypeError):
            log.replay_to(None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# create_checkpoint
# ---------------------------------------------------------------------------
class TestCreateCheckpoint:
    def test_creates_at_last_event_id(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        cp = log.create_checkpoint("v1")
        assert cp.event_id == 2

    def test_zero_when_empty(self):
        log = DocReplayLog()
        cp = log.create_checkpoint("empty")
        assert cp.event_id == 0

    def test_with_explicit_now(self):
        log = DocReplayLog()
        cp = log.create_checkpoint("v", now=42.0)
        assert cp.created_at == 42.0

    def test_overwrites_existing_with_same_name(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.create_checkpoint("v")
        log.append("s", "b")
        cp = log.create_checkpoint("v")
        assert cp.event_id == 2

    def test_empty_name_rejected(self):
        log = DocReplayLog()
        with pytest.raises(ValueError):
            log.create_checkpoint("")


# ---------------------------------------------------------------------------
# get_checkpoint
# ---------------------------------------------------------------------------
class TestGetCheckpoint:
    def test_get_existing(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.create_checkpoint("v1")
        cp = log.get_checkpoint("v1")
        assert cp is not None
        assert cp.name == "v1"

    def test_get_missing(self):
        log = DocReplayLog()
        assert log.get_checkpoint("missing") is None


# ---------------------------------------------------------------------------
# delete_checkpoint
# ---------------------------------------------------------------------------
class TestDeleteCheckpoint:
    def test_delete_existing_returns_true(self):
        log = DocReplayLog()
        log.create_checkpoint("v")
        assert log.delete_checkpoint("v") is True

    def test_delete_missing_returns_false(self):
        log = DocReplayLog()
        assert log.delete_checkpoint("missing") is False

    def test_delete_actually_removes(self):
        log = DocReplayLog()
        log.create_checkpoint("v")
        log.delete_checkpoint("v")
        assert log.get_checkpoint("v") is None


# ---------------------------------------------------------------------------
# replay_from_checkpoint
# ---------------------------------------------------------------------------
class TestReplayFromCheckpoint:
    def test_replays_after_checkpoint(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.create_checkpoint("snap")
        log.append("s", "c")
        log.append("s", "d")
        seen = []
        n = log.replay_from_checkpoint("snap", seen.append)
        assert n == 2
        assert [e.event_type for e in seen] == ["c", "d"]

    def test_returns_zero_when_no_new_events(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.create_checkpoint("snap")
        seen = []
        n = log.replay_from_checkpoint("snap", seen.append)
        assert n == 0
        assert seen == []

    def test_unknown_checkpoint_raises(self):
        log = DocReplayLog()
        with pytest.raises(KeyError):
            log.replay_from_checkpoint("nope", lambda e: None)

    def test_non_callable_rejected(self):
        log = DocReplayLog()
        log.create_checkpoint("v")
        with pytest.raises(TypeError):
            log.replay_from_checkpoint("v", None)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# list_checkpoints
# ---------------------------------------------------------------------------
class TestListCheckpoints:
    def test_empty(self):
        log = DocReplayLog()
        assert log.list_checkpoints() == []

    def test_sorted_by_event_id_desc(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.create_checkpoint("c1")  # id=1
        log.append("s", "b")
        log.create_checkpoint("c2")  # id=2
        log.append("s", "c")
        log.create_checkpoint("c3")  # id=3
        order = [c.name for c in log.list_checkpoints()]
        assert order == ["c3", "c2", "c1"]

    def test_returns_all(self):
        log = DocReplayLog()
        log.create_checkpoint("a")
        log.create_checkpoint("b")
        assert len(log.list_checkpoints()) == 2


# ---------------------------------------------------------------------------
# events_by_type
# ---------------------------------------------------------------------------
class TestEventsByType:
    def test_filters_by_type(self):
        log = DocReplayLog()
        log.append("s", "created")
        log.append("s", "updated")
        log.append("s", "created")
        evs = log.events_by_type("created")
        assert len(evs) == 2
        assert all(e.event_type == "created" for e in evs)

    def test_missing_type_empty(self):
        log = DocReplayLog()
        log.append("s", "t")
        assert log.events_by_type("missing") == []

    def test_sorted_by_event_id(self):
        log = DocReplayLog()
        log.append("s", "t")
        log.append("s", "t")
        log.append("s", "t")
        ids = [e.event_id for e in log.events_by_type("t")]
        assert ids == sorted(ids)

    def test_limit_applied(self):
        log = DocReplayLog()
        for _ in range(5):
            log.append("s", "t")
        assert len(log.events_by_type("t", limit=2)) == 2


# ---------------------------------------------------------------------------
# truncate_before
# ---------------------------------------------------------------------------
class TestTruncateBefore:
    def test_removes_lower_ids(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        log.append("s", "c")
        removed = log.truncate_before(3)
        assert removed == 2
        assert log.stats().total_events == 1

    def test_truncate_zero_removes_nothing(self):
        log = DocReplayLog()
        log.append("s", "a")
        assert log.truncate_before(0) == 0

    def test_truncate_high_removes_all(self):
        log = DocReplayLog()
        log.append("s", "a")
        log.append("s", "b")
        removed = log.truncate_before(1000)
        assert removed == 2
        assert log.stats().total_events == 0

    def test_rebuilds_stream_index(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "b")
        log.append("s1", "c")
        log.truncate_before(3)
        # only event id=3 (stream s1) should remain reachable
        assert [e.event_type for e in log.replay_stream("s1")] == ["c"]
        assert log.replay_stream("s2") == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_stats(self):
        log = DocReplayLog()
        s = log.stats()
        assert s.total_events == 0
        assert s.unique_streams == 0
        assert s.unique_event_types == 0
        assert s.checkpoint_count == 0

    def test_after_appends(self):
        log = DocReplayLog()
        log.append("s1", "a")
        log.append("s2", "a")
        log.append("s1", "b")
        s = log.stats()
        assert s.total_events == 3
        assert s.unique_streams == 2
        assert s.unique_event_types == 2

    def test_checkpoint_count(self):
        log = DocReplayLog()
        log.create_checkpoint("a")
        log.create_checkpoint("b")
        assert log.stats().checkpoint_count == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_appends_yield_unique_ids(self):
        log = DocReplayLog()
        n_threads = 8
        per_thread = 50

        def worker():
            for _ in range(per_thread):
                log.append("s", "t")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        total = n_threads * per_thread
        assert log.stats().total_events == total
        ids = [e.event_id for e in log.replay_all()]
        assert len(set(ids)) == total

    def test_concurrent_appends_to_different_streams(self):
        log = DocReplayLog()

        def worker(sid):
            for _ in range(20):
                log.append(sid, "t")

        threads = [
            threading.Thread(target=worker, args=(f"s{i}",)) for i in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        s = log.stats()
        assert s.total_events == 80
        assert s.unique_streams == 4

    def test_concurrent_checkpoint_create(self):
        log = DocReplayLog()
        log.append("s", "t")

        def worker(i):
            log.create_checkpoint(f"cp-{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert log.stats().checkpoint_count == 10
