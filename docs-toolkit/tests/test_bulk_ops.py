"""Tests for docstoolkit.bulk_ops — E15 Bulk operations module."""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.bulk_ops import (
    BatchConfig,
    BatchResult,
    BulkBatch,
    BulkOperation,
    BulkProcessor,
    OperationHandler,
    OperationStatus,
    OperationType,
)


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

class _OkHandler:
    """Handler that always marks an operation as SUCCESS."""

    def handle(self, op: BulkOperation) -> BulkOperation:
        return op.mark_success()


class _FailHandler:
    """Handler that always marks an operation as FAILED."""

    def handle(self, op: BulkOperation) -> BulkOperation:
        return op.mark_failed("intentional failure")


class _RaisingHandler:
    """Handler that raises an exception."""

    def handle(self, op: BulkOperation) -> BulkOperation:
        raise RuntimeError("boom")


def _make_batch(size: int = 3, config: BatchConfig | None = None) -> BulkBatch:
    batch = BulkBatch(config)
    for i in range(size):
        batch.add(OperationType.INSERT, {"index": i})
    return batch


# ---------------------------------------------------------------------------
# T1  OperationType enum
# ---------------------------------------------------------------------------

def test_operation_type_values():
    assert OperationType.INSERT.value == "insert"
    assert OperationType.UPDATE.value == "update"
    assert OperationType.DELETE.value == "delete"
    assert OperationType.UPSERT.value == "upsert"


def test_operation_type_all_members():
    members = {m.name for m in OperationType}
    assert members == {"INSERT", "UPDATE", "DELETE", "UPSERT"}


# ---------------------------------------------------------------------------
# T2  OperationStatus enum
# ---------------------------------------------------------------------------

def test_operation_status_values():
    assert OperationStatus.PENDING.value == "pending"
    assert OperationStatus.SUCCESS.value == "success"
    assert OperationStatus.FAILED.value == "failed"
    assert OperationStatus.SKIPPED.value == "skipped"


def test_operation_status_all_members():
    members = {m.name for m in OperationStatus}
    assert members == {"PENDING", "SUCCESS", "FAILED", "SKIPPED"}


# ---------------------------------------------------------------------------
# T3  BulkOperation dataclass
# ---------------------------------------------------------------------------

def test_bulk_operation_auto_id():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    assert isinstance(op.op_id, str) and len(op.op_id) == 36  # UUID4


def test_bulk_operation_unique_ids():
    op1 = BulkOperation(op_type=OperationType.INSERT, payload={})
    op2 = BulkOperation(op_type=OperationType.INSERT, payload={})
    assert op1.op_id != op2.op_id


def test_bulk_operation_default_status():
    op = BulkOperation(op_type=OperationType.DELETE, payload={"id": 1})
    assert op.status == OperationStatus.PENDING


def test_bulk_operation_default_error_none():
    op = BulkOperation(op_type=OperationType.UPDATE, payload={})
    assert op.error is None


def test_bulk_operation_created_ts_auto():
    before = time.time()
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    after = time.time()
    assert before <= op.created_ts <= after


def test_bulk_operation_explicit_fields():
    op = BulkOperation(
        op_type=OperationType.UPSERT,
        payload={"key": "val"},
        op_id="custom-id",
        status=OperationStatus.SUCCESS,
        error=None,
    )
    assert op.op_id == "custom-id"
    assert op.op_type == OperationType.UPSERT
    assert op.payload == {"key": "val"}
    assert op.status == OperationStatus.SUCCESS


# ---------------------------------------------------------------------------
# T4  BulkOperation state transitions
# ---------------------------------------------------------------------------

def test_mark_success_returns_new_instance():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = op.mark_success()
    assert result is not op


def test_mark_success_status():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = op.mark_success()
    assert result.status == OperationStatus.SUCCESS


def test_mark_success_clears_error():
    op = BulkOperation(op_type=OperationType.INSERT, payload={}, error="old error")
    result = op.mark_success()
    assert result.error is None


def test_mark_success_preserves_id_and_payload():
    op = BulkOperation(op_type=OperationType.INSERT, payload={"x": 1})
    result = op.mark_success()
    assert result.op_id == op.op_id
    assert result.payload == {"x": 1}


def test_mark_failed_returns_new_instance():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = op.mark_failed("err")
    assert result is not op


def test_mark_failed_status():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = op.mark_failed("something went wrong")
    assert result.status == OperationStatus.FAILED


def test_mark_failed_stores_error():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = op.mark_failed("database timeout")
    assert result.error == "database timeout"


def test_mark_failed_preserves_id():
    op = BulkOperation(op_type=OperationType.UPDATE, payload={})
    result = op.mark_failed("err")
    assert result.op_id == op.op_id


def test_mark_skipped_returns_new_instance():
    op = BulkOperation(op_type=OperationType.DELETE, payload={})
    result = op.mark_skipped()
    assert result is not op


def test_mark_skipped_status():
    op = BulkOperation(op_type=OperationType.DELETE, payload={})
    result = op.mark_skipped()
    assert result.status == OperationStatus.SKIPPED


def test_mark_skipped_clears_error():
    op = BulkOperation(op_type=OperationType.DELETE, payload={}, error="stale error")
    result = op.mark_skipped()
    assert result.error is None


# ---------------------------------------------------------------------------
# T5  BatchConfig dataclass
# ---------------------------------------------------------------------------

def test_batch_config_defaults():
    cfg = BatchConfig()
    assert cfg.max_batch_size == 100
    assert cfg.stop_on_error is False
    assert cfg.dry_run is False


def test_batch_config_custom():
    cfg = BatchConfig(max_batch_size=10, stop_on_error=True, dry_run=True)
    assert cfg.max_batch_size == 10
    assert cfg.stop_on_error is True
    assert cfg.dry_run is True


# ---------------------------------------------------------------------------
# T6  BulkBatch
# ---------------------------------------------------------------------------

def test_bulk_batch_starts_empty():
    batch = BulkBatch()
    assert batch.size() == 0


def test_bulk_batch_add_returns_operation():
    batch = BulkBatch()
    op = batch.add(OperationType.INSERT, {"val": 42})
    assert isinstance(op, BulkOperation)


def test_bulk_batch_add_increments_size():
    batch = BulkBatch()
    batch.add(OperationType.INSERT, {})
    batch.add(OperationType.UPDATE, {})
    assert batch.size() == 2


def test_bulk_batch_add_op_type():
    batch = BulkBatch()
    op = batch.add(OperationType.DELETE, {"id": 7})
    assert op.op_type == OperationType.DELETE
    assert op.payload == {"id": 7}


def test_bulk_batch_add_initial_status_pending():
    batch = BulkBatch()
    op = batch.add(OperationType.UPSERT, {})
    assert op.status == OperationStatus.PENDING


def test_bulk_batch_is_full_false_initially():
    batch = BulkBatch(BatchConfig(max_batch_size=5))
    assert not batch.is_full()


def test_bulk_batch_is_full_true_at_limit():
    cfg = BatchConfig(max_batch_size=3)
    batch = _make_batch(3, cfg)
    assert batch.is_full()


def test_bulk_batch_add_raises_when_full():
    cfg = BatchConfig(max_batch_size=2)
    batch = _make_batch(2, cfg)
    with pytest.raises(ValueError, match="full"):
        batch.add(OperationType.INSERT, {})


def test_bulk_batch_operations_returns_list():
    batch = _make_batch(3)
    ops = batch.operations()
    assert isinstance(ops, list)
    assert len(ops) == 3


def test_bulk_batch_operations_returns_copy():
    batch = _make_batch(2)
    ops = batch.operations()
    ops.clear()
    assert batch.size() == 2


def test_bulk_batch_clear():
    batch = _make_batch(5)
    batch.clear()
    assert batch.size() == 0
    assert not batch.is_full()


def test_bulk_batch_clear_allows_new_adds():
    cfg = BatchConfig(max_batch_size=2)
    batch = _make_batch(2, cfg)
    batch.clear()
    op = batch.add(OperationType.INSERT, {"fresh": True})
    assert op is not None
    assert batch.size() == 1


# ---------------------------------------------------------------------------
# T7  BatchResult
# ---------------------------------------------------------------------------

def test_batch_result_success_rate_zero_total():
    result = BatchResult()
    assert result.success_rate() == 0.0


def test_batch_result_success_rate_all_success():
    result = BatchResult(total=4, succeeded=4, failed=0, skipped=0)
    assert result.success_rate() == pytest.approx(1.0)


def test_batch_result_success_rate_partial():
    result = BatchResult(total=10, succeeded=7, failed=3, skipped=0)
    assert result.success_rate() == pytest.approx(0.7)


def test_batch_result_has_failures_false():
    result = BatchResult(total=3, succeeded=3, failed=0, skipped=0)
    assert result.has_failures() is False


def test_batch_result_has_failures_true():
    result = BatchResult(total=3, succeeded=2, failed=1, skipped=0)
    assert result.has_failures() is True


def test_batch_result_failed_ops_empty():
    op = BulkOperation(op_type=OperationType.INSERT, payload={})
    result = BatchResult(operations=[op.mark_success()], total=1, succeeded=1)
    assert result.failed_ops() == []


def test_batch_result_failed_ops_returns_only_failed():
    op1 = BulkOperation(op_type=OperationType.INSERT, payload={"a": 1})
    op2 = BulkOperation(op_type=OperationType.UPDATE, payload={"b": 2})
    op3 = BulkOperation(op_type=OperationType.DELETE, payload={"c": 3})
    failed_op = op2.mark_failed("err")
    result = BatchResult(
        operations=[op1.mark_success(), failed_op, op3.mark_skipped()],
        total=3,
        succeeded=1,
        failed=1,
        skipped=1,
    )
    failed = result.failed_ops()
    assert len(failed) == 1
    assert failed[0].status == OperationStatus.FAILED


# ---------------------------------------------------------------------------
# T8  BulkProcessor — basic dispatch
# ---------------------------------------------------------------------------

def test_processor_default_config():
    proc = BulkProcessor()
    assert proc._config.max_batch_size == 100


def test_processor_custom_config():
    cfg = BatchConfig(max_batch_size=5)
    proc = BulkProcessor(cfg)
    assert proc._config.max_batch_size == 5


def test_processor_success_handler():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _OkHandler())
    batch = _make_batch(3)
    result = proc.process(batch)
    assert result.succeeded == 3
    assert result.failed == 0
    assert result.total == 3


def test_processor_failed_handler():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _FailHandler())
    batch = _make_batch(2)
    result = proc.process(batch)
    assert result.failed == 2
    assert result.succeeded == 0


def test_processor_no_handler_marks_failed():
    proc = BulkProcessor()
    # No handler registered for INSERT
    batch = _make_batch(1)
    result = proc.process(batch)
    assert result.failed == 1
    failed = result.failed_ops()
    assert len(failed) == 1
    assert "no handler" in failed[0].error


def test_processor_raising_handler_marks_failed():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _RaisingHandler())
    batch = _make_batch(1)
    result = proc.process(batch)
    assert result.failed == 1
    assert "boom" in result.failed_ops()[0].error


def test_processor_mixed_handlers():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _OkHandler())
    proc.register_handler(OperationType.DELETE, _FailHandler())

    batch = BulkBatch()
    batch.add(OperationType.INSERT, {"a": 1})
    batch.add(OperationType.DELETE, {"b": 2})
    batch.add(OperationType.INSERT, {"c": 3})

    result = proc.process(batch)
    assert result.succeeded == 2
    assert result.failed == 1
    assert result.total == 3


def test_processor_operations_in_result():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _OkHandler())
    batch = _make_batch(2)
    result = proc.process(batch)
    assert len(result.operations) == 2
    assert all(op.status == OperationStatus.SUCCESS for op in result.operations)


# ---------------------------------------------------------------------------
# T9  BulkProcessor — stop_on_error
# ---------------------------------------------------------------------------

def test_stop_on_error_halts_after_first_failure():
    cfg = BatchConfig(stop_on_error=True)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _FailHandler())

    batch = _make_batch(5)
    result = proc.process(batch)
    # Only 1 should have been processed (first one fails and processing stops)
    assert result.failed == 1
    assert result.total == 5  # remaining ops still in result as PENDING


def test_stop_on_error_remaining_ops_pending():
    cfg = BatchConfig(stop_on_error=True)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _FailHandler())

    batch = _make_batch(3)
    result = proc.process(batch)
    # First op is FAILED; remaining 2 remain PENDING
    pending = [op for op in result.operations if op.status == OperationStatus.PENDING]
    assert len(pending) == 2


def test_stop_on_error_false_continues():
    cfg = BatchConfig(stop_on_error=False)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _FailHandler())

    batch = _make_batch(4)
    result = proc.process(batch)
    assert result.failed == 4
    assert result.total == 4


def test_stop_on_error_success_before_failure():
    """Two successes, then a failure — stop_on_error stops after the failure."""
    cfg = BatchConfig(stop_on_error=True)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _OkHandler())
    proc.register_handler(OperationType.DELETE, _FailHandler())

    batch = BulkBatch()
    batch.add(OperationType.INSERT, {"n": 1})
    batch.add(OperationType.INSERT, {"n": 2})
    batch.add(OperationType.DELETE, {"n": 3})
    batch.add(OperationType.INSERT, {"n": 4})

    result = proc.process(batch)
    assert result.succeeded == 2
    assert result.failed == 1
    assert result.total == 4
    # Last INSERT remains PENDING
    pending = [op for op in result.operations if op.status == OperationStatus.PENDING]
    assert len(pending) == 1


# ---------------------------------------------------------------------------
# T10  BulkProcessor — dry_run
# ---------------------------------------------------------------------------

def test_dry_run_skips_all():
    cfg = BatchConfig(dry_run=True)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _OkHandler())
    batch = _make_batch(4)
    result = proc.process(batch)
    assert result.skipped == 4
    assert result.succeeded == 0
    assert result.failed == 0


def test_dry_run_does_not_call_handler():
    """Handler call count stays zero in dry_run mode."""
    call_count = {"n": 0}

    class _CountingHandler:
        def handle(self, op: BulkOperation) -> BulkOperation:
            call_count["n"] += 1
            return op.mark_success()

    cfg = BatchConfig(dry_run=True)
    proc = BulkProcessor(cfg)
    proc.register_handler(OperationType.INSERT, _CountingHandler())
    batch = _make_batch(3)
    proc.process(batch)
    assert call_count["n"] == 0


def test_dry_run_all_ops_skipped_status():
    cfg = BatchConfig(dry_run=True)
    proc = BulkProcessor(cfg)
    batch = _make_batch(2)
    result = proc.process(batch)
    assert all(op.status == OperationStatus.SKIPPED for op in result.operations)


def test_dry_run_no_handler_still_skips():
    """Even without a registered handler, dry_run marks ops SKIPPED."""
    cfg = BatchConfig(dry_run=True)
    proc = BulkProcessor(cfg)
    batch = _make_batch(2)
    result = proc.process(batch)
    assert result.skipped == 2
    assert result.failed == 0


# ---------------------------------------------------------------------------
# T11  process_ops convenience wrapper
# ---------------------------------------------------------------------------

def test_process_ops_basic():
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _OkHandler())
    ops = [BulkOperation(op_type=OperationType.INSERT, payload={"i": i}) for i in range(5)]
    result = proc.process_ops(ops)
    assert result.succeeded == 5
    assert result.total == 5


def test_process_ops_empty():
    proc = BulkProcessor()
    result = proc.process_ops([])
    assert result.total == 0
    assert result.succeeded == 0
    assert result.success_rate() == 0.0


def test_process_ops_no_handler():
    proc = BulkProcessor()
    ops = [BulkOperation(op_type=OperationType.UPDATE, payload={})]
    result = proc.process_ops(ops)
    assert result.failed == 1


# ---------------------------------------------------------------------------
# T12  OperationHandler protocol
# ---------------------------------------------------------------------------

def test_operation_handler_protocol_check():
    assert isinstance(_OkHandler(), OperationHandler)
    assert isinstance(_FailHandler(), OperationHandler)


def test_non_handler_fails_protocol_check():
    class _NotHandler:
        pass  # no handle() method

    assert not isinstance(_NotHandler(), OperationHandler)


# ---------------------------------------------------------------------------
# T13  Edge cases
# ---------------------------------------------------------------------------

def test_empty_batch_process():
    proc = BulkProcessor()
    batch = BulkBatch()
    result = proc.process(batch)
    assert result.total == 0
    assert result.success_rate() == 0.0
    assert result.has_failures() is False


def test_batch_default_config_max_size():
    batch = BulkBatch()
    # fill to default max (100)
    for i in range(100):
        batch.add(OperationType.INSERT, {"i": i})
    assert batch.is_full()
    with pytest.raises(ValueError):
        batch.add(OperationType.INSERT, {})


def test_batch_add_preserves_order():
    batch = BulkBatch()
    for i in range(5):
        batch.add(OperationType.INSERT, {"seq": i})
    ops = batch.operations()
    seqs = [op.payload["seq"] for op in ops]
    assert seqs == list(range(5))


def test_success_rate_only_skipped():
    result = BatchResult(total=3, succeeded=0, failed=0, skipped=3)
    assert result.success_rate() == pytest.approx(0.0)


def test_register_handler_overwrites_previous():
    """Re-registering a handler for the same op_type replaces the old one."""
    proc = BulkProcessor()
    proc.register_handler(OperationType.INSERT, _FailHandler())
    proc.register_handler(OperationType.INSERT, _OkHandler())  # overwrite
    batch = _make_batch(2)
    result = proc.process(batch)
    assert result.succeeded == 2
    assert result.failed == 0


def test_bulk_operation_payload_independent():
    """Each BulkOperation stores its own payload dict reference."""
    payload = {"key": "value"}
    op = BulkOperation(op_type=OperationType.INSERT, payload=payload)
    assert op.payload is payload


def test_process_ops_dry_run():
    """process_ops respects dry_run config."""
    cfg = BatchConfig(dry_run=True)
    proc = BulkProcessor(cfg)
    ops = [BulkOperation(op_type=OperationType.DELETE, payload={}) for _ in range(3)]
    result = proc.process_ops(ops)
    assert result.skipped == 3
    assert result.total == 3


def test_batch_result_total_reflects_all_ops():
    ops = [
        BulkOperation(op_type=OperationType.INSERT, payload={}).mark_success(),
        BulkOperation(op_type=OperationType.UPDATE, payload={}).mark_failed("e"),
        BulkOperation(op_type=OperationType.DELETE, payload={}).mark_skipped(),
    ]
    result = BatchResult(operations=ops, total=3, succeeded=1, failed=1, skipped=1)
    assert result.total == 3
    assert len(result.failed_ops()) == 1
    assert result.has_failures() is True
    assert result.success_rate() == pytest.approx(1 / 3)
