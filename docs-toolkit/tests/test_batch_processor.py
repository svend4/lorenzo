"""Tests for docstoolkit.batch_processor (E107)."""
import threading
import pytest

from docstoolkit.batch_processor import BatchConfig, BatchProcessor, BatchResult, ItemResult


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def double(x):
    return x * 2

def fail_on(bad):
    def fn(x):
        if x == bad:
            raise ValueError(f"bad item: {x}")
        return x * 2
    return fn

def always_fail(x):
    raise RuntimeError("always fails")


# ---------------------------------------------------------------------------
# BatchConfig defaults
# ---------------------------------------------------------------------------

class TestBatchConfig:
    def test_defaults(self):
        cfg = BatchConfig()
        assert cfg.batch_size == 10
        assert cfg.max_workers == 1
        assert cfg.on_error == "skip"
        assert cfg.progress_callback is None

    def test_custom(self):
        cfg = BatchConfig(batch_size=5, max_workers=4, on_error="raise")
        assert cfg.batch_size == 5
        assert cfg.max_workers == 4


# ---------------------------------------------------------------------------
# BatchResult properties
# ---------------------------------------------------------------------------

class TestBatchResult:
    def test_successful(self):
        r = BatchResult([
            ItemResult(0, "a", output="A", success=True),
            ItemResult(1, "b", output=None, error=Exception(), success=False),
        ])
        assert len(r.successful) == 1
        assert r.successful[0].item == "a"

    def test_failed(self):
        r = BatchResult([
            ItemResult(0, "a", output="A", success=True),
            ItemResult(1, "b", output=None, error=Exception(), success=False),
        ])
        assert len(r.failed) == 1
        assert r.failed[0].item == "b"

    def test_success_count(self):
        r = BatchResult([
            ItemResult(i, i, output=i, success=True) for i in range(5)
        ])
        assert r.success_count == 5
        assert r.failure_count == 0

    def test_failure_count(self):
        r = BatchResult([
            ItemResult(0, 0, success=True),
            ItemResult(1, 1, success=False),
            ItemResult(2, 2, success=False),
        ])
        assert r.failure_count == 2
        assert r.success_count == 1

    def test_outputs_in_order(self):
        # Shuffle order to test sorting
        r = BatchResult([
            ItemResult(2, 2, output=4, success=True),
            ItemResult(0, 0, output=0, success=True),
            ItemResult(1, 1, output=2, success=True),
        ])
        assert r.outputs == [0, 2, 4]

    def test_outputs_skips_failures(self):
        r = BatchResult([
            ItemResult(0, 0, output=0, success=True),
            ItemResult(1, 1, output=None, success=False),
            ItemResult(2, 2, output=4, success=True),
        ])
        assert r.outputs == [0, 4]

    def test_empty_result(self):
        r = BatchResult()
        assert r.success_count == 0
        assert r.failure_count == 0
        assert r.outputs == []
        assert r.successful == []
        assert r.failed == []


# ---------------------------------------------------------------------------
# BatchProcessor.chunk
# ---------------------------------------------------------------------------

class TestChunk:
    def test_chunk_basic(self):
        p = BatchProcessor(BatchConfig(batch_size=3))
        chunks = p.chunk([1, 2, 3, 4, 5])
        assert chunks == [[1, 2, 3], [4, 5]]

    def test_chunk_exact_multiple(self):
        p = BatchProcessor(BatchConfig(batch_size=2))
        chunks = p.chunk([1, 2, 3, 4])
        assert chunks == [[1, 2], [3, 4]]

    def test_chunk_size_1(self):
        p = BatchProcessor(BatchConfig(batch_size=1))
        chunks = p.chunk([10, 20, 30])
        assert chunks == [[10], [20], [30]]

    def test_chunk_larger_than_items(self):
        p = BatchProcessor(BatchConfig(batch_size=100))
        chunks = p.chunk([1, 2, 3])
        assert chunks == [[1, 2, 3]]

    def test_chunk_empty(self):
        p = BatchProcessor()
        assert p.chunk([]) == []

    def test_chunk_custom_size(self):
        p = BatchProcessor(BatchConfig(batch_size=10))
        chunks = p.chunk([1, 2, 3, 4, 5], size=2)
        assert chunks == [[1, 2], [3, 4], [5]]


# ---------------------------------------------------------------------------
# BatchProcessor.process — basic
# ---------------------------------------------------------------------------

class TestProcessBasic:
    def test_empty_input(self):
        p = BatchProcessor()
        result = p.process([], double)
        assert result.success_count == 0
        assert result.results == []

    def test_single_item_success(self):
        p = BatchProcessor()
        result = p.process([5], double)
        assert result.success_count == 1
        assert result.outputs == [10]

    def test_all_success(self):
        p = BatchProcessor(BatchConfig(batch_size=3))
        result = p.process([1, 2, 3, 4, 5], double)
        assert result.success_count == 5
        assert result.failure_count == 0
        assert result.outputs == [2, 4, 6, 8, 10]

    def test_index_preserved(self):
        p = BatchProcessor(BatchConfig(batch_size=2))
        result = p.process([10, 20, 30], double)
        for i, r in enumerate(result.results):
            assert r.index == i
            assert r.item == [10, 20, 30][i]

    def test_results_in_original_order(self):
        p = BatchProcessor(BatchConfig(batch_size=2))
        result = p.process([1, 2, 3, 4, 5], double)
        assert [r.item for r in result.results] == [1, 2, 3, 4, 5]

    def test_default_config(self):
        p = BatchProcessor()
        result = p.process([1, 2, 3], double)
        assert result.success_count == 3


# ---------------------------------------------------------------------------
# BatchProcessor.process — error handling
# ---------------------------------------------------------------------------

class TestProcessErrors:
    def test_on_error_skip_continues(self):
        p = BatchProcessor(BatchConfig(on_error="skip"))
        result = p.process([1, 2, 3], fail_on(2))
        assert result.success_count == 2
        assert result.failure_count == 1
        assert result.outputs == [2, 6]

    def test_on_error_skip_stores_error(self):
        p = BatchProcessor(BatchConfig(on_error="skip"))
        result = p.process([1, 2], fail_on(1))
        failed = result.failed
        assert len(failed) == 1
        assert isinstance(failed[0].error, ValueError)
        assert not failed[0].success

    def test_on_error_raise_reraises(self):
        p = BatchProcessor(BatchConfig(on_error="raise"))
        with pytest.raises(RuntimeError, match="always fails"):
            p.process([1, 2, 3], always_fail)

    def test_on_error_collect_stores_errors(self):
        p = BatchProcessor(BatchConfig(on_error="collect"))
        result = p.process([1, 2, 3], fail_on(2))
        assert result.failure_count == 1
        assert result.failed[0].error is not None

    def test_on_error_collect_continues(self):
        p = BatchProcessor(BatchConfig(on_error="collect"))
        result = p.process([1, 2, 3, 4], fail_on(2))
        assert result.success_count == 3

    def test_all_fail_skip(self):
        p = BatchProcessor(BatchConfig(on_error="skip"))
        result = p.process([1, 2, 3], always_fail)
        assert result.success_count == 0
        assert result.failure_count == 3
        assert result.outputs == []

    def test_mixed_fail_in_batch(self):
        p = BatchProcessor(BatchConfig(batch_size=3, on_error="skip"))
        result = p.process([1, 2, 3, 4, 5, 6], fail_on(3))
        assert result.success_count == 5
        assert result.failure_count == 1


# ---------------------------------------------------------------------------
# BatchProcessor.process — progress callback
# ---------------------------------------------------------------------------

class TestProgressCallback:
    def test_callback_called_per_batch(self):
        calls = []
        def cb(done, total):
            calls.append((done, total))

        p = BatchProcessor(BatchConfig(batch_size=2, progress_callback=cb))
        p.process([1, 2, 3, 4, 5], double)
        assert len(calls) == 3  # 3 batches: [1,2], [3,4], [5]

    def test_callback_total_correct(self):
        totals = []
        p = BatchProcessor(BatchConfig(
            batch_size=3,
            progress_callback=lambda d, t: totals.append(t)
        ))
        p.process(list(range(7)), double)
        assert all(t == 7 for t in totals)

    def test_callback_done_cumulative(self):
        dones = []
        p = BatchProcessor(BatchConfig(
            batch_size=2,
            progress_callback=lambda d, t: dones.append(d)
        ))
        p.process([1, 2, 3, 4], double)
        assert dones == [2, 4]

    def test_no_callback_no_error(self):
        p = BatchProcessor(BatchConfig(progress_callback=None))
        result = p.process([1, 2, 3], double)
        assert result.success_count == 3


# ---------------------------------------------------------------------------
# BatchProcessor.process — parallel
# ---------------------------------------------------------------------------

class TestProcessParallel:
    def test_parallel_all_success(self):
        p = BatchProcessor(BatchConfig(batch_size=5, max_workers=4))
        result = p.process(list(range(10)), double)
        assert result.success_count == 10
        assert result.outputs == [i * 2 for i in range(10)]

    def test_parallel_preserves_order(self):
        p = BatchProcessor(BatchConfig(batch_size=10, max_workers=4))
        items = list(range(20))
        result = p.process(items, double)
        assert [r.index for r in result.results] == list(range(20))
        assert result.outputs == [i * 2 for i in range(20)]

    def test_parallel_on_error_skip(self):
        p = BatchProcessor(BatchConfig(batch_size=5, max_workers=2, on_error="skip"))
        result = p.process(list(range(10)), fail_on(5))
        assert result.success_count == 9
        assert result.failure_count == 1

    def test_parallel_on_error_raise(self):
        p = BatchProcessor(BatchConfig(batch_size=10, max_workers=2, on_error="raise"))
        with pytest.raises(RuntimeError):
            p.process([1, 2, 3], always_fail)


# ---------------------------------------------------------------------------
# BatchProcessor.process_batches
# ---------------------------------------------------------------------------

class TestProcessBatches:
    def test_returns_list_of_batches(self):
        p = BatchProcessor(BatchConfig(batch_size=2))
        batches = p.process_batches([1, 2, 3, 4, 5], double)
        assert len(batches) == 3  # [1,2], [3,4], [5]

    def test_each_batch_is_list_of_results(self):
        p = BatchProcessor(BatchConfig(batch_size=3))
        batches = p.process_batches([1, 2, 3, 4], double)
        assert len(batches[0]) == 3
        assert len(batches[1]) == 1

    def test_all_items_present(self):
        p = BatchProcessor(BatchConfig(batch_size=2))
        batches = p.process_batches([10, 20, 30], double)
        all_results = [r for batch in batches for r in batch]
        assert sorted(r.item for r in all_results) == [10, 20, 30]

    def test_empty_input(self):
        p = BatchProcessor()
        batches = p.process_batches([], double)
        assert batches == []

    def test_single_batch(self):
        p = BatchProcessor(BatchConfig(batch_size=100))
        batches = p.process_batches([1, 2, 3], double)
        assert len(batches) == 1
        assert len(batches[0]) == 3
