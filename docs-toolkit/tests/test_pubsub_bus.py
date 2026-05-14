"""Comprehensive tests for the pubsub_bus module (E90).

Coverage targets:
- Message dataclass defaults & explicit values
- PubSubBus.subscribe / unsubscribe / clear
- publish & publish_message (exact, wildcard *, wildcard **)
- filter callbacks (accept/reject/raises)
- multiple subscribers on the same topic
- introspection: topics, subscription_count
- MessageHistory: record, get_topic newest-first, count_topic, clear, max_size
"""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.pubsub_bus import (
    Message,
    MessageHistory,
    PubSubBus,
    Subscription,
)
from docstoolkit.pubsub_bus.bus import _match_topic


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

class Recorder:
    """Test helper — records every message it receives."""

    def __init__(self):
        self.received = []

    def __call__(self, message):
        self.received.append(message)


# ===========================================================================
# 1. Message dataclass
# ===========================================================================

class TestMessage:
    def test_default_message_id_present(self):
        m = Message(topic="x", payload=1)
        assert m.message_id

    def test_default_message_id_length(self):
        m = Message(topic="x", payload=1)
        assert len(m.message_id) == 12

    def test_default_message_id_is_string(self):
        m = Message(topic="x", payload=1)
        assert isinstance(m.message_id, str)

    def test_default_message_id_is_hex(self):
        m = Message(topic="x", payload=1)
        int(m.message_id, 16)

    def test_default_message_ids_unique(self):
        a = Message(topic="x", payload=1)
        b = Message(topic="x", payload=1)
        assert a.message_id != b.message_id

    def test_default_timestamp_is_float(self):
        m = Message(topic="x", payload=1)
        assert isinstance(m.timestamp, float)

    def test_default_timestamp_recent(self):
        before = time.time()
        m = Message(topic="x", payload=1)
        after = time.time()
        assert before <= m.timestamp <= after

    def test_default_headers_dict(self):
        m = Message(topic="x", payload=1)
        assert m.headers == {}

    def test_default_headers_is_dict_type(self):
        m = Message(topic="x", payload=1)
        assert isinstance(m.headers, dict)

    def test_default_headers_independent(self):
        a = Message(topic="x", payload=1)
        b = Message(topic="x", payload=1)
        a.headers["k"] = "v"
        assert b.headers == {}

    def test_explicit_topic(self):
        m = Message(topic="orders.created", payload=None)
        assert m.topic == "orders.created"

    def test_explicit_payload_dict(self):
        m = Message(topic="x", payload={"k": 1})
        assert m.payload == {"k": 1}

    def test_explicit_payload_list(self):
        m = Message(topic="x", payload=[1, 2, 3])
        assert m.payload == [1, 2, 3]

    def test_explicit_payload_none(self):
        m = Message(topic="x", payload=None)
        assert m.payload is None

    def test_explicit_payload_str(self):
        m = Message(topic="x", payload="hello")
        assert m.payload == "hello"

    def test_explicit_message_id(self):
        m = Message(topic="x", payload=None, message_id="abc123")
        assert m.message_id == "abc123"

    def test_explicit_headers(self):
        m = Message(topic="x", payload=None, headers={"trace": "t-1"})
        assert m.headers == {"trace": "t-1"}

    def test_explicit_timestamp(self):
        m = Message(topic="x", payload=None, timestamp=42.0)
        assert m.timestamp == 42.0


# ===========================================================================
# 2. Topic-matching primitive
# ===========================================================================

class TestTopicMatch:
    def test_exact_single_segment(self):
        assert _match_topic("a", "a") is True

    def test_exact_multi_segment(self):
        assert _match_topic("users.created", "users.created") is True

    def test_mismatch_segment(self):
        assert _match_topic("users.created", "users.updated") is False

    def test_mismatch_length(self):
        assert _match_topic("users.created", "users") is False

    def test_star_matches_one_segment(self):
        assert _match_topic("users.*", "users.created") is True

    def test_star_does_not_match_multi(self):
        assert _match_topic("users.*", "users.profile.updated") is False

    def test_star_does_not_match_zero(self):
        assert _match_topic("users.*", "users") is False

    def test_double_star_matches_multi(self):
        assert _match_topic("users.**", "users.profile.updated") is True

    def test_double_star_matches_single(self):
        assert _match_topic("users.**", "users.created") is True

    def test_double_star_matches_zero(self):
        assert _match_topic("users.**", "users") is True

    def test_double_star_no_prefix_match(self):
        assert _match_topic("users.**", "orders.created") is False

    def test_star_mid_pattern(self):
        assert _match_topic("a.*.c", "a.b.c") is True

    def test_star_mid_pattern_mismatch_tail(self):
        assert _match_topic("a.*.c", "a.b.d") is False

    def test_double_star_mid_pattern(self):
        assert _match_topic("a.**.c", "a.b.x.y.c") is True

    def test_double_star_mid_pattern_zero(self):
        assert _match_topic("a.**.c", "a.c") is True

    def test_double_star_mid_no_match(self):
        assert _match_topic("a.**.c", "a.b.x") is False

    def test_leading_double_star(self):
        assert _match_topic("**.created", "users.created") is True

    def test_leading_double_star_multi(self):
        assert _match_topic("**.created", "users.profile.created") is True

    def test_leading_double_star_no_match(self):
        assert _match_topic("**.created", "users.updated") is False

    def test_only_double_star(self):
        assert _match_topic("**", "anything.deep.nested") is True

    def test_only_star_single(self):
        assert _match_topic("*", "anything") is True

    def test_only_star_multi(self):
        assert _match_topic("*", "a.b") is False

    def test_consecutive_double_star(self):
        assert _match_topic("a.**.**.b", "a.x.y.b") is True


# ===========================================================================
# 3. Subscription dataclass
# ===========================================================================

class TestSubscription:
    def test_construct(self):
        s = Subscription("id-1", "x.y", lambda m: None)
        assert s.subscription_id == "id-1"
        assert s.topic_pattern == "x.y"
        assert callable(s.callback)
        assert s.filter is None

    def test_filter_default_none(self):
        s = Subscription("id", "t", lambda m: None)
        assert s.filter is None

    def test_filter_explicit(self):
        f = lambda m: True
        s = Subscription("id", "t", lambda m: None, filter=f)
        assert s.filter is f


# ===========================================================================
# 4. PubSubBus subscribe / unsubscribe
# ===========================================================================

class TestSubscribeUnsubscribe:
    def test_subscribe_returns_string_id(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None)
        assert isinstance(sub_id, str) and sub_id

    def test_subscribe_unique_ids(self):
        bus = PubSubBus()
        a = bus.subscribe("x", lambda m: None)
        b = bus.subscribe("x", lambda m: None)
        assert a != b

    def test_subscribe_increases_count(self):
        bus = PubSubBus()
        assert bus.subscription_count() == 0
        bus.subscribe("x", lambda m: None)
        assert bus.subscription_count() == 1
        bus.subscribe("y", lambda m: None)
        assert bus.subscription_count() == 2

    def test_unsubscribe_existing(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None)
        assert bus.unsubscribe(sub_id) is True

    def test_unsubscribe_missing(self):
        bus = PubSubBus()
        assert bus.unsubscribe("does-not-exist") is False

    def test_unsubscribe_decreases_count(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None)
        bus.unsubscribe(sub_id)
        assert bus.subscription_count() == 0

    def test_unsubscribe_twice(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None)
        assert bus.unsubscribe(sub_id) is True
        assert bus.unsubscribe(sub_id) is False

    def test_subscribe_rejects_non_callable(self):
        bus = PubSubBus()
        with pytest.raises(TypeError):
            bus.subscribe("x", "not-callable")

    def test_subscribe_rejects_non_callable_filter(self):
        bus = PubSubBus()
        with pytest.raises(TypeError):
            bus.subscribe("x", lambda m: None, filter="not-callable")

    def test_subscribe_accepts_none_filter(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None, filter=None)
        assert sub_id

    def test_subscribe_accepts_callable_filter(self):
        bus = PubSubBus()
        sub_id = bus.subscribe("x", lambda m: None, filter=lambda m: True)
        assert sub_id

    def test_unsubscribe_after_publish_stops_delivery(self):
        bus = PubSubBus()
        rec = Recorder()
        sub_id = bus.subscribe("x", rec)
        bus.publish("x", payload=1)
        bus.unsubscribe(sub_id)
        bus.publish("x", payload=2)
        assert len(rec.received) == 1


# ===========================================================================
# 5. Publish — exact matches
# ===========================================================================

class TestPublishExact:
    def test_publish_returns_int(self):
        bus = PubSubBus()
        bus.subscribe("x", lambda m: None)
        assert isinstance(bus.publish("x", payload=1), int)

    def test_publish_delivers_to_exact(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload=1)
        assert len(rec.received) == 1

    def test_publish_no_subscribers_returns_zero(self):
        bus = PubSubBus()
        assert bus.publish("x", payload=1) == 0

    def test_publish_no_match_returns_zero(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a", rec)
        assert bus.publish("b", payload=1) == 0
        assert rec.received == []

    def test_publish_payload_preserved(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload={"k": "v"})
        assert rec.received[0].payload == {"k": "v"}

    def test_publish_topic_preserved(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("orders.created", rec)
        bus.publish("orders.created", payload=None)
        assert rec.received[0].topic == "orders.created"

    def test_publish_headers_default_empty(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload=None)
        assert rec.received[0].headers == {}

    def test_publish_headers_propagated(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload=None, headers={"trace": "abc"})
        assert rec.received[0].headers == {"trace": "abc"}

    def test_publish_headers_copy(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        h = {"trace": "abc"}
        bus.publish("x", payload=None, headers=h)
        h["trace"] = "changed"
        assert rec.received[0].headers["trace"] == "abc"

    def test_publish_each_message_has_id(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload=1)
        bus.publish("x", payload=2)
        assert rec.received[0].message_id != rec.received[1].message_id

    def test_publish_message_is_Message_instance(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        bus.publish("x", payload=1)
        assert isinstance(rec.received[0], Message)

    def test_publish_swallows_callback_exception(self):
        bus = PubSubBus()

        def bad(m):
            raise RuntimeError("boom")

        bus.subscribe("x", bad)
        # Should not raise.
        delivered = bus.publish("x", payload=1)
        # Exception-raising callback is NOT counted as delivered.
        assert delivered == 0

    def test_publish_other_subs_still_run_after_exception(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", lambda m: (_ for _ in ()).throw(RuntimeError("boom")))
        bus.subscribe("x", rec)
        bus.publish("x", payload=1)
        assert len(rec.received) == 1


# ===========================================================================
# 6. Publish — wildcard *
# ===========================================================================

class TestPublishWildcardSingle:
    def test_star_matches_one(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.*", rec)
        bus.publish("users.created", payload=None)
        assert len(rec.received) == 1

    def test_star_does_not_match_deeper(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.*", rec)
        bus.publish("users.profile.updated", payload=None)
        assert rec.received == []

    def test_star_does_not_match_shorter(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.*", rec)
        bus.publish("users", payload=None)
        assert rec.received == []

    def test_star_mid_pattern_matches(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a.*.c", rec)
        bus.publish("a.b.c", payload=None)
        assert len(rec.received) == 1

    def test_star_mid_pattern_mismatch(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a.*.c", rec)
        bus.publish("a.b.d", payload=None)
        assert rec.received == []

    def test_only_star_matches_one_segment(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("*", rec)
        bus.publish("foo", payload=None)
        assert len(rec.received) == 1

    def test_only_star_does_not_match_two_segments(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("*", rec)
        bus.publish("foo.bar", payload=None)
        assert rec.received == []


# ===========================================================================
# 7. Publish — wildcard **
# ===========================================================================

class TestPublishWildcardMulti:
    def test_double_star_matches_one_segment(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.**", rec)
        bus.publish("users.created", payload=None)
        assert len(rec.received) == 1

    def test_double_star_matches_multiple_segments(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.**", rec)
        bus.publish("users.profile.updated", payload=None)
        assert len(rec.received) == 1

    def test_double_star_matches_zero(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.**", rec)
        bus.publish("users", payload=None)
        assert len(rec.received) == 1

    def test_double_star_prefix_mismatch(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.**", rec)
        bus.publish("orders.created", payload=None)
        assert rec.received == []

    def test_only_double_star_matches_everything(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("**", rec)
        bus.publish("a", payload=None)
        bus.publish("a.b", payload=None)
        bus.publish("a.b.c", payload=None)
        assert len(rec.received) == 3

    def test_double_star_in_middle(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a.**.z", rec)
        bus.publish("a.b.c.d.z", payload=None)
        assert len(rec.received) == 1

    def test_double_star_in_middle_zero_middle(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a.**.z", rec)
        bus.publish("a.z", payload=None)
        assert len(rec.received) == 1

    def test_double_star_in_middle_mismatch_suffix(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("a.**.z", rec)
        bus.publish("a.b.c", payload=None)
        assert rec.received == []

    def test_leading_double_star(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("**.created", rec)
        bus.publish("users.created", payload=None)
        bus.publish("orders.payments.created", payload=None)
        assert len(rec.received) == 2


# ===========================================================================
# 8. Filter callbacks
# ===========================================================================

class TestFilter:
    def test_filter_accepts_message(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: True)
        bus.publish("x", payload=1)
        assert len(rec.received) == 1

    def test_filter_rejects_message(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: False)
        bus.publish("x", payload=1)
        assert rec.received == []

    def test_filter_rejection_returns_zero_delivered(self):
        bus = PubSubBus()
        bus.subscribe("x", lambda m: None, filter=lambda m: False)
        assert bus.publish("x", payload=1) == 0

    def test_filter_uses_payload(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: m.payload == "ok")
        bus.publish("x", payload="ok")
        bus.publish("x", payload="nope")
        assert len(rec.received) == 1
        assert rec.received[0].payload == "ok"

    def test_filter_uses_headers(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: m.headers.get("env") == "prod")
        bus.publish("x", payload=None, headers={"env": "prod"})
        bus.publish("x", payload=None, headers={"env": "dev"})
        assert len(rec.received) == 1

    def test_filter_exception_skips_delivery(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: (_ for _ in ()).throw(RuntimeError("bad")))
        delivered = bus.publish("x", payload=1)
        assert delivered == 0
        assert rec.received == []

    def test_filter_per_subscriber_independent(self):
        bus = PubSubBus()
        a = Recorder()
        b = Recorder()
        bus.subscribe("x", a, filter=lambda m: m.payload > 0)
        bus.subscribe("x", b, filter=lambda m: m.payload < 0)
        bus.publish("x", payload=5)
        bus.publish("x", payload=-3)
        assert len(a.received) == 1 and a.received[0].payload == 5
        assert len(b.received) == 1 and b.received[0].payload == -3


# ===========================================================================
# 9. Multiple subscribers
# ===========================================================================

class TestMultipleSubscribers:
    def test_all_receive_same_message(self):
        bus = PubSubBus()
        a = Recorder()
        b = Recorder()
        bus.subscribe("x", a)
        bus.subscribe("x", b)
        bus.publish("x", payload=1)
        assert len(a.received) == 1
        assert len(b.received) == 1

    def test_publish_returns_count(self):
        bus = PubSubBus()
        bus.subscribe("x", lambda m: None)
        bus.subscribe("x", lambda m: None)
        bus.subscribe("x", lambda m: None)
        assert bus.publish("x", payload=1) == 3

    def test_mixed_patterns_delivered_correctly(self):
        bus = PubSubBus()
        exact = Recorder()
        single = Recorder()
        multi = Recorder()
        bus.subscribe("users.created", exact)
        bus.subscribe("users.*", single)
        bus.subscribe("users.**", multi)
        bus.publish("users.created", payload=None)
        assert len(exact.received) == 1
        assert len(single.received) == 1
        assert len(multi.received) == 1

    def test_only_matching_subscribers_invoked(self):
        bus = PubSubBus()
        a = Recorder()
        b = Recorder()
        bus.subscribe("users.created", a)
        bus.subscribe("orders.created", b)
        bus.publish("users.created", payload=None)
        assert len(a.received) == 1
        assert b.received == []


# ===========================================================================
# 10. publish_message
# ===========================================================================

class TestPublishMessage:
    def test_publish_message_basic(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        msg = Message(topic="x", payload="hi")
        bus.publish_message(msg)
        assert len(rec.received) == 1

    def test_publish_message_preserves_id(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        msg = Message(topic="x", payload=None, message_id="fixed-id")
        bus.publish_message(msg)
        assert rec.received[0].message_id == "fixed-id"

    def test_publish_message_preserves_timestamp(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        msg = Message(topic="x", payload=None, timestamp=123.0)
        bus.publish_message(msg)
        assert rec.received[0].timestamp == 123.0

    def test_publish_message_preserves_headers(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec)
        msg = Message(topic="x", payload=None, headers={"a": "b"})
        bus.publish_message(msg)
        assert rec.received[0].headers == {"a": "b"}

    def test_publish_message_returns_int(self):
        bus = PubSubBus()
        bus.subscribe("x", lambda m: None)
        msg = Message(topic="x", payload=None)
        assert isinstance(bus.publish_message(msg), int)

    def test_publish_message_no_subscribers(self):
        bus = PubSubBus()
        msg = Message(topic="x", payload=None)
        assert bus.publish_message(msg) == 0

    def test_publish_message_wildcard_match(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("users.**", rec)
        bus.publish_message(Message(topic="users.profile.changed", payload=None))
        assert len(rec.received) == 1

    def test_publish_message_filter_rejects(self):
        bus = PubSubBus()
        rec = Recorder()
        bus.subscribe("x", rec, filter=lambda m: False)
        bus.publish_message(Message(topic="x", payload=None))
        assert rec.received == []


# ===========================================================================
# 11. topics / subscription_count / clear
# ===========================================================================

class TestIntrospection:
    def test_topics_empty(self):
        bus = PubSubBus()
        assert bus.topics() == set()

    def test_topics_distinct(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        bus.subscribe("b", lambda m: None)
        bus.subscribe("a", lambda m: None)  # duplicate pattern
        assert bus.topics() == {"a", "b"}

    def test_topics_returns_set(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        assert isinstance(bus.topics(), set)

    def test_subscription_count_zero(self):
        bus = PubSubBus()
        assert bus.subscription_count() == 0

    def test_subscription_count_global(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        bus.subscribe("b", lambda m: None)
        assert bus.subscription_count() == 2

    def test_subscription_count_by_pattern(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        bus.subscribe("a", lambda m: None)
        bus.subscribe("b", lambda m: None)
        assert bus.subscription_count("a") == 2
        assert bus.subscription_count("b") == 1

    def test_subscription_count_unknown_pattern(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        assert bus.subscription_count("nope") == 0

    def test_clear_removes_all(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        bus.subscribe("b", lambda m: None)
        bus.clear()
        assert bus.subscription_count() == 0
        assert bus.topics() == set()

    def test_clear_then_publish_zero(self):
        bus = PubSubBus()
        bus.subscribe("a", lambda m: None)
        bus.clear()
        assert bus.publish("a", payload=None) == 0

    def test_clear_returns_none(self):
        bus = PubSubBus()
        assert bus.clear() is None


# ===========================================================================
# 12. MessageHistory
# ===========================================================================

class TestMessageHistory:
    def test_default_max_size(self):
        h = MessageHistory()
        assert h.max_size == 1000

    def test_custom_max_size(self):
        h = MessageHistory(max_size=50)
        assert h.max_size == 50

    def test_invalid_max_size_zero(self):
        with pytest.raises(ValueError):
            MessageHistory(max_size=0)

    def test_invalid_max_size_negative(self):
        with pytest.raises(ValueError):
            MessageHistory(max_size=-1)

    def test_record_increases_count(self):
        h = MessageHistory()
        h.record(Message(topic="x", payload=1))
        assert h.count_topic("x") == 1

    def test_record_multiple(self):
        h = MessageHistory()
        for i in range(5):
            h.record(Message(topic="x", payload=i))
        assert h.count_topic("x") == 5

    def test_record_requires_message(self):
        h = MessageHistory()
        with pytest.raises(TypeError):
            h.record("not-a-message")

    def test_record_per_topic_independent(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        h.record(Message(topic="b", payload=2))
        h.record(Message(topic="b", payload=3))
        assert h.count_topic("a") == 1
        assert h.count_topic("b") == 2

    def test_get_topic_empty_returns_list(self):
        h = MessageHistory()
        assert h.get_topic("x") == []

    def test_get_topic_returns_list(self):
        h = MessageHistory()
        h.record(Message(topic="x", payload=1))
        assert isinstance(h.get_topic("x"), list)

    def test_get_topic_newest_first(self):
        h = MessageHistory()
        for i in range(3):
            h.record(Message(topic="x", payload=i))
        items = h.get_topic("x")
        assert [m.payload for m in items] == [2, 1, 0]

    def test_get_topic_default_limit_100(self):
        h = MessageHistory()
        for i in range(150):
            h.record(Message(topic="x", payload=i))
        items = h.get_topic("x")
        assert len(items) == 100

    def test_get_topic_explicit_limit(self):
        h = MessageHistory()
        for i in range(20):
            h.record(Message(topic="x", payload=i))
        items = h.get_topic("x", limit=5)
        assert len(items) == 5

    def test_get_topic_limit_zero(self):
        h = MessageHistory()
        h.record(Message(topic="x", payload=1))
        assert h.get_topic("x", limit=0) == []

    def test_get_topic_limit_negative(self):
        h = MessageHistory()
        h.record(Message(topic="x", payload=1))
        assert h.get_topic("x", limit=-5) == []

    def test_get_topic_limit_larger_than_available(self):
        h = MessageHistory()
        for i in range(3):
            h.record(Message(topic="x", payload=i))
        assert len(h.get_topic("x", limit=100)) == 3

    def test_get_topic_unknown_topic(self):
        h = MessageHistory()
        h.record(Message(topic="x", payload=1))
        assert h.get_topic("y") == []

    def test_get_topic_only_returns_topic(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        h.record(Message(topic="b", payload=2))
        out = h.get_topic("a")
        assert all(m.topic == "a" for m in out)

    def test_max_size_cap(self):
        h = MessageHistory(max_size=3)
        for i in range(10):
            h.record(Message(topic="x", payload=i))
        assert h.count_topic("x") == 3

    def test_max_size_keeps_newest(self):
        h = MessageHistory(max_size=3)
        for i in range(10):
            h.record(Message(topic="x", payload=i))
        items = h.get_topic("x")
        # newest first
        assert [m.payload for m in items] == [9, 8, 7]

    def test_max_size_per_topic_independent(self):
        h = MessageHistory(max_size=2)
        for i in range(5):
            h.record(Message(topic="a", payload=i))
        for i in range(3):
            h.record(Message(topic="b", payload=i))
        assert h.count_topic("a") == 2
        assert h.count_topic("b") == 2

    def test_count_topic_unknown(self):
        h = MessageHistory()
        assert h.count_topic("never") == 0

    def test_clear_all(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        h.record(Message(topic="b", payload=2))
        h.clear()
        assert h.count_topic("a") == 0
        assert h.count_topic("b") == 0
        assert h.all_topics() == []

    def test_clear_specific(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        h.record(Message(topic="b", payload=2))
        h.clear(topic="a")
        assert h.count_topic("a") == 0
        assert h.count_topic("b") == 1

    def test_clear_specific_unknown(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        # Should not raise.
        h.clear(topic="does-not-exist")
        assert h.count_topic("a") == 1

    def test_clear_returns_none(self):
        h = MessageHistory()
        assert h.clear() is None

    def test_all_topics_empty(self):
        h = MessageHistory()
        assert h.all_topics() == []

    def test_all_topics_returns_list(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        assert isinstance(h.all_topics(), list)

    def test_all_topics_contains_each(self):
        h = MessageHistory()
        h.record(Message(topic="a", payload=1))
        h.record(Message(topic="b", payload=1))
        h.record(Message(topic="a", payload=2))
        topics = h.all_topics()
        assert set(topics) == {"a", "b"}

    def test_history_integration_with_bus(self):
        """Use MessageHistory as a bus subscriber."""
        bus = PubSubBus()
        hist = MessageHistory(max_size=10)
        bus.subscribe("**", hist.record)
        bus.publish("users.created", payload={"id": 1})
        bus.publish("orders.placed", payload={"id": 2})
        assert hist.count_topic("users.created") == 1
        assert hist.count_topic("orders.placed") == 1


# ===========================================================================
# 13. Threading / concurrency
# ===========================================================================

class TestThreading:
    def test_concurrent_publish(self):
        bus = PubSubBus()
        rec = Recorder()
        lock = threading.Lock()

        def safe_callback(m):
            with lock:
                rec.received.append(m)

        bus.subscribe("x", safe_callback)

        def worker():
            for _ in range(100):
                bus.publish("x", payload=1)

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(rec.received) == 400

    def test_concurrent_subscribe_unsubscribe(self):
        bus = PubSubBus()
        ids = []
        ids_lock = threading.Lock()

        def adder():
            for _ in range(50):
                sub_id = bus.subscribe("x", lambda m: None)
                with ids_lock:
                    ids.append(sub_id)

        threads = [threading.Thread(target=adder) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert bus.subscription_count() == 200
        # Now unsubscribe in parallel.
        def remover(slice_ids):
            for sid in slice_ids:
                bus.unsubscribe(sid)
        chunks = [ids[i::4] for i in range(4)]
        threads = [threading.Thread(target=remover, args=(c,)) for c in chunks]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert bus.subscription_count() == 0

    def test_history_thread_safe(self):
        hist = MessageHistory(max_size=10_000)

        def worker(prefix):
            for i in range(200):
                hist.record(Message(topic=f"t.{prefix}", payload=i))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        total = sum(hist.count_topic(f"t.{i}") for i in range(5))
        assert total == 1000
