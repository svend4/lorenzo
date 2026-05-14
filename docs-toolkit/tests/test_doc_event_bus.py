"""Tests for the doc_event_bus module."""

from __future__ import annotations

import pytest

from docstoolkit.doc_event_bus import (
    BusStats,
    DispatchMode,
    DocEventBus,
    Event,
    EventPriority,
    Subscription,
)


# ---------------------------------------------------------------- enums


class TestEventPriority:
    def test_has_four_levels(self):
        assert EventPriority.LOW.value == 1
        assert EventPriority.NORMAL.value == 2
        assert EventPriority.HIGH.value == 3
        assert EventPriority.URGENT.value == 4

    def test_ordering_distinct(self):
        values = {p.value for p in EventPriority}
        assert len(values) == 4

    def test_names(self):
        assert {p.name for p in EventPriority} == {"LOW", "NORMAL", "HIGH", "URGENT"}


class TestDispatchMode:
    def test_has_two_modes(self):
        assert DispatchMode.SYNC.value == "sync"
        assert DispatchMode.ASYNC.value == "async"

    def test_distinct(self):
        assert DispatchMode.SYNC is not DispatchMode.ASYNC


# ----------------------------------------------------------- dataclasses


class TestEvent:
    def test_create_minimal(self):
        e = Event(event_id=1, topic="doc.created", data={"id": "x"})
        assert e.event_id == 1
        assert e.topic == "doc.created"
        assert e.data == {"id": "x"}
        assert e.timestamp == 0.0
        assert e.priority is EventPriority.NORMAL
        assert e.source is None

    def test_create_with_source(self):
        e = Event(event_id=2, topic="t", data={}, source="api")
        assert e.source == "api"

    def test_priority_field(self):
        e = Event(event_id=3, topic="t", data={}, priority=EventPriority.HIGH)
        assert e.priority is EventPriority.HIGH


class TestSubscription:
    def test_default_fields(self):
        s = Subscription(sub_id="x", topic_pattern="*", handler=lambda e: None)
        assert s.priority == 0
        assert s.mode is DispatchMode.SYNC
        assert s.enabled is True

    def test_custom_fields(self):
        h = lambda e: None
        s = Subscription(
            sub_id="y",
            topic_pattern="doc.*",
            handler=h,
            priority=5,
            mode=DispatchMode.ASYNC,
            enabled=False,
        )
        assert s.priority == 5
        assert s.mode is DispatchMode.ASYNC
        assert s.enabled is False
        assert s.handler is h


class TestBusStats:
    def test_defaults(self):
        s = BusStats(
            total_events=0,
            total_subscriptions=0,
            total_dispatched=0,
            total_errors=0,
        )
        assert s.by_topic == {}

    def test_with_topics(self):
        s = BusStats(
            total_events=2,
            total_subscriptions=1,
            total_dispatched=3,
            total_errors=0,
            by_topic={"a": 2},
        )
        assert s.by_topic["a"] == 2


# --------------------------------------------------------------- subscribe


class TestSubscribe:
    def test_returns_id(self):
        bus = DocEventBus()
        sid = bus.subscribe("doc.*", lambda e: None)
        assert isinstance(sid, str)
        assert sid.startswith("sub-")

    def test_unique_ids(self):
        bus = DocEventBus()
        ids = {bus.subscribe("a", lambda e: None) for _ in range(5)}
        assert len(ids) == 5

    def test_default_sync(self):
        bus = DocEventBus()
        sid = bus.subscribe("a", lambda e: None)
        subs = bus.subscribers_for("a")
        assert subs[0].mode is DispatchMode.SYNC
        assert subs[0].sub_id == sid

    def test_async_mode(self):
        bus = DocEventBus()
        bus.subscribe("a", lambda e: None, mode=DispatchMode.ASYNC)
        assert bus.subscribers_for("a")[0].mode is DispatchMode.ASYNC

    def test_priority(self):
        bus = DocEventBus()
        bus.subscribe("a", lambda e: None, priority=7)
        assert bus.subscribers_for("a")[0].priority == 7


class TestUnsubscribe:
    def test_removes(self):
        bus = DocEventBus()
        sid = bus.subscribe("a", lambda e: None)
        assert bus.unsubscribe(sid) is True
        assert bus.subscription_count == 0

    def test_missing(self):
        bus = DocEventBus()
        assert bus.unsubscribe("nope") is False

    def test_double_unsubscribe(self):
        bus = DocEventBus()
        sid = bus.subscribe("a", lambda e: None)
        bus.unsubscribe(sid)
        assert bus.unsubscribe(sid) is False


class TestEnableDisable:
    def test_disable_then_no_dispatch(self):
        bus = DocEventBus()
        calls = []
        sid = bus.subscribe("a", lambda e: calls.append(e))
        assert bus.disable_subscription(sid) is True
        bus.publish("a", {})
        assert calls == []

    def test_enable_after_disable(self):
        bus = DocEventBus()
        calls = []
        sid = bus.subscribe("a", lambda e: calls.append(e))
        bus.disable_subscription(sid)
        assert bus.enable_subscription(sid) is True
        bus.publish("a", {})
        assert len(calls) == 1

    def test_enable_missing(self):
        bus = DocEventBus()
        assert bus.enable_subscription("zz") is False

    def test_disable_missing(self):
        bus = DocEventBus()
        assert bus.disable_subscription("zz") is False


# ----------------------------------------------------------------- publish


class TestPublishSync:
    def test_invokes_handler(self):
        bus = DocEventBus()
        seen = []
        bus.subscribe("doc.created", lambda e: seen.append(e))
        ev = bus.publish("doc.created", {"id": "x"})
        assert len(seen) == 1
        assert seen[0].topic == "doc.created"
        assert seen[0].event_id == ev.event_id

    def test_no_match_no_invoke(self):
        bus = DocEventBus()
        seen = []
        bus.subscribe("doc.deleted", lambda e: seen.append(e))
        bus.publish("doc.created", {})
        assert seen == []

    def test_returns_event(self):
        bus = DocEventBus()
        ev = bus.publish("t", {"k": 1}, source="s", now=10.0)
        assert ev.topic == "t"
        assert ev.data == {"k": 1}
        assert ev.source == "s"
        assert ev.timestamp == 10.0

    def test_event_id_increments(self):
        bus = DocEventBus()
        a = bus.publish("t", {})
        b = bus.publish("t", {})
        assert b.event_id == a.event_id + 1

    def test_priority_passed(self):
        bus = DocEventBus()
        captured = []
        bus.subscribe("t", lambda e: captured.append(e.priority))
        bus.publish("t", {}, priority=EventPriority.URGENT)
        assert captured == [EventPriority.URGENT]


class TestPublishAsync:
    def test_not_invoked_immediately(self):
        bus = DocEventBus()
        seen = []
        bus.subscribe("t", lambda e: seen.append(e), mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        assert seen == []
        assert bus.pending_async_count() == 1

    def test_invoked_after_flush(self):
        bus = DocEventBus()
        seen = []
        bus.subscribe("t", lambda e: seen.append(e), mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        bus.flush_async()
        assert len(seen) == 1

    def test_mixed_sync_and_async(self):
        bus = DocEventBus()
        sync_seen = []
        async_seen = []
        bus.subscribe("t", lambda e: sync_seen.append(e), mode=DispatchMode.SYNC)
        bus.subscribe("t", lambda e: async_seen.append(e), mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        assert len(sync_seen) == 1
        assert async_seen == []
        bus.flush_async()
        assert len(async_seen) == 1


class TestPublishSyncOnly:
    def test_returns_count(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None)
        bus.subscribe("t", lambda e: None)
        count = bus.publish_sync_only("t", {})
        assert count == 2

    def test_skips_async(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        count = bus.publish_sync_only("t", {})
        assert count == 0
        assert bus.pending_async_count() == 0

    def test_kwargs_priority(self):
        bus = DocEventBus()
        captured = []
        bus.subscribe("t", lambda e: captured.append(e.priority))
        bus.publish_sync_only("t", {}, priority=EventPriority.HIGH)
        assert captured == [EventPriority.HIGH]


# -------------------------------------------------------------- middleware


class TestMiddleware:
    def test_transforms_event(self):
        bus = DocEventBus()
        captured = []
        bus.subscribe("t", lambda e: captured.append(e.data))

        def mw(e):
            e.data = {"transformed": True}
            return e

        bus.add_middleware(mw)
        bus.publish("t", {"orig": 1})
        assert captured == [{"transformed": True}]

    def test_drop_filters_event(self):
        bus = DocEventBus()
        captured = []
        bus.subscribe("t", lambda e: captured.append(e))
        bus.add_middleware(lambda e: None)
        bus.publish("t", {})
        assert captured == []

    def test_chain_order(self):
        bus = DocEventBus()
        order = []

        def mw1(e):
            order.append("a")
            return e

        def mw2(e):
            order.append("b")
            return e

        bus.add_middleware(mw1)
        bus.add_middleware(mw2)
        bus.subscribe("t", lambda e: None)
        bus.publish("t", {})
        assert order == ["a", "b"]

    def test_returns_id(self):
        bus = DocEventBus()
        mid = bus.add_middleware(lambda e: e)
        assert isinstance(mid, int)


class TestRemoveMiddleware:
    def test_removes(self):
        bus = DocEventBus()
        mid = bus.add_middleware(lambda e: None)
        assert bus.remove_middleware(mid) is True
        captured = []
        bus.subscribe("t", lambda e: captured.append(e))
        bus.publish("t", {})
        assert len(captured) == 1

    def test_missing(self):
        bus = DocEventBus()
        assert bus.remove_middleware(999) is False


# ----------------------------------------------------------------- matches


class TestMatchesExact:
    def test_exact_match(self):
        assert DocEventBus.matches("doc.created", "doc.created") is True

    def test_no_match(self):
        assert DocEventBus.matches("doc.created", "doc.deleted") is False

    def test_segment_count_mismatch(self):
        assert DocEventBus.matches("doc", "doc.created") is False


class TestMatchesStarWildcard:
    def test_star_one_segment(self):
        assert DocEventBus.matches("doc.created", "doc.*") is True

    def test_star_does_not_span(self):
        assert DocEventBus.matches("doc.profile.updated", "doc.*") is False

    def test_star_alone(self):
        assert DocEventBus.matches("doc", "*") is True

    def test_star_in_middle(self):
        assert DocEventBus.matches("doc.user.created", "doc.*.created") is True

    def test_star_no_match_two_segments(self):
        assert DocEventBus.matches("a.b.c", "*") is False


class TestMatchesHashWildcard:
    def test_hash_alone_matches_any(self):
        assert DocEventBus.matches("a", "#") is True
        assert DocEventBus.matches("a.b.c", "#") is True

    def test_hash_multi_segment(self):
        assert DocEventBus.matches("doc.profile.updated", "doc.#") is True

    def test_hash_single_segment(self):
        assert DocEventBus.matches("doc.created", "doc.#") is True

    def test_hash_empty_does_not_match(self):
        assert DocEventBus.matches("", "#") is False

    def test_hash_with_tail(self):
        assert DocEventBus.matches("doc.profile.updated", "#.updated") is True


# ----------------------------------------------------------------- flush


class TestFlushAsync:
    def test_returns_count(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        bus.publish("t", {})
        assert bus.flush_async() == 2

    def test_empty_returns_zero(self):
        bus = DocEventBus()
        assert bus.flush_async() == 0

    def test_drains_queue(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        bus.flush_async()
        assert bus.pending_async_count() == 0


class TestSubscribersFor:
    def test_includes_matches(self):
        bus = DocEventBus()
        s1 = bus.subscribe("doc.*", lambda e: None)
        s2 = bus.subscribe("doc.created", lambda e: None)
        bus.subscribe("user.*", lambda e: None)
        ids = {s.sub_id for s in bus.subscribers_for("doc.created")}
        assert ids == {s1, s2}

    def test_excludes_disabled(self):
        bus = DocEventBus()
        sid = bus.subscribe("t", lambda e: None)
        bus.disable_subscription(sid)
        assert bus.subscribers_for("t") == []

    def test_include_disabled_when_flag(self):
        bus = DocEventBus()
        sid = bus.subscribe("t", lambda e: None)
        bus.disable_subscription(sid)
        subs = bus.subscribers_for("t", enabled_only=False)
        assert len(subs) == 1


# ----------------------------------------------------------------- counts


class TestEventCount:
    def test_starts_zero(self):
        assert DocEventBus().event_count == 0

    def test_increments(self):
        bus = DocEventBus()
        bus.publish("t", {})
        bus.publish("t", {})
        assert bus.event_count == 2


class TestSubscriptionCount:
    def test_starts_zero(self):
        assert DocEventBus().subscription_count == 0

    def test_increments(self):
        bus = DocEventBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        assert bus.subscription_count == 2

    def test_decrements_on_unsubscribe(self):
        bus = DocEventBus()
        sid = bus.subscribe("a", lambda e: None)
        bus.unsubscribe(sid)
        assert bus.subscription_count == 0


class TestPendingAsyncCount:
    def test_initial_zero(self):
        assert DocEventBus().pending_async_count() == 0

    def test_grows(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        bus.publish("t", {})
        assert bus.pending_async_count() == 2


# ----------------------------------------------------------------- stats


class TestStats:
    def test_basic(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None)
        bus.publish("t", {})
        s = bus.stats()
        assert s.total_events == 1
        assert s.total_subscriptions == 1
        assert s.total_dispatched == 1
        assert s.total_errors == 0
        assert s.by_topic == {"t": 1}

    def test_returns_busstats(self):
        bus = DocEventBus()
        assert isinstance(bus.stats(), BusStats)

    def test_by_topic_separated(self):
        bus = DocEventBus()
        bus.publish("a", {})
        bus.publish("b", {})
        bus.publish("a", {})
        s = bus.stats()
        assert s.by_topic == {"a": 2, "b": 1}


# ----------------------------------------------------------- handler errors


class TestHandlerError:
    def test_error_counted(self):
        bus = DocEventBus()

        def bad(e):
            raise ValueError("boom")

        bus.subscribe("t", bad)
        bus.publish("t", {})
        assert bus.stats().total_errors == 1

    def test_other_handlers_run(self):
        bus = DocEventBus()
        seen = []

        def bad(e):
            raise RuntimeError("x")

        bus.subscribe("t", bad)
        bus.subscribe("t", lambda e: seen.append(e))
        bus.publish("t", {})
        assert len(seen) == 1

    def test_async_errors_counted_after_flush(self):
        bus = DocEventBus()

        def bad(e):
            raise RuntimeError

        bus.subscribe("t", bad, mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        assert bus.stats().total_errors == 0
        bus.flush_async()
        assert bus.stats().total_errors == 1


# ---------------------------------------------------------- handler priority


class TestPriority:
    def test_higher_runs_first(self):
        bus = DocEventBus()
        order = []
        bus.subscribe("t", lambda e: order.append("low"), priority=1)
        bus.subscribe("t", lambda e: order.append("high"), priority=10)
        bus.subscribe("t", lambda e: order.append("mid"), priority=5)
        bus.publish("t", {})
        assert order == ["high", "mid", "low"]

    def test_ties_stable_by_subid(self):
        bus = DocEventBus()
        order = []
        bus.subscribe("t", lambda e: order.append(1))
        bus.subscribe("t", lambda e: order.append(2))
        bus.subscribe("t", lambda e: order.append(3))
        bus.publish("t", {})
        assert order == [1, 2, 3]


# ----------------------------------------------------------------- clear


class TestClear:
    def test_resets_state(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None)
        bus.add_middleware(lambda e: e)
        bus.publish("t", {})
        bus.clear()
        assert bus.subscription_count == 0
        assert bus.event_count == 0
        assert bus.stats().total_dispatched == 0
        assert bus.stats().by_topic == {}

    def test_clear_drains_async(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.publish("t", {})
        bus.clear()
        assert bus.pending_async_count() == 0


# ------------------------------------------------------------- edge cases


class TestEdgeCases:
    def test_publish_no_subscribers(self):
        bus = DocEventBus()
        ev = bus.publish("nobody", {"x": 1})
        assert ev.topic == "nobody"
        assert bus.stats().total_dispatched == 0

    def test_middleware_chain_dropped_does_not_dispatch_async(self):
        bus = DocEventBus()
        bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.add_middleware(lambda e: None)
        bus.publish("t", {})
        assert bus.pending_async_count() == 0

    def test_pattern_with_only_hash_matches_deep(self):
        bus = DocEventBus()
        seen = []
        bus.subscribe("#", lambda e: seen.append(e.topic))
        bus.publish("a.b.c.d", {})
        bus.publish("x", {})
        assert seen == ["a.b.c.d", "x"]

    def test_disabled_does_not_consume_async_slot(self):
        bus = DocEventBus()
        sid = bus.subscribe("t", lambda e: None, mode=DispatchMode.ASYNC)
        bus.disable_subscription(sid)
        bus.publish("t", {})
        assert bus.pending_async_count() == 0

    def test_multiple_patterns_match_same_event(self):
        bus = DocEventBus()
        count = []
        bus.subscribe("doc.#", lambda e: count.append(1))
        bus.subscribe("doc.*", lambda e: count.append(2))
        bus.subscribe("#", lambda e: count.append(3))
        bus.publish("doc.created", {})
        assert sorted(count) == [1, 2, 3]


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
