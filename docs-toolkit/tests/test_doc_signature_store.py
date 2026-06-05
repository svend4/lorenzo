"""Tests for E330 DocSignatureStore."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_signature_store import (
    DocSignatureStore,
    Signature,
    SignatureStats,
)


# ---------------------------------------------------------------------------
# TestSignatureDataclass
# ---------------------------------------------------------------------------


class TestSignatureDataclass:
    def test_fields_stored(self):
        s = Signature(
            signature_id="sid",
            doc_id="d1",
            signer="alice",
            signature_value="abc",
        )
        assert s.signature_id == "sid"
        assert s.doc_id == "d1"
        assert s.signer == "alice"
        assert s.signature_value == "abc"

    def test_default_algorithm(self):
        s = Signature("sid", "d1", "alice", "abc")
        assert s.algorithm == "sha256"

    def test_custom_algorithm(self):
        s = Signature("sid", "d1", "alice", "abc", algorithm="ed25519")
        assert s.algorithm == "ed25519"

    def test_default_signed_at(self):
        s = Signature("sid", "d1", "alice", "abc")
        assert s.signed_at == 0.0

    def test_default_revoked_false(self):
        s = Signature("sid", "d1", "alice", "abc")
        assert s.revoked is False

    def test_default_metadata_empty_dict(self):
        s = Signature("sid", "d1", "alice", "abc")
        assert s.metadata == {}

    def test_metadata_independent_between_instances(self):
        a = Signature("a", "d", "x", "v")
        b = Signature("b", "d", "x", "v")
        a.metadata["k"] = 1
        assert b.metadata == {}


# ---------------------------------------------------------------------------
# TestSignatureStatsDataclass
# ---------------------------------------------------------------------------


class TestSignatureStatsDataclass:
    def test_fields_stored(self):
        s = SignatureStats(
            total_signatures=10,
            revoked_count=2,
            unique_docs=3,
            unique_signers=4,
        )
        assert s.total_signatures == 10
        assert s.revoked_count == 2
        assert s.unique_docs == 3
        assert s.unique_signers == 4

    def test_zero_values(self):
        s = SignatureStats(0, 0, 0, 0)
        assert s.total_signatures == 0
        assert s.revoked_count == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_construct(self):
        store = DocSignatureStore()
        assert store is not None

    def test_initial_empty(self):
        store = DocSignatureStore()
        assert store.all_doc_ids() == []

    def test_initial_stats_zero(self):
        store = DocSignatureStore()
        s = store.stats()
        assert s.total_signatures == 0
        assert s.revoked_count == 0
        assert s.unique_docs == 0
        assert s.unique_signers == 0


# ---------------------------------------------------------------------------
# TestSign
# ---------------------------------------------------------------------------


class TestSign:
    def test_returns_signature(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "value")
        assert isinstance(sig, Signature)

    def test_signature_id_is_uuid_hex(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "value")
        assert isinstance(sig.signature_id, str)
        assert len(sig.signature_id) == 32  # uuid4 hex

    def test_signature_ids_unique(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc1", "alice", "v")
        assert s1.signature_id != s2.signature_id

    def test_doc_id_stored(self):
        store = DocSignatureStore()
        sig = store.sign("docX", "alice", "v")
        assert sig.doc_id == "docX"

    def test_signer_stored(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "bob", "v")
        assert sig.signer == "bob"

    def test_signature_value_stored(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "deadbeef")
        assert sig.signature_value == "deadbeef"

    def test_default_algorithm(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert sig.algorithm == "sha256"

    def test_custom_algorithm(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v", algorithm="rsa-pss")
        assert sig.algorithm == "rsa-pss"

    def test_timestamp_set_to_now_by_default(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert sig.signed_at > 0.0

    def test_timestamp_explicit(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v", now=123.456)
        assert sig.signed_at == 123.456

    def test_metadata_default_empty(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert sig.metadata == {}

    def test_metadata_passed(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v", metadata={"role": "approver"})
        assert sig.metadata == {"role": "approver"}

    def test_metadata_is_copied(self):
        store = DocSignatureStore()
        md = {"k": 1}
        sig = store.sign("doc1", "alice", "v", metadata=md)
        md["k"] = 999
        assert sig.metadata["k"] == 1

    def test_not_revoked_by_default(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert sig.revoked is False


# ---------------------------------------------------------------------------
# TestRevoke
# ---------------------------------------------------------------------------


class TestRevoke:
    def test_returns_true_when_found(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert store.revoke(sig.signature_id) is True

    def test_returns_false_when_missing(self):
        store = DocSignatureStore()
        assert store.revoke("nonexistent") is False

    def test_marks_revoked(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.revoke(sig.signature_id)
        assert store.get(sig.signature_id).revoked is True

    def test_revoke_twice_still_true(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.revoke(sig.signature_id)
        assert store.revoke(sig.signature_id) is True


# ---------------------------------------------------------------------------
# TestUnrevoke
# ---------------------------------------------------------------------------


class TestUnrevoke:
    def test_returns_true_when_found(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.revoke(sig.signature_id)
        assert store.unrevoke(sig.signature_id) is True

    def test_returns_false_when_missing(self):
        store = DocSignatureStore()
        assert store.unrevoke("nonexistent") is False

    def test_clears_revoked_flag(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.revoke(sig.signature_id)
        store.unrevoke(sig.signature_id)
        assert store.get(sig.signature_id).revoked is False

    def test_unrevoke_on_active_signature_idempotent(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert store.unrevoke(sig.signature_id) is True
        assert store.get(sig.signature_id).revoked is False


# ---------------------------------------------------------------------------
# TestDelete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_returns_true_when_existed(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        assert store.delete(sig.signature_id) is True

    def test_returns_false_when_missing(self):
        store = DocSignatureStore()
        assert store.delete("nonexistent") is False

    def test_removes_signature(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.delete(sig.signature_id)
        assert store.get(sig.signature_id) is None

    def test_removes_from_doc_index(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.delete(sig.signature_id)
        assert store.signatures_for_doc("doc1", include_revoked=True) == []

    def test_removes_from_signer_index(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.delete(sig.signature_id)
        assert store.signatures_by_signer("alice", include_revoked=True) == []

    def test_delete_one_keeps_others(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc1", "bob", "v")
        store.delete(s1.signature_id)
        remaining = store.signatures_for_doc("doc1")
        assert len(remaining) == 1
        assert remaining[0].signature_id == s2.signature_id


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------


class TestGet:
    def test_returns_signature_when_found(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        result = store.get(sig.signature_id)
        assert result is sig or result.signature_id == sig.signature_id

    def test_returns_none_when_missing(self):
        store = DocSignatureStore()
        assert store.get("nonexistent") is None

    def test_get_after_delete_returns_none(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.delete(sig.signature_id)
        assert store.get(sig.signature_id) is None


# ---------------------------------------------------------------------------
# TestSignaturesForDoc
# ---------------------------------------------------------------------------


class TestSignaturesForDoc:
    def test_empty_for_unknown_doc(self):
        store = DocSignatureStore()
        assert store.signatures_for_doc("nope") == []

    def test_returns_signatures_on_doc(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v", now=1.0)
        s2 = store.sign("doc1", "bob", "v", now=2.0)
        result = store.signatures_for_doc("doc1")
        ids = [s.signature_id for s in result]
        assert s1.signature_id in ids
        assert s2.signature_id in ids

    def test_sorted_by_signed_at(self):
        store = DocSignatureStore()
        s_late = store.sign("doc1", "alice", "v", now=10.0)
        s_early = store.sign("doc1", "bob", "v", now=1.0)
        s_mid = store.sign("doc1", "carol", "v", now=5.0)
        result = store.signatures_for_doc("doc1")
        assert [s.signature_id for s in result] == [
            s_early.signature_id,
            s_mid.signature_id,
            s_late.signature_id,
        ]

    def test_excludes_revoked_by_default(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc1", "bob", "v")
        store.revoke(s1.signature_id)
        result = store.signatures_for_doc("doc1")
        ids = [s.signature_id for s in result]
        assert s2.signature_id in ids
        assert s1.signature_id not in ids

    def test_include_revoked_true(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc1", "bob", "v")
        store.revoke(s1.signature_id)
        result = store.signatures_for_doc("doc1", include_revoked=True)
        ids = {s.signature_id for s in result}
        assert ids == {s1.signature_id, s2.signature_id}

    def test_other_docs_not_included(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        s2 = store.sign("doc2", "bob", "v")
        result = store.signatures_for_doc("doc1")
        assert s2.signature_id not in [s.signature_id for s in result]


# ---------------------------------------------------------------------------
# TestSignaturesBySigner
# ---------------------------------------------------------------------------


class TestSignaturesBySigner:
    def test_empty_for_unknown_signer(self):
        store = DocSignatureStore()
        assert store.signatures_by_signer("nobody") == []

    def test_returns_all_signers_signatures(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc2", "alice", "v")
        result = store.signatures_by_signer("alice")
        assert {s.signature_id for s in result} == {s1.signature_id, s2.signature_id}

    def test_sorted_by_signed_at(self):
        store = DocSignatureStore()
        a = store.sign("doc1", "alice", "v", now=5.0)
        b = store.sign("doc2", "alice", "v", now=1.0)
        result = store.signatures_by_signer("alice")
        assert [s.signature_id for s in result] == [b.signature_id, a.signature_id]

    def test_excludes_revoked_by_default(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc2", "alice", "v")
        store.revoke(s1.signature_id)
        result = store.signatures_by_signer("alice")
        assert [s.signature_id for s in result] == [s2.signature_id]

    def test_include_revoked_true(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc2", "alice", "v")
        store.revoke(s1.signature_id)
        result = store.signatures_by_signer("alice", include_revoked=True)
        assert {s.signature_id for s in result} == {s1.signature_id, s2.signature_id}

    def test_other_signers_not_included(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        b = store.sign("doc1", "bob", "v")
        result = store.signatures_by_signer("alice")
        assert b.signature_id not in [s.signature_id for s in result]


# ---------------------------------------------------------------------------
# TestHasSigned
# ---------------------------------------------------------------------------


class TestHasSigned:
    def test_true_when_signed(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        assert store.has_signed("alice", "doc1") is True

    def test_false_when_not_signed(self):
        store = DocSignatureStore()
        store.sign("doc1", "bob", "v")
        assert store.has_signed("alice", "doc1") is False

    def test_false_when_no_data(self):
        store = DocSignatureStore()
        assert store.has_signed("alice", "doc1") is False

    def test_revoked_excluded(self):
        store = DocSignatureStore()
        sig = store.sign("doc1", "alice", "v")
        store.revoke(sig.signature_id)
        assert store.has_signed("alice", "doc1") is False

    def test_still_true_with_one_active_among_revoked(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        store.sign("doc1", "alice", "v2")
        store.revoke(s1.signature_id)
        assert store.has_signed("alice", "doc1") is True

    def test_different_doc_false(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        assert store.has_signed("alice", "doc2") is False


# ---------------------------------------------------------------------------
# TestSignersForDoc
# ---------------------------------------------------------------------------


class TestSignersForDoc:
    def test_empty_unknown_doc(self):
        store = DocSignatureStore()
        assert store.signers_for_doc("nope") == []

    def test_returns_unique_signers(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v1")
        store.sign("doc1", "alice", "v2")
        store.sign("doc1", "bob", "v")
        assert store.signers_for_doc("doc1") == ["alice", "bob"]

    def test_sorted_alphabetically(self):
        store = DocSignatureStore()
        store.sign("doc1", "charlie", "v")
        store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        assert store.signers_for_doc("doc1") == ["alice", "bob", "charlie"]

    def test_excludes_revoked_signers(self):
        store = DocSignatureStore()
        s = store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        store.revoke(s.signature_id)
        assert store.signers_for_doc("doc1") == ["bob"]

    def test_signer_with_revoked_and_active_still_included(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v1")
        store.sign("doc1", "alice", "v2")
        store.revoke(s1.signature_id)
        assert "alice" in store.signers_for_doc("doc1")


# ---------------------------------------------------------------------------
# TestVerifyCount
# ---------------------------------------------------------------------------


class TestVerifyCount:
    def test_zero_unknown_doc(self):
        store = DocSignatureStore()
        assert store.verify_count("nope") == 0

    def test_counts_active(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        store.sign("doc1", "carol", "v")
        assert store.verify_count("doc1") == 3

    def test_excludes_revoked(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        store.revoke(s1.signature_id)
        assert store.verify_count("doc1") == 1

    def test_other_docs_not_counted(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        store.sign("doc2", "bob", "v")
        assert store.verify_count("doc1") == 1


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty_when_no_signatures(self):
        store = DocSignatureStore()
        assert store.all_doc_ids() == []

    def test_unique_sorted_ids(self):
        store = DocSignatureStore()
        store.sign("zeta", "a", "v")
        store.sign("alpha", "a", "v")
        store.sign("mu", "a", "v")
        store.sign("alpha", "b", "v")  # duplicate doc_id
        assert store.all_doc_ids() == ["alpha", "mu", "zeta"]

    def test_includes_doc_with_only_revoked_signatures(self):
        # delete is the only thing that removes from index; revoke does not.
        store = DocSignatureStore()
        s = store.sign("doc1", "alice", "v")
        store.revoke(s.signature_id)
        assert "doc1" in store.all_doc_ids()

    def test_excludes_deleted_doc(self):
        store = DocSignatureStore()
        s = store.sign("doc1", "alice", "v")
        store.delete(s.signature_id)
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_stats(self):
        store = DocSignatureStore()
        s = store.stats()
        assert s == SignatureStats(0, 0, 0, 0)

    def test_total_signatures_excludes_revoked(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        s = store.sign("doc2", "carol", "v")
        store.revoke(s.signature_id)
        st = store.stats()
        assert st.total_signatures == 2

    def test_revoked_count(self):
        store = DocSignatureStore()
        s1 = store.sign("doc1", "alice", "v")
        s2 = store.sign("doc2", "bob", "v")
        store.sign("doc3", "carol", "v")
        store.revoke(s1.signature_id)
        store.revoke(s2.signature_id)
        st = store.stats()
        assert st.revoked_count == 2

    def test_unique_docs(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        store.sign("doc1", "bob", "v")
        store.sign("doc2", "carol", "v")
        st = store.stats()
        assert st.unique_docs == 2

    def test_unique_signers(self):
        store = DocSignatureStore()
        store.sign("doc1", "alice", "v")
        store.sign("doc2", "alice", "v")
        store.sign("doc1", "bob", "v")
        st = store.stats()
        assert st.unique_signers == 2

    def test_returns_signature_stats_instance(self):
        store = DocSignatureStore()
        assert isinstance(store.stats(), SignatureStats)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_sign_no_loss(self):
        store = DocSignatureStore()
        n_threads = 8
        per_thread = 50

        def worker(idx: int) -> None:
            for i in range(per_thread):
                store.sign(f"doc{idx}", f"user{idx}", f"v{i}")

        threads = [
            threading.Thread(target=worker, args=(i,)) for i in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = store.stats()
        assert st.total_signatures == n_threads * per_thread
        assert st.unique_docs == n_threads
        assert st.unique_signers == n_threads

    def test_concurrent_sign_and_revoke(self):
        store = DocSignatureStore()
        ids_lock = threading.Lock()
        all_ids: list[str] = []

        def writer() -> None:
            for i in range(50):
                sig = store.sign("doc1", "alice", f"v{i}")
                with ids_lock:
                    all_ids.append(sig.signature_id)

        threads = [threading.Thread(target=writer) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Revoke half from the main thread; mutations during revoke should be safe.
        for sid in all_ids[: len(all_ids) // 2]:
            assert store.revoke(sid) is True

        st = store.stats()
        assert st.revoked_count == len(all_ids) // 2
        assert st.total_signatures == len(all_ids) - len(all_ids) // 2
