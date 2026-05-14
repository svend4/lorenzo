import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class CapturedState:
    """A point-in-time snapshot of the corpus."""
    snapshot_id: str
    ts: str
    doc_count: int
    total_bytes: int
    doc_hashes: dict = field(default_factory=dict)   # {doc_id: sha256_hex}
    metadata: dict = field(default_factory=dict)     # arbitrary key-value

    def to_dict(self) -> dict:
        return {
            "snapshot_id": self.snapshot_id,
            "ts": self.ts,
            "doc_count": self.doc_count,
            "total_bytes": self.total_bytes,
            "doc_hashes": self.doc_hashes,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, d: dict) -> "CapturedState":
        return cls(
            snapshot_id=d["snapshot_id"],
            ts=d.get("ts", ""),
            doc_count=int(d.get("doc_count", 0)),
            total_bytes=int(d.get("total_bytes", 0)),
            doc_hashes=d.get("doc_hashes", {}),
            metadata=d.get("metadata", {}),
        )


class SnapshotCapture:
    """Captures corpus state as a CapturedState."""

    def capture(
        self,
        docs: dict,          # {doc_id: content_str}
        snapshot_id: str = "",
        metadata: dict | None = None,
    ) -> CapturedState:
        """Capture state of all documents.

        snapshot_id: auto-generate if empty (timestamp-based: 'snap-YYYYMMDDHHMMSS')
        doc_hashes: {doc_id: sha256(content.encode()).hexdigest()[:16]}
        total_bytes: sum of len(content.encode()) for all docs
        doc_count: len(docs)
        """
        if not snapshot_id:
            snapshot_id = "snap-" + datetime.utcnow().strftime("%Y%m%d%H%M%S")

        ts = datetime.utcnow().isoformat()

        doc_hashes: dict = {}
        total_bytes = 0
        for doc_id, content in docs.items():
            encoded = content.encode()
            total_bytes += len(encoded)
            doc_hashes[doc_id] = hashlib.sha256(encoded).hexdigest()[:16]

        return CapturedState(
            snapshot_id=snapshot_id,
            ts=ts,
            doc_count=len(docs),
            total_bytes=total_bytes,
            doc_hashes=doc_hashes,
            metadata=metadata or {},
        )

    def capture_directory(
        self,
        path: Path,
        pattern: str = "*.md",
        snapshot_id: str = "",
    ) -> CapturedState:
        """Capture all files matching pattern in path.

        doc_id = file path relative to path (as str)
        content = file.read_text(errors='replace')
        Then call capture().
        """
        path = Path(path)
        docs: dict = {}
        for file in sorted(path.rglob(pattern)):
            doc_id = str(file.relative_to(path))
            content = file.read_text(errors="replace")
            docs[doc_id] = content

        return self.capture(docs=docs, snapshot_id=snapshot_id)
