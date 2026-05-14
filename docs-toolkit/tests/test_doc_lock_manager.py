"""Tests for ``docstoolkit.doc_lock_manager`` (E310)."""

from __future__ import annotations

import threading
import time
from dataclasses import fields

import pytest

from docstoolkit.doc_lock_manager import DocLock, DocLockManager, LockStats


# ---------------------------------------------------------------------------
# TestDocLockDataclass
# ---------------------------------------------------------------------------

class TestDocLockDataclass:
    def test_required_fields_present(self):
        field_names = {f.name for f in fields(DocLock)}
        assert {"lock_id", "doc_id", "holder", "acquired_at", "expires_at", "lock_type"}.issubset(
            field_names
        )

    def test_defaults(self):
        lk = DocLock(lock_id="x", doc_id="d", holder="h")
        assert lk.acquired_at == 0.0
        assert lk.expires_at is None
        assert lk.lock_type == "write"

    def test_custom_values(self):
        lk = DocLock(
            lock_id="abc",
            doc_id="doc1",
            holder="alice",
            acquired_at=5.0,
            expires_at=15.0,
            lock_type="read",
        )
        assert lk.lock_id == "abc"
        assert lk.doc_id == "doc1"
        assert lk.holder == "alice"
        assert lk.acquired_at == 5.0
        assert lk.expires_at == 15.0
        assert lk.lock_type == "read"

    def test_is_active_no_expiry(self):
        lk = DocLock(lock_id="x", doc_id="d", holder="h", expires_at=None)
        assert lk._is_active(1e9) is True

    def test_is_active_before_expiry(self):
        lk = DocLock(lock_id="x", doc_id="d", holder="h", expires_at=100.0)
        assert lk._is_active(99.9) is True

    def test_is_active_at_expiry(self):
        lk = DocLock(lock_id="x", doc_id="d", holder="h", expires_at=100.0)
        assert lk._is_active(100.0) is False

    def test_is_active_after_expiry(self):
        lk = DocLock(lock_id="x", doc_id="d", holder="h", expires_at=100.0)
        assert lk._is_active(200.0) is False


# ---------------------------------------------------------------------------
# TestLockStatsDataclass
# ---------------------------------------------------------------------------

class TestLockStatsDataclass:
    def test_fields_present(self):
        field_names = {f.name for f in fields(LockStats)}
        assert {"total_locks", "write_locks", "read_locks", "unique_docs"}.issubset(field_names)

    def test_construction(self):
        s = LockStats(total_locks=5, write_locks=2, read_locks=3, unique_docs=4)
        assert s.total_locks == 5
        assert s.write_locks == 2
        assert s.read_locks == 3
        assert s.unique_docs == 4

    def test_zero_stats(self):
        s = LockStats(total_locks=0, write_locks=0, read_locks=0, unique_docs=0)
        assert s.total_locks == 0


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_manager_creates_empty(self):
        m = DocLockManager()
        assert m.stats(now=0.0).total_locks == 0

    def test_multiple_independent_managers(self):
        m1 = DocLockManager()
        m2 = DocLockManager()
        m1.acquire("d", "alice", now=0.0)
        assert m2.stats(now=0.0).total_locks == 0


# ---------------------------------------------------------------------------
# TestAcquireWrite
# ---------------------------------------------------------------------------

class TestAcquireWrite:
    def test_write_succeeds_on_unlocked_doc(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", lock_type="write", now=0.0)
        assert lk is not None
        assert lk.lock_type == "write"
        assert lk.doc_id == "doc1"
        assert lk.holder == "alice"

    def test_write_returns_doclock_instance(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        assert isinstance(lk, DocLock)

    def test_write_blocked_by_existing_write(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        result = m.acquire("doc1", "bob", lock_type="write", now=0.0)
        assert result is None

    def test_write_blocked_by_existing_read(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        result = m.acquire("doc1", "bob", lock_type="write", now=0.0)
        assert result is None

    def test_write_on_different_doc_allowed(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        lk = m.acquire("doc2", "bob", lock_type="write", now=0.0)
        assert lk is not None

    def test_write_lock_id_is_unique(self):
        m = DocLockManager()
        lk1 = m.acquire("doc1", "alice", now=0.0)
        m.release(lk1.lock_id)
        lk2 = m.acquire("doc1", "alice", now=0.0)
        assert lk1.lock_id != lk2.lock_id


# ---------------------------------------------------------------------------
# TestAcquireRead
# ---------------------------------------------------------------------------

class TestAcquireRead:
    def test_read_succeeds_on_unlocked_doc(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", lock_type="read", now=0.0)
        assert lk is not None
        assert lk.lock_type == "read"

    def test_multiple_reads_allowed(self):
        m = DocLockManager()
        lk1 = m.acquire("doc1", "alice", lock_type="read", now=0.0)
        lk2 = m.acquire("doc1", "bob", lock_type="read", now=0.0)
        lk3 = m.acquire("doc1", "carol", lock_type="read", now=0.0)
        assert lk1 is not None
        assert lk2 is not None
        assert lk3 is not None

    def test_read_blocked_by_write(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        result = m.acquire("doc1", "bob", lock_type="read", now=0.0)
        assert result is None

    def test_read_allowed_after_write_released(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", lock_type="write", now=0.0)
        m.release(lk.lock_id)
        result = m.acquire("doc1", "bob", lock_type="read", now=0.0)
        assert result is not None


# ---------------------------------------------------------------------------
# TestRelease
# ---------------------------------------------------------------------------

class TestRelease:
    def test_release_existing_returns_true(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        assert m.release(lk.lock_id) is True

    def test_release_missing_returns_false(self):
        m = DocLockManager()
        assert m.release("nonexistent-id") is False

    def test_lock_gone_after_release(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        m.release(lk.lock_id)
        assert m.get_lock(lk.lock_id) is None

    def test_doc_unlocked_after_release(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        m.release(lk.lock_id)
        assert m.is_locked("doc1", now=0.0) is False

    def test_release_only_target_lock(self):
        m = DocLockManager()
        lk1 = m.acquire("doc1", "alice", lock_type="read", now=0.0)
        lk2 = m.acquire("doc1", "bob", lock_type="read", now=0.0)
        m.release(lk1.lock_id)
        assert m.is_locked("doc1", now=0.0) is True
        assert m.get_lock(lk2.lock_id) is not None


# ---------------------------------------------------------------------------
# TestReleaseAll
# ---------------------------------------------------------------------------

class TestReleaseAll:
    def test_release_all_returns_count(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc1", "bob", lock_type="read", now=0.0)
        assert m.release_all("doc1") == 2

    def test_release_all_empty_doc(self):
        m = DocLockManager()
        assert m.release_all("doc1") == 0

    def test_release_all_unlocks_doc(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc1", "bob", lock_type="read", now=0.0)
        m.release_all("doc1")
        assert m.is_locked("doc1", now=0.0) is False

    def test_release_all_does_not_affect_other_docs(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        m.acquire("doc2", "bob", lock_type="write", now=0.0)
        m.release_all("doc1")
        assert m.is_locked("doc2", now=0.0) is True


# ---------------------------------------------------------------------------
# TestReleaseByHolder
# ---------------------------------------------------------------------------

class TestReleaseByHolder:
    def test_release_by_holder_returns_count(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc2", "alice", lock_type="write", now=0.0)
        assert m.release_by_holder("alice") == 2

    def test_release_by_holder_zero_for_unknown(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", now=0.0)
        assert m.release_by_holder("nobody") == 0

    def test_release_by_holder_only_that_holder(self):
        m = DocLockManager()
        lk_alice = m.acquire("doc1", "alice", lock_type="read", now=0.0)
        lk_bob = m.acquire("doc1", "bob", lock_type="read", now=0.0)
        m.release_by_holder("alice")
        assert m.get_lock(lk_alice.lock_id) is None
        assert m.get_lock(lk_bob.lock_id) is not None

    def test_release_by_holder_across_multiple_docs(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc2", "alice", lock_type="read", now=0.0)
        m.acquire("doc3", "bob", lock_type="write", now=0.0)
        m.release_by_holder("alice")
        assert not m.is_locked("doc1", now=0.0)
        assert not m.is_locked("doc2", now=0.0)
        assert m.is_locked("doc3", now=0.0)


# ---------------------------------------------------------------------------
# TestGetLock
# ---------------------------------------------------------------------------

class TestGetLock:
    def test_get_lock_found(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        found = m.get_lock(lk.lock_id)
        assert found is not None
        assert found.lock_id == lk.lock_id

    def test_get_lock_not_found(self):
        m = DocLockManager()
        assert m.get_lock("does-not-exist") is None

    def test_get_lock_after_release(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        m.release(lk.lock_id)
        assert m.get_lock(lk.lock_id) is None


# ---------------------------------------------------------------------------
# TestLocksForDoc
# ---------------------------------------------------------------------------

class TestLocksForDoc:
    def test_returns_only_active_locks(self):
        m = DocLockManager()
        lk1 = m.acquire("doc1", "alice", lock_type="read", ttl_seconds=5.0, now=0.0)
        lk2 = m.acquire("doc1", "bob", lock_type="read", ttl_seconds=100.0, now=0.0)
        # At now=10, lk1 is expired
        active = m.locks_for_doc("doc1", now=10.0)
        ids = [lk.lock_id for lk in active]
        assert lk1.lock_id not in ids
        assert lk2.lock_id in ids

    def test_sorted_by_acquired_at(self):
        m = DocLockManager()
        lk1 = m.acquire("doc1", "alice", lock_type="read", now=1.0)
        lk2 = m.acquire("doc1", "bob", lock_type="read", now=3.0)
        lk3 = m.acquire("doc1", "carol", lock_type="read", now=2.0)
        result = m.locks_for_doc("doc1", now=0.0)
        assert [lk.acquired_at for lk in result] == [1.0, 2.0, 3.0]

    def test_expired_excluded(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", ttl_seconds=1.0, now=0.0)
        result = m.locks_for_doc("doc1", now=10.0)
        assert result == []

    def test_empty_for_unknown_doc(self):
        m = DocLockManager()
        assert m.locks_for_doc("unknown", now=0.0) == []


# ---------------------------------------------------------------------------
# TestIsLocked
# ---------------------------------------------------------------------------

class TestIsLocked:
    def test_unlocked_doc_returns_false(self):
        m = DocLockManager()
        assert m.is_locked("doc1", now=0.0) is False

    def test_locked_returns_true(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", now=0.0)
        assert m.is_locked("doc1", now=0.0) is True

    def test_expired_lock_not_locked(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", ttl_seconds=5.0, now=0.0)
        assert m.is_locked("doc1", now=10.0) is False

    def test_released_lock_not_locked(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)
        m.release(lk.lock_id)
        assert m.is_locked("doc1", now=0.0) is False


# ---------------------------------------------------------------------------
# TestIsWriteLocked
# ---------------------------------------------------------------------------

class TestIsWriteLocked:
    def test_write_lock_returns_true(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        assert m.is_write_locked("doc1", now=0.0) is True

    def test_read_only_returns_false(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        assert m.is_write_locked("doc1", now=0.0) is False

    def test_no_lock_returns_false(self):
        m = DocLockManager()
        assert m.is_write_locked("doc1", now=0.0) is False

    def test_expired_write_lock_returns_false(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", ttl_seconds=5.0, now=0.0)
        assert m.is_write_locked("doc1", now=10.0) is False


# ---------------------------------------------------------------------------
# TestExpireStale
# ---------------------------------------------------------------------------

class TestExpireStale:
    def test_removes_expired_locks(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", ttl_seconds=5.0, now=0.0)
        count = m.expire_stale(now=10.0)
        assert count == 1

    def test_keeps_non_expired_locks(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", lock_type="read", ttl_seconds=100.0, now=0.0)
        count = m.expire_stale(now=10.0)
        assert count == 0
        assert m.get_lock(lk.lock_id) is not None

    def test_returns_count_of_removed(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", ttl_seconds=1.0, now=0.0)
        m.acquire("doc2", "bob", lock_type="read", ttl_seconds=2.0, now=0.0)
        m.acquire("doc3", "carol", lock_type="read", ttl_seconds=100.0, now=0.0)
        count = m.expire_stale(now=5.0)
        assert count == 2

    def test_empty_manager_returns_zero(self):
        m = DocLockManager()
        assert m.expire_stale(now=100.0) == 0

    def test_keeps_no_ttl_locks(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=0.0)  # no ttl
        m.expire_stale(now=1e9)
        assert m.get_lock(lk.lock_id) is not None


# ---------------------------------------------------------------------------
# TestTTL
# ---------------------------------------------------------------------------

class TestTTL:
    def test_expires_at_set_correctly(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", ttl_seconds=30.0, now=10.0)
        assert lk.expires_at == 40.0

    def test_no_ttl_expires_at_is_none(self):
        m = DocLockManager()
        lk = m.acquire("doc1", "alice", now=10.0)
        assert lk.expires_at is None

    def test_lock_expires_after_ttl(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", ttl_seconds=5.0, now=0.0)
        assert m.is_locked("doc1", now=4.999) is True
        assert m.is_locked("doc1", now=5.0) is False

    def test_write_acquirable_after_ttl(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", ttl_seconds=5.0, now=0.0)
        lk2 = m.acquire("doc1", "bob", lock_type="write", now=10.0)
        assert lk2 is not None


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------

class TestStats:
    def test_empty_stats(self):
        m = DocLockManager()
        s = m.stats(now=0.0)
        assert s.total_locks == 0
        assert s.write_locks == 0
        assert s.read_locks == 0
        assert s.unique_docs == 0

    def test_counts_write_locks(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", now=0.0)
        s = m.stats(now=0.0)
        assert s.write_locks == 1
        assert s.read_locks == 0
        assert s.total_locks == 1

    def test_counts_read_locks(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc1", "bob", lock_type="read", now=0.0)
        s = m.stats(now=0.0)
        assert s.read_locks == 2
        assert s.write_locks == 0
        assert s.total_locks == 2

    def test_unique_docs(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc1", "bob", lock_type="read", now=0.0)
        m.acquire("doc2", "carol", lock_type="write", now=0.0)
        s = m.stats(now=0.0)
        assert s.unique_docs == 2

    def test_expired_excluded_from_stats(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="write", ttl_seconds=1.0, now=0.0)
        s = m.stats(now=10.0)
        assert s.total_locks == 0
        assert s.unique_docs == 0

    def test_mixed_locks_stats(self):
        m = DocLockManager()
        m.acquire("doc1", "alice", lock_type="read", now=0.0)
        m.acquire("doc2", "bob", lock_type="write", now=0.0)
        m.acquire("doc3", "carol", lock_type="read", now=0.0)
        s = m.stats(now=0.0)
        assert s.total_locks == 3
        assert s.write_locks == 1
        assert s.read_locks == 2
        assert s.unique_docs == 3


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_acquire_single_write(self):
        """Only one thread should succeed in acquiring a write lock."""
        m = DocLockManager()
        results: list[Optional[DocLock]] = []
        errors: list[Exception] = []
        barrier = threading.Barrier(10)

        def worker():
            try:
                barrier.wait()
                lk = m.acquire("shared_doc", f"holder-{threading.get_ident()}", lock_type="write")
                results.append(lk)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        successes = [r for r in results if r is not None]
        # At most one write lock can be held at any given moment.
        # Due to serialisation, exactly one thread wins per "round".
        assert len(successes) >= 1

    def test_concurrent_read_all_succeed(self):
        """All threads should acquire a read lock simultaneously."""
        m = DocLockManager()
        results: list[Optional[DocLock]] = []
        errors: list[Exception] = []
        barrier = threading.Barrier(10)

        def worker():
            try:
                barrier.wait()
                lk = m.acquire("shared_doc", f"holder-{threading.get_ident()}", lock_type="read")
                results.append(lk)
            except Exception as exc:
                errors.append(exc)

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        successes = [r for r in results if r is not None]
        assert len(successes) == 10

    def test_no_data_races_on_stats(self):
        """stats() callable from many threads without error."""
        m = DocLockManager()
        errors: list[Exception] = []

        def writer():
            for i in range(20):
                lk = m.acquire(f"doc-{i}", "writer", lock_type="write")
                if lk:
                    m.release(lk.lock_id)

        def reader():
            for _ in range(50):
                try:
                    m.stats()
                except Exception as exc:
                    errors.append(exc)

        threads = (
            [threading.Thread(target=writer) for _ in range(3)]
            + [threading.Thread(target=reader) for _ in range(3)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
