"""Tests for E368 DocExportManifest."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_export_manifest import (
    DocExportManifest,
    ExportManifest,
    ManifestEntry,
    ManifestStats,
)


# ---------------------------------------------------------------------------
# Dataclass tests
# ---------------------------------------------------------------------------


class TestManifestEntryDataclass:
    def test_create_with_required_fields(self):
        entry = ManifestEntry(path="out/a.pdf", doc_id="doc1", format="pdf")
        assert entry.path == "out/a.pdf"
        assert entry.doc_id == "doc1"
        assert entry.format == "pdf"

    def test_default_size_bytes_is_zero(self):
        entry = ManifestEntry(path="x", doc_id="d", format="md")
        assert entry.size_bytes == 0

    def test_default_checksum_empty(self):
        entry = ManifestEntry(path="x", doc_id="d", format="md")
        assert entry.checksum == ""

    def test_create_with_all_fields(self):
        entry = ManifestEntry(
            path="out/a.pdf", doc_id="d1", format="pdf", size_bytes=1024, checksum="abc"
        )
        assert entry.size_bytes == 1024
        assert entry.checksum == "abc"

    def test_equality(self):
        e1 = ManifestEntry(path="a", doc_id="d", format="pdf")
        e2 = ManifestEntry(path="a", doc_id="d", format="pdf")
        assert e1 == e2

    def test_inequality(self):
        e1 = ManifestEntry(path="a", doc_id="d", format="pdf")
        e2 = ManifestEntry(path="b", doc_id="d", format="pdf")
        assert e1 != e2


class TestExportManifestDataclass:
    def test_create_with_required_fields(self):
        m = ExportManifest(manifest_id="abc")
        assert m.manifest_id == "abc"

    def test_default_created_at_zero(self):
        m = ExportManifest(manifest_id="abc")
        assert m.created_at == 0.0

    def test_default_description_empty(self):
        m = ExportManifest(manifest_id="abc")
        assert m.description == ""

    def test_default_entries_empty_list(self):
        m = ExportManifest(manifest_id="abc")
        assert m.entries == []

    def test_default_entries_independent(self):
        m1 = ExportManifest(manifest_id="a")
        m2 = ExportManifest(manifest_id="b")
        m1.entries.append(ManifestEntry(path="p", doc_id="d", format="f"))
        assert m2.entries == []

    def test_create_with_all_fields(self):
        e = ManifestEntry(path="p", doc_id="d", format="f")
        m = ExportManifest(
            manifest_id="x", created_at=1.5, description="run", entries=[e]
        )
        assert m.created_at == 1.5
        assert m.description == "run"
        assert m.entries == [e]


class TestManifestStatsDataclass:
    def test_create(self):
        s = ManifestStats(
            total_manifests=1, total_entries=2, total_size_bytes=3, unique_docs=4
        )
        assert s.total_manifests == 1
        assert s.total_entries == 2
        assert s.total_size_bytes == 3
        assert s.unique_docs == 4

    def test_equality(self):
        a = ManifestStats(
            total_manifests=0, total_entries=0, total_size_bytes=0, unique_docs=0
        )
        b = ManifestStats(
            total_manifests=0, total_entries=0, total_size_bytes=0, unique_docs=0
        )
        assert a == b


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_on_init(self):
        mgr = DocExportManifest()
        assert mgr.list_manifests() == []

    def test_independent_instances(self):
        m1 = DocExportManifest()
        m2 = DocExportManifest()
        m1.create_manifest()
        assert m2.list_manifests() == []


# ---------------------------------------------------------------------------
# create_manifest
# ---------------------------------------------------------------------------


class TestCreateManifest:
    def test_returns_export_manifest(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert isinstance(m, ExportManifest)

    def test_manifest_id_is_uuid(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        import uuid as _uuid

        # Should not raise
        _uuid.UUID(m.manifest_id)

    def test_different_manifest_ids(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        assert m1.manifest_id != m2.manifest_id

    def test_empty_entries(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert m.entries == []

    def test_description_stored(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest(description="nightly build")
        assert m.description == "nightly build"

    def test_now_used_when_provided(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest(now=1234.5)
        assert m.created_at == 1234.5

    def test_now_default_is_current_time(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert m.created_at > 0.0


# ---------------------------------------------------------------------------
# add_entry
# ---------------------------------------------------------------------------


class TestAddEntry:
    def test_appends_entry(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        e = ManifestEntry(path="p", doc_id="d", format="pdf")
        assert mgr.add_entry(m.manifest_id, e) is True
        assert mgr.get_manifest(m.manifest_id).entries == [e]

    def test_returns_true_when_found(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        e = ManifestEntry(path="p", doc_id="d", format="f")
        assert mgr.add_entry(m.manifest_id, e) is True

    def test_returns_false_when_missing(self):
        mgr = DocExportManifest()
        e = ManifestEntry(path="p", doc_id="d", format="f")
        assert mgr.add_entry("nonexistent", e) is False

    def test_preserves_order(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        e1 = ManifestEntry(path="a", doc_id="d", format="f")
        e2 = ManifestEntry(path="b", doc_id="d", format="f")
        e3 = ManifestEntry(path="c", doc_id="d", format="f")
        mgr.add_entry(m.manifest_id, e1)
        mgr.add_entry(m.manifest_id, e2)
        mgr.add_entry(m.manifest_id, e3)
        paths = [e.path for e in mgr.get_manifest(m.manifest_id).entries]
        assert paths == ["a", "b", "c"]


# ---------------------------------------------------------------------------
# remove_entry
# ---------------------------------------------------------------------------


class TestRemoveEntry:
    def test_removes_existing(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="p", doc_id="d", format="f"))
        assert mgr.remove_entry(m.manifest_id, "p") is True
        assert mgr.get_manifest(m.manifest_id).entries == []

    def test_returns_false_when_entry_missing(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert mgr.remove_entry(m.manifest_id, "nope") is False

    def test_returns_false_when_manifest_missing(self):
        mgr = DocExportManifest()
        assert mgr.remove_entry("nonexistent", "p") is False

    def test_removes_only_matching_path(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="a", doc_id="d", format="f"))
        mgr.add_entry(m.manifest_id, ManifestEntry(path="b", doc_id="d", format="f"))
        mgr.remove_entry(m.manifest_id, "a")
        remaining = [e.path for e in mgr.get_manifest(m.manifest_id).entries]
        assert remaining == ["b"]


# ---------------------------------------------------------------------------
# get_manifest
# ---------------------------------------------------------------------------


class TestGetManifest:
    def test_found(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert mgr.get_manifest(m.manifest_id) is m

    def test_not_found_returns_none(self):
        mgr = DocExportManifest()
        assert mgr.get_manifest("nonexistent") is None


# ---------------------------------------------------------------------------
# delete_manifest
# ---------------------------------------------------------------------------


class TestDeleteManifest:
    def test_deletes_existing(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert mgr.delete_manifest(m.manifest_id) is True
        assert mgr.get_manifest(m.manifest_id) is None

    def test_returns_false_when_missing(self):
        mgr = DocExportManifest()
        assert mgr.delete_manifest("nonexistent") is False

    def test_does_not_affect_others(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.delete_manifest(m1.manifest_id)
        assert mgr.get_manifest(m2.manifest_id) is not None


# ---------------------------------------------------------------------------
# list_manifests
# ---------------------------------------------------------------------------


class TestListManifests:
    def test_empty_initially(self):
        assert DocExportManifest().list_manifests() == []

    def test_sorted_by_created_at(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest(now=3.0)
        m2 = mgr.create_manifest(now=1.0)
        m3 = mgr.create_manifest(now=2.0)
        ids = [m.manifest_id for m in mgr.list_manifests()]
        assert ids == [m2.manifest_id, m3.manifest_id, m1.manifest_id]

    def test_contains_all(self):
        mgr = DocExportManifest()
        a = mgr.create_manifest(now=1.0)
        b = mgr.create_manifest(now=2.0)
        assert {m.manifest_id for m in mgr.list_manifests()} == {
            a.manifest_id,
            b.manifest_id,
        }


# ---------------------------------------------------------------------------
# entries_for_doc
# ---------------------------------------------------------------------------


class TestEntriesForDoc:
    def test_empty_when_no_manifests(self):
        assert DocExportManifest().entries_for_doc("any") == []

    def test_returns_matching(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="a", doc_id="d1", format="f"))
        mgr.add_entry(m.manifest_id, ManifestEntry(path="b", doc_id="d2", format="f"))
        result = mgr.entries_for_doc("d1")
        assert len(result) == 1
        assert result[0].path == "a"

    def test_sorted_by_path(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="z", doc_id="d", format="f"))
        mgr.add_entry(m2.manifest_id, ManifestEntry(path="a", doc_id="d", format="f"))
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="m", doc_id="d", format="f"))
        result = mgr.entries_for_doc("d")
        assert [e.path for e in result] == ["a", "m", "z"]

    def test_cross_manifest(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="a", doc_id="d", format="f"))
        mgr.add_entry(m2.manifest_id, ManifestEntry(path="b", doc_id="d", format="f"))
        assert len(mgr.entries_for_doc("d")) == 2


# ---------------------------------------------------------------------------
# find_by_checksum
# ---------------------------------------------------------------------------


class TestFindByChecksum:
    def test_empty_when_no_match(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(
            m.manifest_id,
            ManifestEntry(path="a", doc_id="d", format="f", checksum="abc"),
        )
        assert mgr.find_by_checksum("xyz") == []

    def test_finds_match(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(
            m.manifest_id,
            ManifestEntry(path="a", doc_id="d", format="f", checksum="abc"),
        )
        result = mgr.find_by_checksum("abc")
        assert len(result) == 1
        assert result[0].path == "a"

    def test_cross_manifest(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(
            m1.manifest_id,
            ManifestEntry(path="a", doc_id="d1", format="f", checksum="dup"),
        )
        mgr.add_entry(
            m2.manifest_id,
            ManifestEntry(path="b", doc_id="d2", format="f", checksum="dup"),
        )
        assert len(mgr.find_by_checksum("dup")) == 2


# ---------------------------------------------------------------------------
# find_by_path
# ---------------------------------------------------------------------------


class TestFindByPath:
    def test_empty_when_no_match(self):
        assert DocExportManifest().find_by_path("p") == []

    def test_finds_exact(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="out/a", doc_id="d", format="f"))
        result = mgr.find_by_path("out/a")
        assert len(result) == 1

    def test_does_not_match_substring(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="out/a", doc_id="d", format="f"))
        assert mgr.find_by_path("out") == []

    def test_cross_manifest(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="same", doc_id="d1", format="f"))
        mgr.add_entry(m2.manifest_id, ManifestEntry(path="same", doc_id="d2", format="f"))
        assert len(mgr.find_by_path("same")) == 2


# ---------------------------------------------------------------------------
# total_size_of
# ---------------------------------------------------------------------------


class TestTotalSizeOf:
    def test_zero_for_missing(self):
        assert DocExportManifest().total_size_of("nope") == 0

    def test_zero_for_empty_manifest(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        assert mgr.total_size_of(m.manifest_id) == 0

    def test_sum_of_sizes(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(
            m.manifest_id, ManifestEntry(path="a", doc_id="d", format="f", size_bytes=100)
        )
        mgr.add_entry(
            m.manifest_id, ManifestEntry(path="b", doc_id="d", format="f", size_bytes=250)
        )
        assert mgr.total_size_of(m.manifest_id) == 350

    def test_scoped_to_manifest(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(
            m1.manifest_id, ManifestEntry(path="a", doc_id="d", format="f", size_bytes=10)
        )
        mgr.add_entry(
            m2.manifest_id, ManifestEntry(path="b", doc_id="d", format="f", size_bytes=20)
        )
        assert mgr.total_size_of(m1.manifest_id) == 10
        assert mgr.total_size_of(m2.manifest_id) == 20


# ---------------------------------------------------------------------------
# clear
# ---------------------------------------------------------------------------


class TestClear:
    def test_returns_zero_when_empty(self):
        assert DocExportManifest().clear() == 0

    def test_returns_count(self):
        mgr = DocExportManifest()
        mgr.create_manifest()
        mgr.create_manifest()
        mgr.create_manifest()
        assert mgr.clear() == 3

    def test_removes_all(self):
        mgr = DocExportManifest()
        mgr.create_manifest()
        mgr.create_manifest()
        mgr.clear()
        assert mgr.list_manifests() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self):
        s = DocExportManifest().stats()
        assert s == ManifestStats(
            total_manifests=0, total_entries=0, total_size_bytes=0, unique_docs=0
        )

    def test_counts_manifests(self):
        mgr = DocExportManifest()
        mgr.create_manifest()
        mgr.create_manifest()
        assert mgr.stats().total_manifests == 2

    def test_counts_entries(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(m.manifest_id, ManifestEntry(path="a", doc_id="d", format="f"))
        mgr.add_entry(m.manifest_id, ManifestEntry(path="b", doc_id="d", format="f"))
        assert mgr.stats().total_entries == 2

    def test_total_size(self):
        mgr = DocExportManifest()
        m = mgr.create_manifest()
        mgr.add_entry(
            m.manifest_id, ManifestEntry(path="a", doc_id="d", format="f", size_bytes=5)
        )
        mgr.add_entry(
            m.manifest_id, ManifestEntry(path="b", doc_id="d", format="f", size_bytes=7)
        )
        assert mgr.stats().total_size_bytes == 12

    def test_unique_docs(self):
        mgr = DocExportManifest()
        m1 = mgr.create_manifest()
        m2 = mgr.create_manifest()
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="a", doc_id="d1", format="f"))
        mgr.add_entry(m1.manifest_id, ManifestEntry(path="b", doc_id="d2", format="f"))
        mgr.add_entry(m2.manifest_id, ManifestEntry(path="c", doc_id="d1", format="f"))
        assert mgr.stats().unique_docs == 2


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_create_manifest(self):
        mgr = DocExportManifest()
        n_threads = 10
        per_thread = 20

        def worker():
            for _ in range(per_thread):
                mgr.create_manifest()

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(mgr.list_manifests()) == n_threads * per_thread

    def test_concurrent_create_unique_ids(self):
        mgr = DocExportManifest()

        def worker():
            for _ in range(15):
                mgr.create_manifest()

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        ids = {m.manifest_id for m in mgr.list_manifests()}
        assert len(ids) == 8 * 15
