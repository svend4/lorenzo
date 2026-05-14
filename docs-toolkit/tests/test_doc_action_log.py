"""Tests for E398 DocActionLog."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_action_log import ActionEvent, ActionStats, DocActionLog


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestActionEventDataclass:
    def test_minimal_construction(self):
        ev = ActionEvent(event_id=1, doc_id="d", actor="a", action="x")
        assert ev.event_id == 1
        assert ev.doc_id == "d"
        assert ev.actor == "a"
        assert ev.action == "x"

    def test_default_timestamp(self):
        ev = ActionEvent(event_id=1, doc_id="d", actor="a", action="x")
        assert ev.timestamp == 0.0

    def test_default_payload_is_empty_dict(self):
        ev = ActionEvent(event_id=1, doc_id="d", actor="a", action="x")
        assert ev.payload == {}

    def test_payload_default_factory_isolated(self):
        a = ActionEvent(event_id=1, doc_id="d", actor="a", action="x")
        b = ActionEvent(event_id=2, doc_id="d", actor="a", action="x")
        a.payload["k"] = 1
        assert b.payload == {}

    def test_default_success_true(self):
        ev = ActionEvent(event_id=1, doc_id="d", actor="a", action="x")
        assert ev.success is True

    def test_explicit_fields(self):
        ev = ActionEvent(
            event_id=7,
            doc_id="doc",
            actor="alice",
            action="edit",
            timestamp=123.0,
            payload={"k": "v"},
            success=False,
        )
        assert ev.event_id == 7
        assert ev.timestamp == 123.0
        assert ev.payload == {"k": "v"}
        assert ev.success is False


class TestActionStatsDataclass:
    def test_construct(self):
        s = ActionStats(
            total_events=10,
            success_count=7,
            failure_count=3,
            unique_docs=2,
            unique_actors=4,
            unique_actions=5,
        )
        assert s.total_events == 10
        assert s.success_count == 7
        assert s.failure_count == 3
        assert s.unique_docs == 2
        assert s.unique_actors == 4
        assert s.unique_actions == 5

    def test_zero_stats(self):
        s = ActionStats(0, 0, 0, 0, 0, 0)
        assert s.total_events == 0
        assert s.success_count == 0


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_log_stats(self):
        log = DocActionLog()
        s = log.stats()
        assert s.total_events == 0
        assert s.success_count == 0
        assert s.failure_count == 0

    def test_empty_queries(self):
        log = DocActionLog()
        assert log.events_for_doc("nope") == []
        assert log.events_for_actor("nope") == []
        assert log.events_by_action("nope") == []
        assert log.failed_events() == []
        assert log.action_counts() == {}
        assert log.actor_counts() == {}

    def test_get_event_missing(self):
        log = DocActionLog()
        assert log.get_event(1) is None


# ---------------------------------------------------------------------------
# log_action
# ---------------------------------------------------------------------------


class TestLogAction:
    def test_returns_event(self):
        log = DocActionLog()
        ev = log.log_action("doc", "alice", "create")
        assert isinstance(ev, ActionEvent)
        assert ev.event_id == 1
        assert ev.doc_id == "doc"
        assert ev.actor == "alice"
        assert ev.action == "create"

    def test_id_increments(self):
        log = DocActionLog()
        a = log.log_action("d", "u", "x")
        b = log.log_action("d", "u", "x")
        c = log.log_action("d", "u", "x")
        assert (a.event_id, b.event_id, c.event_id) == (1, 2, 3)

    def test_default_success_true(self):
        log = DocActionLog()
        ev = log.log_action("d", "u", "x")
        assert ev.success is True

    def test_explicit_failure(self):
        log = DocActionLog()
        ev = log.log_action("d", "u", "x", success=False)
        assert ev.success is False

    def test_payload_is_copied(self):
        log = DocActionLog()
        original = {"k": 1}
        ev = log.log_action("d", "u", "x", payload=original)
        original["k"] = 999
        assert ev.payload == {"k": 1}

    def test_payload_default_empty(self):
        log = DocActionLog()
        ev = log.log_action("d", "u", "x")
        assert ev.payload == {}

    def test_explicit_now(self):
        log = DocActionLog()
        ev = log.log_action("d", "u", "x", now=42.5)
        assert ev.timestamp == 42.5

    def test_default_now_uses_time_time(self):
        log = DocActionLog()
        before = time.time()
        ev = log.log_action("d", "u", "x")
        after = time.time()
        assert before <= ev.timestamp <= after

    def test_event_indexed_by_doc(self):
        log = DocActionLog()
        log.log_action("doc1", "u", "x")
        assert len(log.events_for_doc("doc1")) == 1

    def test_event_indexed_by_actor(self):
        log = DocActionLog()
        log.log_action("d", "alice", "x")
        assert len(log.events_for_actor("alice")) == 1

    def test_event_indexed_by_action(self):
        log = DocActionLog()
        log.log_action("d", "u", "edit")
        assert len(log.events_by_action("edit")) == 1


# ---------------------------------------------------------------------------
# get_event
# ---------------------------------------------------------------------------


class TestGetEvent:
    def test_get_existing(self):
        log = DocActionLog()
        ev = log.log_action("d", "u", "x")
        fetched = log.get_event(ev.event_id)
        assert fetched is ev

    def test_get_missing(self):
        log = DocActionLog()
        log.log_action("d", "u", "x")
        assert log.get_event(99) is None

    def test_get_zero(self):
        log = DocActionLog()
        log.log_action("d", "u", "x")
        assert log.get_event(0) is None

    def test_get_after_multiple(self):
        log = DocActionLog()
        for _ in range(5):
            log.log_action("d", "u", "x")
        assert log.get_event(3).event_id == 3


# ---------------------------------------------------------------------------
# events_for_doc
# ---------------------------------------------------------------------------


class TestEventsForDoc:
    def test_most_recent_first(self):
        log = DocActionLog()
        a = log.log_action("doc", "u", "x", now=1.0)
        b = log.log_action("doc", "u", "x", now=2.0)
        c = log.log_action("doc", "u", "x", now=3.0)
        events = log.events_for_doc("doc")
        assert [e.event_id for e in events] == [c.event_id, b.event_id, a.event_id]

    def test_unknown_doc(self):
        log = DocActionLog()
        log.log_action("doc", "u", "x")
        assert log.events_for_doc("other") == []

    def test_limit(self):
        log = DocActionLog()
        for i in range(5):
            log.log_action("doc", "u", "x", now=float(i))
        result = log.events_for_doc("doc", limit=2)
        assert len(result) == 2

    def test_filters_by_doc(self):
        log = DocActionLog()
        log.log_action("a", "u", "x")
        log.log_action("b", "u", "x")
        log.log_action("a", "u", "x")
        assert len(log.events_for_doc("a")) == 2
        assert len(log.events_for_doc("b")) == 1


# ---------------------------------------------------------------------------
# events_for_actor
# ---------------------------------------------------------------------------


class TestEventsForActor:
    def test_most_recent_first(self):
        log = DocActionLog()
        a = log.log_action("d", "alice", "x", now=1.0)
        b = log.log_action("d", "alice", "x", now=2.0)
        events = log.events_for_actor("alice")
        assert [e.event_id for e in events] == [b.event_id, a.event_id]

    def test_unknown_actor(self):
        log = DocActionLog()
        log.log_action("d", "alice", "x")
        assert log.events_for_actor("bob") == []

    def test_filters_by_actor(self):
        log = DocActionLog()
        log.log_action("d", "alice", "x")
        log.log_action("d", "bob", "x")
        log.log_action("d", "alice", "x")
        assert len(log.events_for_actor("alice")) == 2

    def test_limit(self):
        log = DocActionLog()
        for _ in range(4):
            log.log_action("d", "alice", "x")
        assert len(log.events_for_actor("alice", limit=2)) == 2


# ---------------------------------------------------------------------------
# events_by_action
# ---------------------------------------------------------------------------


class TestEventsByAction:
    def test_most_recent_first(self):
        log = DocActionLog()
        a = log.log_action("d", "u", "edit", now=1.0)
        b = log.log_action("d", "u", "edit", now=2.0)
        events = log.events_by_action("edit")
        assert [e.event_id for e in events] == [b.event_id, a.event_id]

    def test_unknown_action(self):
        log = DocActionLog()
        log.log_action("d", "u", "edit")
        assert log.events_by_action("view") == []

    def test_filters_by_action(self):
        log = DocActionLog()
        log.log_action("d", "u", "edit")
        log.log_action("d", "u", "view")
        log.log_action("d", "u", "edit")
        assert len(log.events_by_action("edit")) == 2

    def test_limit(self):
        log = DocActionLog()
        for _ in range(5):
            log.log_action("d", "u", "edit")
        assert len(log.events_by_action("edit", limit=3)) == 3


# ---------------------------------------------------------------------------
# events_in_range
# ---------------------------------------------------------------------------


class TestEventsInRange:
    def test_inclusive_bounds(self):
        log = DocActionLog()
        a = log.log_action("d", "u", "x", now=1.0)
        b = log.log_action("d", "u", "x", now=2.0)
        c = log.log_action("d", "u", "x", now=3.0)
        result = log.events_in_range(1.0, 3.0)
        assert [e.event_id for e in result] == [a.event_id, b.event_id, c.event_id]

    def test_sorted_ascending(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=3.0)
        log.log_action("d", "u", "x", now=1.0)
        log.log_action("d", "u", "x", now=2.0)
        result = log.events_in_range(0.0, 10.0)
        ts = [e.timestamp for e in result]
        assert ts == sorted(ts)

    def test_excludes_outside_range(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=0.5)
        b = log.log_action("d", "u", "x", now=2.0)
        log.log_action("d", "u", "x", now=4.0)
        result = log.events_in_range(1.0, 3.0)
        assert [e.event_id for e in result] == [b.event_id]

    def test_empty_range(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=5.0)
        assert log.events_in_range(10.0, 20.0) == []

    def test_filter_by_doc(self):
        log = DocActionLog()
        log.log_action("a", "u", "x", now=1.0)
        log.log_action("b", "u", "x", now=2.0)
        result = log.events_in_range(0.0, 10.0, doc_id="a")
        assert len(result) == 1
        assert result[0].doc_id == "a"

    def test_filter_by_doc_unknown(self):
        log = DocActionLog()
        log.log_action("a", "u", "x", now=1.0)
        assert log.events_in_range(0.0, 10.0, doc_id="missing") == []


# ---------------------------------------------------------------------------
# failed_events
# ---------------------------------------------------------------------------


class TestFailedEvents:
    def test_only_failures(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", success=True)
        b = log.log_action("d", "u", "x", success=False)
        log.log_action("d", "u", "x", success=True)
        result = log.failed_events()
        assert [e.event_id for e in result] == [b.event_id]

    def test_most_recent_first(self):
        log = DocActionLog()
        a = log.log_action("d", "u", "x", success=False, now=1.0)
        b = log.log_action("d", "u", "x", success=False, now=2.0)
        result = log.failed_events()
        assert [e.event_id for e in result] == [b.event_id, a.event_id]

    def test_limit(self):
        log = DocActionLog()
        for _ in range(5):
            log.log_action("d", "u", "x", success=False)
        assert len(log.failed_events(limit=3)) == 3

    def test_empty_when_no_failures(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", success=True)
        assert log.failed_events() == []


# ---------------------------------------------------------------------------
# action_counts / actor_counts
# ---------------------------------------------------------------------------


class TestActionCounts:
    def test_counts_by_action(self):
        log = DocActionLog()
        log.log_action("d", "u", "edit")
        log.log_action("d", "u", "edit")
        log.log_action("d", "u", "view")
        c = log.action_counts()
        assert c == {"edit": 2, "view": 1}

    def test_empty(self):
        assert DocActionLog().action_counts() == {}

    def test_single_action(self):
        log = DocActionLog()
        log.log_action("d", "u", "create")
        assert log.action_counts() == {"create": 1}


class TestActorCounts:
    def test_counts_by_actor(self):
        log = DocActionLog()
        log.log_action("d", "alice", "x")
        log.log_action("d", "alice", "x")
        log.log_action("d", "bob", "x")
        c = log.actor_counts()
        assert c == {"alice": 2, "bob": 1}

    def test_empty(self):
        assert DocActionLog().actor_counts() == {}


# ---------------------------------------------------------------------------
# top_actors / top_actions
# ---------------------------------------------------------------------------


class TestTopActors:
    def test_sorted_desc(self):
        log = DocActionLog()
        for _ in range(3):
            log.log_action("d", "alice", "x")
        log.log_action("d", "bob", "x")
        for _ in range(2):
            log.log_action("d", "carol", "x")
        result = log.top_actors()
        assert result[0] == ("alice", 3)
        assert result[1] == ("carol", 2)
        assert result[2] == ("bob", 1)

    def test_limit(self):
        log = DocActionLog()
        log.log_action("d", "a", "x")
        log.log_action("d", "b", "x")
        log.log_action("d", "c", "x")
        assert len(log.top_actors(limit=2)) == 2

    def test_returns_tuples(self):
        log = DocActionLog()
        log.log_action("d", "a", "x")
        result = log.top_actors()
        assert isinstance(result[0], tuple)
        assert len(result[0]) == 2

    def test_empty(self):
        assert DocActionLog().top_actors() == []


class TestTopActions:
    def test_sorted_desc(self):
        log = DocActionLog()
        for _ in range(4):
            log.log_action("d", "u", "edit")
        log.log_action("d", "u", "view")
        for _ in range(2):
            log.log_action("d", "u", "share")
        result = log.top_actions()
        assert result[0] == ("edit", 4)
        assert result[1] == ("share", 2)
        assert result[2] == ("view", 1)

    def test_limit(self):
        log = DocActionLog()
        log.log_action("d", "u", "a")
        log.log_action("d", "u", "b")
        log.log_action("d", "u", "c")
        assert len(log.top_actions(limit=2)) == 2

    def test_empty(self):
        assert DocActionLog().top_actions() == []


# ---------------------------------------------------------------------------
# clear_old
# ---------------------------------------------------------------------------


class TestClearOld:
    def test_returns_count(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=1.0)
        log.log_action("d", "u", "x", now=2.0)
        log.log_action("d", "u", "x", now=3.0)
        removed = log.clear_old(2.5)
        assert removed == 2

    def test_removes_old(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=1.0)
        log.log_action("d", "u", "x", now=5.0)
        log.clear_old(3.0)
        assert log.stats().total_events == 1

    def test_keeps_equal_timestamp(self):
        log = DocActionLog()
        log.log_action("d", "u", "x", now=2.0)
        # before_timestamp=2.0 means timestamp<2.0 is removed; equal is kept
        removed = log.clear_old(2.0)
        assert removed == 0
        assert log.stats().total_events == 1

    def test_empty_log(self):
        log = DocActionLog()
        assert log.clear_old(100.0) == 0

    def test_indices_rebuilt(self):
        log = DocActionLog()
        log.log_action("doc1", "alice", "edit", now=1.0)
        log.log_action("doc2", "bob", "view", now=5.0)
        log.clear_old(3.0)
        assert log.events_for_doc("doc1") == []
        assert len(log.events_for_doc("doc2")) == 1
        assert log.events_for_actor("alice") == []
        assert len(log.events_for_actor("bob")) == 1
        assert log.events_by_action("edit") == []
        assert len(log.events_by_action("view")) == 1


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        log = DocActionLog()
        log.log_action("d1", "alice", "edit", success=True)
        log.log_action("d1", "bob", "view", success=True)
        log.log_action("d2", "alice", "delete", success=False)
        s = log.stats()
        assert s.total_events == 3
        assert s.success_count == 2
        assert s.failure_count == 1
        assert s.unique_docs == 2
        assert s.unique_actors == 2
        assert s.unique_actions == 3

    def test_empty(self):
        s = DocActionLog().stats()
        assert s.total_events == 0
        assert s.success_count == 0
        assert s.failure_count == 0
        assert s.unique_docs == 0
        assert s.unique_actors == 0
        assert s.unique_actions == 0

    def test_returns_actionstats(self):
        s = DocActionLog().stats()
        assert isinstance(s, ActionStats)

    def test_all_success(self):
        log = DocActionLog()
        for _ in range(3):
            log.log_action("d", "u", "x", success=True)
        s = log.stats()
        assert s.success_count == 3
        assert s.failure_count == 0

    def test_all_failure(self):
        log = DocActionLog()
        for _ in range(3):
            log.log_action("d", "u", "x", success=False)
        s = log.stats()
        assert s.success_count == 0
        assert s.failure_count == 3


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_log_action_ids_unique(self):
        log = DocActionLog()
        N_THREADS = 8
        PER_THREAD = 50

        def worker():
            for i in range(PER_THREAD):
                log.log_action(f"doc{i % 5}", f"actor{i % 3}", f"action{i % 2}")

        threads = [threading.Thread(target=worker) for _ in range(N_THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = log.stats()
        assert s.total_events == N_THREADS * PER_THREAD
        ids = {log._events[i].event_id for i in range(len(log._events))}
        assert len(ids) == N_THREADS * PER_THREAD
        assert min(ids) == 1
        assert max(ids) == N_THREADS * PER_THREAD

    def test_concurrent_log_and_query(self):
        log = DocActionLog()
        stop = threading.Event()

        def writer():
            i = 0
            while not stop.is_set():
                log.log_action(f"d{i % 3}", "u", "x")
                i += 1

        def reader():
            while not stop.is_set():
                _ = log.stats()
                _ = log.events_for_doc("d0", limit=5)

        threads = [threading.Thread(target=writer) for _ in range(3)]
        threads += [threading.Thread(target=reader) for _ in range(3)]
        for t in threads:
            t.start()
        time.sleep(0.1)
        stop.set()
        for t in threads:
            t.join()

        # Should not raise; log should be self-consistent.
        s = log.stats()
        assert s.total_events > 0
