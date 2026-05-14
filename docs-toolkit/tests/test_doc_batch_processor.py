"""Tests for docstoolkit.doc_batch_processor (E297).

Covers: BatchJob / BatchResult dataclasses, DocBatchProcessor.create_job,
run_job (success / failure / abort), job_progress, cancel_job, delete_job,
list_jobs, batch_size chunking, max_errors behaviour, and thread safety.
"""

from __future__ import annotations

import threading
import time
from typing import Any

import pytest

from docstoolkit.doc_batch_processor import BatchJob, BatchResult, DocBatchProcessor


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _identity(x: Any) -> Any:
    return x


def _double(x: int) -> int:
    return x * 2


def _always_raise(x: Any) -> None:
    raise ValueError(f"bad item: {x!r}")


def _raise_on(bad_values: set) -> Any:
    def fn(x):
        if x in bad_values:
            raise RuntimeError(f"blocked: {x!r}")
        return x
    return fn


# ---------------------------------------------------------------------------
# BatchJob dataclass
# ---------------------------------------------------------------------------

class TestBatchJobDataclass:
    def test_required_fields(self):
        job = BatchJob(job_id="j1", name="test", total_items=5)
        assert job.job_id == "j1"
        assert job.name == "test"
        assert job.total_items == 5

    def test_defaults(self):
        job = BatchJob(job_id="j1", name="n", total_items=0)
        assert job.processed == 0
        assert job.succeeded == 0
        assert job.failed == 0
        assert job.status == "pending"
        assert job.started_at == 0.0
        assert job.completed_at == 0.0
        assert job.errors == []

    def test_errors_list_is_independent(self):
        j1 = BatchJob(job_id="a", name="a", total_items=1)
        j2 = BatchJob(job_id="b", name="b", total_items=1)
        j1.errors.append("err")
        assert j2.errors == []

    def test_status_mutation(self):
        job = BatchJob(job_id="j", name="n", total_items=3)
        job.status = "running"
        assert job.status == "running"


# ---------------------------------------------------------------------------
# BatchResult dataclass
# ---------------------------------------------------------------------------

class TestBatchResultDataclass:
    def test_fields(self):
        r = BatchResult(
            job_id="j1", total=10, succeeded=8, failed=2,
            duration_ms=123.4, errors=["e1", "e2"],
        )
        assert r.job_id == "j1"
        assert r.total == 10
        assert r.succeeded == 8
        assert r.failed == 2
        assert r.duration_ms == pytest.approx(123.4)
        assert r.errors == ["e1", "e2"]

    def test_errors_default_empty(self):
        r = BatchResult(job_id="x", total=0, succeeded=0, failed=0,
                        duration_ms=0.0, errors=[])
        assert r.errors == []


# ---------------------------------------------------------------------------
# DocBatchProcessor construction
# ---------------------------------------------------------------------------

class TestConstruction:
    def test_defaults(self):
        proc = DocBatchProcessor()
        assert proc._batch_size == 10
        assert proc._max_errors == 0

    def test_custom_batch_size(self):
        proc = DocBatchProcessor(batch_size=3)
        assert proc._batch_size == 3

    def test_custom_max_errors(self):
        proc = DocBatchProcessor(max_errors=5)
        assert proc._max_errors == 5

    def test_invalid_batch_size_raises(self):
        with pytest.raises(ValueError):
            DocBatchProcessor(batch_size=0)

    def test_total_jobs_starts_at_zero(self):
        proc = DocBatchProcessor()
        assert proc.total_jobs == 0


# ---------------------------------------------------------------------------
# create_job
# ---------------------------------------------------------------------------

class TestCreateJob:
    def test_returns_batch_job(self):
        proc = DocBatchProcessor()
        job = proc.create_job("my-job", [1, 2, 3])
        assert isinstance(job, BatchJob)

    def test_status_is_pending(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [])
        assert job.status == "pending"

    def test_total_items_correct(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(7)))
        assert job.total_items == 7

    def test_job_id_is_uuid_string(self):
        import uuid
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        uuid.UUID(job.job_id)  # raises if not valid UUID

    def test_unique_job_ids(self):
        proc = DocBatchProcessor()
        ids = {proc.create_job("j", []).job_id for _ in range(20)}
        assert len(ids) == 20

    def test_name_stored(self):
        proc = DocBatchProcessor()
        job = proc.create_job("hello-world", [])
        assert job.name == "hello-world"

    def test_total_jobs_increments(self):
        proc = DocBatchProcessor()
        proc.create_job("a", [])
        proc.create_job("b", [])
        assert proc.total_jobs == 2

    def test_get_job_after_create(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1, 2])
        assert proc.get_job(job.job_id) is job

    def test_empty_items_list(self):
        proc = DocBatchProcessor()
        job = proc.create_job("empty", [])
        assert job.total_items == 0


# ---------------------------------------------------------------------------
# run_job — success paths
# ---------------------------------------------------------------------------

class TestRunJobSuccess:
    def test_returns_batch_result(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1, 2, 3])
        result = proc.run_job(job.job_id, _identity)
        assert isinstance(result, BatchResult)

    def test_all_succeeded(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(10)))
        result = proc.run_job(job.job_id, _double)
        assert result.succeeded == 10
        assert result.failed == 0

    def test_total_matches_items(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", ["a", "b", "c"])
        result = proc.run_job(job.job_id, _identity)
        assert result.total == 3

    def test_job_status_completed(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.run_job(job.job_id, _identity)
        assert job.status == "completed"

    def test_job_id_in_result(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        result = proc.run_job(job.job_id, _identity)
        assert result.job_id == job.job_id

    def test_empty_job_completes(self):
        proc = DocBatchProcessor()
        job = proc.create_job("empty", [])
        result = proc.run_job(job.job_id, _identity)
        assert result is not None
        assert result.succeeded == 0
        assert result.failed == 0
        assert job.status == "completed"

    def test_unknown_job_returns_none(self):
        proc = DocBatchProcessor()
        result = proc.run_job("does-not-exist", _identity)
        assert result is None

    def test_duration_ms_non_negative(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(5)))
        result = proc.run_job(job.job_id, _identity)
        assert result.duration_ms >= 0.0

    def test_now_parameter_used_for_timestamps(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        fixed = 1_000_000.0
        result = proc.run_job(job.job_id, _identity, now=fixed)
        assert job.started_at == fixed
        assert job.completed_at == fixed
        assert result.duration_ms == pytest.approx(0.0)

    def test_processed_counter_updated(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(5)))
        proc.run_job(job.job_id, _identity)
        assert job.processed == 5

    def test_no_errors_on_success(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1, 2])
        result = proc.run_job(job.job_id, _identity)
        assert result.errors == []
        assert job.errors == []


# ---------------------------------------------------------------------------
# run_job — failure / abort paths
# ---------------------------------------------------------------------------

class TestRunJobFailure:
    def test_all_fail_with_max_errors_zero(self):
        """max_errors=0 means abort on first error."""
        proc = DocBatchProcessor(max_errors=0)
        job = proc.create_job("j", [1, 2, 3])
        result = proc.run_job(job.job_id, _always_raise)
        # Only first item attempted before abort
        assert result.failed == 1
        assert job.status == "failed"

    def test_errors_list_populated(self):
        proc = DocBatchProcessor(max_errors=0)
        job = proc.create_job("j", ["x"])
        proc.run_job(job.job_id, _always_raise)
        assert len(job.errors) == 1
        assert "x" in job.errors[0]

    def test_status_failed_on_abort(self):
        proc = DocBatchProcessor(max_errors=0)
        job = proc.create_job("j", [1])
        proc.run_job(job.job_id, _always_raise)
        assert job.status == "failed"

    def test_max_errors_tolerance(self):
        """max_errors=2: allow 2 failures, abort on 3rd."""
        proc = DocBatchProcessor(batch_size=10, max_errors=2)
        # First 3 items fail, rest succeed
        job = proc.create_job("j", [1, 2, 3, 4, 5, 6])
        result = proc.run_job(job.job_id, _raise_on({1, 2, 3}))
        # Should abort after 3rd failure (failed > max_errors=2)
        assert result.failed == 3
        assert job.status == "failed"

    def test_max_errors_allows_partial_success(self):
        """With max_errors=3, up to 3 errors are tolerated."""
        proc = DocBatchProcessor(batch_size=10, max_errors=10)
        # All items fail — but max_errors=10 so they all run
        items = list(range(5))
        job = proc.create_job("j", items)
        result = proc.run_job(job.job_id, _always_raise)
        assert result.failed == 5
        # 5 failures, max_errors=10 → abort condition (5 > 10) is False → "completed"
        assert job.status == "completed"

    def test_max_errors_no_abort_when_within_tolerance(self):
        proc = DocBatchProcessor(batch_size=10, max_errors=10)
        items = list(range(5))
        job = proc.create_job("j", items)
        proc.run_job(job.job_id, _always_raise)
        # 5 failures, max_errors=10 → not aborted
        assert job.status == "completed"

    def test_mixed_success_and_failure(self):
        proc = DocBatchProcessor(batch_size=10, max_errors=5)
        items = list(range(6))
        job = proc.create_job("j", items)
        # items 1 and 3 fail
        result = proc.run_job(job.job_id, _raise_on({1, 3}))
        assert result.succeeded == 4
        assert result.failed == 2

    def test_error_message_captured(self):
        proc = DocBatchProcessor(max_errors=5)
        job = proc.create_job("j", ["item"])
        proc.run_job(job.job_id, _always_raise)
        assert any("item" in e for e in job.errors)

    def test_result_errors_match_job_errors(self):
        proc = DocBatchProcessor(max_errors=5)
        job = proc.create_job("j", [1, 2])
        result = proc.run_job(job.job_id, _always_raise)
        # At least as many errors in result as collected before possible abort
        assert len(result.errors) == result.failed


# ---------------------------------------------------------------------------
# batch_size chunking
# ---------------------------------------------------------------------------

class TestBatchSizeChunking:
    def test_single_batch(self):
        proc = DocBatchProcessor(batch_size=100)
        job = proc.create_job("j", list(range(5)))
        result = proc.run_job(job.job_id, _identity)
        assert result.succeeded == 5

    def test_exact_multiple(self):
        proc = DocBatchProcessor(batch_size=5)
        job = proc.create_job("j", list(range(10)))
        result = proc.run_job(job.job_id, _identity)
        assert result.succeeded == 10

    def test_non_exact_multiple(self):
        proc = DocBatchProcessor(batch_size=3)
        job = proc.create_job("j", list(range(7)))
        result = proc.run_job(job.job_id, _identity)
        assert result.succeeded == 7

    def test_batch_size_one(self):
        proc = DocBatchProcessor(batch_size=1)
        job = proc.create_job("j", list(range(4)))
        result = proc.run_job(job.job_id, _identity)
        assert result.succeeded == 4

    def test_abort_mid_batch(self):
        """Abort with max_errors=0 stops inside the first batch."""
        proc = DocBatchProcessor(batch_size=10, max_errors=0)
        items = [0, 1, "bad", 3, 4]  # "bad" raises
        job = proc.create_job("j", items)
        result = proc.run_job(job.job_id, lambda x: int(x))
        assert result.failed >= 1
        assert job.status == "failed"


# ---------------------------------------------------------------------------
# job_progress
# ---------------------------------------------------------------------------

class TestJobProgress:
    def test_pending_job_zero(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(10)))
        assert proc.job_progress(job.job_id) == pytest.approx(0.0)

    def test_not_found_returns_none(self):
        proc = DocBatchProcessor()
        assert proc.job_progress("nonexistent") is None

    def test_completed_job_progress(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(5)))
        proc.run_job(job.job_id, _identity)
        assert proc.job_progress(job.job_id) == pytest.approx(1.0)

    def test_empty_job_progress_is_zero(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [])
        assert proc.job_progress(job.job_id) == pytest.approx(0.0)

    def test_progress_between_zero_and_one(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", list(range(10)))
        proc.run_job(job.job_id, _identity)
        p = proc.job_progress(job.job_id)
        assert 0.0 <= p <= 1.0


# ---------------------------------------------------------------------------
# cancel_job
# ---------------------------------------------------------------------------

class TestCancelJob:
    def test_cancel_pending_returns_true(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1, 2])
        assert proc.cancel_job(job.job_id) is True

    def test_cancel_sets_status(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.cancel_job(job.job_id)
        assert job.status == "cancelled"

    def test_cancel_nonexistent_returns_false(self):
        proc = DocBatchProcessor()
        assert proc.cancel_job("nope") is False

    def test_cancel_completed_returns_false(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.run_job(job.job_id, _identity)
        assert proc.cancel_job(job.job_id) is False

    def test_cancel_failed_returns_false(self):
        proc = DocBatchProcessor(max_errors=0)
        job = proc.create_job("j", [1])
        proc.run_job(job.job_id, _always_raise)
        assert proc.cancel_job(job.job_id) is False

    def test_cancel_already_cancelled_returns_false(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.cancel_job(job.job_id)
        assert proc.cancel_job(job.job_id) is False


# ---------------------------------------------------------------------------
# delete_job
# ---------------------------------------------------------------------------

class TestDeleteJob:
    def test_delete_existing_returns_true(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        assert proc.delete_job(job.job_id) is True

    def test_delete_removes_job(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.delete_job(job.job_id)
        assert proc.get_job(job.job_id) is None

    def test_delete_nonexistent_returns_false(self):
        proc = DocBatchProcessor()
        assert proc.delete_job("ghost") is False

    def test_delete_decrements_total_jobs(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.delete_job(job.job_id)
        assert proc.total_jobs == 0

    def test_delete_completed_job(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        proc.run_job(job.job_id, _identity)
        assert proc.delete_job(job.job_id) is True
        assert proc.get_job(job.job_id) is None


# ---------------------------------------------------------------------------
# list_jobs
# ---------------------------------------------------------------------------

class TestListJobs:
    def test_empty_registry(self):
        proc = DocBatchProcessor()
        assert proc.list_jobs() == []

    def test_returns_all_jobs(self):
        proc = DocBatchProcessor()
        proc.create_job("a", [1])
        proc.create_job("b", [2])
        assert len(proc.list_jobs()) == 2

    def test_filter_by_status_pending(self):
        proc = DocBatchProcessor()
        j1 = proc.create_job("a", [1])
        j2 = proc.create_job("b", [2])
        proc.run_job(j2.job_id, _identity)
        pending = proc.list_jobs(status="pending")
        assert len(pending) == 1
        assert pending[0].job_id == j1.job_id

    def test_filter_by_status_completed(self):
        proc = DocBatchProcessor()
        j1 = proc.create_job("a", [1])
        proc.run_job(j1.job_id, _identity)
        completed = proc.list_jobs(status="completed")
        assert len(completed) == 1

    def test_filter_by_status_cancelled(self):
        proc = DocBatchProcessor()
        j1 = proc.create_job("a", [1])
        proc.cancel_job(j1.job_id)
        assert len(proc.list_jobs(status="cancelled")) == 1

    def test_filter_no_match(self):
        proc = DocBatchProcessor()
        proc.create_job("a", [1])
        assert proc.list_jobs(status="failed") == []

    def test_none_status_returns_all(self):
        proc = DocBatchProcessor()
        proc.create_job("a", [1])
        proc.create_job("b", [2])
        assert len(proc.list_jobs(status=None)) == 2


# ---------------------------------------------------------------------------
# get_job
# ---------------------------------------------------------------------------

class TestGetJob:
    def test_returns_job(self):
        proc = DocBatchProcessor()
        job = proc.create_job("j", [1])
        assert proc.get_job(job.job_id) is job

    def test_returns_none_for_missing(self):
        proc = DocBatchProcessor()
        assert proc.get_job("missing") is None


# ---------------------------------------------------------------------------
# total_jobs property
# ---------------------------------------------------------------------------

class TestTotalJobs:
    def test_zero_initially(self):
        assert DocBatchProcessor().total_jobs == 0

    def test_increments_on_create(self):
        proc = DocBatchProcessor()
        proc.create_job("a", [])
        assert proc.total_jobs == 1

    def test_decrements_on_delete(self):
        proc = DocBatchProcessor()
        job = proc.create_job("a", [])
        proc.delete_job(job.job_id)
        assert proc.total_jobs == 0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------

class TestThreadSafety:
    def test_concurrent_create_jobs(self):
        """Many threads create jobs simultaneously; total_jobs must be accurate."""
        proc = DocBatchProcessor()
        n = 50
        barrier = threading.Barrier(n)

        def create():
            barrier.wait()
            proc.create_job("t", [1, 2, 3])

        threads = [threading.Thread(target=create) for _ in range(n)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert proc.total_jobs == n

    def test_concurrent_run_jobs(self):
        """Multiple threads run independent jobs concurrently without corruption."""
        proc = DocBatchProcessor(batch_size=5)
        jobs = [proc.create_job(f"job-{i}", list(range(10))) for i in range(10)]
        results = {}
        errors = []
        lock = threading.Lock()

        def run(job):
            try:
                r = proc.run_job(job.job_id, _double)
                with lock:
                    results[job.job_id] = r
            except Exception as exc:
                with lock:
                    errors.append(exc)

        threads = [threading.Thread(target=run, args=(j,)) for j in jobs]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors
        assert len(results) == 10
        for r in results.values():
            assert r.succeeded == 10

    def test_concurrent_delete_and_list(self):
        """Deleting jobs while listing does not raise exceptions."""
        proc = DocBatchProcessor()
        jobs = [proc.create_job(f"j{i}", [i]) for i in range(20)]
        exceptions = []

        def delete_all():
            for job in jobs:
                try:
                    proc.delete_job(job.job_id)
                except Exception as exc:
                    exceptions.append(exc)

        def list_all():
            for _ in range(50):
                try:
                    proc.list_jobs()
                except Exception as exc:
                    exceptions.append(exc)

        t1 = threading.Thread(target=delete_all)
        t2 = threading.Thread(target=list_all)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert not exceptions
