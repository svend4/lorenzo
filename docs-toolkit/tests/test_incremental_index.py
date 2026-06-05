"""Tests for the incremental_index module (E32)."""
from __future__ import annotations

import time

import pytest

from docstoolkit.incremental_index import (
    ChangeDetector,
    ChangeType,
    DocumentChange,
    IndexConfig,
    IndexJob,
    IndexQueue,
    IndexStats,
    IncrementalIndexer,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_queue() -> IndexQueue:
    return IndexQueue()  # :memory: by default


def make_detector() -> ChangeDetector:
    return ChangeDetector()


# ===========================================================================
# ChangeType
# ===========================================================================

class TestChangeType:
    def test_members_exist(self):
        assert ChangeType.ADDED
        assert ChangeType.MODIFIED
        assert ChangeType.DELETED
        assert ChangeType.UNCHANGED

    def test_values(self):
        assert ChangeType.ADDED.value == "added"
        assert ChangeType.MODIFIED.value == "modified"
        assert ChangeType.DELETED.value == "deleted"
        assert ChangeType.UNCHANGED.value == "unchanged"


# ===========================================================================
# DocumentChange
# ===========================================================================

class TestDocumentChange:
    def test_fields_present(self):
        dc = DocumentChange(
            doc_id="d1",
            change_type=ChangeType.ADDED,
            content_hash="abc123",
        )
        assert dc.doc_id == "d1"
        assert dc.change_type == ChangeType.ADDED
        assert dc.content_hash == "abc123"
        assert dc.old_hash == ""
        assert isinstance(dc.detected_ts, float)

    def test_detected_ts_auto(self):
        before = time.time()
        dc = DocumentChange(doc_id="x", change_type=ChangeType.ADDED, content_hash="h")
        after = time.time()
        assert before <= dc.detected_ts <= after

    def test_is_content_change_added(self):
        dc = DocumentChange(doc_id="x", change_type=ChangeType.ADDED, content_hash="h")
        assert dc.is_content_change() is True

    def test_is_content_change_modified(self):
        dc = DocumentChange(doc_id="x", change_type=ChangeType.MODIFIED, content_hash="h")
        assert dc.is_content_change() is True

    def test_is_content_change_deleted(self):
        dc = DocumentChange(doc_id="x", change_type=ChangeType.DELETED, content_hash="")
        assert dc.is_content_change() is False

    def test_is_content_change_unchanged(self):
        dc = DocumentChange(doc_id="x", change_type=ChangeType.UNCHANGED, content_hash="h")
        assert dc.is_content_change() is False

    def test_old_hash_populated(self):
        dc = DocumentChange(doc_id="x", change_type=ChangeType.MODIFIED, content_hash="new", old_hash="old")
        assert dc.old_hash == "old"


# ===========================================================================
# ChangeDetector
# ===========================================================================

class TestChangeDetectorAdded:
    def test_new_doc_is_added(self):
        det = make_detector()
        change = det.detect("doc1", "hello world")
        assert change.change_type == ChangeType.ADDED
        assert change.doc_id == "doc1"

    def test_added_hash_is_16_chars(self):
        det = make_detector()
        change = det.detect("doc1", "hello")
        assert len(change.content_hash) == 16

    def test_added_old_hash_is_empty(self):
        det = make_detector()
        change = det.detect("doc1", "hello")
        assert change.old_hash == ""

    def test_added_is_content_change(self):
        det = make_detector()
        change = det.detect("doc1", "hello")
        assert change.is_content_change() is True

    def test_added_registers_doc(self):
        det = make_detector()
        det.detect("doc1", "hello")
        assert "doc1" in det.known_docs()


class TestChangeDetectorUnchanged:
    def test_same_content_is_unchanged(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.detect("doc1", "hello")
        assert change.change_type == ChangeType.UNCHANGED

    def test_unchanged_content_hash_matches(self):
        det = make_detector()
        c1 = det.detect("doc1", "hello")
        c2 = det.detect("doc1", "hello")
        assert c1.content_hash == c2.content_hash

    def test_unchanged_old_hash_present(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.detect("doc1", "hello")
        assert change.old_hash != ""

    def test_unchanged_is_not_content_change(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.detect("doc1", "hello")
        assert change.is_content_change() is False


class TestChangeDetectorModified:
    def test_different_content_is_modified(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.detect("doc1", "world")
        assert change.change_type == ChangeType.MODIFIED

    def test_modified_old_hash_is_previous_hash(self):
        det = make_detector()
        c1 = det.detect("doc1", "hello")
        c2 = det.detect("doc1", "world")
        assert c2.old_hash == c1.content_hash

    def test_modified_new_hash_differs(self):
        det = make_detector()
        c1 = det.detect("doc1", "hello")
        c2 = det.detect("doc1", "world")
        assert c2.content_hash != c1.content_hash

    def test_modified_updates_registry(self):
        det = make_detector()
        det.detect("doc1", "hello")
        c2 = det.detect("doc1", "world")
        # Third call with same content should be UNCHANGED using the NEW hash
        c3 = det.detect("doc1", "world")
        assert c3.change_type == ChangeType.UNCHANGED
        assert c3.content_hash == c2.content_hash

    def test_modified_is_content_change(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.detect("doc1", "world")
        assert change.is_content_change() is True


class TestChangeDetectorDeleted:
    def test_mark_deleted_known_doc(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.mark_deleted("doc1")
        assert change is not None
        assert change.change_type == ChangeType.DELETED

    def test_mark_deleted_unknown_doc_returns_none(self):
        det = make_detector()
        result = det.mark_deleted("nonexistent")
        assert result is None

    def test_mark_deleted_removes_from_registry(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.mark_deleted("doc1")
        assert "doc1" not in det.known_docs()

    def test_mark_deleted_preserves_old_hash(self):
        det = make_detector()
        c1 = det.detect("doc1", "hello")
        c2 = det.mark_deleted("doc1")
        assert c2.old_hash == c1.content_hash

    def test_mark_deleted_content_hash_empty(self):
        det = make_detector()
        det.detect("doc1", "hello")
        change = det.mark_deleted("doc1")
        assert change.content_hash == ""

    def test_after_delete_re_add_is_added(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.mark_deleted("doc1")
        change = det.detect("doc1", "hello")
        assert change.change_type == ChangeType.ADDED


class TestChangeDetectorKnownDocs:
    def test_known_docs_empty_initially(self):
        det = make_detector()
        assert det.known_docs() == []

    def test_known_docs_after_detect(self):
        det = make_detector()
        det.detect("a", "content a")
        det.detect("b", "content b")
        known = det.known_docs()
        assert "a" in known
        assert "b" in known
        assert len(known) == 2

    def test_known_docs_after_delete(self):
        det = make_detector()
        det.detect("a", "x")
        det.detect("b", "y")
        det.mark_deleted("a")
        known = det.known_docs()
        assert "a" not in known
        assert "b" in known


class TestChangeDetectorReset:
    def test_reset_single_doc(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.detect("doc2", "world")
        det.reset("doc1")
        assert "doc1" not in det.known_docs()
        assert "doc2" in det.known_docs()

    def test_reset_single_unknown_is_noop(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.reset("unknown")  # should not raise
        assert "doc1" in det.known_docs()

    def test_reset_all(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.detect("doc2", "world")
        det.reset()
        assert det.known_docs() == []

    def test_reset_allows_re_add(self):
        det = make_detector()
        det.detect("doc1", "hello")
        det.reset("doc1")
        change = det.detect("doc1", "hello")
        assert change.change_type == ChangeType.ADDED


# ===========================================================================
# IndexJob
# ===========================================================================

class TestIndexJob:
    def test_fields(self):
        job = IndexJob(job_id="abcd1234", doc_id="d1", change_type=ChangeType.ADDED)
        assert job.job_id == "abcd1234"
        assert job.doc_id == "d1"
        assert job.change_type == ChangeType.ADDED
        assert job.priority == 5
        assert job.status == "pending"
        assert isinstance(job.created_ts, float)

    def test_custom_priority(self):
        job = IndexJob(job_id="x", doc_id="y", change_type=ChangeType.MODIFIED, priority=10)
        assert job.priority == 10

    def test_custom_status(self):
        job = IndexJob(job_id="x", doc_id="y", change_type=ChangeType.MODIFIED, status="done")
        assert job.status == "done"


# ===========================================================================
# IndexQueue
# ===========================================================================

class TestIndexQueueEnqueue:
    def test_enqueue_returns_job(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="hash")
        job = q.enqueue(change)
        assert isinstance(job, IndexJob)
        assert job.doc_id == "d1"
        assert job.change_type == ChangeType.ADDED
        assert job.status == "pending"

    def test_enqueue_job_id_is_8_chars(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change)
        assert len(job.job_id) == 8

    def test_enqueue_increments_pending(self):
        q = make_queue()
        assert q.pending_count() == 0
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        assert q.pending_count() == 1

    def test_enqueue_custom_priority(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change, priority=9)
        assert job.priority == 9


class TestIndexQueueDequeue:
    def test_dequeue_returns_jobs(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        jobs = q.dequeue(1)
        assert len(jobs) == 1
        assert jobs[0].doc_id == "d1"

    def test_dequeue_sets_running_status(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        jobs = q.dequeue(1)
        assert jobs[0].status == "running"

    def test_dequeue_reduces_pending(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        q.dequeue(1)
        assert q.pending_count() == 0

    def test_dequeue_priority_ordering(self):
        q = make_queue()
        c_low = DocumentChange(doc_id="low", change_type=ChangeType.ADDED, content_hash="h1")
        c_high = DocumentChange(doc_id="high", change_type=ChangeType.ADDED, content_hash="h2")
        q.enqueue(c_low, priority=1)
        q.enqueue(c_high, priority=10)
        jobs = q.dequeue(1)
        assert jobs[0].doc_id == "high"

    def test_dequeue_fifo_within_priority(self):
        q = make_queue()
        c1 = DocumentChange(doc_id="first", change_type=ChangeType.ADDED, content_hash="h1")
        c2 = DocumentChange(doc_id="second", change_type=ChangeType.ADDED, content_hash="h2")
        q.enqueue(c1, priority=5)
        q.enqueue(c2, priority=5)
        jobs = q.dequeue(2)
        assert jobs[0].doc_id == "first"
        assert jobs[1].doc_id == "second"

    def test_dequeue_n_greater_than_available(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        jobs = q.dequeue(100)
        assert len(jobs) == 1

    def test_dequeue_empty_queue_returns_empty_list(self):
        q = make_queue()
        jobs = q.dequeue(5)
        assert jobs == []

    def test_dequeue_does_not_return_running_jobs(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        q.dequeue(1)  # moves to running
        jobs2 = q.dequeue(1)
        assert jobs2 == []


class TestIndexQueueComplete:
    def test_complete_marks_done(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change)
        q.dequeue(1)
        q.complete(job.job_id)
        stats = q.stats()
        assert stats["done"] == 1

    def test_complete_reduces_running(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change)
        q.dequeue(1)
        q.complete(job.job_id)
        stats = q.stats()
        assert stats["running"] == 0


class TestIndexQueueFail:
    def test_fail_marks_failed(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change)
        q.dequeue(1)
        q.fail(job.job_id, "something went wrong")
        stats = q.stats()
        assert stats["failed"] == 1

    def test_fail_reduces_running(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        job = q.enqueue(change)
        q.dequeue(1)
        q.fail(job.job_id)
        stats = q.stats()
        assert stats["running"] == 0


class TestIndexQueueStats:
    def test_stats_initial_all_zero(self):
        q = make_queue()
        s = q.stats()
        assert s == {"pending": 0, "running": 0, "done": 0, "failed": 0}

    def test_stats_after_enqueue(self):
        q = make_queue()
        change = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h")
        q.enqueue(change)
        s = q.stats()
        assert s["pending"] == 1

    def test_stats_after_full_cycle(self):
        q = make_queue()
        c1 = DocumentChange(doc_id="d1", change_type=ChangeType.ADDED, content_hash="h1")
        c2 = DocumentChange(doc_id="d2", change_type=ChangeType.MODIFIED, content_hash="h2")
        c3 = DocumentChange(doc_id="d3", change_type=ChangeType.DELETED, content_hash="")
        j1 = q.enqueue(c1)
        j2 = q.enqueue(c2)
        j3 = q.enqueue(c3)
        q.dequeue(3)
        q.complete(j1.job_id)
        q.fail(j2.job_id, "err")
        # j3 stays running
        s = q.stats()
        assert s["done"] == 1
        assert s["failed"] == 1
        assert s["running"] == 1
        assert s["pending"] == 0

    def test_stats_keys_present(self):
        q = make_queue()
        s = q.stats()
        for key in ("pending", "running", "done", "failed"):
            assert key in s


# ===========================================================================
# IndexStats
# ===========================================================================

class TestIndexStats:
    def test_defaults_zero(self):
        s = IndexStats()
        assert s.added == 0
        assert s.modified == 0
        assert s.deleted == 0
        assert s.skipped == 0

    def test_total_processed_empty(self):
        s = IndexStats()
        assert s.total_processed() == 0

    def test_total_processed_counts_non_skipped(self):
        s = IndexStats(added=3, modified=2, deleted=1, skipped=5)
        assert s.total_processed() == 6  # 3 + 2 + 1

    def test_total_processed_excludes_skipped(self):
        s = IndexStats(added=0, modified=0, deleted=0, skipped=10)
        assert s.total_processed() == 0

    def test_total_processed_only_added(self):
        s = IndexStats(added=7)
        assert s.total_processed() == 7


# ===========================================================================
# IncrementalIndexer
# ===========================================================================

class TestIncrementalIndexerSubmit:
    def test_submit_new_doc_enqueues_job(self):
        indexer = IncrementalIndexer()
        change = indexer.submit("doc1", "hello world")
        assert change.change_type == ChangeType.ADDED
        assert indexer.pending_count() == 1

    def test_submit_unchanged_doc_no_job(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "hello")
        indexer.submit("doc1", "hello")  # second call, unchanged
        assert indexer.pending_count() == 1  # only the ADDED job

    def test_submit_modified_doc_enqueues_job(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "hello")
        indexer.queue.dequeue(1)  # drain the ADDED job
        indexer.submit("doc1", "world")
        assert indexer.pending_count() == 1

    def test_submit_returns_document_change(self):
        indexer = IncrementalIndexer()
        result = indexer.submit("doc1", "content")
        assert isinstance(result, DocumentChange)

    def test_submit_with_custom_priority(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content", priority=9)
        jobs = indexer.queue.dequeue(1)
        assert jobs[0].priority == 9


class TestIncrementalIndexerSubmitBatch:
    def test_submit_batch_returns_stats(self):
        indexer = IncrementalIndexer()
        docs = {"a": "content a", "b": "content b", "c": "content c"}
        stats = indexer.submit_batch(docs)
        assert isinstance(stats, IndexStats)

    def test_submit_batch_added_count(self):
        indexer = IncrementalIndexer()
        docs = {"a": "hello", "b": "world"}
        stats = indexer.submit_batch(docs)
        assert stats.added == 2

    def test_submit_batch_unchanged_count(self):
        indexer = IncrementalIndexer()
        docs = {"a": "hello", "b": "world"}
        indexer.submit_batch(docs)
        stats = indexer.submit_batch(docs)  # all unchanged
        assert stats.skipped == 2
        assert stats.added == 0

    def test_submit_batch_mixed(self):
        indexer = IncrementalIndexer()
        docs = {"a": "hello", "b": "world"}
        indexer.submit_batch(docs)
        docs2 = {"a": "hello", "b": "modified", "c": "new"}
        stats = indexer.submit_batch(docs2)
        assert stats.skipped == 1  # a unchanged
        assert stats.modified == 1  # b modified
        assert stats.added == 1    # c new

    def test_submit_batch_enqueues_content_changes(self):
        indexer = IncrementalIndexer()
        docs = {"a": "hello", "b": "world"}
        indexer.submit_batch(docs)
        assert indexer.pending_count() == 2


class TestIncrementalIndexerProcessBatch:
    def test_process_batch_no_handler(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        stats = indexer.process_batch()
        assert stats.total_processed() == 1
        assert indexer.pending_count() == 0

    def test_process_batch_marks_done_with_none_handler(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        indexer.process_batch(handler=lambda job: None)
        s = indexer.queue.stats()
        assert s["done"] == 1

    def test_process_batch_marks_done_with_true_handler(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        indexer.process_batch(handler=lambda job: True)
        s = indexer.queue.stats()
        assert s["done"] == 1

    def test_process_batch_marks_failed_with_false_handler(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        indexer.process_batch(handler=lambda job: False)
        s = indexer.queue.stats()
        assert s["failed"] == 1

    def test_process_batch_marks_failed_on_exception(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")

        def bad_handler(job):
            raise ValueError("something broke")

        indexer.process_batch(handler=bad_handler)
        s = indexer.queue.stats()
        assert s["failed"] == 1

    def test_process_batch_respects_batch_size(self):
        config = IndexConfig(batch_size=2)
        indexer = IncrementalIndexer(config=config)
        for i in range(5):
            indexer.submit(f"doc{i}", f"content {i}")
        stats = indexer.process_batch()
        assert stats.total_processed() == 2
        assert indexer.pending_count() == 3

    def test_process_batch_empty_queue_returns_empty_stats(self):
        indexer = IncrementalIndexer()
        stats = indexer.process_batch()
        assert stats.total_processed() == 0

    def test_process_batch_stats_categories(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "hello")  # ADDED
        det = indexer.detector
        # Force a known doc so we can submit modified
        indexer.submit("doc2", "world")  # ADDED
        indexer.queue.dequeue(2)  # drain pending
        indexer.submit("doc2", "changed")  # MODIFIED
        stats = indexer.process_batch()
        assert stats.modified == 1


class TestIncrementalIndexerPendingCount:
    def test_pending_count_zero_initially(self):
        indexer = IncrementalIndexer()
        assert indexer.pending_count() == 0

    def test_pending_count_after_submit(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        assert indexer.pending_count() == 1

    def test_pending_count_decreases_after_process(self):
        indexer = IncrementalIndexer()
        indexer.submit("doc1", "content")
        indexer.process_batch()
        assert indexer.pending_count() == 0


class TestIncrementalIndexerDefaults:
    def test_default_config_used(self):
        indexer = IncrementalIndexer()
        assert isinstance(indexer.config, IndexConfig)

    def test_default_queue_used(self):
        indexer = IncrementalIndexer()
        assert isinstance(indexer.queue, IndexQueue)

    def test_default_detector_used(self):
        indexer = IncrementalIndexer()
        assert isinstance(indexer.detector, ChangeDetector)

    def test_custom_components_accepted(self):
        config = IndexConfig(batch_size=3)
        queue = IndexQueue()
        detector = ChangeDetector()
        indexer = IncrementalIndexer(config=config, queue=queue, detector=detector)
        assert indexer.config is config
        assert indexer.queue is queue
        assert indexer.detector is detector


# ===========================================================================
# Integration: end-to-end workflow
# ===========================================================================

class TestEndToEnd:
    def test_full_lifecycle(self):
        """Add doc, process, modify, process, delete."""
        indexer = IncrementalIndexer()
        processed = []

        def handler(job: IndexJob):
            processed.append((job.doc_id, job.change_type))
            return True

        # Step 1: submit new doc
        indexer.submit("doc1", "initial content")
        assert indexer.pending_count() == 1

        # Step 2: process
        indexer.process_batch(handler=handler)
        assert indexer.pending_count() == 0
        assert processed[-1] == ("doc1", ChangeType.ADDED)

        # Step 3: same content — no new job
        indexer.submit("doc1", "initial content")
        assert indexer.pending_count() == 0

        # Step 4: modified content
        indexer.submit("doc1", "updated content")
        assert indexer.pending_count() == 1

        indexer.process_batch(handler=handler)
        assert processed[-1] == ("doc1", ChangeType.MODIFIED)

        # Step 5: mark deleted via detector, manually enqueue
        from docstoolkit.incremental_index.change import ChangeType as CT
        del_change = indexer.detector.mark_deleted("doc1")
        assert del_change is not None
        indexer.queue.enqueue(del_change)
        indexer.process_batch(handler=handler)
        assert processed[-1] == ("doc1", CT.DELETED)

    def test_batch_submit_and_process(self):
        indexer = IncrementalIndexer(config=IndexConfig(batch_size=5))
        docs = {f"doc{i}": f"content {i}" for i in range(10)}
        stats = indexer.submit_batch(docs)
        assert stats.added == 10
        assert indexer.pending_count() == 10

        s1 = indexer.process_batch()
        assert s1.total_processed() == 5
        assert indexer.pending_count() == 5

        s2 = indexer.process_batch()
        assert s2.total_processed() == 5
        assert indexer.pending_count() == 0
