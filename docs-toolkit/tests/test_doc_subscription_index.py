"""Tests for docstoolkit.doc_subscription_index (E408)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_subscription_index import (
    DocSubscriptionIndex,
    IndexStats,
    SubscriptionEntry,
)


# ---------------------------------------------------------------------------
# SubscriptionEntry dataclass
# ---------------------------------------------------------------------------

class TestSubscriptionEntry:
    def test_construct_with_required_fields(self):
        e = SubscriptionEntry(sub_id="s1", subscriber_id="alice", topic="news")
        assert e.sub_id == "s1"
        assert e.subscriber_id == "alice"
        assert e.topic == "news"

    def test_default_created_at_is_zero(self):
        e = SubscriptionEntry(sub_id="s1", subscriber_id="a", topic="t")
        assert e.created_at == 0.0

    def test_default_active_true(self):
        e = SubscriptionEntry(sub_id="s1", subscriber_id="a", topic="t")
        assert e.active is True

    def test_custom_created_at(self):
        e = SubscriptionEntry(
            sub_id="s1", subscriber_id="a", topic="t", created_at=123.5
        )
        assert e.created_at == 123.5

    def test_custom_active_false(self):
        e = SubscriptionEntry(
            sub_id="s1", subscriber_id="a", topic="t", active=False
        )
        assert e.active is False

    def test_equality(self):
        a = SubscriptionEntry(sub_id="s", subscriber_id="u", topic="t")
        b = SubscriptionEntry(sub_id="s", subscriber_id="u", topic="t")
        assert a == b

    def test_inequality(self):
        a = SubscriptionEntry(sub_id="s", subscriber_id="u", topic="t")
        b = SubscriptionEntry(sub_id="s", subscriber_id="u", topic="other")
        assert a != b


# ---------------------------------------------------------------------------
# IndexStats dataclass
# ---------------------------------------------------------------------------

class TestIndexStats:
    def test_construct(self):
        s = IndexStats(
            total_subscriptions=3,
            active_subscriptions=2,
            unique_topics=2,
            unique_subscribers=1,
        )
        assert s.total_subscriptions == 3
        assert s.active_subscriptions == 2
        assert s.unique_topics == 2
        assert s.unique_subscribers == 1

    def test_equality(self):
        a = IndexStats(1, 1, 1, 1)
        b = IndexStats(1, 1, 1, 1)
        assert a == b


# ---------------------------------------------------------------------------
# subscribe / get / delete / unsubscribe
# ---------------------------------------------------------------------------

class TestSubscribe:
    def test_returns_entry(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news")
        assert isinstance(e, SubscriptionEntry)

    def test_assigns_uuid_sub_id(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news")
        assert isinstance(e.sub_id, str)
        assert len(e.sub_id) >= 16

    def test_unique_sub_ids(self):
        idx = DocSubscriptionIndex()
        ids = {idx.subscribe("u", "t").sub_id for _ in range(50)}
        assert len(ids) == 50

    def test_default_active_true(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news")
        assert e.active is True

    def test_explicit_now(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news", now=42.0)
        assert e.created_at == 42.0

    def test_default_now_is_recent(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news")
        assert e.created_at > 0.0

    def test_empty_subscriber_raises(self):
        idx = DocSubscriptionIndex()
        with pytest.raises(ValueError):
            idx.subscribe("", "news")

    def test_empty_topic_raises(self):
        idx = DocSubscriptionIndex()
        with pytest.raises(ValueError):
            idx.subscribe("alice", "")

    def test_same_pair_creates_distinct_subscriptions(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("alice", "news")
        b = idx.subscribe("alice", "news")
        assert a.sub_id != b.sub_id


class TestGet:
    def test_returns_existing(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        assert idx.get(e.sub_id) is e

    def test_missing_returns_none(self):
        idx = DocSubscriptionIndex()
        assert idx.get("nope") is None


class TestUnsubscribe:
    def test_marks_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        assert idx.unsubscribe(e.sub_id) is True
        assert idx.get(e.sub_id).active is False

    def test_missing_returns_false(self):
        idx = DocSubscriptionIndex()
        assert idx.unsubscribe("nope") is False

    def test_does_not_remove_entry(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.get(e.sub_id) is not None

    def test_idempotent(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.unsubscribe(e.sub_id) is True
        assert idx.get(e.sub_id).active is False


class TestDelete:
    def test_removes_entry(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        assert idx.delete(e.sub_id) is True
        assert idx.get(e.sub_id) is None

    def test_missing_returns_false(self):
        idx = DocSubscriptionIndex()
        assert idx.delete("nope") is False

    def test_removes_from_topic_index(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.delete(e.sub_id)
        assert idx.subscribers_for_topic("t", active_only=False) == []

    def test_removes_from_subscriber_index(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.delete(e.sub_id)
        assert idx.topics_for_subscriber("u", active_only=False) == []

    def test_topic_disappears_when_empty(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.delete(e.sub_id)
        assert "t" not in idx.all_topics()

    def test_other_subs_unaffected(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("u", "t1")
        b = idx.subscribe("u", "t2")
        idx.delete(a.sub_id)
        assert idx.get(b.sub_id) is not None


# ---------------------------------------------------------------------------
# Lookup helpers
# ---------------------------------------------------------------------------

class TestSubscribersForTopic:
    def test_empty_topic(self):
        idx = DocSubscriptionIndex()
        assert idx.subscribers_for_topic("nope") == []

    def test_single(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("alice", "t")
        assert idx.subscribers_for_topic("t") == ["alice"]

    def test_multiple_sorted_unique(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("carol", "t")
        idx.subscribe("alice", "t")
        idx.subscribe("bob", "t")
        idx.subscribe("alice", "t")  # duplicate subscriber
        assert idx.subscribers_for_topic("t") == ["alice", "bob", "carol"]

    def test_active_only_default(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.subscribers_for_topic("t") == []

    def test_include_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.subscribers_for_topic("t", active_only=False) == ["alice"]


class TestTopicsForSubscriber:
    def test_empty_subscriber(self):
        idx = DocSubscriptionIndex()
        assert idx.topics_for_subscriber("nope") == []

    def test_multiple_sorted_unique(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("u", "news")
        idx.subscribe("u", "alerts")
        idx.subscribe("u", "news")  # duplicate
        assert idx.topics_for_subscriber("u") == ["alerts", "news"]

    def test_active_only_excludes_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "news")
        idx.subscribe("u", "alerts")
        idx.unsubscribe(e.sub_id)
        assert idx.topics_for_subscriber("u") == ["alerts"]

    def test_include_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "news")
        idx.unsubscribe(e.sub_id)
        assert idx.topics_for_subscriber("u", active_only=False) == ["news"]


class TestSubscriptionsForSubscriber:
    def test_sorted_by_created_at(self):
        idx = DocSubscriptionIndex()
        b = idx.subscribe("u", "b", now=20.0)
        a = idx.subscribe("u", "a", now=10.0)
        c = idx.subscribe("u", "c", now=30.0)
        out = idx.subscriptions_for_subscriber("u")
        assert [e.sub_id for e in out] == [a.sub_id, b.sub_id, c.sub_id]

    def test_empty(self):
        idx = DocSubscriptionIndex()
        assert idx.subscriptions_for_subscriber("u") == []

    def test_active_only(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("u", "a", now=1.0)
        idx.subscribe("u", "b", now=2.0)
        idx.unsubscribe(a.sub_id)
        out = idx.subscriptions_for_subscriber("u")
        assert [e.topic for e in out] == ["b"]

    def test_include_inactive(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("u", "a", now=1.0)
        idx.unsubscribe(a.sub_id)
        out = idx.subscriptions_for_subscriber("u", active_only=False)
        assert [e.topic for e in out] == ["a"]


class TestSubscriptionsForTopic:
    def test_sorted_by_created_at(self):
        idx = DocSubscriptionIndex()
        b = idx.subscribe("bob", "t", now=20.0)
        a = idx.subscribe("alice", "t", now=10.0)
        c = idx.subscribe("carol", "t", now=30.0)
        out = idx.subscriptions_for_topic("t")
        assert [e.sub_id for e in out] == [a.sub_id, b.sub_id, c.sub_id]

    def test_empty(self):
        idx = DocSubscriptionIndex()
        assert idx.subscriptions_for_topic("t") == []

    def test_active_only(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("alice", "t", now=1.0)
        idx.subscribe("bob", "t", now=2.0)
        idx.unsubscribe(a.sub_id)
        out = idx.subscriptions_for_topic("t")
        assert [e.subscriber_id for e in out] == ["bob"]

    def test_include_inactive(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("alice", "t", now=1.0)
        idx.unsubscribe(a.sub_id)
        out = idx.subscriptions_for_topic("t", active_only=False)
        assert [e.subscriber_id for e in out] == ["alice"]


class TestIsSubscribed:
    def test_true_when_active(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("alice", "news")
        assert idx.is_subscribed("alice", "news") is True

    def test_false_when_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("alice", "news")
        idx.unsubscribe(e.sub_id)
        assert idx.is_subscribed("alice", "news") is False

    def test_false_when_unknown_subscriber(self):
        idx = DocSubscriptionIndex()
        assert idx.is_subscribed("ghost", "news") is False

    def test_false_when_unknown_topic(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("alice", "news")
        assert idx.is_subscribed("alice", "other") is False

    def test_true_when_any_active_duplicate(self):
        idx = DocSubscriptionIndex()
        a = idx.subscribe("alice", "news")
        idx.subscribe("alice", "news")
        idx.unsubscribe(a.sub_id)
        assert idx.is_subscribed("alice", "news") is True


class TestAllTopicsAndSubscribers:
    def test_all_topics_sorted(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("u", "c")
        idx.subscribe("u", "a")
        idx.subscribe("u", "b")
        assert idx.all_topics() == ["a", "b", "c"]

    def test_all_subscribers_sorted(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("carol", "t")
        idx.subscribe("alice", "t")
        idx.subscribe("bob", "t")
        assert idx.all_subscribers() == ["alice", "bob", "carol"]

    def test_topics_after_delete_disappears(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "only")
        idx.delete(e.sub_id)
        assert idx.all_topics() == []

    def test_empty(self):
        idx = DocSubscriptionIndex()
        assert idx.all_topics() == []
        assert idx.all_subscribers() == []


# ---------------------------------------------------------------------------
# top_topics
# ---------------------------------------------------------------------------

class TestTopTopics:
    def test_sorted_by_count_desc(self):
        idx = DocSubscriptionIndex()
        for u in ("a", "b", "c"):
            idx.subscribe(u, "popular")
        idx.subscribe("a", "small")
        out = idx.top_topics()
        assert out[0] == ("popular", 3)
        assert ("small", 1) in out

    def test_limit_respected(self):
        idx = DocSubscriptionIndex()
        for t in ("a", "b", "c", "d"):
            idx.subscribe("u", t)
        out = idx.top_topics(limit=2)
        assert len(out) == 2

    def test_tie_broken_alphabetically(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("u", "b")
        idx.subscribe("u", "a")
        out = idx.top_topics()
        assert out == [("a", 1), ("b", 1)]

    def test_distinct_subscribers_only(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("a", "t")
        idx.subscribe("a", "t")  # duplicate user
        out = idx.top_topics()
        assert out == [("t", 1)]

    def test_excludes_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("a", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.top_topics() == []

    def test_empty(self):
        idx = DocSubscriptionIndex()
        assert idx.top_topics() == []

    def test_negative_limit_raises(self):
        idx = DocSubscriptionIndex()
        with pytest.raises(ValueError):
            idx.top_topics(limit=-1)

    def test_zero_limit_returns_empty(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("a", "t")
        assert idx.top_topics(limit=0) == []


# ---------------------------------------------------------------------------
# clear_topic / clear_subscriber
# ---------------------------------------------------------------------------

class TestClearTopic:
    def test_removes_all(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("a", "t")
        idx.subscribe("b", "t")
        idx.subscribe("c", "other")
        assert idx.clear_topic("t") == 2
        assert idx.subscribers_for_topic("t", active_only=False) == []
        assert idx.subscribers_for_topic("other") == ["c"]

    def test_unknown_returns_zero(self):
        idx = DocSubscriptionIndex()
        assert idx.clear_topic("nope") == 0

    def test_includes_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("a", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.clear_topic("t") == 1


class TestClearSubscriber:
    def test_removes_all(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("u", "a")
        idx.subscribe("u", "b")
        idx.subscribe("other", "a")
        assert idx.clear_subscriber("u") == 2
        assert idx.topics_for_subscriber("u", active_only=False) == []
        assert idx.subscribers_for_topic("a") == ["other"]

    def test_unknown_returns_zero(self):
        idx = DocSubscriptionIndex()
        assert idx.clear_subscriber("nope") == 0

    def test_includes_inactive(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("u", "t")
        idx.unsubscribe(e.sub_id)
        assert idx.clear_subscriber("u") == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        idx = DocSubscriptionIndex()
        s = idx.stats()
        assert s == IndexStats(0, 0, 0, 0)

    def test_counts(self):
        idx = DocSubscriptionIndex()
        idx.subscribe("a", "t1")
        idx.subscribe("a", "t2")
        e = idx.subscribe("b", "t1")
        idx.unsubscribe(e.sub_id)
        s = idx.stats()
        assert s.total_subscriptions == 3
        assert s.active_subscriptions == 2
        assert s.unique_topics == 2
        assert s.unique_subscribers == 2

    def test_after_delete(self):
        idx = DocSubscriptionIndex()
        e = idx.subscribe("a", "t")
        idx.delete(e.sub_id)
        assert idx.stats() == IndexStats(0, 0, 0, 0)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_subscribe(self):
        idx = DocSubscriptionIndex()

        def worker(uid: int):
            for j in range(20):
                idx.subscribe(f"u{uid}", f"t{j % 5}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = idx.stats()
        assert s.total_subscriptions == 200
        assert s.active_subscriptions == 200
        assert s.unique_subscribers == 10
        assert s.unique_topics == 5

    def test_concurrent_subscribe_and_delete(self):
        idx = DocSubscriptionIndex()
        ids: list[str] = []
        ids_lock = threading.Lock()

        def producer():
            for _ in range(50):
                e = idx.subscribe("u", "t")
                with ids_lock:
                    ids.append(e.sub_id)

        def consumer():
            for _ in range(50):
                with ids_lock:
                    sid = ids.pop() if ids else None
                if sid is not None:
                    idx.delete(sid)

        ts = [threading.Thread(target=producer) for _ in range(4)]
        ts += [threading.Thread(target=consumer) for _ in range(4)]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        s = idx.stats()
        # Index remains internally consistent regardless of interleaving.
        assert s.total_subscriptions >= 0
        assert s.active_subscriptions <= s.total_subscriptions

    def test_concurrent_unsubscribe(self):
        idx = DocSubscriptionIndex()
        entries = [idx.subscribe("u", "t") for _ in range(100)]

        def worker(start: int, end: int):
            for e in entries[start:end]:
                idx.unsubscribe(e.sub_id)

        ts = [
            threading.Thread(target=worker, args=(0, 50)),
            threading.Thread(target=worker, args=(50, 100)),
        ]
        for t in ts:
            t.start()
        for t in ts:
            t.join()

        s = idx.stats()
        assert s.active_subscriptions == 0
        assert s.total_subscriptions == 100
