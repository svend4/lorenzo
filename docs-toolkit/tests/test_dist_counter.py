"""Tests for the dist_counter module — 90+ tests covering all spec requirements."""
import os
import sqlite3
import tempfile
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import pytest

from docstoolkit.dist_counter import (
    CounterError,
    CounterValue,
    CounterStore,
    HierarchicalCounter,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


@pytest.fixture()
def tmp_db_path(tmp_dir):
    return os.path.join(tmp_dir, "counters.db")


@pytest.fixture()
def store():
    s = CounterStore()  # in-memory
    yield s
    s.close()


@pytest.fixture()
def store_disk(tmp_db_path):
    s = CounterStore(tmp_db_path)
    yield s
    s.close()


# ---------------------------------------------------------------------------
# 1. CounterError
# ---------------------------------------------------------------------------

class TestCounterError:
    def test_is_exception_subclass(self):
        assert issubclass(CounterError, Exception)

    def test_can_be_raised(self):
        with pytest.raises(CounterError):
            raise CounterError("boom")

    def test_can_be_caught_as_exception(self):
        try:
            raise CounterError("test")
        except Exception as e:
            assert isinstance(e, CounterError)

    def test_message_preserved(self):
        err = CounterError("my message")
        assert "my message" in str(err)


# ---------------------------------------------------------------------------
# 2. CounterValue dataclass
# ---------------------------------------------------------------------------

class TestCounterValue:
    def test_construct_with_positional(self):
        cv = CounterValue("foo", 5, 123.0)
        assert cv.key == "foo"
        assert cv.value == 5
        assert cv.updated_at == 123.0

    def test_construct_with_kwargs(self):
        cv = CounterValue(key="bar", value=10, updated_at=456.0)
        assert cv.key == "bar"
        assert cv.value == 10
        assert cv.updated_at == 456.0

    def test_is_dataclass(self):
        from dataclasses import fields
        cv = CounterValue("k", 0, 0.0)
        assert len(fields(cv)) == 3

    def test_equality(self):
        a = CounterValue("k", 1, 1.0)
        b = CounterValue("k", 1, 1.0)
        assert a == b

    def test_inequality_different_value(self):
        a = CounterValue("k", 1, 1.0)
        b = CounterValue("k", 2, 1.0)
        assert a != b

    def test_inequality_different_key(self):
        a = CounterValue("k1", 1, 1.0)
        b = CounterValue("k2", 1, 1.0)
        assert a != b

    def test_value_is_int(self):
        cv = CounterValue("k", 42, 1.0)
        assert isinstance(cv.value, int)

    def test_updated_at_is_float(self):
        cv = CounterValue("k", 1, 1.5)
        assert isinstance(cv.updated_at, float)


# ---------------------------------------------------------------------------
# 3. CounterStore — construction
# ---------------------------------------------------------------------------

class TestCounterStoreConstruction:
    def test_default_db_path_is_memory(self):
        s = CounterStore()
        assert s.count() == 0
        s.close()

    def test_explicit_memory(self):
        s = CounterStore(":memory:")
        assert s.count() == 0
        s.close()

    def test_disk_db_creates_file(self, tmp_db_path):
        s = CounterStore(tmp_db_path)
        assert os.path.exists(tmp_db_path)
        s.close()

    def test_creates_counters_table(self, tmp_db_path):
        s = CounterStore(tmp_db_path)
        s.close()
        conn = sqlite3.connect(tmp_db_path)
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        conn.close()
        assert "counters" in tables

    def test_counters_table_columns(self, tmp_db_path):
        s = CounterStore(tmp_db_path)
        s.close()
        conn = sqlite3.connect(tmp_db_path)
        cols = {r[1] for r in conn.execute("PRAGMA table_info(counters)")}
        conn.close()
        assert {"key", "value", "updated_at"} <= cols


# ---------------------------------------------------------------------------
# 4. CounterStore.increment
# ---------------------------------------------------------------------------

class TestIncrement:
    def test_increment_new_key_returns_1(self, store):
        assert store.increment("foo") == 1

    def test_increment_new_key_default_delta(self, store):
        store.increment("foo")
        assert store.get("foo") == 1

    def test_increment_existing_key_returns_new_value(self, store):
        store.increment("foo")
        result = store.increment("foo")
        assert result == 2

    def test_increment_with_delta(self, store):
        assert store.increment("foo", 5) == 5

    def test_increment_with_delta_existing(self, store):
        store.increment("foo", 5)
        assert store.increment("foo", 3) == 8

    def test_increment_with_negative_delta(self, store):
        store.increment("foo", 10)
        assert store.increment("foo", -3) == 7

    def test_increment_zero_delta(self, store):
        store.increment("foo", 5)
        assert store.increment("foo", 0) == 5

    def test_increment_persists(self, store_disk, tmp_db_path):
        store_disk.increment("foo", 7)
        store_disk.close()
        # Re-open the store
        s2 = CounterStore(tmp_db_path)
        assert s2.get("foo") == 7
        s2.close()

    def test_increment_multiple_keys_independent(self, store):
        store.increment("a", 1)
        store.increment("b", 2)
        store.increment("a", 1)
        assert store.get("a") == 2
        assert store.get("b") == 2

    def test_increment_updates_updated_at(self, store):
        before = time.time()
        store.increment("foo")
        cv = store.get_value("foo")
        after = time.time()
        assert before <= cv.updated_at <= after + 1

    def test_increment_returns_int(self, store):
        result = store.increment("foo", 1)
        assert isinstance(result, int)


# ---------------------------------------------------------------------------
# 5. CounterStore.decrement
# ---------------------------------------------------------------------------

class TestDecrement:
    def test_decrement_new_key_returns_neg_1(self, store):
        assert store.decrement("foo") == -1

    def test_decrement_default_delta(self, store):
        store.increment("foo", 5)
        assert store.decrement("foo") == 4

    def test_decrement_with_delta(self, store):
        store.increment("foo", 10)
        assert store.decrement("foo", 3) == 7

    def test_decrement_below_zero(self, store):
        store.increment("foo", 2)
        assert store.decrement("foo", 5) == -3

    def test_decrement_persists(self, store):
        store.increment("foo", 10)
        store.decrement("foo", 4)
        assert store.get("foo") == 6

    def test_decrement_zero_delta(self, store):
        store.increment("foo", 5)
        assert store.decrement("foo", 0) == 5


# ---------------------------------------------------------------------------
# 6. CounterStore.get
# ---------------------------------------------------------------------------

class TestGet:
    def test_get_missing_returns_zero(self, store):
        assert store.get("nope") == 0

    def test_get_after_increment(self, store):
        store.increment("foo", 3)
        assert store.get("foo") == 3

    def test_get_after_multiple_increments(self, store):
        store.increment("foo", 2)
        store.increment("foo", 3)
        assert store.get("foo") == 5

    def test_get_returns_int(self, store):
        store.increment("foo")
        assert isinstance(store.get("foo"), int)

    def test_get_after_set(self, store):
        store.set("foo", 42)
        assert store.get("foo") == 42

    def test_get_after_delete_returns_zero(self, store):
        store.increment("foo", 5)
        store.delete("foo")
        assert store.get("foo") == 0


# ---------------------------------------------------------------------------
# 7. CounterStore.get_value
# ---------------------------------------------------------------------------

class TestGetValue:
    def test_get_value_missing_returns_none(self, store):
        assert store.get_value("nope") is None

    def test_get_value_returns_counter_value(self, store):
        store.increment("foo", 5)
        cv = store.get_value("foo")
        assert isinstance(cv, CounterValue)

    def test_get_value_correct_key(self, store):
        store.increment("foo", 5)
        cv = store.get_value("foo")
        assert cv.key == "foo"

    def test_get_value_correct_value(self, store):
        store.increment("foo", 5)
        cv = store.get_value("foo")
        assert cv.value == 5

    def test_get_value_has_updated_at(self, store):
        before = time.time()
        store.increment("foo")
        after = time.time()
        cv = store.get_value("foo")
        assert before <= cv.updated_at <= after + 1

    def test_get_value_after_set(self, store):
        store.set("foo", 100)
        cv = store.get_value("foo")
        assert cv.value == 100


# ---------------------------------------------------------------------------
# 8. CounterStore.set
# ---------------------------------------------------------------------------

class TestSet:
    def test_set_creates_new_key(self, store):
        store.set("foo", 42)
        assert store.get("foo") == 42

    def test_set_overwrites_existing(self, store):
        store.increment("foo", 5)
        store.set("foo", 100)
        assert store.get("foo") == 100

    def test_set_returns_none(self, store):
        assert store.set("foo", 1) is None

    def test_set_negative_value(self, store):
        store.set("foo", -10)
        assert store.get("foo") == -10

    def test_set_zero(self, store):
        store.set("foo", 0)
        assert store.get("foo") == 0
        # key should still exist
        assert store.get_value("foo") is not None

    def test_set_persists(self, store_disk, tmp_db_path):
        store_disk.set("foo", 99)
        store_disk.close()
        s2 = CounterStore(tmp_db_path)
        assert s2.get("foo") == 99
        s2.close()

    def test_set_updates_updated_at(self, store):
        store.set("foo", 1)
        cv1 = store.get_value("foo")
        time.sleep(0.01)
        store.set("foo", 2)
        cv2 = store.get_value("foo")
        assert cv2.updated_at >= cv1.updated_at


# ---------------------------------------------------------------------------
# 9. CounterStore.delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_returns_true(self, store):
        store.increment("foo")
        assert store.delete("foo") is True

    def test_delete_missing_returns_false(self, store):
        assert store.delete("nope") is False

    def test_delete_removes_key(self, store):
        store.increment("foo", 5)
        store.delete("foo")
        assert store.get_value("foo") is None

    def test_delete_double_returns_false_second_time(self, store):
        store.increment("foo")
        assert store.delete("foo") is True
        assert store.delete("foo") is False

    def test_delete_does_not_affect_other_keys(self, store):
        store.increment("a", 1)
        store.increment("b", 2)
        store.delete("a")
        assert store.get("b") == 2


# ---------------------------------------------------------------------------
# 10. CounterStore.list_all
# ---------------------------------------------------------------------------

class TestListAll:
    def test_list_all_empty(self, store):
        assert store.list_all() == []

    def test_list_all_returns_counter_values(self, store):
        store.increment("foo", 1)
        result = store.list_all()
        assert len(result) == 1
        assert isinstance(result[0], CounterValue)

    def test_list_all_returns_all_keys(self, store):
        store.increment("a", 1)
        store.increment("b", 2)
        store.increment("c", 3)
        keys = [cv.key for cv in store.list_all()]
        assert set(keys) == {"a", "b", "c"}

    def test_list_all_sorted_by_key(self, store):
        store.increment("c", 1)
        store.increment("a", 1)
        store.increment("b", 1)
        result = store.list_all()
        assert [cv.key for cv in result] == ["a", "b", "c"]

    def test_list_all_with_prefix(self, store):
        store.increment("users.alice", 1)
        store.increment("users.bob", 2)
        store.increment("admins.root", 3)
        result = store.list_all(prefix="users.")
        assert {cv.key for cv in result} == {"users.alice", "users.bob"}

    def test_list_all_prefix_no_match(self, store):
        store.increment("foo", 1)
        assert store.list_all(prefix="bar") == []

    def test_list_all_empty_prefix_returns_all(self, store):
        store.increment("foo", 1)
        store.increment("bar", 2)
        result = store.list_all(prefix="")
        assert len(result) == 2

    def test_list_all_prefix_matches_exact(self, store):
        store.increment("foo", 1)
        store.increment("foobar", 2)
        result = store.list_all(prefix="foo")
        assert {cv.key for cv in result} == {"foo", "foobar"}

    def test_list_all_prefix_sorted(self, store):
        store.increment("users.z", 1)
        store.increment("users.a", 1)
        store.increment("users.m", 1)
        result = store.list_all(prefix="users.")
        assert [cv.key for cv in result] == ["users.a", "users.m", "users.z"]

    def test_list_all_with_special_chars_in_prefix(self, store):
        # Underscores and percent signs are SQL LIKE wildcards; we must
        # escape them so they match literally.
        store.set("a_b", 1)
        store.set("axb", 2)
        result = store.list_all(prefix="a_")
        assert {cv.key for cv in result} == {"a_b"}

    def test_list_all_includes_correct_values(self, store):
        store.set("foo", 42)
        result = store.list_all()
        assert result[0].value == 42


# ---------------------------------------------------------------------------
# 11. CounterStore.total
# ---------------------------------------------------------------------------

class TestTotal:
    def test_total_empty_returns_zero(self, store):
        assert store.total() == 0

    def test_total_no_prefix_sums_all(self, store):
        store.set("a", 1)
        store.set("b", 2)
        store.set("c", 3)
        assert store.total() == 6

    def test_total_with_prefix(self, store):
        store.set("users.alice", 5)
        store.set("users.bob", 3)
        store.set("admins.root", 100)
        assert store.total(prefix="users.") == 8

    def test_total_prefix_no_match(self, store):
        store.set("a", 1)
        assert store.total(prefix="nope") == 0

    def test_total_includes_negatives(self, store):
        store.set("a", 5)
        store.set("b", -3)
        assert store.total() == 2

    def test_total_with_empty_prefix(self, store):
        store.set("a", 10)
        store.set("b", 20)
        assert store.total(prefix="") == 30

    def test_total_returns_int(self, store):
        store.set("a", 1)
        assert isinstance(store.total(), int)

    def test_total_after_delete(self, store):
        store.set("a", 5)
        store.set("b", 3)
        store.delete("a")
        assert store.total() == 3


# ---------------------------------------------------------------------------
# 12. CounterStore.count
# ---------------------------------------------------------------------------

class TestCount:
    def test_count_empty(self, store):
        assert store.count() == 0

    def test_count_after_increment(self, store):
        store.increment("foo")
        assert store.count() == 1

    def test_count_multiple_keys(self, store):
        store.increment("a")
        store.increment("b")
        store.increment("c")
        assert store.count() == 3

    def test_count_after_delete(self, store):
        store.increment("a")
        store.increment("b")
        store.delete("a")
        assert store.count() == 1

    def test_count_after_repeat_increment(self, store):
        store.increment("a")
        store.increment("a")
        assert store.count() == 1

    def test_count_returns_int(self, store):
        assert isinstance(store.count(), int)


# ---------------------------------------------------------------------------
# 13. CounterStore.reset
# ---------------------------------------------------------------------------

class TestReset:
    def test_reset_empty_returns_zero(self, store):
        assert store.reset() == 0

    def test_reset_all_returns_count(self, store):
        store.increment("a")
        store.increment("b")
        store.increment("c")
        assert store.reset() == 3

    def test_reset_all_deletes_all(self, store):
        store.increment("a")
        store.increment("b")
        store.reset()
        assert store.count() == 0

    def test_reset_with_prefix(self, store):
        store.set("users.a", 1)
        store.set("users.b", 2)
        store.set("admins.root", 3)
        deleted = store.reset(prefix="users.")
        assert deleted == 2
        assert store.count() == 1
        assert store.get("admins.root") == 3

    def test_reset_prefix_no_match(self, store):
        store.increment("foo")
        assert store.reset(prefix="bar") == 0
        assert store.count() == 1

    def test_reset_empty_prefix_deletes_all(self, store):
        store.increment("a")
        store.increment("b")
        deleted = store.reset(prefix="")
        assert deleted == 2

    def test_reset_returns_int(self, store):
        store.increment("a")
        assert isinstance(store.reset(), int)


# ---------------------------------------------------------------------------
# 14. CounterStore.close
# ---------------------------------------------------------------------------

class TestClose:
    def test_close_returns_none(self):
        s = CounterStore()
        assert s.close() is None

    def test_close_idempotent(self):
        s = CounterStore()
        s.close()
        s.close()  # second call should not raise


# ---------------------------------------------------------------------------
# 15. CounterStore — disk persistence
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_disk_persists_across_sessions(self, tmp_db_path):
        s1 = CounterStore(tmp_db_path)
        s1.increment("foo", 10)
        s1.set("bar", 5)
        s1.close()
        s2 = CounterStore(tmp_db_path)
        assert s2.get("foo") == 10
        assert s2.get("bar") == 5
        s2.close()

    def test_disk_count_persists(self, tmp_db_path):
        s1 = CounterStore(tmp_db_path)
        s1.increment("a")
        s1.increment("b")
        s1.close()
        s2 = CounterStore(tmp_db_path)
        assert s2.count() == 2
        s2.close()

    def test_disk_list_all_persists(self, tmp_db_path):
        s1 = CounterStore(tmp_db_path)
        s1.set("z", 1)
        s1.set("a", 2)
        s1.close()
        s2 = CounterStore(tmp_db_path)
        keys = [cv.key for cv in s2.list_all()]
        assert keys == ["a", "z"]
        s2.close()


# ---------------------------------------------------------------------------
# 16. CounterStore — thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_increment_in_memory_total(self):
        store = CounterStore()
        n = 200
        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(store.increment, "counter") for _ in range(n)]
            for f in as_completed(futures):
                f.result()
        assert store.get("counter") == n
        store.close()

    def test_concurrent_increment_disk_total(self, tmp_db_path):
        store = CounterStore(tmp_db_path)
        n = 200
        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = [ex.submit(store.increment, "counter") for _ in range(n)]
            for f in as_completed(futures):
                f.result()
        assert store.get("counter") == n
        store.close()

    def test_concurrent_increment_distinct_keys(self):
        store = CounterStore()
        n = 50
        keys = [f"key_{i}" for i in range(n)]

        def bump(k):
            store.increment(k, 1)

        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = [ex.submit(bump, k) for k in keys for _ in range(3)]
            for f in as_completed(futures):
                f.result()
        for k in keys:
            assert store.get(k) == 3
        assert store.count() == n
        store.close()

    def test_concurrent_increment_with_varying_delta(self):
        store = CounterStore()
        deltas = [1, 2, 3, 4, 5] * 40
        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = [ex.submit(store.increment, "k", d) for d in deltas]
            for f in as_completed(futures):
                f.result()
        assert store.get("k") == sum(deltas)
        store.close()

    def test_concurrent_mixed_increment_decrement(self):
        store = CounterStore()
        n = 100

        def do_inc():
            store.increment("k", 2)

        def do_dec():
            store.decrement("k", 1)

        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = []
            for _ in range(n):
                futures.append(ex.submit(do_inc))
                futures.append(ex.submit(do_dec))
            for f in as_completed(futures):
                f.result()
        # +2n - 1n = +n
        assert store.get("k") == n
        store.close()


# ---------------------------------------------------------------------------
# 17. CounterStore — error handling
# ---------------------------------------------------------------------------

class TestErrors:
    def test_increment_non_int_delta_raises(self, store):
        with pytest.raises(CounterError):
            store.increment("foo", 1.5)

    def test_increment_string_delta_raises(self, store):
        with pytest.raises(CounterError):
            store.increment("foo", "1")

    def test_increment_non_string_key_raises(self, store):
        with pytest.raises(CounterError):
            store.increment(123, 1)

    def test_set_non_int_value_raises(self, store):
        with pytest.raises(CounterError):
            store.set("foo", 1.5)

    def test_set_string_value_raises(self, store):
        with pytest.raises(CounterError):
            store.set("foo", "1")


# ---------------------------------------------------------------------------
# 18. HierarchicalCounter — basic
# ---------------------------------------------------------------------------

class TestHierarchicalBasic:
    def test_increment_simple_path(self, store):
        hc = HierarchicalCounter(store)
        assert hc.increment(["users", "active"]) == 1

    def test_increment_writes_joined_key(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active"])
        assert store.get("users.active") == 1

    def test_get_returns_leaf_value(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active"], 5)
        assert hc.get(["users", "active"]) == 5

    def test_get_missing_returns_zero(self, store):
        hc = HierarchicalCounter(store)
        assert hc.get(["nope"]) == 0

    def test_increment_with_custom_separator(self, store):
        hc = HierarchicalCounter(store, separator="/")
        hc.increment(["a", "b", "c"])
        assert store.get("a/b/c") == 1

    def test_increment_with_delta(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["x"], 7)
        assert hc.get(["x"]) == 7

    def test_increment_single_component(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["root"])
        assert hc.get(["root"]) == 1
        assert store.get("root") == 1


# ---------------------------------------------------------------------------
# 19. HierarchicalCounter — rollup
# ---------------------------------------------------------------------------

class TestHierarchicalRollup:
    def test_rollup_sums_descendants(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active", "premium"], 5)
        hc.increment(["users", "active", "free"], 3)
        hc.increment(["users", "inactive"], 2)
        assert hc.rollup(["users", "active"]) == 8

    def test_rollup_all_users(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active", "premium"], 5)
        hc.increment(["users", "active", "free"], 3)
        hc.increment(["users", "inactive"], 2)
        assert hc.rollup(["users"]) == 10

    def test_rollup_includes_self(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users"], 10)
        hc.increment(["users", "active"], 5)
        assert hc.rollup(["users"]) == 15

    def test_rollup_leaf_only_returns_leaf(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["a"], 7)
        assert hc.rollup(["a"]) == 7

    def test_rollup_empty_returns_zero(self, store):
        hc = HierarchicalCounter(store)
        assert hc.rollup(["nope"]) == 0

    def test_rollup_does_not_match_sibling_prefix(self, store):
        """Rollup of ["user"] must not match keys starting with "users." """
        hc = HierarchicalCounter(store)
        hc.increment(["user"], 1)
        hc.increment(["users", "active"], 100)
        assert hc.rollup(["user"]) == 1

    def test_rollup_root_path_sums_all(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users"], 1)
        hc.increment(["users", "active"], 2)
        hc.increment(["admins"], 5)
        assert hc.rollup([]) == 8


# ---------------------------------------------------------------------------
# 20. HierarchicalCounter — children
# ---------------------------------------------------------------------------

class TestHierarchicalChildren:
    def test_children_direct_only(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active", "premium"], 1)
        hc.increment(["users", "active", "free"], 1)
        hc.increment(["users", "active", "premium", "us"], 1)
        result = hc.children(["users", "active"])
        assert set(result) == {"users.active.free", "users.active.premium"}

    def test_children_sorted(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["root", "z"], 1)
        hc.increment(["root", "a"], 1)
        hc.increment(["root", "m"], 1)
        assert hc.children(["root"]) == ["root.a", "root.m", "root.z"]

    def test_children_empty(self, store):
        hc = HierarchicalCounter(store)
        assert hc.children(["nope"]) == []

    def test_children_root(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active"], 1)
        hc.increment(["admins", "root"], 1)
        result = hc.children([])
        assert set(result) == {"users", "admins"}

    def test_children_no_duplicates(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active", "a"], 1)
        hc.increment(["users", "active", "b"], 1)
        # Both descendants share "active" as the direct child of "users"
        result = hc.children(["users"])
        assert result == ["users.active"]

    def test_children_with_separator(self, store):
        hc = HierarchicalCounter(store, separator="/")
        hc.increment(["a", "b"], 1)
        hc.increment(["a", "c"], 1)
        assert hc.children(["a"]) == ["a/b", "a/c"]


# ---------------------------------------------------------------------------
# 21. HierarchicalCounter — tree
# ---------------------------------------------------------------------------

class TestHierarchicalTree:
    def test_tree_root_basic(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active"], 5)
        hc.increment(["users", "inactive"], 3)
        tree = hc.tree()
        assert "users" in tree
        assert "active" in tree["users"]
        assert "inactive" in tree["users"]

    def test_tree_leaf_value(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active"], 5)
        tree = hc.tree()
        assert tree["users"]["active"]["_value"] == 5

    def test_tree_under_path(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["users", "active", "premium"], 7)
        hc.increment(["users", "active", "free"], 3)
        tree = hc.tree(["users", "active"])
        assert tree["premium"]["_value"] == 7
        assert tree["free"]["_value"] == 3

    def test_tree_empty(self, store):
        hc = HierarchicalCounter(store)
        assert hc.tree() == {}

    def test_tree_under_missing_path(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["a", "b"], 1)
        assert hc.tree(["nope"]) == {}

    def test_tree_nested_structure(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["a", "b", "c"], 1)
        hc.increment(["a", "b", "d"], 2)
        hc.increment(["a", "e"], 3)
        tree = hc.tree(["a"])
        assert tree["b"]["c"]["_value"] == 1
        assert tree["b"]["d"]["_value"] == 2
        assert tree["e"]["_value"] == 3

    def test_tree_returns_dict(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["x"], 1)
        assert isinstance(hc.tree(), dict)

    def test_tree_includes_intermediate_levels(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["a", "b", "c"], 5)
        tree = hc.tree()
        # The path a -> b -> c must exist in the dict structure
        assert "a" in tree
        assert "b" in tree["a"]
        assert "c" in tree["a"]["b"]


# ---------------------------------------------------------------------------
# 22. HierarchicalCounter — separator + validation
# ---------------------------------------------------------------------------

class TestHierarchicalValidation:
    def test_invalid_empty_separator(self, store):
        with pytest.raises(CounterError):
            HierarchicalCounter(store, separator="")

    def test_path_with_separator_in_component_raises(self, store):
        hc = HierarchicalCounter(store, separator=".")
        with pytest.raises(CounterError):
            hc.increment(["bad.name"], 1)

    def test_path_empty_component_raises(self, store):
        hc = HierarchicalCounter(store)
        with pytest.raises(CounterError):
            hc.increment([""], 1)

    def test_path_non_list_raises(self, store):
        hc = HierarchicalCounter(store)
        with pytest.raises(CounterError):
            hc.increment("not a list", 1)

    def test_default_separator_is_dot(self, store):
        hc = HierarchicalCounter(store)
        hc.increment(["a", "b"], 1)
        assert store.get("a.b") == 1


# ---------------------------------------------------------------------------
# 23. HierarchicalCounter — integration / scenarios
# ---------------------------------------------------------------------------

class TestHierarchicalIntegration:
    def test_full_user_metrics_scenario(self, store):
        hc = HierarchicalCounter(store)
        # Simulate metrics collection
        hc.increment(["events", "signup"], 10)
        hc.increment(["events", "login", "success"], 50)
        hc.increment(["events", "login", "failure"], 5)
        hc.increment(["events", "logout"], 30)

        assert hc.rollup(["events"]) == 95
        assert hc.rollup(["events", "login"]) == 55
        assert hc.get(["events", "signup"]) == 10
        children = hc.children(["events"])
        assert set(children) == {
            "events.signup", "events.login", "events.logout"
        }

    def test_hierarchical_with_disk_store(self, tmp_db_path):
        s = CounterStore(tmp_db_path)
        hc = HierarchicalCounter(s)
        hc.increment(["a", "b"], 5)
        hc.increment(["a", "c"], 3)
        s.close()
        s2 = CounterStore(tmp_db_path)
        hc2 = HierarchicalCounter(s2)
        assert hc2.rollup(["a"]) == 8
        s2.close()

    def test_hierarchical_concurrent_increments(self, store):
        hc = HierarchicalCounter(store)
        n = 100
        with ThreadPoolExecutor(max_workers=8) as ex:
            futures = [
                ex.submit(hc.increment, ["metrics", "counter"], 1)
                for _ in range(n)
            ]
            for f in as_completed(futures):
                f.result()
        assert hc.get(["metrics", "counter"]) == n
