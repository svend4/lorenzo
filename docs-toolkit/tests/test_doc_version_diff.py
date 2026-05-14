"""Tests for docstoolkit.doc_version_diff (E407)."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_version_diff import (
    DiffSummary,
    DocVersionDiff,
    VersionContent,
)


# ---------------------------------------------------------------------------
# VersionContent dataclass
# ---------------------------------------------------------------------------


class TestVersionContent:
    def test_basic_fields(self):
        vc = VersionContent(doc_id="d", version="v1", content="hi")
        assert vc.doc_id == "d"
        assert vc.version == "v1"
        assert vc.content == "hi"

    def test_default_created_at(self):
        vc = VersionContent(doc_id="d", version="v1", content="hi")
        assert vc.created_at == 0.0

    def test_custom_created_at(self):
        vc = VersionContent(doc_id="d", version="v1", content="hi", created_at=42.5)
        assert vc.created_at == 42.5

    def test_equality(self):
        a = VersionContent("d", "v1", "x", 1.0)
        b = VersionContent("d", "v1", "x", 1.0)
        assert a == b

    def test_inequality(self):
        a = VersionContent("d", "v1", "x", 1.0)
        b = VersionContent("d", "v1", "y", 1.0)
        assert a != b


# ---------------------------------------------------------------------------
# DiffSummary dataclass
# ---------------------------------------------------------------------------


class TestDiffSummary:
    def test_basic_fields(self):
        ds = DiffSummary(
            doc_id="d",
            from_version="v1",
            to_version="v2",
            added_lines=1,
            removed_lines=2,
            changed_lines=1,
        )
        assert ds.doc_id == "d"
        assert ds.from_version == "v1"
        assert ds.to_version == "v2"

    def test_defaults(self):
        ds = DiffSummary("d", "v1", "v2", 0, 0, 0)
        assert ds.unified_diff == ""
        assert ds.similarity == 0.0

    def test_counts(self):
        ds = DiffSummary("d", "v1", "v2", 3, 4, 2)
        assert ds.added_lines == 3
        assert ds.removed_lines == 4
        assert ds.changed_lines == 2

    def test_with_diff_text(self):
        ds = DiffSummary("d", "v1", "v2", 0, 0, 0, unified_diff="---\n+++\n")
        assert "---" in ds.unified_diff

    def test_with_similarity(self):
        ds = DiffSummary("d", "v1", "v2", 0, 0, 0, similarity=0.75)
        assert ds.similarity == 0.75


# ---------------------------------------------------------------------------
# store_version / get_version
# ---------------------------------------------------------------------------


class TestStoreVersion:
    def test_returns_version_content(self):
        d = DocVersionDiff()
        out = d.store_version("doc", "v1", "hello")
        assert isinstance(out, VersionContent)
        assert out.doc_id == "doc"
        assert out.version == "v1"
        assert out.content == "hello"

    def test_default_now(self):
        d = DocVersionDiff()
        out = d.store_version("doc", "v1", "x")
        assert out.created_at > 0.0

    def test_explicit_now(self):
        d = DocVersionDiff()
        out = d.store_version("doc", "v1", "x", now=100.0)
        assert out.created_at == 100.0

    def test_overwrite(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "old", now=1.0)
        d.store_version("doc", "v1", "new", now=2.0)
        vc = d.get_version("doc", "v1")
        assert vc.content == "new"
        assert vc.created_at == 2.0

    def test_get_missing_returns_none(self):
        d = DocVersionDiff()
        assert d.get_version("doc", "v1") is None

    def test_get_after_store(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "hi")
        vc = d.get_version("doc", "v1")
        assert vc is not None
        assert vc.content == "hi"

    def test_multiple_docs_independent(self):
        d = DocVersionDiff()
        d.store_version("a", "v1", "A")
        d.store_version("b", "v1", "B")
        assert d.get_version("a", "v1").content == "A"
        assert d.get_version("b", "v1").content == "B"


# ---------------------------------------------------------------------------
# versions_for
# ---------------------------------------------------------------------------


class TestVersionsFor:
    def test_empty(self):
        d = DocVersionDiff()
        assert d.versions_for("doc") == []

    def test_single(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        assert d.versions_for("doc") == ["v1"]

    def test_sorted(self):
        d = DocVersionDiff()
        d.store_version("doc", "v3", "x")
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "x")
        assert d.versions_for("doc") == ["v1", "v2", "v3"]

    def test_isolation_between_docs(self):
        d = DocVersionDiff()
        d.store_version("a", "v1", "x")
        d.store_version("b", "v2", "x")
        assert d.versions_for("a") == ["v1"]
        assert d.versions_for("b") == ["v2"]


# ---------------------------------------------------------------------------
# delete_version
# ---------------------------------------------------------------------------


class TestDeleteVersion:
    def test_delete_existing_returns_true(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        assert d.delete_version("doc", "v1") is True

    def test_delete_missing_returns_false(self):
        d = DocVersionDiff()
        assert d.delete_version("doc", "v1") is False

    def test_delete_removes_from_get(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.delete_version("doc", "v1")
        assert d.get_version("doc", "v1") is None

    def test_delete_removes_from_versions_for(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "y")
        d.delete_version("doc", "v1")
        assert d.versions_for("doc") == ["v2"]

    def test_delete_last_version_removes_doc(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.delete_version("doc", "v1")
        assert "doc" not in d.all_doc_ids()


# ---------------------------------------------------------------------------
# clear_doc
# ---------------------------------------------------------------------------


class TestClearDoc:
    def test_clear_empty(self):
        d = DocVersionDiff()
        assert d.clear_doc("doc") == 0

    def test_clear_single(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        assert d.clear_doc("doc") == 1

    def test_clear_multiple(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "y")
        d.store_version("doc", "v3", "z")
        assert d.clear_doc("doc") == 3

    def test_clear_removes_all_versions(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "y")
        d.clear_doc("doc")
        assert d.versions_for("doc") == []

    def test_clear_isolated_per_doc(self):
        d = DocVersionDiff()
        d.store_version("a", "v1", "x")
        d.store_version("b", "v1", "x")
        d.clear_doc("a")
        assert d.versions_for("b") == ["v1"]


# ---------------------------------------------------------------------------
# all_doc_ids
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self):
        d = DocVersionDiff()
        assert d.all_doc_ids() == []

    def test_single(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        assert d.all_doc_ids() == ["doc"]

    def test_sorted(self):
        d = DocVersionDiff()
        d.store_version("c", "v1", "x")
        d.store_version("a", "v1", "x")
        d.store_version("b", "v1", "x")
        assert d.all_doc_ids() == ["a", "b", "c"]

    def test_unique(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "y")
        assert d.all_doc_ids() == ["doc"]


# ---------------------------------------------------------------------------
# latest_version_for
# ---------------------------------------------------------------------------


class TestLatestVersionFor:
    def test_empty(self):
        d = DocVersionDiff()
        assert d.latest_version_for("doc") is None

    def test_single(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x", now=10.0)
        assert d.latest_version_for("doc") == "v1"

    def test_returns_highest_ts(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x", now=10.0)
        d.store_version("doc", "v2", "y", now=30.0)
        d.store_version("doc", "v3", "z", now=20.0)
        assert d.latest_version_for("doc") == "v2"

    def test_unknown_doc(self):
        d = DocVersionDiff()
        d.store_version("a", "v1", "x")
        assert d.latest_version_for("b") is None


# ---------------------------------------------------------------------------
# compute_diff
# ---------------------------------------------------------------------------


class TestComputeDiff:
    def test_missing_from(self):
        d = DocVersionDiff()
        d.store_version("doc", "v2", "x")
        assert d.compute_diff("doc", "v1", "v2") is None

    def test_missing_to(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        assert d.compute_diff("doc", "v1", "v2") is None

    def test_both_missing(self):
        d = DocVersionDiff()
        assert d.compute_diff("doc", "v1", "v2") is None

    def test_identical_content(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "same")
        d.store_version("doc", "v2", "same")
        out = d.compute_diff("doc", "v1", "v2")
        assert out is not None
        assert out.added_lines == 0
        assert out.removed_lines == 0
        assert out.changed_lines == 0
        assert out.similarity == 1.0

    def test_pure_addition(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "line1\nline2")
        d.store_version("doc", "v2", "line1\nline2\nline3\nline4")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.added_lines == 2
        assert out.removed_lines == 0
        assert out.changed_lines == 0

    def test_pure_removal(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "line1\nline2\nline3")
        d.store_version("doc", "v2", "line1")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.added_lines == 0
        assert out.removed_lines == 2
        assert out.changed_lines == 0

    def test_modification_counts_changed(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "alpha\nbeta\ngamma")
        d.store_version("doc", "v2", "alpha\nBETA\ngamma")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.added_lines == 1
        assert out.removed_lines == 1
        assert out.changed_lines >= 1

    def test_unified_diff_text_nonempty_on_change(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "old")
        d.store_version("doc", "v2", "new")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.unified_diff != ""
        assert "old" in out.unified_diff or "-old" in out.unified_diff
        assert "new" in out.unified_diff or "+new" in out.unified_diff

    def test_unified_diff_empty_on_identical(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "same")
        d.store_version("doc", "v2", "same")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.unified_diff == ""

    def test_unified_diff_has_filenames(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "a")
        d.store_version("doc", "v2", "b")
        out = d.compute_diff("doc", "v1", "v2")
        assert "doc@v1" in out.unified_diff
        assert "doc@v2" in out.unified_diff

    def test_similarity_range(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "hello world")
        d.store_version("doc", "v2", "hello there")
        out = d.compute_diff("doc", "v1", "v2")
        assert 0.0 <= out.similarity <= 1.0

    def test_similarity_zero_for_disjoint(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "aaaa")
        d.store_version("doc", "v2", "bbbb")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.similarity == 0.0

    def test_diff_summary_doc_id_set(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x")
        d.store_version("doc", "v2", "y")
        out = d.compute_diff("doc", "v1", "v2")
        assert out.doc_id == "doc"
        assert out.from_version == "v1"
        assert out.to_version == "v2"


# ---------------------------------------------------------------------------
# compute_diff_to_latest
# ---------------------------------------------------------------------------


class TestComputeDiffToLatest:
    def test_no_versions(self):
        d = DocVersionDiff()
        assert d.compute_diff_to_latest("doc", "v1") is None

    def test_single_version(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "x", now=10.0)
        out = d.compute_diff_to_latest("doc", "v1")
        assert out is not None
        assert out.from_version == "v1"
        assert out.to_version == "v1"
        assert out.similarity == 1.0

    def test_picks_latest_by_ts(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "first", now=10.0)
        d.store_version("doc", "v2", "second", now=20.0)
        d.store_version("doc", "v3", "third", now=15.0)
        out = d.compute_diff_to_latest("doc", "v1")
        assert out.to_version == "v2"

    def test_missing_from_version(self):
        d = DocVersionDiff()
        d.store_version("doc", "v2", "x", now=5.0)
        # from_version doesn't exist
        assert d.compute_diff_to_latest("doc", "v1") is None


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        d = DocVersionDiff()
        s = d.stats()
        assert s["total_versions"] == 0
        assert s["unique_docs"] == 0
        assert s["total_content_chars"] == 0

    def test_single_version(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "hello")
        s = d.stats()
        assert s["total_versions"] == 1
        assert s["unique_docs"] == 1
        assert s["total_content_chars"] == 5

    def test_multiple_versions_same_doc(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "ab")
        d.store_version("doc", "v2", "cde")
        s = d.stats()
        assert s["total_versions"] == 2
        assert s["unique_docs"] == 1
        assert s["total_content_chars"] == 5

    def test_multiple_docs(self):
        d = DocVersionDiff()
        d.store_version("a", "v1", "x")
        d.store_version("b", "v1", "yy")
        s = d.stats()
        assert s["total_versions"] == 2
        assert s["unique_docs"] == 2
        assert s["total_content_chars"] == 3

    def test_after_delete(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "abc")
        d.delete_version("doc", "v1")
        s = d.stats()
        assert s["total_versions"] == 0
        assert s["unique_docs"] == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_store(self):
        d = DocVersionDiff()

        def worker(idx: int) -> None:
            for i in range(20):
                d.store_version(f"doc{idx}", f"v{i}", f"content {idx}/{i}")

        threads = [threading.Thread(target=worker, args=(k,)) for k in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(d.all_doc_ids()) == 8
        for k in range(8):
            assert len(d.versions_for(f"doc{k}")) == 20

    def test_concurrent_store_and_delete(self):
        d = DocVersionDiff()
        for i in range(50):
            d.store_version("doc", f"v{i}", str(i))

        def deleter() -> None:
            for i in range(0, 50, 2):
                d.delete_version("doc", f"v{i}")

        def reader() -> None:
            for _ in range(30):
                d.versions_for("doc")
                d.stats()

        threads = [threading.Thread(target=deleter)] + [
            threading.Thread(target=reader) for _ in range(4)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        remaining = d.versions_for("doc")
        # Odd ones should remain
        for v in remaining:
            assert int(v[1:]) % 2 == 1

    def test_concurrent_stats(self):
        d = DocVersionDiff()
        for i in range(100):
            d.store_version(f"doc{i}", "v1", "x" * i)

        results = []

        def reader() -> None:
            results.append(d.stats())

        threads = [threading.Thread(target=reader) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
        for r in results:
            assert r["unique_docs"] == 100
            assert r["total_versions"] == 100


# ---------------------------------------------------------------------------
# Integration / end-to-end
# ---------------------------------------------------------------------------


class TestIntegration:
    def test_full_workflow(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "line one\nline two", now=1.0)
        d.store_version("doc", "v2", "line one\nline two\nline three", now=2.0)
        out = d.compute_diff("doc", "v1", "v2")
        assert out.added_lines == 1
        assert out.removed_lines == 0
        latest = d.compute_diff_to_latest("doc", "v1")
        assert latest.to_version == "v2"

    def test_round_trip(self):
        d = DocVersionDiff()
        d.store_version("doc", "v1", "alpha")
        vc = d.get_version("doc", "v1")
        assert vc.content == "alpha"
        d.delete_version("doc", "v1")
        assert d.get_version("doc", "v1") is None
