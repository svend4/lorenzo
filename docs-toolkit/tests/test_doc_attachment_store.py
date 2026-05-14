"""Tests for E324 DocAttachmentStore (docstoolkit.doc_attachment_store)."""
from __future__ import annotations

import threading
from dataclasses import fields

import pytest

from docstoolkit.doc_attachment_store import (
    Attachment,
    AttachmentStats,
    DocAttachmentStore,
)


# ---------------------------------------------------------------------------
# TestAttachmentDataclass
# ---------------------------------------------------------------------------


class TestAttachmentDataclass:
    def test_required_fields_present(self):
        names = {f.name for f in fields(Attachment)}
        assert {"attachment_id", "doc_id", "filename"} <= names

    def test_optional_defaults(self):
        att = Attachment(attachment_id="a", doc_id="d", filename="f.txt")
        assert att.mime_type == "application/octet-stream"
        assert att.size_bytes == 0
        assert att.uploaded_at == 0.0
        assert att.uploaded_by == ""
        assert att.checksum == ""
        assert att.metadata == {}

    def test_metadata_is_independent_per_instance(self):
        a1 = Attachment(attachment_id="x", doc_id="d", filename="f1")
        a2 = Attachment(attachment_id="y", doc_id="d", filename="f2")
        a1.metadata["k"] = "v"
        assert "k" not in a2.metadata

    def test_full_construction(self):
        att = Attachment(
            attachment_id="id1",
            doc_id="doc1",
            filename="report.pdf",
            mime_type="application/pdf",
            size_bytes=12345,
            uploaded_at=1_000.0,
            uploaded_by="alice",
            checksum="abc123",
            metadata={"env": "prod"},
        )
        assert att.attachment_id == "id1"
        assert att.doc_id == "doc1"
        assert att.filename == "report.pdf"
        assert att.mime_type == "application/pdf"
        assert att.size_bytes == 12345
        assert att.uploaded_at == 1_000.0
        assert att.uploaded_by == "alice"
        assert att.checksum == "abc123"
        assert att.metadata == {"env": "prod"}


# ---------------------------------------------------------------------------
# TestAttachmentStatsDataclass
# ---------------------------------------------------------------------------


class TestAttachmentStatsDataclass:
    def test_required_fields_present(self):
        names = {f.name for f in fields(AttachmentStats)}
        assert {
            "total_attachments",
            "unique_docs",
            "total_size_bytes",
            "mime_type_counts",
        } <= names

    def test_construction(self):
        st = AttachmentStats(
            total_attachments=3,
            unique_docs=2,
            total_size_bytes=100,
            mime_type_counts={"text/plain": 2, "image/png": 1},
        )
        assert st.total_attachments == 3
        assert st.unique_docs == 2
        assert st.total_size_bytes == 100
        assert st.mime_type_counts == {"text/plain": 2, "image/png": 1}

    def test_mime_type_counts_default_factory(self):
        st = AttachmentStats(
            total_attachments=0, unique_docs=0, total_size_bytes=0
        )
        assert st.mime_type_counts == {}

    def test_mime_type_counts_independent(self):
        s1 = AttachmentStats(total_attachments=0, unique_docs=0, total_size_bytes=0)
        s2 = AttachmentStats(total_attachments=0, unique_docs=0, total_size_bytes=0)
        s1.mime_type_counts["x"] = 1
        assert "x" not in s2.mime_type_counts


# ---------------------------------------------------------------------------
# TestConstruction
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_store_creation(self):
        store = DocAttachmentStore()
        assert store.all_doc_ids() == []

    def test_empty_store_stats(self):
        store = DocAttachmentStore()
        st = store.stats()
        assert st.total_attachments == 0
        assert st.unique_docs == 0
        assert st.total_size_bytes == 0
        assert st.mime_type_counts == {}

    def test_independent_instances(self):
        s1 = DocAttachmentStore()
        s2 = DocAttachmentStore()
        s1.attach("d1", "f.txt")
        assert s2.stats().total_attachments == 0


# ---------------------------------------------------------------------------
# TestAttach
# ---------------------------------------------------------------------------


class TestAttach:
    def test_attach_returns_attachment(self):
        store = DocAttachmentStore()
        att = store.attach("doc1", "a.txt")
        assert isinstance(att, Attachment)

    def test_attach_assigns_uuid(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt")
        a2 = store.attach("d1", "b.txt")
        assert a1.attachment_id != a2.attachment_id
        assert len(a1.attachment_id) >= 32

    def test_attach_uses_now_param(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt", now=12345.0)
        assert att.uploaded_at == 12345.0

    def test_attach_default_timestamp_is_set(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        assert att.uploaded_at > 0.0

    def test_attach_stores_all_fields(self):
        store = DocAttachmentStore()
        att = store.attach(
            "doc1",
            "report.pdf",
            mime_type="application/pdf",
            size_bytes=999,
            uploaded_by="bob",
            checksum="hash123",
            metadata={"src": "upload"},
            now=42.0,
        )
        assert att.doc_id == "doc1"
        assert att.filename == "report.pdf"
        assert att.mime_type == "application/pdf"
        assert att.size_bytes == 999
        assert att.uploaded_by == "bob"
        assert att.checksum == "hash123"
        assert att.metadata == {"src": "upload"}
        assert att.uploaded_at == 42.0

    def test_attach_default_mime_type(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.bin")
        assert att.mime_type == "application/octet-stream"

    def test_attach_metadata_none_creates_empty_dict(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt", metadata=None)
        assert att.metadata == {}

    def test_attach_metadata_is_copied(self):
        store = DocAttachmentStore()
        meta = {"k": "v"}
        att = store.attach("d1", "a.txt", metadata=meta)
        meta["k"] = "changed"
        assert att.metadata == {"k": "v"}

    def test_attach_persists_in_store(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        assert store.get(att.attachment_id) is att

    def test_attach_appears_in_doc_listing(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        listed = store.attachments_for_doc("d1")
        assert len(listed) == 1
        assert listed[0].attachment_id == att.attachment_id


# ---------------------------------------------------------------------------
# TestDetach
# ---------------------------------------------------------------------------


class TestDetach:
    def test_detach_existing_returns_true(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        assert store.detach(att.attachment_id) is True

    def test_detach_unknown_returns_false(self):
        store = DocAttachmentStore()
        assert store.detach("nope") is False

    def test_detach_removes_from_get(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        store.detach(att.attachment_id)
        assert store.get(att.attachment_id) is None

    def test_detach_removes_from_doc_listing(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt")
        a2 = store.attach("d1", "b.txt")
        store.detach(a1.attachment_id)
        listed = store.attachments_for_doc("d1")
        assert len(listed) == 1
        assert listed[0].attachment_id == a2.attachment_id

    def test_detach_last_attachment_removes_doc(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        store.detach(att.attachment_id)
        assert "d1" not in store.all_doc_ids()

    def test_detach_twice_second_returns_false(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        assert store.detach(att.attachment_id) is True
        assert store.detach(att.attachment_id) is False


# ---------------------------------------------------------------------------
# TestDetachAll
# ---------------------------------------------------------------------------


class TestDetachAll:
    def test_detach_all_returns_count(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        store.attach("d1", "b.txt")
        store.attach("d1", "c.txt")
        assert store.detach_all("d1") == 3

    def test_detach_all_empty_doc_returns_zero(self):
        store = DocAttachmentStore()
        assert store.detach_all("missing") == 0

    def test_detach_all_removes_attachments(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt")
        a2 = store.attach("d1", "b.txt")
        store.detach_all("d1")
        assert store.get(a1.attachment_id) is None
        assert store.get(a2.attachment_id) is None

    def test_detach_all_does_not_affect_other_docs(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        a2 = store.attach("d2", "b.txt")
        store.detach_all("d1")
        assert store.get(a2.attachment_id) is not None

    def test_detach_all_removes_doc_from_list(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        store.detach_all("d1")
        assert "d1" not in store.all_doc_ids()


# ---------------------------------------------------------------------------
# TestGet
# ---------------------------------------------------------------------------


class TestGet:
    def test_get_found(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        result = store.get(att.attachment_id)
        assert result is not None
        assert result.attachment_id == att.attachment_id

    def test_get_not_found(self):
        store = DocAttachmentStore()
        assert store.get("nope") is None

    def test_get_after_detach(self):
        store = DocAttachmentStore()
        att = store.attach("d1", "a.txt")
        store.detach(att.attachment_id)
        assert store.get(att.attachment_id) is None


# ---------------------------------------------------------------------------
# TestAttachmentsForDoc
# ---------------------------------------------------------------------------


class TestAttachmentsForDoc:
    def test_empty_doc_returns_empty(self):
        store = DocAttachmentStore()
        assert store.attachments_for_doc("missing") == []

    def test_insertion_order_preserved(self):
        store = DocAttachmentStore()
        a = store.attach("d1", "a.txt", now=1.0)
        b = store.attach("d1", "b.txt", now=2.0)
        c = store.attach("d1", "c.txt", now=3.0)
        result = store.attachments_for_doc("d1")
        assert [x.attachment_id for x in result] == [
            a.attachment_id,
            b.attachment_id,
            c.attachment_id,
        ]

    def test_only_returns_matching_doc(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        store.attach("d2", "b.txt")
        result = store.attachments_for_doc("d1")
        assert len(result) == 1
        assert result[0].doc_id == "d1"

    def test_returns_independent_list(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        result = store.attachments_for_doc("d1")
        result.clear()
        assert len(store.attachments_for_doc("d1")) == 1


# ---------------------------------------------------------------------------
# TestFindByFilename
# ---------------------------------------------------------------------------


class TestFindByFilename:
    def test_exact_match(self):
        store = DocAttachmentStore()
        store.attach("d1", "report.pdf")
        store.attach("d1", "other.pdf")
        result = store.find_by_filename("d1", "report.pdf")
        assert len(result) == 1
        assert result[0].filename == "report.pdf"

    def test_no_match_returns_empty(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        assert store.find_by_filename("d1", "missing.txt") == []

    def test_scoped_to_doc(self):
        store = DocAttachmentStore()
        store.attach("d1", "report.pdf")
        store.attach("d2", "report.pdf")
        result = store.find_by_filename("d1", "report.pdf")
        assert len(result) == 1
        assert result[0].doc_id == "d1"

    def test_sorted_by_uploaded_at(self):
        store = DocAttachmentStore()
        a3 = store.attach("d1", "x.txt", now=300.0)
        a1 = store.attach("d1", "x.txt", now=100.0)
        a2 = store.attach("d1", "x.txt", now=200.0)
        result = store.find_by_filename("d1", "x.txt")
        assert [r.attachment_id for r in result] == [
            a1.attachment_id,
            a2.attachment_id,
            a3.attachment_id,
        ]

    def test_unknown_doc_returns_empty(self):
        store = DocAttachmentStore()
        assert store.find_by_filename("missing", "a.txt") == []

    def test_case_sensitive(self):
        store = DocAttachmentStore()
        store.attach("d1", "Report.pdf")
        assert store.find_by_filename("d1", "report.pdf") == []


# ---------------------------------------------------------------------------
# TestFindByChecksum
# ---------------------------------------------------------------------------


class TestFindByChecksum:
    def test_cross_doc_match(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt", checksum="abc")
        a2 = store.attach("d2", "b.txt", checksum="abc")
        result = store.find_by_checksum("abc")
        ids = {r.attachment_id for r in result}
        assert ids == {a1.attachment_id, a2.attachment_id}

    def test_no_match(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt", checksum="abc")
        assert store.find_by_checksum("xyz") == []

    def test_sorted_by_uploaded_at(self):
        store = DocAttachmentStore()
        a3 = store.attach("d1", "a.txt", checksum="h", now=300.0)
        a1 = store.attach("d2", "b.txt", checksum="h", now=100.0)
        a2 = store.attach("d3", "c.txt", checksum="h", now=200.0)
        result = store.find_by_checksum("h")
        assert [r.attachment_id for r in result] == [
            a1.attachment_id,
            a2.attachment_id,
            a3.attachment_id,
        ]

    def test_empty_string_checksum_matches_defaults(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt")
        result = store.find_by_checksum("")
        assert len(result) == 1
        assert result[0].attachment_id == a1.attachment_id


# ---------------------------------------------------------------------------
# TestTotalSizeForDoc
# ---------------------------------------------------------------------------


class TestTotalSizeForDoc:
    def test_sum_of_sizes(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt", size_bytes=10)
        store.attach("d1", "b.txt", size_bytes=25)
        store.attach("d1", "c.txt", size_bytes=5)
        assert store.total_size_for_doc("d1") == 40

    def test_empty_doc_returns_zero(self):
        store = DocAttachmentStore()
        assert store.total_size_for_doc("missing") == 0

    def test_scoped_to_doc(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt", size_bytes=10)
        store.attach("d2", "b.txt", size_bytes=999)
        assert store.total_size_for_doc("d1") == 10

    def test_after_detach(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a.txt", size_bytes=10)
        store.attach("d1", "b.txt", size_bytes=20)
        store.detach(a1.attachment_id)
        assert store.total_size_for_doc("d1") == 20


# ---------------------------------------------------------------------------
# TestAllDocIds
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self):
        store = DocAttachmentStore()
        assert store.all_doc_ids() == []

    def test_unique_and_sorted(self):
        store = DocAttachmentStore()
        store.attach("zebra", "a.txt")
        store.attach("apple", "b.txt")
        store.attach("mango", "c.txt")
        store.attach("apple", "d.txt")
        assert store.all_doc_ids() == ["apple", "mango", "zebra"]

    def test_removed_doc_disappears(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt")
        store.detach_all("d1")
        assert store.all_doc_ids() == []


# ---------------------------------------------------------------------------
# TestLargestAttachments
# ---------------------------------------------------------------------------


class TestLargestAttachments:
    def test_sorted_by_size_desc(self):
        store = DocAttachmentStore()
        store.attach("d1", "small", size_bytes=10)
        store.attach("d1", "big", size_bytes=1000)
        store.attach("d1", "mid", size_bytes=100)
        result = store.largest_attachments()
        assert [a.size_bytes for a in result] == [1000, 100, 10]

    def test_limit_param(self):
        store = DocAttachmentStore()
        for i in range(10):
            store.attach("d1", f"f{i}", size_bytes=i)
        result = store.largest_attachments(limit=3)
        assert len(result) == 3
        assert [a.size_bytes for a in result] == [9, 8, 7]

    def test_default_limit_is_10(self):
        store = DocAttachmentStore()
        for i in range(15):
            store.attach("d1", f"f{i}", size_bytes=i)
        result = store.largest_attachments()
        assert len(result) == 10

    def test_empty_store(self):
        store = DocAttachmentStore()
        assert store.largest_attachments() == []

    def test_tie_break_by_attachment_id_asc(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a", size_bytes=100)
        a2 = store.attach("d1", "b", size_bytes=100)
        a3 = store.attach("d1", "c", size_bytes=100)
        result = store.largest_attachments()
        expected_order = sorted([a1.attachment_id, a2.attachment_id, a3.attachment_id])
        assert [a.attachment_id for a in result] == expected_order

    def test_limit_zero(self):
        store = DocAttachmentStore()
        store.attach("d1", "a", size_bytes=10)
        assert store.largest_attachments(limit=0) == []


# ---------------------------------------------------------------------------
# TestStats
# ---------------------------------------------------------------------------


class TestStats:
    def test_totals(self):
        store = DocAttachmentStore()
        store.attach("d1", "a", size_bytes=10)
        store.attach("d1", "b", size_bytes=20)
        store.attach("d2", "c", size_bytes=30)
        st = store.stats()
        assert st.total_attachments == 3
        assert st.unique_docs == 2
        assert st.total_size_bytes == 60

    def test_mime_type_counts(self):
        store = DocAttachmentStore()
        store.attach("d1", "a.txt", mime_type="text/plain")
        store.attach("d1", "b.txt", mime_type="text/plain")
        store.attach("d2", "c.png", mime_type="image/png")
        st = store.stats()
        assert st.mime_type_counts == {"text/plain": 2, "image/png": 1}

    def test_empty(self):
        store = DocAttachmentStore()
        st = store.stats()
        assert st.total_attachments == 0
        assert st.unique_docs == 0
        assert st.total_size_bytes == 0
        assert st.mime_type_counts == {}

    def test_stats_after_detach(self):
        store = DocAttachmentStore()
        a1 = store.attach("d1", "a", size_bytes=10, mime_type="text/plain")
        store.attach("d1", "b", size_bytes=20, mime_type="text/plain")
        store.detach(a1.attachment_id)
        st = store.stats()
        assert st.total_attachments == 1
        assert st.total_size_bytes == 20
        assert st.mime_type_counts == {"text/plain": 1}

    def test_stats_returns_attachment_stats_type(self):
        store = DocAttachmentStore()
        assert isinstance(store.stats(), AttachmentStats)


# ---------------------------------------------------------------------------
# TestThreadSafety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_attach_to_same_doc(self):
        store = DocAttachmentStore()
        n_threads = 20
        per_thread = 25

        def worker(idx: int) -> None:
            for j in range(per_thread):
                store.attach("d1", f"t{idx}_f{j}", size_bytes=1)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        st = store.stats()
        assert st.total_attachments == n_threads * per_thread
        assert st.total_size_bytes == n_threads * per_thread
        assert len(store.attachments_for_doc("d1")) == n_threads * per_thread

    def test_concurrent_attach_different_docs(self):
        store = DocAttachmentStore()
        n_threads = 10

        def worker(idx: int) -> None:
            for j in range(10):
                store.attach(f"d{idx}", f"f{j}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert store.stats().total_attachments == n_threads * 10
        assert len(store.all_doc_ids()) == n_threads

    def test_concurrent_attach_and_detach(self):
        store = DocAttachmentStore()
        attach_ids = []
        lock = threading.Lock()

        def attacher() -> None:
            for _ in range(50):
                att = store.attach("d1", "f.txt", size_bytes=1)
                with lock:
                    attach_ids.append(att.attachment_id)

        def detacher() -> None:
            for _ in range(200):
                with lock:
                    aid = attach_ids.pop() if attach_ids else None
                if aid:
                    store.detach(aid)

        threads = [
            threading.Thread(target=attacher),
            threading.Thread(target=attacher),
            threading.Thread(target=detacher),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # Clean up remaining
        st = store.stats()
        # The store should remain self-consistent
        assert st.total_attachments == len(store.attachments_for_doc("d1"))

    def test_unique_attachment_ids_under_concurrency(self):
        store = DocAttachmentStore()

        def worker() -> None:
            for _ in range(50):
                store.attach("d1", "f")

        threads = [threading.Thread(target=worker) for _ in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        ids = [a.attachment_id for a in store.attachments_for_doc("d1")]
        assert len(ids) == len(set(ids))
