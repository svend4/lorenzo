"""Tests for the E366 DocInvitationStore module."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_invitation_store import (
    DocInvitationStore,
    Invitation,
    InvitationStats,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------
class TestInvitationDataclass:
    def test_minimal_construction(self):
        inv = Invitation(
            invitation_id="abc",
            doc_id="d1",
            invitee="u@x.com",
            invited_by="admin",
        )
        assert inv.invitation_id == "abc"
        assert inv.doc_id == "d1"
        assert inv.invitee == "u@x.com"
        assert inv.invited_by == "admin"

    def test_default_role_is_viewer(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.role == "viewer"

    def test_default_status_is_pending(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.status == "pending"

    def test_default_created_at_zero(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.created_at == 0.0

    def test_default_expires_at_none(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.expires_at is None

    def test_default_accepted_at_none(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.accepted_at is None

    def test_default_accepted_by_empty(self):
        inv = Invitation(invitation_id="a", doc_id="d", invitee="u", invited_by="b")
        assert inv.accepted_by == ""

    def test_role_override(self):
        inv = Invitation(
            invitation_id="a",
            doc_id="d",
            invitee="u",
            invited_by="b",
            role="editor",
        )
        assert inv.role == "editor"


class TestInvitationStatsDataclass:
    def test_default_zero(self):
        s = InvitationStats()
        assert s.total == 0
        assert s.pending == 0
        assert s.accepted == 0
        assert s.declined == 0
        assert s.expired == 0
        assert s.revoked == 0

    def test_explicit_values(self):
        s = InvitationStats(total=5, pending=2, accepted=2, declined=1)
        assert s.total == 5
        assert s.pending == 2
        assert s.accepted == 2
        assert s.declined == 1


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------
class TestConstruction:
    def test_empty_store_stats_zero(self):
        store = DocInvitationStore()
        s = store.stats()
        assert s.total == 0

    def test_empty_store_get_returns_none(self):
        store = DocInvitationStore()
        assert store.get("missing") is None

    def test_empty_store_for_doc(self):
        store = DocInvitationStore()
        assert store.invitations_for_doc("d") == []

    def test_empty_store_for_invitee(self):
        store = DocInvitationStore()
        assert store.invitations_for_invitee("u") == []


# ---------------------------------------------------------------------------
# Invite
# ---------------------------------------------------------------------------
class TestInvite:
    def test_returns_invitation_object(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin")
        assert isinstance(inv, Invitation)

    def test_invitation_id_is_uuid(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin")
        # UUID hex form is 36 chars with dashes
        assert len(inv.invitation_id) == 36
        assert inv.invitation_id.count("-") == 4

    def test_invitation_ids_unique(self):
        store = DocInvitationStore()
        ids = {store.invite("d", f"u{i}", "a").invitation_id for i in range(20)}
        assert len(ids) == 20

    def test_default_status_pending(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin")
        assert inv.status == "pending"

    def test_default_role_viewer(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin")
        assert inv.role == "viewer"

    def test_custom_role(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin", role="editor")
        assert inv.role == "editor"

    def test_invited_by_stored(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "u@x.com", "admin42")
        assert inv.invited_by == "admin42"

    def test_invitee_stored(self):
        store = DocInvitationStore()
        inv = store.invite("d1", "person@x.com", "admin")
        assert inv.invitee == "person@x.com"

    def test_doc_id_stored(self):
        store = DocInvitationStore()
        inv = store.invite("doc-xyz", "u", "admin")
        assert inv.doc_id == "doc-xyz"

    def test_created_at_uses_now_param(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a", now=1000.0)
        assert inv.created_at == 1000.0

    def test_created_at_defaults_to_time(self):
        store = DocInvitationStore()
        before = time.time()
        inv = store.invite("d", "u", "a")
        after = time.time()
        assert before <= inv.created_at <= after

    def test_expires_at_stored(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a", expires_at=5000.0)
        assert inv.expires_at == 5000.0

    def test_get_after_invite(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.get(inv.invitation_id) is inv


# ---------------------------------------------------------------------------
# Accept
# ---------------------------------------------------------------------------
class TestAccept:
    def test_accept_returns_true(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.accept(inv.invitation_id) is True

    def test_accept_sets_status(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.accept(inv.invitation_id)
        assert store.get(inv.invitation_id).status == "accepted"

    def test_accept_sets_accepted_at(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.accept(inv.invitation_id, now=2000.0)
        assert store.get(inv.invitation_id).accepted_at == 2000.0

    def test_accept_default_accepted_by_is_invitee(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u@x.com", "a")
        store.accept(inv.invitation_id)
        assert store.get(inv.invitation_id).accepted_by == "u@x.com"

    def test_accept_explicit_accepted_by(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u@x.com", "a")
        store.accept(inv.invitation_id, accepted_by="actual-user")
        assert store.get(inv.invitation_id).accepted_by == "actual-user"

    def test_accept_unknown_returns_false(self):
        store = DocInvitationStore()
        assert store.accept("missing") is False

    def test_accept_already_accepted_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.accept(inv.invitation_id)
        assert store.accept(inv.invitation_id) is False

    def test_accept_after_decline_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.decline(inv.invitation_id)
        assert store.accept(inv.invitation_id) is False

    def test_accept_after_revoke_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.revoke(inv.invitation_id)
        assert store.accept(inv.invitation_id) is False


# ---------------------------------------------------------------------------
# Decline
# ---------------------------------------------------------------------------
class TestDecline:
    def test_decline_returns_true(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.decline(inv.invitation_id) is True

    def test_decline_sets_status(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.decline(inv.invitation_id)
        assert store.get(inv.invitation_id).status == "declined"

    def test_decline_unknown_returns_false(self):
        store = DocInvitationStore()
        assert store.decline("missing") is False

    def test_decline_after_accept_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.accept(inv.invitation_id)
        assert store.decline(inv.invitation_id) is False

    def test_decline_twice_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.decline(inv.invitation_id)
        assert store.decline(inv.invitation_id) is False


# ---------------------------------------------------------------------------
# Revoke
# ---------------------------------------------------------------------------
class TestRevoke:
    def test_revoke_from_pending(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.revoke(inv.invitation_id) is True
        assert store.get(inv.invitation_id).status == "revoked"

    def test_revoke_from_accepted(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.accept(inv.invitation_id)
        assert store.revoke(inv.invitation_id) is True
        assert store.get(inv.invitation_id).status == "revoked"

    def test_revoke_from_declined_fails(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.decline(inv.invitation_id)
        assert store.revoke(inv.invitation_id) is False

    def test_revoke_unknown_returns_false(self):
        store = DocInvitationStore()
        assert store.revoke("missing") is False

    def test_revoke_twice_returns_false(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.revoke(inv.invitation_id)
        assert store.revoke(inv.invitation_id) is False


# ---------------------------------------------------------------------------
# Expire
# ---------------------------------------------------------------------------
class TestExpireIfDue:
    def test_no_expiry_returns_zero(self):
        store = DocInvitationStore()
        store.invite("d", "u", "a")
        assert store.expire_if_due(now=10_000.0) == 0

    def test_expired_invite_counted(self):
        store = DocInvitationStore()
        store.invite("d", "u", "a", expires_at=100.0, now=50.0)
        assert store.expire_if_due(now=200.0) == 1

    def test_expired_status_set(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a", expires_at=100.0, now=50.0)
        store.expire_if_due(now=200.0)
        assert store.get(inv.invitation_id).status == "expired"

    def test_not_yet_expired_not_counted(self):
        store = DocInvitationStore()
        store.invite("d", "u", "a", expires_at=1000.0, now=50.0)
        assert store.expire_if_due(now=200.0) == 0

    def test_already_accepted_not_expired(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a", expires_at=100.0, now=50.0)
        store.accept(inv.invitation_id)
        assert store.expire_if_due(now=200.0) == 0
        assert store.get(inv.invitation_id).status == "accepted"

    def test_multiple_expired(self):
        store = DocInvitationStore()
        for i in range(3):
            store.invite("d", f"u{i}", "a", expires_at=10.0, now=5.0)
        assert store.expire_if_due(now=100.0) == 3


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------
class TestGet:
    def test_get_found(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.get(inv.invitation_id) is inv

    def test_get_not_found(self):
        store = DocInvitationStore()
        assert store.get("nope") is None


# ---------------------------------------------------------------------------
# Invitations for doc
# ---------------------------------------------------------------------------
class TestInvitationsForDoc:
    def test_empty_doc(self):
        store = DocInvitationStore()
        assert store.invitations_for_doc("d") == []

    def test_returns_only_matching_doc(self):
        store = DocInvitationStore()
        store.invite("d1", "u", "a")
        store.invite("d2", "u", "a")
        result = store.invitations_for_doc("d1")
        assert len(result) == 1
        assert result[0].doc_id == "d1"

    def test_sorted_by_created_at(self):
        store = DocInvitationStore()
        a = store.invite("d", "u1", "a", now=300.0)
        b = store.invite("d", "u2", "a", now=100.0)
        c = store.invite("d", "u3", "a", now=200.0)
        result = store.invitations_for_doc("d")
        assert [inv.invitation_id for inv in result] == [
            b.invitation_id,
            c.invitation_id,
            a.invitation_id,
        ]

    def test_status_filter(self):
        store = DocInvitationStore()
        i1 = store.invite("d", "u1", "a")
        store.invite("d", "u2", "a")
        store.accept(i1.invitation_id)
        result = store.invitations_for_doc("d", status="accepted")
        assert len(result) == 1
        assert result[0].invitation_id == i1.invitation_id


# ---------------------------------------------------------------------------
# Invitations for invitee
# ---------------------------------------------------------------------------
class TestInvitationsForInvitee:
    def test_empty_invitee(self):
        store = DocInvitationStore()
        assert store.invitations_for_invitee("u") == []

    def test_returns_only_matching_invitee(self):
        store = DocInvitationStore()
        store.invite("d1", "u1", "a")
        store.invite("d2", "u2", "a")
        result = store.invitations_for_invitee("u1")
        assert len(result) == 1
        assert result[0].invitee == "u1"

    def test_sorted_by_created_at(self):
        store = DocInvitationStore()
        a = store.invite("d1", "u", "a", now=300.0)
        b = store.invite("d2", "u", "a", now=100.0)
        c = store.invite("d3", "u", "a", now=200.0)
        result = store.invitations_for_invitee("u")
        assert [inv.invitation_id for inv in result] == [
            b.invitation_id,
            c.invitation_id,
            a.invitation_id,
        ]

    def test_status_filter(self):
        store = DocInvitationStore()
        i1 = store.invite("d1", "u", "a")
        store.invite("d2", "u", "a")
        store.decline(i1.invitation_id)
        result = store.invitations_for_invitee("u", status="declined")
        assert len(result) == 1
        assert result[0].invitation_id == i1.invitation_id


# ---------------------------------------------------------------------------
# Pending for
# ---------------------------------------------------------------------------
class TestPendingFor:
    def test_empty(self):
        store = DocInvitationStore()
        assert store.pending_for("d") == []

    def test_only_pending(self):
        store = DocInvitationStore()
        i1 = store.invite("d", "u1", "a")
        i2 = store.invite("d", "u2", "a")
        i3 = store.invite("d", "u3", "a")
        store.accept(i2.invitation_id)
        store.decline(i3.invitation_id)
        result = store.pending_for("d")
        assert len(result) == 1
        assert result[0].invitation_id == i1.invitation_id

    def test_pending_for_sorted(self):
        store = DocInvitationStore()
        a = store.invite("d", "u1", "a", now=500.0)
        b = store.invite("d", "u2", "a", now=100.0)
        result = store.pending_for("d")
        assert result[0].invitation_id == b.invitation_id
        assert result[1].invitation_id == a.invitation_id


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------
class TestDelete:
    def test_delete_returns_true(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        assert store.delete(inv.invitation_id) is True

    def test_delete_removes_from_get(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.delete(inv.invitation_id)
        assert store.get(inv.invitation_id) is None

    def test_delete_removes_from_doc_index(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.delete(inv.invitation_id)
        assert store.invitations_for_doc("d") == []

    def test_delete_removes_from_invitee_index(self):
        store = DocInvitationStore()
        inv = store.invite("d", "u", "a")
        store.delete(inv.invitation_id)
        assert store.invitations_for_invitee("u") == []

    def test_delete_unknown_returns_false(self):
        store = DocInvitationStore()
        assert store.delete("missing") is False

    def test_delete_one_keeps_others(self):
        store = DocInvitationStore()
        i1 = store.invite("d", "u1", "a")
        i2 = store.invite("d", "u2", "a")
        store.delete(i1.invitation_id)
        assert store.get(i2.invitation_id) is not None
        remaining = store.invitations_for_doc("d")
        assert len(remaining) == 1
        assert remaining[0].invitation_id == i2.invitation_id


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        store = DocInvitationStore()
        s = store.stats()
        assert s.total == 0

    def test_counts_pending(self):
        store = DocInvitationStore()
        store.invite("d", "u1", "a")
        store.invite("d", "u2", "a")
        s = store.stats()
        assert s.total == 2
        assert s.pending == 2

    def test_counts_accepted(self):
        store = DocInvitationStore()
        i1 = store.invite("d", "u1", "a")
        i2 = store.invite("d", "u2", "a")
        store.accept(i1.invitation_id)
        store.accept(i2.invitation_id)
        s = store.stats()
        assert s.accepted == 2
        assert s.pending == 0

    def test_counts_declined(self):
        store = DocInvitationStore()
        i = store.invite("d", "u", "a")
        store.decline(i.invitation_id)
        s = store.stats()
        assert s.declined == 1

    def test_counts_revoked(self):
        store = DocInvitationStore()
        i = store.invite("d", "u", "a")
        store.revoke(i.invitation_id)
        s = store.stats()
        assert s.revoked == 1

    def test_counts_expired(self):
        store = DocInvitationStore()
        store.invite("d", "u", "a", expires_at=10.0, now=5.0)
        store.expire_if_due(now=100.0)
        s = store.stats()
        assert s.expired == 1

    def test_mixed_counts(self):
        store = DocInvitationStore()
        i1 = store.invite("d", "u1", "a")
        i2 = store.invite("d", "u2", "a")
        i3 = store.invite("d", "u3", "a")
        i4 = store.invite("d", "u4", "a", expires_at=10.0, now=5.0)
        store.invite("d", "u5", "a")
        store.accept(i1.invitation_id)
        store.decline(i2.invitation_id)
        store.revoke(i3.invitation_id)
        store.expire_if_due(now=1000.0)
        s = store.stats()
        assert s.total == 5
        assert s.accepted == 1
        assert s.declined == 1
        assert s.revoked == 1
        assert s.expired == 1
        assert s.pending == 1


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------
class TestThreadSafety:
    def test_concurrent_invites(self):
        store = DocInvitationStore()
        N_THREADS = 8
        PER_THREAD = 25

        def worker(tid: int) -> None:
            for i in range(PER_THREAD):
                store.invite("d", f"u-{tid}-{i}", "admin")

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(N_THREADS)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        s = store.stats()
        assert s.total == N_THREADS * PER_THREAD
        assert s.pending == N_THREADS * PER_THREAD

    def test_concurrent_invites_unique_ids(self):
        store = DocInvitationStore()
        results: list[str] = []
        lock = threading.Lock()

        def worker() -> None:
            for _ in range(20):
                inv = store.invite("d", "u", "a")
                with lock:
                    results.append(inv.invitation_id)

        threads = [threading.Thread(target=worker) for _ in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert len(results) == len(set(results))
