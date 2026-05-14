"""Tests for docstoolkit.doc_review_queue (E312)."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_review_queue import (
    DocReviewQueue,
    QueueStats,
    ReviewDecision,
    ReviewItem,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_queue() -> DocReviewQueue:
    return DocReviewQueue()


def _submit(q: DocReviewQueue, doc_id: str = "doc-1", requester: str = "alice",
            priority: int = 0, note: str = "", now: float = 1.0) -> ReviewItem:
    return q.submit(doc_id=doc_id, requester=requester, priority=priority,
                    note=note, now=now)


# ---------------------------------------------------------------------------
# TestReviewItemDataclass
# ---------------------------------------------------------------------------

class TestReviewItemDataclass:
    def test_required_fields(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.item_id == "id1"
        assert item.doc_id == "doc-1"
        assert item.requester == "alice"

    def test_default_submitted_at(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.submitted_at == 0.0

    def test_default_priority(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.priority == 0

    def test_default_status(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.status == "pending"

    def test_default_assigned_to(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.assigned_to is None

    def test_default_note(self):
        item = ReviewItem(item_id="id1", doc_id="doc-1", requester="alice")
        assert item.note == ""

    def test_custom_values(self):
        item = ReviewItem(
            item_id="id2", doc_id="doc-2", requester="bob",
            submitted_at=42.0, priority=5, status="in_review",
            assigned_to="carol", note="urgent"
        )
        assert item.submitted_at == 42.0
        assert item.priority == 5
        assert item.status == "in_review"
        assert item.assigned_to == "carol"
        assert item.note == "urgent"


# ---------------------------------------------------------------------------
# TestReviewDecisionDataclass
# ---------------------------------------------------------------------------

class TestReviewDecisionDataclass:
    def test_required_fields(self):
        d = ReviewDecision(item_id="id1", doc_id="doc-1", reviewer="bob",
                           decision="approved")
        assert d.item_id == "id1"
        assert d.doc_id == "doc-1"
        assert d.reviewer == "bob"
        assert d.decision == "approved"

    def test_default_decided_at(self):
        d = ReviewDecision(item_id="id1", doc_id="doc-1", reviewer="bob",
                           decision="approved")
        assert d.decided_at == 0.0

    def test_default_comment(self):
        d = ReviewDecision(item_id="id1", doc_id="doc-1", reviewer="bob",
                           decision="approved")
        assert d.comment == ""

    def test_rejected_decision(self):
        d = ReviewDecision(item_id="id1", doc_id="doc-1", reviewer="bob",
                           decision="rejected", decided_at=10.0, comment="not ready")
        assert d.decision == "rejected"
        assert d.decided_at == 10.0
        assert d.comment == "not ready"


# ---------------------------------------------------------------------------
# TestQueueStatsDataclass
# ---------------------------------------------------------------------------

class TestQueueStatsDataclass:
    def test_all_fields(self):
        s = QueueStats(pending=1, in_review=2, approved=3,
                       rejected=4, withdrawn=5, total=15)
        assert s.pending == 1
        assert s.in_review == 2
        assert s.approved == 3
        assert s.rejected == 4
        assert s.withdrawn == 5
        assert s.total == 15

    def test_zero_stats(self):
        s = QueueStats(pending=0, in_review=0, approved=0,
                       rejected=0, withdrawn=0, total=0)
        assert s.total == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_empty_queue(self):
        q = _make_queue()
        s = q.stats()
        assert s.total == 0

    def test_empty_pending(self):
        q = _make_queue()
        assert q.pending_items() == []

    def test_empty_stats_all_zero(self):
        q = _make_queue()
        s = q.stats()
        assert s.pending == 0
        assert s.in_review == 0
        assert s.approved == 0
        assert s.rejected == 0
        assert s.withdrawn == 0


# ---------------------------------------------------------------------------
# TestSubmit
# ---------------------------------------------------------------------------

class TestSubmit:
    def test_returns_review_item(self):
        q = _make_queue()
        item = _submit(q)
        assert isinstance(item, ReviewItem)

    def test_item_id_is_nonempty_string(self):
        q = _make_queue()
        item = _submit(q)
        assert isinstance(item.item_id, str)
        assert len(item.item_id) > 0

    def test_item_id_is_unique(self):
        q = _make_queue()
        ids = {_submit(q).item_id for _ in range(50)}
        assert len(ids) == 50

    def test_doc_id_stored(self):
        q = _make_queue()
        item = _submit(q, doc_id="doc-xyz")
        assert item.doc_id == "doc-xyz"

    def test_requester_stored(self):
        q = _make_queue()
        item = _submit(q, requester="mallory")
        assert item.requester == "mallory"

    def test_submitted_at_stored(self):
        q = _make_queue()
        item = _submit(q, now=99.5)
        assert item.submitted_at == 99.5

    def test_priority_stored(self):
        q = _make_queue()
        item = _submit(q, priority=7)
        assert item.priority == 7

    def test_initial_status_is_pending(self):
        q = _make_queue()
        item = _submit(q)
        assert item.status == "pending"

    def test_note_stored(self):
        q = _make_queue()
        item = _submit(q, note="please review ASAP")
        assert item.note == "please review ASAP"

    def test_item_retrievable_after_submit(self):
        q = _make_queue()
        item = _submit(q)
        assert q.get_item(item.item_id) is item

    def test_stats_total_increments(self):
        q = _make_queue()
        _submit(q)
        _submit(q)
        assert q.stats().total == 2

    def test_stats_pending_increments(self):
        q = _make_queue()
        _submit(q)
        _submit(q)
        assert q.stats().pending == 2


# ---------------------------------------------------------------------------
# TestAssign
# ---------------------------------------------------------------------------

class TestAssign:
    def test_assign_pending_returns_true(self):
        q = _make_queue()
        item = _submit(q)
        assert q.assign(item.item_id, "bob") is True

    def test_assign_sets_in_review(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        assert item.status == "in_review"

    def test_assign_sets_assigned_to(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        assert item.assigned_to == "bob"

    def test_assign_missing_returns_false(self):
        q = _make_queue()
        assert q.assign("no-such-id", "bob") is False

    def test_assign_already_in_review_returns_false(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        assert q.assign(item.item_id, "carol") is False

    def test_assign_approved_returns_false(self):
        q = _make_queue()
        item = _submit(q)
        q.approve(item.item_id, "bob", now=2.0)
        assert q.assign(item.item_id, "carol") is False

    def test_assign_withdrawn_returns_false(self):
        q = _make_queue()
        item = _submit(q)
        q.withdraw(item.item_id)
        assert q.assign(item.item_id, "bob") is False


# ---------------------------------------------------------------------------
# TestApprove
# ---------------------------------------------------------------------------

class TestApprove:
    def test_approve_returns_decision(self):
        q = _make_queue()
        item = _submit(q)
        decision = q.approve(item.item_id, "bob", now=5.0)
        assert isinstance(decision, ReviewDecision)

    def test_approve_sets_status_approved(self):
        q = _make_queue()
        item = _submit(q)
        q.approve(item.item_id, "bob", now=5.0)
        assert item.status == "approved"

    def test_approve_decision_fields(self):
        q = _make_queue()
        item = _submit(q, doc_id="doc-42")
        decision = q.approve(item.item_id, "bob", comment="LGTM", now=5.0)
        assert decision.item_id == item.item_id
        assert decision.doc_id == "doc-42"
        assert decision.reviewer == "bob"
        assert decision.decision == "approved"
        assert decision.decided_at == 5.0
        assert decision.comment == "LGTM"

    def test_approve_decision_retrievable(self):
        q = _make_queue()
        item = _submit(q)
        decision = q.approve(item.item_id, "bob", now=5.0)
        assert q.get_decision(item.item_id) is decision

    def test_approve_missing_returns_none(self):
        q = _make_queue()
        assert q.approve("ghost-id", "bob", now=5.0) is None

    def test_approve_can_approve_in_review(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        decision = q.approve(item.item_id, "bob", now=7.0)
        assert decision is not None
        assert item.status == "approved"


# ---------------------------------------------------------------------------
# TestReject
# ---------------------------------------------------------------------------

class TestReject:
    def test_reject_returns_decision(self):
        q = _make_queue()
        item = _submit(q)
        decision = q.reject(item.item_id, "bob", now=6.0)
        assert isinstance(decision, ReviewDecision)

    def test_reject_sets_status_rejected(self):
        q = _make_queue()
        item = _submit(q)
        q.reject(item.item_id, "bob", now=6.0)
        assert item.status == "rejected"

    def test_reject_decision_fields(self):
        q = _make_queue()
        item = _submit(q, doc_id="doc-99")
        decision = q.reject(item.item_id, "carol", comment="needs work", now=6.0)
        assert decision.decision == "rejected"
        assert decision.reviewer == "carol"
        assert decision.comment == "needs work"
        assert decision.decided_at == 6.0
        assert decision.doc_id == "doc-99"

    def test_reject_decision_retrievable(self):
        q = _make_queue()
        item = _submit(q)
        decision = q.reject(item.item_id, "carol", now=6.0)
        assert q.get_decision(item.item_id) is decision

    def test_reject_missing_returns_none(self):
        q = _make_queue()
        assert q.reject("ghost-id", "carol", now=6.0) is None


# ---------------------------------------------------------------------------
# TestWithdraw
# ---------------------------------------------------------------------------

class TestWithdraw:
    def test_withdraw_pending_returns_true(self):
        q = _make_queue()
        item = _submit(q)
        assert q.withdraw(item.item_id) is True

    def test_withdraw_sets_status_withdrawn(self):
        q = _make_queue()
        item = _submit(q)
        q.withdraw(item.item_id)
        assert item.status == "withdrawn"

    def test_withdraw_in_review_returns_true(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        assert q.withdraw(item.item_id) is True

    def test_withdraw_in_review_sets_withdrawn(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        q.withdraw(item.item_id)
        assert item.status == "withdrawn"

    def test_withdraw_approved_returns_false(self):
        q = _make_queue()
        item = _submit(q)
        q.approve(item.item_id, "bob", now=2.0)
        assert q.withdraw(item.item_id) is False

    def test_withdraw_rejected_returns_false(self):
        q = _make_queue()
        item = _submit(q)
        q.reject(item.item_id, "bob", now=2.0)
        assert q.withdraw(item.item_id) is False

    def test_withdraw_missing_returns_false(self):
        q = _make_queue()
        assert q.withdraw("no-such-id") is False


# ---------------------------------------------------------------------------
# TestGetItem
# ---------------------------------------------------------------------------

class TestGetItem:
    def test_get_existing_item(self):
        q = _make_queue()
        item = _submit(q)
        assert q.get_item(item.item_id) is item

    def test_get_missing_item_returns_none(self):
        q = _make_queue()
        assert q.get_item("nonexistent") is None


# ---------------------------------------------------------------------------
# TestGetDecision
# ---------------------------------------------------------------------------

class TestGetDecision:
    def test_get_existing_decision(self):
        q = _make_queue()
        item = _submit(q)
        decision = q.approve(item.item_id, "bob", now=3.0)
        assert q.get_decision(item.item_id) is decision

    def test_get_decision_before_review_returns_none(self):
        q = _make_queue()
        item = _submit(q)
        assert q.get_decision(item.item_id) is None

    def test_get_missing_decision_returns_none(self):
        q = _make_queue()
        assert q.get_decision("ghost") is None


# ---------------------------------------------------------------------------
# TestPendingItems
# ---------------------------------------------------------------------------

class TestPendingItems:
    def test_only_pending_items_returned(self):
        q = _make_queue()
        item1 = _submit(q, now=1.0)
        item2 = _submit(q, now=2.0)
        q.approve(item2.item_id, "bob", now=3.0)
        pending = q.pending_items()
        assert item1 in pending
        assert item2 not in pending

    def test_sorted_by_priority_desc(self):
        q = _make_queue()
        low = _submit(q, priority=1, now=1.0)
        high = _submit(q, priority=10, now=2.0)
        mid = _submit(q, priority=5, now=3.0)
        pending = q.pending_items()
        assert pending[0] is high
        assert pending[1] is mid
        assert pending[2] is low

    def test_same_priority_sorted_by_submitted_at(self):
        q = _make_queue()
        early = _submit(q, priority=3, now=1.0)
        late = _submit(q, priority=3, now=5.0)
        pending = q.pending_items()
        assert pending[0] is early
        assert pending[1] is late

    def test_empty_when_no_pending(self):
        q = _make_queue()
        item = _submit(q)
        q.approve(item.item_id, "bob", now=2.0)
        assert q.pending_items() == []

    def test_withdrawn_not_in_pending(self):
        q = _make_queue()
        item = _submit(q)
        q.withdraw(item.item_id)
        assert q.pending_items() == []


# ---------------------------------------------------------------------------
# TestItemsForDoc
# ---------------------------------------------------------------------------

class TestItemsForDoc:
    def test_returns_items_for_doc(self):
        q = _make_queue()
        a = _submit(q, doc_id="doc-A", now=1.0)
        b = _submit(q, doc_id="doc-A", now=2.0)
        _submit(q, doc_id="doc-B", now=3.0)
        items = q.items_for_doc("doc-A")
        assert len(items) == 2
        assert a in items
        assert b in items

    def test_sorted_by_submitted_at(self):
        q = _make_queue()
        first = _submit(q, doc_id="doc-A", now=1.0)
        second = _submit(q, doc_id="doc-A", now=3.0)
        items = q.items_for_doc("doc-A")
        assert items[0] is first
        assert items[1] is second

    def test_empty_for_unknown_doc(self):
        q = _make_queue()
        assert q.items_for_doc("nonexistent-doc") == []

    def test_includes_all_statuses(self):
        q = _make_queue()
        item1 = _submit(q, doc_id="doc-A", now=1.0)
        item2 = _submit(q, doc_id="doc-A", now=2.0)
        q.approve(item2.item_id, "bob", now=3.0)
        items = q.items_for_doc("doc-A")
        assert len(items) == 2


# ---------------------------------------------------------------------------
# TestItemsByStatus
# ---------------------------------------------------------------------------

class TestItemsByStatus:
    def test_filters_by_pending(self):
        q = _make_queue()
        item = _submit(q, now=1.0)
        items = q.items_by_status("pending")
        assert item in items

    def test_filters_by_in_review(self):
        q = _make_queue()
        item = _submit(q, now=1.0)
        q.assign(item.item_id, "bob")
        items = q.items_by_status("in_review")
        assert item in items
        assert q.items_by_status("pending") == []

    def test_filters_by_approved(self):
        q = _make_queue()
        item = _submit(q, now=1.0)
        q.approve(item.item_id, "bob", now=2.0)
        items = q.items_by_status("approved")
        assert item in items

    def test_filters_by_rejected(self):
        q = _make_queue()
        item = _submit(q, now=1.0)
        q.reject(item.item_id, "bob", now=2.0)
        items = q.items_by_status("rejected")
        assert item in items

    def test_filters_by_withdrawn(self):
        q = _make_queue()
        item = _submit(q, now=1.0)
        q.withdraw(item.item_id)
        items = q.items_by_status("withdrawn")
        assert item in items

    def test_sorted_by_submitted_at(self):
        q = _make_queue()
        first = _submit(q, now=1.0)
        second = _submit(q, now=3.0)
        items = q.items_by_status("pending")
        assert items[0] is first
        assert items[1] is second

    def test_empty_for_unknown_status(self):
        q = _make_queue()
        _submit(q, now=1.0)
        assert q.items_by_status("nonexistent") == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_stats(self):
        q = _make_queue()
        s = q.stats()
        assert s == QueueStats(pending=0, in_review=0, approved=0,
                               rejected=0, withdrawn=0, total=0)

    def test_pending_count(self):
        q = _make_queue()
        _submit(q)
        _submit(q)
        s = q.stats()
        assert s.pending == 2
        assert s.total == 2

    def test_in_review_count(self):
        q = _make_queue()
        item = _submit(q)
        q.assign(item.item_id, "bob")
        s = q.stats()
        assert s.in_review == 1
        assert s.pending == 0

    def test_approved_count(self):
        q = _make_queue()
        item = _submit(q)
        q.approve(item.item_id, "bob", now=2.0)
        s = q.stats()
        assert s.approved == 1

    def test_rejected_count(self):
        q = _make_queue()
        item = _submit(q)
        q.reject(item.item_id, "bob", now=2.0)
        s = q.stats()
        assert s.rejected == 1

    def test_withdrawn_count(self):
        q = _make_queue()
        item = _submit(q)
        q.withdraw(item.item_id)
        s = q.stats()
        assert s.withdrawn == 1

    def test_mixed_counts(self):
        q = _make_queue()
        p1 = _submit(q, now=1.0)
        p2 = _submit(q, now=2.0)
        ir = _submit(q, now=3.0)
        ap = _submit(q, now=4.0)
        rj = _submit(q, now=5.0)
        wd = _submit(q, now=6.0)
        q.assign(ir.item_id, "bob")
        q.approve(ap.item_id, "bob", now=7.0)
        q.reject(rj.item_id, "carol", now=7.0)
        q.withdraw(wd.item_id)
        s = q.stats()
        assert s.pending == 2
        assert s.in_review == 1
        assert s.approved == 1
        assert s.rejected == 1
        assert s.withdrawn == 1
        assert s.total == 6


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_submit(self):
        q = _make_queue()
        results: list[ReviewItem] = []
        lock = threading.Lock()

        def worker():
            item = q.submit(doc_id="doc-concurrent", requester="user")
            with lock:
                results.append(item)

        threads = [threading.Thread(target=worker) for _ in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 50
        ids = {item.item_id for item in results}
        assert len(ids) == 50
        assert q.stats().total == 50

    def test_concurrent_approve_reject(self):
        q = _make_queue()
        items = [_submit(q, doc_id=f"doc-{i}", now=float(i)) for i in range(20)]
        errors: list[Exception] = []

        def approve_worker(item: ReviewItem):
            try:
                q.approve(item.item_id, "reviewer", now=100.0)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=approve_worker, args=(item,)) for item in items]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        s = q.stats()
        assert s.approved == 20
