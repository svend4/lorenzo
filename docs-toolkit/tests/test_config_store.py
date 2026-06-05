"""Tests for docstoolkit.config_store — ~85 test cases.

Covers:
  - set/get basic operations
  - get with default
  - get_entry returning ConfigEntry
  - delete (True/False return values)
  - list all entries in a namespace
  - list with prefix filter
  - namespaces()
  - subscribe callback on set
  - subscribe callback on delete (old_value, None)
  - subscribe NOT called when value is unchanged
  - export_namespace
  - import_namespace with overwrite=True / False
  - import_namespace return count
  - count() total and by namespace
  - clear_namespace
  - Persistence (file-based DB)
  - Virtual time via now_fn
  - JSON types (int, float, list, dict, bool, None)
  - Thread safety (concurrent sets)
"""
import os
import tempfile
import threading
import time
from pathlib import Path

import pytest

from docstoolkit.config_store import ConfigEntry, ConfigStore


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def store():
    """In-memory ConfigStore; auto-closed after each test."""
    s = ConfigStore()
    yield s
    s.close()


@pytest.fixture
def tstore():
    """In-memory ConfigStore with a virtual clock starting at 1000.0."""
    _t = [1000.0]

    def now():
        return _t[0]

    def tick(delta=1.0):
        _t[0] += delta

    s = ConfigStore(now_fn=now)
    yield s, now, tick
    s.close()


# ---------------------------------------------------------------------------
# set / get — basics
# ---------------------------------------------------------------------------

class TestSetGet:
    def test_set_returns_config_entry(self, store):
        entry = store.set("ns", "a.b", 42)
        assert isinstance(entry, ConfigEntry)

    def test_set_get_roundtrip(self, store):
        store.set("ns", "key", "hello")
        assert store.get("ns", "key") == "hello"

    def test_overwrite_value(self, store):
        store.set("ns", "x", 1)
        store.set("ns", "x", 2)
        assert store.get("ns", "x") == 2

    def test_set_stores_description(self, store):
        store.set("ns", "k", 7, description="port number")
        entry = store.get_entry("ns", "k")
        assert entry.description == "port number"

    def test_overwrite_updates_description(self, store):
        store.set("ns", "k", 1, description="old")
        store.set("ns", "k", 2, description="new")
        entry = store.get_entry("ns", "k")
        assert entry.description == "new"

    def test_different_namespaces_isolated(self, store):
        store.set("ns1", "key", "alpha")
        store.set("ns2", "key", "beta")
        assert store.get("ns1", "key") == "alpha"
        assert store.get("ns2", "key") == "beta"

    def test_dot_notation_key(self, store):
        store.set("app", "server.port", 8080)
        assert store.get("app", "server.port") == 8080

    def test_deeply_nested_key(self, store):
        store.set("app", "a.b.c.d", "deep")
        assert store.get("app", "a.b.c.d") == "deep"


# ---------------------------------------------------------------------------
# get with default
# ---------------------------------------------------------------------------

class TestGetDefault:
    def test_missing_key_returns_none(self, store):
        assert store.get("ns", "missing") is None

    def test_missing_key_returns_custom_default(self, store):
        assert store.get("ns", "missing", default=99) == 99

    def test_missing_namespace_returns_default(self, store):
        assert store.get("no-such-ns", "key", default="fallback") == "fallback"

    def test_default_zero(self, store):
        assert store.get("ns", "k", default=0) == 0

    def test_default_empty_list(self, store):
        assert store.get("ns", "k", default=[]) == []

    def test_existing_key_ignores_default(self, store):
        store.set("ns", "k", 5)
        assert store.get("ns", "k", default=99) == 5


# ---------------------------------------------------------------------------
# get_entry
# ---------------------------------------------------------------------------

class TestGetEntry:
    def test_returns_config_entry(self, store):
        store.set("ns", "k", "v")
        entry = store.get_entry("ns", "k")
        assert isinstance(entry, ConfigEntry)

    def test_entry_fields(self, store):
        store.set("ns", "k", 123, description="desc")
        entry = store.get_entry("ns", "k")
        assert entry.namespace == "ns"
        assert entry.key == "k"
        assert entry.value == 123
        assert entry.description == "desc"

    def test_missing_returns_none(self, store):
        assert store.get_entry("ns", "nonexistent") is None

    def test_entry_has_timestamps(self, tstore):
        s, now, tick = tstore
        s.set("ns", "k", 1)
        entry = s.get_entry("ns", "k")
        assert entry.created_at == 1000.0
        assert entry.updated_at == 1000.0

    def test_entry_updated_at_changes_on_overwrite(self, tstore):
        s, now, tick = tstore
        s.set("ns", "k", 1)
        tick(5.0)
        s.set("ns", "k", 2)
        entry = s.get_entry("ns", "k")
        assert entry.created_at == 1000.0
        assert entry.updated_at == 1005.0

    def test_entry_created_at_preserved_on_overwrite(self, tstore):
        s, now, tick = tstore
        s.set("ns", "k", "original")
        tick(10.0)
        s.set("ns", "k", "updated")
        entry = s.get_entry("ns", "k")
        assert entry.created_at == 1000.0  # unchanged


# ---------------------------------------------------------------------------
# delete
# ---------------------------------------------------------------------------

class TestDelete:
    def test_delete_existing_returns_true(self, store):
        store.set("ns", "k", 1)
        assert store.delete("ns", "k") is True

    def test_delete_removes_entry(self, store):
        store.set("ns", "k", 1)
        store.delete("ns", "k")
        assert store.get("ns", "k") is None

    def test_delete_missing_returns_false(self, store):
        assert store.delete("ns", "nonexistent") is False

    def test_delete_only_target_key(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        store.delete("ns", "a")
        assert store.get("ns", "a") is None
        assert store.get("ns", "b") == 2

    def test_double_delete_second_returns_false(self, store):
        store.set("ns", "k", 1)
        store.delete("ns", "k")
        assert store.delete("ns", "k") is False


# ---------------------------------------------------------------------------
# list
# ---------------------------------------------------------------------------

class TestList:
    def test_list_all_in_namespace(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        store.set("ns", "c", 3)
        entries = store.list("ns")
        keys = [e.key for e in entries]
        assert sorted(keys) == ["a", "b", "c"]

    def test_list_empty_namespace(self, store):
        assert store.list("empty") == []

    def test_list_does_not_cross_namespaces(self, store):
        store.set("ns1", "x", 1)
        store.set("ns2", "y", 2)
        entries = store.list("ns1")
        assert len(entries) == 1
        assert entries[0].key == "x"

    def test_list_returns_config_entries(self, store):
        store.set("ns", "k", 42)
        entries = store.list("ns")
        assert all(isinstance(e, ConfigEntry) for e in entries)

    def test_list_sorted_by_key(self, store):
        store.set("ns", "z.first", 1)
        store.set("ns", "a.first", 2)
        store.set("ns", "m.mid", 3)
        entries = store.list("ns")
        keys = [e.key for e in entries]
        assert keys == sorted(keys)


class TestListPrefix:
    def test_prefix_filter(self, store):
        store.set("ns", "server.port", 8080)
        store.set("ns", "server.host", "localhost")
        store.set("ns", "db.host", "db-host")
        entries = store.list("ns", prefix="server.")
        keys = {e.key for e in entries}
        assert keys == {"server.port", "server.host"}

    def test_prefix_no_match(self, store):
        store.set("ns", "a.b", 1)
        entries = store.list("ns", prefix="z.")
        assert entries == []

    def test_prefix_exact_key(self, store):
        store.set("ns", "exact", 7)
        store.set("ns", "exact.sub", 8)
        entries = store.list("ns", prefix="exact")
        keys = {e.key for e in entries}
        # "exact" and "exact.sub" both start with "exact"
        assert "exact" in keys
        assert "exact.sub" in keys

    def test_prefix_with_special_chars_percent(self, store):
        store.set("ns", "100%full", "yes")
        store.set("ns", "other", "no")
        entries = store.list("ns", prefix="100%")
        keys = [e.key for e in entries]
        assert keys == ["100%full"]

    def test_prefix_with_special_chars_underscore(self, store):
        store.set("ns", "a_b", 1)
        store.set("ns", "axb", 2)
        store.set("ns", "other", 3)
        # prefix "a_b" should only match "a_b", not "axb"
        entries = store.list("ns", prefix="a_b")
        keys = [e.key for e in entries]
        assert keys == ["a_b"]


# ---------------------------------------------------------------------------
# namespaces
# ---------------------------------------------------------------------------

class TestNamespaces:
    def test_empty_store(self, store):
        assert store.namespaces() == []

    def test_single_namespace(self, store):
        store.set("ns1", "k", 1)
        assert store.namespaces() == ["ns1"]

    def test_multiple_namespaces_sorted(self, store):
        store.set("beta", "k", 1)
        store.set("alpha", "k", 2)
        store.set("gamma", "k", 3)
        assert store.namespaces() == ["alpha", "beta", "gamma"]

    def test_duplicate_namespace_appears_once(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        assert store.namespaces() == ["ns"]

    def test_namespace_removed_after_clear(self, store):
        store.set("ns", "k", 1)
        store.clear_namespace("ns")
        assert "ns" not in store.namespaces()


# ---------------------------------------------------------------------------
# subscribe
# ---------------------------------------------------------------------------

class TestSubscribe:
    def test_callback_called_on_new_set(self, store):
        calls = []
        store.subscribe("ns", "k", lambda old, new: calls.append((old, new)))
        store.set("ns", "k", 42)
        assert calls == [(None, 42)]

    def test_callback_called_on_overwrite(self, store):
        store.set("ns", "k", 1)
        calls = []
        store.subscribe("ns", "k", lambda old, new: calls.append((old, new)))
        store.set("ns", "k", 2)
        assert calls == [(1, 2)]

    def test_callback_not_called_if_value_unchanged(self, store):
        store.set("ns", "k", 42)
        calls = []
        store.subscribe("ns", "k", lambda old, new: calls.append((old, new)))
        store.set("ns", "k", 42)  # same value
        assert calls == []

    def test_callback_on_delete(self, store):
        store.set("ns", "k", 99)
        calls = []
        store.subscribe("ns", "k", lambda old, new: calls.append((old, new)))
        store.delete("ns", "k")
        assert calls == [(99, None)]

    def test_multiple_callbacks_for_same_key(self, store):
        results_a = []
        results_b = []
        store.subscribe("ns", "k", lambda o, n: results_a.append(n))
        store.subscribe("ns", "k", lambda o, n: results_b.append(n))
        store.set("ns", "k", 7)
        assert results_a == [7]
        assert results_b == [7]

    def test_callback_not_called_for_different_key(self, store):
        calls = []
        store.subscribe("ns", "watched", lambda o, n: calls.append(n))
        store.set("ns", "other", 5)
        assert calls == []

    def test_callback_not_called_for_different_namespace(self, store):
        calls = []
        store.subscribe("ns1", "k", lambda o, n: calls.append(n))
        store.set("ns2", "k", 5)
        assert calls == []

    def test_callback_called_in_order(self, store):
        order = []
        store.subscribe("ns", "k", lambda o, n: order.append("first"))
        store.subscribe("ns", "k", lambda o, n: order.append("second"))
        store.set("ns", "k", 1)
        assert order == ["first", "second"]

    def test_callback_exception_does_not_propagate(self, store):
        def bad_cb(old, new):
            raise RuntimeError("boom")

        store.subscribe("ns", "k", bad_cb)
        # Should not raise
        store.set("ns", "k", 1)
        assert store.get("ns", "k") == 1

    def test_no_callback_for_unsubscribed_key(self, store):
        store.subscribe("ns", "other", lambda o, n: None)
        calls = []
        store.subscribe("ns", "watched", lambda o, n: calls.append(n))
        store.set("ns", "watched", "hi")
        assert calls == ["hi"]


# ---------------------------------------------------------------------------
# export_namespace
# ---------------------------------------------------------------------------

class TestExportNamespace:
    def test_export_all_keys(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", "two")
        store.set("ns", "c", [3])
        exported = store.export_namespace("ns")
        assert exported == {"a": 1, "b": "two", "c": [3]}

    def test_export_empty_namespace(self, store):
        assert store.export_namespace("empty") == {}

    def test_export_does_not_include_other_namespaces(self, store):
        store.set("ns1", "x", 1)
        store.set("ns2", "y", 2)
        exported = store.export_namespace("ns1")
        assert "y" not in exported

    def test_export_returns_plain_dict(self, store):
        store.set("ns", "k", 42)
        exported = store.export_namespace("ns")
        assert type(exported) is dict


# ---------------------------------------------------------------------------
# import_namespace
# ---------------------------------------------------------------------------

class TestImportNamespace:
    def test_import_inserts_new_keys(self, store):
        n = store.import_namespace("ns", {"a": 1, "b": 2})
        assert n == 2
        assert store.get("ns", "a") == 1
        assert store.get("ns", "b") == 2

    def test_import_overwrite_true_updates_existing(self, store):
        store.set("ns", "a", "old")
        store.import_namespace("ns", {"a": "new"}, overwrite=True)
        assert store.get("ns", "a") == "new"

    def test_import_overwrite_false_skips_existing(self, store):
        store.set("ns", "a", "original")
        store.import_namespace("ns", {"a": "replaced"}, overwrite=False)
        assert store.get("ns", "a") == "original"

    def test_import_overwrite_false_inserts_new(self, store):
        store.set("ns", "existing", 1)
        store.import_namespace("ns", {"existing": 99, "new_key": 2}, overwrite=False)
        assert store.get("ns", "existing") == 1
        assert store.get("ns", "new_key") == 2

    def test_import_returns_count_all_new(self, store):
        count = store.import_namespace("ns", {"a": 1, "b": 2, "c": 3})
        assert count == 3

    def test_import_returns_count_with_skip(self, store):
        store.set("ns", "a", 0)
        count = store.import_namespace("ns", {"a": 99, "b": 1}, overwrite=False)
        assert count == 1  # only "b" was imported

    def test_import_returns_count_with_overwrite(self, store):
        store.set("ns", "a", 0)
        count = store.import_namespace("ns", {"a": 99, "b": 1}, overwrite=True)
        assert count == 2

    def test_import_empty_dict(self, store):
        count = store.import_namespace("ns", {})
        assert count == 0


# ---------------------------------------------------------------------------
# count
# ---------------------------------------------------------------------------

class TestCount:
    def test_count_empty_store(self, store):
        assert store.count() == 0

    def test_count_all_entries(self, store):
        store.set("ns1", "a", 1)
        store.set("ns1", "b", 2)
        store.set("ns2", "c", 3)
        assert store.count() == 3

    def test_count_by_namespace(self, store):
        store.set("ns1", "a", 1)
        store.set("ns1", "b", 2)
        store.set("ns2", "c", 3)
        assert store.count("ns1") == 2
        assert store.count("ns2") == 1

    def test_count_missing_namespace(self, store):
        assert store.count("nonexistent") == 0

    def test_count_decreases_after_delete(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        store.delete("ns", "a")
        assert store.count("ns") == 1

    def test_count_total_decreases_after_clear(self, store):
        store.set("ns1", "a", 1)
        store.set("ns2", "b", 2)
        store.clear_namespace("ns1")
        assert store.count() == 1


# ---------------------------------------------------------------------------
# clear_namespace
# ---------------------------------------------------------------------------

class TestClearNamespace:
    def test_clear_removes_all_entries(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        store.clear_namespace("ns")
        assert store.list("ns") == []

    def test_clear_returns_count(self, store):
        store.set("ns", "a", 1)
        store.set("ns", "b", 2)
        assert store.clear_namespace("ns") == 2

    def test_clear_empty_namespace_returns_zero(self, store):
        assert store.clear_namespace("empty") == 0

    def test_clear_does_not_affect_other_namespaces(self, store):
        store.set("ns1", "a", 1)
        store.set("ns2", "b", 2)
        store.clear_namespace("ns1")
        assert store.get("ns2", "b") == 2


# ---------------------------------------------------------------------------
# Persistence (file-based DB)
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_data_survives_reopen(self, tmp_path):
        db = str(tmp_path / "cfg.db")
        s1 = ConfigStore(db_path=db)
        s1.set("app", "key", "persisted_value")
        s1.close()

        s2 = ConfigStore(db_path=db)
        assert s2.get("app", "key") == "persisted_value"
        s2.close()

    def test_delete_persists(self, tmp_path):
        db = str(tmp_path / "cfg.db")
        s1 = ConfigStore(db_path=db)
        s1.set("app", "key", "value")
        s1.delete("app", "key")
        s1.close()

        s2 = ConfigStore(db_path=db)
        assert s2.get("app", "key") is None
        s2.close()

    def test_multiple_namespaces_persist(self, tmp_path):
        db = str(tmp_path / "cfg.db")
        s1 = ConfigStore(db_path=db)
        s1.set("ns1", "a", 1)
        s1.set("ns2", "b", 2)
        s1.close()

        s2 = ConfigStore(db_path=db)
        assert s2.namespaces() == ["ns1", "ns2"]
        s2.close()


# ---------------------------------------------------------------------------
# Virtual time via now_fn
# ---------------------------------------------------------------------------

class TestVirtualTime:
    def test_created_at_uses_now_fn(self, tstore):
        s, now, tick = tstore
        entry = s.set("ns", "k", 1)
        assert entry.created_at == 1000.0

    def test_updated_at_advances(self, tstore):
        s, now, tick = tstore
        s.set("ns", "k", 1)
        tick(5.0)
        entry = s.set("ns", "k", 2)
        assert entry.updated_at == 1005.0

    def test_created_at_stable_across_updates(self, tstore):
        s, now, tick = tstore
        s.set("ns", "k", "first")
        tick(100.0)
        s.set("ns", "k", "second")
        entry = s.get_entry("ns", "k")
        assert entry.created_at == 1000.0

    def test_two_entries_get_different_timestamps(self, tstore):
        s, now, tick = tstore
        e1 = s.set("ns", "k1", 1)
        tick(3.0)
        e2 = s.set("ns", "k2", 2)
        assert e1.created_at == 1000.0
        assert e2.created_at == 1003.0


# ---------------------------------------------------------------------------
# JSON types
# ---------------------------------------------------------------------------

class TestJsonTypes:
    @pytest.mark.parametrize("value", [
        42,
        3.14,
        "hello",
        True,
        False,
        None,
        [1, 2, 3],
        {"nested": {"deep": True}},
        [],
        {},
        [None, True, 1, "mix"],
    ])
    def test_roundtrip(self, store, value):
        store.set("ns", "k", value)
        assert store.get("ns", "k") == value

    def test_int_stays_int(self, store):
        store.set("ns", "k", 7)
        assert type(store.get("ns", "k")) is int

    def test_float_stays_float(self, store):
        store.set("ns", "k", 1.5)
        assert type(store.get("ns", "k")) is float

    def test_bool_stays_bool(self, store):
        store.set("ns", "k", True)
        val = store.get("ns", "k")
        assert val is True
        assert type(val) is bool

    def test_none_value(self, store):
        store.set("ns", "k", None)
        assert store.get("ns", "k") is None

    def test_list_value(self, store):
        store.set("ns", "k", [1, 2, 3])
        assert store.get("ns", "k") == [1, 2, 3]

    def test_dict_value(self, store):
        data = {"a": 1, "b": [2, 3]}
        store.set("ns", "k", data)
        assert store.get("ns", "k") == data


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_sets_no_data_corruption(self):
        """All threads write distinct keys; final state must match expectations."""
        s = ConfigStore()
        errors = []
        n_threads = 20
        n_keys_per_thread = 50

        def worker(thread_id):
            try:
                for i in range(n_keys_per_thread):
                    key = f"t{thread_id}.key{i}"
                    s.set("shared", key, thread_id * 1000 + i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Thread errors: {errors}"
        total = s.count("shared")
        assert total == n_threads * n_keys_per_thread
        s.close()

    def test_concurrent_sets_same_key(self):
        """Multiple threads writing the same key; store must remain consistent."""
        s = ConfigStore()
        errors = []
        n_threads = 10

        def writer(val):
            try:
                for _ in range(100):
                    s.set("ns", "shared_key", val)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=writer, args=(i,)) for i in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        val = s.get("ns", "shared_key")
        assert val in list(range(n_threads))  # some thread's value won
        s.close()

    def test_concurrent_reads_and_writes(self):
        """Interleaved readers and writers must not raise exceptions."""
        s = ConfigStore()
        errors = []
        s.set("ns", "counter", 0)

        def writer():
            try:
                for i in range(200):
                    s.set("ns", "counter", i)
            except Exception as e:
                errors.append(e)

        def reader():
            try:
                for _ in range(200):
                    s.get("ns", "counter")
            except Exception as e:
                errors.append(e)

        threads = (
            [threading.Thread(target=writer) for _ in range(5)]
            + [threading.Thread(target=reader) for _ in range(5)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == []
        s.close()
