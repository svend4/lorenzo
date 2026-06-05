"""Snapshot data structures for the snapshot store."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SnapshotMetadata:
    """Metadata for a stored snapshot (without the payload)."""

    snapshot_id: str
    name: str
    created_at: float
    description: str = ""
    tags: list[str] = field(default_factory=list)
    size_bytes: int = 0


@dataclass
class Snapshot:
    """A full snapshot: metadata plus raw byte payload."""

    metadata: SnapshotMetadata
    data: bytes
