"""Tests for E358 DocSignoffTracker."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_signoff_tracker import (
    DocSignoffTracker,
    Signoff,
    SignoffStats,
)


# ---------- Signoff dataclass ----------


class TestSignoffDataclass:
    def test_required_fields(self):
        s = Signoff(doc_id="d1", user_id="u1")
        assert s.doc_id == "d1"
        assert s.user_id == "u1"

    def test_defaults(self):
        s = Signoff(doc_id="d1", user_id="u1")
        assert s.version == ""
        assert s.signed_at == 0.0
        assert s.revoked is False
        assert s.note == ""

    def test_custom_values(self):
        s = Signoff(
            doc_id="d", user_id="u", version="v1", signed_at=1.5,
            revoked=True, note="hello",
        )
        assert s.version == "v1"
        assert s.signed_at == 1.5
        assert s.revoked is True
        assert s.note == "hello"

    def test_equality(self):
        a = Signoff("d", "u", "v", 1.0, False, "")
        b = Signoff("d", "u", "v", 1.0, False, "")
        assert a == b

    def test_mutable(self):
        s = Signoff("d", "u")
        s.revoked = True
        assert s.revoked is True


# ---------- SignoffStats dataclass ----------


class TestSignoffStatsDataclass:
    def test_defaults(self):
        st = SignoffStats()
        assert st.total_signoffs == 0
        assert st.revoked_count == 0
        assert st.unique_docs == 0
        assert st.unique_users == 0

    def test_construction(self):
        st = SignoffStats(
            total_signoffs=3, revoked_count=1, unique_docs=2, unique_users=2,
        )
        assert st.total_signoffs == 3
        assert st.revoked_count == 1
        assert st.unique_docs == 2
        assert st.unique_users == 2

    def test_equality(self):
        a = SignoffStats(1, 2, 3, 4)
        b = SignoffStats(1, 2, 3, 4)
        assert a == b


# ---------- Construction ----------


class TestConstruction:
    def test_empty_on_create(self):
        t = DocSignoffTracker()
        assert t.all_doc_ids() == []
        assert t.stats() == SignoffStats()

    def test_get_missing(self):
        t = DocSignoffTracker()
        assert t.get("d", "u") is None

    def test_independent_instances(self):
        t1 = DocSignoffTracker()
        t2 = DocSignoffTracker()
        t1.sign_off("d", "u")
        assert t2.get("d", "u") is None


# ---------- sign_off ----------


class TestSignOff:
    def test_creates_new(self):
        t = DocSignoffTracker()
        s = t.sign_off("d1", "u1")
        assert isinstance(s, Signoff)
        assert s.doc_id == "d1"
        assert s.user_id == "u1"
        assert s.revoked is False

    def test_uses_provided_now(self):
        t = DocSignoffTracker()
        s = t.sign_off("d", "u", now=123.0)
        assert s.signed_at == 123.0

    def test_defaults_now_to_time(self):
        t = DocSignoffTracker()
        s = t.sign_off("d", "u")
        assert s.signed_at > 0.0

    def test_with_version_and_note(self):
        t = DocSignoffTracker()
        s = t.sign_off("d", "u", version="v2", note="ok")
        assert s.version == "v2"
        assert s.note == "ok"

    def test_replace_existing(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u", version="v1", now=1.0)
        s = t.sign_off("d", "u", version="v2", now=2.0)
        assert s.version == "v2"
        assert s.signed_at == 2.0
        assert t.get("d", "u").version == "v2"

    def test_replace_resets_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        assert t.get("d", "u").revoked is True
        t.sign_off("d", "u")
        assert t.get("d", "u").revoked is False

    def test_indexes_updated(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.signers_for_doc("d") == ["u"]
        assert t.docs_for_user("u") == ["d"]


# ---------- revoke ----------


class TestRevoke:
    def test_returns_true_when_exists(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.revoke("d", "u") is True

    def test_returns_false_when_missing(self):
        t = DocSignoffTracker()
        assert t.revoke("d", "u") is False

    def test_sets_revoked_flag(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        assert t.get("d", "u").revoked is True

    def test_idempotent(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.revoke("d", "u") is True
        assert t.revoke("d", "u") is True
        assert t.get("d", "u").revoked is True


# ---------- unrevoke ----------


class TestUnrevoke:
    def test_returns_true_when_exists(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        assert t.unrevoke("d", "u") is True

    def test_returns_false_when_missing(self):
        t = DocSignoffTracker()
        assert t.unrevoke("d", "u") is False

    def test_clears_flag(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        t.unrevoke("d", "u")
        assert t.get("d", "u").revoked is False

    def test_idempotent_when_not_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.unrevoke("d", "u") is True
        assert t.get("d", "u").revoked is False


# ---------- delete ----------


class TestDelete:
    def test_returns_true_when_exists(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.delete("d", "u") is True

    def test_returns_false_when_missing(self):
        t = DocSignoffTracker()
        assert t.delete("d", "u") is False

    def test_fully_removes(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.delete("d", "u")
        assert t.get("d", "u") is None

    def test_index_cleaned(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.delete("d", "u")
        assert t.signers_for_doc("d") == []
        assert t.docs_for_user("u") == []
        assert t.all_doc_ids() == []

    def test_partial_delete_keeps_doc(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.delete("d", "u1")
        assert t.signers_for_doc("d") == ["u2"]


# ---------- get ----------


class TestGet:
    def test_found(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u", version="v", now=1.0)
        s = t.get("d", "u")
        assert s is not None
        assert s.version == "v"
        assert s.signed_at == 1.0

    def test_not_found(self):
        t = DocSignoffTracker()
        assert t.get("missing", "u") is None

    def test_returns_revoked_record(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        s = t.get("d", "u")
        assert s is not None
        assert s.revoked is True


# ---------- has_signed_off ----------


class TestHasSignedOff:
    def test_true_when_signed(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        assert t.has_signed_off("u", "d") is True

    def test_false_when_missing(self):
        t = DocSignoffTracker()
        assert t.has_signed_off("u", "d") is False

    def test_false_when_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        assert t.has_signed_off("u", "d") is False

    def test_true_after_unrevoke(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        t.unrevoke("d", "u")
        assert t.has_signed_off("u", "d") is True

    def test_argument_order(self):
        # has_signed_off(user_id, doc_id) — distinct order from sign_off
        t = DocSignoffTracker()
        t.sign_off(doc_id="docA", user_id="userA")
        assert t.has_signed_off("userA", "docA") is True
        assert t.has_signed_off("docA", "userA") is False


# ---------- signers_for_doc ----------


class TestSignersForDoc:
    def test_sorted(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u3")
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        assert t.signers_for_doc("d") == ["u1", "u2", "u3"]

    def test_empty_for_unknown(self):
        t = DocSignoffTracker()
        assert t.signers_for_doc("nope") == []

    def test_excludes_revoked_by_default(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.revoke("d", "u2")
        assert t.signers_for_doc("d") == ["u1"]

    def test_include_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.revoke("d", "u2")
        assert t.signers_for_doc("d", include_revoked=True) == ["u1", "u2"]

    def test_isolated_per_doc(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "v")
        assert t.signers_for_doc("d1") == ["u"]
        assert t.signers_for_doc("d2") == ["v"]


# ---------- docs_for_user ----------


class TestDocsForUser:
    def test_sorted(self):
        t = DocSignoffTracker()
        t.sign_off("d3", "u")
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        assert t.docs_for_user("u") == ["d1", "d2", "d3"]

    def test_empty_for_unknown(self):
        t = DocSignoffTracker()
        assert t.docs_for_user("nope") == []

    def test_excludes_revoked_by_default(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        t.revoke("d1", "u")
        assert t.docs_for_user("u") == ["d2"]

    def test_include_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        t.revoke("d1", "u")
        assert t.docs_for_user("u", include_revoked=True) == ["d1", "d2"]


# ---------- signoff_count ----------


class TestSignoffCount:
    def test_zero_unknown(self):
        t = DocSignoffTracker()
        assert t.signoff_count("d") == 0

    def test_counts_active(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.sign_off("d", "u3")
        assert t.signoff_count("d") == 3

    def test_excludes_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.revoke("d", "u1")
        assert t.signoff_count("d") == 1

    def test_zero_after_all_revoked(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.revoke("d", "u1")
        assert t.signoff_count("d") == 0


# ---------- all_doc_ids ----------


class TestAllDocIds:
    def test_empty(self):
        t = DocSignoffTracker()
        assert t.all_doc_ids() == []

    def test_sorted_unique(self):
        t = DocSignoffTracker()
        t.sign_off("d3", "u")
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        t.sign_off("d1", "v")
        assert t.all_doc_ids() == ["d1", "d2", "d3"]

    def test_keeps_revoked_docs(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.revoke("d", "u")
        assert t.all_doc_ids() == ["d"]


# ---------- clear_doc ----------


class TestClearDoc:
    def test_returns_count(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        assert t.clear_doc("d") == 2

    def test_zero_when_unknown(self):
        t = DocSignoffTracker()
        assert t.clear_doc("d") == 0

    def test_removes_records(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.clear_doc("d")
        assert t.get("d", "u1") is None
        assert t.get("d", "u2") is None
        assert "d" not in t.all_doc_ids()

    def test_does_not_touch_other_docs(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        t.clear_doc("d1")
        assert t.get("d2", "u") is not None

    def test_counts_revoked_too(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.revoke("d", "u1")
        assert t.clear_doc("d") == 2


# ---------- clear_user ----------


class TestClearUser:
    def test_returns_count(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        assert t.clear_user("u") == 2

    def test_zero_when_unknown(self):
        t = DocSignoffTracker()
        assert t.clear_user("u") == 0

    def test_removes_records(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u")
        t.sign_off("d2", "u")
        t.clear_user("u")
        assert t.docs_for_user("u") == []

    def test_does_not_touch_other_users(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u1")
        t.sign_off("d", "u2")
        t.clear_user("u1")
        assert t.get("d", "u2") is not None
        assert t.signers_for_doc("d") == ["u2"]


# ---------- stats ----------


class TestStats:
    def test_empty(self):
        t = DocSignoffTracker()
        assert t.stats() == SignoffStats(0, 0, 0, 0)

    def test_totals(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u1")
        t.sign_off("d1", "u2")
        t.sign_off("d2", "u1")
        st = t.stats()
        assert st.total_signoffs == 3
        assert st.revoked_count == 0
        assert st.unique_docs == 2
        assert st.unique_users == 2

    def test_revoked_separately_counted(self):
        t = DocSignoffTracker()
        t.sign_off("d1", "u1")
        t.sign_off("d2", "u2")
        t.revoke("d1", "u1")
        st = t.stats()
        assert st.total_signoffs == 1
        assert st.revoked_count == 1
        assert st.unique_docs == 2
        assert st.unique_users == 2

    def test_after_delete(self):
        t = DocSignoffTracker()
        t.sign_off("d", "u")
        t.delete("d", "u")
        assert t.stats() == SignoffStats(0, 0, 0, 0)


# ---------- Thread safety ----------


class TestThreadSafety:
    def test_concurrent_sign_off_unique_pairs(self):
        t = DocSignoffTracker()
        n_threads = 8
        per_thread = 50

        def worker(tid: int) -> None:
            for i in range(per_thread):
                t.sign_off(f"d{i}", f"u{tid}")

        threads = [
            threading.Thread(target=worker, args=(i,))
            for i in range(n_threads)
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        st = t.stats()
        assert st.total_signoffs == n_threads * per_thread
        assert st.unique_docs == per_thread
        assert st.unique_users == n_threads

    def test_concurrent_sign_off_same_pair(self):
        t = DocSignoffTracker()

        def worker() -> None:
            for _ in range(100):
                t.sign_off("d", "u")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        # Only one entry for (d, u) regardless of contention
        st = t.stats()
        assert st.total_signoffs == 1
        assert st.unique_docs == 1
        assert st.unique_users == 1

    def test_concurrent_sign_off_and_revoke(self):
        t = DocSignoffTracker()
        for i in range(20):
            t.sign_off(f"d{i}", "u")

        def signer() -> None:
            for i in range(20):
                t.sign_off(f"d{i}", "u")

        def revoker() -> None:
            for i in range(20):
                t.revoke(f"d{i}", "u")

        threads = [
            threading.Thread(target=signer),
            threading.Thread(target=revoker),
            threading.Thread(target=signer),
            threading.Thread(target=revoker),
        ]
        for th in threads:
            th.start()
        for th in threads:
            th.join()

        # All 20 (d, u) keys must still exist (delete not called)
        assert len(t.all_doc_ids()) == 20
        for i in range(20):
            assert t.get(f"d{i}", "u") is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
