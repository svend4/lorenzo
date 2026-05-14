"""Tests for E316 DocArchiveStore (docstoolkit.doc_archive_store)."""
from __future__ import annotations

import threading
import time
from dataclasses import fields

import pytest

from docstoolkit.doc_archive_store import ArchivedDoc, ArchiveStats, DocArchiveStore


# ---------------------------------------------------------------------------
# TestArchivedDocDataclass
# ---------------------------------------------------------------------------


class TestArchivedDocDataclass:
    def test_required_fields_present(self):
        names = {f.name for f in fields(ArchivedDoc)}
        assert {"archive_id", "doc_id", "content"} <= names

    def test_optional_defaults(self):
        doc = ArchivedDoc(archive_id="a", doc_id="d", content="c")
        assert doc.archived_at == 0.0
        assert doc.archived_by == ""
        assert doc.reason == ""
        assert doc.metadata == {}

    def test_metadata_is_independent_per_instance(self):
        doc1 = ArchivedDoc(archive_id="a1", doc_id="d", content="x")
        doc2 = ArchivedDoc(archive_id="a2", doc_id="d", content="y")
        doc1.metadata["k"] = "v"
        assert "k" not in doc2.metadata

    def test_full_construction(self):
        doc = ArchivedDoc(
            archive_id="id1",
            doc_id="doc1",
            content="hello",
            archived_at=1_000.0,
            archived_by="alice",
            reason="manual",
            metadata={"env": "prod"},
        )
        assert doc.archive_id == "id1"
        assert doc.doc_id == "doc1"
        assert doc.content == "hello"
        assert doc.archived_at == 1_000.0
        assert doc.archived_by == "alice"
        assert doc.reason == "manual"
        assert doc.metadata == {"env": "prod"}

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ArchivedDoc)


# ---------------------------------------------------------------------------
# TestArchiveStatsDataclass
# ---------------------------------------------------------------------------


class TestArchiveStatsDataclass:
    def test_fields(self):
        names = {f.name for f in fields(ArchiveStats)}
        assert names == {"total_archives", "unique_docs", "total_size_chars"}

    def test_construction(self):
        s = ArchiveStats(total_archives=5, unique_docs=3, total_size_chars=100)
        assert s.total_archives == 5
        assert s.unique_docs == 3
        assert s.total_size_chars == 100

    def test_is_dataclass(self):
        import dataclasses
        assert dataclasses.is_dataclass(ArchiveStats)


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_default_init(self):
        store = DocArchiveStore()
        assert store is not None

    def test_initial_stats_empty(self):
        store = DocArchiveStore()
        s = store.stats()
        assert s.total_archives == 0
        assert s.unique_docs == 0
        assert s.total_size_chars == 0

    def test_initial_all_doc_ids_empty(self):
        store = DocArchiveStore()
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestArchive
# ---------------------------------------------------------------------------


class TestArchive:
    def test_returns_archived_doc(self):
        store = DocArchiveStore()
        result = store.archive("doc1", "content")
        assert isinstance(result, ArchivedDoc)

    def test_archive_id_is_uuid(self):
        import uuid
        store = DocArchiveStore()
        result = store.archive("doc1", "content")
        # Should parse without error
        parsed = uuid.UUID(result.archive_id)
        assert str(parsed) == result.archive_id

    def test_archive_id_unique_across_calls(self):
        store = DocArchiveStore()
        ids = {store.archive("doc1", "c").archive_id for _ in range(10)}
        assert len(ids) == 10

    def test_doc_id_stored(self):
        store = DocArchiveStore()
        result = store.archive("mydoc", "body")
        assert result.doc_id == "mydoc"

    def test_content_stored(self):
        store = DocArchiveStore()
        result = store.archive("d", "hello world")
        assert result.content == "hello world"

    def test_archived_at_defaults_to_now(self):
        store = DocArchiveStore()
        before = time.time()
        result = store.archive("d", "c")
        after = time.time()
        assert before <= result.archived_at <= after

    def test_archived_at_custom_now(self):
        store = DocArchiveStore()
        result = store.archive("d", "c", now=12345.6)
        assert result.archived_at == 12345.6

    def test_archived_by_stored(self):
        store = DocArchiveStore()
        result = store.archive("d", "c", archived_by="bob")
        assert result.archived_by == "bob"

    def test_reason_stored(self):
        store = DocArchiveStore()
        result = store.archive("d", "c", reason="pre-delete")
        assert result.reason == "pre-delete"

    def test_metadata_stored(self):
        store = DocArchiveStore()
        result = store.archive("d", "c", metadata={"key": "val"})
        assert result.metadata == {"key": "val"}

    def test_metadata_defaults_to_empty_dict(self):
        store = DocArchiveStore()
        result = store.archive("d", "c")
        assert result.metadata == {}

    def test_metadata_is_copied(self):
        store = DocArchiveStore()
        m = {"k": "v"}
        result = store.archive("d", "c", metadata=m)
        m["extra"] = "x"
        assert "extra" not in result.metadata

    def test_multiple_archives_same_doc(self):
        store = DocArchiveStore()
        a1 = store.archive("doc", "v1")
        a2 = store.archive("doc", "v2")
        a3 = store.archive("doc", "v3")
        assert a1.archive_id != a2.archive_id != a3.archive_id

    def test_archive_increments_stats(self):
        store = DocArchiveStore()
        store.archive("d", "hello")
        s = store.stats()
        assert s.total_archives == 1

    def test_empty_content_archived(self):
        store = DocArchiveStore()
        result = store.archive("d", "")
        assert result.content == ""


# ---------------------------------------------------------------------------
# TestRestoreLatest
# ---------------------------------------------------------------------------


class TestRestoreLatest:
    def test_returns_none_for_unknown_doc(self):
        store = DocArchiveStore()
        assert store.restore_latest("no-such-doc") is None

    def test_returns_only_archive(self):
        store = DocArchiveStore()
        a = store.archive("doc", "v1")
        result = store.restore_latest("doc")
        assert result is not None
        assert result.archive_id == a.archive_id

    def test_returns_most_recent(self):
        store = DocArchiveStore()
        store.archive("doc", "v1", now=1.0)
        store.archive("doc", "v2", now=2.0)
        a3 = store.archive("doc", "v3", now=3.0)
        result = store.restore_latest("doc")
        assert result is not None
        assert result.archive_id == a3.archive_id
        assert result.content == "v3"

    def test_does_not_affect_other_docs(self):
        store = DocArchiveStore()
        store.archive("doc_a", "a_content")
        b = store.archive("doc_b", "b_content")
        result = store.restore_latest("doc_b")
        assert result is not None
        assert result.archive_id == b.archive_id


# ---------------------------------------------------------------------------
# TestRestoreById
# ---------------------------------------------------------------------------


class TestRestoreById:
    def test_found(self):
        store = DocArchiveStore()
        a = store.archive("doc", "body")
        result = store.restore_by_id(a.archive_id)
        assert result is not None
        assert result.archive_id == a.archive_id

    def test_not_found(self):
        store = DocArchiveStore()
        assert store.restore_by_id("nonexistent-id") is None

    def test_content_matches(self):
        store = DocArchiveStore()
        a = store.archive("doc", "specific content")
        result = store.restore_by_id(a.archive_id)
        assert result is not None
        assert result.content == "specific content"


# ---------------------------------------------------------------------------
# TestDeleteArchive
# ---------------------------------------------------------------------------


class TestDeleteArchive:
    def test_returns_true_when_exists(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        assert store.delete_archive(a.archive_id) is True

    def test_returns_false_when_not_exists(self):
        store = DocArchiveStore()
        assert store.delete_archive("ghost-id") is False

    def test_archive_removed_after_delete(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        store.delete_archive(a.archive_id)
        assert store.get_archive(a.archive_id) is None

    def test_stats_updated_after_delete(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        store.delete_archive(a.archive_id)
        assert store.stats().total_archives == 0

    def test_doc_removed_from_all_doc_ids_when_last_archive_deleted(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        store.delete_archive(a.archive_id)
        assert "doc" not in store.all_doc_ids()

    def test_doc_remains_in_all_doc_ids_when_other_archives_exist(self):
        store = DocArchiveStore()
        a1 = store.archive("doc", "v1")
        store.archive("doc", "v2")
        store.delete_archive(a1.archive_id)
        assert "doc" in store.all_doc_ids()

    def test_double_delete_returns_false(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        store.delete_archive(a.archive_id)
        assert store.delete_archive(a.archive_id) is False


# ---------------------------------------------------------------------------
# TestPurgeDoc
# ---------------------------------------------------------------------------


class TestPurgeDoc:
    def test_returns_count(self):
        store = DocArchiveStore()
        store.archive("doc", "v1")
        store.archive("doc", "v2")
        store.archive("doc", "v3")
        assert store.purge_doc("doc") == 3

    def test_returns_zero_for_unknown_doc(self):
        store = DocArchiveStore()
        assert store.purge_doc("ghost") == 0

    def test_all_archives_removed(self):
        store = DocArchiveStore()
        ids = [store.archive("doc", f"v{i}").archive_id for i in range(4)]
        store.purge_doc("doc")
        for aid in ids:
            assert store.get_archive(aid) is None

    def test_doc_removed_from_all_doc_ids(self):
        store = DocArchiveStore()
        store.archive("doc", "v1")
        store.purge_doc("doc")
        assert "doc" not in store.all_doc_ids()

    def test_other_docs_unaffected(self):
        store = DocArchiveStore()
        store.archive("doc_a", "a")
        store.archive("doc_b", "b")
        store.purge_doc("doc_a")
        assert "doc_b" in store.all_doc_ids()
        assert store.restore_latest("doc_b") is not None


# ---------------------------------------------------------------------------
# TestArchivesForDoc
# ---------------------------------------------------------------------------


class TestArchivesForDoc:
    def test_empty_for_unknown_doc(self):
        store = DocArchiveStore()
        assert store.archives_for_doc("ghost") == []

    def test_most_recent_first(self):
        store = DocArchiveStore()
        a1 = store.archive("doc", "v1", now=1.0)
        a2 = store.archive("doc", "v2", now=2.0)
        a3 = store.archive("doc", "v3", now=3.0)
        result = store.archives_for_doc("doc")
        assert [r.archive_id for r in result] == [
            a3.archive_id,
            a2.archive_id,
            a1.archive_id,
        ]

    def test_limit_respected(self):
        store = DocArchiveStore()
        for i in range(5):
            store.archive("doc", f"v{i}", now=float(i))
        result = store.archives_for_doc("doc", limit=2)
        assert len(result) == 2

    def test_limit_returns_most_recent(self):
        store = DocArchiveStore()
        for i in range(5):
            store.archive("doc", f"v{i}", now=float(i))
        result = store.archives_for_doc("doc", limit=2)
        assert result[0].content == "v4"
        assert result[1].content == "v3"

    def test_no_limit_returns_all(self):
        store = DocArchiveStore()
        for i in range(5):
            store.archive("doc", f"v{i}")
        result = store.archives_for_doc("doc")
        assert len(result) == 5

    def test_single_archive_returned(self):
        store = DocArchiveStore()
        a = store.archive("doc", "only")
        result = store.archives_for_doc("doc")
        assert len(result) == 1
        assert result[0].archive_id == a.archive_id


# ---------------------------------------------------------------------------
# TestGetArchive
# ---------------------------------------------------------------------------


class TestGetArchive:
    def test_found(self):
        store = DocArchiveStore()
        a = store.archive("doc", "body")
        result = store.get_archive(a.archive_id)
        assert result is not None
        assert result.archive_id == a.archive_id

    def test_not_found(self):
        store = DocArchiveStore()
        assert store.get_archive("missing") is None

    def test_returns_same_object_as_restore_by_id(self):
        store = DocArchiveStore()
        a = store.archive("doc", "c")
        assert store.get_archive(a.archive_id) is store.restore_by_id(a.archive_id)


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty_initially(self):
        store = DocArchiveStore()
        assert store.all_doc_ids() == []

    def test_sorted(self):
        store = DocArchiveStore()
        store.archive("doc_c", "c")
        store.archive("doc_a", "a")
        store.archive("doc_b", "b")
        assert store.all_doc_ids() == ["doc_a", "doc_b", "doc_c"]

    def test_no_duplicates_for_same_doc(self):
        store = DocArchiveStore()
        store.archive("doc", "v1")
        store.archive("doc", "v2")
        store.archive("doc", "v3")
        ids = store.all_doc_ids()
        assert ids.count("doc") == 1

    def test_only_docs_with_archives(self):
        store = DocArchiveStore()
        a = store.archive("doc", "v1")
        store.delete_archive(a.archive_id)
        assert "doc" not in store.all_doc_ids()

    def test_multiple_docs(self):
        store = DocArchiveStore()
        for name in ["beta", "alpha", "gamma"]:
            store.archive(name, "content")
        assert store.all_doc_ids() == ["alpha", "beta", "gamma"]


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_store(self):
        store = DocArchiveStore()
        s = store.stats()
        assert s.total_archives == 0
        assert s.unique_docs == 0
        assert s.total_size_chars == 0

    def test_total_archives(self):
        store = DocArchiveStore()
        for i in range(4):
            store.archive("doc", f"v{i}")
        assert store.stats().total_archives == 4

    def test_unique_docs(self):
        store = DocArchiveStore()
        store.archive("a", "x")
        store.archive("b", "y")
        store.archive("a", "z")  # second archive for "a"
        assert store.stats().unique_docs == 2

    def test_total_size_chars(self):
        store = DocArchiveStore()
        store.archive("d", "hello")  # 5 chars
        store.archive("d", "world!")  # 6 chars
        assert store.stats().total_size_chars == 11

    def test_size_chars_decreases_after_delete(self):
        store = DocArchiveStore()
        a = store.archive("d", "hello")  # 5 chars
        store.archive("d", "world!")     # 6 chars
        store.delete_archive(a.archive_id)
        assert store.stats().total_size_chars == 6

    def test_stats_after_purge(self):
        store = DocArchiveStore()
        store.archive("doc", "v1")
        store.archive("doc", "v2")
        store.purge_doc("doc")
        s = store.stats()
        assert s.total_archives == 0
        assert s.unique_docs == 0
        assert s.total_size_chars == 0


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_archive_calls(self):
        store = DocArchiveStore()
        errors: list = []
        results: list = []
        lock = threading.Lock()

        def worker(i: int) -> None:
            try:
                doc = store.archive(f"doc_{i % 5}", f"content_{i}")
                with lock:
                    results.append(doc.archive_id)
            except Exception as exc:  # noqa: BLE001
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(50)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Errors during concurrent archive: {errors}"
        assert len(results) == 50
        assert len(set(results)) == 50  # all UUIDs unique

    def test_concurrent_mixed_operations(self):
        store = DocArchiveStore()
        errors: list = []

        # Pre-populate
        archive_ids = [
            store.archive("shared", f"initial_{i}").archive_id for i in range(10)
        ]

        def archiver() -> None:
            try:
                for i in range(20):
                    store.archive("shared", f"data_{i}")
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def reader() -> None:
            try:
                for _ in range(20):
                    store.restore_latest("shared")
                    store.archives_for_doc("shared", limit=5)
                    store.stats()
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        def deleter() -> None:
            try:
                for aid in archive_ids[:5]:
                    store.delete_archive(aid)
            except Exception as exc:  # noqa: BLE001
                errors.append(exc)

        threads = (
            [threading.Thread(target=archiver) for _ in range(3)]
            + [threading.Thread(target=reader) for _ in range(3)]
            + [threading.Thread(target=deleter)]
        )
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Errors during mixed concurrent ops: {errors}"
