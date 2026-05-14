"""Tests for the event_buffer module (E167)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.event_buffer import BufferEvent, BufferStats, EventBuffer


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestBufferEvent:
    def test_required_fields(self):
        e = BufferEvent(event_id=1, event_type="t", timestamp=10.0)
        assert e.event_id == 1
        assert e.event_type == "t"
        assert e.timestamp == 10.0

    def test_data_default_factory(self):
        e1 = BufferEvent(event_id=1, event_type="t", timestamp=0.0)
        e2 = BufferEvent(event_id=2, event_type="t", timestamp=0.0)
        e1.data["x"] = 1
        # Mutating one event's data must not leak into another.
        assert e2.data == {}

    def test_source_default_none(self):
        e = BufferEvent(event_id=1, event_type="t", timestamp=0.0)
        assert e.source is None

    def test_explicit_data_and_source(self):
        e = BufferEvent(
            event_id=1,
            event_type="login",
            timestamp=0.0,
            data={"user": "alice"},
            source="auth",
        )
        assert e.data == {"user": "alice"}
        assert e.source == "auth"


class TestBufferStats:
    def test_construction(self):
        s = BufferStats(
            total_capacity=10,
            current_size=3,
            dropped_count=1,
            event_types={"a": 2, "b": 1},
        )
        assert s.total_capacity == 10
        assert s.current_size == 3
        assert s.dropped_count == 1
        assert s.event_types == {"a": 2, "b": 1}


# ---------------------------------------------------------------------------
# push
# ---------------------------------------------------------------------------
class TestPush:
    def test_returns_buffer_event(self):
        buf = EventBuffer(capacity=10)
        e = buf.push("login", {"user": "alice"}, source="auth", now=1.0)
        assert isinstance(e, BufferEvent)
        assert e.event_type == "login"
        assert e.data == {"user": "alice"}
        assert e.source == "auth"
        assert e.timestamp == 1.0

    def test_auto_increments_event_id(self):
        buf = EventBuffer(capacity=10)
        a = buf.push("a")
        b = buf.push("b")
        c = buf.push("c")
        assert a.event_id == 0
        assert b.event_id == 1
        assert c.event_id == 2

    def test_event_id_continues_after_eviction(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        c = buf.push("c")  # evicts a
        d = buf.push("d")  # evicts b
        assert c.event_id == 2
        assert d.event_id == 3

    def test_event_id_continues_after_pop(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.pop()
        b = buf.push("b")
        assert b.event_id == 1

    def test_default_data_is_empty_dict(self):
        buf = EventBuffer(capacity=10)
        e = buf.push("x")
        assert e.data == {}

    def test_default_source_is_none(self):
        buf = EventBuffer(capacity=10)
        e = buf.push("x")
        assert e.source is None

    def test_default_now_is_zero(self):
        buf = EventBuffer(capacity=10)
        e = buf.push("x")
        assert e.timestamp == 0.0

    def test_data_is_copied(self):
        buf = EventBuffer(capacity=10)
        d = {"k": 1}
        e = buf.push("x", d)
        d["k"] = 2
        assert e.data == {"k": 1}


# ---------------------------------------------------------------------------
# push_event
# ---------------------------------------------------------------------------
class TestPushEvent:
    def test_assigns_event_id(self):
        buf = EventBuffer(capacity=10)
        e = BufferEvent(event_id=999, event_type="x", timestamp=5.0)
        buf.push_event(e)
        # The buffer reassigns the id to a fresh sequence value.
        assert buf.peek().event_id == 0

    def test_keeps_other_fields(self):
        buf = EventBuffer(capacity=10)
        e = BufferEvent(
            event_id=999,
            event_type="login",
            timestamp=5.0,
            data={"u": "alice"},
            source="auth",
        )
        buf.push_event(e)
        out = buf.peek()
        assert out.event_type == "login"
        assert out.timestamp == 5.0
        assert out.data == {"u": "alice"}
        assert out.source == "auth"

    def test_sequence_with_push(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        e = BufferEvent(event_id=0, event_type="b", timestamp=0.0)
        buf.push_event(e)
        c = buf.push("c")
        ids = [ev.event_id for ev in buf.all()]
        assert ids == [0, 1, 2]
        assert c.event_id == 2

    def test_rejects_non_buffer_event(self):
        buf = EventBuffer(capacity=10)
        with pytest.raises(TypeError):
            buf.push_event({"event_type": "x"})


# ---------------------------------------------------------------------------
# pop
# ---------------------------------------------------------------------------
class TestPop:
    def test_pop_returns_oldest_first(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        assert buf.pop().event_type == "a"
        assert buf.pop().event_type == "b"
        assert buf.pop().event_type == "c"

    def test_pop_empty_returns_none(self):
        buf = EventBuffer(capacity=10)
        assert buf.pop() is None

    def test_pop_decreases_size(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.pop()
        assert buf.size == 1


# ---------------------------------------------------------------------------
# peek
# ---------------------------------------------------------------------------
class TestPeek:
    def test_peek_returns_oldest(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        assert buf.peek().event_type == "a"

    def test_peek_does_not_remove(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.peek()
        assert buf.size == 1

    def test_peek_empty(self):
        buf = EventBuffer(capacity=10)
        assert buf.peek() is None


# ---------------------------------------------------------------------------
# peek_latest
# ---------------------------------------------------------------------------
class TestPeekLatest:
    def test_peek_latest_returns_newest(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        assert buf.peek_latest().event_type == "c"

    def test_peek_latest_does_not_remove(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.peek_latest()
        assert buf.size == 1

    def test_peek_latest_empty(self):
        buf = EventBuffer(capacity=10)
        assert buf.peek_latest() is None


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_empties_buffer(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.clear()
        assert buf.size == 0
        assert buf.is_empty

    def test_clear_preserves_event_id_counter(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.clear()
        e = buf.push("c")
        assert e.event_id == 2

    def test_clear_preserves_dropped_count(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        buf.push("c")  # drop
        buf.clear()
        assert buf.stats().dropped_count == 1


# ---------------------------------------------------------------------------
# is_full / is_empty
# ---------------------------------------------------------------------------
class TestIsFullEmpty:
    def test_empty_buffer(self):
        buf = EventBuffer(capacity=3)
        assert buf.is_empty
        assert not buf.is_full

    def test_partial_buffer(self):
        buf = EventBuffer(capacity=3)
        buf.push("a")
        assert not buf.is_empty
        assert not buf.is_full

    def test_full_buffer(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        assert buf.is_full
        assert not buf.is_empty

    def test_remains_full_after_eviction(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        assert buf.is_full


# ---------------------------------------------------------------------------
# capacity / eviction
# ---------------------------------------------------------------------------
class TestCapacity:
    def test_capacity_property(self):
        buf = EventBuffer(capacity=5)
        assert buf.capacity == 5

    def test_default_capacity(self):
        buf = EventBuffer()
        assert buf.capacity == 1000

    def test_eviction_at_capacity(self):
        buf = EventBuffer(capacity=3)
        for t in ["a", "b", "c", "d", "e"]:
            buf.push(t)
        kinds = [e.event_type for e in buf.all()]
        assert kinds == ["c", "d", "e"]

    def test_size_capped(self):
        buf = EventBuffer(capacity=3)
        for i in range(10):
            buf.push("x")
        assert buf.size == 3

    def test_negative_capacity_raises(self):
        with pytest.raises(ValueError):
            EventBuffer(capacity=-1)

    def test_non_int_capacity_raises(self):
        with pytest.raises(TypeError):
            EventBuffer(capacity=3.5)


# ---------------------------------------------------------------------------
# dropped_count
# ---------------------------------------------------------------------------
class TestDroppedCount:
    def test_no_drops_under_capacity(self):
        buf = EventBuffer(capacity=5)
        for i in range(3):
            buf.push("x")
        assert buf.stats().dropped_count == 0

    def test_drops_after_overflow(self):
        buf = EventBuffer(capacity=3)
        for i in range(5):
            buf.push("x")
        assert buf.stats().dropped_count == 2

    def test_no_drops_when_pop_first(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        buf.pop()
        buf.push("c")  # no eviction needed
        assert buf.stats().dropped_count == 0

    def test_drops_include_push_event(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        buf.push_event(BufferEvent(event_id=0, event_type="c", timestamp=0.0))
        assert buf.stats().dropped_count == 1


# ---------------------------------------------------------------------------
# all (oldest first)
# ---------------------------------------------------------------------------
class TestAll:
    def test_all_oldest_first(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        kinds = [e.event_type for e in buf.all()]
        assert kinds == ["a", "b", "c"]

    def test_all_returns_list_copy(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        out = buf.all()
        out.clear()
        # Mutating the returned list does not touch the buffer.
        assert buf.size == 1

    def test_all_empty(self):
        buf = EventBuffer(capacity=10)
        assert buf.all() == []


# ---------------------------------------------------------------------------
# filter_by_type
# ---------------------------------------------------------------------------
class TestFilterByType:
    def test_basic(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("a")
        out = buf.filter_by_type("a")
        assert len(out) == 2
        assert all(e.event_type == "a" for e in out)

    def test_empty_match(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        assert buf.filter_by_type("missing") == []

    def test_preserves_order(self):
        buf = EventBuffer(capacity=10)
        for i, t in enumerate(["a", "b", "a", "b"]):
            buf.push(t)
        out = buf.filter_by_type("a")
        assert [e.event_id for e in out] == [0, 2]


# ---------------------------------------------------------------------------
# filter_by_source
# ---------------------------------------------------------------------------
class TestFilterBySource:
    def test_basic(self):
        buf = EventBuffer(capacity=10)
        buf.push("x", source="s1")
        buf.push("x", source="s2")
        buf.push("x", source="s1")
        out = buf.filter_by_source("s1")
        assert len(out) == 2

    def test_no_match(self):
        buf = EventBuffer(capacity=10)
        buf.push("x", source="s1")
        assert buf.filter_by_source("s9") == []

    def test_none_source(self):
        buf = EventBuffer(capacity=10)
        buf.push("x")  # source=None
        buf.push("y", source="s1")
        out = buf.filter_by_source(None)
        assert len(out) == 1
        assert out[0].event_type == "x"


# ---------------------------------------------------------------------------
# filter_by_time
# ---------------------------------------------------------------------------
class TestFilterByTime:
    def test_start_only(self):
        buf = EventBuffer(capacity=10)
        for t in [1.0, 2.0, 3.0, 4.0]:
            buf.push("x", now=t)
        out = buf.filter_by_time(start=3.0)
        assert [e.timestamp for e in out] == [3.0, 4.0]

    def test_end_only(self):
        buf = EventBuffer(capacity=10)
        for t in [1.0, 2.0, 3.0, 4.0]:
            buf.push("x", now=t)
        out = buf.filter_by_time(end=2.0)
        assert [e.timestamp for e in out] == [1.0, 2.0]

    def test_start_and_end(self):
        buf = EventBuffer(capacity=10)
        for t in [1.0, 2.0, 3.0, 4.0]:
            buf.push("x", now=t)
        out = buf.filter_by_time(start=2.0, end=3.0)
        assert [e.timestamp for e in out] == [2.0, 3.0]

    def test_no_bounds_returns_all(self):
        buf = EventBuffer(capacity=10)
        for t in [1.0, 2.0]:
            buf.push("x", now=t)
        out = buf.filter_by_time()
        assert len(out) == 2

    def test_bounds_inclusive(self):
        buf = EventBuffer(capacity=10)
        buf.push("x", now=1.0)
        buf.push("x", now=2.0)
        out = buf.filter_by_time(start=1.0, end=2.0)
        assert len(out) == 2


# ---------------------------------------------------------------------------
# count_by_type
# ---------------------------------------------------------------------------
class TestCountByType:
    def test_basic(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("a")
        buf.push("c")
        assert buf.count_by_type() == {"a": 2, "b": 1, "c": 1}

    def test_empty(self):
        buf = EventBuffer(capacity=10)
        assert buf.count_by_type() == {}

    def test_after_eviction(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("a")
        buf.push("b")  # evicts oldest a
        assert buf.count_by_type() == {"a": 1, "b": 1}


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_stats_full_snapshot(self):
        buf = EventBuffer(capacity=3)
        buf.push("a")
        buf.push("b")
        buf.push("a")
        s = buf.stats()
        assert isinstance(s, BufferStats)
        assert s.total_capacity == 3
        assert s.current_size == 3
        assert s.dropped_count == 0
        assert s.event_types == {"a": 2, "b": 1}

    def test_stats_after_overflow(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        s = buf.stats()
        assert s.current_size == 2
        assert s.dropped_count == 1
        assert s.event_types == {"b": 1, "c": 1}

    def test_stats_empty(self):
        buf = EventBuffer(capacity=5)
        s = buf.stats()
        assert s.current_size == 0
        assert s.dropped_count == 0
        assert s.event_types == {}


# ---------------------------------------------------------------------------
# replay
# ---------------------------------------------------------------------------
class TestReplay:
    def test_replay_all(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        buf.push("b")
        buf.push("c")
        out = buf.replay()
        assert [e.event_type for e in out] == ["a", "b", "c"]

    def test_replay_from_id(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")  # id=0
        buf.push("b")  # id=1
        buf.push("c")  # id=2
        out = buf.replay(start_event_id=1)
        assert [e.event_id for e in out] == [1, 2]

    def test_replay_skips_evicted(self):
        buf = EventBuffer(capacity=2)
        buf.push("a")  # id=0 — evicted
        buf.push("b")  # id=1
        buf.push("c")  # id=2
        out = buf.replay(start_event_id=0)
        # Only currently-buffered events are returned.
        assert [e.event_id for e in out] == [1, 2]

    def test_replay_above_max(self):
        buf = EventBuffer(capacity=10)
        buf.push("a")
        assert buf.replay(start_event_id=100) == []

    def test_replay_oldest_first(self):
        buf = EventBuffer(capacity=10)
        for t in ["a", "b", "c"]:
            buf.push(t)
        out = buf.replay()
        ids = [e.event_id for e in out]
        assert ids == sorted(ids)


# ---------------------------------------------------------------------------
# subscribe
# ---------------------------------------------------------------------------
class TestSubscribe:
    def test_callback_fires_on_push(self):
        buf = EventBuffer(capacity=10)
        seen = []
        buf.subscribe(lambda e: seen.append(e))
        buf.push("a")
        assert len(seen) == 1
        assert seen[0].event_type == "a"

    def test_callback_fires_on_push_event(self):
        buf = EventBuffer(capacity=10)
        seen = []
        buf.subscribe(lambda e: seen.append(e))
        buf.push_event(BufferEvent(event_id=0, event_type="b", timestamp=0.0))
        assert len(seen) == 1
        assert seen[0].event_type == "b"

    def test_callback_does_not_fire_on_pop(self):
        buf = EventBuffer(capacity=10)
        seen = []
        buf.push("a")
        buf.subscribe(lambda e: seen.append(e))
        buf.pop()
        assert seen == []

    def test_subscribe_returns_id(self):
        buf = EventBuffer(capacity=10)
        sid = buf.subscribe(lambda e: None)
        assert isinstance(sid, int)

    def test_callback_exception_does_not_break_buffer(self):
        buf = EventBuffer(capacity=10)

        def boom(e):
            raise RuntimeError("boom")

        buf.subscribe(boom)
        # Should not raise.
        buf.push("a")
        assert buf.size == 1

    def test_subscribe_non_callable_raises(self):
        buf = EventBuffer(capacity=10)
        with pytest.raises(TypeError):
            buf.subscribe("not callable")


# ---------------------------------------------------------------------------
# unsubscribe
# ---------------------------------------------------------------------------
class TestUnsubscribe:
    def test_unsubscribe_removes_callback(self):
        buf = EventBuffer(capacity=10)
        seen = []
        sid = buf.subscribe(lambda e: seen.append(e))
        buf.unsubscribe(sid)
        buf.push("a")
        assert seen == []

    def test_unsubscribe_returns_true(self):
        buf = EventBuffer(capacity=10)
        sid = buf.subscribe(lambda e: None)
        assert buf.unsubscribe(sid) is True

    def test_unsubscribe_missing_returns_false(self):
        buf = EventBuffer(capacity=10)
        assert buf.unsubscribe(999) is False

    def test_unsubscribe_idempotent(self):
        buf = EventBuffer(capacity=10)
        sid = buf.subscribe(lambda e: None)
        assert buf.unsubscribe(sid) is True
        assert buf.unsubscribe(sid) is False


# ---------------------------------------------------------------------------
# Multiple subscribers
# ---------------------------------------------------------------------------
class TestMultipleSubscribers:
    def test_all_subscribers_fire(self):
        buf = EventBuffer(capacity=10)
        a, b, c = [], [], []
        buf.subscribe(lambda e: a.append(e))
        buf.subscribe(lambda e: b.append(e))
        buf.subscribe(lambda e: c.append(e))
        buf.push("x")
        assert len(a) == len(b) == len(c) == 1

    def test_only_remaining_fires_after_unsub(self):
        buf = EventBuffer(capacity=10)
        a, b = [], []
        sid_a = buf.subscribe(lambda e: a.append(e))
        buf.subscribe(lambda e: b.append(e))
        buf.unsubscribe(sid_a)
        buf.push("x")
        assert a == []
        assert len(b) == 1

    def test_subscriber_callback_can_push(self):
        # Subscribers fire outside the lock, so a callback may safely
        # call back into the buffer without deadlocking.
        buf = EventBuffer(capacity=10)
        seen = []

        def on_event(e):
            seen.append(e.event_type)
            if e.event_type == "a":
                buf.push("b")

        buf.subscribe(on_event)
        buf.push("a")
        # Both events end up in the buffer; subscriber saw both.
        kinds = [e.event_type for e in buf.all()]
        assert kinds == ["a", "b"]
        assert "a" in seen and "b" in seen

    def test_thread_safety_concurrent_pushes(self):
        buf = EventBuffer(capacity=10_000)

        def worker():
            for _ in range(200):
                buf.push("x")

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert buf.size == 1000
        # event_ids should all be distinct.
        ids = [e.event_id for e in buf.all()]
        assert len(set(ids)) == 1000


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_capacity_zero_drops_everything(self):
        buf = EventBuffer(capacity=0)
        buf.push("a")
        buf.push("b")
        assert buf.size == 0
        assert buf.is_empty
        # is_full is False because capacity is 0 (nothing can be "full").
        assert buf.is_full is False
        s = buf.stats()
        assert s.current_size == 0
        assert s.dropped_count == 2

    def test_capacity_zero_subscribers_still_fire(self):
        buf = EventBuffer(capacity=0)
        seen = []
        buf.subscribe(lambda e: seen.append(e))
        buf.push("a")
        assert len(seen) == 1

    def test_pop_from_empty(self):
        buf = EventBuffer(capacity=10)
        assert buf.pop() is None
        assert buf.size == 0

    def test_large_capacity(self):
        buf = EventBuffer(capacity=100_000)
        for i in range(50_000):
            buf.push("x", now=float(i))
        assert buf.size == 50_000
        assert buf.peek().event_id == 0
        assert buf.peek_latest().event_id == 49_999
        assert buf.stats().dropped_count == 0

    def test_filter_methods_consistent_after_clear(self):
        buf = EventBuffer(capacity=10)
        buf.push("a", source="s1", now=1.0)
        buf.clear()
        assert buf.filter_by_type("a") == []
        assert buf.filter_by_source("s1") == []
        assert buf.filter_by_time(start=0.0, end=10.0) == []
        assert buf.count_by_type() == {}
        assert buf.replay() == []

    def test_imports(self):
        # Smoke test: public API is importable from the package root.
        from docstoolkit.event_buffer import (
            BufferEvent as BE,
            BufferStats as BS,
            EventBuffer as EB,
        )

        assert BE is BufferEvent
        assert BS is BufferStats
        assert EB is EventBuffer
