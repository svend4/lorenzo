"""Change detection module for incremental indexing (E32)."""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum


class ChangeType(Enum):
    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    UNCHANGED = "unchanged"


@dataclass
class DocumentChange:
    doc_id: str
    change_type: ChangeType
    content_hash: str
    detected_ts: float = field(default_factory=time.time)
    old_hash: str = ""

    def is_content_change(self) -> bool:
        """Return True if the change represents actual content change (ADDED or MODIFIED)."""
        return self.change_type in (ChangeType.ADDED, ChangeType.MODIFIED)


def _sha256_short(content: str) -> str:
    """Return the first 16 hex characters of the SHA-256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]


class ChangeDetector:
    """Detects changes to documents by maintaining an internal hash registry."""

    def __init__(self) -> None:
        self._registry: dict[str, str] = {}  # doc_id -> content_hash

    def detect(self, doc_id: str, content: str) -> DocumentChange:
        """Detect the type of change for a document given its current content."""
        new_hash = _sha256_short(content)
        if doc_id not in self._registry:
            self._registry[doc_id] = new_hash
            return DocumentChange(
                doc_id=doc_id,
                change_type=ChangeType.ADDED,
                content_hash=new_hash,
            )
        old_hash = self._registry[doc_id]
        if old_hash == new_hash:
            return DocumentChange(
                doc_id=doc_id,
                change_type=ChangeType.UNCHANGED,
                content_hash=new_hash,
                old_hash=old_hash,
            )
        # Hash differs — modified
        self._registry[doc_id] = new_hash
        return DocumentChange(
            doc_id=doc_id,
            change_type=ChangeType.MODIFIED,
            content_hash=new_hash,
            old_hash=old_hash,
        )

    def mark_deleted(self, doc_id: str) -> DocumentChange | None:
        """Mark a document as deleted. Returns a DELETED change or None if unknown."""
        if doc_id not in self._registry:
            return None
        old_hash = self._registry.pop(doc_id)
        return DocumentChange(
            doc_id=doc_id,
            change_type=ChangeType.DELETED,
            content_hash="",
            old_hash=old_hash,
        )

    def known_docs(self) -> list[str]:
        """Return a list of all currently known document IDs."""
        return list(self._registry.keys())

    def reset(self, doc_id: str | None = None) -> None:
        """Reset state for one doc (if doc_id provided) or all docs."""
        if doc_id is None:
            self._registry.clear()
        else:
            self._registry.pop(doc_id, None)
