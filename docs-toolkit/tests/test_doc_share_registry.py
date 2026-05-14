"""Tests for docstoolkit.doc_share_registry (E309)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_share_registry import (
    DocShareRegistry,
    ShareGrant,
    ShareLink,
    ShareStats,
)


# ---------------------------------------------------------------------------
# TestShareLinkDataclass
# ---------------------------------------------------------------------------

class TestShareLinkDataclass:
    def test_required_fields(self):
        lnk = ShareLink(link_id="a", doc_id="d1", created_by="u1")
        assert lnk.link_id == "a"
        assert lnk.doc_id == "d1"
        assert lnk.created_by == "u1"

    def test_defaults(self):
        lnk = ShareLink(link_id="a", doc_id="d1", created_by="u1")
        assert lnk.created_at == 0.0
        assert lnk.expires_at is None
        assert lnk.access_level == "read"
        assert lnk.use_count == 0
        assert lnk.revoked is False

    def test_custom_values(self):
        lnk = ShareLink(
            link_id="x",
            doc_id="d",
            created_by="u",
            created_at=100.0,
            expires_at=200.0,
            access_level="edit",
            use_count=3,
            revoked=True,
        )
        assert lnk.created_at == 100.0
        assert lnk.expires_at == 200.0
        assert lnk.access_level == "edit"
        assert lnk.use_count == 3
        assert lnk.revoked is True


# ---------------------------------------------------------------------------
# TestShareGrantDataclass
# ---------------------------------------------------------------------------

class TestShareGrantDataclass:
    def test_required_fields(self):
        g = ShareGrant(grant_id="g1", doc_id="d1", granted_to="u1", granted_by="u2")
        assert g.grant_id == "g1"
        assert g.doc_id == "d1"
        assert g.granted_to == "u1"
        assert g.granted_by == "u2"

    def test_defaults(self):
        g = ShareGrant(grant_id="g1", doc_id="d1", granted_to="u1", granted_by="u2")
        assert g.granted_at == 0.0
        assert g.access_level == "read"
        assert g.revoked is False

    def test_custom_values(self):
        g = ShareGrant(
            grant_id="g2",
            doc_id="d2",
            granted_to="alice",
            granted_by="bob",
            granted_at=500.0,
            access_level="comment",
            revoked=True,
        )
        assert g.granted_at == 500.0
        assert g.access_level == "comment"
        assert g.revoked is True


# ---------------------------------------------------------------------------
# TestShareStatsDataclass
# ---------------------------------------------------------------------------

class TestShareStatsDataclass:
    def test_fields(self):
        s = ShareStats(total_links=5, total_grants=3, unique_shared_docs=4)
        assert s.total_links == 5
        assert s.total_grants == 3
        assert s.unique_shared_docs == 4

    def test_zero_values(self):
        s = ShareStats(total_links=0, total_grants=0, unique_shared_docs=0)
        assert s.total_links == 0
        assert s.total_grants == 0
        assert s.unique_shared_docs == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_default_construction(self):
        reg = DocShareRegistry()
        st = reg.stats()
        assert st.total_links == 0
        assert st.total_grants == 0
        assert st.unique_shared_docs == 0

    def test_multiple_independent_instances(self):
        reg1 = DocShareRegistry()
        reg2 = DocShareRegistry()
        reg1.create_link("d1", "u1")
        assert reg2.stats().total_links == 0


# ---------------------------------------------------------------------------
# TestCreateLink
# ---------------------------------------------------------------------------

class TestCreateLink:
    def test_returns_share_link(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "user1")
        assert isinstance(lnk, ShareLink)

    def test_uuid_generated(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "user1")
        # UUID4 format: 8-4-4-4-12 hex chars separated by hyphens
        assert len(lnk.link_id) == 36
        assert lnk.link_id.count("-") == 4

    def test_doc_id_and_creator_stored(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "alice")
        assert lnk.doc_id == "doc1"
        assert lnk.created_by == "alice"

    def test_timestamp_stored(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1", now=1_000.0)
        assert lnk.created_at == 1_000.0

    def test_default_access_level(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1")
        assert lnk.access_level == "read"

    def test_custom_access_level(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1", access_level="edit")
        assert lnk.access_level == "edit"

    def test_expires_at_none_by_default(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1")
        assert lnk.expires_at is None

    def test_expires_at_stored(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1", expires_at=9_999.0)
        assert lnk.expires_at == 9_999.0

    def test_use_count_starts_at_zero(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1")
        assert lnk.use_count == 0

    def test_not_revoked_on_creation(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("doc1", "u1")
        assert lnk.revoked is False

    def test_unique_ids_across_calls(self):
        reg = DocShareRegistry()
        ids = {reg.create_link("doc1", "u1").link_id for _ in range(20)}
        assert len(ids) == 20


# ---------------------------------------------------------------------------
# TestRevokeLink
# ---------------------------------------------------------------------------

class TestRevokeLink:
    def test_returns_true_on_success(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        assert reg.revoke_link(lnk.link_id) is True

    def test_revoked_flag_set(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        reg.revoke_link(lnk.link_id)
        assert reg.get_link(lnk.link_id).revoked is True

    def test_returns_false_for_unknown_id(self):
        reg = DocShareRegistry()
        assert reg.revoke_link("no-such-id") is False

    def test_double_revoke_still_true(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        reg.revoke_link(lnk.link_id)
        # second revoke should still return True (link is found)
        assert reg.revoke_link(lnk.link_id) is True


# ---------------------------------------------------------------------------
# TestGetLink
# ---------------------------------------------------------------------------

class TestGetLink:
    def test_found(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        result = reg.get_link(lnk.link_id)
        assert result is not None
        assert result.link_id == lnk.link_id

    def test_not_found(self):
        reg = DocShareRegistry()
        assert reg.get_link("ghost") is None

    def test_returns_same_object(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        assert reg.get_link(lnk.link_id) is lnk


# ---------------------------------------------------------------------------
# TestUseLink
# ---------------------------------------------------------------------------

class TestUseLink:
    def test_increments_use_count(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        assert reg.use_link(lnk.link_id) is True
        assert reg.get_link(lnk.link_id).use_count == 1

    def test_multiple_uses(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        for _ in range(5):
            reg.use_link(lnk.link_id)
        assert reg.get_link(lnk.link_id).use_count == 5

    def test_false_if_revoked(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        reg.revoke_link(lnk.link_id)
        assert reg.use_link(lnk.link_id) is False

    def test_use_count_unchanged_after_revoke(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        reg.use_link(lnk.link_id)
        reg.revoke_link(lnk.link_id)
        reg.use_link(lnk.link_id)
        assert reg.get_link(lnk.link_id).use_count == 1

    def test_false_if_expired(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u", expires_at=100.0, now=50.0)
        assert reg.use_link(lnk.link_id, now=200.0) is False

    def test_true_when_not_yet_expired(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u", expires_at=300.0, now=50.0)
        assert reg.use_link(lnk.link_id, now=100.0) is True

    def test_true_if_no_expiry(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d", "u")
        assert reg.use_link(lnk.link_id) is True

    def test_false_for_unknown_link(self):
        reg = DocShareRegistry()
        assert reg.use_link("nonexistent") is False


# ---------------------------------------------------------------------------
# TestLinksForDoc
# ---------------------------------------------------------------------------

class TestLinksForDoc:
    def test_empty_for_unknown_doc(self):
        reg = DocShareRegistry()
        assert reg.links_for_doc("ghost") == []

    def test_returns_links_for_doc(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        reg.create_link("d2", "u1")
        result = reg.links_for_doc("d1")
        assert len(result) == 1
        assert result[0].link_id == lnk.link_id

    def test_sorted_by_created_at(self):
        reg = DocShareRegistry()
        lnk1 = reg.create_link("d1", "u1", now=300.0)
        lnk2 = reg.create_link("d1", "u1", now=100.0)
        lnk3 = reg.create_link("d1", "u1", now=200.0)
        result = reg.links_for_doc("d1")
        assert [l.link_id for l in result] == [lnk2.link_id, lnk3.link_id, lnk1.link_id]

    def test_revoked_excluded_by_default(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        reg.revoke_link(lnk.link_id)
        assert reg.links_for_doc("d1") == []

    def test_revoked_included_when_flag_set(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        reg.revoke_link(lnk.link_id)
        result = reg.links_for_doc("d1", include_revoked=True)
        assert len(result) == 1
        assert result[0].revoked is True


# ---------------------------------------------------------------------------
# TestGrantAccess
# ---------------------------------------------------------------------------

class TestGrantAccess:
    def test_returns_share_grant(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        assert isinstance(g, ShareGrant)

    def test_uuid_generated(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        assert len(g.grant_id) == 36
        assert g.grant_id.count("-") == 4

    def test_fields_stored(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "bob", access_level="comment", now=555.0)
        assert g.doc_id == "d1"
        assert g.granted_to == "alice"
        assert g.granted_by == "bob"
        assert g.access_level == "comment"
        assert g.granted_at == 555.0

    def test_default_access_level(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        assert g.access_level == "read"

    def test_not_revoked_on_creation(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        assert g.revoked is False


# ---------------------------------------------------------------------------
# TestRevokeGrant
# ---------------------------------------------------------------------------

class TestRevokeGrant:
    def test_returns_true_on_success(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d", "alice", "admin")
        assert reg.revoke_grant(g.grant_id) is True

    def test_revoked_flag_set(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        assert reg.get_grant(g.grant_id).revoked is True

    def test_returns_false_for_unknown_id(self):
        reg = DocShareRegistry()
        assert reg.revoke_grant("no-such-grant") is False


# ---------------------------------------------------------------------------
# TestGetGrant
# ---------------------------------------------------------------------------

class TestGetGrant:
    def test_found(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        result = reg.get_grant(g.grant_id)
        assert result is not None
        assert result.grant_id == g.grant_id

    def test_not_found(self):
        reg = DocShareRegistry()
        assert reg.get_grant("ghost") is None

    def test_returns_same_object(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        assert reg.get_grant(g.grant_id) is g


# ---------------------------------------------------------------------------
# TestGrantsForDoc
# ---------------------------------------------------------------------------

class TestGrantsForDoc:
    def test_empty_for_unknown_doc(self):
        reg = DocShareRegistry()
        assert reg.grants_for_doc("ghost") == []

    def test_returns_grants_for_doc(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.grant_access("d2", "bob", "admin")
        result = reg.grants_for_doc("d1")
        assert len(result) == 1
        assert result[0].grant_id == g.grant_id

    def test_sorted_by_granted_at(self):
        reg = DocShareRegistry()
        g1 = reg.grant_access("d1", "alice", "admin", now=300.0)
        g2 = reg.grant_access("d1", "bob", "admin", now=100.0)
        g3 = reg.grant_access("d1", "carol", "admin", now=200.0)
        result = reg.grants_for_doc("d1")
        assert [g.grant_id for g in result] == [g2.grant_id, g3.grant_id, g1.grant_id]

    def test_revoked_excluded_by_default(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        assert reg.grants_for_doc("d1") == []

    def test_revoked_included_when_flag_set(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        result = reg.grants_for_doc("d1", include_revoked=True)
        assert len(result) == 1
        assert result[0].revoked is True


# ---------------------------------------------------------------------------
# TestGrantsForUser
# ---------------------------------------------------------------------------

class TestGrantsForUser:
    def test_empty_for_unknown_user(self):
        reg = DocShareRegistry()
        assert reg.grants_for_user("nobody") == []

    def test_returns_grants_for_user(self):
        reg = DocShareRegistry()
        g1 = reg.grant_access("d1", "alice", "admin", now=10.0)
        g2 = reg.grant_access("d2", "alice", "admin", now=20.0)
        reg.grant_access("d3", "bob", "admin")
        result = reg.grants_for_user("alice")
        ids = [g.grant_id for g in result]
        assert g1.grant_id in ids
        assert g2.grant_id in ids
        assert len(result) == 2

    def test_sorted_by_granted_at(self):
        reg = DocShareRegistry()
        g1 = reg.grant_access("d1", "alice", "admin", now=50.0)
        g2 = reg.grant_access("d2", "alice", "admin", now=10.0)
        result = reg.grants_for_user("alice")
        assert result[0].grant_id == g2.grant_id
        assert result[1].grant_id == g1.grant_id

    def test_cross_doc_grants(self):
        reg = DocShareRegistry()
        for i in range(4):
            reg.grant_access(f"doc{i}", "alice", "admin", now=float(i))
        result = reg.grants_for_user("alice")
        assert len(result) == 4

    def test_revoked_excluded_by_default(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        assert reg.grants_for_user("alice") == []

    def test_revoked_included_when_flag_set(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        result = reg.grants_for_user("alice", include_revoked=True)
        assert len(result) == 1


# ---------------------------------------------------------------------------
# TestHasAccess
# ---------------------------------------------------------------------------

class TestHasAccess:
    def test_true_with_active_grant(self):
        reg = DocShareRegistry()
        reg.grant_access("d1", "alice", "admin")
        assert reg.has_access("alice", "d1") is True

    def test_false_after_revoke(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g.grant_id)
        assert reg.has_access("alice", "d1") is False

    def test_false_for_unknown_user(self):
        reg = DocShareRegistry()
        reg.grant_access("d1", "alice", "admin")
        assert reg.has_access("bob", "d1") is False

    def test_false_for_unknown_doc(self):
        reg = DocShareRegistry()
        assert reg.has_access("alice", "no-doc") is False

    def test_true_when_one_of_two_grants_active(self):
        reg = DocShareRegistry()
        g1 = reg.grant_access("d1", "alice", "admin")
        reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g1.grant_id)
        # second grant still active
        assert reg.has_access("alice", "d1") is True

    def test_false_when_all_grants_revoked(self):
        reg = DocShareRegistry()
        g1 = reg.grant_access("d1", "alice", "admin")
        g2 = reg.grant_access("d1", "alice", "admin")
        reg.revoke_grant(g1.grant_id)
        reg.revoke_grant(g2.grant_id)
        assert reg.has_access("alice", "d1") is False


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_registry(self):
        reg = DocShareRegistry()
        st = reg.stats()
        assert st.total_links == 0
        assert st.total_grants == 0
        assert st.unique_shared_docs == 0

    def test_counts_active_links(self):
        reg = DocShareRegistry()
        reg.create_link("d1", "u1")
        reg.create_link("d2", "u1")
        st = reg.stats()
        assert st.total_links == 2

    def test_revoked_links_not_counted(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        reg.create_link("d1", "u1")
        reg.revoke_link(lnk.link_id)
        st = reg.stats()
        assert st.total_links == 1

    def test_counts_active_grants(self):
        reg = DocShareRegistry()
        reg.grant_access("d1", "alice", "admin")
        reg.grant_access("d2", "bob", "admin")
        st = reg.stats()
        assert st.total_grants == 2

    def test_revoked_grants_not_counted(self):
        reg = DocShareRegistry()
        g = reg.grant_access("d1", "alice", "admin")
        reg.grant_access("d1", "bob", "admin")
        reg.revoke_grant(g.grant_id)
        st = reg.stats()
        assert st.total_grants == 1

    def test_unique_shared_docs(self):
        reg = DocShareRegistry()
        reg.create_link("d1", "u1")
        reg.create_link("d1", "u1")   # same doc, should count once
        reg.create_link("d2", "u1")
        reg.grant_access("d3", "alice", "admin")
        st = reg.stats()
        assert st.unique_shared_docs == 3

    def test_unique_docs_link_and_grant_same_doc(self):
        reg = DocShareRegistry()
        reg.create_link("d1", "u1")
        reg.grant_access("d1", "alice", "admin")
        st = reg.stats()
        assert st.unique_shared_docs == 1

    def test_revoked_items_excluded_from_unique_docs(self):
        reg = DocShareRegistry()
        lnk = reg.create_link("d1", "u1")
        g = reg.grant_access("d2", "alice", "admin")
        reg.revoke_link(lnk.link_id)
        reg.revoke_grant(g.grant_id)
        st = reg.stats()
        assert st.unique_shared_docs == 0


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_create_link(self):
        reg = DocShareRegistry()
        errors: list[Exception] = []
        results: list[ShareLink] = []
        lock = threading.Lock()

        def worker():
            try:
                for _ in range(50):
                    lnk = reg.create_link("shared-doc", "user1")
                    with lock:
                        results.append(lnk)
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        assert len(results) == 500
        # all link_ids must be unique
        ids = {lnk.link_id for lnk in results}
        assert len(ids) == 500

    def test_concurrent_grant_and_revoke(self):
        reg = DocShareRegistry()
        errors: list[Exception] = []

        def granter():
            try:
                for i in range(30):
                    reg.grant_access("doc-x", f"user{i}", "admin")
            except Exception as exc:
                errors.append(exc)

        def checker():
            try:
                for _ in range(30):
                    reg.has_access("user0", "doc-x")
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=granter) for _ in range(5)]
        threads += [threading.Thread(target=checker) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
