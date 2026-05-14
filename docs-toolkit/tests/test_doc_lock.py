"""Tests for ``docstoolkit.doc_lock``."""

from __future__ import annotations

import pytest

from docstoolkit.doc_lock import (
    LockError,
    LockInfo,
    LockManager,
    LockState,
    LockType,
)


# ----------------------------------------------------------------------
# Enums
# ----------------------------------------------------------------------
class TestLockType:
    def test_shared_value(self):
        assert LockType.SHARED.value == "shared"

    def test_exclusive_value(self):
        assert LockType.EXCLUSIVE.value == "exclusive"

    def test_distinct(self):
        assert LockType.SHARED is not LockType.EXCLUSIVE


class TestLockState:
    def test_available(self):
        assert LockState.AVAILABLE.value == "available"

    def test_locked_shared(self):
        assert LockState.LOCKED_SHARED.value == "locked_shared"

    def test_locked_exclusive(self):
        assert LockState.LOCKED_EXCLUSIVE.value == "locked_exclusive"

    def test_all_distinct(self):
        values = {LockState.AVAILABLE, LockState.LOCKED_SHARED, LockState.LOCKED_EXCLUSIVE}
        assert len(values) == 3


# ----------------------------------------------------------------------
# LockInfo
# ----------------------------------------------------------------------
class TestLockInfo:
    def test_fields(self):
        info = LockInfo(
            doc_id="d1",
            lock_type=LockType.SHARED,
            holder_id="alice",
            acquired_at=10.0,
            expires_at=20.0,
        )
        assert info.doc_id == "d1"
        assert info.lock_type == LockType.SHARED
        assert info.holder_id == "alice"
        assert info.acquired_at == 10.0
        assert info.expires_at == 20.0

    def test_is_expired_no_expiry(self):
        info = LockInfo("d", LockType.SHARED, "h", 0.0, None)
        assert info.is_expired(now=1e9) is False

    def test_is_expired_future(self):
        info = LockInfo("d", LockType.SHARED, "h", 0.0, 100.0)
        assert info.is_expired(now=50.0) is False

    def test_is_expired_at_boundary(self):
        info = LockInfo("d", LockType.SHARED, "h", 0.0, 100.0)
        assert info.is_expired(now=100.0) is True

    def test_is_expired_past(self):
        info = LockInfo("d", LockType.SHARED, "h", 0.0, 100.0)
        assert info.is_expired(now=200.0) is True


# ----------------------------------------------------------------------
# Acquire SHARED
# ----------------------------------------------------------------------
class TestAcquireShared:
    def test_single_shared(self):
        m = LockManager()
        assert m.acquire_shared("d", "alice") is True

    def test_multiple_holders(self):
        m = LockManager()
        assert m.acquire_shared("d", "alice") is True
        assert m.acquire_shared("d", "bob") is True
        assert m.acquire_shared("d", "carol") is True
        assert set(m.holders("d")) == {"alice", "bob", "carol"}

    def test_shared_independent_docs(self):
        m = LockManager()
        assert m.acquire_shared("d1", "alice") is True
        assert m.acquire_shared("d2", "alice") is True

    def test_empty_doc_id_raises(self):
        m = LockManager()
        with pytest.raises(LockError):
            m.acquire_shared("", "alice")

    def test_empty_holder_raises(self):
        m = LockManager()
        with pytest.raises(LockError):
            m.acquire_shared("d", "")


# ----------------------------------------------------------------------
# Acquire EXCLUSIVE
# ----------------------------------------------------------------------
class TestAcquireExclusive:
    def test_single_exclusive(self):
        m = LockManager()
        assert m.acquire_exclusive("d", "alice") is True

    def test_second_exclusive_denied(self):
        m = LockManager()
        assert m.acquire_exclusive("d", "alice") is True
        assert m.acquire_exclusive("d", "bob") is False

    def test_exclusive_different_docs(self):
        m = LockManager()
        assert m.acquire_exclusive("d1", "alice") is True
        assert m.acquire_exclusive("d2", "bob") is True

    def test_empty_args_raise(self):
        m = LockManager()
        with pytest.raises(LockError):
            m.acquire_exclusive("", "alice")
        with pytest.raises(LockError):
            m.acquire_exclusive("d", "")


# ----------------------------------------------------------------------
# Exclusive blocks shared
# ----------------------------------------------------------------------
class TestExclusiveBlocksShared:
    def test_shared_after_exclusive_denied(self):
        m = LockManager()
        assert m.acquire_exclusive("d", "alice") is True
        assert m.acquire_shared("d", "bob") is False

    def test_multiple_shared_denied(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice")
        assert m.acquire_shared("d", "bob") is False
        assert m.acquire_shared("d", "carol") is False

    def test_shared_allowed_after_exclusive_released(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice")
        m.release("d", "alice")
        assert m.acquire_shared("d", "bob") is True


# ----------------------------------------------------------------------
# Shared blocks exclusive
# ----------------------------------------------------------------------
class TestSharedBlocksExclusive:
    def test_exclusive_after_shared_denied(self):
        m = LockManager()
        assert m.acquire_shared("d", "alice") is True
        assert m.acquire_exclusive("d", "bob") is False

    def test_exclusive_blocked_by_multiple_shared(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.acquire_shared("d", "bob")
        assert m.acquire_exclusive("d", "carol") is False

    def test_exclusive_allowed_after_shared_released(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.release("d", "alice")
        assert m.acquire_exclusive("d", "bob") is True


# ----------------------------------------------------------------------
# Release
# ----------------------------------------------------------------------
class TestRelease:
    def test_release_existing(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.release("d", "alice") is True

    def test_release_missing_doc(self):
        m = LockManager()
        assert m.release("missing", "alice") is False

    def test_release_wrong_holder(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.release("d", "bob") is False

    def test_release_only_specific_holder(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.acquire_shared("d", "bob")
        assert m.release("d", "alice") is True
        assert m.holders("d") == ["bob"]

    def test_release_exclusive(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice")
        assert m.release("d", "alice") is True
        assert m.state("d") == LockState.AVAILABLE


# ----------------------------------------------------------------------
# Release all
# ----------------------------------------------------------------------
class TestReleaseAll:
    def test_release_all_empty(self):
        m = LockManager()
        assert m.release_all("alice") == 0

    def test_release_all_one(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.release_all("alice") == 1

    def test_release_all_multiple_docs(self):
        m = LockManager()
        m.acquire_shared("d1", "alice")
        m.acquire_shared("d2", "alice")
        m.acquire_exclusive("d3", "alice")
        assert m.release_all("alice") == 3

    def test_release_all_leaves_others(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.acquire_shared("d", "bob")
        m.release_all("alice")
        assert m.holders("d") == ["bob"]


# ----------------------------------------------------------------------
# State
# ----------------------------------------------------------------------
class TestState:
    def test_available_initially(self):
        m = LockManager()
        assert m.state("d") == LockState.AVAILABLE

    def test_shared_state(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.state("d") == LockState.LOCKED_SHARED

    def test_exclusive_state(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice")
        assert m.state("d") == LockState.LOCKED_EXCLUSIVE

    def test_state_after_release(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.release("d", "alice")
        assert m.state("d") == LockState.AVAILABLE


# ----------------------------------------------------------------------
# Holders
# ----------------------------------------------------------------------
class TestHolders:
    def test_no_holders(self):
        m = LockManager()
        assert m.holders("d") == []

    def test_one_holder(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.holders("d") == ["alice"]

    def test_many_holders(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.acquire_shared("d", "bob")
        assert set(m.holders("d")) == {"alice", "bob"}


# ----------------------------------------------------------------------
# IsLocked
# ----------------------------------------------------------------------
class TestIsLocked:
    def test_unlocked(self):
        m = LockManager()
        assert m.is_locked("d") is False

    def test_locked_shared(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.is_locked("d") is True

    def test_locked_exclusive(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice")
        assert m.is_locked("d") is True


# ----------------------------------------------------------------------
# IsHeldBy
# ----------------------------------------------------------------------
class TestIsHeldBy:
    def test_no_lock(self):
        m = LockManager()
        assert m.is_held_by("d", "alice") is False

    def test_held_by_correct(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.is_held_by("d", "alice") is True

    def test_held_by_wrong(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.is_held_by("d", "bob") is False


# ----------------------------------------------------------------------
# Expiration
# ----------------------------------------------------------------------
class TestExpiration:
    def test_no_timeout_never_expires(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=None, now=0.0)
        assert m.is_locked("d", now=1e9) is True

    def test_expires_at_boundary(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=10.0, now=0.0)
        assert m.is_locked("d", now=9.999) is True
        assert m.is_locked("d", now=10.0) is False

    def test_expired_allows_new_exclusive(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=5.0, now=0.0)
        assert m.acquire_exclusive("d", "bob", now=10.0) is True

    def test_expired_state_available(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice", timeout=5.0, now=0.0)
        assert m.state("d", now=100.0) == LockState.AVAILABLE

    def test_expired_holders_empty(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=5.0, now=0.0)
        assert m.holders("d", now=100.0) == []


# ----------------------------------------------------------------------
# Cleanup expired
# ----------------------------------------------------------------------
class TestCleanupExpired:
    def test_cleanup_empty(self):
        m = LockManager()
        assert m.cleanup_expired(now=10.0) == 0

    def test_cleanup_no_expired(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=100.0, now=0.0)
        assert m.cleanup_expired(now=10.0) == 0

    def test_cleanup_removes_expired(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=5.0, now=0.0)
        m.acquire_shared("d2", "bob", timeout=100.0, now=0.0)
        assert m.cleanup_expired(now=10.0) == 1

    def test_cleanup_multiple(self):
        m = LockManager()
        m.acquire_shared("d1", "alice", timeout=1.0, now=0.0)
        m.acquire_shared("d2", "bob", timeout=2.0, now=0.0)
        m.acquire_shared("d3", "carol", timeout=3.0, now=0.0)
        assert m.cleanup_expired(now=100.0) == 3
        assert m.lock_count() == 0


# ----------------------------------------------------------------------
# Lock count
# ----------------------------------------------------------------------
class TestLockCount:
    def test_count_zero(self):
        m = LockManager()
        assert m.lock_count() == 0
        assert m.lock_count("d") == 0

    def test_count_one_doc(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.acquire_shared("d", "bob")
        assert m.lock_count("d") == 2

    def test_total_count(self):
        m = LockManager()
        m.acquire_shared("d1", "alice")
        m.acquire_shared("d2", "bob")
        m.acquire_exclusive("d3", "carol")
        assert m.lock_count() == 3


# ----------------------------------------------------------------------
# All locked docs
# ----------------------------------------------------------------------
class TestAllLockedDocs:
    def test_empty(self):
        m = LockManager()
        assert m.all_locked_docs() == []

    def test_one_doc(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.all_locked_docs() == ["d"]

    def test_multiple_docs(self):
        m = LockManager()
        m.acquire_shared("d1", "alice")
        m.acquire_exclusive("d2", "bob")
        assert set(m.all_locked_docs()) == {"d1", "d2"}

    def test_expired_excluded(self):
        m = LockManager()
        m.acquire_shared("d1", "alice", timeout=5.0, now=0.0)
        m.acquire_shared("d2", "bob", timeout=100.0, now=0.0)
        assert m.all_locked_docs(now=10.0) == ["d2"]


# ----------------------------------------------------------------------
# Info
# ----------------------------------------------------------------------
class TestInfo:
    def test_info_empty(self):
        m = LockManager()
        assert m.info("d") == []

    def test_info_returns_lock_info(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=10.0, now=5.0)
        infos = m.info("d")
        assert len(infos) == 1
        assert infos[0].holder_id == "alice"
        assert infos[0].lock_type == LockType.SHARED
        assert infos[0].acquired_at == 5.0
        assert infos[0].expires_at == 15.0

    def test_info_copy_isolation(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        infos = m.info("d")
        infos.clear()
        # original state untouched
        assert m.holders("d") == ["alice"]

    def test_info_exclusive(self):
        m = LockManager()
        m.acquire_exclusive("d", "alice", now=0.0)
        infos = m.info("d")
        assert infos[0].lock_type == LockType.EXCLUSIVE


# ----------------------------------------------------------------------
# Idempotent re-acquire
# ----------------------------------------------------------------------
class TestIdempotent:
    def test_reacquire_shared_same_holder(self):
        m = LockManager()
        assert m.acquire_shared("d", "alice", timeout=10.0, now=0.0) is True
        assert m.acquire_shared("d", "alice", timeout=20.0, now=5.0) is True
        # Still only one shared lock for alice
        infos = m.info("d")
        assert len(infos) == 1
        assert infos[0].expires_at == 25.0  # 5 + 20

    def test_reacquire_exclusive_same_holder(self):
        m = LockManager()
        assert m.acquire_exclusive("d", "alice", timeout=10.0, now=0.0) is True
        assert m.acquire_exclusive("d", "alice", timeout=20.0, now=5.0) is True
        assert m.lock_count("d") == 1

    def test_reacquire_extends_timeout(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=5.0, now=0.0)
        m.acquire_shared("d", "alice", timeout=100.0, now=2.0)
        assert m.is_locked("d", now=50.0) is True


# ----------------------------------------------------------------------
# Edge cases
# ----------------------------------------------------------------------
class TestEdgeCases:
    def test_release_missing(self):
        m = LockManager()
        assert m.release("missing", "alice") is False

    def test_release_all_unknown_holder(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.release_all("unknown") == 0

    def test_state_unknown_doc(self):
        m = LockManager()
        assert m.state("never") == LockState.AVAILABLE

    def test_info_unknown_doc(self):
        m = LockManager()
        assert m.info("never") == []

    def test_acquire_exclusive_when_self_holds_shared(self):
        # Same holder already holds shared → can upgrade to exclusive
        m = LockManager()
        m.acquire_shared("d", "alice")
        assert m.acquire_exclusive("d", "alice") is True
        assert m.state("d") == LockState.LOCKED_EXCLUSIVE

    def test_lock_count_after_release(self):
        m = LockManager()
        m.acquire_shared("d", "alice")
        m.release("d", "alice")
        assert m.lock_count("d") == 0
        assert m.lock_count() == 0

    def test_zero_timeout_expires_immediately(self):
        m = LockManager()
        m.acquire_shared("d", "alice", timeout=0.0, now=0.0)
        # At now=0, expires_at=0, is_expired uses ``now >= expires_at`` → expired
        assert m.is_locked("d", now=0.0) is False
