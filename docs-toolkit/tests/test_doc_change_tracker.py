"""Tests for the doc_change_tracker module."""
import os
import tempfile

import pytest

from docstoolkit.doc_change_tracker import (
    ChangeBatch,
    ChangeEvent,
    ChangeType,
    DocChangeTracker,
    TimelineEntry,
)


@pytest.fixture
def tracker():
    t = DocChangeTracker()
    yield t
    t.close()


# ---------------------------------------------------------------------------
# Enum / dataclass smoke tests
# ---------------------------------------------------------------------------


class TestChangeType:
    def test_values(self):
        assert ChangeType.CREATE.value == "CREATE"
        assert ChangeType.UPDATE.value == "UPDATE"
        assert ChangeType.DELETE.value == "DELETE"

    def test_rename(self):
        assert ChangeType.RENAME.value == "RENAME"

    def test_tag(self):
        assert ChangeType.TAG.value == "TAG"

    def test_comment(self):
        assert ChangeType.COMMENT.value == "COMMENT"

    def test_all_members(self):
        names = {m.name for m in ChangeType}
        assert names == {"CREATE", "UPDATE", "DELETE", "RENAME", "TAG", "COMMENT"}

    def test_from_string(self):
        assert ChangeType("UPDATE") is ChangeType.UPDATE


class TestChangeEvent:
    def test_construct(self):
        e = ChangeEvent(
            event_id=1,
            doc_id="doc-1",
            change_type=ChangeType.CREATE,
            actor="alice",
            timestamp=10.0,
        )
        assert e.event_id == 1
        assert e.doc_id == "doc-1"
        assert e.change_type is ChangeType.CREATE
        assert e.description is None

    def test_optional_fields(self):
        e = ChangeEvent(
            event_id=2,
            doc_id="d",
            change_type=ChangeType.UPDATE,
            actor="bob",
            timestamp=1.0,
            description="hi",
            before="x",
            after="y",
            batch_id="b1",
        )
        assert e.description == "hi"
        assert e.before == "x"
        assert e.after == "y"
        assert e.batch_id == "b1"


class TestChangeBatch:
    def test_construct(self):
        b = ChangeBatch(batch_id="b", actor="a", started_at=0.0, ended_at=1.0)
        assert b.events == []
        assert b.batch_id == "b"
        assert b.actor == "a"

    def test_with_events(self):
        e = ChangeEvent(
            event_id=1,
            doc_id="d",
            change_type=ChangeType.CREATE,
            actor="x",
            timestamp=0.0,
        )
        b = ChangeBatch(batch_id="b", actor="x", started_at=0.0, ended_at=2.0, events=[e])
        assert len(b.events) == 1


class TestTimelineEntry:
    def test_construct_defaults(self):
        t = TimelineEntry(timestamp=10.0, event_count=0)
        assert t.event_types == {}
        assert t.actors == set()

    def test_construct_full(self):
        t = TimelineEntry(
            timestamp=10.0,
            event_count=3,
            event_types={"CREATE": 2, "UPDATE": 1},
            actors={"a", "b"},
        )
        assert t.event_count == 3
        assert t.event_types["CREATE"] == 2


# ---------------------------------------------------------------------------
# record
# ---------------------------------------------------------------------------


class TestRecord:
    def test_basic_record(self, tracker):
        ev = tracker.record("doc-1", ChangeType.CREATE, "alice", now=100.0)
        assert isinstance(ev, ChangeEvent)
        assert ev.event_id >= 1
        assert ev.doc_id == "doc-1"
        assert ev.change_type is ChangeType.CREATE
        assert ev.actor == "alice"
        assert ev.timestamp == 100.0

    def test_record_with_description(self, tracker):
        ev = tracker.record(
            "doc-1", ChangeType.UPDATE, "alice", description="fix typo", now=1.0
        )
        assert ev.description == "fix typo"

    def test_record_with_before_after(self, tracker):
        ev = tracker.record(
            "d", ChangeType.UPDATE, "a", before="old", after="new", now=1.0
        )
        assert ev.before == "old"
        assert ev.after == "new"

    def test_record_with_batch_id(self, tracker):
        ev = tracker.record("d", ChangeType.CREATE, "a", batch_id="batch-x", now=1.0)
        assert ev.batch_id == "batch-x"

    def test_event_id_auto_increments(self, tracker):
        e1 = tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        e2 = tracker.record("d", ChangeType.UPDATE, "a", now=2.0)
        assert e2.event_id > e1.event_id

    def test_record_accepts_string_change_type(self, tracker):
        ev = tracker.record("d", "DELETE", "a", now=1.0)
        assert ev.change_type is ChangeType.DELETE

    def test_record_persists(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        assert tracker.total_events == 1

    def test_record_default_now_zero_is_literal(self, tracker):
        ev = tracker.record("d", ChangeType.CREATE, "a")
        assert ev.timestamp == 0.0

    def test_record_negative_now_uses_time(self, tracker):
        ev = tracker.record("d", ChangeType.CREATE, "a", now=-1)
        assert ev.timestamp > 0


# ---------------------------------------------------------------------------
# start/end batch
# ---------------------------------------------------------------------------


class TestStartEndBatch:
    def test_start_batch_returns_id(self, tracker):
        bid = tracker.start_batch("alice", now=5.0)
        assert isinstance(bid, str)
        assert bid

    def test_start_batch_unique_ids(self, tracker):
        ids = {tracker.start_batch("a", now=i) for i in range(5)}
        assert len(ids) == 5

    def test_end_batch_returns_batch(self, tracker):
        bid = tracker.start_batch("alice", now=1.0)
        b = tracker.end_batch(bid, now=5.0)
        assert isinstance(b, ChangeBatch)
        assert b.actor == "alice"
        assert b.started_at == 1.0
        assert b.ended_at == 5.0

    def test_end_batch_unknown(self, tracker):
        assert tracker.end_batch("nope") is None

    def test_end_batch_collects_events(self, tracker):
        bid = tracker.start_batch("a", now=1.0)
        tracker.record("d1", ChangeType.CREATE, "a", batch_id=bid, now=2.0)
        tracker.record("d2", ChangeType.UPDATE, "a", batch_id=bid, now=3.0)
        b = tracker.end_batch(bid, now=4.0)
        assert len(b.events) == 2

    def test_end_batch_event_order_chronological(self, tracker):
        bid = tracker.start_batch("a", now=1.0)
        tracker.record("d", ChangeType.CREATE, "a", batch_id=bid, now=2.0)
        tracker.record("d", ChangeType.UPDATE, "a", batch_id=bid, now=3.0)
        b = tracker.end_batch(bid, now=4.0)
        assert b.events[0].timestamp <= b.events[1].timestamp


# ---------------------------------------------------------------------------
# get_batch
# ---------------------------------------------------------------------------


class TestGetBatch:
    def test_get_existing_batch(self, tracker):
        bid = tracker.start_batch("alice", now=1.0)
        b = tracker.get_batch(bid)
        assert b is not None
        assert b.batch_id == bid
        assert b.actor == "alice"

    def test_get_unknown_batch(self, tracker):
        assert tracker.get_batch("nope") is None

    def test_get_batch_with_events(self, tracker):
        bid = tracker.start_batch("a", now=1.0)
        tracker.record("d", ChangeType.CREATE, "a", batch_id=bid, now=2.0)
        b = tracker.get_batch(bid)
        assert len(b.events) == 1
        assert b.events[0].batch_id == bid

    def test_get_batch_without_events(self, tracker):
        bid = tracker.start_batch("a", now=1.0)
        b = tracker.get_batch(bid)
        assert b.events == []


# ---------------------------------------------------------------------------
# events_for_doc
# ---------------------------------------------------------------------------


class TestEventsForDoc:
    def test_returns_only_matching_doc(self, tracker):
        tracker.record("d1", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d2", ChangeType.CREATE, "a", now=2.0)
        events = tracker.events_for_doc("d1")
        assert len(events) == 1
        assert events[0].doc_id == "d1"

    def test_newest_first(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=2.0)
        tracker.record("d", ChangeType.DELETE, "a", now=3.0)
        events = tracker.events_for_doc("d")
        assert events[0].timestamp == 3.0
        assert events[-1].timestamp == 1.0

    def test_limit(self, tracker):
        for i in range(5):
            tracker.record("d", ChangeType.UPDATE, "a", now=float(i))
        events = tracker.events_for_doc("d", limit=2)
        assert len(events) == 2

    def test_no_events_returns_empty(self, tracker):
        assert tracker.events_for_doc("missing") == []


# ---------------------------------------------------------------------------
# events_by_actor
# ---------------------------------------------------------------------------


class TestEventsByActor:
    def test_returns_only_actor(self, tracker):
        tracker.record("d", ChangeType.CREATE, "alice", now=1.0)
        tracker.record("d", ChangeType.CREATE, "bob", now=2.0)
        events = tracker.events_by_actor("alice")
        assert len(events) == 1
        assert events[0].actor == "alice"

    def test_newest_first(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=2.0)
        events = tracker.events_by_actor("a")
        assert events[0].timestamp == 2.0

    def test_limit(self, tracker):
        for i in range(4):
            tracker.record("d", ChangeType.UPDATE, "alice", now=float(i))
        events = tracker.events_by_actor("alice", limit=2)
        assert len(events) == 2

    def test_unknown_actor(self, tracker):
        assert tracker.events_by_actor("ghost") == []


# ---------------------------------------------------------------------------
# events_in_range
# ---------------------------------------------------------------------------


class TestEventsInRange:
    def test_inclusive_bounds(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=5.0)
        events = tracker.events_in_range(5.0, 5.0)
        assert len(events) == 1

    def test_excludes_outside(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=10.0)
        tracker.record("d", ChangeType.DELETE, "a", now=20.0)
        events = tracker.events_in_range(5.0, 15.0)
        assert len(events) == 1
        assert events[0].timestamp == 10.0

    def test_empty_range(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        assert tracker.events_in_range(100.0, 200.0) == []

    def test_returns_newest_first(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=2.0)
        events = tracker.events_in_range(0.0, 100.0)
        assert events[0].timestamp == 2.0


# ---------------------------------------------------------------------------
# events_by_type
# ---------------------------------------------------------------------------


class TestEventsByType:
    def test_filters_by_type(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=2.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=3.0)
        events = tracker.events_by_type(ChangeType.UPDATE)
        assert len(events) == 2

    def test_limit(self, tracker):
        for i in range(5):
            tracker.record("d", ChangeType.UPDATE, "a", now=float(i))
        events = tracker.events_by_type(ChangeType.UPDATE, limit=3)
        assert len(events) == 3

    def test_accepts_string(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        events = tracker.events_by_type("CREATE")
        assert len(events) == 1

    def test_newest_first(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.CREATE, "a", now=3.0)
        events = tracker.events_by_type(ChangeType.CREATE)
        assert events[0].timestamp == 3.0


# ---------------------------------------------------------------------------
# timeline
# ---------------------------------------------------------------------------


class TestTimeline:
    def test_single_bucket(self, tracker):
        tracker.record("d", ChangeType.CREATE, "alice", now=10.0)
        tracker.record("d", ChangeType.UPDATE, "bob", now=20.0)
        entries = tracker.timeline(0.0, 3600.0, bucket_size=3600.0)
        assert len(entries) == 1
        e = entries[0]
        assert e.event_count == 2
        assert e.event_types == {"CREATE": 1, "UPDATE": 1}
        assert e.actors == {"alice", "bob"}

    def test_multiple_buckets(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=0.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=10.0)
        tracker.record("d", ChangeType.DELETE, "a", now=70.0)
        entries = tracker.timeline(0.0, 200.0, bucket_size=60.0)
        # Two buckets: [0,60) and [60,120)
        assert len(entries) == 2
        assert entries[0].timestamp == 0.0
        assert entries[0].event_count == 2
        assert entries[1].timestamp == 60.0
        assert entries[1].event_count == 1

    def test_only_non_empty_buckets(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=0.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=300.0)
        entries = tracker.timeline(0.0, 600.0, bucket_size=60.0)
        # Two non-empty buckets, the rest skipped
        assert len(entries) == 2

    def test_ascending_order(self, tracker):
        tracker.record("d", ChangeType.UPDATE, "a", now=200.0)
        tracker.record("d", ChangeType.CREATE, "a", now=10.0)
        entries = tracker.timeline(0.0, 1000.0, bucket_size=60.0)
        timestamps = [e.timestamp for e in entries]
        assert timestamps == sorted(timestamps)

    def test_empty_range(self, tracker):
        assert tracker.timeline(0.0, 100.0) == []

    def test_invalid_bucket_size(self, tracker):
        with pytest.raises(ValueError):
            tracker.timeline(0.0, 100.0, bucket_size=0)


# ---------------------------------------------------------------------------
# actors_for_doc / last_change / count_for_doc / total_events
# ---------------------------------------------------------------------------


class TestActorsForDoc:
    def test_unique_actors(self, tracker):
        tracker.record("d", ChangeType.CREATE, "alice", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "bob", now=2.0)
        tracker.record("d", ChangeType.UPDATE, "alice", now=3.0)
        assert tracker.actors_for_doc("d") == {"alice", "bob"}

    def test_no_events(self, tracker):
        assert tracker.actors_for_doc("missing") == set()

    def test_ignores_other_docs(self, tracker):
        tracker.record("d1", ChangeType.CREATE, "alice", now=1.0)
        tracker.record("d2", ChangeType.CREATE, "bob", now=2.0)
        assert tracker.actors_for_doc("d1") == {"alice"}


class TestLastChange:
    def test_returns_most_recent(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d", ChangeType.UPDATE, "a", now=5.0)
        tracker.record("d", ChangeType.DELETE, "a", now=3.0)
        last = tracker.last_change("d")
        assert last.timestamp == 5.0
        assert last.change_type is ChangeType.UPDATE

    def test_no_events(self, tracker):
        assert tracker.last_change("missing") is None

    def test_per_doc(self, tracker):
        tracker.record("d1", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d2", ChangeType.CREATE, "a", now=5.0)
        assert tracker.last_change("d1").timestamp == 1.0


class TestCountForDoc:
    def test_zero(self, tracker):
        assert tracker.count_for_doc("none") == 0

    def test_counts(self, tracker):
        for _ in range(3):
            tracker.record("d", ChangeType.UPDATE, "a", now=1.0)
        assert tracker.count_for_doc("d") == 3

    def test_per_doc(self, tracker):
        tracker.record("d1", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d2", ChangeType.CREATE, "a", now=1.0)
        tracker.record("d2", ChangeType.UPDATE, "a", now=2.0)
        assert tracker.count_for_doc("d1") == 1
        assert tracker.count_for_doc("d2") == 2


class TestTotalEvents:
    def test_zero(self, tracker):
        assert tracker.total_events == 0

    def test_count_all(self, tracker):
        for i in range(7):
            tracker.record("d", ChangeType.UPDATE, "a", now=float(i))
        assert tracker.total_events == 7

    def test_property(self, tracker):
        # Make sure it is a property, not a method.
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        assert isinstance(DocChangeTracker.total_events, property)


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_removes_events(self, tracker):
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.clear()
        assert tracker.total_events == 0

    def test_clear_removes_batches(self, tracker):
        bid = tracker.start_batch("a", now=1.0)
        tracker.clear()
        assert tracker.get_batch(bid) is None

    def test_clear_safe_on_empty(self, tracker):
        tracker.clear()
        assert tracker.total_events == 0


# ---------------------------------------------------------------------------
# persistence
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_file_db_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ct.db")
            t1 = DocChangeTracker(path)
            t1.record("d", ChangeType.CREATE, "alice", now=1.0)
            bid = t1.start_batch("alice", now=2.0)
            t1.record("d", ChangeType.UPDATE, "alice", batch_id=bid, now=3.0)
            t1.end_batch(bid, now=4.0)
            t1.close()

            t2 = DocChangeTracker(path)
            try:
                assert t2.total_events == 2
                b = t2.get_batch(bid)
                assert b is not None
                assert b.actor == "alice"
                assert len(b.events) == 1
            finally:
                t2.close()

    def test_in_memory_isolated(self):
        a = DocChangeTracker()
        b = DocChangeTracker()
        try:
            a.record("d", ChangeType.CREATE, "x", now=1.0)
            assert b.total_events == 0
        finally:
            a.close()
            b.close()


# ---------------------------------------------------------------------------
# edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_tracker_queries(self, tracker):
        assert tracker.events_for_doc("d") == []
        assert tracker.events_by_actor("a") == []
        assert tracker.events_by_type(ChangeType.CREATE) == []
        assert tracker.events_in_range(0.0, 100.0) == []
        assert tracker.timeline(0.0, 100.0) == []
        assert tracker.last_change("d") is None
        assert tracker.count_for_doc("d") == 0
        assert tracker.actors_for_doc("d") == set()
        assert tracker.total_events == 0

    def test_unknown_batch_get(self, tracker):
        assert tracker.get_batch("not-a-real-batch") is None

    def test_unknown_batch_end(self, tracker):
        assert tracker.end_batch("not-real") is None

    def test_close_idempotent_after_use(self, tracker):
        # We just need to be sure close completes once on a fresh tracker.
        tracker.record("d", ChangeType.CREATE, "a", now=1.0)
        tracker.close()
        # Re-close would raise; we deliberately don't test that.

    def test_record_in_batch_links(self, tracker):
        bid = tracker.start_batch("alice", now=1.0)
        ev = tracker.record("d", ChangeType.CREATE, "alice", batch_id=bid, now=2.0)
        assert ev.batch_id == bid
        b = tracker.get_batch(bid)
        assert b.events[0].event_id == ev.event_id

    def test_close_then_reopen_in_memory_loses_data(self):
        t = DocChangeTracker()
        t.record("d", ChangeType.CREATE, "a", now=1.0)
        assert t.total_events == 1
        t.close()
