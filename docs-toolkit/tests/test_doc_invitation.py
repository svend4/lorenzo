"""Tests for the doc_invitation module."""

from __future__ import annotations

import pytest

from docstoolkit.doc_invitation import (
    DocInvitation,
    Invitation,
    InviteRole,
    InviteStats,
    InviteStatus,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mgr() -> DocInvitation:
    return DocInvitation()


def _create(mgr: DocInvitation, **kwargs) -> Invitation:
    defaults = dict(
        doc_id="doc1",
        invitee_email="alice@example.com",
        inviter_id="bob",
        role=InviteRole.VIEWER,
        now=1000.0,
    )
    defaults.update(kwargs)
    return mgr.create_invite(**defaults)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TestInviteStatus:
    def test_all_members_present(self):
        names = {s.name for s in InviteStatus}
        assert names == {
            "PENDING",
            "ACCEPTED",
            "DECLINED",
            "EXPIRED",
            "REVOKED",
        }

    def test_values_are_strings(self):
        assert InviteStatus.PENDING.value == "pending"
        assert InviteStatus.ACCEPTED.value == "accepted"
        assert InviteStatus.DECLINED.value == "declined"
        assert InviteStatus.EXPIRED.value == "expired"
        assert InviteStatus.REVOKED.value == "revoked"


class TestInviteRole:
    def test_all_members_present(self):
        names = {r.name for r in InviteRole}
        assert names == {"VIEWER", "COMMENTER", "EDITOR", "ADMIN"}

    def test_values(self):
        assert InviteRole.VIEWER.value == "viewer"
        assert InviteRole.COMMENTER.value == "commenter"
        assert InviteRole.EDITOR.value == "editor"
        assert InviteRole.ADMIN.value == "admin"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestInvitation:
    def test_basic_construction(self):
        inv = Invitation(
            invite_id="inv_00000001",
            doc_id="doc1",
            invitee_email="x@y.z",
            inviter_id="u1",
            role=InviteRole.EDITOR,
            token="tok",
        )
        assert inv.invite_id == "inv_00000001"
        assert inv.status == InviteStatus.PENDING
        assert inv.created_at == 0.0
        assert inv.expires_at is None
        assert inv.accepted_at is None
        assert inv.accepted_by_user_id is None
        assert inv.message is None

    def test_full_construction(self):
        inv = Invitation(
            invite_id="x",
            doc_id="d",
            invitee_email="a@b",
            inviter_id="i",
            role=InviteRole.ADMIN,
            token="t",
            status=InviteStatus.ACCEPTED,
            created_at=1.0,
            expires_at=2.0,
            accepted_at=1.5,
            accepted_by_user_id="u",
            message="hi",
        )
        assert inv.status == InviteStatus.ACCEPTED
        assert inv.message == "hi"
        assert inv.accepted_by_user_id == "u"


class TestInviteStats:
    def test_defaults(self):
        s = InviteStats()
        assert s.total == 0
        assert s.pending == 0
        assert s.accepted == 0
        assert s.declined == 0
        assert s.expired == 0
        assert s.revoked == 0

    def test_acceptance_rate_zero(self):
        s = InviteStats()
        assert s.acceptance_rate == 0.0

    def test_acceptance_rate_nonzero(self):
        s = InviteStats(total=4, accepted=1)
        assert s.acceptance_rate == 0.25

    def test_acceptance_rate_all_accepted(self):
        s = InviteStats(total=3, accepted=3)
        assert s.acceptance_rate == 1.0


# ---------------------------------------------------------------------------
# create_invite
# ---------------------------------------------------------------------------


class TestCreateInvite:
    def test_returns_invitation(self, mgr):
        inv = _create(mgr)
        assert isinstance(inv, Invitation)

    def test_default_role_viewer(self, mgr):
        inv = _create(mgr)
        assert inv.role == InviteRole.VIEWER

    def test_custom_role(self, mgr):
        inv = _create(mgr, role=InviteRole.ADMIN)
        assert inv.role == InviteRole.ADMIN

    def test_status_is_pending(self, mgr):
        inv = _create(mgr)
        assert inv.status == InviteStatus.PENDING

    def test_token_is_generated(self, mgr):
        inv = _create(mgr)
        assert isinstance(inv.token, str)
        assert len(inv.token) >= 32

    def test_unique_ids(self, mgr):
        a = _create(mgr)
        b = _create(mgr)
        assert a.invite_id != b.invite_id

    def test_unique_tokens(self, mgr):
        a = _create(mgr)
        b = _create(mgr)
        assert a.token != b.token

    def test_invite_id_pattern(self, mgr):
        inv = _create(mgr)
        assert inv.invite_id.startswith("inv_")

    def test_created_at_recorded(self, mgr):
        inv = _create(mgr, now=42.5)
        assert inv.created_at == 42.5

    def test_expires_at_recorded(self, mgr):
        inv = _create(mgr, expires_at=99.0)
        assert inv.expires_at == 99.0

    def test_message_recorded(self, mgr):
        inv = _create(mgr, message="Welcome")
        assert inv.message == "Welcome"

    def test_increments_total(self, mgr):
        assert mgr.total_invites == 0
        _create(mgr)
        assert mgr.total_invites == 1


# ---------------------------------------------------------------------------
# accept
# ---------------------------------------------------------------------------


class TestAccept:
    def test_accept_pending(self, mgr):
        inv = _create(mgr)
        result = mgr.accept(inv.token, user_id="u42", now=1100.0)
        assert result is not None
        assert result.status == InviteStatus.ACCEPTED

    def test_accept_sets_accepted_at(self, mgr):
        inv = _create(mgr)
        result = mgr.accept(inv.token, user_id="u42", now=1100.0)
        assert result.accepted_at == 1100.0

    def test_accept_sets_user_id(self, mgr):
        inv = _create(mgr)
        result = mgr.accept(inv.token, user_id="u42", now=1100.0)
        assert result.accepted_by_user_id == "u42"

    def test_unknown_token(self, mgr):
        assert mgr.accept("nope", user_id="u", now=0.0) is None

    def test_accept_persists(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        fetched = mgr.get_invite(inv.invite_id)
        assert fetched.status == InviteStatus.ACCEPTED


class TestAcceptExpired:
    def test_accept_after_expiry_fails(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        assert mgr.accept(inv.token, user_id="u", now=1600.0) is None

    def test_accept_after_expiry_marks_expired(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        mgr.accept(inv.token, user_id="u", now=1600.0)
        assert mgr.get_invite(inv.invite_id).status == InviteStatus.EXPIRED

    def test_accept_exactly_at_expiry(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        assert mgr.accept(inv.token, user_id="u", now=1500.0) is None

    def test_accept_before_expiry_ok(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        result = mgr.accept(inv.token, user_id="u", now=1499.0)
        assert result is not None
        assert result.status == InviteStatus.ACCEPTED


class TestAcceptAlreadyAccepted:
    def test_double_accept_returns_none(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u1", now=1100.0)
        assert mgr.accept(inv.token, user_id="u2", now=1200.0) is None

    def test_accept_after_decline_fails(self, mgr):
        inv = _create(mgr)
        mgr.decline(inv.token, now=1100.0)
        assert mgr.accept(inv.token, user_id="u", now=1200.0) is None

    def test_accept_after_revoke_fails(self, mgr):
        inv = _create(mgr)
        mgr.revoke(inv.invite_id)
        assert mgr.accept(inv.token, user_id="u", now=1100.0) is None


# ---------------------------------------------------------------------------
# decline
# ---------------------------------------------------------------------------


class TestDecline:
    def test_decline_pending(self, mgr):
        inv = _create(mgr)
        result = mgr.decline(inv.token, now=1100.0)
        assert result is not None
        assert result.status == InviteStatus.DECLINED

    def test_unknown_token(self, mgr):
        assert mgr.decline("nope", now=0.0) is None

    def test_double_decline(self, mgr):
        inv = _create(mgr)
        mgr.decline(inv.token, now=1100.0)
        assert mgr.decline(inv.token, now=1200.0) is None

    def test_decline_after_accept(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        assert mgr.decline(inv.token, now=1200.0) is None

    def test_decline_expired_fails(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        assert mgr.decline(inv.token, now=1600.0) is None
        assert mgr.get_invite(inv.invite_id).status == InviteStatus.EXPIRED


# ---------------------------------------------------------------------------
# revoke
# ---------------------------------------------------------------------------


class TestRevoke:
    def test_revoke_pending(self, mgr):
        inv = _create(mgr)
        assert mgr.revoke(inv.invite_id) is True
        assert mgr.get_invite(inv.invite_id).status == InviteStatus.REVOKED

    def test_revoke_unknown(self, mgr):
        assert mgr.revoke("nope") is False

    def test_revoke_accepted_fails(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        assert mgr.revoke(inv.invite_id) is False

    def test_revoke_already_revoked(self, mgr):
        inv = _create(mgr)
        mgr.revoke(inv.invite_id)
        assert mgr.revoke(inv.invite_id) is False


# ---------------------------------------------------------------------------
# expire_overdue
# ---------------------------------------------------------------------------


class TestExpireOverdue:
    def test_no_expires_no_effect(self, mgr):
        _create(mgr)
        assert mgr.expire_overdue(now=9999.0) == 0

    def test_expires_in_future(self, mgr):
        _create(mgr, expires_at=2000.0)
        assert mgr.expire_overdue(now=1500.0) == 0

    def test_expires_at_now(self, mgr):
        _create(mgr, expires_at=2000.0)
        assert mgr.expire_overdue(now=2000.0) == 1

    def test_expires_past(self, mgr):
        _create(mgr, expires_at=1500.0)
        assert mgr.expire_overdue(now=1600.0) == 1

    def test_only_pending_affected(self, mgr):
        a = _create(mgr, expires_at=1500.0)
        b = _create(mgr, expires_at=1500.0)
        mgr.accept(a.token, user_id="u", now=1100.0)
        # b stays pending, will expire; a is accepted, untouched
        count = mgr.expire_overdue(now=2000.0)
        assert count == 1
        assert mgr.get_invite(a.invite_id).status == InviteStatus.ACCEPTED
        assert mgr.get_invite(b.invite_id).status == InviteStatus.EXPIRED

    def test_multiple_expirations(self, mgr):
        for _ in range(5):
            _create(mgr, expires_at=1500.0)
        assert mgr.expire_overdue(now=2000.0) == 5


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------


class TestGetInvite:
    def test_existing(self, mgr):
        inv = _create(mgr)
        assert mgr.get_invite(inv.invite_id) is inv

    def test_missing(self, mgr):
        assert mgr.get_invite("nope") is None


class TestGetByToken:
    def test_existing(self, mgr):
        inv = _create(mgr)
        assert mgr.get_by_token(inv.token).invite_id == inv.invite_id

    def test_missing(self, mgr):
        assert mgr.get_by_token("nope") is None


class TestInvitesForDoc:
    def test_filter_by_doc(self, mgr):
        a = _create(mgr, doc_id="doc1")
        b = _create(mgr, doc_id="doc2")
        c = _create(mgr, doc_id="doc1")
        result = mgr.invites_for_doc("doc1")
        ids = {i.invite_id for i in result}
        assert ids == {a.invite_id, c.invite_id}

    def test_filter_by_doc_and_status(self, mgr):
        a = _create(mgr, doc_id="doc1")
        b = _create(mgr, doc_id="doc1")
        mgr.accept(a.token, user_id="u", now=1100.0)
        result = mgr.invites_for_doc(
            "doc1", status=InviteStatus.PENDING
        )
        assert [i.invite_id for i in result] == [b.invite_id]

    def test_empty(self, mgr):
        assert mgr.invites_for_doc("nope") == []


class TestInvitesForEmail:
    def test_filter_by_email(self, mgr):
        a = _create(mgr, invitee_email="x@x")
        b = _create(mgr, invitee_email="y@y")
        result = mgr.invites_for_email("x@x")
        assert [i.invite_id for i in result] == [a.invite_id]

    def test_filter_by_email_and_status(self, mgr):
        a = _create(mgr, invitee_email="x@x")
        b = _create(mgr, invitee_email="x@x")
        mgr.revoke(a.invite_id)
        result = mgr.invites_for_email(
            "x@x", status=InviteStatus.REVOKED
        )
        assert [i.invite_id for i in result] == [a.invite_id]

    def test_empty(self, mgr):
        assert mgr.invites_for_email("none@none") == []


class TestInvitesByInviter:
    def test_filter(self, mgr):
        a = _create(mgr, inviter_id="bob")
        b = _create(mgr, inviter_id="alice")
        c = _create(mgr, inviter_id="bob")
        result = mgr.invites_by_inviter("bob")
        ids = {i.invite_id for i in result}
        assert ids == {a.invite_id, c.invite_id}

    def test_empty(self, mgr):
        assert mgr.invites_by_inviter("none") == []


class TestPendingInvites:
    def test_only_pending_returned(self, mgr):
        a = _create(mgr)
        b = _create(mgr)
        mgr.accept(a.token, user_id="u", now=1100.0)
        pending = mgr.pending_invites(now=1200.0)
        assert [i.invite_id for i in pending] == [b.invite_id]

    def test_excludes_expired(self, mgr):
        a = _create(mgr, expires_at=1500.0)
        b = _create(mgr, expires_at=3000.0)
        pending = mgr.pending_invites(now=2000.0)
        assert [i.invite_id for i in pending] == [b.invite_id]

    def test_empty(self, mgr):
        assert mgr.pending_invites(now=0.0) == []


# ---------------------------------------------------------------------------
# resend
# ---------------------------------------------------------------------------


class TestResend:
    def test_resend_pending(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        assert mgr.resend(inv.invite_id, new_expires_at=5000.0) is True
        assert mgr.get_invite(inv.invite_id).expires_at == 5000.0

    def test_resend_unknown(self, mgr):
        assert mgr.resend("nope") is False

    def test_resend_accepted_fails(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        assert mgr.resend(inv.invite_id, new_expires_at=5000.0) is False

    def test_resend_clear_expiry(self, mgr):
        inv = _create(mgr, expires_at=1500.0)
        mgr.resend(inv.invite_id, new_expires_at=None)
        assert mgr.get_invite(inv.invite_id).expires_at is None


# ---------------------------------------------------------------------------
# change_role
# ---------------------------------------------------------------------------


class TestChangeRole:
    def test_change_pending(self, mgr):
        inv = _create(mgr, role=InviteRole.VIEWER)
        assert mgr.change_role(inv.invite_id, InviteRole.EDITOR) is True
        assert mgr.get_invite(inv.invite_id).role == InviteRole.EDITOR

    def test_change_unknown(self, mgr):
        assert mgr.change_role("nope", InviteRole.EDITOR) is False

    def test_change_accepted_fails(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        assert mgr.change_role(inv.invite_id, InviteRole.ADMIN) is False

    def test_change_revoked_fails(self, mgr):
        inv = _create(mgr)
        mgr.revoke(inv.invite_id)
        assert mgr.change_role(inv.invite_id, InviteRole.ADMIN) is False


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self, mgr):
        s = mgr.stats()
        assert s.total == 0
        assert s.acceptance_rate == 0.0

    def test_mixed(self, mgr):
        a = _create(mgr)
        b = _create(mgr)
        c = _create(mgr)
        d = _create(mgr)
        e = _create(mgr, expires_at=1500.0)
        mgr.accept(a.token, user_id="u", now=1100.0)
        mgr.decline(b.token, now=1100.0)
        mgr.revoke(c.invite_id)
        mgr.expire_overdue(now=2000.0)
        # d remains pending
        s = mgr.stats()
        assert s.total == 5
        assert s.accepted == 1
        assert s.declined == 1
        assert s.revoked == 1
        assert s.expired == 1
        assert s.pending == 1

    def test_returns_new_object(self, mgr):
        s1 = mgr.stats()
        s2 = mgr.stats()
        assert s1 is not s2


class TestAcceptanceRate:
    def test_after_accepts(self, mgr):
        a = _create(mgr)
        b = _create(mgr)
        c = _create(mgr)
        d = _create(mgr)
        mgr.accept(a.token, user_id="u", now=1100.0)
        mgr.accept(b.token, user_id="u", now=1100.0)
        assert mgr.stats().acceptance_rate == 0.5

    def test_zero_when_empty(self, mgr):
        assert mgr.stats().acceptance_rate == 0.0


# ---------------------------------------------------------------------------
# total_invites & clear
# ---------------------------------------------------------------------------


class TestTotalInvites:
    def test_zero(self, mgr):
        assert mgr.total_invites == 0

    def test_grows(self, mgr):
        for i in range(7):
            _create(mgr)
        assert mgr.total_invites == 7

    def test_includes_terminal_invites(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        assert mgr.total_invites == 1


class TestClear:
    def test_clear_empties(self, mgr):
        _create(mgr)
        _create(mgr)
        mgr.clear()
        assert mgr.total_invites == 0

    def test_clear_resets_counter(self, mgr):
        _create(mgr)
        mgr.clear()
        inv = _create(mgr)
        assert inv.invite_id == "inv_00000001"

    def test_clear_invalidates_tokens(self, mgr):
        inv = _create(mgr)
        mgr.clear()
        assert mgr.get_by_token(inv.token) is None


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_accept_unknown_token(self, mgr):
        assert mgr.accept("zzz", user_id="u", now=0.0) is None

    def test_token_uniqueness_many(self, mgr):
        tokens = {_create(mgr).token for _ in range(50)}
        assert len(tokens) == 50

    def test_invite_id_sequence(self, mgr):
        ids = [_create(mgr).invite_id for _ in range(3)]
        assert ids == ["inv_00000001", "inv_00000002", "inv_00000003"]

    def test_expire_overdue_idempotent(self, mgr):
        _create(mgr, expires_at=1500.0)
        first = mgr.expire_overdue(now=2000.0)
        second = mgr.expire_overdue(now=2000.0)
        assert first == 1
        assert second == 0

    def test_get_by_token_after_status_change(self, mgr):
        inv = _create(mgr)
        mgr.accept(inv.token, user_id="u", now=1100.0)
        # token should still resolve to the same invite
        assert mgr.get_by_token(inv.token).invite_id == inv.invite_id

    def test_same_email_multiple_docs(self, mgr):
        _create(mgr, doc_id="d1", invitee_email="x@x")
        _create(mgr, doc_id="d2", invitee_email="x@x")
        assert len(mgr.invites_for_email("x@x")) == 2
