"""Tests for the doc_event_store module (E283).

Covers:
- DocEvent dataclass
- StreamInfo dataclass
- EventStoreStats dataclass
- DocEventStore: append, get_event, read_stream, read_all, latest,
  stream_info, streams, events_by_type, truncate_stream, stats,
  total_events, total_streams properties
- Edge cases: empty store, missing stream, limits, from_seq/from_event_id,
  truncate, thread safety
"""

from __future__ import annotations

import threading
import time
from dataclasses import fields

import pytest

from docstoolkit.doc_event_store import (
    DocEvent,
    DocEventStore,
    EventStoreStats,
    StreamInfo,
)


# =========================================================================
# DocEvent dataclass
# =========================================================================


class TestDocEvent:
    def test_fields_present(self):
        names = {f.name for f in fields(DocEvent)}
        assert names == {"event_id", "stream_id", "event_type", "payload", "timestamp", "sequence"}

    def test_create_minimal(self):
        e = DocEvent(
            event_id=1,
            stream_id="doc:1",
            event_type="created",
            payload={"x": 1},
            timestamp=1000.0,
            sequence=1,
        )
        assert e.event_id == 1
        assert e.stream_id == "doc:1"
        assert e.event_type == "created"
        assert e.payload == {"x": 1}
        assert e.timestamp == 1000.0
        assert e.sequence == 1

    def test_payload_is_dict(self):
        e = DocEvent(1, "s", "t", {}, 0.0, 1)
        assert isinstance(e.payload, dict)

    def test_different_stream_ids(self):
        e = DocEvent(1, "doc:abc-123", "updated", {}, 0.0, 1)
        assert e.stream_id == "doc:abc-123"


# =========================================================================
# StreamInfo dataclass
# =========================================================================


class TestStreamInfo:
    def test_fields_present(self):
        names = {f.name for f in fields(StreamInfo)}
        assert names == {"stream_id", "event_count", "first_at", "last_at", "latest_sequence"}

    def test_create(self):
        si = StreamInfo(
            stream_id="doc:5",
            event_count=3,
            first_at=100.0,
            last_at=300.0,
            latest_sequence=3,
        )
        assert si.stream_id == "doc:5"
        assert si.event_count == 3
        assert si.first_at == 100.0
        assert si.last_at == 300.0
        assert si.latest_sequence == 3


# =========================================================================
# EventStoreStats dataclass
# =========================================================================


class TestEventStoreStats:
    def test_fields_present(self):
        names = {f.name for f in fields(EventStoreStats)}
        assert names == {"total_events", "total_streams", "event_types"}

    def test_create(self):
        st = EventStoreStats(total_events=10, total_streams=2, event_types=["created", "updated"])
        assert st.total_events == 10
        assert st.total_streams == 2
        assert st.event_types == ["created", "updated"]


# =========================================================================
# DocEventStore — basic construction
# =========================================================================


class TestDocEventStoreInit:
    def test_empty_on_creation(self):
        store = DocEventStore()
        assert store.total_events == 0
        assert store.total_streams == 0

    def test_streams_empty_list(self):
        store = DocEventStore()
        assert store.streams() == []

    def test_stats_empty(self):
        store = DocEventStore()
        st = store.stats()
        assert st.total_events == 0
        assert st.total_streams == 0
        assert st.event_types == []

    def test_read_all_empty(self):
        store = DocEventStore()
        assert store.read_all() == []

    def test_read_stream_unknown(self):
        store = DocEventStore()
        assert store.read_stream("doc:999") == []

    def test_stream_info_unknown(self):
        store = DocEventStore()
        assert store.stream_info("doc:999") is None

    def test_latest_unknown(self):
        store = DocEventStore()
        assert store.latest("doc:999") is None

    def test_get_event_zero(self):
        store = DocEventStore()
        assert store.get_event(0) is None

    def test_get_event_negative(self):
        store = DocEventStore()
        assert store.get_event(-1) is None


# =========================================================================
# DocEventStore — append
# =========================================================================


class TestAppend:
    def test_returns_doc_event(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert isinstance(e, DocEvent)

    def test_event_id_starts_at_1(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert e.event_id == 1

    def test_event_id_increments(self):
        store = DocEventStore()
        e1 = store.append("doc:1", "created")
        e2 = store.append("doc:1", "updated")
        assert e2.event_id == e1.event_id + 1

    def test_sequence_starts_at_1(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert e.sequence == 1

    def test_sequence_increments_per_stream(self):
        store = DocEventStore()
        e1 = store.append("doc:1", "created")
        e2 = store.append("doc:1", "updated")
        assert e1.sequence == 1
        assert e2.sequence == 2

    def test_sequence_independent_across_streams(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        e = store.append("doc:2", "created")
        assert e.sequence == 1

    def test_payload_default_empty_dict(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert e.payload == {}

    def test_payload_stored(self):
        store = DocEventStore()
        e = store.append("doc:1", "created", {"title": "Hello"})
        assert e.payload == {"title": "Hello"}

    def test_stream_id_stored(self):
        store = DocEventStore()
        e = store.append("doc:42", "created")
        assert e.stream_id == "doc:42"

    def test_event_type_stored(self):
        store = DocEventStore()
        e = store.append("doc:1", "deleted")
        assert e.event_type == "deleted"

    def test_timestamp_auto(self):
        before = time.time()
        store = DocEventStore()
        e = store.append("doc:1", "created")
        after = time.time()
        assert before <= e.timestamp <= after

    def test_timestamp_override(self):
        store = DocEventStore()
        e = store.append("doc:1", "created", now=12345.0)
        assert e.timestamp == 12345.0

    def test_total_events_increments(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        assert store.total_events == 2

    def test_total_streams_increments(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        assert store.total_streams == 2

    def test_same_stream_does_not_add_new_stream(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        assert store.total_streams == 1


# =========================================================================
# DocEventStore — get_event
# =========================================================================


class TestGetEvent:
    def test_retrieves_by_event_id(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert store.get_event(e.event_id) == e

    def test_missing_id_returns_none(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        assert store.get_event(999) is None

    def test_all_events_retrievable(self):
        store = DocEventStore()
        events = [store.append("doc:1", "e") for _ in range(5)]
        for e in events:
            assert store.get_event(e.event_id) == e


# =========================================================================
# DocEventStore — read_stream
# =========================================================================


class TestReadStream:
    def test_returns_all_stream_events(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        result = store.read_stream("doc:1")
        assert len(result) == 2

    def test_ordered_by_sequence(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        result = store.read_stream("doc:1")
        assert result[0].sequence < result[1].sequence

    def test_excludes_other_streams(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        result = store.read_stream("doc:1")
        assert all(e.stream_id == "doc:1" for e in result)

    def test_from_seq_filters(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        result = store.read_stream("doc:1", from_seq=3)
        assert all(e.sequence >= 3 for e in result)
        assert len(result) == 3

    def test_from_seq_1_returns_all(self):
        store = DocEventStore()
        for _ in range(3):
            store.append("doc:1", "e")
        assert len(store.read_stream("doc:1", from_seq=1)) == 3

    def test_limit_truncates(self):
        store = DocEventStore()
        for _ in range(10):
            store.append("doc:1", "e")
        result = store.read_stream("doc:1", limit=3)
        assert len(result) == 3

    def test_limit_none_returns_all(self):
        store = DocEventStore()
        for _ in range(7):
            store.append("doc:1", "e")
        assert len(store.read_stream("doc:1", limit=None)) == 7

    def test_unknown_stream_empty(self):
        store = DocEventStore()
        assert store.read_stream("doc:none") == []

    def test_returns_new_list(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        r1 = store.read_stream("doc:1")
        r2 = store.read_stream("doc:1")
        assert r1 is not r2


# =========================================================================
# DocEventStore — read_all
# =========================================================================


class TestReadAll:
    def test_returns_all_events(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        assert len(store.read_all()) == 2

    def test_ordered_by_event_id(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        result = store.read_all()
        ids = [e.event_id for e in result]
        assert ids == sorted(ids)

    def test_from_event_id_filters(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        result = store.read_all(from_event_id=3)
        assert all(e.event_id >= 3 for e in result)
        assert len(result) == 3

    def test_from_event_id_1_returns_all(self):
        store = DocEventStore()
        for _ in range(4):
            store.append("doc:1", "e")
        assert len(store.read_all(from_event_id=1)) == 4

    def test_limit_applied(self):
        store = DocEventStore()
        for _ in range(8):
            store.append("doc:1", "e")
        assert len(store.read_all(limit=3)) == 3

    def test_empty_store(self):
        store = DocEventStore()
        assert store.read_all() == []


# =========================================================================
# DocEventStore — latest
# =========================================================================


class TestLatest:
    def test_returns_last_event(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        last = store.append("doc:1", "updated")
        assert store.latest("doc:1") == last

    def test_unknown_stream(self):
        store = DocEventStore()
        assert store.latest("doc:999") is None

    def test_single_event(self):
        store = DocEventStore()
        e = store.append("doc:1", "created")
        assert store.latest("doc:1") == e

    def test_does_not_cross_streams(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        e2 = store.append("doc:2", "created")
        store.append("doc:2", "updated")
        assert store.latest("doc:1").stream_id == "doc:1"
        assert store.latest("doc:2").stream_id == "doc:2"


# =========================================================================
# DocEventStore — stream_info
# =========================================================================


class TestStreamInfo_:
    def test_returns_stream_info(self):
        store = DocEventStore()
        store.append("doc:1", "created", now=100.0)
        store.append("doc:1", "updated", now=200.0)
        info = store.stream_info("doc:1")
        assert isinstance(info, StreamInfo)
        assert info.stream_id == "doc:1"
        assert info.event_count == 2
        assert info.first_at == 100.0
        assert info.last_at == 200.0
        assert info.latest_sequence == 2

    def test_missing_stream_is_none(self):
        store = DocEventStore()
        assert store.stream_info("doc:missing") is None

    def test_single_event_first_eq_last(self):
        store = DocEventStore()
        store.append("doc:1", "created", now=500.0)
        info = store.stream_info("doc:1")
        assert info.first_at == info.last_at == 500.0


# =========================================================================
# DocEventStore — streams()
# =========================================================================


class TestStreams:
    def test_sorted(self):
        store = DocEventStore()
        store.append("doc:z", "e")
        store.append("doc:a", "e")
        store.append("doc:m", "e")
        assert store.streams() == ["doc:a", "doc:m", "doc:z"]

    def test_empty(self):
        store = DocEventStore()
        assert store.streams() == []

    def test_no_duplicates(self):
        store = DocEventStore()
        store.append("doc:1", "e")
        store.append("doc:1", "e")
        assert store.streams() == ["doc:1"]


# =========================================================================
# DocEventStore — events_by_type
# =========================================================================


class TestEventsByType:
    def test_filters_by_type(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        store.append("doc:2", "created")
        result = store.events_by_type("created")
        assert len(result) == 2
        assert all(e.event_type == "created" for e in result)

    def test_ordered_by_event_id(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        result = store.events_by_type("created")
        assert result[0].event_id < result[1].event_id

    def test_unknown_type_empty(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        assert store.events_by_type("deleted") == []

    def test_limit_applied(self):
        store = DocEventStore()
        for i in range(5):
            store.append(f"doc:{i}", "created")
        assert len(store.events_by_type("created", limit=2)) == 2

    def test_cross_stream(self):
        store = DocEventStore()
        store.append("doc:1", "deleted")
        store.append("doc:2", "deleted")
        store.append("doc:3", "created")
        result = store.events_by_type("deleted")
        assert len(result) == 2


# =========================================================================
# DocEventStore — truncate_stream
# =========================================================================


class TestTruncateStream:
    def test_removes_oldest_events(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        removed = store.truncate_stream("doc:1", keep_last=2)
        assert removed == 3
        remaining = store.read_stream("doc:1")
        assert len(remaining) == 2

    def test_keep_last_sequences(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        store.truncate_stream("doc:1", keep_last=2)
        remaining = store.read_stream("doc:1")
        assert remaining[0].sequence == 4
        assert remaining[1].sequence == 5

    def test_keep_last_zero_removes_all(self):
        store = DocEventStore()
        for _ in range(3):
            store.append("doc:1", "e")
        removed = store.truncate_stream("doc:1", keep_last=0)
        assert removed == 3
        assert store.read_stream("doc:1") == []

    def test_keep_more_than_present_no_op(self):
        store = DocEventStore()
        store.append("doc:1", "e")
        store.append("doc:1", "e")
        removed = store.truncate_stream("doc:1", keep_last=10)
        assert removed == 0

    def test_unknown_stream_returns_zero(self):
        store = DocEventStore()
        assert store.truncate_stream("doc:999", keep_last=2) == 0

    def test_negative_keep_last_raises(self):
        store = DocEventStore()
        with pytest.raises(ValueError):
            store.truncate_stream("doc:1", keep_last=-1)

    def test_removed_events_absent_from_read_all(self):
        store = DocEventStore()
        for _ in range(4):
            store.append("doc:1", "e")
        store.truncate_stream("doc:1", keep_last=2)
        all_events = store.read_all()
        assert len(all_events) == 2

    def test_removed_events_absent_from_get_event(self):
        store = DocEventStore()
        e1 = store.append("doc:1", "e")
        for _ in range(3):
            store.append("doc:1", "e")
        store.truncate_stream("doc:1", keep_last=2)
        assert store.get_event(e1.event_id) is None

    def test_total_events_updated_after_truncate(self):
        store = DocEventStore()
        for _ in range(5):
            store.append("doc:1", "e")
        store.truncate_stream("doc:1", keep_last=3)
        assert store.total_events == 3

    def test_does_not_affect_other_streams(self):
        store = DocEventStore()
        for _ in range(3):
            store.append("doc:1", "e")
        for _ in range(3):
            store.append("doc:2", "e")
        store.truncate_stream("doc:1", keep_last=1)
        assert len(store.read_stream("doc:2")) == 3


# =========================================================================
# DocEventStore — stats & properties
# =========================================================================


class TestStats:
    def test_stats_after_appends(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:1", "updated")
        store.append("doc:2", "created")
        st = store.stats()
        assert st.total_events == 3
        assert st.total_streams == 2
        assert st.event_types == ["created", "updated"]

    def test_event_types_sorted(self):
        store = DocEventStore()
        store.append("doc:1", "updated")
        store.append("doc:1", "created")
        store.append("doc:1", "deleted")
        st = store.stats()
        assert st.event_types == sorted(st.event_types)

    def test_event_types_unique(self):
        store = DocEventStore()
        store.append("doc:1", "created")
        store.append("doc:2", "created")
        st = store.stats()
        assert st.event_types.count("created") == 1

    def test_total_events_property(self):
        store = DocEventStore()
        store.append("doc:1", "e")
        store.append("doc:1", "e")
        assert store.total_events == 2

    def test_total_streams_property(self):
        store = DocEventStore()
        store.append("doc:1", "e")
        store.append("doc:2", "e")
        store.append("doc:3", "e")
        assert store.total_streams == 3


# =========================================================================
# Thread safety
# =========================================================================


class TestThreadSafety:
    def test_concurrent_appends_no_data_loss(self):
        store = DocEventStore()
        n_threads = 8
        events_per_thread = 50

        def worker(stream_id: str):
            for _ in range(events_per_thread):
                store.append(stream_id, "e")

        threads = [
            threading.Thread(target=worker, args=(f"doc:{i}",))
            for i in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert store.total_events == n_threads * events_per_thread
        assert store.total_streams == n_threads

    def test_concurrent_appends_unique_event_ids(self):
        store = DocEventStore()
        collected: list = []
        lock = threading.Lock()

        def worker():
            e = store.append("doc:shared", "e")
            with lock:
                collected.append(e.event_id)

        threads = [threading.Thread(target=worker) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(collected)) == 100

    def test_concurrent_reads_do_not_raise(self):
        store = DocEventStore()
        for _ in range(20):
            store.append("doc:1", "e")

        errors: list = []

        def reader():
            try:
                store.read_stream("doc:1")
                store.read_all()
                store.stats()
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=reader) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
