"""Tests for docstoolkit.doc_share_audit (E402)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_share_audit import (
    AuditStats,
    DocShareAudit,
    ShareEvent,
)


# ---------------------------------------------------------------------------
# TestShareEventDataclass
# ---------------------------------------------------------------------------

class TestShareEventDataclass:
    def test_defaults(self):
        ev = ShareEvent()
        assert ev.event_id == 0
        assert ev.doc_id == ""
        assert ev.actor == ""
        assert ev.target == ""
        assert ev.action == ""
        assert ev.permissions == []
        assert ev.timestamp == 0.0
        assert ev.note == ""

    def test_custom_values(self):
        ev = ShareEvent(
            event_id=1,
            doc_id="d1",
            actor="alice",
            target="bob",
            action="share",
            permissions=["read", "comment"],
            timestamp=123.45,
            note="hello",
        )
        assert ev.event_id == 1
        assert ev.doc_id == "d1"
        assert ev.actor == "alice"
        assert ev.target == "bob"
        assert ev.action == "share"
        assert ev.permissions == ["read", "comment"]
        assert ev.timestamp == 123.45
        assert ev.note == "hello"

    def test_permissions_default_is_independent(self):
        a = ShareEvent()
        b = ShareEvent()
        a.permissions.append("read")
        assert b.permissions == []

    def test_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(ShareEvent)


# ---------------------------------------------------------------------------
# TestAuditStatsDataclass
# ---------------------------------------------------------------------------

class TestAuditStatsDataclass:
    def test_defaults(self):
        s = AuditStats()
        assert s.total_events == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.unique_targets == 0
        assert s.action_counts == {}

    def test_custom(self):
        s = AuditStats(
            total_events=5,
            unique_docs=2,
            unique_actors=3,
            unique_targets=4,
            action_counts={"share": 3, "unshare": 2},
        )
        assert s.total_events == 5
        assert s.unique_docs == 2
        assert s.unique_actors == 3
        assert s.unique_targets == 4
        assert s.action_counts == {"share": 3, "unshare": 2}

    def test_action_counts_independent(self):
        a = AuditStats()
        b = AuditStats()
        a.action_counts["x"] = 1
        assert b.action_counts == {}

    def test_is_dataclass(self):
        from dataclasses import is_dataclass
        assert is_dataclass(AuditStats)


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_audit(self):
        a = DocShareAudit()
        assert a.stats().total_events == 0

    def test_initial_next_id(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share", now=1.0)
        assert ev.event_id == 1

    def test_independent_instances(self):
        a = DocShareAudit()
        b = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        assert b.stats().total_events == 0


# ---------------------------------------------------------------------------
# TestLogEvent
# ---------------------------------------------------------------------------

class TestLogEvent:
    def test_returns_event(self):
        a = DocShareAudit()
        ev = a.log_event("d", "alice", "bob", "share", now=1.0)
        assert isinstance(ev, ShareEvent)
        assert ev.doc_id == "d"
        assert ev.actor == "alice"
        assert ev.target == "bob"
        assert ev.action == "share"

    def test_id_increments(self):
        a = DocShareAudit()
        e1 = a.log_event("d", "u", "t", "share", now=1.0)
        e2 = a.log_event("d", "u", "t", "share", now=2.0)
        e3 = a.log_event("d", "u", "t", "share", now=3.0)
        assert e1.event_id == 1
        assert e2.event_id == 2
        assert e3.event_id == 3

    def test_uses_now(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share", now=42.0)
        assert ev.timestamp == 42.0

    def test_uses_time_when_now_none(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share")
        assert ev.timestamp > 0

    def test_permissions_copied(self):
        a = DocShareAudit()
        perms = ["read", "write"]
        ev = a.log_event("d", "u", "t", "share", permissions=perms, now=1.0)
        perms.append("admin")
        assert ev.permissions == ["read", "write"]

    def test_permissions_default_empty(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share", now=1.0)
        assert ev.permissions == []

    def test_note_default_empty(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share", now=1.0)
        assert ev.note == ""

    def test_note_set(self):
        a = DocShareAudit()
        ev = a.log_event("d", "u", "t", "share", note="hi", now=1.0)
        assert ev.note == "hi"


# ---------------------------------------------------------------------------
# TestGetEvent
# ---------------------------------------------------------------------------

class TestGetEvent:
    def test_get_existing(self):
        a = DocShareAudit()
        e1 = a.log_event("d", "u", "t", "share", now=1.0)
        assert a.get_event(e1.event_id) is e1

    def test_get_missing(self):
        a = DocShareAudit()
        assert a.get_event(999) is None

    def test_get_zero(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        assert a.get_event(0) is None

    def test_get_negative(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        assert a.get_event(-1) is None

    def test_get_after_delete(self):
        a = DocShareAudit()
        e1 = a.log_event("d", "u", "t", "share", now=1.0)
        e2 = a.log_event("d", "u", "t", "share", now=2.0)
        a.delete_old(1.5)
        assert a.get_event(e1.event_id) is None
        assert a.get_event(e2.event_id).event_id == e2.event_id


# ---------------------------------------------------------------------------
# TestEventsForDoc
# ---------------------------------------------------------------------------

class TestEventsForDoc:
    def test_empty(self):
        a = DocShareAudit()
        assert a.events_for_doc("d") == []

    def test_most_recent_first(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t1", "share", now=1.0)
        a.log_event("d", "u", "t2", "share", now=2.0)
        a.log_event("d", "u", "t3", "share", now=3.0)
        evs = a.events_for_doc("d")
        assert [e.target for e in evs] == ["t3", "t2", "t1"]

    def test_filters_by_doc(self):
        a = DocShareAudit()
        a.log_event("d1", "u", "t", "share", now=1.0)
        a.log_event("d2", "u", "t", "share", now=2.0)
        assert len(a.events_for_doc("d1")) == 1
        assert len(a.events_for_doc("d2")) == 1

    def test_action_filter(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "unshare", now=2.0)
        a.log_event("d", "u", "t", "share", now=3.0)
        evs = a.events_for_doc("d", action="share")
        assert len(evs) == 2
        assert all(e.action == "share" for e in evs)

    def test_limit(self):
        a = DocShareAudit()
        for i in range(5):
            a.log_event("d", "u", "t", "share", now=float(i))
        evs = a.events_for_doc("d", limit=2)
        assert len(evs) == 2
        assert evs[0].timestamp == 4.0
        assert evs[1].timestamp == 3.0


# ---------------------------------------------------------------------------
# TestEventsForActor
# ---------------------------------------------------------------------------

class TestEventsForActor:
    def test_empty(self):
        a = DocShareAudit()
        assert a.events_for_actor("u") == []

    def test_most_recent_first(self):
        a = DocShareAudit()
        a.log_event("d", "alice", "t", "share", now=1.0)
        a.log_event("d", "alice", "t", "share", now=2.0)
        evs = a.events_for_actor("alice")
        assert evs[0].timestamp == 2.0
        assert evs[1].timestamp == 1.0

    def test_filters_by_actor(self):
        a = DocShareAudit()
        a.log_event("d", "alice", "t", "share", now=1.0)
        a.log_event("d", "bob", "t", "share", now=2.0)
        assert len(a.events_for_actor("alice")) == 1
        assert len(a.events_for_actor("bob")) == 1
        assert len(a.events_for_actor("carol")) == 0

    def test_limit(self):
        a = DocShareAudit()
        for i in range(4):
            a.log_event("d", "alice", "t", "share", now=float(i))
        assert len(a.events_for_actor("alice", limit=2)) == 2


# ---------------------------------------------------------------------------
# TestEventsForTarget
# ---------------------------------------------------------------------------

class TestEventsForTarget:
    def test_empty(self):
        a = DocShareAudit()
        assert a.events_for_target("t") == []

    def test_most_recent_first(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", now=1.0)
        a.log_event("d", "u", "bob", "share", now=2.0)
        evs = a.events_for_target("bob")
        assert evs[0].timestamp == 2.0
        assert evs[1].timestamp == 1.0

    def test_filters_by_target(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", now=1.0)
        a.log_event("d", "u", "carol", "share", now=2.0)
        assert len(a.events_for_target("bob")) == 1
        assert len(a.events_for_target("carol")) == 1

    def test_limit(self):
        a = DocShareAudit()
        for i in range(5):
            a.log_event("d", "u", "bob", "share", now=float(i))
        assert len(a.events_for_target("bob", limit=3)) == 3


# ---------------------------------------------------------------------------
# TestEventsByAction
# ---------------------------------------------------------------------------

class TestEventsByAction:
    def test_empty(self):
        a = DocShareAudit()
        assert a.events_by_action("share") == []

    def test_filters_by_action(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "unshare", now=2.0)
        a.log_event("d", "u", "t", "share", now=3.0)
        assert len(a.events_by_action("share")) == 2
        assert len(a.events_by_action("unshare")) == 1
        assert len(a.events_by_action("revoke")) == 0

    def test_most_recent_first(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=2.0)
        a.log_event("d", "u", "t", "share", now=3.0)
        evs = a.events_by_action("share")
        assert [e.timestamp for e in evs] == [3.0, 2.0, 1.0]

    def test_limit(self):
        a = DocShareAudit()
        for i in range(5):
            a.log_event("d", "u", "t", "share", now=float(i))
        assert len(a.events_by_action("share", limit=2)) == 2


# ---------------------------------------------------------------------------
# TestEventsInRange
# ---------------------------------------------------------------------------

class TestEventsInRange:
    def test_empty(self):
        a = DocShareAudit()
        assert a.events_in_range(0.0, 100.0) == []

    def test_inclusive_bounds(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=2.0)
        a.log_event("d", "u", "t", "share", now=3.0)
        evs = a.events_in_range(1.0, 3.0)
        assert len(evs) == 3

    def test_exclusive_outside(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=5.0)
        evs = a.events_in_range(2.0, 4.0)
        assert evs == []

    def test_ascending_order(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=3.0)
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=2.0)
        evs = a.events_in_range(0.0, 10.0)
        assert [e.timestamp for e in evs] == [1.0, 2.0, 3.0]

    def test_doc_filter(self):
        a = DocShareAudit()
        a.log_event("d1", "u", "t", "share", now=1.0)
        a.log_event("d2", "u", "t", "share", now=2.0)
        evs = a.events_in_range(0.0, 10.0, doc_id="d1")
        assert len(evs) == 1
        assert evs[0].doc_id == "d1"


# ---------------------------------------------------------------------------
# TestCurrentShares
# ---------------------------------------------------------------------------

class TestCurrentShares:
    def test_empty(self):
        a = DocShareAudit()
        assert a.current_shares("d") == {}

    def test_single_share(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        assert a.current_shares("d") == {"bob": ["read"]}

    def test_multiple_targets(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d", "u", "carol", "share", permissions=["write"], now=2.0)
        cs = a.current_shares("d")
        assert cs == {"bob": ["read"], "carol": ["write"]}

    def test_unshare_removes(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d", "u", "bob", "unshare", now=2.0)
        assert a.current_shares("d") == {}

    def test_revoke_removes(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d", "u", "bob", "revoke", now=2.0)
        assert a.current_shares("d") == {}

    def test_modify_replaces(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d", "u", "bob", "modify", permissions=["read", "write"], now=2.0)
        assert a.current_shares("d") == {"bob": ["read", "write"]}

    def test_replay_order_by_timestamp(self):
        a = DocShareAudit()
        # log out of timestamp order
        a.log_event("d", "u", "bob", "modify", permissions=["write"], now=3.0)
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        # replay should apply share(t=1) then modify(t=3) → write
        assert a.current_shares("d") == {"bob": ["write"]}

    def test_unshare_then_reshare(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d", "u", "bob", "unshare", now=2.0)
        a.log_event("d", "u", "bob", "share", permissions=["admin"], now=3.0)
        assert a.current_shares("d") == {"bob": ["admin"]}

    def test_separate_docs(self):
        a = DocShareAudit()
        a.log_event("d1", "u", "bob", "share", permissions=["read"], now=1.0)
        a.log_event("d2", "u", "carol", "share", permissions=["write"], now=2.0)
        assert a.current_shares("d1") == {"bob": ["read"]}
        assert a.current_shares("d2") == {"carol": ["write"]}


# ---------------------------------------------------------------------------
# TestDeleteOld
# ---------------------------------------------------------------------------

class TestDeleteOld:
    def test_empty(self):
        a = DocShareAudit()
        assert a.delete_old(100.0) == 0

    def test_removes_old(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=5.0)
        a.log_event("d", "u", "t", "share", now=10.0)
        removed = a.delete_old(6.0)
        assert removed == 2
        assert a.stats().total_events == 1

    def test_returns_count(self):
        a = DocShareAudit()
        for i in range(5):
            a.log_event("d", "u", "t", "share", now=float(i))
        # i=0..4 → drop those strictly < 3.0 → 0,1,2 → 3 removed
        assert a.delete_old(3.0) == 3

    def test_indexes_rebuilt(self):
        a = DocShareAudit()
        a.log_event("d1", "alice", "bob", "share", now=1.0)
        a.log_event("d2", "alice", "carol", "share", now=10.0)
        a.delete_old(5.0)
        assert len(a.events_for_doc("d1")) == 0
        assert len(a.events_for_doc("d2")) == 1
        assert len(a.events_for_actor("alice")) == 1
        assert len(a.events_for_target("bob")) == 0
        assert len(a.events_for_target("carol")) == 1

    def test_keeps_exact_boundary(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=5.0)
        # strict <  → 5.0 is kept when before_timestamp=5.0
        assert a.delete_old(5.0) == 0
        assert a.stats().total_events == 1


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty(self):
        a = DocShareAudit()
        s = a.stats()
        assert s.total_events == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.unique_targets == 0
        assert s.action_counts == {}

    def test_total_events(self):
        a = DocShareAudit()
        for i in range(7):
            a.log_event("d", "u", "t", "share", now=float(i))
        assert a.stats().total_events == 7

    def test_unique_docs(self):
        a = DocShareAudit()
        a.log_event("d1", "u", "t", "share", now=1.0)
        a.log_event("d2", "u", "t", "share", now=2.0)
        a.log_event("d1", "u", "t", "share", now=3.0)
        assert a.stats().unique_docs == 2

    def test_unique_actors(self):
        a = DocShareAudit()
        a.log_event("d", "alice", "t", "share", now=1.0)
        a.log_event("d", "bob", "t", "share", now=2.0)
        a.log_event("d", "alice", "t", "share", now=3.0)
        assert a.stats().unique_actors == 2

    def test_unique_targets(self):
        a = DocShareAudit()
        a.log_event("d", "u", "bob", "share", now=1.0)
        a.log_event("d", "u", "carol", "share", now=2.0)
        a.log_event("d", "u", "bob", "share", now=3.0)
        assert a.stats().unique_targets == 2

    def test_action_counts(self):
        a = DocShareAudit()
        a.log_event("d", "u", "t", "share", now=1.0)
        a.log_event("d", "u", "t", "share", now=2.0)
        a.log_event("d", "u", "t", "unshare", now=3.0)
        a.log_event("d", "u", "t", "modify", now=4.0)
        ac = a.stats().action_counts
        assert ac == {"share": 2, "unshare": 1, "modify": 1}


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_log_event(self):
        a = DocShareAudit()
        N = 50
        THREADS = 8

        def worker(idx: int):
            for i in range(N):
                a.log_event(f"d{idx}", "u", "t", "share", now=float(i))

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = a.stats()
        assert s.total_events == N * THREADS
        ids = {ev.event_id for ev in a._events}
        assert len(ids) == N * THREADS  # all unique
        assert min(ids) == 1
        assert max(ids) == N * THREADS

    def test_concurrent_log_and_read(self):
        a = DocShareAudit()

        def writer():
            for i in range(100):
                a.log_event("d", "u", "t", "share", now=float(i))

        def reader():
            for _ in range(100):
                a.events_for_doc("d")
                a.stats()

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=writer),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert a.stats().total_events == 200
