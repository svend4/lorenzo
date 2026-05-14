"""Tests for docstoolkit.doc_session (E232)."""

from __future__ import annotations

import pytest

from docstoolkit.doc_session import DocSession, Session, SessionStats, SessionStatus


# ---------------------------------------------------------------------------
# SessionStatus
# ---------------------------------------------------------------------------
class TestSessionStatus:
    def test_values(self):
        assert SessionStatus.ACTIVE.value == "active"
        assert SessionStatus.IDLE.value == "idle"
        assert SessionStatus.EXPIRED.value == "expired"
        assert SessionStatus.REVOKED.value == "revoked"

    def test_distinct_members(self):
        members = {SessionStatus.ACTIVE, SessionStatus.IDLE,
                   SessionStatus.EXPIRED, SessionStatus.REVOKED}
        assert len(members) == 4


# ---------------------------------------------------------------------------
# Session dataclass
# ---------------------------------------------------------------------------
class TestSession:
    def test_construct_with_required_fields(self):
        s = Session(
            session_id="sid",
            user_id="u1",
            created_at=1.0,
            last_activity=1.0,
            expires_at=10.0,
        )
        assert s.session_id == "sid"
        assert s.user_id == "u1"
        assert s.status == SessionStatus.ACTIVE
        assert s.data == {}
        assert s.roles == set()

    def test_default_data_and_roles_independent(self):
        a = Session("a", "u", 0.0, 0.0, 1.0)
        b = Session("b", "u", 0.0, 0.0, 1.0)
        a.data["x"] = 1
        a.roles.add("admin")
        assert b.data == {}
        assert b.roles == set()


# ---------------------------------------------------------------------------
# SessionStats dataclass
# ---------------------------------------------------------------------------
class TestSessionStats:
    def test_construct(self):
        stats = SessionStats(total=5, active=2, idle=1, expired=1,
                             revoked=1, unique_users=3)
        assert stats.total == 5
        assert stats.active == 2
        assert stats.idle == 1
        assert stats.expired == 1
        assert stats.revoked == 1
        assert stats.unique_users == 3


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------
class TestCreate:
    def test_basic_create(self):
        m = DocSession(default_ttl=100, idle_after=50)
        s = m.create("alice", now=1000.0)
        assert s.user_id == "alice"
        assert s.created_at == 1000.0
        assert s.last_activity == 1000.0
        assert s.expires_at == 1100.0
        assert s.status == SessionStatus.ACTIVE

    def test_create_unique_ids(self):
        m = DocSession()
        s1 = m.create("u")
        s2 = m.create("u")
        assert s1.session_id != s2.session_id

    def test_custom_ttl(self):
        m = DocSession(default_ttl=100)
        s = m.create("alice", ttl=500, now=10.0)
        assert s.expires_at == 510.0

    def test_with_roles(self):
        m = DocSession()
        s = m.create("alice", roles={"admin", "editor"})
        assert s.roles == {"admin", "editor"}

    def test_with_data(self):
        m = DocSession()
        s = m.create("alice", data={"ip": "127.0.0.1"})
        assert s.data == {"ip": "127.0.0.1"}

    def test_create_independent_data_dict(self):
        m = DocSession()
        d = {"key": "value"}
        s = m.create("alice", data=d)
        d["key"] = "other"
        assert s.data["key"] == "value"


# ---------------------------------------------------------------------------
# Get
# ---------------------------------------------------------------------------
class TestGet:
    def test_get_existing(self):
        m = DocSession(default_ttl=100, idle_after=50)
        s = m.create("u", now=1000.0)
        fetched = m.get(s.session_id, now=1010.0)
        assert fetched is not None
        assert fetched.session_id == s.session_id

    def test_get_missing(self):
        m = DocSession()
        assert m.get("nonexistent") is None

    def test_get_updates_last_activity(self):
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=1000.0)
        m.get(s.session_id, now=1050.0)
        peeked = m.peek(s.session_id, now=1050.0)
        assert peeked.last_activity == 1050.0

    def test_get_returns_idle_then_revives(self):
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=1000.0)
        # Peek at idle time
        idle_peek = m.peek(s.session_id, now=1200.0)
        assert idle_peek.status == SessionStatus.IDLE
        # get() during idle reactivates
        got = m.get(s.session_id, now=1201.0)
        assert got.status == SessionStatus.ACTIVE
        assert got.last_activity == 1201.0

    def test_get_expired_does_not_touch(self):
        m = DocSession(default_ttl=100, idle_after=50)
        s = m.create("u", now=1000.0)
        got = m.get(s.session_id, now=2000.0)
        assert got is not None
        assert got.status == SessionStatus.EXPIRED
        assert got.last_activity == 1000.0

    def test_get_revoked_does_not_touch(self):
        m = DocSession()
        s = m.create("u", now=0.0)
        m.revoke(s.session_id)
        got = m.get(s.session_id, now=10.0)
        assert got is not None
        assert got.status == SessionStatus.REVOKED
        assert got.last_activity == 0.0


# ---------------------------------------------------------------------------
# Peek
# ---------------------------------------------------------------------------
class TestPeek:
    def test_peek_no_update(self):
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=0.0)
        p = m.peek(s.session_id, now=50.0)
        assert p.last_activity == 0.0
        assert p.status == SessionStatus.ACTIVE

    def test_peek_missing(self):
        m = DocSession()
        assert m.peek("missing") is None

    def test_peek_idle_status(self):
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=0.0)
        p = m.peek(s.session_id, now=200.0)
        assert p.status == SessionStatus.IDLE

    def test_peek_expired_status(self):
        m = DocSession(default_ttl=100, idle_after=50)
        s = m.create("u", now=0.0)
        p = m.peek(s.session_id, now=200.0)
        assert p.status == SessionStatus.EXPIRED


# ---------------------------------------------------------------------------
# Touch
# ---------------------------------------------------------------------------
class TestTouch:
    def test_touch_updates_activity(self):
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=0.0)
        assert m.touch(s.session_id, now=50.0) is True
        assert m.peek(s.session_id, now=50.0).last_activity == 50.0

    def test_touch_missing(self):
        m = DocSession()
        assert m.touch("missing", now=1.0) is False

    def test_touch_revoked(self):
        m = DocSession()
        s = m.create("u", now=0.0)
        m.revoke(s.session_id)
        assert m.touch(s.session_id, now=10.0) is False

    def test_touch_expired(self):
        m = DocSession(default_ttl=10)
        s = m.create("u", now=0.0)
        assert m.touch(s.session_id, now=100.0) is False


# ---------------------------------------------------------------------------
# Revoke
# ---------------------------------------------------------------------------
class TestRevoke:
    def test_revoke_existing(self):
        m = DocSession()
        s = m.create("u")
        assert m.revoke(s.session_id) is True
        assert m.peek(s.session_id).status == SessionStatus.REVOKED

    def test_revoke_missing(self):
        m = DocSession()
        assert m.revoke("missing") is False

    def test_revoke_twice(self):
        m = DocSession()
        s = m.create("u")
        m.revoke(s.session_id)
        assert m.revoke(s.session_id) is False


# ---------------------------------------------------------------------------
# RevokeUser
# ---------------------------------------------------------------------------
class TestRevokeUser:
    def test_revokes_all_user_sessions(self):
        m = DocSession()
        a = m.create("alice")
        b = m.create("alice")
        c = m.create("bob")
        count = m.revoke_user("alice")
        assert count == 2
        assert m.peek(a.session_id).status == SessionStatus.REVOKED
        assert m.peek(b.session_id).status == SessionStatus.REVOKED
        assert m.peek(c.session_id).status == SessionStatus.ACTIVE

    def test_revoke_user_no_sessions(self):
        m = DocSession()
        assert m.revoke_user("ghost") == 0

    def test_revoke_user_skips_already_revoked(self):
        m = DocSession()
        a = m.create("alice")
        m.revoke(a.session_id)
        b = m.create("alice")
        count = m.revoke_user("alice")
        assert count == 1
        assert m.peek(b.session_id).status == SessionStatus.REVOKED


# ---------------------------------------------------------------------------
# Extend
# ---------------------------------------------------------------------------
class TestExtend:
    def test_extend_success(self):
        m = DocSession(default_ttl=100)
        s = m.create("u", now=0.0)
        assert m.extend(s.session_id, additional_ttl=200, now=50.0) is True
        assert m.peek(s.session_id, now=50.0).expires_at == 300.0

    def test_extend_missing(self):
        m = DocSession()
        assert m.extend("missing", 100.0) is False

    def test_extend_revoked(self):
        m = DocSession()
        s = m.create("u")
        m.revoke(s.session_id)
        assert m.extend(s.session_id, 100.0) is False

    def test_extend_expired(self):
        m = DocSession(default_ttl=10)
        s = m.create("u", now=0.0)
        assert m.extend(s.session_id, 100.0, now=100.0) is False


# ---------------------------------------------------------------------------
# UpdateData
# ---------------------------------------------------------------------------
class TestUpdateData:
    def test_update_merges(self):
        m = DocSession()
        s = m.create("u", data={"a": 1})
        assert m.update_data(s.session_id, {"b": 2}) is True
        assert m.peek(s.session_id).data == {"a": 1, "b": 2}

    def test_update_overwrites_existing_key(self):
        m = DocSession()
        s = m.create("u", data={"a": 1})
        m.update_data(s.session_id, {"a": 2})
        assert m.peek(s.session_id).data["a"] == 2

    def test_update_missing(self):
        m = DocSession()
        assert m.update_data("missing", {"x": 1}) is False

    def test_update_revoked(self):
        m = DocSession()
        s = m.create("u")
        m.revoke(s.session_id)
        assert m.update_data(s.session_id, {"x": 1}) is False


# ---------------------------------------------------------------------------
# AddRole
# ---------------------------------------------------------------------------
class TestAddRole:
    def test_add_role(self):
        m = DocSession()
        s = m.create("u")
        assert m.add_role(s.session_id, "admin") is True
        assert "admin" in m.peek(s.session_id).roles

    def test_add_role_idempotent(self):
        m = DocSession()
        s = m.create("u")
        m.add_role(s.session_id, "admin")
        m.add_role(s.session_id, "admin")
        assert m.peek(s.session_id).roles == {"admin"}

    def test_add_role_missing(self):
        m = DocSession()
        assert m.add_role("missing", "admin") is False

    def test_add_role_revoked(self):
        m = DocSession()
        s = m.create("u")
        m.revoke(s.session_id)
        assert m.add_role(s.session_id, "admin") is False


# ---------------------------------------------------------------------------
# RemoveRole
# ---------------------------------------------------------------------------
class TestRemoveRole:
    def test_remove_role(self):
        m = DocSession()
        s = m.create("u", roles={"admin", "editor"})
        assert m.remove_role(s.session_id, "admin") is True
        assert m.peek(s.session_id).roles == {"editor"}

    def test_remove_nonexistent_role(self):
        m = DocSession()
        s = m.create("u", roles={"admin"})
        assert m.remove_role(s.session_id, "editor") is False

    def test_remove_role_missing_session(self):
        m = DocSession()
        assert m.remove_role("missing", "admin") is False

    def test_remove_role_revoked(self):
        m = DocSession()
        s = m.create("u", roles={"admin"})
        m.revoke(s.session_id)
        assert m.remove_role(s.session_id, "admin") is False


# ---------------------------------------------------------------------------
# HasRole
# ---------------------------------------------------------------------------
class TestHasRole:
    def test_has_role_true(self):
        m = DocSession()
        s = m.create("u", roles={"admin"})
        assert m.has_role(s.session_id, "admin") is True

    def test_has_role_false(self):
        m = DocSession()
        s = m.create("u", roles={"admin"})
        assert m.has_role(s.session_id, "editor") is False

    def test_has_role_missing_session(self):
        m = DocSession()
        assert m.has_role("missing", "admin") is False


# ---------------------------------------------------------------------------
# SessionsForUser
# ---------------------------------------------------------------------------
class TestSessionsForUser:
    def test_returns_only_user_sessions(self):
        m = DocSession()
        a1 = m.create("alice")
        a2 = m.create("alice")
        m.create("bob")
        ids = {s.session_id for s in m.sessions_for_user("alice")}
        assert ids == {a1.session_id, a2.session_id}

    def test_empty_for_unknown_user(self):
        m = DocSession()
        assert m.sessions_for_user("ghost") == []

    def test_includes_revoked_and_expired(self):
        m = DocSession(default_ttl=10)
        a = m.create("alice", now=0.0)
        b = m.create("alice", now=0.0)
        m.revoke(a.session_id)
        result = m.sessions_for_user("alice", now=100.0)
        statuses = {s.status for s in result}
        assert SessionStatus.REVOKED in statuses
        assert SessionStatus.EXPIRED in statuses
        assert len(result) == 2
        # silence linter on b
        assert b is not None


# ---------------------------------------------------------------------------
# ActiveSessions
# ---------------------------------------------------------------------------
class TestActiveSessions:
    def test_returns_only_active(self):
        m = DocSession(default_ttl=100, idle_after=50)
        a = m.create("u1", now=0.0)
        b = m.create("u2", now=0.0)
        m.revoke(b.session_id)
        result = m.active_sessions(now=10.0)
        assert [s.session_id for s in result] == [a.session_id]

    def test_empty_when_none(self):
        m = DocSession()
        assert m.active_sessions() == []

    def test_idle_excluded(self):
        m = DocSession(default_ttl=1000, idle_after=10)
        m.create("u", now=0.0)
        assert m.active_sessions(now=100.0) == []


# ---------------------------------------------------------------------------
# IdleSessions
# ---------------------------------------------------------------------------
class TestIdleSessions:
    def test_returns_only_idle(self):
        m = DocSession(default_ttl=1000, idle_after=10)
        a = m.create("u1", now=0.0)
        m.create("u2", now=99.0)  # still active
        result = m.idle_sessions(now=100.0)
        assert [s.session_id for s in result] == [a.session_id]

    def test_empty_when_none(self):
        m = DocSession()
        assert m.idle_sessions() == []


# ---------------------------------------------------------------------------
# ExpiredSessions
# ---------------------------------------------------------------------------
class TestExpiredSessions:
    def test_returns_only_expired(self):
        m = DocSession(default_ttl=10)
        a = m.create("u1", now=0.0)
        m.create("u2", now=200.0)
        result = m.expired_sessions(now=100.0)
        assert [s.session_id for s in result] == [a.session_id]

    def test_revoked_not_counted_as_expired(self):
        m = DocSession(default_ttl=10)
        s = m.create("u", now=0.0)
        m.revoke(s.session_id)
        assert m.expired_sessions(now=100.0) == []


# ---------------------------------------------------------------------------
# CleanupExpired
# ---------------------------------------------------------------------------
class TestCleanupExpired:
    def test_removes_expired(self):
        m = DocSession(default_ttl=10)
        a = m.create("u1", now=0.0)
        b = m.create("u2", now=0.0)
        c = m.create("u3", now=200.0)
        count = m.cleanup_expired(now=100.0)
        assert count == 2
        assert m.peek(a.session_id, now=100.0) is None
        assert m.peek(b.session_id, now=100.0) is None
        assert m.peek(c.session_id, now=100.0) is not None

    def test_keeps_revoked(self):
        m = DocSession(default_ttl=10)
        s = m.create("u", now=0.0)
        m.revoke(s.session_id)
        count = m.cleanup_expired(now=100.0)
        assert count == 0
        assert m.peek(s.session_id, now=100.0) is not None

    def test_no_expired(self):
        m = DocSession(default_ttl=1000)
        m.create("u", now=0.0)
        assert m.cleanup_expired(now=10.0) == 0


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------
class TestStats:
    def test_stats_distribution(self):
        m = DocSession(default_ttl=100, idle_after=50)
        m.create("alice", now=0.0)               # ACTIVE at now=10
        m.create("bob", now=-60.0)               # IDLE at now=10 (last_activity=-60)
        m.create("carol", now=-200.0)            # EXPIRED at now=10
        d = m.create("dave", now=0.0)
        m.revoke(d.session_id)                   # REVOKED
        stats = m.stats(now=10.0)
        assert stats.total == 4
        assert stats.active == 1
        assert stats.idle == 1
        assert stats.expired == 1
        assert stats.revoked == 1
        assert stats.unique_users == 4

    def test_stats_empty(self):
        m = DocSession()
        stats = m.stats()
        assert stats.total == 0
        assert stats.active == 0
        assert stats.unique_users == 0

    def test_unique_users_dedup(self):
        m = DocSession()
        m.create("alice")
        m.create("alice")
        m.create("bob")
        stats = m.stats()
        assert stats.unique_users == 2


# ---------------------------------------------------------------------------
# SessionCount
# ---------------------------------------------------------------------------
class TestSessionCount:
    def test_count_active(self):
        m = DocSession(default_ttl=100, idle_after=50)
        m.create("u1", now=0.0)
        m.create("u2", now=0.0)
        assert m.session_count(now=10.0) == 2

    def test_count_excludes_idle(self):
        m = DocSession(default_ttl=1000, idle_after=10)
        m.create("u", now=0.0)
        assert m.session_count(now=100.0) == 0

    def test_count_excludes_revoked(self):
        m = DocSession()
        s = m.create("u")
        m.revoke(s.session_id)
        assert m.session_count() == 0


# ---------------------------------------------------------------------------
# TotalSessions
# ---------------------------------------------------------------------------
class TestTotalSessions:
    def test_total_includes_all(self):
        m = DocSession(default_ttl=10)
        m.create("u1", now=0.0)
        s2 = m.create("u2", now=0.0)
        m.revoke(s2.session_id)
        m.create("u3", now=0.0)
        assert m.total_sessions == 3

    def test_total_empty(self):
        assert DocSession().total_sessions == 0


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_removes_all(self):
        m = DocSession()
        m.create("u1")
        m.create("u2")
        m.clear()
        assert m.total_sessions == 0

    def test_clear_empty(self):
        m = DocSession()
        m.clear()
        assert m.total_sessions == 0


# ---------------------------------------------------------------------------
# EdgeCases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_boundary_idle(self):
        # Exactly at idle_after threshold -> IDLE
        m = DocSession(default_ttl=1000, idle_after=100)
        s = m.create("u", now=0.0)
        assert m.peek(s.session_id, now=100.0).status == SessionStatus.IDLE

    def test_boundary_expired(self):
        # Exactly at expires_at -> EXPIRED
        m = DocSession(default_ttl=100, idle_after=50)
        s = m.create("u", now=0.0)
        assert m.peek(s.session_id, now=100.0).status == SessionStatus.EXPIRED

    def test_revoked_then_check_status(self):
        m = DocSession(default_ttl=100)
        s = m.create("u", now=0.0)
        m.revoke(s.session_id)
        # Even when time passes far beyond expiry, status stays REVOKED
        assert m.peek(s.session_id, now=99999.0).status == SessionStatus.REVOKED

    def test_get_after_cleanup(self):
        m = DocSession(default_ttl=10)
        s = m.create("u", now=0.0)
        m.cleanup_expired(now=100.0)
        assert m.get(s.session_id, now=100.0) is None

    def test_zero_ttl(self):
        m = DocSession()
        s = m.create("u", ttl=0, now=0.0)
        assert m.peek(s.session_id, now=0.0).status == SessionStatus.EXPIRED

    def test_session_count_after_clear(self):
        m = DocSession()
        m.create("u")
        m.clear()
        assert m.session_count() == 0

    def test_extend_keeps_session_findable(self):
        m = DocSession(default_ttl=50)
        s = m.create("u", now=0.0)
        m.extend(s.session_id, 100.0, now=10.0)
        # Without extension, at now=80 the session would be expired
        assert m.peek(s.session_id, now=80.0).status != SessionStatus.EXPIRED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
