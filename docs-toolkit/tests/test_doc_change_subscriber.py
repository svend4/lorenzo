"""Tests for docstoolkit.doc_change_subscriber (E393)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_change_subscriber import (
    DeliveryRecord,
    DocChangeSubscriber,
    SubscriberStats,
    Subscription,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------
class TestSubscriptionDataclass:
    def test_construct_minimal(self):
        s = Subscription(sub_id="x", user_id="u", doc_pattern="*")
        assert s.sub_id == "x"
        assert s.user_id == "u"
        assert s.doc_pattern == "*"

    def test_default_change_types_empty(self):
        s = Subscription(sub_id="x", user_id="u", doc_pattern="*")
        assert s.change_types == []

    def test_change_types_independent_per_instance(self):
        a = Subscription(sub_id="a", user_id="u", doc_pattern="*")
        b = Subscription(sub_id="b", user_id="u", doc_pattern="*")
        a.change_types.append("created")
        assert b.change_types == []

    def test_default_active_true(self):
        s = Subscription(sub_id="x", user_id="u", doc_pattern="*")
        assert s.active is True

    def test_default_created_at_zero(self):
        s = Subscription(sub_id="x", user_id="u", doc_pattern="*")
        assert s.created_at == 0.0

    def test_with_all_fields(self):
        s = Subscription(
            sub_id="x", user_id="u", doc_pattern="docs/*",
            change_types=["updated"], created_at=12.5, active=False,
        )
        assert s.created_at == 12.5
        assert s.active is False
        assert s.change_types == ["updated"]


class TestDeliveryRecordDataclass:
    def test_construct_minimal(self):
        r = DeliveryRecord(record_id=1, sub_id="s", doc_id="d", change_type="updated")
        assert r.record_id == 1
        assert r.sub_id == "s"
        assert r.doc_id == "d"
        assert r.change_type == "updated"

    def test_default_delivered_at_zero(self):
        r = DeliveryRecord(record_id=1, sub_id="s", doc_id="d", change_type="updated")
        assert r.delivered_at == 0.0

    def test_with_timestamp(self):
        r = DeliveryRecord(
            record_id=2, sub_id="s", doc_id="d",
            change_type="updated", delivered_at=42.0,
        )
        assert r.delivered_at == 42.0


class TestSubscriberStatsDataclass:
    def test_construct(self):
        st = SubscriberStats(
            total_subscriptions=4,
            active_subscriptions=3,
            total_deliveries=10,
            unique_subscribers=2,
        )
        assert st.total_subscriptions == 4
        assert st.active_subscriptions == 3
        assert st.total_deliveries == 10
        assert st.unique_subscribers == 2


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_default_construct(self):
        sub = DocChangeSubscriber()
        assert sub.stats().total_subscriptions == 0

    def test_initial_no_deliveries(self):
        sub = DocChangeSubscriber()
        assert sub.stats().total_deliveries == 0

    def test_initial_no_users(self):
        sub = DocChangeSubscriber()
        assert sub.stats().unique_subscribers == 0


# ---------------------------------------------------------------------------
# Subscribe
# ---------------------------------------------------------------------------
class TestSubscribe:
    def test_returns_subscription(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u1", "docs/*")
        assert isinstance(s, Subscription)

    def test_has_unique_id(self):
        sub = DocChangeSubscriber()
        s1 = sub.subscribe("u1", "*")
        s2 = sub.subscribe("u1", "*")
        assert s1.sub_id != s2.sub_id

    def test_stores_user_id(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("alice", "*")
        assert s.user_id == "alice"

    def test_stores_pattern(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "docs/**")
        assert s.doc_pattern == "docs/**"

    def test_default_change_types_empty(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert s.change_types == []

    def test_explicit_change_types(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*", change_types=["created", "updated"])
        assert s.change_types == ["created", "updated"]

    def test_active_by_default(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert s.active is True

    def test_now_default_zero(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert s.created_at == 0.0

    def test_now_custom(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*", now=100.5)
        assert s.created_at == 100.5

    def test_change_types_copied(self):
        """Verify caller-provided list isn't shared."""
        sub = DocChangeSubscriber()
        original = ["created"]
        s = sub.subscribe("u", "*", change_types=original)
        original.append("deleted")
        assert s.change_types == ["created"]

    def test_appears_in_stats(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        assert sub.stats().total_subscriptions == 1


# ---------------------------------------------------------------------------
# Unsubscribe
# ---------------------------------------------------------------------------
class TestUnsubscribe:
    def test_unknown_returns_false(self):
        sub = DocChangeSubscriber()
        assert sub.unsubscribe("nope") is False

    def test_marks_inactive(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert sub.unsubscribe(s.sub_id) is True
        assert sub.get_subscription(s.sub_id).active is False

    def test_idempotent_returns_false_second_time(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        sub.unsubscribe(s.sub_id)
        assert sub.unsubscribe(s.sub_id) is False

    def test_keeps_record_in_storage(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        sub.unsubscribe(s.sub_id)
        assert sub.get_subscription(s.sub_id) is not None


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
class TestDeleteSubscription:
    def test_unknown_returns_false(self):
        sub = DocChangeSubscriber()
        assert sub.delete_subscription("missing") is False

    def test_removes_record(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert sub.delete_subscription(s.sub_id) is True
        assert sub.get_subscription(s.sub_id) is None

    def test_stats_decreases(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        sub.delete_subscription(s.sub_id)
        assert sub.stats().total_subscriptions == 0


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------
class TestGetSubscription:
    def test_unknown_returns_none(self):
        sub = DocChangeSubscriber()
        assert sub.get_subscription("missing") is None

    def test_existing_returns_sub(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert sub.get_subscription(s.sub_id) is s


# ---------------------------------------------------------------------------
# Subscriptions for user
# ---------------------------------------------------------------------------
class TestSubscriptionsForUser:
    def test_empty_when_no_subs(self):
        sub = DocChangeSubscriber()
        assert sub.subscriptions_for_user("u") == []

    def test_only_user_subs(self):
        sub = DocChangeSubscriber()
        a = sub.subscribe("alice", "*")
        sub.subscribe("bob", "*")
        results = sub.subscriptions_for_user("alice")
        assert results == [a]

    def test_active_only_default(self):
        sub = DocChangeSubscriber()
        a = sub.subscribe("u", "*", now=1.0)
        b = sub.subscribe("u", "*", now=2.0)
        sub.unsubscribe(b.sub_id)
        assert sub.subscriptions_for_user("u") == [a]

    def test_active_only_false_includes_inactive(self):
        sub = DocChangeSubscriber()
        a = sub.subscribe("u", "*", now=1.0)
        b = sub.subscribe("u", "*", now=2.0)
        sub.unsubscribe(b.sub_id)
        results = sub.subscriptions_for_user("u", active_only=False)
        assert results == [a, b]

    def test_sorted_by_created_at(self):
        sub = DocChangeSubscriber()
        s2 = sub.subscribe("u", "*", now=5.0)
        s1 = sub.subscribe("u", "*", now=1.0)
        s3 = sub.subscribe("u", "*", now=10.0)
        assert sub.subscriptions_for_user("u") == [s1, s2, s3]


# ---------------------------------------------------------------------------
# Matching
# ---------------------------------------------------------------------------
class TestMatchingSubscriptions:
    def test_no_subs_empty(self):
        sub = DocChangeSubscriber()
        assert sub.matching_subscriptions("d", "updated") == []

    def test_wildcard_matches_all(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert sub.matching_subscriptions("anything", "updated") == [s]

    def test_exact_match(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "docs/foo.md")
        assert sub.matching_subscriptions("docs/foo.md", "x") == [s]

    def test_pattern_no_match(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "docs/foo.md")
        assert sub.matching_subscriptions("docs/bar.md", "x") == []

    def test_prefix_pattern(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "docs/*")
        assert sub.matching_subscriptions("docs/x.md", "updated") == [s]
        assert sub.matching_subscriptions("other/y.md", "updated") == []

    def test_empty_change_types_matches_any(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        assert sub.matching_subscriptions("d", "weird_kind") == [s]

    def test_change_type_allow_list_matches(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*", change_types=["updated"])
        assert sub.matching_subscriptions("d", "updated") == [s]

    def test_change_type_allow_list_excludes(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*", change_types=["updated"])
        assert sub.matching_subscriptions("d", "created") == []

    def test_inactive_excluded(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        sub.unsubscribe(s.sub_id)
        assert sub.matching_subscriptions("d", "updated") == []


# ---------------------------------------------------------------------------
# Dispatch
# ---------------------------------------------------------------------------
class TestDispatch:
    def test_no_matches_empty(self):
        sub = DocChangeSubscriber()
        assert sub.dispatch("d", "updated") == []

    def test_creates_records(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        records = sub.dispatch("d1", "updated")
        assert len(records) == 1
        assert records[0].doc_id == "d1"
        assert records[0].change_type == "updated"

    def test_record_ids_auto_increment(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        r1 = sub.dispatch("d", "u")[0]
        r2 = sub.dispatch("d", "u")[0]
        assert r1.record_id == 1
        assert r2.record_id == 2

    def test_uses_now_timestamp(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        recs = sub.dispatch("d", "updated", now=99.0)
        assert recs[0].delivered_at == 99.0

    def test_inactive_excluded(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        sub.unsubscribe(s.sub_id)
        assert sub.dispatch("d", "updated") == []

    def test_multiple_subscribers(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u1", "*")
        sub.subscribe("u2", "*")
        recs = sub.dispatch("d", "updated")
        assert len(recs) == 2

    def test_change_type_filter(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*", change_types=["updated"])
        assert len(sub.dispatch("d", "updated")) == 1
        assert len(sub.dispatch("d", "deleted")) == 0

    def test_pattern_filter(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "docs/*")
        assert len(sub.dispatch("docs/a", "x")) == 1
        assert len(sub.dispatch("other/a", "x")) == 0

    def test_records_appended_to_history(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        sub.dispatch("d", "x")
        sub.dispatch("d", "x")
        assert sub.stats().total_deliveries == 2


# ---------------------------------------------------------------------------
# Deliveries for sub
# ---------------------------------------------------------------------------
class TestDeliveriesForSub:
    def test_empty(self):
        sub = DocChangeSubscriber()
        assert sub.deliveries_for_sub("nope") == []

    def test_most_recent_first(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        r1 = sub.dispatch("d", "x", now=1.0)[0]
        r2 = sub.dispatch("d", "x", now=2.0)[0]
        r3 = sub.dispatch("d", "x", now=3.0)[0]
        results = sub.deliveries_for_sub(s.sub_id)
        assert [r.record_id for r in results] == [r3.record_id, r2.record_id, r1.record_id]

    def test_limit(self):
        sub = DocChangeSubscriber()
        s = sub.subscribe("u", "*")
        for i in range(5):
            sub.dispatch("d", "x", now=float(i))
        assert len(sub.deliveries_for_sub(s.sub_id, limit=2)) == 2

    def test_only_for_this_sub(self):
        sub = DocChangeSubscriber()
        s1 = sub.subscribe("u", "docs/a")
        s2 = sub.subscribe("u", "docs/b")
        sub.dispatch("docs/a", "x")
        sub.dispatch("docs/b", "x")
        assert len(sub.deliveries_for_sub(s1.sub_id)) == 1
        assert len(sub.deliveries_for_sub(s2.sub_id)) == 1


# ---------------------------------------------------------------------------
# Deliveries for user
# ---------------------------------------------------------------------------
class TestDeliveriesForUser:
    def test_empty(self):
        sub = DocChangeSubscriber()
        assert sub.deliveries_for_user("u") == []

    def test_aggregates_across_subs(self):
        sub = DocChangeSubscriber()
        sub.subscribe("alice", "docs/a")
        sub.subscribe("alice", "docs/b")
        sub.dispatch("docs/a", "x")
        sub.dispatch("docs/b", "x")
        assert len(sub.deliveries_for_user("alice")) == 2

    def test_excludes_other_users(self):
        sub = DocChangeSubscriber()
        sub.subscribe("alice", "*")
        sub.subscribe("bob", "*")
        sub.dispatch("d", "x")
        assert len(sub.deliveries_for_user("alice")) == 1
        assert len(sub.deliveries_for_user("bob")) == 1

    def test_most_recent_first(self):
        sub = DocChangeSubscriber()
        sub.subscribe("alice", "*")
        r1 = sub.dispatch("d", "x", now=1.0)[0]
        r2 = sub.dispatch("d", "x", now=2.0)[0]
        results = sub.deliveries_for_user("alice")
        assert results[0].record_id == r2.record_id
        assert results[1].record_id == r1.record_id

    def test_limit(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        for _ in range(4):
            sub.dispatch("d", "x")
        assert len(sub.deliveries_for_user("u", limit=2)) == 2


# ---------------------------------------------------------------------------
# Clear deliveries
# ---------------------------------------------------------------------------
class TestClearDeliveries:
    def test_empty_returns_zero(self):
        sub = DocChangeSubscriber()
        assert sub.clear_deliveries() == 0

    def test_returns_count(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        sub.dispatch("d", "x")
        sub.dispatch("d", "x")
        sub.dispatch("d", "x")
        assert sub.clear_deliveries() == 3

    def test_clears_records(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        sub.dispatch("d", "x")
        sub.clear_deliveries()
        assert sub.stats().total_deliveries == 0


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty_state(self):
        sub = DocChangeSubscriber()
        st = sub.stats()
        assert st.total_subscriptions == 0
        assert st.active_subscriptions == 0
        assert st.total_deliveries == 0
        assert st.unique_subscribers == 0

    def test_counts_total(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        sub.subscribe("u", "*")
        assert sub.stats().total_subscriptions == 2

    def test_active_vs_total(self):
        sub = DocChangeSubscriber()
        s1 = sub.subscribe("u", "*")
        sub.subscribe("u", "*")
        sub.unsubscribe(s1.sub_id)
        st = sub.stats()
        assert st.total_subscriptions == 2
        assert st.active_subscriptions == 1

    def test_unique_subscribers(self):
        sub = DocChangeSubscriber()
        sub.subscribe("alice", "*")
        sub.subscribe("alice", "*")
        sub.subscribe("bob", "*")
        assert sub.stats().unique_subscribers == 2

    def test_total_deliveries(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")
        sub.dispatch("d", "x")
        sub.dispatch("d", "x")
        assert sub.stats().total_deliveries == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_subscribe(self):
        sub = DocChangeSubscriber()

        def worker():
            for _ in range(50):
                sub.subscribe("u", "*")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert sub.stats().total_subscriptions == 200

    def test_concurrent_dispatch(self):
        sub = DocChangeSubscriber()
        sub.subscribe("u", "*")

        def worker():
            for _ in range(50):
                sub.dispatch("d", "x")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert sub.stats().total_deliveries == 200

    def test_concurrent_subscribe_and_dispatch(self):
        sub = DocChangeSubscriber()
        # seed a subscriber so dispatch produces records
        sub.subscribe("u", "*")

        def subber():
            for _ in range(30):
                sub.subscribe("u", "*")

        def dispatcher():
            for _ in range(30):
                sub.dispatch("d", "x")

        threads = [threading.Thread(target=subber) for _ in range(2)]
        threads += [threading.Thread(target=dispatcher) for _ in range(2)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = sub.stats()
        assert st.total_subscriptions == 61  # 1 seed + 60 from 2 subbers
        # Each dispatch records at least 1 record (matches "u"); we don't pin
        # the exact value because record_ids are well-defined but matching
        # subs grow during the run. We assert it's at least 60 (initial sub).
        assert st.total_deliveries >= 60


if __name__ == "__main__":  # pragma: no cover
    pytest.main([__file__, "-q"])
