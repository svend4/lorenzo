"""Tests for docstoolkit.atomic_ops (E96)."""
import threading
import pytest

from docstoolkit.atomic_ops import (
    OpResult,
    AtomicStore,
    TransactionError,
    AtomicTransaction,
)


# ---------------------------------------------------------------------------
# OpResult
# ---------------------------------------------------------------------------

class TestOpResult:
    def test_success_result(self):
        r = OpResult(success=True, value=42, previous=None, error="")
        assert r.success
        assert r.value == 42
        assert r.previous is None
        assert r.error == ""

    def test_failure_result(self):
        r = OpResult(success=False, value=None, previous=10, error="CAS mismatch")
        assert not r.success
        assert r.error == "CAS mismatch"
        assert r.previous == 10


# ---------------------------------------------------------------------------
# AtomicStore — basic operations
# ---------------------------------------------------------------------------

class TestAtomicStoreBasic:
    def test_get_missing(self):
        s = AtomicStore()
        assert s.get("x") is None

    def test_get_default(self):
        s = AtomicStore()
        assert s.get("x", 99) == 99

    def test_set_and_get(self):
        s = AtomicStore()
        s.set("k", "v")
        assert s.get("k") == "v"

    def test_set_returns_version(self):
        s = AtomicStore()
        v1 = s.set("k", "a")
        assert v1 == 1
        v2 = s.set("k", "b")
        assert v2 == 2

    def test_set_overwrites(self):
        s = AtomicStore()
        s.set("k", "first")
        s.set("k", "second")
        assert s.get("k") == "second"

    def test_exists_false(self):
        s = AtomicStore()
        assert not s.exists("k")

    def test_exists_true(self):
        s = AtomicStore()
        s.set("k", 1)
        assert s.exists("k")

    def test_delete_existing(self):
        s = AtomicStore()
        s.set("k", 1)
        assert s.delete("k")
        assert not s.exists("k")

    def test_delete_missing(self):
        s = AtomicStore()
        assert not s.delete("k")

    def test_version_missing(self):
        s = AtomicStore()
        assert s.version("k") == 0

    def test_version_increments(self):
        s = AtomicStore()
        s.set("k", 1)
        assert s.version("k") == 1
        s.set("k", 2)
        assert s.version("k") == 2

    def test_key_type_check(self):
        s = AtomicStore()
        with pytest.raises(TypeError):
            s.get(123)
        with pytest.raises(TypeError):
            s.set(123, "v")
        with pytest.raises(TypeError):
            s.delete(123)
        with pytest.raises(TypeError):
            s.exists(123)
        with pytest.raises(TypeError):
            s.version(123)

    def test_close(self):
        s = AtomicStore()
        s.close()
        with pytest.raises(RuntimeError):
            s.get("k")


# ---------------------------------------------------------------------------
# AtomicStore — value types
# ---------------------------------------------------------------------------

class TestAtomicStoreValueTypes:
    def test_integer(self):
        s = AtomicStore()
        s.set("n", 42)
        assert s.get("n") == 42

    def test_float(self):
        s = AtomicStore()
        s.set("f", 3.14)
        assert s.get("f") == pytest.approx(3.14)

    def test_string(self):
        s = AtomicStore()
        s.set("s", "hello")
        assert s.get("s") == "hello"

    def test_bool(self):
        s = AtomicStore()
        s.set("b", True)
        assert s.get("b") is True

    def test_none(self):
        s = AtomicStore()
        s.set("n", None)
        # After set, exists should be true
        assert s.exists("n")
        # get returns None (the value)
        assert s.get("n") is None

    def test_list(self):
        s = AtomicStore()
        s.set("l", [1, 2, 3])
        assert s.get("l") == [1, 2, 3]

    def test_dict(self):
        s = AtomicStore()
        s.set("d", {"a": 1, "b": [2, 3]})
        assert s.get("d") == {"a": 1, "b": [2, 3]}

    def test_empty_string(self):
        s = AtomicStore()
        s.set("e", "")
        assert s.get("e") == ""

    def test_zero(self):
        s = AtomicStore()
        s.set("z", 0)
        assert s.get("z") == 0


# ---------------------------------------------------------------------------
# AtomicStore — CAS
# ---------------------------------------------------------------------------

class TestAtomicStoreCAS:
    def test_cas_success(self):
        s = AtomicStore()
        s.set("k", 10)
        result = s.cas("k", 10, 20)
        assert result.success
        assert result.value == 20
        assert result.previous == 10
        assert s.get("k") == 20

    def test_cas_mismatch(self):
        s = AtomicStore()
        s.set("k", 10)
        result = s.cas("k", 99, 20)
        assert not result.success
        assert result.previous == 10
        assert s.get("k") == 10  # unchanged

    def test_cas_missing_key_with_none(self):
        s = AtomicStore()
        result = s.cas("k", None, "new")
        assert result.success
        assert s.get("k") == "new"

    def test_cas_missing_key_wrong_expected(self):
        s = AtomicStore()
        result = s.cas("k", "wrong", "new")
        assert not result.success
        assert result.previous is None

    def test_cas_sequential(self):
        s = AtomicStore()
        s.set("counter", 0)
        for expected in range(5):
            r = s.cas("counter", expected, expected + 1)
            assert r.success
        assert s.get("counter") == 5

    def test_cas_key_type_check(self):
        s = AtomicStore()
        with pytest.raises(TypeError):
            s.cas(123, None, 1)


# ---------------------------------------------------------------------------
# AtomicStore — increment / decrement
# ---------------------------------------------------------------------------

class TestAtomicStoreIncrement:
    def test_increment_new_key(self):
        s = AtomicStore()
        val = s.increment("c")
        assert val == 1
        assert s.get("c") == 1

    def test_increment_existing(self):
        s = AtomicStore()
        s.set("c", 5)
        val = s.increment("c", 3)
        assert val == 8

    def test_increment_default_delta(self):
        s = AtomicStore()
        s.set("c", 0)
        s.increment("c")
        s.increment("c")
        assert s.get("c") == 2

    def test_increment_negative_delta(self):
        s = AtomicStore()
        s.set("c", 10)
        val = s.increment("c", -4)
        assert val == 6

    def test_decrement(self):
        s = AtomicStore()
        s.set("c", 10)
        val = s.decrement("c", 3)
        assert val == 7

    def test_decrement_new_key(self):
        s = AtomicStore()
        val = s.decrement("c", 1)
        assert val == -1

    def test_increment_float_value(self):
        s = AtomicStore()
        s.set("c", 1.5)
        val = s.increment("c", 2)
        assert val == 3

    def test_increment_non_numeric_raises(self):
        s = AtomicStore()
        s.set("k", "string")
        with pytest.raises(TypeError):
            s.increment("k")

    def test_increment_delta_type_check(self):
        s = AtomicStore()
        with pytest.raises(TypeError):
            s.increment("k", 1.5)

    def test_increment_bool_delta_rejected(self):
        s = AtomicStore()
        with pytest.raises(TypeError):
            s.increment("k", True)

    def test_concurrent_increments(self):
        s = AtomicStore()
        s.set("c", 0)
        errors = []

        def inc():
            try:
                for _ in range(10):
                    s.increment("c")
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=inc) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert s.get("c") == 100


# ---------------------------------------------------------------------------
# AtomicStore — getset
# ---------------------------------------------------------------------------

class TestAtomicStoreGetSet:
    def test_getset_new_key(self):
        s = AtomicStore()
        prev = s.getset("k", "new")
        assert prev is None
        assert s.get("k") == "new"

    def test_getset_existing_key(self):
        s = AtomicStore()
        s.set("k", "old")
        prev = s.getset("k", "new")
        assert prev == "old"
        assert s.get("k") == "new"

    def test_getset_type_check(self):
        s = AtomicStore()
        with pytest.raises(TypeError):
            s.getset(123, "v")


# ---------------------------------------------------------------------------
# AtomicTransaction
# ---------------------------------------------------------------------------

class TestAtomicTransaction:
    def test_basic_commit(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            tx.set("a", 1)
            tx.set("b", 2)
        assert s.get("a") == 1
        assert s.get("b") == 2

    def test_rollback_on_exception(self):
        s = AtomicStore()
        s.set("a", 0)
        with pytest.raises(ValueError):
            with AtomicTransaction(s) as tx:
                tx.set("a", 99)
                raise ValueError("intentional")
        assert s.get("a") == 0  # rolled back

    def test_get_inside_transaction(self):
        s = AtomicStore()
        s.set("k", 42)
        with AtomicTransaction(s) as tx:
            val = tx.get("k")
        assert val == 42

    def test_get_default_inside_transaction(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            val = tx.get("missing", "default")
        assert val == "default"

    def test_increment_inside_transaction(self):
        s = AtomicStore()
        s.set("c", 5)
        with AtomicTransaction(s) as tx:
            val = tx.increment("c", 3)
        assert val == 8
        assert s.get("c") == 8

    def test_decrement_inside_transaction(self):
        s = AtomicStore()
        s.set("c", 10)
        with AtomicTransaction(s) as tx:
            val = tx.decrement("c", 4)
        assert val == 6
        assert s.get("c") == 6

    def test_increment_rollback(self):
        s = AtomicStore()
        s.set("c", 10)
        with pytest.raises(RuntimeError):
            with AtomicTransaction(s) as tx:
                tx.increment("c", 5)
                raise RuntimeError("fail")
        assert s.get("c") == 10  # rolled back

    def test_cas_inside_transaction(self):
        s = AtomicStore()
        s.set("k", 1)
        with AtomicTransaction(s) as tx:
            r = tx.cas("k", 1, 100)
        assert r.success
        assert s.get("k") == 100

    def test_cas_mismatch_inside_transaction(self):
        s = AtomicStore()
        s.set("k", 1)
        with AtomicTransaction(s) as tx:
            r = tx.cas("k", 99, 100)
        assert not r.success
        assert s.get("k") == 1  # unchanged

    def test_version_increments_in_tx(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            v1 = tx.set("k", "a")
            assert v1 == 1
            v2 = tx.set("k", "b")
            assert v2 == 2
        assert s.version("k") == 2

    def test_not_active_outside_context(self):
        s = AtomicStore()
        tx = AtomicTransaction(s)
        with pytest.raises(TransactionError):
            tx.get("k")
        with pytest.raises(TransactionError):
            tx.set("k", 1)

    def test_double_enter_raises(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            with pytest.raises(TransactionError):
                tx.__enter__()

    def test_type_check_store(self):
        with pytest.raises(TypeError):
            AtomicTransaction("not a store")

    def test_key_type_check_in_tx(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            with pytest.raises(TypeError):
                tx.get(123)
            with pytest.raises(TypeError):
                tx.set(123, 1)

    def test_increment_non_numeric_in_tx_does_not_commit(self):
        s = AtomicStore()
        s.set("good", 5)
        s.set("bad", "string")
        with pytest.raises(TypeError):
            with AtomicTransaction(s) as tx:
                tx.increment("good", 1)
                tx.increment("bad", 1)  # raises TypeError
        # Transaction rolled back, good should be unchanged
        assert s.get("good") == 5

    def test_multiple_operations_commit_atomically(self):
        s = AtomicStore()
        s.set("x", 0)
        s.set("y", 0)
        with AtomicTransaction(s) as tx:
            tx.increment("x", 5)
            tx.increment("y", 10)
        assert s.get("x") == 5
        assert s.get("y") == 10

    def test_new_key_in_transaction(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            v = tx.set("new_key", "value")
        assert v == 1
        assert s.get("new_key") == "value"

    def test_increment_new_key_in_transaction(self):
        s = AtomicStore()
        with AtomicTransaction(s) as tx:
            val = tx.increment("counter", 7)
        assert val == 7
        assert s.get("counter") == 7
