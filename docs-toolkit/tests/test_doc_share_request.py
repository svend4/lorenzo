"""Tests for E406 DocShareRequest."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_share_request import (
    DocShareRequest,
    ShareRequest,
    ShareRequestStats,
)


# --------------------------------------------------------------------- fixtures

@pytest.fixture
def store() -> DocShareRequest:
    return DocShareRequest()


# --------------------------------------------------------------------- creation

class TestRequestShare:
    def test_returns_share_request(self, store: DocShareRequest) -> None:
        r = store.request_share("doc1", "alice", "bob", ["read"])
        assert isinstance(r, ShareRequest)

    def test_has_uuid_id(self, store: DocShareRequest) -> None:
        r = store.request_share("doc1", "alice", "bob", ["read"])
        assert isinstance(r.request_id, str)
        assert len(r.request_id) == 32

    def test_unique_ids(self, store: DocShareRequest) -> None:
        ids = {
            store.request_share("d", "a", "b", []).request_id for _ in range(20)
        }
        assert len(ids) == 20

    def test_initial_status_pending(self, store: DocShareRequest) -> None:
        r = store.request_share("doc1", "alice", "bob", ["read"])
        assert r.status == "pending"

    def test_stores_fields(self, store: DocShareRequest) -> None:
        r = store.request_share(
            "doc1", "alice", "bob", ["read", "write"], reason="need access"
        )
        assert r.doc_id == "doc1"
        assert r.requester == "alice"
        assert r.target == "bob"
        assert r.permissions == ["read", "write"]
        assert r.reason == "need access"

    def test_permissions_copied(self, store: DocShareRequest) -> None:
        perms = ["read"]
        r = store.request_share("d", "a", "b", perms)
        perms.append("write")
        assert r.permissions == ["read"]

    def test_custom_now(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=1234.5)
        assert r.created_at == 1234.5

    def test_default_now_uses_time(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert r.created_at > 0

    def test_default_reason_empty(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert r.reason == ""

    def test_decided_by_initially_empty(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert r.decided_by == ""

    def test_decided_at_initially_none(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert r.decided_at is None

    def test_stored_in_state(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.get(r.request_id) is r


# --------------------------------------------------------------------- approve

class TestApprove:
    def test_approve_pending(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.approve(r.request_id, "admin") is True

    def test_status_becomes_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.get(r.request_id).status == "approved"

    def test_decided_by_set(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin", note="ok", now=42.0)
        got = store.get(r.request_id)
        assert got.decided_by == "admin"
        assert got.decision_note == "ok"
        assert got.decided_at == 42.0

    def test_approve_missing(self, store: DocShareRequest) -> None:
        assert store.approve("nope", "admin") is False

    def test_approve_already_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.approve(r.request_id, "admin2") is False

    def test_approve_rejected_request(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.reject(r.request_id, "admin")
        assert store.approve(r.request_id, "admin") is False

    def test_approve_cancelled_request(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.cancel(r.request_id)
        assert store.approve(r.request_id, "admin") is False

    def test_approve_expired_request(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=0.0)
        store.expire_old(1.0, now=100.0)
        assert store.approve(r.request_id, "admin") is False

    def test_approve_default_now(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.get(r.request_id).decided_at is not None


# --------------------------------------------------------------------- reject

class TestReject:
    def test_reject_pending(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.reject(r.request_id, "admin") is True

    def test_status_becomes_rejected(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.reject(r.request_id, "admin")
        assert store.get(r.request_id).status == "rejected"

    def test_reject_fields_set(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.reject(r.request_id, "admin", note="no", now=7.0)
        got = store.get(r.request_id)
        assert got.decided_by == "admin"
        assert got.decision_note == "no"
        assert got.decided_at == 7.0

    def test_reject_missing(self, store: DocShareRequest) -> None:
        assert store.reject("nope", "admin") is False

    def test_reject_already_rejected(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.reject(r.request_id, "admin")
        assert store.reject(r.request_id, "admin2") is False

    def test_reject_already_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.reject(r.request_id, "admin") is False

    def test_reject_cancelled(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.cancel(r.request_id)
        assert store.reject(r.request_id, "admin") is False


# --------------------------------------------------------------------- cancel

class TestCancel:
    def test_cancel_pending(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.cancel(r.request_id) is True

    def test_status_becomes_cancelled(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.cancel(r.request_id)
        assert store.get(r.request_id).status == "cancelled"

    def test_cancel_missing(self, store: DocShareRequest) -> None:
        assert store.cancel("nope") is False

    def test_cancel_already_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.cancel(r.request_id) is False

    def test_cancel_already_rejected(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.reject(r.request_id, "admin")
        assert store.cancel(r.request_id) is False

    def test_cancel_already_cancelled(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.cancel(r.request_id)
        assert store.cancel(r.request_id) is False


# --------------------------------------------------------------------- expire_old

class TestExpireOld:
    def test_expires_old_pending(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=0.0)
        count = store.expire_old(10.0, now=100.0)
        assert count == 1
        assert store.get(r.request_id).status == "expired"

    def test_does_not_expire_recent(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=95.0)
        count = store.expire_old(10.0, now=100.0)
        assert count == 0
        assert store.get(r.request_id).status == "pending"

    def test_does_not_expire_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=0.0)
        store.approve(r.request_id, "admin")
        count = store.expire_old(1.0, now=100.0)
        assert count == 0
        assert store.get(r.request_id).status == "approved"

    def test_does_not_expire_rejected(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=0.0)
        store.reject(r.request_id, "admin")
        count = store.expire_old(1.0, now=100.0)
        assert count == 0

    def test_does_not_expire_cancelled(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [], now=0.0)
        store.cancel(r.request_id)
        count = store.expire_old(1.0, now=100.0)
        assert count == 0

    def test_expires_multiple(self, store: DocShareRequest) -> None:
        for i in range(5):
            store.request_share(f"d{i}", "a", "b", [], now=0.0)
        count = store.expire_old(1.0, now=100.0)
        assert count == 5

    def test_exact_threshold_not_expired(self, store: DocShareRequest) -> None:
        store.request_share("d", "a", "b", [], now=0.0)
        count = store.expire_old(10.0, now=10.0)
        assert count == 0

    def test_default_now(self, store: DocShareRequest) -> None:
        store.request_share("d", "a", "b", [], now=0.0)
        count = store.expire_old(1.0)
        assert count == 1


# --------------------------------------------------------------------- get

class TestGet:
    def test_get_existing(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.get(r.request_id) is r

    def test_get_missing(self, store: DocShareRequest) -> None:
        assert store.get("nope") is None


# --------------------------------------------------------------------- queries

class TestRequestsForDoc:
    def test_returns_matching(self, store: DocShareRequest) -> None:
        store.request_share("doc1", "a", "b", [])
        store.request_share("doc2", "a", "b", [])
        store.request_share("doc1", "c", "d", [])
        assert len(store.requests_for_doc("doc1")) == 2

    def test_sorted_by_created_at(self, store: DocShareRequest) -> None:
        store.request_share("doc1", "a", "b", [], now=3.0)
        store.request_share("doc1", "a", "b", [], now=1.0)
        store.request_share("doc1", "a", "b", [], now=2.0)
        rs = store.requests_for_doc("doc1")
        assert [r.created_at for r in rs] == [1.0, 2.0, 3.0]

    def test_filter_by_status(self, store: DocShareRequest) -> None:
        r1 = store.request_share("doc1", "a", "b", [])
        store.request_share("doc1", "a", "b", [])
        store.approve(r1.request_id, "admin")
        approved = store.requests_for_doc("doc1", status="approved")
        assert len(approved) == 1

    def test_empty(self, store: DocShareRequest) -> None:
        assert store.requests_for_doc("doc1") == []

    def test_no_match(self, store: DocShareRequest) -> None:
        store.request_share("doc1", "a", "b", [])
        assert store.requests_for_doc("other") == []


class TestRequestsByRequester:
    def test_returns_matching(self, store: DocShareRequest) -> None:
        store.request_share("d", "alice", "b", [])
        store.request_share("d", "alice", "c", [])
        store.request_share("d", "bob", "c", [])
        assert len(store.requests_by_requester("alice")) == 2

    def test_sorted_by_created_at(self, store: DocShareRequest) -> None:
        store.request_share("d", "alice", "b", [], now=2.0)
        store.request_share("d", "alice", "b", [], now=1.0)
        rs = store.requests_by_requester("alice")
        assert [r.created_at for r in rs] == [1.0, 2.0]

    def test_filter_by_status(self, store: DocShareRequest) -> None:
        r1 = store.request_share("d", "alice", "b", [])
        store.request_share("d", "alice", "b", [])
        store.reject(r1.request_id, "admin")
        rejected = store.requests_by_requester("alice", status="rejected")
        assert len(rejected) == 1

    def test_no_match(self, store: DocShareRequest) -> None:
        assert store.requests_by_requester("nobody") == []


class TestRequestsForTarget:
    def test_returns_matching(self, store: DocShareRequest) -> None:
        store.request_share("d", "a", "bob", [])
        store.request_share("d", "c", "bob", [])
        store.request_share("d", "a", "alice", [])
        assert len(store.requests_for_target("bob")) == 2

    def test_sorted_by_created_at(self, store: DocShareRequest) -> None:
        store.request_share("d", "a", "bob", [], now=5.0)
        store.request_share("d", "a", "bob", [], now=1.0)
        rs = store.requests_for_target("bob")
        assert [r.created_at for r in rs] == [1.0, 5.0]

    def test_filter_by_status(self, store: DocShareRequest) -> None:
        r1 = store.request_share("d", "a", "bob", [])
        store.request_share("d", "a", "bob", [])
        store.approve(r1.request_id, "admin")
        pending = store.requests_for_target("bob", status="pending")
        assert len(pending) == 1

    def test_no_match(self, store: DocShareRequest) -> None:
        assert store.requests_for_target("nobody") == []


class TestPendingRequests:
    def test_returns_pending_only(self, store: DocShareRequest) -> None:
        r1 = store.request_share("d", "a", "b", [])
        r2 = store.request_share("d", "a", "b", [])
        store.request_share("d", "a", "b", [])
        store.approve(r1.request_id, "admin")
        store.reject(r2.request_id, "admin")
        assert len(store.pending_requests()) == 1

    def test_sorted_by_created_at(self, store: DocShareRequest) -> None:
        store.request_share("d", "a", "b", [], now=3.0)
        store.request_share("d", "a", "b", [], now=1.0)
        store.request_share("d", "a", "b", [], now=2.0)
        rs = store.pending_requests()
        assert [r.created_at for r in rs] == [1.0, 2.0, 3.0]

    def test_empty(self, store: DocShareRequest) -> None:
        assert store.pending_requests() == []


# --------------------------------------------------------------------- delete

class TestDelete:
    def test_delete_existing(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        assert store.delete(r.request_id) is True
        assert store.get(r.request_id) is None

    def test_delete_missing(self, store: DocShareRequest) -> None:
        assert store.delete("nope") is False

    def test_delete_approved(self, store: DocShareRequest) -> None:
        r = store.request_share("d", "a", "b", [])
        store.approve(r.request_id, "admin")
        assert store.delete(r.request_id) is True


# --------------------------------------------------------------------- stats

class TestStats:
    def test_empty(self, store: DocShareRequest) -> None:
        s = store.stats()
        assert s == ShareRequestStats(0, 0, 0, 0, 0, 0)

    def test_all_states(self, store: DocShareRequest) -> None:
        r1 = store.request_share("d", "a", "b", [])
        r2 = store.request_share("d", "a", "b", [])
        r3 = store.request_share("d", "a", "b", [])
        r4 = store.request_share("d", "a", "b", [], now=0.0)
        store.request_share("d", "a", "b", [])
        store.approve(r1.request_id, "admin")
        store.reject(r2.request_id, "admin")
        store.cancel(r3.request_id)
        store.expire_old(1.0, now=100.0)
        s = store.stats()
        assert s.total == 5
        assert s.approved == 1
        assert s.rejected == 1
        assert s.cancelled == 1
        assert s.expired == 1
        assert s.pending == 1

    def test_total_counts(self, store: DocShareRequest) -> None:
        for _ in range(7):
            store.request_share("d", "a", "b", [])
        assert store.stats().total == 7


# --------------------------------------------------------------------- thread safety

class TestThreadSafety:
    def test_concurrent_create(self) -> None:
        store = DocShareRequest()

        def worker() -> None:
            for _ in range(50):
                store.request_share("d", "a", "b", ["read"])

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.stats().total == 8 * 50

    def test_concurrent_approve_only_one_wins(self) -> None:
        store = DocShareRequest()
        r = store.request_share("d", "a", "b", [])
        results: list[bool] = []
        lock = threading.Lock()

        def worker() -> None:
            ok = store.approve(r.request_id, "admin")
            with lock:
                results.append(ok)

        threads = [threading.Thread(target=worker) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert sum(1 for x in results if x) == 1

    def test_concurrent_mixed_operations(self) -> None:
        store = DocShareRequest()
        ids: list[str] = []
        for _ in range(20):
            ids.append(store.request_share("d", "a", "b", []).request_id)

        def approver() -> None:
            for rid in ids:
                store.approve(rid, "admin")

        def reader() -> None:
            for _ in range(50):
                store.pending_requests()
                store.stats()

        threads = [
            threading.Thread(target=approver),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.stats().approved == 20

    def test_concurrent_delete(self) -> None:
        store = DocShareRequest()
        ids = [
            store.request_share("d", "a", "b", []).request_id
            for _ in range(100)
        ]

        def worker(subset: list[str]) -> None:
            for rid in subset:
                store.delete(rid)

        half = len(ids) // 2
        t1 = threading.Thread(target=worker, args=(ids[:half],))
        t2 = threading.Thread(target=worker, args=(ids[half:],))
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        assert store.stats().total == 0
