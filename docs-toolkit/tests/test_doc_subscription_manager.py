"""Tests for docstoolkit.doc_subscription_manager (E321)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_subscription_manager import (
    DocSubscriptionManager,
    Subscription,
    SubscriptionStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mgr() -> DocSubscriptionManager:
    return DocSubscriptionManager()


# ---------------------------------------------------------------------------
# TestSubscriptionDataclass
# ---------------------------------------------------------------------------

class TestSubscriptionDataclass:
    def test_fields_exist(self):
        s = Subscription(sub_id="s1", user_id="u1", target="doc:1")
        assert s.sub_id == "s1"
        assert s.user_id == "u1"
        assert s.target == "doc:1"

    def test_events_default_empty(self):
        s = Subscription(sub_id="s1", user_id="u1", target="t")
        assert s.events == []

    def test_created_at_default_zero(self):
        s = Subscription(sub_id="s1", user_id="u1", target="t")
        assert s.created_at == 0.0

    def test_active_default_true(self):
        s = Subscription(sub_id="s1", user_id="u1", target="t")
        assert s.active is True

    def test_events_independent(self):
        """Each instance gets its own list."""
        a = Subscription(sub_id="a", user_id="u", target="t")
        b = Subscription(sub_id="b", user_id="u", target="t")
        a.events.append("x")
        assert b.events == []

    def test_custom_values(self):
        s = Subscription(
            sub_id="x", user_id="alice", target="topic:news",
            events=["edit", "delete"], created_at=1000.0, active=False,
        )
        assert s.events == ["edit", "delete"]
        assert s.created_at == 1000.0
        assert s.active is False


# ---------------------------------------------------------------------------
# TestSubscriptionStatsDataclass
# ---------------------------------------------------------------------------

class TestSubscriptionStatsDataclass:
    def test_fields(self):
        st = SubscriptionStats(
            total_subscriptions=10,
            active_subscriptions=7,
            unique_users=3,
            unique_targets=5,
        )
        assert st.total_subscriptions == 10
        assert st.active_subscriptions == 7
        assert st.unique_users == 3
        assert st.unique_targets == 5

    def test_zero_stats(self):
        st = SubscriptionStats(0, 0, 0, 0)
        assert st.total_subscriptions == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_manager(self):
        mgr = _mgr()
        s = mgr.stats()
        assert s.total_subscriptions == 0
        assert s.active_subscriptions == 0
        assert s.unique_users == 0
        assert s.unique_targets == 0

    def test_multiple_managers_independent(self):
        m1 = _mgr()
        m2 = _mgr()
        m1.subscribe("u1", "doc:1")
        assert m2.stats().total_subscriptions == 0


# ---------------------------------------------------------------------------
# TestSubscribe
# ---------------------------------------------------------------------------

class TestSubscribe:
    def test_returns_subscription(self):
        sub = _mgr().subscribe("alice", "doc:42")
        assert isinstance(sub, Subscription)

    def test_uuid_sub_id(self):
        import uuid
        sub = _mgr().subscribe("alice", "doc:42")
        uuid.UUID(sub.sub_id)  # raises if not valid UUID

    def test_user_id_stored(self):
        sub = _mgr().subscribe("bob", "topic:news")
        assert sub.user_id == "bob"

    def test_target_stored(self):
        sub = _mgr().subscribe("alice", "topic:news")
        assert sub.target == "topic:news"

    def test_active_true(self):
        sub = _mgr().subscribe("u", "t")
        assert sub.active is True

    def test_events_none_defaults_to_empty(self):
        sub = _mgr().subscribe("u", "t", events=None)
        assert sub.events == []

    def test_events_stored(self):
        sub = _mgr().subscribe("u", "t", events=["edit", "publish"])
        assert sub.events == ["edit", "publish"]

    def test_events_copied(self):
        evs = ["edit"]
        sub = _mgr().subscribe("u", "t", events=evs)
        evs.append("delete")
        assert sub.events == ["edit"]

    def test_now_param_used(self):
        sub = _mgr().subscribe("u", "t", now=9999.0)
        assert sub.created_at == 9999.0

    def test_timestamp_set_when_now_none(self):
        before = time.time()
        sub = _mgr().subscribe("u", "t")
        after = time.time()
        assert before <= sub.created_at <= after

    def test_unique_sub_ids(self):
        mgr = _mgr()
        ids = {mgr.subscribe("u", "t").sub_id for _ in range(20)}
        assert len(ids) == 20

    def test_multiple_subs_same_user(self):
        mgr = _mgr()
        s1 = mgr.subscribe("u", "doc:1")
        s2 = mgr.subscribe("u", "doc:2")
        assert s1.sub_id != s2.sub_id

    def test_wildcard_target(self):
        sub = _mgr().subscribe("u", "*")
        assert sub.target == "*"


# ---------------------------------------------------------------------------
# TestUnsubscribe
# ---------------------------------------------------------------------------

class TestUnsubscribe:
    def test_returns_true_when_found(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        assert mgr.unsubscribe(sub.sub_id) is True

    def test_returns_false_when_not_found(self):
        assert _mgr().unsubscribe("nonexistent") is False

    def test_sets_active_false(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.unsubscribe(sub.sub_id)
        assert mgr.get(sub.sub_id).active is False

    def test_does_not_remove_subscription(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.unsubscribe(sub.sub_id)
        assert mgr.get(sub.sub_id) is not None

    def test_idempotent(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.unsubscribe(sub.sub_id)
        assert mgr.unsubscribe(sub.sub_id) is True  # still found, already inactive


# ---------------------------------------------------------------------------
# TestReactivate
# ---------------------------------------------------------------------------

class TestReactivate:
    def test_returns_true_when_found(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.unsubscribe(sub.sub_id)
        assert mgr.reactivate(sub.sub_id) is True

    def test_returns_false_when_not_found(self):
        assert _mgr().reactivate("nonexistent") is False

    def test_sets_active_true(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.unsubscribe(sub.sub_id)
        mgr.reactivate(sub.sub_id)
        assert mgr.get(sub.sub_id).active is True

    def test_already_active_still_returns_true(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        assert mgr.reactivate(sub.sub_id) is True


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_returns_true_when_existed(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        assert mgr.delete(sub.sub_id) is True

    def test_returns_false_when_not_existed(self):
        assert _mgr().delete("nonexistent") is False

    def test_get_returns_none_after_delete(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.delete(sub.sub_id)
        assert mgr.get(sub.sub_id) is None

    def test_not_in_user_index_after_delete(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.delete(sub.sub_id)
        assert mgr.subscriptions_for_user("u", active_only=False) == []

    def test_not_in_target_index_after_delete(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.delete(sub.sub_id)
        assert mgr.subscriptions_for_target("t", active_only=False) == []

    def test_second_delete_returns_false(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.delete(sub.sub_id)
        assert mgr.delete(sub.sub_id) is False


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------

class TestGet:
    def test_get_existing(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        found = mgr.get(sub.sub_id)
        assert found is sub

    def test_get_nonexistent(self):
        assert _mgr().get("missing") is None


# ---------------------------------------------------------------------------
# TestSubscriptionsForUser
# ---------------------------------------------------------------------------

class TestSubscriptionsForUser:
    def test_returns_empty_for_unknown_user(self):
        assert _mgr().subscriptions_for_user("nobody") == []

    def test_returns_active_subscriptions(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "t")
        result = mgr.subscriptions_for_user("u")
        assert s in result

    def test_active_only_excludes_inactive(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "t")
        mgr.unsubscribe(s.sub_id)
        assert mgr.subscriptions_for_user("u", active_only=True) == []

    def test_active_only_false_includes_inactive(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "t")
        mgr.unsubscribe(s.sub_id)
        result = mgr.subscriptions_for_user("u", active_only=False)
        assert s in result

    def test_sorted_by_created_at(self):
        mgr = _mgr()
        s1 = mgr.subscribe("u", "t1", now=200.0)
        s2 = mgr.subscribe("u", "t2", now=100.0)
        s3 = mgr.subscribe("u", "t3", now=300.0)
        result = mgr.subscriptions_for_user("u")
        assert result == [s2, s1, s3]

    def test_only_own_user(self):
        mgr = _mgr()
        mgr.subscribe("alice", "t")
        mgr.subscribe("bob", "t")
        assert all(s.user_id == "alice" for s in mgr.subscriptions_for_user("alice"))


# ---------------------------------------------------------------------------
# TestSubscriptionsForTarget
# ---------------------------------------------------------------------------

class TestSubscriptionsForTarget:
    def test_returns_empty_for_unknown_target(self):
        assert _mgr().subscriptions_for_target("unknown") == []

    def test_returns_active_subscriptions(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "doc:5")
        assert s in mgr.subscriptions_for_target("doc:5")

    def test_active_only_excludes_inactive(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "doc:5")
        mgr.unsubscribe(s.sub_id)
        assert mgr.subscriptions_for_target("doc:5", active_only=True) == []

    def test_active_only_false_includes_inactive(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "doc:5")
        mgr.unsubscribe(s.sub_id)
        result = mgr.subscriptions_for_target("doc:5", active_only=False)
        assert s in result

    def test_sorted_by_created_at(self):
        mgr = _mgr()
        s1 = mgr.subscribe("u1", "t", now=50.0)
        s2 = mgr.subscribe("u2", "t", now=10.0)
        s3 = mgr.subscribe("u3", "t", now=80.0)
        result = mgr.subscriptions_for_target("t")
        assert result == [s2, s1, s3]

    def test_only_own_target(self):
        mgr = _mgr()
        mgr.subscribe("u", "topic:a")
        mgr.subscribe("u", "topic:b")
        result = mgr.subscriptions_for_target("topic:a")
        assert all(s.target == "topic:a" for s in result)


# ---------------------------------------------------------------------------
# TestSubscribersForTarget
# ---------------------------------------------------------------------------

class TestSubscribersForTarget:
    def test_empty_for_unknown_target(self):
        assert _mgr().subscribers_for_target("unknown") == []

    def test_returns_user_ids(self):
        mgr = _mgr()
        mgr.subscribe("charlie", "doc:7")
        mgr.subscribe("alice", "doc:7")
        result = mgr.subscribers_for_target("doc:7")
        assert "alice" in result
        assert "charlie" in result

    def test_sorted(self):
        mgr = _mgr()
        mgr.subscribe("charlie", "t")
        mgr.subscribe("alice", "t")
        mgr.subscribe("bob", "t")
        assert mgr.subscribers_for_target("t") == ["alice", "bob", "charlie"]

    def test_unique_user_ids(self):
        mgr = _mgr()
        mgr.subscribe("alice", "t")
        mgr.subscribe("alice", "t")  # second subscription same user
        assert mgr.subscribers_for_target("t") == ["alice"]

    def test_inactive_excluded(self):
        mgr = _mgr()
        s = mgr.subscribe("alice", "t")
        mgr.unsubscribe(s.sub_id)
        assert mgr.subscribers_for_target("t") == []

    def test_reactivated_included(self):
        mgr = _mgr()
        s = mgr.subscribe("alice", "t")
        mgr.unsubscribe(s.sub_id)
        mgr.reactivate(s.sub_id)
        assert "alice" in mgr.subscribers_for_target("t")


# ---------------------------------------------------------------------------
# TestMatches
# ---------------------------------------------------------------------------

class TestMatches:
    def test_empty_events_matches_any_event(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1", events=[])
        result = mgr.matches("u", "doc:1", "edit")
        assert len(result) == 1

    def test_event_in_list_matches(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1", events=["edit", "publish"])
        assert len(mgr.matches("u", "doc:1", "edit")) == 1

    def test_event_not_in_list_no_match(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1", events=["publish"])
        assert mgr.matches("u", "doc:1", "delete") == []

    def test_inactive_excluded(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "doc:1")
        mgr.unsubscribe(s.sub_id)
        assert mgr.matches("u", "doc:1", "edit") == []

    def test_wrong_user_no_match(self):
        mgr = _mgr()
        mgr.subscribe("alice", "doc:1")
        assert mgr.matches("bob", "doc:1", "edit") == []

    def test_wrong_target_no_match(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1")
        assert mgr.matches("u", "doc:2", "edit") == []

    def test_multiple_matching_subs(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1", events=[])
        mgr.subscribe("u", "doc:1", events=["edit"])
        result = mgr.matches("u", "doc:1", "edit")
        assert len(result) == 2

    def test_partial_match_only_relevant(self):
        mgr = _mgr()
        mgr.subscribe("u", "doc:1", events=["publish"])
        mgr.subscribe("u", "doc:1", events=["edit"])
        result = mgr.matches("u", "doc:1", "edit")
        assert len(result) == 1
        assert result[0].events == ["edit"]


# ---------------------------------------------------------------------------
# TestDeactivateAll
# ---------------------------------------------------------------------------

class TestDeactivateAll:
    def test_returns_count_deactivated(self):
        mgr = _mgr()
        mgr.subscribe("u", "t1")
        mgr.subscribe("u", "t2")
        mgr.subscribe("u", "t3")
        assert mgr.deactivate_all("u") == 3

    def test_all_become_inactive(self):
        mgr = _mgr()
        mgr.subscribe("u", "t1")
        mgr.subscribe("u", "t2")
        mgr.deactivate_all("u")
        assert mgr.subscriptions_for_user("u", active_only=True) == []

    def test_already_inactive_not_counted(self):
        mgr = _mgr()
        s = mgr.subscribe("u", "t")
        mgr.unsubscribe(s.sub_id)
        count = mgr.deactivate_all("u")
        assert count == 0

    def test_other_users_unaffected(self):
        mgr = _mgr()
        mgr.subscribe("alice", "t")
        mgr.subscribe("bob", "t")
        mgr.deactivate_all("alice")
        assert len(mgr.subscriptions_for_user("bob")) == 1

    def test_unknown_user_returns_zero(self):
        assert _mgr().deactivate_all("nobody") == 0


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        s = _mgr().stats()
        assert s.total_subscriptions == 0
        assert s.active_subscriptions == 0
        assert s.unique_users == 0
        assert s.unique_targets == 0

    def test_counts_total_and_active(self):
        mgr = _mgr()
        s1 = mgr.subscribe("u1", "t1")
        s2 = mgr.subscribe("u2", "t2")
        mgr.unsubscribe(s2.sub_id)
        st = mgr.stats()
        assert st.total_subscriptions == 2
        assert st.active_subscriptions == 1

    def test_unique_users(self):
        mgr = _mgr()
        mgr.subscribe("alice", "t1")
        mgr.subscribe("alice", "t2")
        mgr.subscribe("bob", "t1")
        assert mgr.stats().unique_users == 2

    def test_unique_targets(self):
        mgr = _mgr()
        mgr.subscribe("u1", "doc:1")
        mgr.subscribe("u2", "doc:1")
        mgr.subscribe("u3", "doc:2")
        assert mgr.stats().unique_targets == 2

    def test_stats_after_delete(self):
        mgr = _mgr()
        sub = mgr.subscribe("u", "t")
        mgr.delete(sub.sub_id)
        st = mgr.stats()
        assert st.total_subscriptions == 0
        assert st.unique_users == 0

    def test_stats_returns_dataclass(self):
        assert isinstance(_mgr().stats(), SubscriptionStats)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_subscribe(self):
        mgr = _mgr()
        results: list[Subscription] = []
        errors: list[Exception] = []
        lock = threading.Lock()

        def worker(uid: str) -> None:
            try:
                sub = mgr.subscribe(uid, "shared-target")
                with lock:
                    results.append(sub)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker, args=(f"user-{i}",)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert len(results) == 50
        assert mgr.stats().total_subscriptions == 50

    def test_concurrent_subscribe_unsubscribe(self):
        mgr = _mgr()
        subs = [mgr.subscribe(f"u{i}", "t") for i in range(20)]
        errors: list[Exception] = []
        lock = threading.Lock()

        def unsub(s: Subscription) -> None:
            try:
                mgr.unsubscribe(s.sub_id)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=unsub, args=(s,)) for s in subs]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        assert mgr.stats().active_subscriptions == 0

    def test_concurrent_subscribe_unique_ids(self):
        mgr = _mgr()
        ids: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            sub = mgr.subscribe("u", "t")
            with lock:
                ids.append(sub.sub_id)

        threads = [threading.Thread(target=worker) for _ in range(100)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(set(ids)) == 100
