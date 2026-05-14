"""Tests for E349 DocSigningRequest."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_signing_request import (
    DocSigningRequest,
    Signer,
    SigningRequest,
    SigningStats,
)


# --------------------------------------------------------------------- dataclasses


class TestSigningRequestDataclass:
    def test_construct_minimal(self):
        r = SigningRequest(request_id="r1", doc_id="d1", requested_by="alice")
        assert r.request_id == "r1"
        assert r.doc_id == "d1"
        assert r.requested_by == "alice"

    def test_defaults(self):
        r = SigningRequest(request_id="r1", doc_id="d1", requested_by="alice")
        assert r.created_at == 0.0
        assert r.expires_at is None
        assert r.status == "pending"
        assert r.message == ""

    def test_custom_fields(self):
        r = SigningRequest(
            request_id="r1",
            doc_id="d1",
            requested_by="alice",
            created_at=100.0,
            expires_at=200.0,
            status="in_progress",
            message="please sign",
        )
        assert r.created_at == 100.0
        assert r.expires_at == 200.0
        assert r.status == "in_progress"
        assert r.message == "please sign"


class TestSignerDataclass:
    def test_construct_minimal(self):
        s = Signer(signer_id="s1", request_id="r1", name="bob")
        assert s.signer_id == "s1"
        assert s.request_id == "r1"
        assert s.name == "bob"

    def test_defaults(self):
        s = Signer(signer_id="s1", request_id="r1", name="bob")
        assert s.email == ""
        assert s.order == 0
        assert s.signed_at is None
        assert s.declined is False

    def test_custom_fields(self):
        s = Signer(
            signer_id="s1",
            request_id="r1",
            name="bob",
            email="bob@x.com",
            order=2,
            signed_at=123.0,
            declined=True,
        )
        assert s.email == "bob@x.com"
        assert s.order == 2
        assert s.signed_at == 123.0
        assert s.declined is True


class TestSigningStatsDataclass:
    def test_construct(self):
        st = SigningStats(
            total_requests=1,
            pending=2,
            in_progress=3,
            completed=4,
            expired=5,
            cancelled=6,
            total_signers=7,
            total_signed=8,
        )
        assert st.total_requests == 1
        assert st.pending == 2
        assert st.in_progress == 3
        assert st.completed == 4
        assert st.expired == 5
        assert st.cancelled == 6
        assert st.total_signers == 7
        assert st.total_signed == 8


# --------------------------------------------------------------------- construction


class TestConstruction:
    def test_empty_store(self):
        d = DocSigningRequest()
        st = d.stats()
        assert st.total_requests == 0
        assert st.total_signers == 0

    def test_independent_instances(self):
        d1 = DocSigningRequest()
        d2 = DocSigningRequest()
        d1.create_request("doc1", "alice")
        assert d2.stats().total_requests == 0


# --------------------------------------------------------------------- create


class TestCreateRequest:
    def test_returns_request(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert isinstance(r, SigningRequest)
        assert r.doc_id == "doc1"
        assert r.requested_by == "alice"

    def test_uuid_request_id(self):
        d = DocSigningRequest()
        r1 = d.create_request("doc1", "alice")
        r2 = d.create_request("doc1", "alice")
        assert r1.request_id != r2.request_id
        assert len(r1.request_id) > 0

    def test_default_status_pending(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert r.status == "pending"

    def test_created_at_is_set(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", now=42.0)
        assert r.created_at == 42.0

    def test_created_at_auto_when_none(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert r.created_at > 0

    def test_signers_created_with_order(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1",
            "alice",
            signers=[("bob", "b@x"), ("carol", "c@x"), ("dave", "d@x")],
        )
        signers = d.signers_of(r.request_id)
        assert [s.name for s in signers] == ["bob", "carol", "dave"]
        assert [s.order for s in signers] == [0, 1, 2]

    def test_signers_email(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("bob", "b@x"), ("carol", "c@x")]
        )
        signers = d.signers_of(r.request_id)
        assert signers[0].email == "b@x"
        assert signers[1].email == "c@x"

    def test_empty_signers_list(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert d.signers_of(r.request_id) == []

    def test_signer_uuids_unique(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("a", ""), ("b", "")])
        signers = d.signers_of(r.request_id)
        assert signers[0].signer_id != signers[1].signer_id

    def test_message_stored(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", message="hi please")
        assert r.message == "hi please"

    def test_expires_at_stored(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", expires_at=999.0)
        assert r.expires_at == 999.0


# --------------------------------------------------------------------- add_signer


class TestAddSigner:
    def test_appends_signer(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.add_signer(r.request_id, "carol", "c@x")
        assert s is not None
        assert s.name == "carol"
        assert s.email == "c@x"

    def test_next_order(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("a", ""), ("b", "")])
        s = d.add_signer(r.request_id, "c")
        assert s.order == 2

    def test_first_order_when_empty(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        s = d.add_signer(r.request_id, "first")
        assert s.order == 0

    def test_returns_none_for_missing(self):
        d = DocSigningRequest()
        assert d.add_signer("nonexistent", "bob") is None

    def test_appears_in_signers_of(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        d.add_signer(r.request_id, "bob")
        assert len(d.signers_of(r.request_id)) == 1


# --------------------------------------------------------------------- sign


class TestSign:
    def test_returns_true(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        signer = d.signers_of(r.request_id)[0]
        assert d.sign(signer.signer_id) is True

    def test_sets_signed_at(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        signer = d.signers_of(r.request_id)[0]
        d.sign(signer.signer_id, now=123.0)
        s = d.get_signer(signer.signer_id)
        assert s.signed_at == 123.0

    def test_returns_false_for_missing(self):
        d = DocSigningRequest()
        assert d.sign("nonexistent") is False

    def test_returns_false_when_already_signed(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        signer = d.signers_of(r.request_id)[0]
        d.sign(signer.signer_id)
        assert d.sign(signer.signer_id) is False

    def test_completes_request_when_all_signed(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("bob", ""), ("carol", "")]
        )
        signers = d.signers_of(r.request_id)
        d.sign(signers[0].signer_id)
        assert d.get_request(r.request_id).status == "in_progress"
        d.sign(signers[1].signer_id)
        assert d.get_request(r.request_id).status == "completed"

    def test_not_completed_with_pending_others(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("a", ""), ("b", ""), ("c", "")]
        )
        signers = d.signers_of(r.request_id)
        d.sign(signers[0].signer_id)
        assert d.get_request(r.request_id).status != "completed"


# --------------------------------------------------------------------- decline


class TestDecline:
    def test_returns_true(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.signers_of(r.request_id)[0]
        assert d.decline(s.signer_id) is True

    def test_sets_declined_flag(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.signers_of(r.request_id)[0]
        d.decline(s.signer_id)
        assert d.get_signer(s.signer_id).declined is True

    def test_returns_false_for_missing(self):
        d = DocSigningRequest()
        assert d.decline("nope") is False

    def test_returns_false_when_already_declined(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.signers_of(r.request_id)[0]
        d.decline(s.signer_id)
        assert d.decline(s.signer_id) is False


# --------------------------------------------------------------------- cancel


class TestCancel:
    def test_returns_true(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert d.cancel(r.request_id) is True

    def test_status_cancelled(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        d.cancel(r.request_id)
        assert d.get_request(r.request_id).status == "cancelled"

    def test_returns_false_for_missing(self):
        d = DocSigningRequest()
        assert d.cancel("nope") is False

    def test_noop_for_completed(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.signers_of(r.request_id)[0]
        d.sign(s.signer_id)
        assert d.get_request(r.request_id).status == "completed"
        assert d.cancel(r.request_id) is False
        assert d.get_request(r.request_id).status == "completed"

    def test_noop_for_already_cancelled(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        d.cancel(r.request_id)
        assert d.cancel(r.request_id) is False


# --------------------------------------------------------------------- expire


class TestExpireIfDue:
    def test_expires_one(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", expires_at=10.0, now=1.0)
        n = d.expire_if_due(now=20.0)
        assert n == 1
        assert d.get_request(r.request_id).status == "expired"

    def test_not_expired_yet(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", expires_at=100.0, now=1.0)
        n = d.expire_if_due(now=50.0)
        assert n == 0
        assert d.get_request(r.request_id).status == "pending"

    def test_no_expiry_set(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        n = d.expire_if_due(now=1e18)
        assert n == 0
        assert d.get_request(r.request_id).status == "pending"

    def test_ignores_terminal(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", expires_at=10.0, now=1.0)
        d.cancel(r.request_id)
        n = d.expire_if_due(now=100.0)
        assert n == 0
        assert d.get_request(r.request_id).status == "cancelled"

    def test_count_multiple(self):
        d = DocSigningRequest()
        d.create_request("doc1", "alice", expires_at=10.0, now=1.0)
        d.create_request("doc2", "alice", expires_at=20.0, now=1.0)
        d.create_request("doc3", "alice", expires_at=1000.0, now=1.0)
        n = d.expire_if_due(now=100.0)
        assert n == 2


# --------------------------------------------------------------------- get_request


class TestGetRequest:
    def test_found(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert d.get_request(r.request_id) is r or d.get_request(
            r.request_id
        ).request_id == r.request_id

    def test_not_found(self):
        d = DocSigningRequest()
        assert d.get_request("nope") is None


# --------------------------------------------------------------------- get_signer


class TestGetSigner:
    def test_found(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("bob", "")])
        s = d.signers_of(r.request_id)[0]
        assert d.get_signer(s.signer_id).name == "bob"

    def test_not_found(self):
        d = DocSigningRequest()
        assert d.get_signer("nope") is None


# --------------------------------------------------------------------- signers_of


class TestSignersOf:
    def test_sorted_by_order(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("a", ""), ("b", ""), ("c", "")]
        )
        signers = d.signers_of(r.request_id)
        assert [s.order for s in signers] == [0, 1, 2]

    def test_empty_for_no_signers(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice")
        assert d.signers_of(r.request_id) == []

    def test_empty_for_missing_request(self):
        d = DocSigningRequest()
        assert d.signers_of("nope") == []


# --------------------------------------------------------------------- pending


class TestPendingSigners:
    def test_excludes_signed(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("a", ""), ("b", "")])
        signers = d.signers_of(r.request_id)
        d.sign(signers[0].signer_id)
        pending = d.pending_signers(r.request_id)
        assert len(pending) == 1
        assert pending[0].name == "b"

    def test_excludes_declined(self):
        d = DocSigningRequest()
        r = d.create_request("doc1", "alice", signers=[("a", ""), ("b", "")])
        signers = d.signers_of(r.request_id)
        d.decline(signers[0].signer_id)
        pending = d.pending_signers(r.request_id)
        assert len(pending) == 1
        assert pending[0].name == "b"

    def test_sorted_by_order(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("a", ""), ("b", ""), ("c", "")]
        )
        pending = d.pending_signers(r.request_id)
        assert [s.order for s in pending] == [0, 1, 2]


# --------------------------------------------------------------------- requests_for_doc


class TestRequestsForDoc:
    def test_filter_by_doc(self):
        d = DocSigningRequest()
        d.create_request("doc1", "alice", now=1.0)
        d.create_request("doc2", "alice", now=2.0)
        d.create_request("doc1", "bob", now=3.0)
        rs = d.requests_for_doc("doc1")
        assert len(rs) == 2
        assert all(r.doc_id == "doc1" for r in rs)

    def test_sorted_by_created_at(self):
        d = DocSigningRequest()
        d.create_request("doc1", "alice", now=5.0)
        d.create_request("doc1", "alice", now=1.0)
        d.create_request("doc1", "alice", now=3.0)
        rs = d.requests_for_doc("doc1")
        assert [r.created_at for r in rs] == [1.0, 3.0, 5.0]

    def test_empty_when_no_match(self):
        d = DocSigningRequest()
        assert d.requests_for_doc("nope") == []


# --------------------------------------------------------------------- requests_by_status


class TestRequestsByStatus:
    def test_filter_pending(self):
        d = DocSigningRequest()
        r1 = d.create_request("doc1", "alice", now=1.0)
        r2 = d.create_request("doc2", "alice", now=2.0)
        d.cancel(r1.request_id)
        rs = d.requests_by_status("pending")
        assert len(rs) == 1
        assert rs[0].request_id == r2.request_id

    def test_filter_cancelled(self):
        d = DocSigningRequest()
        r1 = d.create_request("doc1", "alice", now=1.0)
        d.create_request("doc2", "alice", now=2.0)
        d.cancel(r1.request_id)
        rs = d.requests_by_status("cancelled")
        assert len(rs) == 1
        assert rs[0].request_id == r1.request_id

    def test_sorted_by_created_at(self):
        d = DocSigningRequest()
        d.create_request("doc1", "alice", now=3.0)
        d.create_request("doc2", "alice", now=1.0)
        d.create_request("doc3", "alice", now=2.0)
        rs = d.requests_by_status("pending")
        assert [r.created_at for r in rs] == [1.0, 2.0, 3.0]


# --------------------------------------------------------------------- stats


class TestStats:
    def test_empty(self):
        d = DocSigningRequest()
        st = d.stats()
        assert st.total_requests == 0
        assert st.pending == 0
        assert st.total_signers == 0
        assert st.total_signed == 0

    def test_counts_requests(self):
        d = DocSigningRequest()
        d.create_request("doc1", "alice")
        d.create_request("doc2", "alice")
        st = d.stats()
        assert st.total_requests == 2
        assert st.pending == 2

    def test_counts_signers_and_signed(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1", "alice", signers=[("a", ""), ("b", ""), ("c", "")]
        )
        signers = d.signers_of(r.request_id)
        d.sign(signers[0].signer_id)
        d.sign(signers[1].signer_id)
        st = d.stats()
        assert st.total_signers == 3
        assert st.total_signed == 2

    def test_counts_each_status(self):
        d = DocSigningRequest()
        r1 = d.create_request("doc1", "alice", expires_at=10.0, now=1.0)
        r2 = d.create_request("doc2", "alice", signers=[("a", "")])
        r3 = d.create_request("doc3", "alice")
        r4 = d.create_request("doc4", "alice", signers=[("b", "")])
        # r1 -> expired
        d.expire_if_due(now=100.0)
        # r2 -> completed
        sig = d.signers_of(r2.request_id)[0]
        d.sign(sig.signer_id)
        # r3 -> cancelled
        d.cancel(r3.request_id)
        # r4 -> in_progress (decline triggers)
        sig4 = d.signers_of(r4.request_id)[0]
        d.decline(sig4.signer_id)
        st = d.stats()
        assert st.expired == 1
        assert st.completed == 1
        assert st.cancelled == 1
        assert st.in_progress == 1


# --------------------------------------------------------------------- thread safety


class TestThreadSafety:
    def test_concurrent_create_request(self):
        d = DocSigningRequest()
        n_threads = 16
        per_thread = 20

        def worker():
            for _ in range(per_thread):
                d.create_request("doc1", "alice", signers=[("a", "")])

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = d.stats()
        assert st.total_requests == n_threads * per_thread
        assert st.total_signers == n_threads * per_thread

    def test_concurrent_sign(self):
        d = DocSigningRequest()
        r = d.create_request(
            "doc1",
            "alice",
            signers=[(f"name{i}", "") for i in range(50)],
        )
        signers = d.signers_of(r.request_id)

        def worker(sid: str):
            d.sign(sid)

        threads = [threading.Thread(target=worker, args=(s.signer_id,)) for s in signers]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert d.get_request(r.request_id).status == "completed"
        st = d.stats()
        assert st.total_signed == 50
