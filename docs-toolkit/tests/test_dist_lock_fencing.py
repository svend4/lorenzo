"""Tests for docstoolkit.dist_lock.manager — fencing-token distributed lock."""
from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.dist_lock import FencedLockManager, FencingError, FencingToken


# ---------------------------------------------------------------------------
# FencingToken
# ---------------------------------------------------------------------------

class TestFencingToken:
    def test_is_fresh_same_epoch(self):
        tok = FencingToken(epoch=5, owner="x", lock_name="L", issued_at=0.0)
        assert tok.is_fresh(5) is True

    def test_is_fresh_stale_token(self):
        tok = FencingToken(epoch=3, owner="x", lock_name="L", issued_at=0.0)
        assert tok.is_fresh(5) is False

    def test_is_fresh_newer_token_still_false(self):
        # epoch 7 presented against current 5 is *also* False (should not happen
        # in practice, but we only accept exact match for current epoch)
        tok = FencingToken(epoch=7, owner="x", lock_name="L", issued_at=0.0)
        assert tok.is_fresh(5) is False

    def test_repr(self):
        tok = FencingToken(epoch=1, owner="bob", lock_name="L", issued_at=0.0)
        assert "epoch=1" in repr(tok)
        assert "bob" in repr(tok)


# ---------------------------------------------------------------------------
# FencedLockManager — basic acquire / release
# ---------------------------------------------------------------------------

class TestFencedLockManagerAcquire:
    def test_acquire_returns_token(self):
        mgr = FencedLockManager()
        tok = mgr.acquire("res-A")
        assert isinstance(tok, FencingToken)
        assert tok.epoch >= 1
        assert tok.lock_name == "res-A"

    def test_acquire_fails_when_held(self):
        mgr = FencedLockManager()
        mgr.acquire("res-B", owner="alice")
        tok2 = mgr.acquire("res-B", owner="bob")
        assert tok2 is None

    def test_acquire_steals_expired_lock(self):
        mgr = FencedLockManager(ttl=0.05)
        tok1 = mgr.acquire("res-C", owner="alice")
        assert tok1 is not None
        time.sleep(0.1)
        tok2 = mgr.acquire("res-C", owner="bob")
        assert tok2 is not None
        assert tok2.epoch > tok1.epoch  # epoch must strictly increase

    def test_epoch_strictly_increases_across_acquires(self):
        mgr = FencedLockManager(ttl=0.05)
        epochs = []
        for _ in range(5):
            tok = mgr.acquire("res-D", owner="x")
            assert tok is not None
            epochs.append(tok.epoch)
            time.sleep(0.07)  # let TTL expire
        assert epochs == sorted(set(epochs))

    def test_is_locked_after_acquire(self):
        mgr = FencedLockManager()
        mgr.acquire("lock-1", owner="x")
        assert mgr.is_locked("lock-1") is True

    def test_is_locked_false_after_release(self):
        mgr = FencedLockManager()
        mgr.acquire("lock-2", owner="y")
        mgr.release("lock-2", owner="y")
        assert mgr.is_locked("lock-2") is False

    def test_is_locked_false_for_unknown(self):
        mgr = FencedLockManager()
        assert mgr.is_locked("no-such-lock") is False

    def test_release_wrong_owner_returns_false(self):
        mgr = FencedLockManager()
        mgr.acquire("lock-3", owner="alice")
        assert mgr.release("lock-3", owner="bob") is False
        assert mgr.is_locked("lock-3") is True

    def test_current_epoch_returns_none_for_unlocked(self):
        mgr = FencedLockManager()
        assert mgr.current_epoch("no-lock") is None

    def test_current_epoch_matches_token_epoch(self):
        mgr = FencedLockManager()
        tok = mgr.acquire("ep-lock", owner="x")
        assert mgr.current_epoch("ep-lock") == tok.epoch


# ---------------------------------------------------------------------------
# FencedLockManager — validate_write (core fencing logic)
# ---------------------------------------------------------------------------

class TestFencingValidation:
    def test_valid_write_succeeds(self):
        mgr = FencedLockManager()
        tok = mgr.acquire("res", owner="x")
        # Should not raise
        mgr.validate_write("doc-1", tok)

    def test_stale_token_raises_fencing_error(self):
        mgr = FencedLockManager(ttl=0.05)
        tok1 = mgr.acquire("res", owner="x")
        time.sleep(0.07)  # expire
        tok2 = mgr.acquire("res", owner="y")
        assert tok2.epoch > tok1.epoch

        # First write with new token sets max_epoch
        mgr.validate_write("doc-stale", tok2)

        # Now trying to write with old token must fail
        with pytest.raises(FencingError, match="Stale token"):
            mgr.validate_write("doc-stale", tok1)

    def test_network_partition_scenario(self):
        """Simulate: worker-1 holds lock, pauses, lock stolen, worker-1 resumes."""
        mgr = FencedLockManager(ttl=0.05)

        # Worker 1 acquires lock and gets token
        tok1 = mgr.acquire("shared-doc", owner="worker-1")
        assert tok1 is not None

        # Lock expires while worker-1 is paused
        time.sleep(0.07)

        # Worker 2 steals the lock
        tok2 = mgr.acquire("shared-doc", owner="worker-2")
        assert tok2 is not None
        assert tok2.epoch > tok1.epoch

        # Worker-2 does a valid write first (registers max_epoch)
        mgr.validate_write("shared-doc", tok2)

        # Worker-1 wakes up and tries to write with stale token
        with pytest.raises(FencingError):
            mgr.validate_write("shared-doc", tok1)

    def test_same_resource_multiple_valid_writes(self):
        mgr = FencedLockManager()
        tok = mgr.acquire("res", owner="x")
        # Multiple writes with same token should all succeed
        mgr.validate_write("my-resource", tok)
        mgr.validate_write("my-resource", tok)

    def test_different_resources_independent(self):
        """Token valid for resource-A should not affect resource-B validation."""
        mgr = FencedLockManager()
        tok = mgr.acquire("lock", owner="x")
        mgr.validate_write("resource-A", tok)
        # resource-B has its own tracking, no FencingError here
        mgr.validate_write("resource-B", tok)


# ---------------------------------------------------------------------------
# FencedLockManager — context manager
# ---------------------------------------------------------------------------

class TestFencedLockCtx:
    def test_context_manager_acquires_and_releases(self):
        mgr = FencedLockManager()
        with mgr.lock("ctx-lock") as tok:
            assert isinstance(tok, FencingToken)
            assert mgr.is_locked("ctx-lock")
        assert not mgr.is_locked("ctx-lock")

    def test_context_manager_releases_on_exception(self):
        mgr = FencedLockManager()
        try:
            with mgr.lock("ctx-lock2") as tok:
                raise ValueError("boom")
        except ValueError:
            pass
        assert not mgr.is_locked("ctx-lock2")

    def test_context_manager_raises_if_held(self):
        mgr = FencedLockManager()
        mgr.acquire("busy-lock", owner="alice")
        with pytest.raises(FencingError):
            with mgr.lock("busy-lock"):
                pass  # should not reach here


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestFencedLockThreadSafety:
    def test_only_one_worker_acquires(self, tmp_path):
        db = str(tmp_path / "locks.db")
        mgr = FencedLockManager(db_path=db, ttl=10.0, max_retries=0)

        tokens = []
        lock = threading.Lock()

        def try_acquire():
            tok = mgr.acquire("shared", owner=None)
            if tok is not None:
                with lock:
                    tokens.append(tok)

        threads = [threading.Thread(target=try_acquire) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # At most one token issued (SQLite serializes writes)
        assert len(tokens) <= 1

    def test_no_double_fencing_error_on_concurrent_writes(self, tmp_path):
        """Sequential valid writes from same token should not error."""
        db = str(tmp_path / "locks2.db")
        mgr = FencedLockManager(db_path=db)
        tok = mgr.acquire("seq-lock", owner="x")

        errors = []
        lock = threading.Lock()

        def do_write():
            try:
                mgr.validate_write("sequential-doc", tok)
            except FencingError as e:
                with lock:
                    errors.append(str(e))

        # Same token, same epoch → all writes should succeed
        threads = [threading.Thread(target=do_write) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
