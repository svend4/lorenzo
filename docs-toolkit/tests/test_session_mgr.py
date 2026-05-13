"""Tests for docstoolkit.session_mgr (E68).

Covers:
- Session dataclass: is_expired, touch, get/set
- SessionStore (SQLite): create, get, touch, invalidate, cleanup, active_for_user, count_active
- SessionManager: create/get/refresh/destroy/user_sessions/cleanup
- TTL behaviour (short real sleep)
- Edge cases: unknown ids, double invalidate, mixed statuses
"""

from __future__ import annotations

import time

import pytest

from docstoolkit.session_mgr import Session, SessionManager, SessionStatus, SessionStore


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_store(**kwargs) -> SessionStore:
    return SessionStore(db_path=":memory:", **kwargs)


# ===========================================================================
# 1. Session dataclass
# ===========================================================================

class TestSessionDefaults:
    def test_session_id_generated(self):
        s = Session(user_id="alice")
        assert s.session_id
        assert len(s.session_id) == 32  # uuid4().hex

    def test_unique_session_ids(self):
        s1 = Session(user_id="alice")
        s2 = Session(user_id="alice")
        assert s1.session_id != s2.session_id

    def test_status_default_active(self):
        s = Session(user_id="alice")
        assert s.status == SessionStatus.ACTIVE

    def test_expires_at_default_zero(self):
        s = Session(user_id="alice")
        assert s.expires_at == 0.0

    def test_created_at_set(self):
        before = time.time()
        s = Session(user_id="alice")
        after = time.time()
        assert before <= s.created_at <= after

    def test_last_accessed_set(self):
        before = time.time()
        s = Session(user_id="alice")
        after = time.time()
        assert before <= s.last_accessed <= after

    def test_data_default_empty_dict(self):
        s = Session(user_id="alice")
        assert s.data == {}

    def test_data_not_shared_between_instances(self):
        s1 = Session(user_id="alice")
        s2 = Session(user_id="bob")
        s1.data["x"] = 1
        assert "x" not in s2.data


class TestSessionIsExpired:
    def test_no_expiry_never_expires(self):
        s = Session(user_id="alice", expires_at=0.0)
        assert s.is_expired() is False

    def test_future_expiry_not_expired(self):
        s = Session(user_id="alice", expires_at=time.time() + 9999)
        assert s.is_expired() is False

    def test_past_expiry_is_expired(self):
        s = Session(user_id="alice", expires_at=time.time() - 1)
        assert s.is_expired() is True

    def test_is_expired_with_explicit_now(self):
        now = time.time()
        s = Session(user_id="alice", expires_at=now + 10)
        assert s.is_expired(now=now + 5) is False
        assert s.is_expired(now=now + 15) is True

    def test_is_expired_exact_boundary(self):
        now = 1_000_000.0
        s = Session(user_id="alice", expires_at=now)
        # at exactly expires_at it is NOT yet expired (now > expires_at is False)
        assert s.is_expired(now=now) is False
        assert s.is_expired(now=now + 0.001) is True


class TestSessionTouch:
    def test_touch_updates_last_accessed(self):
        s = Session(user_id="alice")
        old = s.last_accessed
        time.sleep(0.01)
        s.touch()
        assert s.last_accessed > old

    def test_touch_with_explicit_now(self):
        s = Session(user_id="alice")
        future = time.time() + 500
        s.touch(now=future)
        assert s.last_accessed == future

    def test_touch_does_not_change_created_at(self):
        s = Session(user_id="alice")
        original_created = s.created_at
        s.touch(now=time.time() + 100)
        assert s.created_at == original_created


class TestSessionGetSet:
    def test_set_and_get(self):
        s = Session(user_id="alice")
        s.set("role", "admin")
        assert s.get("role") == "admin"

    def test_get_missing_key_returns_default(self):
        s = Session(user_id="alice")
        assert s.get("missing") is None

    def test_get_missing_key_custom_default(self):
        s = Session(user_id="alice")
        assert s.get("missing", 42) == 42

    def test_set_overwrites(self):
        s = Session(user_id="alice")
        s.set("key", "v1")
        s.set("key", "v2")
        assert s.get("key") == "v2"

    def test_set_reflects_in_data_dict(self):
        s = Session(user_id="alice")
        s.set("x", 99)
        assert s.data["x"] == 99

    def test_data_dict_reflects_in_get(self):
        s = Session(user_id="alice")
        s.data["y"] = "hello"
        assert s.get("y") == "hello"


# ===========================================================================
# 2. SessionStore
# ===========================================================================

class TestSessionStoreCreate:
    def test_create_returns_session(self):
        store = make_store()
        s = store.create("alice")
        assert isinstance(s, Session)
        store.close()

    def test_create_user_id(self):
        store = make_store()
        s = store.create("bob")
        assert s.user_id == "bob"
        store.close()

    def test_create_status_active(self):
        store = make_store()
        s = store.create("alice")
        assert s.status == SessionStatus.ACTIVE
        store.close()

    def test_create_with_data(self):
        store = make_store()
        s = store.create("alice", data={"theme": "dark"})
        assert s.data == {"theme": "dark"}
        store.close()

    def test_create_default_ttl_sets_expires_at(self):
        ttl = 3600.0
        store = make_store(ttl_seconds=ttl)
        before = time.time()
        s = store.create("alice")
        after = time.time()
        assert before + ttl <= s.expires_at <= after + ttl
        store.close()

    def test_create_with_custom_ttl(self):
        store = make_store(ttl_seconds=3600.0)
        before = time.time()
        s = store.create("alice", ttl=60.0)
        after = time.time()
        assert before + 60 <= s.expires_at <= after + 60
        store.close()

    def test_create_with_ttl_zero_never_expires(self):
        store = make_store(ttl_seconds=3600.0)
        s = store.create("alice", ttl=0)
        assert s.expires_at == 0.0
        store.close()

    def test_create_default_ttl_zero_never_expires(self):
        store = make_store(ttl_seconds=0)
        s = store.create("alice")
        assert s.expires_at == 0.0
        store.close()

    def test_create_unique_ids(self):
        store = make_store()
        ids = {store.create("alice").session_id for _ in range(10)}
        assert len(ids) == 10
        store.close()


class TestSessionStoreGet:
    def test_get_existing(self):
        store = make_store()
        s = store.create("alice")
        fetched = store.get(s.session_id)
        assert fetched is not None
        assert fetched.session_id == s.session_id
        store.close()

    def test_get_unknown_returns_none(self):
        store = make_store()
        assert store.get("nonexistent") is None
        store.close()

    def test_get_expired_returns_none(self):
        store = make_store()
        s = store.create("alice", ttl=0.01)
        time.sleep(0.05)
        assert store.get(s.session_id) is None
        store.close()

    def test_get_invalidated_returns_none(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        assert store.get(s.session_id) is None
        store.close()

    def test_get_preserves_data(self):
        store = make_store()
        s = store.create("alice", data={"k": "v"})
        fetched = store.get(s.session_id)
        assert fetched.data == {"k": "v"}
        store.close()

    def test_get_preserves_user_id(self):
        store = make_store()
        s = store.create("charlie")
        fetched = store.get(s.session_id)
        assert fetched.user_id == "charlie"
        store.close()

    def test_get_never_expiring_session(self):
        store = make_store(ttl_seconds=0)
        s = store.create("alice")
        time.sleep(0.02)
        assert store.get(s.session_id) is not None
        store.close()


class TestSessionStoreTouch:
    def test_touch_returns_true(self):
        store = make_store()
        s = store.create("alice")
        assert store.touch(s.session_id) is True
        store.close()

    def test_touch_updates_last_accessed_in_db(self):
        store = make_store()
        s = store.create("alice")
        future = time.time() + 999
        store.touch(s.session_id, now=future)
        fetched = store.get(s.session_id)
        assert fetched.last_accessed == pytest.approx(future)
        store.close()

    def test_touch_unknown_returns_false(self):
        store = make_store()
        assert store.touch("bad-id") is False
        store.close()

    def test_touch_expired_returns_false(self):
        store = make_store()
        s = store.create("alice", ttl=0.01)
        time.sleep(0.05)
        assert store.touch(s.session_id) is False
        store.close()

    def test_touch_invalidated_returns_false(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        assert store.touch(s.session_id) is False
        store.close()


class TestSessionStoreInvalidate:
    def test_invalidate_returns_true(self):
        store = make_store()
        s = store.create("alice")
        assert store.invalidate(s.session_id) is True
        store.close()

    def test_invalidate_makes_get_return_none(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        assert store.get(s.session_id) is None
        store.close()

    def test_invalidate_unknown_returns_false(self):
        store = make_store()
        assert store.invalidate("no-such-id") is False
        store.close()

    def test_double_invalidate_both_return_true(self):
        """Invalidating twice is idempotent; second call still returns True
        because the row still exists in the database."""
        store = make_store()
        s = store.create("alice")
        assert store.invalidate(s.session_id) is True
        assert store.invalidate(s.session_id) is True
        store.close()


class TestSessionStoreCleanup:
    def test_cleanup_removes_expired(self):
        store = make_store()
        s = store.create("alice", ttl=0.01)
        time.sleep(0.05)
        count = store.cleanup()
        assert count >= 1
        store.close()

    def test_cleanup_removes_invalidated(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        count = store.cleanup()
        assert count >= 1
        store.close()

    def test_cleanup_returns_correct_count(self):
        store = make_store()
        s1 = store.create("alice", ttl=0.01)
        s2 = store.create("bob", ttl=0.01)
        _keep = store.create("carol", ttl=9999)
        time.sleep(0.05)
        count = store.cleanup()
        assert count == 2
        store.close()

    def test_cleanup_does_not_remove_active(self):
        store = make_store()
        s = store.create("alice", ttl=9999)
        store.cleanup()
        assert store.get(s.session_id) is not None
        store.close()

    def test_cleanup_empty_store_returns_zero(self):
        store = make_store()
        assert store.cleanup() == 0
        store.close()

    def test_cleanup_with_mixed_statuses(self):
        store = make_store()
        s_active = store.create("alice", ttl=9999)
        s_invalidated = store.create("bob")
        store.invalidate(s_invalidated.session_id)
        s_expired = store.create("carol", ttl=0.01)
        time.sleep(0.05)

        count = store.cleanup()
        assert count == 2
        assert store.get(s_active.session_id) is not None
        store.close()

    def test_cleanup_with_explicit_now(self):
        store = make_store()
        s = store.create("alice", ttl=100)
        # Simulate cleanup "in the future" when session is expired
        future = time.time() + 200
        count = store.cleanup(now=future)
        assert count >= 1
        store.close()


class TestSessionStoreActiveForUser:
    def test_active_for_user_returns_sessions(self):
        store = make_store()
        s = store.create("alice")
        sessions = store.active_for_user("alice")
        assert any(x.session_id == s.session_id for x in sessions)
        store.close()

    def test_active_for_user_excludes_other_users(self):
        store = make_store()
        store.create("alice")
        store.create("bob")
        sessions = store.active_for_user("alice")
        assert all(x.user_id == "alice" for x in sessions)
        store.close()

    def test_active_for_user_excludes_invalidated(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        sessions = store.active_for_user("alice")
        assert not any(x.session_id == s.session_id for x in sessions)
        store.close()

    def test_active_for_user_excludes_expired(self):
        store = make_store()
        s = store.create("alice", ttl=0.01)
        time.sleep(0.05)
        sessions = store.active_for_user("alice")
        assert not any(x.session_id == s.session_id for x in sessions)
        store.close()

    def test_active_for_user_multiple_sessions(self):
        store = make_store()
        s1 = store.create("alice")
        s2 = store.create("alice")
        sessions = store.active_for_user("alice")
        ids = {x.session_id for x in sessions}
        assert s1.session_id in ids
        assert s2.session_id in ids
        store.close()

    def test_active_for_user_unknown_user_empty_list(self):
        store = make_store()
        assert store.active_for_user("nobody") == []
        store.close()


class TestSessionStoreCountActive:
    def test_count_active_empty(self):
        store = make_store()
        assert store.count_active() == 0
        store.close()

    def test_count_active_increments(self):
        store = make_store()
        store.create("alice")
        store.create("bob")
        assert store.count_active() == 2
        store.close()

    def test_count_active_excludes_invalidated(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        assert store.count_active() == 0
        store.close()

    def test_count_active_excludes_expired(self):
        store = make_store()
        store.create("alice", ttl=0.01)
        time.sleep(0.05)
        assert store.count_active() == 0
        store.close()

    def test_count_active_only_counts_active(self):
        store = make_store()
        store.create("alice")         # active
        s2 = store.create("bob")      # will be invalidated
        store.create("carol", ttl=0.01)  # will expire
        store.invalidate(s2.session_id)
        time.sleep(0.05)
        assert store.count_active() == 1
        store.close()


# ===========================================================================
# 3. SessionManager
# ===========================================================================

class TestSessionManagerCreate:
    def test_create_session_returns_session(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        assert isinstance(s, Session)

    def test_create_session_user_id(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        assert s.user_id == "alice"

    def test_create_session_with_data(self):
        mgr = SessionManager()
        s = mgr.create_session("alice", data={"role": "admin"})
        assert s.data["role"] == "admin"

    def test_create_session_with_ttl(self):
        mgr = SessionManager()
        before = time.time()
        s = mgr.create_session("alice", ttl=60.0)
        after = time.time()
        assert before + 60 <= s.expires_at <= after + 60


class TestSessionManagerGet:
    def test_get_session_found(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        fetched = mgr.get_session(s.session_id)
        assert fetched is not None
        assert fetched.session_id == s.session_id

    def test_get_session_not_found(self):
        mgr = SessionManager()
        assert mgr.get_session("no-such-id") is None

    def test_get_session_expired_returns_none(self):
        mgr = SessionManager()
        s = mgr.create_session("alice", ttl=0.01)
        time.sleep(0.05)
        assert mgr.get_session(s.session_id) is None


class TestSessionManagerRefresh:
    def test_refresh_returns_true(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        assert mgr.refresh_session(s.session_id) is True

    def test_refresh_unknown_returns_false(self):
        mgr = SessionManager()
        assert mgr.refresh_session("bad") is False

    def test_refresh_updates_last_accessed(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        old = s.last_accessed
        future = time.time() + 999
        mgr._store.touch(s.session_id, now=future)
        fetched = mgr.get_session(s.session_id)
        assert fetched.last_accessed > old


class TestSessionManagerDestroy:
    def test_destroy_returns_true(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        assert mgr.destroy_session(s.session_id) is True

    def test_destroy_makes_session_unavailable(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        mgr.destroy_session(s.session_id)
        assert mgr.get_session(s.session_id) is None

    def test_destroy_unknown_returns_false(self):
        mgr = SessionManager()
        assert mgr.destroy_session("no-id") is False


class TestSessionManagerUserSessions:
    def test_user_sessions_returns_list(self):
        mgr = SessionManager()
        mgr.create_session("alice")
        sessions = mgr.user_sessions("alice")
        assert len(sessions) >= 1

    def test_user_sessions_empty_for_unknown_user(self):
        mgr = SessionManager()
        assert mgr.user_sessions("ghost") == []

    def test_user_sessions_excludes_destroyed(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        mgr.destroy_session(s.session_id)
        assert mgr.user_sessions("alice") == []


class TestSessionManagerCleanup:
    def test_cleanup_removes_expired(self):
        mgr = SessionManager()
        mgr.create_session("alice", ttl=0.01)
        time.sleep(0.05)
        count = mgr.cleanup()
        assert count >= 1

    def test_cleanup_returns_zero_when_nothing_to_do(self):
        mgr = SessionManager()
        mgr.create_session("alice", ttl=9999)
        assert mgr.cleanup() == 0

    def test_cleanup_removes_destroyed(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        mgr.destroy_session(s.session_id)
        count = mgr.cleanup()
        assert count >= 1


class TestSessionManagerCustomStore:
    def test_accepts_custom_store(self):
        store = make_store(ttl_seconds=7200)
        mgr = SessionManager(store=store)
        s = mgr.create_session("dave")
        assert s.user_id == "dave"
        store.close()


# ===========================================================================
# 4. TTL behaviour (real time)
# ===========================================================================

class TestTTLBehaviour:
    def test_session_expires_after_ttl(self):
        store = make_store()
        s = store.create("alice", ttl=0.05)
        assert store.get(s.session_id) is not None
        time.sleep(0.1)
        assert store.get(s.session_id) is None
        store.close()

    def test_session_still_active_within_ttl(self):
        store = make_store()
        s = store.create("alice", ttl=5.0)
        time.sleep(0.05)
        assert store.get(s.session_id) is not None
        store.close()

    def test_manager_session_expires_after_ttl(self):
        mgr = SessionManager()
        s = mgr.create_session("alice", ttl=0.05)
        assert mgr.get_session(s.session_id) is not None
        time.sleep(0.1)
        assert mgr.get_session(s.session_id) is None

    def test_count_active_decreases_after_expiry(self):
        store = make_store()
        store.create("alice", ttl=0.05)
        assert store.count_active() == 1
        time.sleep(0.1)
        assert store.count_active() == 0
        store.close()


# ===========================================================================
# 5. Edge cases
# ===========================================================================

class TestEdgeCases:
    def test_create_with_none_data_defaults_empty_dict(self):
        store = make_store()
        s = store.create("alice", data=None)
        assert s.data == {}
        store.close()

    def test_session_data_stored_and_retrieved_correctly(self):
        store = make_store()
        payload = {"nested": {"a": 1}, "list": [1, 2, 3]}
        s = store.create("alice", data=payload)
        fetched = store.get(s.session_id)
        assert fetched.data == payload
        store.close()

    def test_double_invalidate_session_still_not_found(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        store.invalidate(s.session_id)  # idempotent
        assert store.get(s.session_id) is None
        store.close()

    def test_cleanup_twice_second_returns_zero(self):
        store = make_store()
        s = store.create("alice", ttl=0.01)
        time.sleep(0.05)
        first = store.cleanup()
        second = store.cleanup()
        assert first >= 1
        assert second == 0
        store.close()

    def test_multiple_users_independent_sessions(self):
        store = make_store()
        sa = store.create("alice")
        sb = store.create("bob")
        assert store.active_for_user("alice") == [
            x for x in [store.get(sa.session_id)]
        ]
        assert store.active_for_user("bob") == [
            x for x in [store.get(sb.session_id)]
        ]
        store.close()

    def test_invalidated_not_counted_as_active(self):
        store = make_store()
        s = store.create("alice")
        store.invalidate(s.session_id)
        assert store.count_active() == 0
        store.close()

    def test_store_default_in_memory(self):
        store = SessionStore()
        s = store.create("alice")
        assert store.get(s.session_id) is not None
        store.close()

    def test_manager_default_no_args(self):
        mgr = SessionManager()
        s = mgr.create_session("alice")
        assert mgr.get_session(s.session_id) is not None

    def test_session_status_enum_values(self):
        assert SessionStatus.ACTIVE.value == "active"
        assert SessionStatus.EXPIRED.value == "expired"
        assert SessionStatus.INVALIDATED.value == "invalidated"

    def test_session_set_multiple_keys(self):
        s = Session(user_id="alice")
        s.set("a", 1)
        s.set("b", 2)
        s.set("c", 3)
        assert s.get("a") == 1
        assert s.get("b") == 2
        assert s.get("c") == 3

    def test_cleanup_mixed_invalidated_and_expired(self):
        store = make_store()
        s1 = store.create("alice", ttl=0.01)   # will expire
        s2 = store.create("bob")                # will be invalidated
        s3 = store.create("carol", ttl=9999)    # stays active
        store.invalidate(s2.session_id)
        time.sleep(0.05)
        count = store.cleanup()
        assert count == 2
        assert store.get(s3.session_id) is not None
        store.close()
