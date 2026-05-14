"""Tests for docstoolkit.doc_review_assignment (E385)."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_review_assignment import (
    AssignmentStats,
    DocReviewAssignment,
    ReviewAssignment,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make() -> DocReviewAssignment:
    return DocReviewAssignment()


def _assign(
    a: DocReviewAssignment,
    doc_id: str = "doc-1",
    reviewer: str = "alice",
    assigned_by: str = "boss",
    due_date=None,
    note: str = "",
    now: float = 1.0,
) -> ReviewAssignment:
    return a.assign(
        doc_id=doc_id,
        reviewer=reviewer,
        assigned_by=assigned_by,
        due_date=due_date,
        note=note,
        now=now,
    )


# ---------------------------------------------------------------------------
# TestReviewAssignmentDataclass
# ---------------------------------------------------------------------------

class TestReviewAssignmentDataclass:
    def test_required_fields(self):
        r = ReviewAssignment(
            assignment_id="id1", doc_id="doc-1",
            reviewer="alice", assigned_by="boss",
        )
        assert r.assignment_id == "id1"
        assert r.doc_id == "doc-1"
        assert r.reviewer == "alice"
        assert r.assigned_by == "boss"

    def test_default_assigned_at(self):
        r = ReviewAssignment(
            assignment_id="i", doc_id="d", reviewer="a", assigned_by="b",
        )
        assert r.assigned_at == 0.0

    def test_default_due_date(self):
        r = ReviewAssignment(
            assignment_id="i", doc_id="d", reviewer="a", assigned_by="b",
        )
        assert r.due_date is None

    def test_default_status(self):
        r = ReviewAssignment(
            assignment_id="i", doc_id="d", reviewer="a", assigned_by="b",
        )
        assert r.status == "assigned"

    def test_default_completed_at(self):
        r = ReviewAssignment(
            assignment_id="i", doc_id="d", reviewer="a", assigned_by="b",
        )
        assert r.completed_at is None

    def test_default_note(self):
        r = ReviewAssignment(
            assignment_id="i", doc_id="d", reviewer="a", assigned_by="b",
        )
        assert r.note == ""

    def test_custom_values(self):
        r = ReviewAssignment(
            assignment_id="id2", doc_id="doc-2",
            reviewer="bob", assigned_by="root",
            assigned_at=10.0, due_date=20.0,
            status="in_progress", completed_at=15.0, note="ugh",
        )
        assert r.assigned_at == 10.0
        assert r.due_date == 20.0
        assert r.status == "in_progress"
        assert r.completed_at == 15.0
        assert r.note == "ugh"


# ---------------------------------------------------------------------------
# TestAssignmentStatsDataclass
# ---------------------------------------------------------------------------

class TestAssignmentStatsDataclass:
    def test_required_fields(self):
        s = AssignmentStats(
            total=10, assigned=4, in_progress=2,
            completed=3, declined=1, overdue=2,
        )
        assert s.total == 10
        assert s.assigned == 4
        assert s.in_progress == 2
        assert s.completed == 3
        assert s.declined == 1
        assert s.overdue == 2

    def test_zero_values(self):
        s = AssignmentStats(
            total=0, assigned=0, in_progress=0,
            completed=0, declined=0, overdue=0,
        )
        assert s.total == 0
        assert s.overdue == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty(self):
        a = _make()
        assert isinstance(a, DocReviewAssignment)

    def test_initial_stats(self):
        a = _make()
        s = a.stats()
        assert s.total == 0
        assert s.assigned == 0
        assert s.in_progress == 0
        assert s.completed == 0
        assert s.declined == 0
        assert s.overdue == 0

    def test_initial_get_missing(self):
        a = _make()
        assert a.get("nope") is None

    def test_initial_doc_lookup_empty(self):
        a = _make()
        assert a.assignments_for_doc("doc-x") == []

    def test_initial_reviewer_lookup_empty(self):
        a = _make()
        assert a.assignments_for_reviewer("alice") == []


# ---------------------------------------------------------------------------
# TestAssign
# ---------------------------------------------------------------------------

class TestAssign:
    def test_returns_review_assignment(self):
        a = _make()
        r = _assign(a)
        assert isinstance(r, ReviewAssignment)

    def test_assignment_id_generated(self):
        a = _make()
        r1 = _assign(a)
        r2 = _assign(a)
        assert r1.assignment_id != r2.assignment_id
        assert len(r1.assignment_id) > 0

    def test_initial_status_is_assigned(self):
        a = _make()
        r = _assign(a)
        assert r.status == "assigned"

    def test_assigned_at_set(self):
        a = _make()
        r = _assign(a, now=42.5)
        assert r.assigned_at == 42.5

    def test_assigned_at_defaults_to_time(self):
        a = _make()
        before = time.time()
        r = a.assign(doc_id="d", reviewer="a", assigned_by="b")
        after = time.time()
        assert before <= r.assigned_at <= after

    def test_due_date_none_default(self):
        a = _make()
        r = _assign(a)
        assert r.due_date is None

    def test_due_date_set(self):
        a = _make()
        r = _assign(a, due_date=100.0)
        assert r.due_date == 100.0

    def test_note_stored(self):
        a = _make()
        r = _assign(a, note="please be thorough")
        assert r.note == "please be thorough"

    def test_completed_at_none_initially(self):
        a = _make()
        r = _assign(a)
        assert r.completed_at is None

    def test_assigned_by_stored(self):
        a = _make()
        r = _assign(a, assigned_by="manager42")
        assert r.assigned_by == "manager42"

    def test_indexed_by_doc(self):
        a = _make()
        r = _assign(a, doc_id="doc-X")
        items = a.assignments_for_doc("doc-X")
        assert len(items) == 1
        assert items[0].assignment_id == r.assignment_id

    def test_indexed_by_reviewer(self):
        a = _make()
        r = _assign(a, reviewer="rev-X")
        items = a.assignments_for_reviewer("rev-X")
        assert len(items) == 1
        assert items[0].assignment_id == r.assignment_id

    def test_multiple_for_same_doc(self):
        a = _make()
        _assign(a, doc_id="d1", reviewer="r1", now=1.0)
        _assign(a, doc_id="d1", reviewer="r2", now=2.0)
        assert len(a.assignments_for_doc("d1")) == 2


# ---------------------------------------------------------------------------
# TestStart
# ---------------------------------------------------------------------------

class TestStart:
    def test_start_from_assigned(self):
        a = _make()
        r = _assign(a)
        assert a.start(r.assignment_id) is True
        assert a.get(r.assignment_id).status == "in_progress"

    def test_start_unknown(self):
        a = _make()
        assert a.start("missing") is False

    def test_start_already_in_progress(self):
        a = _make()
        r = _assign(a)
        a.start(r.assignment_id)
        assert a.start(r.assignment_id) is False

    def test_start_after_completed(self):
        a = _make()
        r = _assign(a)
        a.complete(r.assignment_id)
        assert a.start(r.assignment_id) is False

    def test_start_after_declined(self):
        a = _make()
        r = _assign(a)
        a.decline(r.assignment_id)
        assert a.start(r.assignment_id) is False


# ---------------------------------------------------------------------------
# TestComplete
# ---------------------------------------------------------------------------

class TestComplete:
    def test_complete_from_assigned(self):
        a = _make()
        r = _assign(a)
        assert a.complete(r.assignment_id, now=10.0) is True
        got = a.get(r.assignment_id)
        assert got.status == "completed"
        assert got.completed_at == 10.0

    def test_complete_from_in_progress(self):
        a = _make()
        r = _assign(a)
        a.start(r.assignment_id)
        assert a.complete(r.assignment_id, now=20.0) is True
        got = a.get(r.assignment_id)
        assert got.status == "completed"
        assert got.completed_at == 20.0

    def test_complete_unknown(self):
        a = _make()
        assert a.complete("nope") is False

    def test_complete_already_completed(self):
        a = _make()
        r = _assign(a)
        a.complete(r.assignment_id)
        assert a.complete(r.assignment_id) is False

    def test_complete_after_declined(self):
        a = _make()
        r = _assign(a)
        a.decline(r.assignment_id)
        assert a.complete(r.assignment_id) is False

    def test_complete_default_now(self):
        a = _make()
        r = _assign(a)
        before = time.time()
        a.complete(r.assignment_id)
        after = time.time()
        c = a.get(r.assignment_id).completed_at
        assert before <= c <= after


# ---------------------------------------------------------------------------
# TestDecline
# ---------------------------------------------------------------------------

class TestDecline:
    def test_decline_from_assigned(self):
        a = _make()
        r = _assign(a)
        assert a.decline(r.assignment_id) is True
        assert a.get(r.assignment_id).status == "declined"

    def test_decline_from_in_progress(self):
        a = _make()
        r = _assign(a)
        a.start(r.assignment_id)
        assert a.decline(r.assignment_id) is True
        assert a.get(r.assignment_id).status == "declined"

    def test_decline_unknown(self):
        a = _make()
        assert a.decline("missing") is False

    def test_decline_already_completed(self):
        a = _make()
        r = _assign(a)
        a.complete(r.assignment_id)
        assert a.decline(r.assignment_id) is False

    def test_decline_already_declined(self):
        a = _make()
        r = _assign(a)
        a.decline(r.assignment_id)
        assert a.decline(r.assignment_id) is False


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------

class TestGet:
    def test_get_existing(self):
        a = _make()
        r = _assign(a)
        got = a.get(r.assignment_id)
        assert got is r or got == r
        assert got.doc_id == r.doc_id

    def test_get_missing(self):
        a = _make()
        assert a.get("nope") is None


# ---------------------------------------------------------------------------
# TestAssignmentsForDoc
# ---------------------------------------------------------------------------

class TestAssignmentsForDoc:
    def test_returns_only_for_doc(self):
        a = _make()
        _assign(a, doc_id="d1")
        _assign(a, doc_id="d2")
        items = a.assignments_for_doc("d1")
        assert len(items) == 1
        assert items[0].doc_id == "d1"

    def test_sorted_by_assigned_at(self):
        a = _make()
        _assign(a, doc_id="d", reviewer="r1", now=5.0)
        _assign(a, doc_id="d", reviewer="r2", now=2.0)
        _assign(a, doc_id="d", reviewer="r3", now=8.0)
        items = a.assignments_for_doc("d")
        assert [i.assigned_at for i in items] == [2.0, 5.0, 8.0]

    def test_empty_for_unknown_doc(self):
        a = _make()
        _assign(a, doc_id="d1")
        assert a.assignments_for_doc("nope") == []

    def test_status_filter(self):
        a = _make()
        r1 = _assign(a, doc_id="d", reviewer="r1", now=1.0)
        _assign(a, doc_id="d", reviewer="r2", now=2.0)
        a.complete(r1.assignment_id)
        items = a.assignments_for_doc("d", status="completed")
        assert len(items) == 1
        assert items[0].assignment_id == r1.assignment_id

    def test_status_filter_none_returns_all(self):
        a = _make()
        _assign(a, doc_id="d", reviewer="r1")
        _assign(a, doc_id="d", reviewer="r2")
        assert len(a.assignments_for_doc("d", status=None)) == 2


# ---------------------------------------------------------------------------
# TestAssignmentsForReviewer
# ---------------------------------------------------------------------------

class TestAssignmentsForReviewer:
    def test_returns_only_for_reviewer(self):
        a = _make()
        _assign(a, reviewer="alice")
        _assign(a, reviewer="bob")
        items = a.assignments_for_reviewer("alice")
        assert len(items) == 1
        assert items[0].reviewer == "alice"

    def test_sorted_by_assigned_at(self):
        a = _make()
        _assign(a, reviewer="alice", doc_id="d1", now=10.0)
        _assign(a, reviewer="alice", doc_id="d2", now=1.0)
        _assign(a, reviewer="alice", doc_id="d3", now=5.0)
        items = a.assignments_for_reviewer("alice")
        assert [i.assigned_at for i in items] == [1.0, 5.0, 10.0]

    def test_empty_for_unknown_reviewer(self):
        a = _make()
        _assign(a, reviewer="alice")
        assert a.assignments_for_reviewer("zorg") == []

    def test_status_filter(self):
        a = _make()
        r1 = _assign(a, reviewer="alice", doc_id="d1", now=1.0)
        _assign(a, reviewer="alice", doc_id="d2", now=2.0)
        a.start(r1.assignment_id)
        items = a.assignments_for_reviewer("alice", status="in_progress")
        assert len(items) == 1
        assert items[0].assignment_id == r1.assignment_id


# ---------------------------------------------------------------------------
# TestOverdue
# ---------------------------------------------------------------------------

class TestOverdue:
    def test_overdue_assigned(self):
        a = _make()
        r = _assign(a, due_date=10.0, now=1.0)
        items = a.overdue(now=100.0)
        assert len(items) == 1
        assert items[0].assignment_id == r.assignment_id

    def test_overdue_in_progress(self):
        a = _make()
        r = _assign(a, due_date=10.0, now=1.0)
        a.start(r.assignment_id)
        items = a.overdue(now=100.0)
        assert len(items) == 1

    def test_not_overdue_when_due_in_future(self):
        a = _make()
        _assign(a, due_date=200.0, now=1.0)
        assert a.overdue(now=100.0) == []

    def test_not_overdue_no_due_date(self):
        a = _make()
        _assign(a, due_date=None, now=1.0)
        assert a.overdue(now=100.0) == []

    def test_completed_not_overdue(self):
        a = _make()
        r = _assign(a, due_date=10.0, now=1.0)
        a.complete(r.assignment_id)
        assert a.overdue(now=100.0) == []

    def test_declined_not_overdue(self):
        a = _make()
        r = _assign(a, due_date=10.0, now=1.0)
        a.decline(r.assignment_id)
        assert a.overdue(now=100.0) == []

    def test_sorted_asc(self):
        a = _make()
        _assign(a, doc_id="d1", reviewer="r1", due_date=50.0, now=1.0)
        _assign(a, doc_id="d2", reviewer="r2", due_date=20.0, now=1.0)
        _assign(a, doc_id="d3", reviewer="r3", due_date=40.0, now=1.0)
        items = a.overdue(now=100.0)
        assert [i.due_date for i in items] == [20.0, 40.0, 50.0]

    def test_default_now(self):
        a = _make()
        _assign(a, due_date=1.0, now=0.0)  # in past
        items = a.overdue()  # uses time.time()
        assert len(items) == 1


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing(self):
        a = _make()
        r = _assign(a)
        assert a.delete(r.assignment_id) is True
        assert a.get(r.assignment_id) is None

    def test_delete_missing(self):
        a = _make()
        assert a.delete("nope") is False

    def test_delete_removes_from_doc_index(self):
        a = _make()
        r = _assign(a, doc_id="d1")
        a.delete(r.assignment_id)
        assert a.assignments_for_doc("d1") == []

    def test_delete_removes_from_reviewer_index(self):
        a = _make()
        r = _assign(a, reviewer="alice")
        a.delete(r.assignment_id)
        assert a.assignments_for_reviewer("alice") == []

    def test_delete_one_keeps_others(self):
        a = _make()
        r1 = _assign(a, doc_id="d1", reviewer="alice", now=1.0)
        r2 = _assign(a, doc_id="d1", reviewer="bob", now=2.0)
        a.delete(r1.assignment_id)
        items = a.assignments_for_doc("d1")
        assert len(items) == 1
        assert items[0].assignment_id == r2.assignment_id


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_counts_by_status(self):
        a = _make()
        r1 = _assign(a, doc_id="d1", reviewer="a", now=1.0)
        r2 = _assign(a, doc_id="d2", reviewer="b", now=1.0)
        r3 = _assign(a, doc_id="d3", reviewer="c", now=1.0)
        r4 = _assign(a, doc_id="d4", reviewer="d", now=1.0)
        _assign(a, doc_id="d5", reviewer="e", now=1.0)
        a.start(r1.assignment_id)
        a.complete(r2.assignment_id)
        a.decline(r3.assignment_id)
        # r4 and the 5th remain "assigned"
        _ = r4
        s = a.stats()
        assert s.total == 5
        assert s.assigned == 2
        assert s.in_progress == 1
        assert s.completed == 1
        assert s.declined == 1

    def test_overdue_count(self):
        a = _make()
        _assign(a, doc_id="d1", reviewer="r1", due_date=10.0, now=1.0)
        _assign(a, doc_id="d2", reviewer="r2", due_date=200.0, now=1.0)
        r3 = _assign(a, doc_id="d3", reviewer="r3", due_date=10.0, now=1.0)
        a.complete(r3.assignment_id)
        s = a.stats(now=100.0)
        # only the first is overdue and active
        assert s.overdue == 1

    def test_stats_empty(self):
        a = _make()
        s = a.stats()
        assert s.total == 0
        assert s.assigned == 0
        assert s.overdue == 0

    def test_stats_overdue_default_now(self):
        a = _make()
        _assign(a, due_date=1.0, now=0.0)  # past
        s = a.stats()
        assert s.overdue == 1


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_assign(self):
        a = _make()
        N = 50
        T = 8
        results: list[ReviewAssignment] = []
        lock = threading.Lock()

        def worker(tid: int):
            for i in range(N):
                r = a.assign(
                    doc_id=f"doc-{tid}",
                    reviewer=f"rev-{tid}",
                    assigned_by="boss",
                    now=float(i),
                )
                with lock:
                    results.append(r)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(T)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        assert len(results) == N * T
        ids = {r.assignment_id for r in results}
        assert len(ids) == N * T  # all unique
        assert a.stats().total == N * T

    def test_concurrent_assign_and_complete(self):
        a = _make()
        created: list[str] = []
        lock = threading.Lock()

        def assigner():
            for i in range(30):
                r = a.assign(
                    doc_id=f"d{i}", reviewer="rev",
                    assigned_by="boss", now=float(i),
                )
                with lock:
                    created.append(r.assignment_id)

        def completer():
            for _ in range(50):
                with lock:
                    ids = list(created)
                for aid in ids:
                    a.complete(aid)

        t1 = threading.Thread(target=assigner)
        t2 = threading.Thread(target=completer)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        # final pass to complete any leftovers
        for aid in created:
            a.complete(aid)
        s = a.stats()
        assert s.total == 30
        assert s.completed == 30
