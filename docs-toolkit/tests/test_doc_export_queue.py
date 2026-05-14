"""Tests for E346 DocExportQueue."""
from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_export_queue import DocExportQueue, ExportJob, ExportStats


# ---------------------------------------------------------------- dataclasses
class TestExportJobDataclass:
    def test_minimal_construction(self):
        job = ExportJob(job_id="abc", doc_id="d1", format="pdf")
        assert job.job_id == "abc"
        assert job.doc_id == "d1"
        assert job.format == "pdf"

    def test_defaults(self):
        job = ExportJob(job_id="x", doc_id="y", format="html")
        assert job.requested_by == ""
        assert job.requested_at == 0.0
        assert job.status == "queued"
        assert job.priority == 0
        assert job.started_at is None
        assert job.completed_at is None
        assert job.output_path == ""
        assert job.error == ""

    def test_full_construction(self):
        job = ExportJob(
            job_id="a",
            doc_id="b",
            format="markdown",
            requested_by="alice",
            requested_at=100.0,
            status="completed",
            priority=5,
            started_at=110.0,
            completed_at=120.0,
            output_path="/tmp/out.md",
            error="",
        )
        assert job.requested_by == "alice"
        assert job.priority == 5
        assert job.output_path == "/tmp/out.md"

    def test_equality(self):
        a = ExportJob(job_id="x", doc_id="d", format="pdf")
        b = ExportJob(job_id="x", doc_id="d", format="pdf")
        assert a == b


class TestExportStatsDataclass:
    def test_construction(self):
        s = ExportStats(
            total=5, queued=2, running=1, completed=1, failed=1, cancelled=0
        )
        assert s.total == 5
        assert s.queued == 2
        assert s.running == 1
        assert s.completed == 1
        assert s.failed == 1
        assert s.cancelled == 0

    def test_equality(self):
        a = ExportStats(total=0, queued=0, running=0, completed=0, failed=0, cancelled=0)
        b = ExportStats(total=0, queued=0, running=0, completed=0, failed=0, cancelled=0)
        assert a == b


# ---------------------------------------------------------------- construction
class TestConstruction:
    def test_empty(self):
        q = DocExportQueue()
        assert q.stats().total == 0

    def test_independent_instances(self):
        q1 = DocExportQueue()
        q2 = DocExportQueue()
        q1.enqueue("d1", "pdf")
        assert q2.stats().total == 0


# ---------------------------------------------------------------- enqueue
class TestEnqueue:
    def test_basic(self):
        q = DocExportQueue()
        job = q.enqueue("d1", "pdf")
        assert isinstance(job, ExportJob)
        assert job.doc_id == "d1"
        assert job.format == "pdf"
        assert job.status == "queued"

    def test_uuid_job_id(self):
        q = DocExportQueue()
        job = q.enqueue("d1", "pdf")
        # uuid4().hex is 32 hex chars
        assert len(job.job_id) == 32
        int(job.job_id, 16)  # must be hex

    def test_unique_job_ids(self):
        q = DocExportQueue()
        ids = {q.enqueue("d", "pdf").job_id for _ in range(20)}
        assert len(ids) == 20

    def test_timestamp_set(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf", now=12345.0)
        assert job.requested_at == 12345.0

    def test_auto_timestamp(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert job.requested_at > 0.0

    def test_status_queued(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert job.status == "queued"

    def test_requested_by(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf", requested_by="alice")
        assert job.requested_by == "alice"

    def test_priority(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf", priority=7)
        assert job.priority == 7

    def test_stored(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.get_job(job.job_id) is job or q.get_job(job.job_id) == job


# ---------------------------------------------------------------- start
class TestStartJob:
    def test_queued_to_running(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.start_job(job.job_id, now=10.0) is True
        again = q.get_job(job.job_id)
        assert again.status == "running"
        assert again.started_at == 10.0

    def test_auto_now(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.get_job(job.job_id).started_at is not None

    def test_unknown_id(self):
        q = DocExportQueue()
        assert q.start_job("nope") is False

    def test_already_running(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.start_job(job.job_id) is False

    def test_completed_cannot_start(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        q.complete_job(job.job_id)
        assert q.start_job(job.job_id) is False

    def test_cancelled_cannot_start(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.cancel_job(job.job_id)
        assert q.start_job(job.job_id) is False


# ---------------------------------------------------------------- complete
class TestCompleteJob:
    def test_running_to_completed(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.complete_job(job.job_id, output_path="/tmp/x.pdf", now=99.0) is True
        j = q.get_job(job.job_id)
        assert j.status == "completed"
        assert j.completed_at == 99.0
        assert j.output_path == "/tmp/x.pdf"

    def test_default_output_path(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.complete_job(job.job_id) is True
        assert q.get_job(job.job_id).output_path == ""

    def test_cannot_complete_queued(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.complete_job(job.job_id) is False

    def test_cannot_complete_unknown(self):
        q = DocExportQueue()
        assert q.complete_job("missing") is False

    def test_cannot_complete_twice(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        q.complete_job(job.job_id)
        assert q.complete_job(job.job_id) is False


# ---------------------------------------------------------------- fail
class TestFailJob:
    def test_running_to_failed(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.fail_job(job.job_id, error="boom", now=200.0) is True
        j = q.get_job(job.job_id)
        assert j.status == "failed"
        assert j.error == "boom"
        assert j.completed_at == 200.0

    def test_cannot_fail_queued(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.fail_job(job.job_id, error="x") is False

    def test_cannot_fail_unknown(self):
        q = DocExportQueue()
        assert q.fail_job("missing", error="x") is False

    def test_cannot_fail_completed(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        q.complete_job(job.job_id)
        assert q.fail_job(job.job_id, error="x") is False


# ---------------------------------------------------------------- cancel
class TestCancelJob:
    def test_queued_to_cancelled(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.cancel_job(job.job_id) is True
        assert q.get_job(job.job_id).status == "cancelled"

    def test_running_to_cancelled(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        assert q.cancel_job(job.job_id) is True
        assert q.get_job(job.job_id).status == "cancelled"

    def test_cannot_cancel_completed(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        q.complete_job(job.job_id)
        assert q.cancel_job(job.job_id) is False

    def test_cannot_cancel_failed(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.start_job(job.job_id)
        q.fail_job(job.job_id, error="x")
        assert q.cancel_job(job.job_id) is False

    def test_cannot_cancel_unknown(self):
        q = DocExportQueue()
        assert q.cancel_job("nope") is False

    def test_cannot_cancel_twice(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.cancel_job(job.job_id)
        assert q.cancel_job(job.job_id) is False


# ---------------------------------------------------------------- get
class TestGetJob:
    def test_found(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.get_job(job.job_id) is not None

    def test_not_found(self):
        q = DocExportQueue()
        assert q.get_job("nope") is None


# ---------------------------------------------------------------- next_queued
class TestNextQueued:
    def test_empty(self):
        q = DocExportQueue()
        assert q.next_queued() is None

    def test_highest_priority(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", priority=1, now=1.0)
        high = q.enqueue("d2", "pdf", priority=10, now=2.0)
        q.enqueue("d3", "pdf", priority=5, now=3.0)
        assert q.next_queued().job_id == high.job_id

    def test_tie_by_requested_at(self):
        q = DocExportQueue()
        first = q.enqueue("d1", "pdf", priority=5, now=1.0)
        q.enqueue("d2", "pdf", priority=5, now=2.0)
        assert q.next_queued().job_id == first.job_id

    def test_does_not_change_state(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.next_queued()
        assert q.get_job(job.job_id).status == "queued"

    def test_skips_non_queued(self):
        q = DocExportQueue()
        j1 = q.enqueue("d1", "pdf", priority=10)
        q.start_job(j1.job_id)
        j2 = q.enqueue("d2", "pdf", priority=1)
        assert q.next_queued().job_id == j2.job_id

    def test_all_non_queued(self):
        q = DocExportQueue()
        j = q.enqueue("d", "pdf")
        q.cancel_job(j.job_id)
        assert q.next_queued() is None


# ---------------------------------------------------------------- queued_jobs
class TestQueuedJobs:
    def test_empty(self):
        q = DocExportQueue()
        assert q.queued_jobs() == []

    def test_sorted_priority_desc(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", priority=1, now=1.0)
        q.enqueue("d2", "pdf", priority=5, now=2.0)
        q.enqueue("d3", "pdf", priority=3, now=3.0)
        result = q.queued_jobs()
        assert [j.priority for j in result] == [5, 3, 1]

    def test_tiebreak_requested_at(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", priority=5, now=5.0)
        q.enqueue("d2", "pdf", priority=5, now=1.0)
        q.enqueue("d3", "pdf", priority=5, now=3.0)
        result = q.queued_jobs()
        assert [j.requested_at for j in result] == [1.0, 3.0, 5.0]

    def test_excludes_non_queued(self):
        q = DocExportQueue()
        j = q.enqueue("d", "pdf")
        q.start_job(j.job_id)
        assert q.queued_jobs() == []


# ---------------------------------------------------------------- by status
class TestJobsByStatus:
    def test_filter(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", now=1.0)
        j2 = q.enqueue("d2", "pdf", now=2.0)
        q.start_job(j2.job_id)
        assert len(q.jobs_by_status("queued")) == 1
        assert len(q.jobs_by_status("running")) == 1

    def test_sorted(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", now=3.0)
        q.enqueue("d2", "pdf", now=1.0)
        q.enqueue("d3", "pdf", now=2.0)
        result = q.jobs_by_status("queued")
        assert [j.requested_at for j in result] == [1.0, 2.0, 3.0]

    def test_unknown_status_returns_empty(self):
        q = DocExportQueue()
        q.enqueue("d", "pdf")
        assert q.jobs_by_status("zzz") == []


# ---------------------------------------------------------------- for doc
class TestJobsForDoc:
    def test_filter_by_doc_id(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", now=1.0)
        q.enqueue("d1", "html", now=2.0)
        q.enqueue("d2", "pdf", now=3.0)
        assert len(q.jobs_for_doc("d1")) == 2
        assert len(q.jobs_for_doc("d2")) == 1

    def test_sorted_by_requested_at(self):
        q = DocExportQueue()
        q.enqueue("d1", "pdf", now=3.0)
        q.enqueue("d1", "html", now=1.0)
        q.enqueue("d1", "md", now=2.0)
        result = q.jobs_for_doc("d1")
        assert [j.requested_at for j in result] == [1.0, 2.0, 3.0]

    def test_unknown_doc(self):
        q = DocExportQueue()
        assert q.jobs_for_doc("missing") == []


# ---------------------------------------------------------------- delete
class TestDeleteJob:
    def test_existing(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        assert q.delete_job(job.job_id) is True
        assert q.get_job(job.job_id) is None

    def test_missing(self):
        q = DocExportQueue()
        assert q.delete_job("nope") is False

    def test_decreases_total(self):
        q = DocExportQueue()
        job = q.enqueue("d", "pdf")
        q.delete_job(job.job_id)
        assert q.stats().total == 0


# ---------------------------------------------------------------- purge
class TestPurgeCompleted:
    def test_count(self):
        q = DocExportQueue()
        for i in range(3):
            j = q.enqueue(f"d{i}", "pdf")
            q.start_job(j.job_id)
            q.complete_job(j.job_id)
        assert q.purge_completed() == 3
        assert q.stats().total == 0

    def test_only_completed_and_failed(self):
        q = DocExportQueue()
        j1 = q.enqueue("d1", "pdf")
        q.start_job(j1.job_id)
        q.complete_job(j1.job_id)
        j2 = q.enqueue("d2", "pdf")
        q.start_job(j2.job_id)
        q.fail_job(j2.job_id, error="e")
        j3 = q.enqueue("d3", "pdf")
        j4 = q.enqueue("d4", "pdf")
        q.cancel_job(j4.job_id)
        removed = q.purge_completed()
        assert removed == 2
        # remaining: j3 (queued) and j4 (cancelled)
        assert q.stats().total == 2
        assert q.get_job(j3.job_id) is not None
        assert q.get_job(j4.job_id) is not None
        assert q.get_job(j1.job_id) is None
        assert q.get_job(j2.job_id) is None

    def test_empty(self):
        q = DocExportQueue()
        assert q.purge_completed() == 0


# ---------------------------------------------------------------- stats
class TestStats:
    def test_empty(self):
        q = DocExportQueue()
        s = q.stats()
        assert s == ExportStats(
            total=0, queued=0, running=0, completed=0, failed=0, cancelled=0
        )

    def test_counts_by_status(self):
        q = DocExportQueue()
        # 2 queued
        q.enqueue("d1", "pdf")
        q.enqueue("d2", "pdf")
        # 1 running
        jr = q.enqueue("d3", "pdf")
        q.start_job(jr.job_id)
        # 1 completed
        jc = q.enqueue("d4", "pdf")
        q.start_job(jc.job_id)
        q.complete_job(jc.job_id)
        # 1 failed
        jf = q.enqueue("d5", "pdf")
        q.start_job(jf.job_id)
        q.fail_job(jf.job_id, error="x")
        # 1 cancelled
        jcn = q.enqueue("d6", "pdf")
        q.cancel_job(jcn.job_id)

        s = q.stats()
        assert s.total == 6
        assert s.queued == 2
        assert s.running == 1
        assert s.completed == 1
        assert s.failed == 1
        assert s.cancelled == 1

    def test_returns_export_stats(self):
        q = DocExportQueue()
        assert isinstance(q.stats(), ExportStats)


# ---------------------------------------------------------------- threading
class TestThreadSafety:
    def test_concurrent_enqueue(self):
        q = DocExportQueue()
        n_threads = 8
        per_thread = 50

        def worker():
            for i in range(per_thread):
                q.enqueue(f"d{i}", "pdf")

        threads = [threading.Thread(target=worker) for _ in range(n_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert q.stats().total == n_threads * per_thread

    def test_concurrent_unique_ids(self):
        q = DocExportQueue()

        def worker():
            for _ in range(25):
                q.enqueue("d", "pdf")

        threads = [threading.Thread(target=worker) for _ in range(4)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        all_ids = {j.job_id for j in q.queued_jobs()}
        assert len(all_ids) == 100
