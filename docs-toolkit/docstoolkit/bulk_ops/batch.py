"""Bulk operations — batch container and result aggregation."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.bulk_ops.operation import BulkOperation, OperationStatus, OperationType


@dataclass
class BatchConfig:
    """Configuration for a BulkBatch / BulkProcessor run."""

    max_batch_size: int = 100
    stop_on_error: bool = False
    dry_run: bool = False


@dataclass
class BatchResult:
    """Aggregated outcome of processing a batch of operations."""

    operations: list[BulkOperation] = field(default_factory=list)
    total: int = 0
    succeeded: int = 0
    failed: int = 0
    skipped: int = 0

    # ------------------------------------------------------------------
    # Convenience helpers
    # ------------------------------------------------------------------

    def success_rate(self) -> float:
        """Fraction of operations that succeeded (0.0–1.0).  Returns 0.0 for empty batches."""
        if self.total == 0:
            return 0.0
        return self.succeeded / self.total

    def has_failures(self) -> bool:
        """True when at least one operation failed."""
        return self.failed > 0

    def failed_ops(self) -> list[BulkOperation]:
        """Return only the operations whose status is FAILED."""
        return [op for op in self.operations if op.status == OperationStatus.FAILED]


class BulkBatch:
    """Ordered collection of BulkOperations with a configurable size cap."""

    def __init__(self, config: BatchConfig | None = None) -> None:
        self._config: BatchConfig = config if config is not None else BatchConfig()
        self._ops: list[BulkOperation] = []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, op_type: OperationType, payload: dict) -> BulkOperation:
        """Create and append a new PENDING operation.

        Raises:
            ValueError: when the batch has already reached *max_batch_size*.
        """
        if self.is_full():
            raise ValueError(
                f"Batch is full (max_batch_size={self._config.max_batch_size})"
            )
        op = BulkOperation(op_type=op_type, payload=payload)
        self._ops.append(op)
        return op

    def clear(self) -> None:
        """Remove all operations from the batch."""
        self._ops.clear()

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def size(self) -> int:
        """Current number of operations in the batch."""
        return len(self._ops)

    def is_full(self) -> bool:
        """True when no more operations can be added."""
        return len(self._ops) >= self._config.max_batch_size

    def operations(self) -> list[BulkOperation]:
        """Return a shallow copy of the operations list."""
        return list(self._ops)
