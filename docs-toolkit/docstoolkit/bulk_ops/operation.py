"""Bulk operations — operation primitives: types, statuses, and the BulkOperation record."""
from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum


class OperationType(Enum):
    INSERT = "insert"
    UPDATE = "update"
    DELETE = "delete"
    UPSERT = "upsert"


class OperationStatus(Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class BulkOperation:
    """A single unit of work in a bulk batch."""

    op_type: OperationType
    payload: dict
    op_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: OperationStatus = OperationStatus.PENDING
    error: str | None = None
    created_ts: float = field(default_factory=time.time)

    # ------------------------------------------------------------------
    # State transitions — return new instances (immutable-style)
    # ------------------------------------------------------------------

    def mark_success(self) -> "BulkOperation":
        """Return a copy of this operation marked as SUCCESS."""
        from dataclasses import replace
        return replace(self, status=OperationStatus.SUCCESS, error=None)

    def mark_failed(self, error: str) -> "BulkOperation":
        """Return a copy of this operation marked as FAILED with an error message."""
        from dataclasses import replace
        return replace(self, status=OperationStatus.FAILED, error=error)

    def mark_skipped(self) -> "BulkOperation":
        """Return a copy of this operation marked as SKIPPED."""
        from dataclasses import replace
        return replace(self, status=OperationStatus.SKIPPED, error=None)
