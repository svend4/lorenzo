"""Tests for E181 docstoolkit.doc_archive."""
from __future__ import annotations

import gzip
import os
import tempfile

import pytest

from docstoolkit.doc_archive import (
    ArchivedDoc,
    ArchiveStats,
    DocArchive,
    RetentionPolicy,
)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


class TestArchivedDoc:
    def test_construction_fields(self):
        d = ArchivedDoc(doc_id="a", original_size=100, compressed_size=40, archived_at=1.0)
        assert d.doc_id == "a"
        assert d.original_size == 100
        assert d.compressed_size == 40
        assert d.archived_at == 1.0

    def test_compression_ratio_normal(self):
        d = ArchivedDoc("a", 200, 50, 0.0)
        assert d.compression_ratio == 0.25

    def test_compression_ratio_zero_original(self):
        d = ArchivedDoc("a", 0, 20, 0.0)
        assert d.compression_ratio == 0.0

    def test_compression_ratio_one_to_one(self):
        d = ArchivedDoc("a", 100, 100, 0.0)
        assert d.compression_ratio == 1.0


class TestRetentionPolicy:
    def test_defaults(self):
        p = RetentionPolicy()
        assert p.max_age_seconds is None
        assert p.max_count is None
        assert p.min_count == 0

    def test_custom_values(self):
        p = RetentionPolicy(max_age_seconds=10.0, max_count=5, min_count=2)
        assert p.max_age_seconds == 10.0
        assert p.max_count == 5
        assert p.min_count == 2


class TestArchiveStats:
    def test_space_saved_positive(self):
        s = ArchiveStats(total_archived=2, total_original_size=1000, total_compressed_size=400)
        assert s.space_saved == 600

    def test_space_saved_zero(self):
        s = ArchiveStats(total_archived=0, total_original_size=0, total_compressed_size=0)
        assert s.space_saved == 0

    def test_avg_ratio_normal(self):
        s = ArchiveStats(total_archived=2, total_original_size=1000, total_compressed_size=250)
        assert s.avg_ratio == 0.25

    def test_avg_ratio_zero_original(self):
        s = ArchiveStats(total_archived=0, total_original_size=0, total_compressed_size=0)
        assert s.avg_ratio == 0.0


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def arch():
    a = DocArchive()
    yield a
    a.close()


# ---------------------------------------------------------------------------
# Archive (compress & store)
# ---------------------------------------------------------------------------


class TestArchive:
    def test_archive_returns_archived_doc(self, arch):
        d = arch.archive("doc1", "hello world", now=1.0)
        assert isinstance(d, ArchivedDoc)
        assert d.doc_id == "doc1"
        assert d.archived_at == 1.0

    def test_archive_records_original_size(self, arch):
        text = "hello world"
        d = arch.archive("doc1", text, now=0.0)
        assert d.original_size == len(text.encode("utf-8"))

    def test_archive_records_compressed_size(self, arch):
        text = "a" * 1000
        d = arch.archive("doc1", text, now=0.0)
        expected = len(gzip.compress(text.encode("utf-8")))
        assert d.compressed_size == expected

    def test_archive_overwrites_existing(self, arch):
        arch.archive("doc1", "old", now=1.0)
        arch.archive("doc1", "new", now=2.0)
        assert arch.count == 1
        assert arch.restore("doc1") == "new"

    def test_archive_empty_content(self, arch):
        d = arch.archive("doc1", "", now=0.0)
        assert d.original_size == 0
        assert arch.restore("doc1") == ""


# ---------------------------------------------------------------------------
# Restore (decompress)
# ---------------------------------------------------------------------------


class TestRestore:
    def test_restore_roundtrip(self, arch):
        arch.archive("doc1", "hello", now=0.0)
        assert arch.restore("doc1") == "hello"

    def test_restore_unicode(self, arch):
        text = "Привет, мир! 你好 🌍"
        arch.archive("doc1", text, now=0.0)
        assert arch.restore("doc1") == text

    def test_restore_missing_returns_none(self, arch):
        assert arch.restore("nope") is None

    def test_restore_large_document(self, arch):
        text = "abc " * 10_000
        arch.archive("big", text, now=0.0)
        assert arch.restore("big") == text


# ---------------------------------------------------------------------------
# Exists
# ---------------------------------------------------------------------------


class TestExists:
    def test_exists_true(self, arch):
        arch.archive("d", "x", now=0.0)
        assert arch.exists("d") is True

    def test_exists_false(self, arch):
        assert arch.exists("nope") is False

    def test_exists_after_delete(self, arch):
        arch.archive("d", "x", now=0.0)
        arch.delete("d")
        assert arch.exists("d") is False


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------


class TestDelete:
    def test_delete_removes_doc(self, arch):
        arch.archive("d", "x", now=0.0)
        assert arch.delete("d") is True
        assert arch.count == 0

    def test_delete_missing_returns_false(self, arch):
        assert arch.delete("nope") is False

    def test_delete_idempotent(self, arch):
        arch.archive("d", "x", now=0.0)
        assert arch.delete("d") is True
        assert arch.delete("d") is False


# ---------------------------------------------------------------------------
# List all
# ---------------------------------------------------------------------------


class TestListAll:
    def test_list_empty(self, arch):
        assert arch.list_all() == []

    def test_list_returns_all(self, arch):
        arch.archive("a", "x", now=1.0)
        arch.archive("b", "y", now=2.0)
        arch.archive("c", "z", now=3.0)
        docs = arch.list_all()
        assert len(docs) == 3
        assert {d.doc_id for d in docs} == {"a", "b", "c"}

    def test_list_sorted_by_time_ascending(self, arch):
        arch.archive("late", "x", now=3.0)
        arch.archive("early", "y", now=1.0)
        arch.archive("mid", "z", now=2.0)
        ids = [d.doc_id for d in arch.list_all()]
        assert ids == ["early", "mid", "late"]


# ---------------------------------------------------------------------------
# Retention — age
# ---------------------------------------------------------------------------


class TestApplyRetentionAge:
    def test_drops_old_entries(self, arch):
        arch.archive("old", "x", now=0.0)
        arch.archive("new", "y", now=100.0)
        removed = arch.apply_retention(RetentionPolicy(max_age_seconds=10.0), now=100.0)
        assert removed == 1
        assert arch.exists("old") is False
        assert arch.exists("new") is True

    def test_keeps_all_within_age(self, arch):
        arch.archive("a", "x", now=95.0)
        arch.archive("b", "y", now=99.0)
        removed = arch.apply_retention(RetentionPolicy(max_age_seconds=10.0), now=100.0)
        assert removed == 0
        assert arch.count == 2

    def test_no_age_limit(self, arch):
        arch.archive("a", "x", now=0.0)
        removed = arch.apply_retention(RetentionPolicy(), now=1_000_000.0)
        assert removed == 0


# ---------------------------------------------------------------------------
# Retention — count
# ---------------------------------------------------------------------------


class TestApplyRetentionCount:
    def test_drops_oldest_above_cap(self, arch):
        for i in range(5):
            arch.archive(f"d{i}", "x", now=float(i))
        removed = arch.apply_retention(RetentionPolicy(max_count=3), now=10.0)
        assert removed == 2
        assert arch.exists("d0") is False
        assert arch.exists("d1") is False
        assert arch.exists("d2") is True
        assert arch.exists("d4") is True

    def test_keeps_all_below_cap(self, arch):
        arch.archive("a", "x", now=1.0)
        arch.archive("b", "y", now=2.0)
        removed = arch.apply_retention(RetentionPolicy(max_count=5), now=10.0)
        assert removed == 0

    def test_max_count_zero_clears_all(self, arch):
        arch.archive("a", "x", now=1.0)
        arch.archive("b", "y", now=2.0)
        removed = arch.apply_retention(RetentionPolicy(max_count=0), now=10.0)
        assert removed == 2
        assert arch.count == 0


# ---------------------------------------------------------------------------
# Retention — min_count
# ---------------------------------------------------------------------------


class TestApplyRetentionMinCount:
    def test_min_count_prevents_full_eviction(self, arch):
        # All entries are "old" — without min_count they would all be evicted.
        for i in range(5):
            arch.archive(f"d{i}", "x", now=float(i))
        removed = arch.apply_retention(
            RetentionPolicy(max_age_seconds=1.0, min_count=2), now=1000.0
        )
        # 5 candidates for removal, but min_count=2 retains 2 newest
        assert removed == 3
        assert arch.count == 2
        # The newest two (d3, d4) should be retained
        remaining = {d.doc_id for d in arch.list_all()}
        assert remaining == {"d3", "d4"}

    def test_min_count_with_max_count(self, arch):
        for i in range(4):
            arch.archive(f"d{i}", "x", now=float(i))
        # cap = 1, but min_count = 3
        removed = arch.apply_retention(
            RetentionPolicy(max_count=1, min_count=3), now=10.0
        )
        assert removed == 1
        assert arch.count == 3

    def test_min_count_zero_default(self, arch):
        for i in range(3):
            arch.archive(f"d{i}", "x", now=float(i))
        removed = arch.apply_retention(
            RetentionPolicy(max_age_seconds=0.1), now=1000.0
        )
        assert removed == 3
        assert arch.count == 0


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_stats_empty(self, arch):
        s = arch.stats()
        assert s.total_archived == 0
        assert s.total_original_size == 0
        assert s.total_compressed_size == 0
        assert s.space_saved == 0
        assert s.avg_ratio == 0.0

    def test_stats_counts_documents(self, arch):
        arch.archive("a", "x" * 100, now=1.0)
        arch.archive("b", "y" * 100, now=2.0)
        s = arch.stats()
        assert s.total_archived == 2

    def test_stats_sizes_match_blobs(self, arch):
        text = "a" * 1000
        arch.archive("d", text, now=0.0)
        s = arch.stats()
        assert s.total_original_size == len(text.encode("utf-8"))
        expected = len(gzip.compress(text.encode("utf-8")))
        assert s.total_compressed_size == expected

    def test_stats_space_saved_for_compressible(self, arch):
        arch.archive("d", "a" * 5000, now=0.0)
        s = arch.stats()
        assert s.space_saved > 0


# ---------------------------------------------------------------------------
# Compression ratio
# ---------------------------------------------------------------------------


class TestCompressionRatio:
    def test_compressible_content_has_low_ratio(self, arch):
        d = arch.archive("d", "a" * 5000, now=0.0)
        assert d.compression_ratio < 0.5

    def test_ratio_zero_for_empty(self, arch):
        d = arch.archive("d", "", now=0.0)
        assert d.compression_ratio == 0.0

    def test_ratio_matches_dataclass_property(self, arch):
        d = arch.archive("d", "hello world hello world", now=0.0)
        expected = d.compressed_size / d.original_size
        assert d.compression_ratio == expected


# ---------------------------------------------------------------------------
# Oldest / newest
# ---------------------------------------------------------------------------


class TestOldestNewest:
    def test_oldest_empty(self, arch):
        assert arch.oldest() is None

    def test_newest_empty(self, arch):
        assert arch.newest() is None

    def test_oldest_and_newest(self, arch):
        arch.archive("a", "x", now=5.0)
        arch.archive("b", "y", now=1.0)
        arch.archive("c", "z", now=10.0)
        assert arch.oldest().doc_id == "b"
        assert arch.newest().doc_id == "c"

    def test_single_doc_is_both_oldest_and_newest(self, arch):
        arch.archive("only", "x", now=7.0)
        assert arch.oldest().doc_id == "only"
        assert arch.newest().doc_id == "only"


# ---------------------------------------------------------------------------
# Batch
# ---------------------------------------------------------------------------


class TestArchiveBatch:
    def test_batch_archives_all(self, arch):
        docs = {"a": "x", "b": "y", "c": "z"}
        result = arch.archive_batch(docs, now=5.0)
        assert len(result) == 3
        assert arch.count == 3

    def test_batch_returns_metadata(self, arch):
        docs = {"a": "hello", "b": "world"}
        result = arch.archive_batch(docs, now=2.5)
        ids = {d.doc_id for d in result}
        assert ids == {"a", "b"}
        for d in result:
            assert d.archived_at == 2.5

    def test_batch_empty(self, arch):
        result = arch.archive_batch({}, now=0.0)
        assert result == []
        assert arch.count == 0

    def test_batch_overwrites(self, arch):
        arch.archive("a", "old", now=0.0)
        arch.archive_batch({"a": "new", "b": "also"}, now=1.0)
        assert arch.restore("a") == "new"
        assert arch.restore("b") == "also"
        assert arch.count == 2


# ---------------------------------------------------------------------------
# Clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_clear_empty(self, arch):
        arch.clear()
        assert arch.count == 0

    def test_clear_removes_all(self, arch):
        arch.archive("a", "x", now=0.0)
        arch.archive("b", "y", now=1.0)
        arch.clear()
        assert arch.count == 0
        assert arch.list_all() == []

    def test_clear_then_reuse(self, arch):
        arch.archive("a", "x", now=0.0)
        arch.clear()
        arch.archive("a", "y", now=1.0)
        assert arch.restore("a") == "y"


# ---------------------------------------------------------------------------
# Persistence (file-backed db)
# ---------------------------------------------------------------------------


class TestPersistence:
    def test_persists_across_instances(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "archive.db")
            a1 = DocArchive(db_path=path)
            a1.archive("d", "hello", now=1.0)
            a1.close()

            a2 = DocArchive(db_path=path)
            try:
                assert a2.exists("d") is True
                assert a2.restore("d") == "hello"
            finally:
                a2.close()

    def test_file_db_count_persists(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "archive.db")
            a1 = DocArchive(db_path=path)
            a1.archive("a", "x", now=1.0)
            a1.archive("b", "y", now=2.0)
            a1.close()

            a2 = DocArchive(db_path=path)
            try:
                assert a2.count == 2
            finally:
                a2.close()

    def test_close_is_idempotent(self):
        a = DocArchive()
        a.close()
        a.close()  # should not raise


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_empty_content_roundtrip(self, arch):
        arch.archive("e", "", now=0.0)
        assert arch.restore("e") == ""
        assert arch.exists("e") is True

    def test_unicode_content(self, arch):
        text = "日本語テキスト — кириллица — 🚀🌍🌟"
        arch.archive("u", text, now=0.0)
        assert arch.restore("u") == text

    def test_large_content(self, arch):
        text = ("Lorem ipsum dolor sit amet " * 5000)
        arch.archive("big", text, now=0.0)
        assert arch.restore("big") == text
        # Highly compressible
        d = next(d for d in arch.list_all() if d.doc_id == "big")
        assert d.compression_ratio < 0.1

    def test_total_size_bytes_matches_stats(self, arch):
        arch.archive("a", "abc" * 200, now=0.0)
        arch.archive("b", "xyz" * 200, now=1.0)
        assert arch.total_size_bytes() == arch.stats().total_compressed_size

    def test_count_property(self, arch):
        assert arch.count == 0
        arch.archive("a", "x", now=0.0)
        assert arch.count == 1
        arch.archive("b", "y", now=1.0)
        assert arch.count == 2

    def test_doc_ids_with_special_characters(self, arch):
        doc_id = "doc/with:special?chars*and spaces"
        arch.archive(doc_id, "content", now=0.0)
        assert arch.restore(doc_id) == "content"

    def test_apply_retention_on_empty_archive(self, arch):
        removed = arch.apply_retention(
            RetentionPolicy(max_age_seconds=1.0, max_count=1), now=100.0
        )
        assert removed == 0
