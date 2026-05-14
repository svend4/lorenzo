"""Tests for docstoolkit.doc_notification_center (E282).

Covers:
- Dataclass construction and field defaults
- subscribe / unsubscribe
- publish / delivery
- pause / resume
- history (filtering, limit, order)
- clear_history
- fnmatch patterns
- stats / total_subscriptions property
- thread safety
- edge cases (callbacks raising, no subscribers, re-entrant publish, etc.)
"""

from __future__ import annotations

import threading
import time
from typing import List

import pytest

from docstoolkit.doc_notification_center import (
    DocNotificationCenter,
    Notification,
    NotifStats,
    Subscription,
)

T0 = 1_700_000_000.0


def _center() -> DocNotificationCenter:
    return DocNotificationCenter()


# ================================================================ dataclasses


class TestNotification:
    def test_required_fields(self):
        n = Notification(notif_id=1, topic="t", payload={"k": "v"}, timestamp=T0)
        assert n.notif_id == 1
        assert n.topic == "t"
        assert n.payload == {"k": "v"}
        assert n.timestamp == T0

    def test_sender_default_empty(self):
        n = Notification(notif_id=2, topic="t", payload={}, timestamp=0.0)
        assert n.sender == ""

    def test_sender_custom(self):
        n = Notification(notif_id=3, topic="t", payload={}, timestamp=0.0, sender="api")
        assert n.sender == "api"

    def test_payload_identity(self):
        data = {"a": 1, "b": [1, 2, 3]}
        n = Notification(notif_id=4, topic="t", payload=data, timestamp=0.0)
        assert n.payload is data


class TestSubscription:
    def test_required_fields(self):
        cb = lambda n: None
        s = Subscription(sub_id="x", topic="doc.*", callback=cb)
        assert s.sub_id == "x"
        assert s.topic == "doc.*"
        assert s.callback is cb

    def test_active_default_true(self):
        s = Subscription(sub_id="y", topic="*", callback=lambda n: None)
        assert s.active is True

    def test_active_can_be_false(self):
        s = Subscription(sub_id="z", topic="*", callback=lambda n: None, active=False)
        assert s.active is False


class TestNotifStats:
    def test_construction(self):
        st = NotifStats(
            total_published=5,
            total_delivered=10,
            total_subscriptions=2,
            topics_seen=["a", "b"],
        )
        assert st.total_published == 5
        assert st.total_delivered == 10
        assert st.total_subscriptions == 2
        assert st.topics_seen == ["a", "b"]

    def test_topics_seen_is_list(self):
        st = NotifStats(
            total_published=0,
            total_delivered=0,
            total_subscriptions=0,
            topics_seen=[],
        )
        assert isinstance(st.topics_seen, list)


# ================================================================ subscribe


class TestSubscribe:
    def test_returns_subscription(self):
        c = _center()
        sub = c.subscribe("doc.*", lambda n: None)
        assert isinstance(sub, Subscription)

    def test_sub_id_auto_generated(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        assert sub.sub_id != ""
        assert isinstance(sub.sub_id, str)

    def test_custom_sub_id(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None, sub_id="my-id")
        assert sub.sub_id == "my-id"

    def test_stores_topic(self):
        c = _center()
        sub = c.subscribe("doc.*", lambda n: None)
        assert sub.topic == "doc.*"

    def test_multiple_unique_ids(self):
        c = _center()
        ids = {c.subscribe("t", lambda n: None).sub_id for _ in range(10)}
        assert len(ids) == 10

    def test_subscription_active_by_default(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        assert sub.active is True

    def test_total_subscriptions_increments(self):
        c = _center()
        assert c.total_subscriptions == 0
        c.subscribe("a", lambda n: None)
        c.subscribe("b", lambda n: None)
        assert c.total_subscriptions == 2


# ================================================================ unsubscribe


class TestUnsubscribe:
    def test_returns_true_when_removed(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        assert c.unsubscribe(sub.sub_id) is True

    def test_returns_false_when_missing(self):
        c = _center()
        assert c.unsubscribe("nonexistent") is False

    def test_double_unsubscribe_returns_false(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.unsubscribe(sub.sub_id)
        assert c.unsubscribe(sub.sub_id) is False

    def test_subscription_removed_from_center(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.unsubscribe(sub.sub_id)
        assert c.total_subscriptions == 0

    def test_callback_not_called_after_unsubscribe(self):
        c = _center()
        calls: List[Notification] = []
        sub = c.subscribe("t", lambda n: calls.append(n))
        c.unsubscribe(sub.sub_id)
        c.publish("t", {}, now=T0)
        assert calls == []


# ================================================================ publish


class TestPublish:
    def test_returns_notification(self):
        c = _center()
        n = c.publish("t", {"x": 1}, now=T0)
        assert isinstance(n, Notification)

    def test_notif_id_starts_at_1(self):
        c = _center()
        n = c.publish("t", {}, now=T0)
        assert n.notif_id == 1

    def test_notif_id_increments(self):
        c = _center()
        a = c.publish("t", {}, now=T0)
        b = c.publish("t", {}, now=T0 + 1)
        c2 = c.publish("t", {}, now=T0 + 2)
        assert a.notif_id == 1
        assert b.notif_id == 2
        assert c2.notif_id == 3

    def test_topic_stored(self):
        c = _center()
        n = c.publish("doc.created", {}, now=T0)
        assert n.topic == "doc.created"

    def test_payload_stored(self):
        c = _center()
        n = c.publish("t", {"key": "value"}, now=T0)
        assert n.payload == {"key": "value"}

    def test_sender_stored(self):
        c = _center()
        n = c.publish("t", {}, sender="worker", now=T0)
        assert n.sender == "worker"

    def test_sender_default_empty(self):
        c = _center()
        n = c.publish("t", {}, now=T0)
        assert n.sender == ""

    def test_custom_timestamp(self):
        c = _center()
        n = c.publish("t", {}, now=999.5)
        assert n.timestamp == 999.5

    def test_callback_receives_notification(self):
        c = _center()
        received: List[Notification] = []
        c.subscribe("t", lambda n: received.append(n))
        notif = c.publish("t", {"v": 42}, now=T0)
        assert len(received) == 1
        assert received[0] is notif

    def test_no_subscribers_no_error(self):
        c = _center()
        n = c.publish("ghost", {"a": 1}, now=T0)
        assert n.notif_id == 1

    def test_multiple_subscribers_all_called(self):
        c = _center()
        calls_a: List[int] = []
        calls_b: List[int] = []
        c.subscribe("t", lambda n: calls_a.append(n.notif_id))
        c.subscribe("t", lambda n: calls_b.append(n.notif_id))
        c.publish("t", {}, now=T0)
        assert len(calls_a) == 1
        assert len(calls_b) == 1

    def test_callback_raising_does_not_abort_others(self):
        c = _center()
        good_calls: List[int] = []

        def bad(n: Notification) -> None:
            raise RuntimeError("intentional")

        c.subscribe("t", bad)
        c.subscribe("t", lambda n: good_calls.append(n.notif_id))
        c.publish("t", {}, now=T0)
        assert len(good_calls) == 1

    def test_delivered_counted_only_for_successful_callbacks(self):
        c = _center()

        def bad(n: Notification) -> None:
            raise ValueError

        c.subscribe("t", bad)
        c.subscribe("t", lambda n: None)
        c.publish("t", {}, now=T0)
        st = c.stats()
        assert st.total_delivered == 1

    def test_no_match_no_callback(self):
        c = _center()
        calls: List[Notification] = []
        c.subscribe("doc.deleted", lambda n: calls.append(n))
        c.publish("doc.created", {}, now=T0)
        assert calls == []

    def test_publish_adds_to_history(self):
        c = _center()
        c.publish("t", {}, now=T0)
        assert len(c.history()) == 1


# ================================================================ pause / resume


class TestPauseResume:
    def test_pause_returns_true(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        assert c.pause(sub.sub_id) is True

    def test_pause_missing_returns_false(self):
        c = _center()
        assert c.pause("no-such-id") is False

    def test_resume_returns_true(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.pause(sub.sub_id)
        assert c.resume(sub.sub_id) is True

    def test_resume_missing_returns_false(self):
        c = _center()
        assert c.resume("no-such-id") is False

    def test_paused_callback_not_called(self):
        c = _center()
        calls: List[Notification] = []
        sub = c.subscribe("t", lambda n: calls.append(n))
        c.pause(sub.sub_id)
        c.publish("t", {}, now=T0)
        assert calls == []

    def test_resumed_callback_called_again(self):
        c = _center()
        calls: List[Notification] = []
        sub = c.subscribe("t", lambda n: calls.append(n))
        c.pause(sub.sub_id)
        c.publish("t", {}, now=T0)
        c.resume(sub.sub_id)
        c.publish("t", {}, now=T0 + 1)
        assert len(calls) == 1

    def test_pause_does_not_remove_subscription(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.pause(sub.sub_id)
        assert c.total_subscriptions == 1

    def test_pause_sets_active_false(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.pause(sub.sub_id)
        subs = c.subscriptions()
        assert subs[0].active is False

    def test_resume_sets_active_true(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.pause(sub.sub_id)
        c.resume(sub.sub_id)
        subs = c.subscriptions()
        assert subs[0].active is True

    def test_paused_not_counted_in_delivered(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.pause(sub.sub_id)
        c.publish("t", {}, now=T0)
        assert c.stats().total_delivered == 0


# ================================================================ history


class TestHistory:
    def test_empty_initially(self):
        c = _center()
        assert c.history() == []

    def test_newest_first(self):
        c = _center()
        c.publish("t", {}, now=T0)
        c.publish("t", {}, now=T0 + 1)
        c.publish("t", {}, now=T0 + 2)
        hist = c.history()
        assert hist[0].timestamp == T0 + 2
        assert hist[1].timestamp == T0 + 1
        assert hist[2].timestamp == T0

    def test_limit(self):
        c = _center()
        for i in range(10):
            c.publish("t", {}, now=T0 + i)
        hist = c.history(limit=3)
        assert len(hist) == 3

    def test_default_limit_20(self):
        c = _center()
        for _ in range(25):
            c.publish("t", {}, now=T0)
        hist = c.history()
        assert len(hist) == 20

    def test_filter_by_topic(self):
        c = _center()
        c.publish("doc.created", {}, now=T0)
        c.publish("doc.deleted", {}, now=T0 + 1)
        c.publish("doc.created", {}, now=T0 + 2)
        hist = c.history(topic="doc.created")
        assert all(n.topic == "doc.created" for n in hist)
        assert len(hist) == 2

    def test_filter_no_match_returns_empty(self):
        c = _center()
        c.publish("doc.created", {}, now=T0)
        assert c.history(topic="user.login") == []

    def test_all_topics_without_filter(self):
        c = _center()
        c.publish("a", {}, now=T0)
        c.publish("b", {}, now=T0 + 1)
        c.publish("c", {}, now=T0 + 2)
        hist = c.history()
        topics = {n.topic for n in hist}
        assert topics == {"a", "b", "c"}

    def test_limit_zero_returns_empty(self):
        c = _center()
        c.publish("t", {}, now=T0)
        assert c.history(limit=0) == []


# ================================================================ clear_history


class TestClearHistory:
    def test_clear_all_returns_count(self):
        c = _center()
        c.publish("a", {}, now=T0)
        c.publish("b", {}, now=T0 + 1)
        removed = c.clear_history()
        assert removed == 2

    def test_clear_all_empties_history(self):
        c = _center()
        c.publish("t", {}, now=T0)
        c.clear_history()
        assert c.history() == []

    def test_clear_by_topic_returns_count(self):
        c = _center()
        c.publish("doc.created", {}, now=T0)
        c.publish("doc.created", {}, now=T0 + 1)
        c.publish("doc.deleted", {}, now=T0 + 2)
        removed = c.clear_history(topic="doc.created")
        assert removed == 2

    def test_clear_by_topic_leaves_others(self):
        c = _center()
        c.publish("doc.created", {}, now=T0)
        c.publish("doc.deleted", {}, now=T0 + 1)
        c.clear_history(topic="doc.created")
        hist = c.history()
        assert len(hist) == 1
        assert hist[0].topic == "doc.deleted"

    def test_clear_empty_returns_zero(self):
        c = _center()
        assert c.clear_history() == 0

    def test_clear_missing_topic_returns_zero(self):
        c = _center()
        c.publish("a", {}, now=T0)
        removed = c.clear_history(topic="z")
        assert removed == 0

    def test_clear_then_publish_restores(self):
        c = _center()
        c.publish("t", {}, now=T0)
        c.clear_history()
        c.publish("t", {}, now=T0 + 1)
        hist = c.history()
        assert len(hist) == 1
        assert hist[0].notif_id == 2  # counter continues


# ================================================================ fnmatch patterns


class TestFnmatchPatterns:
    def test_star_suffix(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("doc.*", lambda n: calls.append(n.topic))
        c.publish("doc.created", {}, now=T0)
        c.publish("doc.updated", {}, now=T0 + 1)
        assert calls == ["doc.created", "doc.updated"]

    def test_star_no_match_different_prefix(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("doc.*", lambda n: calls.append(n.topic))
        c.publish("user.created", {}, now=T0)
        assert calls == []

    def test_star_alone_matches_single_word(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("*", lambda n: calls.append(n.topic))
        c.publish("anything", {}, now=T0)
        assert "anything" in calls

    def test_exact_match(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("doc.created", lambda n: calls.append(n.topic))
        c.publish("doc.created", {}, now=T0)
        c.publish("doc.updated", {}, now=T0 + 1)
        assert calls == ["doc.created"]

    def test_double_star_matches_multi_segment(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("*.*", lambda n: calls.append(n.topic))
        c.publish("doc.created", {}, now=T0)
        c.publish("user.deleted", {}, now=T0 + 1)
        assert len(calls) == 2

    def test_question_mark_pattern(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("do?.created", lambda n: calls.append(n.topic))
        c.publish("doc.created", {}, now=T0)
        assert "doc.created" in calls

    def test_bracket_pattern(self):
        c = _center()
        calls: List[str] = []
        c.subscribe("[abc].event", lambda n: calls.append(n.topic))
        c.publish("a.event", {}, now=T0)
        c.publish("b.event", {}, now=T0 + 1)
        c.publish("d.event", {}, now=T0 + 2)
        assert "a.event" in calls
        assert "b.event" in calls
        assert "d.event" not in calls

    def test_multiple_subs_same_pattern(self):
        c = _center()
        a_calls: List[int] = []
        b_calls: List[int] = []
        c.subscribe("doc.*", lambda n: a_calls.append(n.notif_id))
        c.subscribe("doc.*", lambda n: b_calls.append(n.notif_id))
        c.publish("doc.x", {}, now=T0)
        assert len(a_calls) == 1
        assert len(b_calls) == 1
        assert a_calls == b_calls


# ================================================================ stats


class TestStats:
    def test_initial_stats(self):
        c = _center()
        st = c.stats()
        assert st.total_published == 0
        assert st.total_delivered == 0
        assert st.total_subscriptions == 0
        assert st.topics_seen == []

    def test_returns_notifstats(self):
        c = _center()
        assert isinstance(c.stats(), NotifStats)

    def test_total_published_increments(self):
        c = _center()
        c.publish("t", {}, now=T0)
        c.publish("t", {}, now=T0 + 1)
        assert c.stats().total_published == 2

    def test_total_delivered_counts_callbacks(self):
        c = _center()
        c.subscribe("t", lambda n: None)
        c.subscribe("t", lambda n: None)
        c.publish("t", {}, now=T0)
        assert c.stats().total_delivered == 2

    def test_total_subscriptions_reflects_current(self):
        c = _center()
        c.subscribe("a", lambda n: None)
        c.subscribe("b", lambda n: None)
        assert c.stats().total_subscriptions == 2

    def test_topics_seen_sorted(self):
        c = _center()
        c.publish("z.topic", {}, now=T0)
        c.publish("a.topic", {}, now=T0 + 1)
        c.publish("m.topic", {}, now=T0 + 2)
        st = c.stats()
        assert st.topics_seen == sorted(st.topics_seen)

    def test_topics_seen_unique(self):
        c = _center()
        c.publish("t", {}, now=T0)
        c.publish("t", {}, now=T0 + 1)
        c.publish("t", {}, now=T0 + 2)
        st = c.stats()
        assert st.topics_seen.count("t") == 1

    def test_total_subscriptions_property(self):
        c = _center()
        c.subscribe("a", lambda n: None)
        assert c.total_subscriptions == 1

    def test_subscriptions_method_no_filter(self):
        c = _center()
        c.subscribe("a", lambda n: None)
        c.subscribe("b", lambda n: None)
        assert len(c.subscriptions()) == 2

    def test_subscriptions_method_with_filter(self):
        c = _center()
        c.subscribe("doc.*", lambda n: None)
        c.subscribe("user.*", lambda n: None)
        doc_subs = c.subscriptions(topic="doc.*")
        assert len(doc_subs) == 1
        assert doc_subs[0].topic == "doc.*"

    def test_topics_seen_preserved_after_clear_history(self):
        c = _center()
        c.publish("unique.topic", {}, now=T0)
        c.clear_history()
        st = c.stats()
        assert "unique.topic" in st.topics_seen


# ================================================================ thread safety


class TestThreadSafety:
    def test_concurrent_subscribe_unique_ids(self):
        c = _center()
        results: List[Subscription] = []
        lock = threading.Lock()

        def worker():
            sub = c.subscribe("t", lambda n: None)
            with lock:
                results.append(sub)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 20
        ids = {s.sub_id for s in results}
        assert len(ids) == 20

    def test_concurrent_publish_total(self):
        c = _center()
        calls: List[int] = []
        lock = threading.Lock()
        c.subscribe("t", lambda n: (lock.acquire(), calls.append(1), lock.release()))
        errors: List[Exception] = []

        def publisher():
            try:
                for i in range(10):
                    c.publish("t", {"i": i}, now=T0 + i)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=publisher) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert c.stats().total_published == 50

    def test_concurrent_publish_increments_notif_ids_uniquely(self):
        c = _center()
        notif_ids: List[int] = []
        lock = threading.Lock()

        def publisher():
            for _ in range(10):
                n = c.publish("t", {}, now=T0)
                with lock:
                    notif_ids.append(n.notif_id)

        threads = [threading.Thread(target=publisher) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(notif_ids) == 50
        assert len(set(notif_ids)) == 50

    def test_callback_outside_lock_no_deadlock(self):
        """Reentrant publish from a callback must not deadlock."""
        c = _center()
        secondary_calls: List[int] = []

        def reentrant_callback(n: Notification) -> None:
            if n.topic == "primary":
                notif = c.publish("secondary", {"from": n.notif_id}, now=T0)
                secondary_calls.append(notif.notif_id)

        c.subscribe("primary", reentrant_callback)
        c.publish("primary", {}, now=T0)
        assert len(secondary_calls) == 1


# ================================================================ edge cases


class TestEdgeCases:
    def test_empty_payload(self):
        c = _center()
        received: List[dict] = []
        c.subscribe("t", lambda n: received.append(n.payload))
        c.publish("t", {}, now=T0)
        assert received == [{}]

    def test_large_payload(self):
        c = _center()
        received: List[dict] = []
        big = {str(i): i for i in range(1000)}
        c.subscribe("t", lambda n: received.append(n.payload))
        c.publish("t", big, now=T0)
        assert received[0] == big

    def test_history_not_affected_by_unsubscribe(self):
        c = _center()
        sub = c.subscribe("t", lambda n: None)
        c.publish("t", {"msg": "hello"}, now=T0)
        c.unsubscribe(sub.sub_id)
        hist = c.history()
        assert len(hist) == 1

    def test_subscribe_same_sub_id_overwrites(self):
        c = _center()
        calls_a: List[int] = []
        calls_b: List[int] = []
        c.subscribe("t", lambda n: calls_a.append(1), sub_id="fixed")
        c.subscribe("t", lambda n: calls_b.append(1), sub_id="fixed")
        c.publish("t", {}, now=T0)
        assert calls_a == []
        assert calls_b == [1]

    def test_total_subscriptions_after_unsubscribe(self):
        c = _center()
        sub1 = c.subscribe("a", lambda n: None)
        c.subscribe("b", lambda n: None)
        c.unsubscribe(sub1.sub_id)
        assert c.total_subscriptions == 1

    def test_stats_after_multiple_topics(self):
        c = _center()
        c.subscribe("a", lambda n: None)
        c.publish("a", {}, now=T0)
        c.publish("b", {}, now=T0 + 1)
        c.publish("a", {}, now=T0 + 2)
        st = c.stats()
        assert st.total_published == 3
        assert st.total_delivered == 2  # only "a" sub fires


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-v"])
