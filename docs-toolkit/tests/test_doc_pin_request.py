"""Tests for E383 DocPinRequest."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_pin_request import (
    DocPinRequest,
    PinRequest,
    PinRequestStats,
)


# --------------------------------------------------------------------- dataclasses


class TestPinRequestDataclass:
    def test_construct_minimal(self):
        r = PinRequest(request_id="r1", doc_id="d1", requested_by="alice")
        assert r.request_id == "r1"
        assert r.doc_id == "d1"
        assert r.requested_by == "alice"

    def test_defaults(self):
        r = PinRequest(request_id="r1", doc_id="d1", requested_by="alice")
        assert r.reason == ""
        assert r.created_at == 0.0
        assert r.status == "pending"
        assert r.decided_by == ""
        assert r.decided_at is None
        assert r.decision_note == ""

    def test_construct_full(self):
        r = PinRequest(
            request_id="r1",
            doc_id="d1",
            requested_by="alice",
            reason="important",
            created_at=100.0,
            status="approved",
            decided_by="bob",
            decided_at=200.0,
            decision_note="ok",
        )
        assert r.reason == "important"
        assert r.created_at == 100.0
        assert r.status == "approved"
        assert r.decided_by == "bob"
        assert r.decided_at == 200.0
        assert r.decision_note == "ok"

    def test_mutable(self):
        r = PinRequest(request_id="r1", doc_id="d1", requested_by="alice")
        r.status = "approved"
        assert r.status == "approved"


class TestPinRequestStatsDataclass:
    def test_construct(self):
        s = PinRequestStats(total=5, pending=2, approved=1, rejected=1, expired=1)
        assert s.total == 5
        assert s.pending == 2
        assert s.approved == 1
        assert s.rejected == 1
        assert s.expired == 1

    def test_zero(self):
        s = PinRequestStats(total=0, pending=0, approved=0, rejected=0, expired=0)
        assert s.total == 0
        assert s.pending == 0


# --------------------------------------------------------------------- construction


class TestConstruction:
    def test_default_empty(self):
        store = DocPinRequest()
        assert store.stats().total == 0

    def test_independent_instances(self):
        a = DocPinRequest()
        b = DocPinRequest()
        a.request_pin("d1", "u1")
        assert a.stats().total == 1
        assert b.stats().total == 0


# --------------------------------------------------------------------- request_pin


class TestRequestPin:
    def test_basic(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert r.doc_id == "d1"
        assert r.requested_by == "alice"
        assert r.status == "pending"

    def test_uuid_unique(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        r2 = store.request_pin("d1", "alice")
        assert r1.request_id != r2.request_id

    def test_uuid_hex_length(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        # uuid4().hex is 32 chars
        assert len(r.request_id) == 32

    def test_reason_stored(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", reason="critical")
        assert r.reason == "critical"

    def test_status_pending(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert r.status == "pending"

    def test_created_at_from_now(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", now=1234.5)
        assert r.created_at == 1234.5

    def test_created_at_default(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert r.created_at > 0

    def test_stored(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.get(r.request_id) is r


# --------------------------------------------------------------------- approve


class TestApprove:
    def test_approve_pending(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.approve(r.request_id, "bob") is True
        assert store.get(r.request_id).status == "approved"

    def test_approve_sets_decided_by(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.approve(r.request_id, "bob", note="ok", now=999.0)
        got = store.get(r.request_id)
        assert got.decided_by == "bob"
        assert got.decision_note == "ok"
        assert got.decided_at == 999.0

    def test_approve_unknown(self):
        store = DocPinRequest()
        assert store.approve("missing", "bob") is False

    def test_approve_twice(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.approve(r.request_id, "bob") is True
        assert store.approve(r.request_id, "carol") is False

    def test_approve_rejected_fails(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.reject(r.request_id, "bob")
        assert store.approve(r.request_id, "carol") is False

    def test_approve_expired_fails(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", now=0.0)
        store.expire_old(10.0, now=100.0)
        assert store.approve(r.request_id, "bob") is False


# --------------------------------------------------------------------- reject


class TestReject:
    def test_reject_pending(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.reject(r.request_id, "bob") is True
        assert store.get(r.request_id).status == "rejected"

    def test_reject_sets_decided_by(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.reject(r.request_id, "bob", note="no", now=500.0)
        got = store.get(r.request_id)
        assert got.decided_by == "bob"
        assert got.decision_note == "no"
        assert got.decided_at == 500.0

    def test_reject_unknown(self):
        store = DocPinRequest()
        assert store.reject("missing", "bob") is False

    def test_reject_twice(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.reject(r.request_id, "bob") is True
        assert store.reject(r.request_id, "carol") is False

    def test_reject_approved_fails(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.approve(r.request_id, "bob")
        assert store.reject(r.request_id, "carol") is False


# --------------------------------------------------------------------- expire_old


class TestExpireOld:
    def test_expire_one(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice", now=0.0)
        count = store.expire_old(10.0, now=100.0)
        assert count == 1

    def test_expire_none(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice", now=0.0)
        count = store.expire_old(1000.0, now=50.0)
        assert count == 0

    def test_expire_many(self):
        store = DocPinRequest()
        for _ in range(5):
            store.request_pin("d1", "alice", now=0.0)
        count = store.expire_old(10.0, now=100.0)
        assert count == 5

    def test_expire_sets_status(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", now=0.0)
        store.expire_old(10.0, now=100.0)
        assert store.get(r.request_id).status == "expired"

    def test_expire_skips_approved(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", now=0.0)
        store.approve(r.request_id, "bob")
        count = store.expire_old(10.0, now=1000.0)
        assert count == 0
        assert store.get(r.request_id).status == "approved"

    def test_expire_skips_rejected(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice", now=0.0)
        store.reject(r.request_id, "bob")
        count = store.expire_old(10.0, now=1000.0)
        assert count == 0

    def test_expire_only_old(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice", now=0.0)
        store.request_pin("d2", "alice", now=95.0)
        count = store.expire_old(10.0, now=100.0)
        assert count == 1


# --------------------------------------------------------------------- get


class TestGet:
    def test_get_existing(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.get(r.request_id) is not None

    def test_get_missing(self):
        store = DocPinRequest()
        assert store.get("nope") is None

    def test_get_returns_same(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        got = store.get(r.request_id)
        assert got.doc_id == "d1"
        assert got.requested_by == "alice"


# --------------------------------------------------------------------- requests_for_doc


class TestRequestsForDoc:
    def test_empty(self):
        store = DocPinRequest()
        assert store.requests_for_doc("d1") == []

    def test_filter_by_doc(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice")
        store.request_pin("d2", "alice")
        store.request_pin("d1", "bob")
        result = store.requests_for_doc("d1")
        assert len(result) == 2

    def test_sorted_by_created_at(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice", now=300.0)
        store.request_pin("d1", "bob", now=100.0)
        store.request_pin("d1", "carol", now=200.0)
        result = store.requests_for_doc("d1")
        assert [r.requested_by for r in result] == ["bob", "carol", "alice"]

    def test_status_filter(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        store.request_pin("d1", "bob")
        store.approve(r1.request_id, "carol")
        approved = store.requests_for_doc("d1", status="approved")
        pending = store.requests_for_doc("d1", status="pending")
        assert len(approved) == 1
        assert len(pending) == 1

    def test_status_filter_no_match(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice")
        assert store.requests_for_doc("d1", status="approved") == []


# --------------------------------------------------------------------- requests_by_user


class TestRequestsByUser:
    def test_empty(self):
        store = DocPinRequest()
        assert store.requests_by_user("alice") == []

    def test_filter_by_user(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice")
        store.request_pin("d2", "alice")
        store.request_pin("d3", "bob")
        assert len(store.requests_by_user("alice")) == 2
        assert len(store.requests_by_user("bob")) == 1

    def test_sorted_by_created_at(self):
        store = DocPinRequest()
        store.request_pin("d3", "alice", now=300.0)
        store.request_pin("d1", "alice", now=100.0)
        store.request_pin("d2", "alice", now=200.0)
        result = store.requests_by_user("alice")
        assert [r.doc_id for r in result] == ["d1", "d2", "d3"]

    def test_status_filter(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        store.request_pin("d2", "alice")
        store.reject(r1.request_id, "bob")
        rejected = store.requests_by_user("alice", status="rejected")
        pending = store.requests_by_user("alice", status="pending")
        assert len(rejected) == 1
        assert len(pending) == 1


# --------------------------------------------------------------------- pending_requests


class TestPendingRequests:
    def test_empty(self):
        store = DocPinRequest()
        assert store.pending_requests() == []

    def test_only_pending(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        store.request_pin("d2", "alice")
        store.approve(r1.request_id, "bob")
        pending = store.pending_requests()
        assert len(pending) == 1
        assert pending[0].doc_id == "d2"

    def test_sorted_by_created_at(self):
        store = DocPinRequest()
        store.request_pin("d3", "alice", now=300.0)
        store.request_pin("d1", "alice", now=100.0)
        store.request_pin("d2", "alice", now=200.0)
        result = store.pending_requests()
        assert [r.doc_id for r in result] == ["d1", "d2", "d3"]

    def test_excludes_rejected_and_expired(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice", now=0.0)
        r2 = store.request_pin("d2", "alice", now=0.0)
        store.request_pin("d3", "alice", now=1000.0)
        store.reject(r1.request_id, "bob")
        store.expire_old(10.0, now=100.0)  # expires r2
        result = store.pending_requests()
        assert len(result) == 1
        assert result[0].doc_id == "d3"


# --------------------------------------------------------------------- cancel


class TestCancel:
    def test_cancel_pending(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.cancel(r.request_id) is True
        assert store.get(r.request_id).status == "rejected"

    def test_cancel_unknown(self):
        store = DocPinRequest()
        assert store.cancel("missing") is False

    def test_cancel_approved_fails(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.approve(r.request_id, "bob")
        assert store.cancel(r.request_id) is False

    def test_cancel_rejected_fails(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.reject(r.request_id, "bob")
        assert store.cancel(r.request_id) is False

    def test_cancel_no_decided_by(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.cancel(r.request_id)
        got = store.get(r.request_id)
        assert got.decided_by == ""


# --------------------------------------------------------------------- delete


class TestDelete:
    def test_delete_existing(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        assert store.delete(r.request_id) is True
        assert store.get(r.request_id) is None

    def test_delete_missing(self):
        store = DocPinRequest()
        assert store.delete("missing") is False

    def test_delete_decreases_total(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.request_pin("d2", "bob")
        assert store.stats().total == 2
        store.delete(r.request_id)
        assert store.stats().total == 1

    def test_delete_approved(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.approve(r.request_id, "bob")
        assert store.delete(r.request_id) is True


# --------------------------------------------------------------------- stats


class TestStats:
    def test_empty(self):
        store = DocPinRequest()
        s = store.stats()
        assert s.total == 0
        assert s.pending == 0
        assert s.approved == 0
        assert s.rejected == 0
        assert s.expired == 0

    def test_counts_pending(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice")
        store.request_pin("d2", "bob")
        s = store.stats()
        assert s.total == 2
        assert s.pending == 2

    def test_counts_approved(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        r2 = store.request_pin("d2", "alice")
        store.approve(r1.request_id, "bob")
        store.approve(r2.request_id, "bob")
        s = store.stats()
        assert s.approved == 2
        assert s.pending == 0

    def test_counts_rejected(self):
        store = DocPinRequest()
        r = store.request_pin("d1", "alice")
        store.reject(r.request_id, "bob")
        s = store.stats()
        assert s.rejected == 1

    def test_counts_expired(self):
        store = DocPinRequest()
        store.request_pin("d1", "alice", now=0.0)
        store.expire_old(10.0, now=100.0)
        s = store.stats()
        assert s.expired == 1

    def test_mixed(self):
        store = DocPinRequest()
        r1 = store.request_pin("d1", "alice")
        r2 = store.request_pin("d2", "alice")
        r3 = store.request_pin("d3", "alice", now=0.0)
        store.request_pin("d4", "alice")
        store.approve(r1.request_id, "bob")
        store.reject(r2.request_id, "bob")
        store.expire_old(10.0, now=100.0)  # expires r3 (and d4 if it has now=time.time())
        s = store.stats()
        assert s.total == 4
        assert s.approved == 1
        assert s.rejected == 1
        # r3 was created at 0.0 and is now > 10s old, so expired
        assert s.expired >= 1


# --------------------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_request_pin(self):
        store = DocPinRequest()
        n_threads = 10
        n_per_thread = 20

        def worker():
            for i in range(n_per_thread):
                store.request_pin("d1", "alice")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert store.stats().total == n_threads * n_per_thread

    def test_concurrent_unique_ids(self):
        store = DocPinRequest()
        ids: list[str] = []
        lock = threading.Lock()

        def worker():
            local = []
            for _ in range(50):
                r = store.request_pin("d1", "alice")
                local.append(r.request_id)
            with lock:
                ids.extend(local)

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(ids) == len(set(ids))

    def test_concurrent_mixed_ops(self):
        store = DocPinRequest()
        requests = [store.request_pin("d1", "alice") for _ in range(50)]

        def approver(reqs):
            for r in reqs:
                store.approve(r.request_id, "bob")

        def rejecter(reqs):
            for r in reqs:
                store.reject(r.request_id, "bob")

        t1 = threading.Thread(target=approver, args=(requests[:25],))
        t2 = threading.Thread(target=rejecter, args=(requests[25:],))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        s = store.stats()
        assert s.total == 50
        assert s.approved + s.rejected == 50
