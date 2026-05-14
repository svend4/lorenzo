"""Tests for E338 DocPubSubBus."""

from __future__ import annotations

import threading
import time
import uuid

import pytest

from docstoolkit.doc_pubsub_bus import (
    DocPubSubBus,
    PubSubEvent,
    PubSubStats,
    SubscriberInfo,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestPubSubEventDataclass:
    def test_defaults(self):
        ev = PubSubEvent()
        assert ev.event_id == 0
        assert ev.event_type == ""
        assert ev.doc_id is None
        assert ev.payload == {}
        assert ev.published_at == 0.0

    def test_explicit_fields(self):
        ev = PubSubEvent(event_id=5, event_type="created", doc_id="d1", payload={"k": 1}, published_at=10.5)
        assert ev.event_id == 5
        assert ev.event_type == "created"
        assert ev.doc_id == "d1"
        assert ev.payload == {"k": 1}
        assert ev.published_at == 10.5

    def test_payload_is_independent_per_instance(self):
        a = PubSubEvent()
        b = PubSubEvent()
        a.payload["x"] = 1
        assert b.payload == {}

    def test_equality(self):
        a = PubSubEvent(event_id=1, event_type="t", doc_id="d", payload={"a": 1}, published_at=1.0)
        b = PubSubEvent(event_id=1, event_type="t", doc_id="d", payload={"a": 1}, published_at=1.0)
        assert a == b


class TestSubscriberInfoDataclass:
    def test_defaults(self):
        info = SubscriberInfo()
        assert info.sub_id == ""
        assert info.event_pattern == ""
        assert info.subscribed_at == 0.0
        assert info.delivery_count == 0

    def test_explicit_fields(self):
        info = SubscriberInfo(sub_id="abc", event_pattern="*", subscribed_at=2.0, delivery_count=3)
        assert info.sub_id == "abc"
        assert info.event_pattern == "*"
        assert info.subscribed_at == 2.0
        assert info.delivery_count == 3

    def test_mutability(self):
        info = SubscriberInfo(sub_id="abc", event_pattern="t")
        info.delivery_count += 1
        assert info.delivery_count == 1


class TestPubSubStatsDataclass:
    def test_defaults(self):
        s = PubSubStats()
        assert s.total_events == 0
        assert s.total_subscribers == 0
        assert s.total_deliveries == 0

    def test_explicit(self):
        s = PubSubStats(total_events=1, total_subscribers=2, total_deliveries=3)
        assert s.total_events == 1
        assert s.total_subscribers == 2
        assert s.total_deliveries == 3


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_bus(self):
        bus = DocPubSubBus()
        assert bus.stats().total_events == 0
        assert bus.stats().total_subscribers == 0
        assert bus.stats().total_deliveries == 0

    def test_no_subscribers_initially(self):
        bus = DocPubSubBus()
        assert bus.list_subscribers() == []

    def test_no_events_initially(self):
        bus = DocPubSubBus()
        assert bus.recent_events() == []


# ---------------------------------------------------------------------------
# Subscribe
# ---------------------------------------------------------------------------


class TestSubscribe:
    def test_returns_info(self):
        bus = DocPubSubBus()
        info = bus.subscribe("created", lambda e: None)
        assert isinstance(info, SubscriberInfo)

    def test_assigns_uuid(self):
        bus = DocPubSubBus()
        info = bus.subscribe("created", lambda e: None)
        uuid.UUID(info.sub_id)  # raises if not a valid UUID

    def test_unique_uuids(self):
        bus = DocPubSubBus()
        info1 = bus.subscribe("a", lambda e: None)
        info2 = bus.subscribe("a", lambda e: None)
        assert info1.sub_id != info2.sub_id

    def test_stores_pattern(self):
        bus = DocPubSubBus()
        info = bus.subscribe("updated", lambda e: None)
        assert info.event_pattern == "updated"

    def test_timestamp_set(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None, now=99.0)
        assert info.subscribed_at == 99.0

    def test_timestamp_default_now(self):
        bus = DocPubSubBus()
        before = time.time()
        info = bus.subscribe("a", lambda e: None)
        after = time.time()
        assert before <= info.subscribed_at <= after

    def test_delivery_count_starts_zero(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        assert info.delivery_count == 0

    def test_appears_in_list(self):
        bus = DocPubSubBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        assert len(bus.list_subscribers()) == 2


# ---------------------------------------------------------------------------
# Unsubscribe
# ---------------------------------------------------------------------------


class TestUnsubscribe:
    def test_returns_true_when_existed(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        assert bus.unsubscribe(info.sub_id) is True

    def test_returns_false_when_missing(self):
        bus = DocPubSubBus()
        assert bus.unsubscribe("not-here") is False

    def test_removes_from_list(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        bus.unsubscribe(info.sub_id)
        assert bus.list_subscribers() == []

    def test_no_more_deliveries(self):
        bus = DocPubSubBus()
        seen = []
        info = bus.subscribe("a", lambda e: seen.append(e))
        bus.publish("a")
        bus.unsubscribe(info.sub_id)
        bus.publish("a")
        assert len(seen) == 1

    def test_double_unsubscribe(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        assert bus.unsubscribe(info.sub_id) is True
        assert bus.unsubscribe(info.sub_id) is False


# ---------------------------------------------------------------------------
# Publish
# ---------------------------------------------------------------------------


class TestPublish:
    def test_returns_event(self):
        bus = DocPubSubBus()
        ev = bus.publish("created", doc_id="d1", payload={"x": 1})
        assert isinstance(ev, PubSubEvent)
        assert ev.event_type == "created"
        assert ev.doc_id == "d1"
        assert ev.payload == {"x": 1}

    def test_event_stored(self):
        bus = DocPubSubBus()
        ev = bus.publish("t")
        assert bus.get_event(ev.event_id) == ev

    def test_id_increments(self):
        bus = DocPubSubBus()
        e1 = bus.publish("a")
        e2 = bus.publish("a")
        e3 = bus.publish("a")
        assert (e1.event_id, e2.event_id, e3.event_id) == (1, 2, 3)

    def test_callback_called(self):
        bus = DocPubSubBus()
        seen: list[PubSubEvent] = []
        bus.subscribe("a", lambda e: seen.append(e))
        ev = bus.publish("a")
        assert seen == [ev]

    def test_callback_called_with_correct_payload(self):
        bus = DocPubSubBus()
        captured = {}

        def cb(e: PubSubEvent) -> None:
            captured["payload"] = e.payload
            captured["doc"] = e.doc_id

        bus.subscribe("a", cb)
        bus.publish("a", doc_id="d2", payload={"k": "v"})
        assert captured == {"payload": {"k": "v"}, "doc": "d2"}

    def test_now_used(self):
        bus = DocPubSubBus()
        ev = bus.publish("a", now=123.5)
        assert ev.published_at == 123.5

    def test_default_payload_is_dict(self):
        bus = DocPubSubBus()
        ev = bus.publish("a")
        assert ev.payload == {}

    def test_payload_copied(self):
        bus = DocPubSubBus()
        payload = {"a": 1}
        ev = bus.publish("a", payload=payload)
        payload["a"] = 99
        assert ev.payload == {"a": 1}

    def test_no_subscribers_ok(self):
        bus = DocPubSubBus()
        ev = bus.publish("a")
        assert ev.event_id == 1

    def test_callback_exception_swallowed(self):
        bus = DocPubSubBus()

        def bad(_e: PubSubEvent) -> None:
            raise RuntimeError("boom")

        bus.subscribe("a", bad)
        # Should not raise.
        bus.publish("a")
        assert bus.stats().total_events == 1


# ---------------------------------------------------------------------------
# Wildcard subscription
# ---------------------------------------------------------------------------


class TestWildcardSubscription:
    def test_wildcard_receives_all(self):
        bus = DocPubSubBus()
        seen: list[str] = []
        bus.subscribe("*", lambda e: seen.append(e.event_type))
        bus.publish("a")
        bus.publish("b")
        bus.publish("c")
        assert seen == ["a", "b", "c"]

    def test_wildcard_plus_exact(self):
        bus = DocPubSubBus()
        all_seen: list[str] = []
        a_seen: list[str] = []
        bus.subscribe("*", lambda e: all_seen.append(e.event_type))
        bus.subscribe("a", lambda e: a_seen.append(e.event_type))
        bus.publish("a")
        bus.publish("b")
        assert all_seen == ["a", "b"]
        assert a_seen == ["a"]


# ---------------------------------------------------------------------------
# Exact subscription
# ---------------------------------------------------------------------------


class TestExactSubscription:
    def test_only_matching(self):
        bus = DocPubSubBus()
        seen: list[str] = []
        bus.subscribe("created", lambda e: seen.append(e.event_type))
        bus.publish("updated")
        bus.publish("created")
        bus.publish("deleted")
        assert seen == ["created"]

    def test_case_sensitive(self):
        bus = DocPubSubBus()
        seen: list[str] = []
        bus.subscribe("Created", lambda e: seen.append(e.event_type))
        bus.publish("created")
        assert seen == []


# ---------------------------------------------------------------------------
# Delivery count
# ---------------------------------------------------------------------------


class TestDeliveryCount:
    def test_starts_zero(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        subs = bus.list_subscribers()
        assert subs[0].delivery_count == 0
        assert info.delivery_count == 0

    def test_increments_per_delivery(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        bus.publish("a")
        bus.publish("a")
        bus.publish("a")
        assert info.delivery_count == 3

    def test_not_incremented_on_mismatch(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        bus.publish("b")
        bus.publish("c")
        assert info.delivery_count == 0

    def test_wildcard_counts(self):
        bus = DocPubSubBus()
        info = bus.subscribe("*", lambda e: None)
        bus.publish("a")
        bus.publish("b")
        assert info.delivery_count == 2


# ---------------------------------------------------------------------------
# Callback outside lock
# ---------------------------------------------------------------------------


class TestCallbackOutsideLock:
    def test_long_callback_does_not_block_other_publishes(self):
        bus = DocPubSubBus()
        blocker = threading.Event()
        in_callback = threading.Event()

        def slow(_e: PubSubEvent) -> None:
            in_callback.set()
            blocker.wait(timeout=2.0)

        bus.subscribe("slow", slow)

        # Start slow publish in a thread.
        t = threading.Thread(target=bus.publish, args=("slow",))
        t.start()

        # Wait until we're inside the callback.
        assert in_callback.wait(timeout=2.0)

        # Other publishes should still succeed without waiting.
        start = time.time()
        bus.publish("fast")
        elapsed = time.time() - start
        assert elapsed < 1.0

        blocker.set()
        t.join(timeout=2.0)


# ---------------------------------------------------------------------------
# get_event
# ---------------------------------------------------------------------------


class TestGetEvent:
    def test_found(self):
        bus = DocPubSubBus()
        ev = bus.publish("a")
        assert bus.get_event(ev.event_id) == ev

    def test_not_found(self):
        bus = DocPubSubBus()
        bus.publish("a")
        assert bus.get_event(999) is None

    def test_empty(self):
        bus = DocPubSubBus()
        assert bus.get_event(1) is None


# ---------------------------------------------------------------------------
# events_by_type
# ---------------------------------------------------------------------------


class TestEventsByType:
    def test_only_matching(self):
        bus = DocPubSubBus()
        bus.publish("a", now=1.0)
        bus.publish("b", now=2.0)
        bus.publish("a", now=3.0)
        result = bus.events_by_type("a")
        assert [e.published_at for e in result] == [1.0, 3.0]

    def test_sorted_by_time(self):
        bus = DocPubSubBus()
        bus.publish("a", now=3.0)
        bus.publish("a", now=1.0)
        bus.publish("a", now=2.0)
        result = bus.events_by_type("a")
        assert [e.published_at for e in result] == [1.0, 2.0, 3.0]

    def test_limit(self):
        bus = DocPubSubBus()
        for i in range(5):
            bus.publish("a", now=float(i))
        result = bus.events_by_type("a", limit=2)
        assert len(result) == 2
        assert [e.published_at for e in result] == [0.0, 1.0]

    def test_empty(self):
        bus = DocPubSubBus()
        assert bus.events_by_type("a") == []


# ---------------------------------------------------------------------------
# events_for_doc
# ---------------------------------------------------------------------------


class TestEventsForDoc:
    def test_only_matching_doc(self):
        bus = DocPubSubBus()
        bus.publish("a", doc_id="d1", now=1.0)
        bus.publish("a", doc_id="d2", now=2.0)
        bus.publish("a", doc_id="d1", now=3.0)
        result = bus.events_for_doc("d1")
        assert [e.published_at for e in result] == [1.0, 3.0]

    def test_sorted_by_time(self):
        bus = DocPubSubBus()
        bus.publish("a", doc_id="d1", now=5.0)
        bus.publish("a", doc_id="d1", now=2.0)
        result = bus.events_for_doc("d1")
        assert [e.published_at for e in result] == [2.0, 5.0]

    def test_limit(self):
        bus = DocPubSubBus()
        for i in range(4):
            bus.publish("a", doc_id="d1", now=float(i))
        result = bus.events_for_doc("d1", limit=2)
        assert len(result) == 2

    def test_no_match(self):
        bus = DocPubSubBus()
        bus.publish("a", doc_id="d1")
        assert bus.events_for_doc("dX") == []


# ---------------------------------------------------------------------------
# recent_events
# ---------------------------------------------------------------------------


class TestRecentEvents:
    def test_most_recent_first(self):
        bus = DocPubSubBus()
        bus.publish("a", now=1.0)
        bus.publish("a", now=2.0)
        bus.publish("a", now=3.0)
        result = bus.recent_events()
        assert [e.published_at for e in result] == [3.0, 2.0, 1.0]

    def test_limit(self):
        bus = DocPubSubBus()
        for i in range(20):
            bus.publish("a", now=float(i))
        result = bus.recent_events(limit=3)
        assert len(result) == 3
        assert [e.published_at for e in result] == [19.0, 18.0, 17.0]

    def test_default_limit_10(self):
        bus = DocPubSubBus()
        for i in range(15):
            bus.publish("a", now=float(i))
        result = bus.recent_events()
        assert len(result) == 10

    def test_empty(self):
        bus = DocPubSubBus()
        assert bus.recent_events() == []


# ---------------------------------------------------------------------------
# list_subscribers
# ---------------------------------------------------------------------------


class TestListSubscribers:
    def test_sorted_by_sub_id(self):
        bus = DocPubSubBus()
        infos = [bus.subscribe(f"t{i}", lambda e: None) for i in range(5)]
        listed = bus.list_subscribers()
        assert [s.sub_id for s in listed] == sorted(s.sub_id for s in infos)

    def test_empty(self):
        bus = DocPubSubBus()
        assert bus.list_subscribers() == []

    def test_includes_all(self):
        bus = DocPubSubBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        bus.subscribe("c", lambda e: None)
        assert len(bus.list_subscribers()) == 3


# ---------------------------------------------------------------------------
# subscriber_count_for
# ---------------------------------------------------------------------------


class TestSubscriberCountFor:
    def test_zero(self):
        bus = DocPubSubBus()
        assert bus.subscriber_count_for("a") == 0

    def test_exact_only(self):
        bus = DocPubSubBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        assert bus.subscriber_count_for("a") == 1
        assert bus.subscriber_count_for("b") == 1
        assert bus.subscriber_count_for("c") == 0

    def test_wildcard_counts(self):
        bus = DocPubSubBus()
        bus.subscribe("*", lambda e: None)
        assert bus.subscriber_count_for("anything") == 1

    def test_wildcard_plus_exact(self):
        bus = DocPubSubBus()
        bus.subscribe("*", lambda e: None)
        bus.subscribe("a", lambda e: None)
        bus.subscribe("a", lambda e: None)
        assert bus.subscriber_count_for("a") == 3
        assert bus.subscriber_count_for("b") == 1


# ---------------------------------------------------------------------------
# clear_history
# ---------------------------------------------------------------------------


class TestClearHistory:
    def test_returns_count(self):
        bus = DocPubSubBus()
        bus.publish("a")
        bus.publish("a")
        bus.publish("a")
        assert bus.clear_history() == 3

    def test_events_gone(self):
        bus = DocPubSubBus()
        bus.publish("a")
        bus.clear_history()
        assert bus.recent_events() == []
        assert bus.stats().total_events == 0

    def test_subscribers_preserved(self):
        bus = DocPubSubBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        bus.publish("a")
        bus.clear_history()
        assert len(bus.list_subscribers()) == 2

    def test_empty_returns_zero(self):
        bus = DocPubSubBus()
        assert bus.clear_history() == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_initial(self):
        bus = DocPubSubBus()
        s = bus.stats()
        assert s.total_events == 0
        assert s.total_subscribers == 0
        assert s.total_deliveries == 0

    def test_after_publish(self):
        bus = DocPubSubBus()
        bus.publish("a")
        bus.publish("a")
        assert bus.stats().total_events == 2

    def test_after_subscribe(self):
        bus = DocPubSubBus()
        bus.subscribe("a", lambda e: None)
        bus.subscribe("b", lambda e: None)
        assert bus.stats().total_subscribers == 2

    def test_total_deliveries(self):
        bus = DocPubSubBus()
        bus.subscribe("*", lambda e: None)
        bus.subscribe("a", lambda e: None)
        bus.publish("a")
        bus.publish("b")
        # "*" gets both (2), "a" gets one (1) → 3
        assert bus.stats().total_deliveries == 3

    def test_unsubscribe_lowers_subscribers(self):
        bus = DocPubSubBus()
        info = bus.subscribe("a", lambda e: None)
        bus.unsubscribe(info.sub_id)
        assert bus.stats().total_subscribers == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_publish(self):
        bus = DocPubSubBus()
        seen: list[PubSubEvent] = []
        lock = threading.Lock()

        def cb(e: PubSubEvent) -> None:
            with lock:
                seen.append(e)

        bus.subscribe("*", cb)

        N = 50
        WORKERS = 10

        def worker() -> None:
            for _ in range(N):
                bus.publish("x")

        threads = [threading.Thread(target=worker) for _ in range(WORKERS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert bus.stats().total_events == N * WORKERS
        assert len(seen) == N * WORKERS
        ids = {e.event_id for e in seen}
        assert len(ids) == N * WORKERS  # all unique

    def test_concurrent_subscribe(self):
        bus = DocPubSubBus()

        def worker() -> None:
            for _ in range(20):
                bus.subscribe("a", lambda e: None)

        threads = [threading.Thread(target=worker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert bus.stats().total_subscribers == 100

    def test_concurrent_publish_and_subscribe(self):
        bus = DocPubSubBus()
        stop = threading.Event()

        def subscriber_worker() -> None:
            while not stop.is_set():
                info = bus.subscribe("a", lambda e: None)
                bus.unsubscribe(info.sub_id)

        def publisher_worker() -> None:
            for _ in range(50):
                bus.publish("a")

        sub_threads = [threading.Thread(target=subscriber_worker) for _ in range(3)]
        pub_threads = [threading.Thread(target=publisher_worker) for _ in range(3)]

        for t in sub_threads:
            t.start()
        for t in pub_threads:
            t.start()
        for t in pub_threads:
            t.join()
        stop.set()
        for t in sub_threads:
            t.join()

        assert bus.stats().total_events == 150


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
