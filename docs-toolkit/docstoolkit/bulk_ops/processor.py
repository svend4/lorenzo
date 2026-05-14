"""Bulk operations — processor that dispatches operations to registered handlers."""
from __future__ import annotations

from typing import Protocol, runtime_checkable

from docstoolkit.bulk_ops.batch import BatchConfig, BatchResult, BulkBatch
from docstoolkit.bulk_ops.operation import BulkOperation, OperationStatus, OperationType


@runtime_checkable
class OperationHandler(Protocol):
    """Protocol for objects that can handle a single BulkOperation."""

    def handle(self, op: BulkOperation) -> BulkOperation:
        """Process *op* and return the updated operation (SUCCESS or FAILED)."""
        ...


class BulkProcessor:
    """Dispatch-based processor that executes batches of operations."""

    def __init__(self, config: BatchConfig | None = None) -> None:
        self._config: BatchConfig = config if config is not None else BatchConfig()
        self._handlers: dict[OperationType, OperationHandler] = {}

    # ------------------------------------------------------------------
    # Handler registration
    # ------------------------------------------------------------------

    def register_handler(self, op_type: OperationType, handler: OperationHandler) -> None:
        """Bind *handler* to *op_type*."""
        self._handlers[op_type] = handler

    # ------------------------------------------------------------------
    # Processing
    # ------------------------------------------------------------------

    def process(self, batch: BulkBatch) -> BatchResult:
        """Execute every operation in *batch* according to the current config.

        Behaviour:
        - **dry_run**: every operation is marked SKIPPED without calling any handler.
        - **stop_on_error**: processing halts immediately after the first FAILED op;
          remaining operations stay PENDING and are included in the result as-is.
        - **no handler**: the operation is marked FAILED with a "no handler" error.
        """
        return self._run(batch.operations())

    def process_ops(self, ops: list[BulkOperation]) -> BatchResult:
        """Convenience wrapper: process a plain list of BulkOperation objects."""
        # Wrap in a temporary batch to reuse _run
        return self._run(ops)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _run(self, ops: list[BulkOperation]) -> BatchResult:
        processed: list[BulkOperation] = []
        succeeded = 0
        failed = 0
        skipped = 0

        for op in ops:
            if self._config.dry_run:
                result_op = op.mark_skipped()
                processed.append(result_op)
                skipped += 1
                continue

            handler = self._handlers.get(op.op_type)
            if handler is None:
                result_op = op.mark_failed(
                    f"no handler registered for op_type '{op.op_type.value}'"
                )
                processed.append(result_op)
                failed += 1
                if self._config.stop_on_error:
                    # Append remaining ops unchanged and stop
                    remaining = ops[len(processed):]
                    processed.extend(remaining)
                    break
                continue

            try:
                result_op = handler.handle(op)
            except Exception as exc:  # noqa: BLE001
                result_op = op.mark_failed(str(exc))

            processed.append(result_op)

            if result_op.status == OperationStatus.SUCCESS:
                succeeded += 1
            elif result_op.status == OperationStatus.FAILED:
                failed += 1
                if self._config.stop_on_error:
                    # Append remaining ops unchanged and stop
                    remaining = ops[len(processed):]
                    processed.extend(remaining)
                    break
            elif result_op.status == OperationStatus.SKIPPED:
                skipped += 1

        return BatchResult(
            operations=processed,
            total=len(processed),
            succeeded=succeeded,
            failed=failed,
            skipped=skipped,
        )
