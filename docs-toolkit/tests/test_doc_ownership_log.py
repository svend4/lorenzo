"""Tests for E440 DocOwnershipLog."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_ownership_log import (
    DocOwnershipLog,
    OwnershipEvent,
    OwnershipStats,
)


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def test_construct_empty_log():
    log = DocOwnershipLog()
    assert log.stats().total_events == 0


def test_empty_get_event_returns_none():
    log = DocOwnershipLog()
    assert log.get_event(1) is None


def test_empty_events_for_doc():
    log = DocOwnershipLog()
    assert log.events_for_doc("d1") == []


def test_empty_events_for_subject():
    log = DocOwnershipLog()
    assert log.events_for_subject("u1") == []


def test_empty_events_by_action():
    log = DocOwnershipLog()
    assert log.events_by_action("assign") == []


def test_empty_owners_of():
    log = DocOwnershipLog()
    assert log.owners_of("d1") == []


def test_empty_last_assign_for():
    log = DocOwnershipLog()
    assert log.last_assign_for("d1") is None


# ---------------------------------------------------------------------------
# log_event basics
# ---------------------------------------------------------------------------


def test_log_event_returns_event():
    log = DocOwnershipLog()
    ev = log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert isinstance(ev, OwnershipEvent)


def test_log_event_assigns_id_starting_at_1():
    log = DocOwnershipLog()
    ev = log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert ev.event_id == 1


def test_log_event_assigns_sequential_ids():
    log = DocOwnershipLog()
    e1 = log.log_event("d1", "assign", "admin", "alice", now=1.0)
    e2 = log.log_event("d2", "assign", "admin", "bob", now=2.0)
    e3 = log.log_event("d1", "transfer", "admin", "carol", now=3.0)
    assert (e1.event_id, e2.event_id, e3.event_id) == (1, 2, 3)


def test_log_event_stores_all_fields():
    log = DocOwnershipLog()
    ev = log.log_event(
        "d1",
        "transfer",
        "admin",
        "alice",
        previous_owner="bob",
        note="quarterly rotation",
        now=42.5,
    )
    assert ev.doc_id == "d1"
    assert ev.action == "transfer"
    assert ev.actor == "admin"
    assert ev.subject == "alice"
    assert ev.previous_owner == "bob"
    assert ev.note == "quarterly rotation"
    assert ev.timestamp == 42.5


def test_log_event_defaults():
    log = DocOwnershipLog()
    ev = log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert ev.previous_owner is None
    assert ev.note == ""


def test_log_event_uses_time_when_now_none(monkeypatch):
    log = DocOwnershipLog()
    monkeypatch.setattr("time.time", lambda: 999.0)
    ev = log.log_event("d1", "assign", "admin", "alice")
    assert ev.timestamp == 999.0


def test_log_event_invalid_action_raises():
    log = DocOwnershipLog()
    with pytest.raises(ValueError):
        log.log_event("d1", "delete", "admin", "alice", now=1.0)


def test_log_event_all_valid_actions():
    log = DocOwnershipLog()
    for action in ("assign", "transfer", "revoke", "co_assign", "co_revoke"):
        ev = log.log_event("d1", action, "admin", "alice", now=1.0)
        assert ev.action == action


# ---------------------------------------------------------------------------
# get_event
# ---------------------------------------------------------------------------


def test_get_event_returns_logged():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    ev = log.get_event(1)
    assert ev is not None
    assert ev.doc_id == "d1"


def test_get_event_unknown_id():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert log.get_event(999) is None


def test_get_event_multiple():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    assert log.get_event(1).subject == "alice"
    assert log.get_event(2).subject == "bob"


# ---------------------------------------------------------------------------
# events_for_doc
# ---------------------------------------------------------------------------


def test_events_for_doc_filters_correctly():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    log.log_event("d1", "transfer", "admin", "carol", now=3.0)
    assert [e.event_id for e in log.events_for_doc("d1")] == [3, 1]
    assert [e.event_id for e in log.events_for_doc("d2")] == [2]


def test_events_for_doc_most_recent_first():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d1", "transfer", "admin", "b", now=2.0)
    log.log_event("d1", "transfer", "admin", "c", now=3.0)
    evs = log.events_for_doc("d1")
    assert [e.subject for e in evs] == ["c", "b", "a"]


def test_events_for_doc_limit():
    log = DocOwnershipLog()
    for i in range(5):
        log.log_event("d1", "assign", "admin", f"u{i}", now=float(i))
    evs = log.events_for_doc("d1", limit=2)
    assert len(evs) == 2
    assert evs[0].subject == "u4"
    assert evs[1].subject == "u3"


def test_events_for_doc_unknown():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert log.events_for_doc("missing") == []


# ---------------------------------------------------------------------------
# events_for_subject
# ---------------------------------------------------------------------------


def test_events_for_subject_filters_correctly():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    log.log_event("d3", "assign", "admin", "alice", now=3.0)
    assert [e.event_id for e in log.events_for_subject("alice")] == [3, 1]


def test_events_for_subject_most_recent_first():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "co_assign", "admin", "alice", now=2.0)
    evs = log.events_for_subject("alice")
    assert evs[0].timestamp == 2.0
    assert evs[1].timestamp == 1.0


def test_events_for_subject_limit():
    log = DocOwnershipLog()
    for i in range(4):
        log.log_event(f"d{i}", "assign", "admin", "alice", now=float(i))
    evs = log.events_for_subject("alice", limit=2)
    assert len(evs) == 2


def test_events_for_subject_unknown():
    log = DocOwnershipLog()
    assert log.events_for_subject("ghost") == []


# ---------------------------------------------------------------------------
# events_by_action
# ---------------------------------------------------------------------------


def test_events_by_action_filters():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "transfer", "admin", "bob", now=2.0)
    log.log_event("d3", "assign", "admin", "carol", now=3.0)
    assigns = log.events_by_action("assign")
    assert len(assigns) == 2
    assert {e.subject for e in assigns} == {"alice", "carol"}


def test_events_by_action_most_recent_first():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d2", "assign", "admin", "b", now=2.0)
    log.log_event("d3", "assign", "admin", "c", now=3.0)
    evs = log.events_by_action("assign")
    assert [e.subject for e in evs] == ["c", "b", "a"]


def test_events_by_action_limit():
    log = DocOwnershipLog()
    for i in range(5):
        log.log_event(f"d{i}", "assign", "admin", "alice", now=float(i))
    evs = log.events_by_action("assign", limit=3)
    assert len(evs) == 3


def test_events_by_action_unknown_action_returns_empty():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert log.events_by_action("co_revoke") == []


# ---------------------------------------------------------------------------
# events_in_range
# ---------------------------------------------------------------------------


def test_events_in_range_inclusive():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d1", "transfer", "admin", "b", now=2.0)
    log.log_event("d1", "transfer", "admin", "c", now=3.0)
    evs = log.events_in_range(1.0, 3.0)
    assert len(evs) == 3


def test_events_in_range_excludes_outside():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d1", "transfer", "admin", "b", now=5.0)
    log.log_event("d1", "transfer", "admin", "c", now=10.0)
    evs = log.events_in_range(3.0, 7.0)
    assert len(evs) == 1
    assert evs[0].subject == "b"


def test_events_in_range_ascending_order():
    log = DocOwnershipLog()
    log.log_event("d1", "transfer", "admin", "c", now=3.0)
    log.log_event("d1", "transfer", "admin", "a", now=1.0)
    log.log_event("d1", "transfer", "admin", "b", now=2.0)
    evs = log.events_in_range(0.0, 10.0)
    assert [e.event_id for e in evs] == [1, 2, 3]


def test_events_in_range_filtered_by_doc():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d2", "assign", "admin", "b", now=2.0)
    log.log_event("d1", "transfer", "admin", "c", now=3.0)
    evs = log.events_in_range(0.0, 10.0, doc_id="d1")
    assert [e.subject for e in evs] == ["a", "c"]


def test_events_in_range_empty():
    log = DocOwnershipLog()
    assert log.events_in_range(0.0, 100.0) == []


def test_events_in_range_unknown_doc():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    assert log.events_in_range(0.0, 100.0, doc_id="missing") == []


# ---------------------------------------------------------------------------
# last_assign_for
# ---------------------------------------------------------------------------


def test_last_assign_for_returns_latest_assign():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    ev = log.last_assign_for("d1")
    assert ev is not None
    assert ev.subject == "alice"


def test_last_assign_for_returns_latest_transfer():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "transfer", "admin", "carol", now=3.0)
    ev = log.last_assign_for("d1")
    assert ev.subject == "carol"
    assert ev.action == "transfer"


def test_last_assign_for_ignores_revoke():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "revoke", "admin", "alice", now=2.0)
    ev = log.last_assign_for("d1")
    assert ev.subject == "alice"
    assert ev.action == "assign"


def test_last_assign_for_none_if_no_assign_or_transfer():
    log = DocOwnershipLog()
    log.log_event("d1", "co_assign", "admin", "alice", now=1.0)
    assert log.last_assign_for("d1") is None


def test_last_assign_for_unknown_doc():
    log = DocOwnershipLog()
    assert log.last_assign_for("missing") is None


# ---------------------------------------------------------------------------
# owners_of (replay)
# ---------------------------------------------------------------------------


def test_owners_of_single_assign():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    assert log.owners_of("d1") == ["alice"]


def test_owners_of_transfer_replaces_primary():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "transfer", "admin", "bob", now=2.0)
    assert log.owners_of("d1") == ["bob"]


def test_owners_of_revoke_removes_primary():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "revoke", "admin", "alice", now=2.0)
    assert log.owners_of("d1") == []


def test_owners_of_co_assign_adds():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    assert log.owners_of("d1") == ["alice", "bob"]


def test_owners_of_co_revoke_removes():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    log.log_event("d1", "co_revoke", "admin", "bob", now=3.0)
    assert log.owners_of("d1") == ["alice"]


def test_owners_of_co_assign_skipped_if_already_primary():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "alice", now=2.0)
    assert log.owners_of("d1") == ["alice"]


def test_owners_of_co_assign_no_duplicate():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=3.0)
    assert log.owners_of("d1") == ["alice", "bob"]


def test_owners_of_transfer_to_existing_coowner_removes_from_co():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    log.log_event("d1", "transfer", "admin", "bob", now=3.0)
    assert log.owners_of("d1") == ["bob"]


def test_owners_of_complex_sequence():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "co_assign", "admin", "bob", now=2.0)
    log.log_event("d1", "co_assign", "admin", "carol", now=3.0)
    log.log_event("d1", "transfer", "admin", "dan", now=4.0)
    log.log_event("d1", "co_revoke", "admin", "bob", now=5.0)
    assert log.owners_of("d1") == ["dan", "carol"]


def test_owners_of_revoke_unaffected_primary():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "revoke", "admin", "bob", now=2.0)  # bob isn't primary
    assert log.owners_of("d1") == ["alice"]


def test_owners_of_unknown_doc():
    log = DocOwnershipLog()
    assert log.owners_of("missing") == []


# ---------------------------------------------------------------------------
# delete_old
# ---------------------------------------------------------------------------


def test_delete_old_removes_old_events():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "transfer", "admin", "bob", now=10.0)
    log.log_event("d1", "transfer", "admin", "carol", now=100.0)
    removed = log.delete_old(50.0)
    assert removed == 2
    assert log.stats().total_events == 1


def test_delete_old_zero_when_nothing_old():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=100.0)
    assert log.delete_old(50.0) == 0


def test_delete_old_rebuilds_indexes():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d1", "transfer", "admin", "bob", now=100.0)
    log.delete_old(50.0)
    assert len(log.events_for_doc("d1")) == 1
    assert len(log.events_for_subject("alice")) == 0
    assert len(log.events_for_subject("bob")) == 1


def test_delete_old_empty_log():
    log = DocOwnershipLog()
    assert log.delete_old(100.0) == 0


# ---------------------------------------------------------------------------
# clear_all
# ---------------------------------------------------------------------------


def test_clear_all_returns_count():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    assert log.clear_all() == 2


def test_clear_all_empties_state():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.clear_all()
    assert log.stats().total_events == 0
    assert log.events_for_doc("d1") == []
    assert log.events_for_subject("alice") == []


def test_clear_all_resets_id_counter():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    log.clear_all()
    ev = log.log_event("d3", "assign", "admin", "carol", now=3.0)
    assert ev.event_id == 1


def test_clear_all_on_empty_returns_zero():
    log = DocOwnershipLog()
    assert log.clear_all() == 0


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


def test_stats_empty():
    log = DocOwnershipLog()
    s = log.stats()
    assert s.total_events == 0
    assert s.unique_docs == 0
    assert s.unique_actors == 0
    assert s.unique_subjects == 0
    assert s.action_counts == {}


def test_stats_counts_correctly():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "alice", now=1.0)
    log.log_event("d2", "assign", "admin", "bob", now=2.0)
    log.log_event("d1", "transfer", "manager", "carol", now=3.0)
    log.log_event("d1", "co_assign", "manager", "bob", now=4.0)
    s = log.stats()
    assert s.total_events == 4
    assert s.unique_docs == 2
    assert s.unique_actors == 2
    assert s.unique_subjects == 3
    assert s.action_counts == {"assign": 2, "transfer": 1, "co_assign": 1}


def test_stats_returns_ownership_stats_instance():
    log = DocOwnershipLog()
    assert isinstance(log.stats(), OwnershipStats)


def test_stats_action_counts_all_actions():
    log = DocOwnershipLog()
    log.log_event("d1", "assign", "admin", "a", now=1.0)
    log.log_event("d1", "transfer", "admin", "b", now=2.0)
    log.log_event("d1", "revoke", "admin", "b", now=3.0)
    log.log_event("d1", "co_assign", "admin", "c", now=4.0)
    log.log_event("d1", "co_revoke", "admin", "c", now=5.0)
    s = log.stats()
    assert s.action_counts == {
        "assign": 1,
        "transfer": 1,
        "revoke": 1,
        "co_assign": 1,
        "co_revoke": 1,
    }


# ---------------------------------------------------------------------------
# Dataclass behavior
# ---------------------------------------------------------------------------


def test_ownership_event_dataclass_fields():
    ev = OwnershipEvent(
        event_id=1,
        doc_id="d",
        action="assign",
        actor="admin",
        subject="alice",
    )
    assert ev.previous_owner is None
    assert ev.note == ""
    assert ev.timestamp == 0.0


def test_ownership_stats_default_action_counts():
    s = OwnershipStats(
        total_events=0,
        unique_docs=0,
        unique_actors=0,
        unique_subjects=0,
    )
    assert s.action_counts == {}


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_concurrent_logging():
    log = DocOwnershipLog()
    n_threads = 8
    per_thread = 100

    def worker(tid: int):
        for i in range(per_thread):
            log.log_event(
                f"d{tid}",
                "assign",
                f"actor{tid}",
                f"user{tid}_{i}",
                now=float(i),
            )

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = log.stats()
    assert s.total_events == n_threads * per_thread


def test_thread_safety_unique_ids():
    log = DocOwnershipLog()
    n_threads = 4
    per_thread = 50

    def worker(tid: int):
        for i in range(per_thread):
            log.log_event(f"d{tid}", "assign", "admin", f"u{tid}_{i}", now=1.0)

    threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # Collect all event ids
    all_ids = set()
    for tid in range(n_threads):
        for ev in log.events_for_doc(f"d{tid}"):
            all_ids.add(ev.event_id)
    assert len(all_ids) == n_threads * per_thread


def test_thread_safety_mixed_read_write():
    log = DocOwnershipLog()
    stop = threading.Event()
    errors: list[Exception] = []

    def writer():
        i = 0
        while not stop.is_set():
            try:
                log.log_event("d1", "assign", "admin", f"u{i}", now=float(i))
                i += 1
            except Exception as e:  # pragma: no cover
                errors.append(e)

    def reader():
        while not stop.is_set():
            try:
                log.events_for_doc("d1")
                log.stats()
                log.owners_of("d1")
            except Exception as e:  # pragma: no cover
                errors.append(e)

    w = threading.Thread(target=writer)
    r = threading.Thread(target=reader)
    w.start()
    r.start()
    threading.Event().wait(0.1)
    stop.set()
    w.join()
    r.join()

    assert errors == []
    assert log.stats().total_events > 0
