"""Tests for E443 DocPinAudit."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_pin_audit import (
    DocPinAudit,
    PinAuditEvent,
    PinAuditStats,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


@pytest.fixture
def audit() -> DocPinAudit:
    return DocPinAudit()


@pytest.fixture
def seeded() -> DocPinAudit:
    a = DocPinAudit()
    a.log("d1", "alice", "pin", reason="initial", now=100.0)
    a.log("d1", "alice", "renew", now=200.0)
    a.log("d1", "bob", "unpin", reason="cleanup", now=300.0)
    a.log("d2", "alice", "pin", now=150.0)
    a.log("d2", "carol", "pin", now=250.0)
    a.log("d2", "carol", "move", metadata={"to": "section/x"}, now=350.0)
    a.log("d3", "bob", "pin", now=400.0)
    a.log("d3", "bob", "transfer", now=500.0)
    return a


# ---------------------------------------------------------------------------
# Imports & API surface
# ---------------------------------------------------------------------------


def test_module_exports():
    import docstoolkit.doc_pin_audit as mod

    assert set(mod.__all__) == {
        "PinAuditEvent",
        "PinAuditStats",
        "DocPinAudit",
    }


def test_classes_importable():
    assert PinAuditEvent is not None
    assert PinAuditStats is not None
    assert DocPinAudit is not None


# ---------------------------------------------------------------------------
# PinAuditEvent / PinAuditStats dataclass shape
# ---------------------------------------------------------------------------


def test_event_default_fields():
    ev = PinAuditEvent(event_id=1, doc_id="d", actor="a", action="pin")
    assert ev.timestamp == 0.0
    assert ev.reason == ""
    assert ev.metadata == {}


def test_event_custom_fields():
    ev = PinAuditEvent(
        event_id=5,
        doc_id="d",
        actor="a",
        action="pin",
        timestamp=12.5,
        reason="r",
        metadata={"k": 1},
    )
    assert ev.event_id == 5
    assert ev.timestamp == 12.5
    assert ev.reason == "r"
    assert ev.metadata == {"k": 1}


def test_event_metadata_default_is_independent():
    ev1 = PinAuditEvent(event_id=1, doc_id="a", actor="x", action="pin")
    ev2 = PinAuditEvent(event_id=2, doc_id="b", actor="x", action="pin")
    ev1.metadata["x"] = 1
    assert ev2.metadata == {}


def test_stats_defaults():
    s = PinAuditStats(total_events=0, unique_docs=0, unique_actors=0)
    assert s.action_counts == {}


def test_stats_custom():
    s = PinAuditStats(
        total_events=3,
        unique_docs=2,
        unique_actors=2,
        action_counts={"pin": 2, "unpin": 1},
    )
    assert s.total_events == 3
    assert s.action_counts["pin"] == 2


# ---------------------------------------------------------------------------
# log()
# ---------------------------------------------------------------------------


def test_log_returns_event(audit):
    ev = audit.log("d1", "alice", "pin")
    assert isinstance(ev, PinAuditEvent)
    assert ev.event_id == 1
    assert ev.doc_id == "d1"
    assert ev.actor == "alice"
    assert ev.action == "pin"


def test_log_assigns_incrementing_ids(audit):
    a = audit.log("d1", "alice", "pin")
    b = audit.log("d1", "alice", "renew")
    c = audit.log("d2", "bob", "pin")
    assert (a.event_id, b.event_id, c.event_id) == (1, 2, 3)


def test_log_with_now(audit):
    ev = audit.log("d1", "alice", "pin", now=123.5)
    assert ev.timestamp == 123.5


def test_log_uses_time_when_now_none(audit):
    before = time.time()
    ev = audit.log("d1", "alice", "pin")
    after = time.time()
    assert before <= ev.timestamp <= after


def test_log_default_reason_and_metadata(audit):
    ev = audit.log("d1", "alice", "pin")
    assert ev.reason == ""
    assert ev.metadata == {}


def test_log_with_reason(audit):
    ev = audit.log("d1", "alice", "pin", reason="bookmarking")
    assert ev.reason == "bookmarking"


def test_log_with_metadata(audit):
    ev = audit.log("d1", "alice", "pin", metadata={"src": "ui"})
    assert ev.metadata == {"src": "ui"}


def test_log_metadata_is_copied(audit):
    src = {"k": 1}
    ev = audit.log("d1", "alice", "pin", metadata=src)
    src["k"] = 999
    assert ev.metadata == {"k": 1}


def test_log_metadata_none_becomes_empty(audit):
    ev = audit.log("d1", "alice", "pin", metadata=None)
    assert ev.metadata == {}


def test_log_accepts_arbitrary_action_strings(audit):
    ev = audit.log("d1", "alice", "weird-custom-action")
    assert ev.action == "weird-custom-action"


# ---------------------------------------------------------------------------
# get_event()
# ---------------------------------------------------------------------------


def test_get_event_existing(seeded):
    ev = seeded.get_event(1)
    assert ev is not None
    assert ev.doc_id == "d1"
    assert ev.action == "pin"


def test_get_event_missing(audit):
    assert audit.get_event(1) is None


def test_get_event_zero_or_negative(seeded):
    assert seeded.get_event(0) is None
    assert seeded.get_event(-1) is None


def test_get_event_beyond_range(seeded):
    assert seeded.get_event(9999) is None


def test_get_event_after_deletion_uses_fallback(audit):
    audit.log("d1", "a", "pin", now=10.0)
    audit.log("d1", "a", "pin", now=20.0)
    audit.log("d1", "a", "pin", now=30.0)
    audit.delete_old(25.0)  # removes events 1 and 2
    ev = audit.get_event(3)
    assert ev is not None
    assert ev.timestamp == 30.0


# ---------------------------------------------------------------------------
# events_for_doc()
# ---------------------------------------------------------------------------


def test_events_for_doc_basic(seeded):
    evs = seeded.events_for_doc("d1")
    assert [e.event_id for e in evs] == [3, 2, 1]  # most recent first


def test_events_for_doc_unknown(audit):
    assert audit.events_for_doc("nope") == []


def test_events_for_doc_filter_by_action(seeded):
    evs = seeded.events_for_doc("d1", action="pin")
    assert len(evs) == 1
    assert evs[0].action == "pin"


def test_events_for_doc_filter_no_matches(seeded):
    assert seeded.events_for_doc("d1", action="transfer") == []


def test_events_for_doc_limit(seeded):
    evs = seeded.events_for_doc("d1", limit=2)
    assert [e.event_id for e in evs] == [3, 2]


def test_events_for_doc_limit_with_action(seeded):
    evs = seeded.events_for_doc("d2", action="pin", limit=1)
    assert len(evs) == 1
    assert evs[0].action == "pin"


# ---------------------------------------------------------------------------
# events_for_actor()
# ---------------------------------------------------------------------------


def test_events_for_actor_basic(seeded):
    evs = seeded.events_for_actor("alice")
    # alice has events 1, 2, 4 — most recent first
    assert [e.event_id for e in evs] == [4, 2, 1]


def test_events_for_actor_unknown(audit):
    assert audit.events_for_actor("ghost") == []


def test_events_for_actor_limit(seeded):
    evs = seeded.events_for_actor("alice", limit=2)
    assert len(evs) == 2
    assert evs[0].event_id == 4
    assert evs[1].event_id == 2


# ---------------------------------------------------------------------------
# events_by_action()
# ---------------------------------------------------------------------------


def test_events_by_action_basic(seeded):
    evs = seeded.events_by_action("pin")
    # pin events: 1, 4, 5, 7 — most recent first
    assert [e.event_id for e in evs] == [7, 5, 4, 1]


def test_events_by_action_no_matches(audit):
    audit.log("d", "a", "pin")
    assert audit.events_by_action("unpin") == []


def test_events_by_action_limit(seeded):
    evs = seeded.events_by_action("pin", limit=2)
    assert [e.event_id for e in evs] == [7, 5]


def test_events_by_action_single(seeded):
    evs = seeded.events_by_action("transfer")
    assert len(evs) == 1
    assert evs[0].event_id == 8


# ---------------------------------------------------------------------------
# events_in_range()
# ---------------------------------------------------------------------------


def test_events_in_range_basic(seeded):
    evs = seeded.events_in_range(150.0, 300.0)
    # events with ts in [150, 300]: id4(150), id2(200), id5(250), id3(300)
    assert [e.event_id for e in evs] == [4, 2, 5, 3]


def test_events_in_range_inclusive_bounds(seeded):
    evs = seeded.events_in_range(100.0, 100.0)
    assert [e.event_id for e in evs] == [1]


def test_events_in_range_no_match(seeded):
    assert seeded.events_in_range(1000.0, 2000.0) == []


def test_events_in_range_with_doc(seeded):
    evs = seeded.events_in_range(0.0, 1000.0, doc_id="d2")
    # d2 events: id4(150), id5(250), id6(350) — sorted ascending
    assert [e.event_id for e in evs] == [4, 5, 6]


def test_events_in_range_with_doc_no_match(seeded):
    assert seeded.events_in_range(0.0, 1000.0, doc_id="unknown") == []


def test_events_in_range_returns_sorted_asc(audit):
    audit.log("d", "a", "pin", now=30.0)
    audit.log("d", "a", "pin", now=10.0)
    audit.log("d", "a", "pin", now=20.0)
    evs = audit.events_in_range(0.0, 100.0)
    assert [e.timestamp for e in evs] == [10.0, 20.0, 30.0]


# ---------------------------------------------------------------------------
# last_pin_event_for()
# ---------------------------------------------------------------------------


def test_last_pin_event_returns_renew_if_most_recent(seeded):
    # d1: pin@100, renew@200, unpin@300 -> last pin-like is renew(id=2)
    ev = seeded.last_pin_event_for("d1")
    assert ev is not None
    assert ev.event_id == 2
    assert ev.action == "renew"


def test_last_pin_event_skips_non_pin_actions(audit):
    audit.log("d", "a", "pin", now=10.0)
    audit.log("d", "a", "move", now=20.0)
    audit.log("d", "a", "transfer", now=30.0)
    ev = audit.last_pin_event_for("d")
    assert ev is not None
    assert ev.action == "pin"
    assert ev.timestamp == 10.0


def test_last_pin_event_unknown_doc(audit):
    assert audit.last_pin_event_for("missing") is None


def test_last_pin_event_no_pin_actions(audit):
    audit.log("d", "a", "unpin")
    audit.log("d", "a", "move")
    assert audit.last_pin_event_for("d") is None


def test_last_pin_event_for_d3(seeded):
    # d3: pin@400, transfer@500 -> last pin-like is pin (id=7)
    ev = seeded.last_pin_event_for("d3")
    assert ev is not None
    assert ev.event_id == 7


# ---------------------------------------------------------------------------
# most_pinned_docs()
# ---------------------------------------------------------------------------


def test_most_pinned_docs_basic(seeded):
    # pin counts (action == "pin" only): d1=1, d2=2, d3=1
    result = seeded.most_pinned_docs()
    assert result[0] == ("d2", 2)
    assert ("d1", 1) in result
    assert ("d3", 1) in result


def test_most_pinned_docs_does_not_count_renew(audit):
    audit.log("a", "x", "pin")
    audit.log("a", "x", "renew")
    audit.log("a", "x", "renew")
    result = audit.most_pinned_docs()
    assert result == [("a", 1)]


def test_most_pinned_docs_empty(audit):
    assert audit.most_pinned_docs() == []


def test_most_pinned_docs_limit(seeded):
    result = seeded.most_pinned_docs(limit=1)
    assert result == [("d2", 2)]


def test_most_pinned_docs_tie_break_alphabetical(audit):
    audit.log("zebra", "x", "pin")
    audit.log("apple", "x", "pin")
    audit.log("mango", "x", "pin")
    result = audit.most_pinned_docs()
    assert result == [("apple", 1), ("mango", 1), ("zebra", 1)]


def test_most_pinned_docs_excludes_docs_without_pin(audit):
    audit.log("only-unpin", "x", "unpin")
    audit.log("only-move", "x", "move")
    assert audit.most_pinned_docs() == []


# ---------------------------------------------------------------------------
# pin_activity_summary()
# ---------------------------------------------------------------------------


def test_pin_activity_summary_basic(seeded):
    summary = seeded.pin_activity_summary()
    assert summary["pin"] == 4
    assert summary["renew"] == 1
    assert summary["unpin"] == 1
    assert summary["move"] == 1
    assert summary["transfer"] == 1


def test_pin_activity_summary_empty(audit):
    assert audit.pin_activity_summary() == {}


def test_pin_activity_summary_single_action(audit):
    audit.log("d", "a", "pin")
    audit.log("d", "a", "pin")
    audit.log("d", "a", "pin")
    assert audit.pin_activity_summary() == {"pin": 3}


# ---------------------------------------------------------------------------
# delete_old()
# ---------------------------------------------------------------------------


def test_delete_old_removes_strictly_before(audit):
    audit.log("d", "a", "pin", now=10.0)
    audit.log("d", "a", "pin", now=20.0)
    audit.log("d", "a", "pin", now=30.0)
    removed = audit.delete_old(20.0)
    assert removed == 1  # only ts=10 is strictly before 20
    remaining = [e.timestamp for e in audit.events_for_doc("d")]
    assert sorted(remaining) == [20.0, 30.0]


def test_delete_old_none_removed(seeded):
    removed = seeded.delete_old(0.0)
    assert removed == 0


def test_delete_old_all_removed(seeded):
    removed = seeded.delete_old(10_000.0)
    assert removed == 8
    assert seeded.stats().total_events == 0


def test_delete_old_rebuilds_indices(audit):
    audit.log("d1", "a1", "pin", now=10.0)
    audit.log("d2", "a2", "pin", now=20.0)
    audit.log("d3", "a3", "pin", now=30.0)
    audit.delete_old(25.0)
    assert audit.events_for_doc("d1") == []
    assert audit.events_for_doc("d2") == []
    assert len(audit.events_for_doc("d3")) == 1
    assert audit.events_for_actor("a1") == []
    assert audit.events_for_actor("a2") == []
    assert len(audit.events_for_actor("a3")) == 1


def test_delete_old_preserves_event_ids(audit):
    e1 = audit.log("d", "a", "pin", now=10.0)
    e2 = audit.log("d", "a", "pin", now=20.0)
    audit.delete_old(15.0)
    assert audit.get_event(e1.event_id) is None
    assert audit.get_event(e2.event_id) is not None


# ---------------------------------------------------------------------------
# clear_all()
# ---------------------------------------------------------------------------


def test_clear_all_returns_count(seeded):
    removed = seeded.clear_all()
    assert removed == 8


def test_clear_all_empties_state(seeded):
    seeded.clear_all()
    s = seeded.stats()
    assert s.total_events == 0
    assert s.unique_docs == 0
    assert s.unique_actors == 0
    assert s.action_counts == {}


def test_clear_all_resets_next_id(audit):
    audit.log("d", "a", "pin")
    audit.log("d", "a", "pin")
    audit.clear_all()
    ev = audit.log("d", "a", "pin")
    assert ev.event_id == 1


def test_clear_all_on_empty(audit):
    assert audit.clear_all() == 0


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------


def test_stats_empty(audit):
    s = audit.stats()
    assert s.total_events == 0
    assert s.unique_docs == 0
    assert s.unique_actors == 0
    assert s.action_counts == {}


def test_stats_seeded(seeded):
    s = seeded.stats()
    assert s.total_events == 8
    assert s.unique_docs == 3
    assert s.unique_actors == 3
    assert s.action_counts["pin"] == 4


def test_stats_after_delete(seeded):
    seeded.delete_old(250.0)
    s = seeded.stats()
    # surviving events: id3(300), id6(350), id7(400), id8(500), id5(250)
    assert s.total_events == 5


def test_stats_returns_pinaudit_stats(audit):
    audit.log("d", "a", "pin")
    s = audit.stats()
    assert isinstance(s, PinAuditStats)


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


def test_thread_safety_unique_event_ids(audit):
    n_threads = 8
    per_thread = 100

    def worker(tag: str) -> None:
        for i in range(per_thread):
            audit.log(f"doc-{tag}", f"actor-{tag}", "pin")

    threads = [
        threading.Thread(target=worker, args=(str(i),)) for i in range(n_threads)
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    s = audit.stats()
    assert s.total_events == n_threads * per_thread
    ids = set()
    for tag in range(n_threads):
        for ev in audit.events_for_doc(f"doc-{tag}"):
            ids.add(ev.event_id)
    assert len(ids) == n_threads * per_thread
    assert min(ids) == 1
    assert max(ids) == n_threads * per_thread


def test_thread_safety_mixed_writes_and_reads():
    a = DocPinAudit()
    stop = threading.Event()

    def writer() -> None:
        i = 0
        while not stop.is_set():
            a.log(f"d{i % 5}", f"act{i % 3}", "pin")
            i += 1

    def reader() -> None:
        while not stop.is_set():
            a.stats()
            a.events_for_doc("d1")
            a.most_pinned_docs()

    writers = [threading.Thread(target=writer) for _ in range(3)]
    readers = [threading.Thread(target=reader) for _ in range(3)]
    for t in writers + readers:
        t.start()
    time.sleep(0.1)
    stop.set()
    for t in writers + readers:
        t.join()

    # No exceptions and stats are internally consistent
    s = a.stats()
    assert s.total_events > 0


def test_thread_safety_delete_during_writes():
    a = DocPinAudit()
    for i in range(50):
        a.log("d", "actor", "pin", now=float(i))

    results: list[int] = []

    def deleter() -> None:
        results.append(a.delete_old(25.0))

    def writer() -> None:
        for i in range(50, 100):
            a.log("d", "actor", "pin", now=float(i))

    t1 = threading.Thread(target=deleter)
    t2 = threading.Thread(target=writer)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # The deleter removed exactly 25 events (ts 0..24).
    assert results == [25]
    # All surviving events are >= 25.0
    for ev in a.events_for_doc("d"):
        assert ev.timestamp >= 25.0


# ---------------------------------------------------------------------------
# Misc edge cases
# ---------------------------------------------------------------------------


def test_events_for_doc_returns_copies_in_list(seeded):
    evs1 = seeded.events_for_doc("d1")
    evs2 = seeded.events_for_doc("d1")
    # Same underlying event objects but distinct lists
    assert evs1 is not evs2
    assert evs1 == evs2


def test_log_does_not_share_metadata_between_events(audit):
    md = {"shared": True}
    e1 = audit.log("d", "a", "pin", metadata=md)
    e2 = audit.log("d", "a", "pin", metadata=md)
    e1.metadata["only_in_e1"] = 1
    assert "only_in_e1" not in e2.metadata


def test_action_counts_match_summary(seeded):
    s = seeded.stats()
    summary = seeded.pin_activity_summary()
    assert s.action_counts == summary
