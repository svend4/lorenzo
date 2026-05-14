"""Tests for docstoolkit.doc_persistence (E272)."""

from __future__ import annotations

import os
import tempfile
import threading

import pytest

from docstoolkit.doc_persistence import (
    DocPersistence,
    PersistedDoc,
    PersistenceStats,
)


# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def store() -> DocPersistence:
    s = DocPersistence(":memory:")
    yield s
    if s.is_open:
        s.close()


@pytest.fixture
def file_store(tmp_path):
    db = tmp_path / "p.db"
    s = DocPersistence(str(db))
    yield s, str(db)
    if s.is_open:
        s.close()


# ── PersistedDoc ─────────────────────────────────────────────────────────────

class TestPersistedDoc:
    def test_default_values(self):
        d = PersistedDoc()
        assert d.doc_id == ""
        assert d.content == ""
        assert d.metadata == {}
        assert d.created_at == 0.0
        assert d.updated_at == 0.0
        assert d.version == 1

    def test_construct_with_values(self):
        d = PersistedDoc(
            doc_id="x",
            content="hi",
            metadata={"a": 1},
            created_at=1.0,
            updated_at=2.0,
            version=3,
        )
        assert d.doc_id == "x"
        assert d.content == "hi"
        assert d.metadata == {"a": 1}
        assert d.created_at == 1.0
        assert d.updated_at == 2.0
        assert d.version == 3

    def test_metadata_default_is_independent(self):
        a = PersistedDoc()
        b = PersistedDoc()
        a.metadata["x"] = 1
        assert "x" not in b.metadata


# ── PersistenceStats ─────────────────────────────────────────────────────────

class TestPersistenceStats:
    def test_defaults(self):
        s = PersistenceStats()
        assert s.total_docs == 0
        assert s.total_size == 0
        assert s.versions == 0
        assert s.avg_doc_size == 0.0

    def test_constructed(self):
        s = PersistenceStats(
            total_docs=3, total_size=300, versions=6, avg_doc_size=50.0
        )
        assert s.total_docs == 3
        assert s.total_size == 300
        assert s.versions == 6
        assert s.avg_doc_size == 50.0


# ── Save ─────────────────────────────────────────────────────────────────────

class TestSave:
    def test_save_new_doc_returns_version_1(self, store):
        d = store.save("a", "hello")
        assert d.doc_id == "a"
        assert d.content == "hello"
        assert d.version == 1
        assert d.metadata == {}

    def test_save_increments_version(self, store):
        store.save("a", "v1")
        d2 = store.save("a", "v2")
        d3 = store.save("a", "v3")
        assert d2.version == 2
        assert d3.version == 3

    def test_save_metadata_stored(self, store):
        d = store.save("a", "x", metadata={"k": "v", "n": 1})
        assert d.metadata == {"k": "v", "n": 1}

    def test_save_default_metadata_empty(self, store):
        d = store.save("a", "x")
        assert d.metadata == {}

    def test_save_uses_provided_now(self, store):
        d = store.save("a", "x", now=1234.5)
        assert d.created_at == 1234.5
        assert d.updated_at == 1234.5

    def test_save_preserves_created_at_across_versions(self, store):
        store.save("a", "x", now=100.0)
        d2 = store.save("a", "y", now=200.0)
        assert d2.created_at == 100.0
        assert d2.updated_at == 200.0

    def test_save_default_now_is_time_time(self, store):
        import time
        before = time.time()
        d = store.save("a", "x")
        after = time.time()
        assert before <= d.updated_at <= after

    def test_save_returns_persisted_doc(self, store):
        d = store.save("a", "x")
        assert isinstance(d, PersistedDoc)

    def test_save_rejects_non_string_doc_id(self, store):
        with pytest.raises(TypeError):
            store.save(123, "x")  # type: ignore[arg-type]

    def test_save_rejects_non_string_content(self, store):
        with pytest.raises(TypeError):
            store.save("a", 123)  # type: ignore[arg-type]

    def test_save_rejects_non_dict_metadata(self, store):
        with pytest.raises(TypeError):
            store.save("a", "x", metadata=[("k", "v")])  # type: ignore[arg-type]

    def test_save_empty_string_content_allowed(self, store):
        d = store.save("a", "")
        assert d.content == ""

    def test_save_unicode_content(self, store):
        d = store.save("a", "пиво café 🍺")
        loaded = store.load("a")
        assert loaded.content == "пиво café 🍺"

    def test_save_complex_metadata(self, store):
        meta = {"list": [1, 2, 3], "nested": {"a": 1}, "bool": True, "none": None}
        d = store.save("a", "x", metadata=meta)
        loaded = store.load("a")
        assert loaded.metadata == meta

    def test_save_multiple_docs_independent_versions(self, store):
        store.save("a", "1")
        store.save("b", "1")
        store.save("a", "2")
        assert store.latest_version("a") == 2
        assert store.latest_version("b") == 1


# ── Load ─────────────────────────────────────────────────────────────────────

class TestLoad:
    def test_load_missing_returns_none(self, store):
        assert store.load("missing") is None

    def test_load_returns_latest_version(self, store):
        store.save("a", "v1")
        store.save("a", "v2")
        d = store.load("a")
        assert d.version == 2
        assert d.content == "v2"

    def test_load_returns_persisted_doc(self, store):
        store.save("a", "x")
        d = store.load("a")
        assert isinstance(d, PersistedDoc)

    def test_load_metadata_roundtrip(self, store):
        store.save("a", "x", metadata={"k": "v"})
        d = store.load("a")
        assert d.metadata == {"k": "v"}


# ── Load Version ─────────────────────────────────────────────────────────────

class TestLoadVersion:
    def test_load_specific_version(self, store):
        store.save("a", "v1")
        store.save("a", "v2")
        store.save("a", "v3")
        d = store.load_version("a", 2)
        assert d.version == 2
        assert d.content == "v2"

    def test_load_missing_doc(self, store):
        assert store.load_version("none", 1) is None

    def test_load_missing_version(self, store):
        store.save("a", "v1")
        assert store.load_version("a", 99) is None

    def test_load_version_1(self, store):
        store.save("a", "first")
        store.save("a", "second")
        d = store.load_version("a", 1)
        assert d.content == "first"


# ── Delete ───────────────────────────────────────────────────────────────────

class TestDelete:
    def test_delete_existing(self, store):
        store.save("a", "x")
        assert store.delete("a") is True
        assert store.load("a") is None

    def test_delete_removes_all_versions(self, store):
        store.save("a", "v1")
        store.save("a", "v2")
        store.save("a", "v3")
        assert store.delete("a") is True
        assert store.version_count("a") == 0

    def test_delete_missing_returns_false(self, store):
        assert store.delete("nope") is False

    def test_delete_only_targets_one_doc(self, store):
        store.save("a", "x")
        store.save("b", "y")
        store.delete("a")
        assert store.exists("b") is True


# ── Exists ───────────────────────────────────────────────────────────────────

class TestExists:
    def test_exists_true(self, store):
        store.save("a", "x")
        assert store.exists("a") is True

    def test_exists_false(self, store):
        assert store.exists("a") is False

    def test_exists_after_delete(self, store):
        store.save("a", "x")
        store.delete("a")
        assert store.exists("a") is False

    def test_exists_with_multiple_versions(self, store):
        store.save("a", "v1")
        store.save("a", "v2")
        assert store.exists("a") is True


# ── List All ─────────────────────────────────────────────────────────────────

class TestListAll:
    def test_list_all_empty(self, store):
        assert store.list_all() == []

    def test_list_all_returns_latest_versions(self, store):
        store.save("a", "v1", now=1.0)
        store.save("a", "v2", now=2.0)
        store.save("b", "b1", now=3.0)
        docs = store.list_all()
        assert len(docs) == 2
        ids = {d.doc_id: d for d in docs}
        assert ids["a"].version == 2
        assert ids["a"].content == "v2"
        assert ids["b"].version == 1

    def test_list_all_with_limit(self, store):
        for i in range(5):
            store.save(f"d{i}", str(i), now=float(i))
        docs = store.list_all(limit=2)
        assert len(docs) == 2

    def test_list_all_orders_by_updated_at_desc(self, store):
        store.save("a", "1", now=10.0)
        store.save("b", "2", now=20.0)
        store.save("c", "3", now=15.0)
        docs = store.list_all()
        assert [d.doc_id for d in docs] == ["b", "c", "a"]


# ── List Doc IDs ─────────────────────────────────────────────────────────────

class TestListDocIds:
    def test_empty(self, store):
        assert store.list_doc_ids() == []

    def test_sorted(self, store):
        store.save("zebra", "x")
        store.save("apple", "y")
        store.save("mango", "z")
        assert store.list_doc_ids() == ["apple", "mango", "zebra"]

    def test_distinct(self, store):
        store.save("a", "1")
        store.save("a", "2")
        store.save("a", "3")
        assert store.list_doc_ids() == ["a"]


# ── Versions Of ──────────────────────────────────────────────────────────────

class TestVersionsOf:
    def test_no_versions(self, store):
        assert store.versions_of("missing") == []

    def test_single_version(self, store):
        store.save("a", "x")
        assert store.versions_of("a") == [1]

    def test_multiple_versions_ascending(self, store):
        store.save("a", "1")
        store.save("a", "2")
        store.save("a", "3")
        assert store.versions_of("a") == [1, 2, 3]


# ── Version Count ────────────────────────────────────────────────────────────

class TestVersionCount:
    def test_zero(self, store):
        assert store.version_count("none") == 0

    def test_after_saves(self, store):
        store.save("a", "1")
        store.save("a", "2")
        store.save("a", "3")
        assert store.version_count("a") == 3

    def test_after_delete(self, store):
        store.save("a", "x")
        store.delete("a")
        assert store.version_count("a") == 0


# ── Latest Version ───────────────────────────────────────────────────────────

class TestLatestVersion:
    def test_missing(self, store):
        assert store.latest_version("missing") is None

    def test_returns_max(self, store):
        store.save("a", "1")
        store.save("a", "2")
        store.save("a", "3")
        assert store.latest_version("a") == 3

    def test_after_delete(self, store):
        store.save("a", "x")
        store.delete("a")
        assert store.latest_version("a") is None


# ── Purge Old Versions ───────────────────────────────────────────────────────

class TestPurgeOldVersions:
    def test_purge_keeps_n_most_recent(self, store):
        for i in range(10):
            store.save("a", f"v{i}", now=float(i))
        removed = store.purge_old_versions("a", keep_last_n=3)
        assert removed == 7
        versions = store.versions_of("a")
        assert versions == [8, 9, 10]

    def test_purge_when_fewer_versions_than_n(self, store):
        store.save("a", "1")
        store.save("a", "2")
        removed = store.purge_old_versions("a", keep_last_n=5)
        assert removed == 0
        assert store.version_count("a") == 2

    def test_purge_no_versions(self, store):
        removed = store.purge_old_versions("missing", keep_last_n=5)
        assert removed == 0

    def test_purge_keep_zero(self, store):
        store.save("a", "1")
        store.save("a", "2")
        removed = store.purge_old_versions("a", keep_last_n=0)
        assert removed == 2
        assert store.version_count("a") == 0

    def test_purge_negative_keep_raises(self, store):
        with pytest.raises(ValueError):
            store.purge_old_versions("a", keep_last_n=-1)

    def test_purge_default_keep_10(self, store):
        for i in range(15):
            store.save("a", str(i))
        removed = store.purge_old_versions("a")
        assert removed == 5
        assert store.version_count("a") == 10


# ── Purge All Old Versions ───────────────────────────────────────────────────

class TestPurgeAllOldVersions:
    def test_purge_all_empty(self, store):
        assert store.purge_all_old_versions() == 0

    def test_purge_all_multiple_docs(self, store):
        for i in range(5):
            store.save("a", f"a{i}")
        for i in range(7):
            store.save("b", f"b{i}")
        removed = store.purge_all_old_versions(keep_last_n=2)
        assert removed == (5 - 2) + (7 - 2)  # 3 + 5 = 8
        assert store.version_count("a") == 2
        assert store.version_count("b") == 2

    def test_purge_all_negative_raises(self, store):
        with pytest.raises(ValueError):
            store.purge_all_old_versions(keep_last_n=-2)

    def test_purge_all_keep_zero_deletes_all(self, store):
        store.save("a", "1")
        store.save("b", "1")
        removed = store.purge_all_old_versions(keep_last_n=0)
        assert removed == 2
        assert store.total_versions == 0


# ── Total Docs ───────────────────────────────────────────────────────────────

class TestTotalDocs:
    def test_zero(self, store):
        assert store.total_docs == 0

    def test_after_saves(self, store):
        store.save("a", "x")
        store.save("b", "y")
        store.save("a", "z")  # second version of a
        assert store.total_docs == 2


# ── Total Versions ───────────────────────────────────────────────────────────

class TestTotalVersions:
    def test_zero(self, store):
        assert store.total_versions == 0

    def test_after_saves(self, store):
        store.save("a", "1")
        store.save("a", "2")
        store.save("b", "1")
        assert store.total_versions == 3


# ── Stats ────────────────────────────────────────────────────────────────────

class TestStats:
    def test_empty_stats(self, store):
        s = store.stats()
        assert s.total_docs == 0
        assert s.versions == 0
        assert s.total_size == 0
        assert s.avg_doc_size == 0.0

    def test_stats_after_saves(self, store):
        store.save("a", "hello")  # 5 bytes
        store.save("b", "world!")  # 6 bytes
        s = store.stats()
        assert s.total_docs == 2
        assert s.versions == 2
        assert s.total_size == 11
        assert s.avg_doc_size == 5.5

    def test_stats_returns_dataclass(self, store):
        s = store.stats()
        assert isinstance(s, PersistenceStats)

    def test_stats_counts_all_versions(self, store):
        store.save("a", "ab")
        store.save("a", "abc")
        s = store.stats()
        assert s.versions == 2
        assert s.total_size == 5
        assert s.total_docs == 1


# ── Vacuum ───────────────────────────────────────────────────────────────────

class TestVacuum:
    def test_vacuum_clean_returns_zero(self, store):
        store.save("a", "x")
        assert store.vacuum() == 0

    def test_vacuum_empty(self, store):
        assert store.vacuum() == 0

    def test_vacuum_removes_corrupt_metadata(self, store):
        store.save("a", "x", metadata={"k": "v"})
        store.save("b", "y", metadata={"k": "v"})
        # Inject corrupt JSON directly
        with store._lock:
            store._conn.execute(
                "UPDATE docs SET metadata_json='{not json' WHERE doc_id='a'"
            )
            store._conn.commit()
        removed = store.vacuum()
        assert removed == 1
        assert store.exists("a") is False
        assert store.exists("b") is True


# ── Close ────────────────────────────────────────────────────────────────────

class TestClose:
    def test_close_marks_not_open(self, store):
        store.close()
        assert store.is_open is False

    def test_close_is_idempotent(self, store):
        store.close()
        store.close()
        assert store.is_open is False

    def test_operations_after_close_raise(self, store):
        store.close()
        with pytest.raises(RuntimeError):
            store.save("a", "x")
        with pytest.raises(RuntimeError):
            store.load("a")


# ── Is Open ──────────────────────────────────────────────────────────────────

class TestIsOpen:
    def test_default_open(self, store):
        assert store.is_open is True

    def test_after_close(self, store):
        store.close()
        assert store.is_open is False


# ── Persistence (file db) ────────────────────────────────────────────────────

class TestPersistence:
    def test_data_survives_reopen(self, tmp_path):
        db = str(tmp_path / "p.db")
        s1 = DocPersistence(db)
        s1.save("a", "hello", metadata={"k": "v"}, now=10.0)
        s1.save("a", "world", metadata={"k": "v2"}, now=20.0)
        s1.close()

        s2 = DocPersistence(db)
        try:
            d = s2.load("a")
            assert d is not None
            assert d.content == "world"
            assert d.metadata == {"k": "v2"}
            assert d.version == 2
            assert d.created_at == 10.0
            assert s2.total_docs == 1
            assert s2.total_versions == 2
        finally:
            s2.close()

    def test_versions_survive_reopen(self, tmp_path):
        db = str(tmp_path / "p2.db")
        s1 = DocPersistence(db)
        for i in range(5):
            s1.save("doc", f"v{i}", now=float(i))
        s1.close()

        s2 = DocPersistence(db)
        try:
            assert s2.versions_of("doc") == [1, 2, 3, 4, 5]
            v3 = s2.load_version("doc", 3)
            assert v3.content == "v2"
        finally:
            s2.close()

    def test_file_db_path_created(self, tmp_path):
        db = str(tmp_path / "n.db")
        s = DocPersistence(db)
        try:
            s.save("a", "x")
        finally:
            s.close()
        assert os.path.exists(db)


# ── Edge Cases ───────────────────────────────────────────────────────────────

class TestEdgeCases:
    def test_concurrent_saves(self, store):
        # Many threads saving different doc_ids simultaneously
        errors: list[BaseException] = []

        def worker(i: int):
            try:
                for j in range(10):
                    store.save(f"d{i}", f"v{j}")
            except BaseException as e:  # pragma: no cover
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert not errors
        for i in range(5):
            assert store.version_count(f"d{i}") == 10

    def test_concurrent_saves_same_doc(self, store):
        # Concurrent saves to same doc id — versions must remain unique
        def worker():
            for _ in range(20):
                store.save("shared", "x")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert store.version_count("shared") == 80
        # Versions must be a contiguous range 1..80
        assert store.versions_of("shared") == list(range(1, 81))

    def test_large_content(self, store):
        big = "x" * 100_000
        store.save("big", big)
        d = store.load("big")
        assert len(d.content) == 100_000

    def test_metadata_isolation(self, store):
        meta = {"k": [1, 2]}
        store.save("a", "x", metadata=meta)
        meta["k"].append(3)
        loaded = store.load("a")
        # Stored metadata should not be affected by external mutation
        assert loaded.metadata == {"k": [1, 2]}

    def test_empty_doc_id_allowed(self, store):
        d = store.save("", "x")
        assert d.doc_id == ""
        assert store.load("") is not None

    def test_version_starts_at_one(self, store):
        d = store.save("a", "x")
        assert d.version == 1

    def test_delete_then_resave_starts_at_1(self, store):
        store.save("a", "v1")
        store.save("a", "v2")
        store.delete("a")
        d = store.save("a", "new")
        assert d.version == 1

    def test_stats_average_with_versions(self, store):
        store.save("a", "abcd")  # 4
        store.save("a", "abcdef")  # 6
        s = store.stats()
        assert s.versions == 2
        assert s.total_size == 10
        assert s.avg_doc_size == 5.0
