"""Tests for the ``doc_event_replay`` module."""
import os
import tempfile
import threading

import pytest

from docstoolkit.doc_event_replay import (
    DocEventReplay,
    RecordedEvent,
    ReplayFilter,
    ReplayResult,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


class CollectingHandler:
    """Handler that records every event it sees and returns ``True`` by default."""

    def __init__(self, return_value: bool = True):
        self.seen: list = []
        self.return_value = return_value

    def __call__(self, event: RecordedEvent) -> bool:
        self.seen.append(event)
        return self.return_value


def _make_log(events=None) -> DocEventReplay:
    """Build a fresh in-memory log, optionally pre-populated with events."""
    log = DocEventReplay()
    if events:
        for e in events:
            log.record(**e)
    return log


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestRecordedEvent:
    def test_defaults(self):
        e = RecordedEvent()
        assert e.event_id == 0
        assert e.event_type == ""
        assert e.doc_id == ""
        assert e.payload == {}
        assert e.timestamp == 0.0
        assert e.actor is None

    def test_custom_values(self):
        e = RecordedEvent(
            event_id=42,
            event_type="EDIT",
            doc_id="doc-1",
            payload={"k": "v"},
            timestamp=12.5,
            actor="alice",
        )
        assert e.event_id == 42
        assert e.event_type == "EDIT"
        assert e.doc_id == "doc-1"
        assert e.payload == {"k": "v"}
        assert e.timestamp == 12.5
        assert e.actor == "alice"

    def test_payload_is_mutable_dict(self):
        e = RecordedEvent()
        e.payload["x"] = 1
        assert e.payload == {"x": 1}

    def test_independent_payload_per_instance(self):
        a = RecordedEvent()
        b = RecordedEvent()
        a.payload["x"] = 1
        assert b.payload == {}


class TestReplayResult:
    def test_defaults(self):
        r = ReplayResult()
        assert r.events_replayed == 0
        assert r.events_skipped == 0
        assert r.errors == []
        assert r.start_time == 0.0
        assert r.end_time == 0.0
        assert r.success is True

    def test_custom_values(self):
        r = ReplayResult(
            events_replayed=3,
            events_skipped=1,
            errors=["boom"],
            start_time=1.0,
            end_time=5.0,
            success=False,
        )
        assert r.events_replayed == 3
        assert r.events_skipped == 1
        assert r.errors == ["boom"]
        assert r.start_time == 1.0
        assert r.end_time == 5.0
        assert r.success is False


class TestReplayFilter:
    def test_defaults_match_everything(self):
        f = ReplayFilter()
        e = RecordedEvent(event_type="EDIT", doc_id="d", actor="a", timestamp=1.0)
        assert f.matches(e) is True

    def test_event_types_filter(self):
        f = ReplayFilter(event_types=["EDIT"])
        assert f.matches(RecordedEvent(event_type="EDIT")) is True
        assert f.matches(RecordedEvent(event_type="DELETE")) is False

    def test_doc_ids_filter(self):
        f = ReplayFilter(doc_ids=["d1", "d2"])
        assert f.matches(RecordedEvent(doc_id="d1")) is True
        assert f.matches(RecordedEvent(doc_id="d3")) is False

    def test_actors_filter(self):
        f = ReplayFilter(actors=["alice"])
        assert f.matches(RecordedEvent(actor="alice")) is True
        assert f.matches(RecordedEvent(actor="bob")) is False

    def test_start_filter(self):
        f = ReplayFilter(start=10.0)
        assert f.matches(RecordedEvent(timestamp=10.0)) is True
        assert f.matches(RecordedEvent(timestamp=11.0)) is True
        assert f.matches(RecordedEvent(timestamp=9.0)) is False

    def test_end_filter(self):
        f = ReplayFilter(end=10.0)
        assert f.matches(RecordedEvent(timestamp=10.0)) is True
        assert f.matches(RecordedEvent(timestamp=9.0)) is True
        assert f.matches(RecordedEvent(timestamp=11.0)) is False

    def test_combined_filter(self):
        f = ReplayFilter(
            event_types=["EDIT"], doc_ids=["d1"], start=5.0, end=10.0
        )
        good = RecordedEvent(event_type="EDIT", doc_id="d1", timestamp=7.0)
        bad_type = RecordedEvent(event_type="DELETE", doc_id="d1", timestamp=7.0)
        bad_doc = RecordedEvent(event_type="EDIT", doc_id="other", timestamp=7.0)
        bad_time = RecordedEvent(event_type="EDIT", doc_id="d1", timestamp=20.0)
        assert f.matches(good) is True
        assert f.matches(bad_type) is False
        assert f.matches(bad_doc) is False
        assert f.matches(bad_time) is False


# ---------------------------------------------------------------------------
# Recording
# ---------------------------------------------------------------------------


class TestRecord:
    def test_returns_recorded_event(self):
        log = _make_log()
        e = log.record("EDIT", "doc-1", {"k": "v"}, actor="alice", now=1.0)
        assert isinstance(e, RecordedEvent)
        assert e.event_type == "EDIT"
        assert e.doc_id == "doc-1"
        assert e.payload == {"k": "v"}
        assert e.actor == "alice"
        assert e.timestamp == 1.0

    def test_auto_increment_event_id(self):
        log = _make_log()
        a = log.record("EDIT", "d", {}, now=1.0)
        b = log.record("EDIT", "d", {}, now=2.0)
        c = log.record("EDIT", "d", {}, now=3.0)
        assert a.event_id < b.event_id < c.event_id

    def test_record_persists_to_db(self):
        log = _make_log()
        e = log.record("EDIT", "doc-1", {"k": "v"}, now=1.0)
        fetched = log.get(e.event_id)
        assert fetched is not None
        assert fetched.payload == {"k": "v"}

    def test_record_default_actor_is_none(self):
        log = _make_log()
        e = log.record("EDIT", "doc-1", {})
        assert e.actor is None

    def test_record_default_now(self):
        log = _make_log()
        e = log.record("EDIT", "doc-1", {})
        assert e.timestamp == 0.0

    def test_payload_isolated_from_caller(self):
        log = _make_log()
        payload = {"k": "v"}
        e = log.record("EDIT", "d", payload, now=1.0)
        payload["k"] = "mutated"
        fetched = log.get(e.event_id)
        assert fetched.payload == {"k": "v"}

    def test_complex_payload(self):
        log = _make_log()
        payload = {"a": [1, 2, 3], "b": {"nested": True}, "c": None}
        e = log.record("EDIT", "d", payload, now=1.0)
        fetched = log.get(e.event_id)
        assert fetched.payload == payload


# ---------------------------------------------------------------------------
# Replay
# ---------------------------------------------------------------------------


class TestReplayBasic:
    def test_replay_empty_log(self):
        log = _make_log()
        h = CollectingHandler()
        r = log.replay(h)
        assert r.events_replayed == 0
        assert r.events_skipped == 0
        assert r.errors == []
        assert r.start_time == 0.0
        assert r.end_time == 0.0
        assert r.success is True

    def test_replay_all_events(self):
        log = _make_log()
        log.record("EDIT", "d1", {}, now=1.0)
        log.record("EDIT", "d2", {}, now=2.0)
        log.record("DELETE", "d3", {}, now=3.0)
        h = CollectingHandler()
        r = log.replay(h)
        assert r.events_replayed == 3
        assert r.events_skipped == 0
        assert r.success is True

    def test_replay_returns_replay_result(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        r = log.replay(CollectingHandler())
        assert isinstance(r, ReplayResult)

    def test_replay_in_chronological_order(self):
        log = _make_log()
        log.record("A", "d", {}, now=1.0)
        log.record("B", "d", {}, now=2.0)
        log.record("C", "d", {}, now=3.0)
        h = CollectingHandler()
        log.replay(h)
        assert [e.event_type for e in h.seen] == ["A", "B", "C"]

    def test_replay_sets_start_end_times(self):
        log = _make_log()
        log.record("E", "d", {}, now=10.0)
        log.record("E", "d", {}, now=20.0)
        log.record("E", "d", {}, now=30.0)
        r = log.replay(CollectingHandler())
        assert r.start_time == 10.0
        assert r.end_time == 30.0

    def test_replay_passes_recorded_event(self):
        log = _make_log()
        log.record("EDIT", "d1", {"k": "v"}, actor="alice", now=1.0)
        h = CollectingHandler()
        log.replay(h)
        assert len(h.seen) == 1
        ev = h.seen[0]
        assert ev.event_type == "EDIT"
        assert ev.doc_id == "d1"
        assert ev.payload == {"k": "v"}
        assert ev.actor == "alice"


class TestReplayWithFilter:
    def test_filter_by_event_type(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        log.record("DELETE", "d", {}, now=2.0)
        log.record("EDIT", "d", {}, now=3.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(event_types=["EDIT"]))
        assert r.events_replayed == 2
        assert all(e.event_type == "EDIT" for e in h.seen)

    def test_filter_by_doc_ids(self):
        log = _make_log()
        log.record("E", "d1", {}, now=1.0)
        log.record("E", "d2", {}, now=2.0)
        log.record("E", "d3", {}, now=3.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(doc_ids=["d1", "d3"]))
        assert r.events_replayed == 2
        assert {e.doc_id for e in h.seen} == {"d1", "d3"}

    def test_filter_by_actors(self):
        log = _make_log()
        log.record("E", "d", {}, actor="alice", now=1.0)
        log.record("E", "d", {}, actor="bob", now=2.0)
        log.record("E", "d", {}, actor="alice", now=3.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(actors=["alice"]))
        assert r.events_replayed == 2
        assert all(e.actor == "alice" for e in h.seen)

    def test_filter_by_time_range(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=10.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(start=2.0, end=8.0))
        assert r.events_replayed == 1
        assert h.seen[0].timestamp == 5.0

    def test_filter_combined(self):
        log = _make_log()
        log.record("EDIT", "d1", {}, actor="alice", now=1.0)
        log.record("DELETE", "d1", {}, actor="alice", now=2.0)
        log.record("EDIT", "d2", {}, actor="alice", now=3.0)
        log.record("EDIT", "d1", {}, actor="bob", now=4.0)
        h = CollectingHandler()
        r = log.replay(
            h,
            ReplayFilter(
                event_types=["EDIT"], doc_ids=["d1"], actors=["alice"]
            ),
        )
        assert r.events_replayed == 1
        assert h.seen[0].timestamp == 1.0

    def test_filter_no_matches(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(event_types=["DELETE"]))
        assert r.events_replayed == 0
        assert r.events_skipped == 0
        assert h.seen == []

    def test_filter_empty_lists_match_nothing(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(event_types=[]))
        assert r.events_replayed == 0
        assert h.seen == []


class TestReplayRange:
    def test_basic_range(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=10.0)
        h = CollectingHandler()
        r = log.replay_range(h, 2.0, 8.0)
        assert r.events_replayed == 1

    def test_inclusive_bounds(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=10.0)
        h = CollectingHandler()
        r = log.replay_range(h, 1.0, 10.0)
        assert r.events_replayed == 3

    def test_empty_range(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        h = CollectingHandler()
        r = log.replay_range(h, 100.0, 200.0)
        assert r.events_replayed == 0

    def test_zero_width_range_hits_only_exact_match(self):
        log = _make_log()
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=6.0)
        h = CollectingHandler()
        r = log.replay_range(h, 5.0, 5.0)
        assert r.events_replayed == 1


class TestReplayToPoint:
    def test_basic(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=10.0)
        h = CollectingHandler()
        r = log.replay_to_point(h, 5.0)
        assert r.events_replayed == 2

    def test_inclusive_upper_bound(self):
        log = _make_log()
        log.record("E", "d", {}, now=5.0)
        h = CollectingHandler()
        r = log.replay_to_point(h, 5.0)
        assert r.events_replayed == 1

    def test_point_before_any_event(self):
        log = _make_log()
        log.record("E", "d", {}, now=10.0)
        h = CollectingHandler()
        r = log.replay_to_point(h, 1.0)
        assert r.events_replayed == 0

    def test_point_after_all_events(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        h = CollectingHandler()
        r = log.replay_to_point(h, 100.0)
        assert r.events_replayed == 2


class TestReplayHandlerSkip:
    def test_handler_returning_false_counts_as_skipped(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        h = CollectingHandler(return_value=False)
        r = log.replay(h)
        assert r.events_replayed == 0
        assert r.events_skipped == 2
        assert r.success is True

    def test_mixed_skip_and_replay(self):
        log = _make_log()
        for i in range(4):
            log.record("E", "d", {"i": i}, now=float(i))

        def handler(event):
            return event.payload["i"] % 2 == 0

        r = log.replay(handler)
        assert r.events_replayed == 2
        assert r.events_skipped == 2


class TestReplayHandlerError:
    def test_handler_exception_captured(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)

        def handler(event):
            raise RuntimeError("boom")

        r = log.replay(handler)
        assert r.events_replayed == 0
        assert r.events_skipped == 1
        assert len(r.errors) == 1
        assert "RuntimeError" in r.errors[0]
        assert "boom" in r.errors[0]
        assert r.success is False

    def test_handler_continues_after_error(self):
        log = _make_log()
        log.record("E", "d", {"i": 0}, now=1.0)
        log.record("E", "d", {"i": 1}, now=2.0)
        log.record("E", "d", {"i": 2}, now=3.0)

        def handler(event):
            if event.payload["i"] == 1:
                raise ValueError("bad")
            return True

        r = log.replay(handler)
        assert r.events_replayed == 2
        assert r.events_skipped == 1
        assert len(r.errors) == 1
        assert r.success is False

    def test_multiple_errors_captured(self):
        log = _make_log()
        for i in range(3):
            log.record("E", "d", {"i": i}, now=float(i))

        def handler(event):
            raise RuntimeError(f"err-{event.payload['i']}")

        r = log.replay(handler)
        assert len(r.errors) == 3
        assert r.events_replayed == 0
        assert r.events_skipped == 3


# ---------------------------------------------------------------------------
# Queries
# ---------------------------------------------------------------------------


class TestCount:
    def test_empty(self):
        log = _make_log()
        assert log.count() == 0

    def test_no_filter(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        assert log.count() == 2

    def test_with_filter(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        log.record("DELETE", "d", {}, now=2.0)
        log.record("EDIT", "d", {}, now=3.0)
        assert log.count(ReplayFilter(event_types=["EDIT"])) == 2

    def test_filter_no_matches(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        assert log.count(ReplayFilter(event_types=["NONE"])) == 0


class TestEventsForDoc:
    def test_returns_all_events_for_doc(self):
        log = _make_log()
        log.record("E", "d1", {}, now=1.0)
        log.record("E", "d2", {}, now=2.0)
        log.record("E", "d1", {}, now=3.0)
        events = log.events_for_doc("d1")
        assert len(events) == 2
        assert all(e.doc_id == "d1" for e in events)

    def test_chronological_order(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        log.record("E", "d", {}, now=3.0)
        events = log.events_for_doc("d")
        assert [e.timestamp for e in events] == [1.0, 2.0, 3.0]

    def test_limit(self):
        log = _make_log()
        for i in range(5):
            log.record("E", "d", {}, now=float(i))
        events = log.events_for_doc("d", limit=2)
        assert len(events) == 2

    def test_unknown_doc(self):
        log = _make_log()
        assert log.events_for_doc("nope") == []


class TestEventsByActor:
    def test_returns_all_events_for_actor(self):
        log = _make_log()
        log.record("E", "d", {}, actor="alice", now=1.0)
        log.record("E", "d", {}, actor="bob", now=2.0)
        log.record("E", "d", {}, actor="alice", now=3.0)
        events = log.events_by_actor("alice")
        assert len(events) == 2

    def test_limit(self):
        log = _make_log()
        for _ in range(5):
            log.record("E", "d", {}, actor="alice", now=1.0)
        assert len(log.events_by_actor("alice", limit=3)) == 3

    def test_unknown_actor(self):
        log = _make_log()
        log.record("E", "d", {}, actor="bob", now=1.0)
        assert log.events_by_actor("alice") == []


class TestEventsByType:
    def test_returns_all_events_of_type(self):
        log = _make_log()
        log.record("EDIT", "d", {}, now=1.0)
        log.record("DELETE", "d", {}, now=2.0)
        log.record("EDIT", "d", {}, now=3.0)
        events = log.events_by_type("EDIT")
        assert len(events) == 2

    def test_limit(self):
        log = _make_log()
        for _ in range(5):
            log.record("EDIT", "d", {}, now=1.0)
        assert len(log.events_by_type("EDIT", limit=2)) == 2

    def test_unknown_type(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        assert log.events_by_type("NONE") == []


class TestLatestEvent:
    def test_returns_latest(self):
        log = _make_log()
        log.record("A", "d", {}, now=1.0)
        log.record("B", "d", {}, now=2.0)
        log.record("C", "d", {}, now=3.0)
        e = log.latest_event("d")
        assert e is not None
        assert e.event_type == "C"

    def test_returns_none_for_unknown(self):
        log = _make_log()
        assert log.latest_event("nope") is None

    def test_isolated_by_doc(self):
        log = _make_log()
        log.record("X", "d1", {}, now=1.0)
        log.record("Y", "d2", {}, now=2.0)
        e = log.latest_event("d1")
        assert e.event_type == "X"


class TestGet:
    def test_returns_event_by_id(self):
        log = _make_log()
        e = log.record("E", "d", {"k": "v"}, now=1.0)
        fetched = log.get(e.event_id)
        assert fetched is not None
        assert fetched.event_id == e.event_id
        assert fetched.payload == {"k": "v"}

    def test_returns_none_for_unknown(self):
        log = _make_log()
        assert log.get(9999) is None

    def test_round_trip_preserves_actor_none(self):
        log = _make_log()
        e = log.record("E", "d", {}, actor=None, now=1.0)
        fetched = log.get(e.event_id)
        assert fetched.actor is None


# ---------------------------------------------------------------------------
# Maintenance
# ---------------------------------------------------------------------------


class TestPurgeOlderThan:
    def test_removes_old_events(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=5.0)
        log.record("E", "d", {}, now=10.0)
        # cutoff = now(10) - older_than(4) = 6, so 1.0 and 5.0 dropped
        removed = log.purge_older_than(older_than=4.0, now=10.0)
        assert removed == 2
        assert log.total_events == 1

    def test_keeps_recent_events(self):
        log = _make_log()
        log.record("E", "d", {}, now=10.0)
        removed = log.purge_older_than(older_than=100.0, now=10.0)
        assert removed == 0
        assert log.total_events == 1

    def test_purge_all(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        removed = log.purge_older_than(older_than=0.0, now=100.0)
        assert removed == 2
        assert log.total_events == 0

    def test_purge_empty_log(self):
        log = _make_log()
        assert log.purge_older_than(1.0, now=10.0) == 0


class TestClear:
    def test_clear_removes_all(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.record("E", "d", {}, now=2.0)
        log.clear()
        assert log.total_events == 0

    def test_clear_empty_log(self):
        log = _make_log()
        log.clear()
        assert log.total_events == 0

    def test_record_after_clear(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        log.clear()
        e = log.record("E", "d", {}, now=2.0)
        assert log.total_events == 1
        assert log.get(e.event_id) is not None


class TestTotalEvents:
    def test_empty_log(self):
        log = _make_log()
        assert log.total_events == 0

    def test_increments_on_record(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        assert log.total_events == 1
        log.record("E", "d", {}, now=2.0)
        assert log.total_events == 2

    def test_property(self):
        log = _make_log()
        # access as attribute, not callable
        assert isinstance(log.total_events, int)


# ---------------------------------------------------------------------------
# Persistence
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_file_db_persists_between_instances(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "events.db")
            log1 = DocEventReplay(db_path=path)
            log1.record("EDIT", "doc-1", {"k": "v"}, actor="alice", now=1.0)
            log1.record("DELETE", "doc-2", {}, now=2.0)
            log1.close()

            log2 = DocEventReplay(db_path=path)
            assert log2.total_events == 2
            events = log2.events_for_doc("doc-1")
            assert len(events) == 1
            assert events[0].payload == {"k": "v"}
            log2.close()

    def test_in_memory_does_not_persist(self):
        log1 = DocEventReplay()
        log1.record("E", "d", {}, now=1.0)
        assert log1.total_events == 1
        log1.close()
        log2 = DocEventReplay()
        assert log2.total_events == 0

    def test_close_is_safe(self):
        log = DocEventReplay()
        log.record("E", "d", {}, now=1.0)
        log.close()


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_log_no_matches(self):
        log = _make_log()
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(event_types=["X"]))
        assert r.events_replayed == 0
        assert r.events_skipped == 0
        assert r.errors == []
        assert h.seen == []

    def test_payload_default_empty_dict(self):
        log = _make_log()
        e = log.record("E", "d", {})
        assert e.payload == {}
        assert log.get(e.event_id).payload == {}

    def test_replay_includes_null_actor(self):
        log = _make_log()
        log.record("E", "d", {}, actor=None, now=1.0)
        log.record("E", "d", {}, actor="alice", now=2.0)
        h = CollectingHandler()
        r = log.replay(h)
        assert r.events_replayed == 2

    def test_filter_actors_with_none(self):
        log = _make_log()
        log.record("E", "d", {}, actor=None, now=1.0)
        log.record("E", "d", {}, actor="alice", now=2.0)
        h = CollectingHandler()
        r = log.replay(h, ReplayFilter(actors=[None]))
        assert r.events_replayed == 1
        assert h.seen[0].actor is None

    def test_filter_event_types_empty_list(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        assert log.count(ReplayFilter(event_types=[])) == 0

    def test_filter_doc_ids_empty_list(self):
        log = _make_log()
        log.record("E", "d", {}, now=1.0)
        assert log.count(ReplayFilter(doc_ids=[])) == 0

    def test_thread_safety_record(self):
        log = _make_log()

        def worker():
            for _ in range(20):
                log.record("E", "d", {}, now=1.0)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert log.total_events == 100

    def test_unicode_payload(self):
        log = _make_log()
        payload = {"text": "Привет, мир! 你好"}
        e = log.record("E", "d", payload, now=1.0)
        assert log.get(e.event_id).payload == payload

    def test_unicode_doc_id_and_actor(self):
        log = _make_log()
        log.record("E", "документ-1", {}, actor="алиса", now=1.0)
        assert len(log.events_for_doc("документ-1")) == 1
        assert len(log.events_by_actor("алиса")) == 1

    def test_negative_timestamps_supported(self):
        log = _make_log()
        log.record("E", "d", {}, now=-5.0)
        log.record("E", "d", {}, now=0.0)
        r = log.replay_range(CollectingHandler(), -10.0, -1.0)
        assert r.events_replayed == 1
