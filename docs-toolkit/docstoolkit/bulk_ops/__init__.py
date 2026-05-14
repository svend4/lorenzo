"""Bulk operations module — batch INSERT/UPDATE/DELETE/UPSERT with pluggable handlers."""
from docstoolkit.bulk_ops.operation import (
    BulkOperation,
    OperationStatus,
    OperationType,
)
from docstoolkit.bulk_ops.batch import (
    BatchConfig,
    BatchResult,
    BulkBatch,
)
from docstoolkit.bulk_ops.processor import (
    BulkProcessor,
    OperationHandler,
)

__all__ = [
    # operation
    "OperationType",
    "OperationStatus",
    "BulkOperation",
    # batch
    "BatchConfig",
    "BatchResult",
    "BulkBatch",
    # processor
    "OperationHandler",
    "BulkProcessor",
]
