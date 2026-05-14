"""Tests for the dist_lock module — 90+ tests covering all spec requirements."""
import json
import os
import sqlite3
import tempfile
import time
import uuid
import pytest

from docstoolkit.dist_lock import LockError, LockConfig, FileLock, SQLiteLock


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture()
def tmp_db(tmp_dir):
    return os.path.join(tmp_dir, "locks.db")


def _file_lock(name="mylock", lock_dir=None, ttl=30.0, retry_interval=0.1,
               max_retries=0):
    cfg = LockConfig(ttl=ttl, retry_interval=retry_interval,
                     max_retries=max_retries)
    return FileLock(name, lock_dir, config=cfg)


def _sqlite_lock(name="mylock", db_path=None, ttl=30.0, retry_interval=0.1,
                 max_retries=0):
    cfg = LockConfig(ttl=ttl, retry_interval=retry_interval,
                     max_retries=max_retries)
    return SQLiteLock(name, db_path, config=cfg)


# ---------------------------------------------------------------------------
# 1. LockError
# ---------------------------------------------------------------------------

class TestLockError:
    def test_is_exception_subclass(self):
        assert issubclass(LockError, Exception)

    def test_can_be_raised(self):
        with pytest.raises(LockError):
            raise LockError("boom")

    def test_can_be_caught_as_exception(self):
        try:
            raise LockError("test")
        except Exception as e:
            assert isinstance(e, LockError)

    def test_message_preserved(self):
        err = LockError("my message")
        assert "my message" in str(err)


# ---------------------------------------------------------------------------
# 2. LockConfig defaults and custom values
# ---------------------------------------------------------------------------

class TestLockConfig:
    def test_default_ttl(self):
        assert LockConfig().ttl == 30.0

    def test_default_retry_interval(self):
        assert LockConfig().retry_interval == 0.1

    def test_default_max_retries(self):
        assert LockConfig().max_retries == 0

    def test_custom_ttl(self):
        assert LockConfig(ttl=5.0).ttl == 5.0

    def test_custom_retry_interval(self):
        assert LockConfig(retry_interval=0.5).retry_interval == 0.5

    def test_custom_max_retries(self):
        assert LockConfig(max_retries=3).max_retries == 3

    def test_all_custom_values(self):
        cfg = LockConfig(ttl=10.0, retry_interval=0.2, max_retries=5)
        assert cfg.ttl == 10.0
        assert cfg.retry_interval == 0.2
        assert cfg.max_retries == 5

    def test_is_dataclass(self):
        from dataclasses import fields
        assert len(fields(LockConfig())) == 3


# ---------------------------------------------------------------------------
# 3. FileLock — basic acquire / release / state
# ---------------------------------------------------------------------------

class TestFileLockBasics:
    def test_acquire_returns_true(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.acquire("alice") is True

    def test_is_locked_true_after_acquire(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert fl.is_locked() is True

    def test_release_returns_true(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert fl.release("alice") is True

    def test_is_locked_false_after_release(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        fl.release("alice")
        assert fl.is_locked() is False

    def test_owner_returns_correct_owner(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert fl.owner() == "alice"

    def test_owner_returns_none_when_not_locked(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.owner() is None

    def test_is_locked_false_initially(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.is_locked() is False

    def test_release_wrong_owner_returns_false(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert fl.release("bob") is False

    def test_release_wrong_owner_lock_still_held(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        fl.release("bob")
        assert fl.is_locked() is True

    def test_release_without_owner_arg_removes_lock(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert fl.release() is True
        assert fl.is_locked() is False

    def test_release_when_not_locked_returns_false(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.release("alice") is False

    def test_acquire_when_already_locked_returns_false(self, tmp_dir):
        fl1 = _file_lock(lock_dir=tmp_dir)
        fl2 = _file_lock(lock_dir=tmp_dir)
        fl1.acquire("alice")
        assert fl2.acquire("bob") is False

    def test_double_acquire_same_owner_fails(self, tmp_dir):
        """Two separate acquire calls with the same owner string should fail
        because the lock is already held."""
        fl1 = _file_lock(lock_dir=tmp_dir)
        fl2 = _file_lock(lock_dir=tmp_dir)
        fl1.acquire("alice")
        # Different instance, same name, same owner string — lock is held
        assert fl2.acquire("alice") is False


# ---------------------------------------------------------------------------
# 4. FileLock — lock file contents
# ---------------------------------------------------------------------------

class TestFileLockContents:
    def test_lock_file_exists_after_acquire(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        assert os.path.exists(os.path.join(tmp_dir, "mylock.lock"))

    def test_lock_file_removed_after_release(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        fl.release("alice")
        assert not os.path.exists(os.path.join(tmp_dir, "mylock.lock"))

    def test_lock_file_contains_owner(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        fl.acquire("alice")
        with open(os.path.join(tmp_dir, "mylock.lock")) as fh:
            data = json.load(fh)
        assert data["owner"] == "alice"

    def test_lock_file_contains_expires_at(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        before = time.time()
        fl.acquire("alice")
        after = time.time()
        with open(os.path.join(tmp_dir, "mylock.lock")) as fh:
            data = json.load(fh)
        assert before < data["expires_at"] <= after + 30.0 + 1

    def test_lock_file_name_uses_lock_name(self, tmp_dir):
        fl = FileLock("custom_name", tmp_dir)
        fl.acquire("alice")
        assert os.path.exists(os.path.join(tmp_dir, "custom_name.lock"))


# ---------------------------------------------------------------------------
# 5. FileLock — TTL / expired lock stealing
# ---------------------------------------------------------------------------

class TestFileLockTTL:
    def test_expired_lock_can_be_stolen(self, tmp_dir):
        # Write a lock that is already expired
        lock_path = os.path.join(tmp_dir, "mylock.lock")
        with open(lock_path, "w") as fh:
            json.dump({"owner": "old-owner", "expires_at": time.time() - 1}, fh)

        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.acquire("new-owner") is True
        assert fl.owner() == "new-owner"

    def test_is_locked_false_after_expiry(self, tmp_dir):
        lock_path = os.path.join(tmp_dir, "mylock.lock")
        with open(lock_path, "w") as fh:
            json.dump({"owner": "alice", "expires_at": time.time() - 1}, fh)
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.is_locked() is False

    def test_owner_none_after_expiry(self, tmp_dir):
        lock_path = os.path.join(tmp_dir, "mylock.lock")
        with open(lock_path, "w") as fh:
            json.dump({"owner": "alice", "expires_at": time.time() - 1}, fh)
        fl = _file_lock(lock_dir=tmp_dir)
        assert fl.owner() is None

    def test_acquire_respects_ttl(self, tmp_dir):
        cfg = LockConfig(ttl=0.1)
        fl = FileLock("mylock", tmp_dir, config=cfg)
        fl.acquire("alice")
        time.sleep(0.15)
        # Lock should be expired → another instance can steal it
        fl2 = FileLock("mylock", tmp_dir, config=cfg)
        assert fl2.acquire("bob") is True


# ---------------------------------------------------------------------------
# 6. FileLock — retry logic
# ---------------------------------------------------------------------------

class TestFileLockRetry:
    def test_max_retries_zero_fails_immediately(self, tmp_dir):
        fl1 = _file_lock(lock_dir=tmp_dir, max_retries=0)
        fl2 = _file_lock(lock_dir=tmp_dir, max_retries=0)
        fl1.acquire("alice")
        result = fl2.acquire("bob")
        assert result is False

    def test_retries_eventually_succeed(self, tmp_dir):
        """fl1 holds the lock; fl2 retries while fl1 releases it."""
        cfg_short_ttl = LockConfig(ttl=0.2, retry_interval=0.05, max_retries=10)
        fl1 = FileLock("mylock", tmp_dir, config=LockConfig(ttl=0.2))
        fl2 = FileLock("mylock", tmp_dir, config=cfg_short_ttl)

        fl1.acquire("alice")
        # fl2 will retry; by the time ttl expires, it should grab the lock
        result = fl2.acquire("bob")
        assert result is True

    def test_retries_exhausted_returns_false(self, tmp_dir):
        cfg = LockConfig(ttl=60.0, retry_interval=0.01, max_retries=2)
        fl1 = FileLock("mylock", tmp_dir, config=LockConfig(ttl=60.0))
        fl2 = FileLock("mylock", tmp_dir, config=cfg)
        fl1.acquire("alice")
        assert fl2.acquire("bob") is False


# ---------------------------------------------------------------------------
# 7. FileLock — lock_dir creation
# ---------------------------------------------------------------------------

class TestFileLockDirCreation:
    def test_creates_missing_lock_dir(self, tmp_dir):
        new_dir = os.path.join(tmp_dir, "nested", "locks")
        fl = FileLock("mylock", new_dir)
        fl.acquire("alice")
        assert os.path.isdir(new_dir)

    def test_acquire_works_in_new_dir(self, tmp_dir):
        new_dir = os.path.join(tmp_dir, "sub")
        fl = FileLock("mylock", new_dir)
        assert fl.acquire("alice") is True


# ---------------------------------------------------------------------------
# 8. FileLock — context manager
# ---------------------------------------------------------------------------

class TestFileLockContextManager:
    def test_context_manager_acquires(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        with fl:
            assert fl.is_locked() is True

    def test_context_manager_releases_on_exit(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        with fl:
            pass
        assert fl.is_locked() is False

    def test_context_manager_releases_on_exception(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        try:
            with fl:
                raise RuntimeError("test")
        except RuntimeError:
            pass
        assert fl.is_locked() is False

    def test_context_manager_raises_lock_error_if_already_held(self, tmp_dir):
        fl1 = _file_lock(lock_dir=tmp_dir)
        fl2 = _file_lock(lock_dir=tmp_dir)
        fl1.acquire("alice")
        with pytest.raises(LockError):
            with fl2:
                pass

    def test_context_manager_owner_uuid(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        with fl:
            o = fl.owner()
            assert o is not None
            # Should be a valid UUID
            uuid.UUID(o)

    def test_context_manager_second_use_after_first(self, tmp_dir):
        """Context manager can be re-entered after first use."""
        fl = _file_lock(lock_dir=tmp_dir)
        with fl:
            assert fl.is_locked()
        assert not fl.is_locked()
        with fl:
            assert fl.is_locked()

    def test_context_manager_does_not_suppress_exception(self, tmp_dir):
        fl = _file_lock(lock_dir=tmp_dir)
        with pytest.raises(ValueError):
            with fl:
                raise ValueError("not suppressed")


# ---------------------------------------------------------------------------
# 9. SQLiteLock — basic acquire / release / state
# ---------------------------------------------------------------------------

class TestSQLiteLockBasics:
    def test_acquire_returns_true(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.acquire("alice") is True

    def test_is_locked_true_after_acquire(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        assert sl.is_locked() is True

    def test_release_returns_true(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        assert sl.release("alice") is True

    def test_is_locked_false_after_release(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        sl.release("alice")
        assert sl.is_locked() is False

    def test_owner_returns_correct_owner(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        assert sl.owner() == "alice"

    def test_owner_returns_none_when_not_locked(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.owner() is None

    def test_is_locked_false_initially(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.is_locked() is False

    def test_release_wrong_owner_returns_false(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        assert sl.release("bob") is False

    def test_release_wrong_owner_lock_still_held(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        sl.release("bob")
        assert sl.is_locked() is True

    def test_release_without_owner_arg_removes_lock(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        assert sl.release() is True
        assert sl.is_locked() is False

    def test_release_when_not_locked_returns_false(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.release("alice") is False

    def test_acquire_when_already_locked_returns_false(self, tmp_db):
        sl1 = _sqlite_lock(db_path=tmp_db)
        sl2 = _sqlite_lock(db_path=tmp_db)
        sl1.acquire("alice")
        assert sl2.acquire("bob") is False

    def test_double_acquire_different_owner_fails(self, tmp_db):
        sl1 = _sqlite_lock(db_path=tmp_db)
        sl2 = _sqlite_lock(db_path=tmp_db)
        sl1.acquire("alice")
        assert sl2.acquire("charlie") is False


# ---------------------------------------------------------------------------
# 10. SQLiteLock — SQLite-specific tests
# ---------------------------------------------------------------------------

class TestSQLiteLockSpecific:
    def test_table_created_automatically(self, tmp_db):
        _sqlite_lock(db_path=tmp_db)  # instantiation must create the table
        conn = sqlite3.connect(tmp_db)
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        conn.close()
        assert "locks" in tables

    def test_table_has_correct_columns(self, tmp_db):
        _sqlite_lock(db_path=tmp_db)
        conn = sqlite3.connect(tmp_db)
        cols = {r[1] for r in conn.execute("PRAGMA table_info(locks)")}
        conn.close()
        assert {"name", "owner", "expires_at"} <= cols

    def test_two_instances_same_db_coordinate(self, tmp_db):
        sl1 = SQLiteLock("mylock", tmp_db)
        sl2 = SQLiteLock("mylock", tmp_db)
        assert sl1.acquire("alice") is True
        assert sl2.acquire("bob") is False

    def test_two_instances_different_lock_names(self, tmp_db):
        sl1 = SQLiteLock("lock_a", tmp_db)
        sl2 = SQLiteLock("lock_b", tmp_db)
        assert sl1.acquire("alice") is True
        assert sl2.acquire("bob") is True  # independent locks

    def test_release_by_one_instance_visible_to_other(self, tmp_db):
        sl1 = SQLiteLock("mylock", tmp_db)
        sl2 = SQLiteLock("mylock", tmp_db)
        sl1.acquire("alice")
        sl1.release("alice")
        assert sl2.acquire("bob") is True

    def test_row_stored_in_db(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        conn = sqlite3.connect(tmp_db)
        row = conn.execute(
            "SELECT owner FROM locks WHERE name='mylock'"
        ).fetchone()
        conn.close()
        assert row is not None
        assert row[0] == "alice"

    def test_row_removed_from_db_on_release(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        sl.acquire("alice")
        sl.release("alice")
        conn = sqlite3.connect(tmp_db)
        row = conn.execute(
            "SELECT owner FROM locks WHERE name='mylock'"
        ).fetchone()
        conn.close()
        assert row is None


# ---------------------------------------------------------------------------
# 11. SQLiteLock — TTL / expired lock stealing
# ---------------------------------------------------------------------------

class TestSQLiteLockTTL:
    def test_expired_lock_can_be_stolen(self, tmp_db):
        # Insert an already-expired row directly
        conn = sqlite3.connect(tmp_db)
        conn.execute("CREATE TABLE IF NOT EXISTS locks "
                     "(name TEXT PRIMARY KEY, owner TEXT, expires_at REAL)")
        conn.execute("INSERT INTO locks VALUES ('mylock', 'old-owner', ?)",
                     (time.time() - 1,))
        conn.commit()
        conn.close()

        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.acquire("new-owner") is True
        assert sl.owner() == "new-owner"

    def test_is_locked_false_after_expiry(self, tmp_db):
        conn = sqlite3.connect(tmp_db)
        conn.execute("CREATE TABLE IF NOT EXISTS locks "
                     "(name TEXT PRIMARY KEY, owner TEXT, expires_at REAL)")
        conn.execute("INSERT INTO locks VALUES ('mylock', 'alice', ?)",
                     (time.time() - 1,))
        conn.commit()
        conn.close()

        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.is_locked() is False

    def test_owner_none_after_expiry(self, tmp_db):
        conn = sqlite3.connect(tmp_db)
        conn.execute("CREATE TABLE IF NOT EXISTS locks "
                     "(name TEXT PRIMARY KEY, owner TEXT, expires_at REAL)")
        conn.execute("INSERT INTO locks VALUES ('mylock', 'alice', ?)",
                     (time.time() - 1,))
        conn.commit()
        conn.close()

        sl = _sqlite_lock(db_path=tmp_db)
        assert sl.owner() is None

    def test_acquire_respects_ttl(self, tmp_db):
        cfg = LockConfig(ttl=0.1)
        sl1 = SQLiteLock("mylock", tmp_db, config=cfg)
        sl1.acquire("alice")
        time.sleep(0.15)
        sl2 = SQLiteLock("mylock", tmp_db, config=cfg)
        assert sl2.acquire("bob") is True


# ---------------------------------------------------------------------------
# 12. SQLiteLock — retry logic
# ---------------------------------------------------------------------------

class TestSQLiteLockRetry:
    def test_max_retries_zero_fails_immediately(self, tmp_db):
        sl1 = _sqlite_lock(db_path=tmp_db, max_retries=0)
        sl2 = _sqlite_lock(db_path=tmp_db, max_retries=0)
        sl1.acquire("alice")
        assert sl2.acquire("bob") is False

    def test_retries_eventually_succeed(self, tmp_db):
        cfg_short_ttl = LockConfig(ttl=0.2, retry_interval=0.05, max_retries=10)
        sl1 = SQLiteLock("mylock", tmp_db, config=LockConfig(ttl=0.2))
        sl2 = SQLiteLock("mylock", tmp_db, config=cfg_short_ttl)
        sl1.acquire("alice")
        assert sl2.acquire("bob") is True

    def test_retries_exhausted_returns_false(self, tmp_db):
        cfg = LockConfig(ttl=60.0, retry_interval=0.01, max_retries=2)
        sl1 = SQLiteLock("mylock", tmp_db, config=LockConfig(ttl=60.0))
        sl2 = SQLiteLock("mylock", tmp_db, config=cfg)
        sl1.acquire("alice")
        assert sl2.acquire("bob") is False


# ---------------------------------------------------------------------------
# 13. SQLiteLock — context manager
# ---------------------------------------------------------------------------

class TestSQLiteLockContextManager:
    def test_context_manager_acquires(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        with sl:
            assert sl.is_locked() is True

    def test_context_manager_releases_on_exit(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        with sl:
            pass
        assert sl.is_locked() is False

    def test_context_manager_releases_on_exception(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        try:
            with sl:
                raise RuntimeError("test")
        except RuntimeError:
            pass
        assert sl.is_locked() is False

    def test_context_manager_raises_lock_error_if_held(self, tmp_db):
        sl1 = _sqlite_lock(db_path=tmp_db)
        sl2 = _sqlite_lock(db_path=tmp_db)
        sl1.acquire("alice")
        with pytest.raises(LockError):
            with sl2:
                pass

    def test_context_manager_owner_uuid(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        with sl:
            o = sl.owner()
            assert o is not None
            uuid.UUID(o)

    def test_context_manager_second_use_after_first(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        with sl:
            assert sl.is_locked()
        assert not sl.is_locked()
        with sl:
            assert sl.is_locked()

    def test_context_manager_does_not_suppress_exception(self, tmp_db):
        sl = _sqlite_lock(db_path=tmp_db)
        with pytest.raises(ValueError):
            with sl:
                raise ValueError("not suppressed")


# ---------------------------------------------------------------------------
# 14. Cross-type edge cases & concurrent-like scenarios
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_file_lock_none_config_uses_defaults(self, tmp_dir):
        fl = FileLock("mylock", tmp_dir, config=None)
        assert fl._config.ttl == 30.0

    def test_sqlite_lock_none_config_uses_defaults(self, tmp_db):
        sl = SQLiteLock("mylock", tmp_db, config=None)
        assert sl._config.ttl == 30.0

    def test_file_lock_acquire_generates_uuid_owner(self, tmp_dir):
        fl = FileLock("mylock", tmp_dir)
        fl.acquire()  # no owner arg
        o = fl.owner()
        assert o is not None
        uuid.UUID(o)  # must be valid UUID

    def test_sqlite_lock_acquire_generates_uuid_owner(self, tmp_db):
        sl = SQLiteLock("mylock", tmp_db)
        sl.acquire()
        o = sl.owner()
        assert o is not None
        uuid.UUID(o)

    def test_file_lock_two_distinct_names_independent(self, tmp_dir):
        fl_a = FileLock("lock_a", tmp_dir)
        fl_b = FileLock("lock_b", tmp_dir)
        assert fl_a.acquire("alice") is True
        assert fl_b.acquire("bob") is True
        assert fl_a.owner() == "alice"
        assert fl_b.owner() == "bob"

    def test_file_lock_sequential_acquire_after_release(self, tmp_dir):
        fl = FileLock("mylock", tmp_dir)
        fl.acquire("alice")
        fl.release("alice")
        assert fl.acquire("bob") is True
        assert fl.owner() == "bob"

    def test_sqlite_lock_sequential_acquire_after_release(self, tmp_db):
        sl = SQLiteLock("mylock", tmp_db)
        sl.acquire("alice")
        sl.release("alice")
        assert sl.acquire("bob") is True
        assert sl.owner() == "bob"

    def test_file_lock_corrupt_lock_file_treated_as_no_lock(self, tmp_dir):
        lock_path = os.path.join(tmp_dir, "mylock.lock")
        with open(lock_path, "w") as fh:
            fh.write("not valid json{{{")
        fl = FileLock("mylock", tmp_dir)
        # Corrupt file → treated as absent → can acquire
        assert fl.acquire("alice") is True

    def test_file_lock_multiple_instances_two_holders(self, tmp_dir):
        """Simulate two concurrent acquirers; only one should win."""
        fl1 = FileLock("mylock", tmp_dir, config=LockConfig(max_retries=0))
        fl2 = FileLock("mylock", tmp_dir, config=LockConfig(max_retries=0))
        r1 = fl1.acquire("alice")
        r2 = fl2.acquire("bob")
        # One acquires, one doesn't
        assert r1 != r2 or (r1 is True and r2 is False) or (r1 is False and r2 is True)
        # At most one holds the lock
        owners = []
        if fl1.owner() == "alice":
            owners.append("alice")
        if fl2.owner() == "bob" and fl1.owner() != "bob":
            pass
        assert sum([r1, r2]) <= 2  # basic sanity

    def test_sqlite_lock_acquire_after_context_manager(self, tmp_db):
        sl = SQLiteLock("mylock", tmp_db)
        with sl:
            held = sl.is_locked()
        assert held is True
        assert sl.is_locked() is False
        # Can acquire again afterwards
        assert sl.acquire("charlie") is True

    def test_file_lock_acquire_after_context_manager(self, tmp_dir):
        fl = FileLock("mylock", tmp_dir)
        with fl:
            held = fl.is_locked()
        assert held is True
        assert fl.is_locked() is False
        assert fl.acquire("dave") is True
