"""Tests for ``docstoolkit.doc_share``."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_share import (
    AccessRecord,
    DocShare,
    PermissionLevel,
    ShareLink,
    ShareStats,
    ShareStatus,
)


# ---------------------------------------------------------------------------
# enums and dataclasses
# ---------------------------------------------------------------------------
class TestShareStatus:
    def test_members(self):
        assert ShareStatus.ACTIVE.value == "active"
        assert ShareStatus.EXPIRED.value == "expired"
        assert ShareStatus.REVOKED.value == "revoked"
        assert ShareStatus.EXHAUSTED.value == "exhausted"

    def test_count(self):
        assert len(list(ShareStatus)) == 4

    def test_distinct_values(self):
        values = {s.value for s in ShareStatus}
        assert len(values) == 4


class TestPermissionLevel:
    def test_members(self):
        assert PermissionLevel.VIEW.value == "view"
        assert PermissionLevel.COMMENT.value == "comment"
        assert PermissionLevel.EDIT.value == "edit"

    def test_count(self):
        assert len(list(PermissionLevel)) == 3


class TestShareLink:
    def test_defaults(self):
        link = ShareLink(
            share_id="s",
            doc_id="d",
            token="t",
            created_by="u",
            created_at=1.0,
        )
        assert link.expires_at is None
        assert link.max_uses is None
        assert link.use_count == 0
        assert link.password_hash is None
        assert link.permission is PermissionLevel.VIEW
        assert link.revoked is False

    def test_custom_fields(self):
        link = ShareLink(
            share_id="s",
            doc_id="d",
            token="t",
            created_by="u",
            created_at=1.0,
            expires_at=2.0,
            max_uses=5,
            permission=PermissionLevel.EDIT,
        )
        assert link.expires_at == 2.0
        assert link.max_uses == 5
        assert link.permission is PermissionLevel.EDIT


class TestAccessRecord:
    def test_defaults(self):
        rec = AccessRecord(share_id="s", accessed_at=1.0, succeeded=True)
        assert rec.reason is None

    def test_failure(self):
        rec = AccessRecord(share_id="s", accessed_at=1.0, succeeded=False, reason="x")
        assert not rec.succeeded
        assert rec.reason == "x"


class TestShareStats:
    def test_construct(self):
        s = ShareStats(
            total_shares=4,
            active=2,
            expired=1,
            revoked=0,
            exhausted=1,
            total_uses=7,
        )
        assert s.total_shares == 4
        assert s.total_uses == 7


# ---------------------------------------------------------------------------
# create_share
# ---------------------------------------------------------------------------
class TestCreateShare:
    def test_returns_share_link(self):
        ds = DocShare()
        link = ds.create_share("doc1", "alice", now=100.0)
        assert isinstance(link, ShareLink)
        assert link.doc_id == "doc1"
        assert link.created_by == "alice"
        assert link.created_at == 100.0

    def test_unique_ids(self):
        ds = DocShare()
        a = ds.create_share("d", "u", now=1.0)
        b = ds.create_share("d", "u", now=1.0)
        assert a.share_id != b.share_id
        assert a.token != b.token

    def test_token_is_urlsafe_and_long(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        # token_urlsafe(32) yields ~43 chars of URL-safe base64.
        assert len(link.token) >= 32
        assert all(c.isalnum() or c in "-_" for c in link.token)

    def test_default_permission(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert link.permission is PermissionLevel.VIEW

    def test_custom_permission(self):
        ds = DocShare()
        link = ds.create_share("d", "u", permission=PermissionLevel.EDIT, now=1.0)
        assert link.permission is PermissionLevel.EDIT

    def test_expires_and_max_uses(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=200.0, max_uses=3, now=1.0)
        assert link.expires_at == 200.0
        assert link.max_uses == 3
        assert link.use_count == 0

    def test_now_zero_uses_walltime(self):
        ds = DocShare()
        link = ds.create_share("d", "u")  # now=0.0
        assert link.created_at > 0

    def test_stored_in_manager(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.get_share(link.share_id) is link


class TestCreateShareWithPassword:
    def test_password_hashed(self):
        ds = DocShare(secret="pepper")
        link = ds.create_share("d", "u", password="open-sesame", now=1.0)
        assert link.password_hash is not None
        assert link.password_hash != "open-sesame"

    def test_no_password_means_no_hash(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert link.password_hash is None

    def test_different_secrets_yield_different_hashes(self):
        a = DocShare(secret="s1")
        b = DocShare(secret="s2")
        la = a.create_share("d", "u", password="pw", now=1.0)
        lb = b.create_share("d", "u", password="pw", now=1.0)
        assert la.password_hash != lb.password_hash


# ---------------------------------------------------------------------------
# revoke
# ---------------------------------------------------------------------------
class TestRevoke:
    def test_revoke_existing(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.revoke(link.share_id) is True
        assert ds.get_share(link.share_id).revoked is True

    def test_revoke_unknown(self):
        ds = DocShare()
        assert ds.revoke("missing") is False

    def test_revoke_twice(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.revoke(link.share_id)
        assert ds.revoke(link.share_id) is False


# ---------------------------------------------------------------------------
# access
# ---------------------------------------------------------------------------
class TestAccess:
    def test_access_returns_link_and_increments(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        got = ds.access(link.token, now=2.0)
        assert got is link
        assert link.use_count == 1

    def test_access_unknown_token(self):
        ds = DocShare()
        assert ds.access("bogus", now=1.0) is None

    def test_access_records_success(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.access(link.token, now=2.0)
        hist = ds.access_history(link.share_id)
        assert len(hist) == 1
        assert hist[0].succeeded is True

    def test_access_records_failure_for_unknown_token(self):
        ds = DocShare()
        ds.access("bogus", now=1.0)
        all_hist = ds.access_history()
        assert len(all_hist) == 1
        assert all_hist[0].succeeded is False
        assert all_hist[0].reason == "unknown_token"

    def test_repeated_access_counts(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        for i in range(5):
            ds.access(link.token, now=2.0 + i)
        assert link.use_count == 5


class TestAccessExpired:
    def test_expired_returns_none(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=100.0, now=1.0)
        assert ds.access(link.token, now=200.0) is None

    def test_expired_does_not_increment(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=100.0, now=1.0)
        ds.access(link.token, now=200.0)
        assert link.use_count == 0

    def test_expired_recorded(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=100.0, now=1.0)
        ds.access(link.token, now=200.0)
        hist = ds.access_history(link.share_id)
        assert hist[0].reason == "expired"


class TestAccessExhausted:
    def test_max_uses_consumed(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=2, now=1.0)
        assert ds.access(link.token, now=2.0) is link
        assert ds.access(link.token, now=3.0) is link
        assert ds.access(link.token, now=4.0) is None
        assert link.use_count == 2

    def test_exhausted_reason_logged(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=1, now=1.0)
        ds.access(link.token, now=2.0)
        ds.access(link.token, now=3.0)
        last = ds.access_history(link.share_id)[-1]
        assert last.reason == "exhausted"


class TestAccessWrongPassword:
    def test_wrong_password_rejected(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.access(link.token, password="other", now=2.0) is None

    def test_missing_password_rejected(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.access(link.token, now=2.0) is None
        last = ds.access_history(link.share_id)[-1]
        assert last.reason == "password_required"

    def test_wrong_password_does_not_increment(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        ds.access(link.token, password="bad", now=2.0)
        assert link.use_count == 0

    def test_correct_password_succeeds(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.access(link.token, password="pw", now=2.0) is link
        assert link.use_count == 1

    def test_wrong_password_logged(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        ds.access(link.token, password="bad", now=2.0)
        last = ds.access_history(link.share_id)[-1]
        assert last.reason == "wrong_password"
        assert not last.succeeded


class TestVerifyPassword:
    def test_correct(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.verify_password(link.share_id, "pw") is True

    def test_wrong(self):
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.verify_password(link.share_id, "no") is False

    def test_no_password_set(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.verify_password(link.share_id, "anything") is False

    def test_unknown_share(self):
        ds = DocShare()
        assert ds.verify_password("missing", "pw") is False


# ---------------------------------------------------------------------------
# lookups
# ---------------------------------------------------------------------------
class TestGetShare:
    def test_found(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.get_share(link.share_id) is link

    def test_missing(self):
        ds = DocShare()
        assert ds.get_share("none") is None


class TestGetByToken:
    def test_found(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.get_by_token(link.token) is link

    def test_missing(self):
        ds = DocShare()
        assert ds.get_by_token("bogus") is None


class TestStatusOf:
    def test_active(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.status_of(link.share_id, now=2.0) is ShareStatus.ACTIVE

    def test_expired(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=10.0, now=1.0)
        assert ds.status_of(link.share_id, now=20.0) is ShareStatus.EXPIRED

    def test_revoked(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.revoke(link.share_id)
        assert ds.status_of(link.share_id, now=2.0) is ShareStatus.REVOKED

    def test_exhausted(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=1, now=1.0)
        ds.access(link.token, now=2.0)
        assert ds.status_of(link.share_id, now=3.0) is ShareStatus.EXHAUSTED

    def test_unknown(self):
        ds = DocShare()
        assert ds.status_of("missing", now=1.0) is None

    def test_revoked_beats_expired(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=10.0, now=1.0)
        ds.revoke(link.share_id)
        assert ds.status_of(link.share_id, now=999.0) is ShareStatus.REVOKED


class TestSharesForDoc:
    def test_filters(self):
        ds = DocShare()
        a = ds.create_share("doc1", "u", now=1.0)
        b = ds.create_share("doc1", "u", now=1.0)
        ds.create_share("doc2", "u", now=1.0)
        ids = {s.share_id for s in ds.shares_for_doc("doc1")}
        assert ids == {a.share_id, b.share_id}

    def test_empty(self):
        ds = DocShare()
        assert ds.shares_for_doc("nope") == []


class TestSharesByCreator:
    def test_filters(self):
        ds = DocShare()
        a = ds.create_share("d", "alice", now=1.0)
        ds.create_share("d", "bob", now=1.0)
        out = ds.shares_by_creator("alice")
        assert [s.share_id for s in out] == [a.share_id]

    def test_empty(self):
        ds = DocShare()
        assert ds.shares_by_creator("nobody") == []


class TestAccessHistory:
    def test_full_history(self):
        ds = DocShare()
        a = ds.create_share("d", "u", now=1.0)
        b = ds.create_share("d", "u", now=1.0)
        ds.access(a.token, now=2.0)
        ds.access(b.token, now=3.0)
        assert len(ds.access_history()) == 2

    def test_filtered(self):
        ds = DocShare()
        a = ds.create_share("d", "u", now=1.0)
        b = ds.create_share("d", "u", now=1.0)
        ds.access(a.token, now=2.0)
        ds.access(b.token, now=3.0)
        only_a = ds.access_history(a.share_id)
        assert len(only_a) == 1
        assert only_a[0].share_id == a.share_id


# ---------------------------------------------------------------------------
# lifecycle
# ---------------------------------------------------------------------------
class TestCleanupExpired:
    def test_removes_expired(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=10.0, now=1.0)
        removed = ds.cleanup_expired(now=100.0)
        assert removed == 1
        assert ds.get_share(link.share_id) is None

    def test_removes_exhausted(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=1, now=1.0)
        ds.access(link.token, now=2.0)
        removed = ds.cleanup_expired(now=3.0)
        assert removed == 1

    def test_keeps_active(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.cleanup_expired(now=2.0) == 0
        assert ds.get_share(link.share_id) is link

    def test_keeps_revoked(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.revoke(link.share_id)
        assert ds.cleanup_expired(now=2.0) == 0
        assert ds.get_share(link.share_id) is not None

    def test_token_lookup_cleared(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=10.0, now=1.0)
        ds.cleanup_expired(now=100.0)
        assert ds.get_by_token(link.token) is None


class TestExtendExpiry:
    def test_extends_existing(self):
        ds = DocShare()
        link = ds.create_share("d", "u", expires_at=100.0, now=1.0)
        assert ds.extend_expiry(link.share_id, 50.0, now=2.0) is True
        assert link.expires_at == 150.0

    def test_adds_when_no_expiry(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.extend_expiry(link.share_id, 50.0, now=10.0) is True
        assert link.expires_at == 60.0

    def test_unknown(self):
        ds = DocShare()
        assert ds.extend_expiry("missing", 10.0, now=1.0) is False

    def test_revoked_cannot_extend(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.revoke(link.share_id)
        assert ds.extend_expiry(link.share_id, 10.0, now=2.0) is False


class TestChangePermission:
    def test_update(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        assert ds.change_permission(link.share_id, PermissionLevel.EDIT) is True
        assert link.permission is PermissionLevel.EDIT

    def test_unknown(self):
        ds = DocShare()
        assert ds.change_permission("missing", PermissionLevel.EDIT) is False


# ---------------------------------------------------------------------------
# aggregates
# ---------------------------------------------------------------------------
class TestStats:
    def test_empty(self):
        ds = DocShare()
        s = ds.stats()
        assert s.total_shares == 0
        assert s.active == 0
        assert s.total_uses == 0

    def test_mixed(self):
        ds = DocShare()
        active = ds.create_share("d", "u", now=1.0)
        expired = ds.create_share("d", "u", expires_at=10.0, now=1.0)
        exhausted = ds.create_share("d", "u", max_uses=1, now=1.0)
        revoked = ds.create_share("d", "u", now=1.0)
        ds.access(active.token, now=2.0)
        ds.access(exhausted.token, now=2.0)
        ds.revoke(revoked.share_id)
        s = ds.stats(now=100.0)
        assert s.total_shares == 4
        assert s.active == 1
        assert s.expired == 1
        assert s.exhausted == 1
        assert s.revoked == 1
        assert s.total_uses == 2
        # confirm at least one use came from each consumed share
        assert active.use_count == 1
        assert exhausted.use_count == 1


class TestTotalShares:
    def test_zero(self):
        ds = DocShare()
        assert ds.total_shares == 0

    def test_grows(self):
        ds = DocShare()
        ds.create_share("d", "u", now=1.0)
        ds.create_share("d", "u", now=1.0)
        assert ds.total_shares == 2


class TestClear:
    def test_clears_everything(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.access(link.token, now=2.0)
        ds.clear()
        assert ds.total_shares == 0
        assert ds.access_history() == []
        assert ds.get_by_token(link.token) is None


# ---------------------------------------------------------------------------
# edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_thread_safety(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=1000, now=1.0)

        def worker():
            for _ in range(100):
                ds.access(link.token, now=2.0)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert link.use_count == 1000

    def test_create_with_zero_now_uses_walltime(self):
        ds = DocShare()
        link = ds.create_share("d", "u")
        assert link.created_at > 0

    def test_password_with_empty_secret(self):
        ds = DocShare(secret="")
        link = ds.create_share("d", "u", password="pw", now=1.0)
        assert ds.verify_password(link.share_id, "pw") is True

    def test_max_uses_zero_immediately_exhausted(self):
        ds = DocShare()
        link = ds.create_share("d", "u", max_uses=0, now=1.0)
        assert ds.status_of(link.share_id, now=2.0) is ShareStatus.EXHAUSTED
        assert ds.access(link.token, now=2.0) is None

    def test_password_change_via_create_only(self):
        # Changing a password directly is not part of the public API; verify
        # that mutating the underlying record reflects via verify_password.
        ds = DocShare(secret="s")
        link = ds.create_share("d", "u", password="a", now=1.0)
        assert ds.verify_password(link.share_id, "a")
        assert not ds.verify_password(link.share_id, "b")

    def test_access_history_empty_initially(self):
        ds = DocShare()
        assert ds.access_history() == []

    def test_revoked_share_access_blocked(self):
        ds = DocShare()
        link = ds.create_share("d", "u", now=1.0)
        ds.revoke(link.share_id)
        assert ds.access(link.token, now=2.0) is None
        last = ds.access_history(link.share_id)[-1]
        assert last.reason == "revoked"
