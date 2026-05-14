"""Tests for docstoolkit.message_router."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.message_router import (
    HandlerInfo,
    Message,
    MessagePriority,
    MessageRouter,
    RouterStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_message(topic: str = "test.topic", payload=None) -> Message:
    return Message(msg_id="m1", topic=topic, payload=payload)


# ---------------------------------------------------------------------------
# Enums / dataclasses
# ---------------------------------------------------------------------------


class TestMessagePriority:
    def test_has_critical(self):
        assert MessagePriority.CRITICAL is not None

    def test_has_high(self):
        assert MessagePriority.HIGH is not None

    def test_has_normal(self):
        assert MessagePriority.NORMAL is not None

    def test_has_low(self):
        assert MessagePriority.LOW is not None

    def test_priority_ordering(self):
        # value ordering: CRITICAL > HIGH > NORMAL > LOW
        assert MessagePriority.CRITICAL.value > MessagePriority.HIGH.value
        assert MessagePriority.HIGH.value > MessagePriority.NORMAL.value
        assert MessagePriority.NORMAL.value > MessagePriority.LOW.value


class TestMessage:
    def test_basic_construction(self):
        m = Message(msg_id="x", topic="t", payload={"a": 1})
        assert m.msg_id == "x"
        assert m.topic == "t"
        assert m.payload == {"a": 1}

    def test_default_priority_normal(self):
        m = Message(msg_id="x", topic="t", payload=None)
        assert m.priority == MessagePriority.NORMAL

    def test_default_headers_empty(self):
        m = Message(msg_id="x", topic="t", payload=None)
        assert m.headers == {}

    def test_default_timestamp_zero(self):
        m = Message(msg_id="x", topic="t", payload=None)
        assert m.timestamp == 0.0

    def test_custom_headers(self):
        m = Message(msg_id="x", topic="t", payload=None, headers={"k": "v"})
        assert m.headers["k"] == "v"


class TestHandlerInfo:
    def test_basic_construction(self):
        h = HandlerInfo(handler_id="h1", topic_pattern="users.*", handler=lambda m: None)
        assert h.handler_id == "h1"
        assert h.topic_pattern == "users.*"
        assert callable(h.handler)

    def test_default_priority_zero(self):
        h = HandlerInfo(handler_id="h", topic_pattern="t", handler=lambda m: None)
        assert h.priority == 0

    def test_custom_priority(self):
        h = HandlerInfo(handler_id="h", topic_pattern="t", handler=lambda m: None, priority=5)
        assert h.priority == 5


class TestRouterStats:
    def test_default_values(self):
        s = RouterStats()
        assert s.total_dispatched == 0
        assert s.total_handled == 0
        assert s.total_dropped == 0
        assert s.topics == {}

    def test_topic_counts(self):
        s = RouterStats(topics={"a": 2})
        assert s.topics["a"] == 2


# ---------------------------------------------------------------------------
# Subscribe / unsubscribe
# ---------------------------------------------------------------------------


class TestSubscribe:
    def test_returns_handler_id(self):
        r = MessageRouter()
        hid = r.subscribe("topic", lambda m: None)
        assert isinstance(hid, str) and hid

    def test_subscribers_count_increments(self):
        r = MessageRouter()
        assert r.subscribers_count == 0
        r.subscribe("a", lambda m: None)
        assert r.subscribers_count == 1
        r.subscribe("b", lambda m: None)
        assert r.subscribers_count == 2

    def test_subscribe_empty_pattern_raises(self):
        r = MessageRouter()
        with pytest.raises(ValueError):
            r.subscribe("", lambda m: None)

    def test_subscribe_non_callable_raises(self):
        r = MessageRouter()
        with pytest.raises(TypeError):
            r.subscribe("a", "not callable")  # type: ignore[arg-type]

    def test_subscribe_with_priority(self):
        r = MessageRouter()
        hid = r.subscribe("a", lambda m: None, priority=10)
        infos = r.handlers_for("a")
        assert infos[0].priority == 10
        assert infos[0].handler_id == hid


class TestUnsubscribe:
    def test_unsubscribe_existing(self):
        r = MessageRouter()
        hid = r.subscribe("a", lambda m: None)
        assert r.unsubscribe(hid) is True
        assert r.subscribers_count == 0

    def test_unsubscribe_missing_returns_false(self):
        r = MessageRouter()
        assert r.unsubscribe("missing") is False

    def test_unsubscribe_idempotent(self):
        r = MessageRouter()
        hid = r.subscribe("a", lambda m: None)
        r.unsubscribe(hid)
        assert r.unsubscribe(hid) is False


# ---------------------------------------------------------------------------
# Basic publish
# ---------------------------------------------------------------------------


class TestPublishBasic:
    def test_publish_invokes_handler(self):
        r = MessageRouter()
        received = []
        r.subscribe("hello", lambda m: received.append(m))
        invoked = r.publish("hello", {"x": 1})
        assert invoked == 1
        assert len(received) == 1
        assert received[0].topic == "hello"
        assert received[0].payload == {"x": 1}

    def test_publish_no_subscribers_returns_zero(self):
        r = MessageRouter()
        assert r.publish("nothing", None) == 0

    def test_publish_assigns_msg_id(self):
        r = MessageRouter()
        captured = []
        r.subscribe("t", lambda m: captured.append(m))
        r.publish("t", "payload")
        assert captured[0].msg_id

    def test_publish_message_directly(self):
        r = MessageRouter()
        captured = []
        r.subscribe("t", lambda m: captured.append(m))
        msg = Message(msg_id="custom", topic="t", payload="p")
        invoked = r.publish_message(msg)
        assert invoked == 1
        assert captured[0].msg_id == "custom"

    def test_publish_propagates_priority(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))
        r.publish("t", None, priority=MessagePriority.CRITICAL)
        assert seen[0].priority == MessagePriority.CRITICAL

    def test_publish_headers_copied(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))
        headers = {"a": "b"}
        r.publish("t", None, headers=headers)
        assert seen[0].headers == {"a": "b"}
        # mutating original should not affect message
        headers["a"] = "z"
        assert seen[0].headers == {"a": "b"}


# ---------------------------------------------------------------------------
# Topic matching
# ---------------------------------------------------------------------------


class TestTopicExact:
    def test_exact_match(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.created", lambda m: seen.append(m))
        r.publish("users.created", None)
        assert len(seen) == 1

    def test_different_topic_skipped(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.created", lambda m: seen.append(m))
        r.publish("users.deleted", None)
        assert seen == []

    def test_topic_segment_difference(self):
        r = MessageRouter()
        seen = []
        r.subscribe("a.b.c", lambda m: seen.append(m))
        r.publish("a.b", None)
        assert seen == []


class TestTopicSingleWildcard:
    def test_star_matches_single_segment(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.*", lambda m: seen.append(m))
        r.publish("users.created", None)
        r.publish("users.updated", None)
        assert len(seen) == 2

    def test_star_does_not_match_multi_segment(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.*", lambda m: seen.append(m))
        r.publish("users.profile.created", None)
        assert seen == []

    def test_bare_star_matches_any_single_segment(self):
        r = MessageRouter()
        seen = []
        r.subscribe("*", lambda m: seen.append(m))
        r.publish("anything", None)
        r.publish("else", None)
        r.publish("two.parts", None)
        assert len(seen) == 2

    def test_star_in_middle(self):
        r = MessageRouter()
        seen = []
        r.subscribe("a.*.c", lambda m: seen.append(m))
        r.publish("a.b.c", None)
        r.publish("a.x.c", None)
        r.publish("a.b.d", None)
        assert len(seen) == 2


class TestTopicMultiWildcard:
    def test_hash_matches_single_trailing(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.#", lambda m: seen.append(m))
        r.publish("users.created", None)
        assert len(seen) == 1

    def test_hash_matches_many_trailing(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.#", lambda m: seen.append(m))
        r.publish("users.profile.created", None)
        r.publish("users.profile.updates.name", None)
        assert len(seen) == 2

    def test_hash_does_not_match_root(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.#", lambda m: seen.append(m))
        # 'users' alone has no trailing segments after the prefix
        r.publish("users", None)
        assert seen == []

    def test_hash_unaffected_by_other_prefix(self):
        r = MessageRouter()
        seen = []
        r.subscribe("users.#", lambda m: seen.append(m))
        r.publish("orders.created", None)
        assert seen == []


# ---------------------------------------------------------------------------
# Handler priority
# ---------------------------------------------------------------------------


class TestHandlerPriority:
    def test_higher_priority_first(self):
        r = MessageRouter()
        order = []
        r.subscribe("t", lambda m: order.append("low"), priority=1)
        r.subscribe("t", lambda m: order.append("high"), priority=10)
        r.subscribe("t", lambda m: order.append("mid"), priority=5)
        r.publish("t", None)
        assert order == ["high", "mid", "low"]

    def test_equal_priority_runs_all(self):
        r = MessageRouter()
        count = [0]
        r.subscribe("t", lambda m: count.__setitem__(0, count[0] + 1), priority=0)
        r.subscribe("t", lambda m: count.__setitem__(0, count[0] + 1), priority=0)
        r.publish("t", None)
        assert count[0] == 2

    def test_negative_priority(self):
        r = MessageRouter()
        order = []
        r.subscribe("t", lambda m: order.append("neg"), priority=-5)
        r.subscribe("t", lambda m: order.append("zero"), priority=0)
        r.publish("t", None)
        assert order == ["zero", "neg"]


# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------


class TestMiddleware:
    def test_middleware_can_transform_payload(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))

        def upper_mw(msg):
            msg.payload = msg.payload.upper()
            return msg

        r.add_middleware(upper_mw)
        r.publish("t", "hello")
        assert seen[0].payload == "HELLO"

    def test_multiple_middleware_run_in_order(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))

        def first(msg):
            msg.headers["chain"] = "first"
            return msg

        def second(msg):
            msg.headers["chain"] += ",second"
            return msg

        r.add_middleware(first)
        r.add_middleware(second)
        r.publish("t", None)
        assert seen[0].headers["chain"] == "first,second"

    def test_add_middleware_returns_id(self):
        r = MessageRouter()
        mw_id = r.add_middleware(lambda m: m)
        assert isinstance(mw_id, int)

    def test_remove_middleware(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))

        mw_id = r.add_middleware(lambda m: None)
        assert r.remove_middleware(mw_id) is True
        r.publish("t", None)
        assert len(seen) == 1

    def test_remove_missing_middleware_returns_false(self):
        r = MessageRouter()
        assert r.remove_middleware(999) is False

    def test_non_callable_middleware_raises(self):
        r = MessageRouter()
        with pytest.raises(TypeError):
            r.add_middleware("not callable")  # type: ignore[arg-type]


class TestMiddlewareDrop:
    def test_returning_none_drops_message(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))
        r.add_middleware(lambda m: None)
        invoked = r.publish("t", None)
        assert invoked == 0
        assert seen == []

    def test_dropped_message_counted_in_stats(self):
        r = MessageRouter()
        r.add_middleware(lambda m: None)
        r.publish("t", None)
        assert r.stats().total_dropped == 1

    def test_middleware_exception_drops_message(self):
        r = MessageRouter()
        seen = []
        r.subscribe("t", lambda m: seen.append(m))

        def bad(msg):
            raise RuntimeError("boom")

        r.add_middleware(bad)
        invoked = r.publish("t", None)
        assert invoked == 0
        assert seen == []
        assert r.stats().total_dropped == 1


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_initial_stats_empty(self):
        r = MessageRouter()
        s = r.stats()
        assert s.total_dispatched == 0
        assert s.total_handled == 0
        assert s.total_dropped == 0

    def test_dispatched_increments(self):
        r = MessageRouter()
        r.publish("a", None)
        r.publish("b", None)
        assert r.stats().total_dispatched == 2

    def test_handled_counts_invocations(self):
        r = MessageRouter()
        r.subscribe("t", lambda m: None)
        r.subscribe("t", lambda m: None)
        r.publish("t", None)
        assert r.stats().total_handled == 2

    def test_topic_counts(self):
        r = MessageRouter()
        r.publish("a", None)
        r.publish("a", None)
        r.publish("b", None)
        s = r.stats()
        assert s.topics["a"] == 2
        assert s.topics["b"] == 1

    def test_stats_is_snapshot(self):
        r = MessageRouter()
        r.publish("a", None)
        snap = r.stats()
        r.publish("a", None)
        # earlier snapshot unchanged
        assert snap.total_dispatched == 1

    def test_topic_count_property(self):
        r = MessageRouter()
        assert r.topic_count == 0
        r.publish("a", None)
        r.publish("b", None)
        r.publish("a", None)
        assert r.topic_count == 2


# ---------------------------------------------------------------------------
# handlers_for
# ---------------------------------------------------------------------------


class TestHandlersFor:
    def test_returns_matching_handlers(self):
        r = MessageRouter()
        r.subscribe("users.*", lambda m: None)
        r.subscribe("users.#", lambda m: None)
        r.subscribe("orders.*", lambda m: None)
        infos = r.handlers_for("users.created")
        assert len(infos) == 2

    def test_returns_empty_when_no_match(self):
        r = MessageRouter()
        r.subscribe("users.*", lambda m: None)
        assert r.handlers_for("orders.created") == []

    def test_sorted_by_priority(self):
        r = MessageRouter()
        r.subscribe("t", lambda m: None, priority=1)
        r.subscribe("t", lambda m: None, priority=9)
        r.subscribe("t", lambda m: None, priority=5)
        infos = r.handlers_for("t")
        priorities = [h.priority for h in infos]
        assert priorities == sorted(priorities, reverse=True)


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_removes_handlers(self):
        r = MessageRouter()
        r.subscribe("a", lambda m: None)
        r.clear()
        assert r.subscribers_count == 0

    def test_clear_removes_middleware(self):
        r = MessageRouter()
        seen = []
        r.add_middleware(lambda m: None)
        r.subscribe("t", lambda m: seen.append(m))
        r.clear()
        r.subscribe("t", lambda m: seen.append(m))
        r.publish("t", None)
        # middleware no longer drops
        assert len(seen) == 1

    def test_clear_resets_stats(self):
        r = MessageRouter()
        r.publish("a", None)
        r.clear()
        s = r.stats()
        assert s.total_dispatched == 0
        assert s.topics == {}

    def test_clear_resets_topic_count(self):
        r = MessageRouter()
        r.publish("a", None)
        r.clear()
        assert r.topic_count == 0


# ---------------------------------------------------------------------------
# Handler errors
# ---------------------------------------------------------------------------


class TestHandlerError:
    def test_handler_exception_does_not_stop_others(self):
        r = MessageRouter()
        seen = []

        def bad(m):
            raise RuntimeError("boom")

        r.subscribe("t", bad, priority=10)
        r.subscribe("t", lambda m: seen.append("ok"), priority=1)
        invoked = r.publish("t", None)
        assert invoked == 2
        assert seen == ["ok"]

    def test_handler_exception_counted_as_handled(self):
        r = MessageRouter()
        r.subscribe("t", lambda m: (_ for _ in ()).throw(RuntimeError("x")))
        r.publish("t", None)
        assert r.stats().total_handled == 1


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_publish_without_subscribers_or_middleware(self):
        r = MessageRouter()
        assert r.publish("t", None) == 0
        assert r.stats().total_dispatched == 1
        assert r.stats().total_handled == 0
        assert r.stats().total_dropped == 0

    def test_publish_after_unsubscribe(self):
        r = MessageRouter()
        seen = []
        hid = r.subscribe("t", lambda m: seen.append(m))
        r.unsubscribe(hid)
        r.publish("t", None)
        assert seen == []

    def test_concurrent_publish_safe(self):
        r = MessageRouter()
        seen = []
        lock = threading.Lock()

        def handler(m):
            with lock:
                seen.append(m.payload)

        r.subscribe("t", handler)

        def worker(start, end):
            for i in range(start, end):
                r.publish("t", i)

        threads = [threading.Thread(target=worker, args=(i * 25, (i + 1) * 25)) for i in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(seen) == 100

    def test_subscribe_during_publish_does_not_break(self):
        # Snapshot semantics: a subscription added inside a handler
        # should NOT receive the in-flight message.
        r = MessageRouter()
        seen = []

        def first(m):
            r.subscribe("t", lambda m2: seen.append("late"))

        r.subscribe("t", first)
        r.publish("t", None)
        assert seen == []

    def test_publish_message_uses_existing_topic(self):
        r = MessageRouter()
        seen = []
        r.subscribe("custom.topic", lambda m: seen.append(m))
        m = Message(msg_id="abc", topic="custom.topic", payload="p")
        r.publish_message(m)
        assert len(seen) == 1

    def test_handlers_for_empty_router(self):
        r = MessageRouter()
        assert r.handlers_for("anything") == []
