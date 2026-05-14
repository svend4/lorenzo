"""E324 DocAttachmentStore — manage file attachments for documents.

All operations are thread-safe via a single ``threading.Lock``.
No third-party dependencies; only the Python standard library is used.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Attachment:
    """A file attachment to a document."""

    attachment_id: str
    doc_id: str
    filename: str
    mime_type: str = "application/octet-stream"
    size_bytes: int = 0
    uploaded_at: float = 0.0
    uploaded_by: str = ""
    checksum: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class AttachmentStats:
    """Aggregate statistics over all attachments held in the store."""

    total_attachments: int
    unique_docs: int
    total_size_bytes: int
    mime_type_counts: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# DocAttachmentStore
# ---------------------------------------------------------------------------


class DocAttachmentStore:
    """Thread-safe in-memory store for document attachments.

    Attachments are keyed by a UUID ``attachment_id``; insertion order
    for each document is preserved so that :meth:`attachments_for_doc`
    returns attachments in the order they were uploaded.
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        # attachment_id → Attachment
        self._attachments: Dict[str, Attachment] = {}
        # doc_id → list of attachment_ids in insertion order
        self._by_doc: Dict[str, List[str]] = {}

    # ------------------------------------------------------------------
    # Mutating operations
    # ------------------------------------------------------------------

    def attach(
        self,
        doc_id: str,
        filename: str,
        mime_type: str = "application/octet-stream",
        size_bytes: int = 0,
        uploaded_by: str = "",
        checksum: str = "",
        metadata: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> Attachment:
        """Create a new attachment record for *doc_id*.

        Returns
        -------
        Attachment
            The newly created attachment.
        """
        attachment_id = str(uuid.uuid4())
        uploaded_at = now if now is not None else time.time()
        att = Attachment(
            attachment_id=attachment_id,
            doc_id=doc_id,
            filename=filename,
            mime_type=mime_type,
            size_bytes=size_bytes,
            uploaded_at=uploaded_at,
            uploaded_by=uploaded_by,
            checksum=checksum,
            metadata=dict(metadata) if metadata is not None else {},
        )
        with self._lock:
            self._attachments[attachment_id] = att
            self._by_doc.setdefault(doc_id, []).append(attachment_id)
        return att

    def detach(self, attachment_id: str) -> bool:
        """Remove a single attachment by *attachment_id*.

        Returns
        -------
        bool
            ``True`` if the attachment existed and was removed; ``False``
            otherwise.
        """
        with self._lock:
            att = self._attachments.pop(attachment_id, None)
            if att is None:
                return False
            ids = self._by_doc.get(att.doc_id, [])
            try:
                ids.remove(attachment_id)
            except ValueError:
                pass
            if not ids:
                self._by_doc.pop(att.doc_id, None)
            return True

    def detach_all(self, doc_id: str) -> int:
        """Delete **all** attachments for *doc_id*.

        Returns
        -------
        int
            Number of attachments that were removed.
        """
        with self._lock:
            ids = self._by_doc.pop(doc_id, [])
            for aid in ids:
                self._attachments.pop(aid, None)
            return len(ids)

    # ------------------------------------------------------------------
    # Read operations
    # ------------------------------------------------------------------

    def get(self, attachment_id: str) -> Optional[Attachment]:
        """Return the attachment with the given *attachment_id*, or ``None``."""
        with self._lock:
            return self._attachments.get(attachment_id)

    def attachments_for_doc(self, doc_id: str) -> List[Attachment]:
        """Return attachments for *doc_id* in insertion order."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            return [self._attachments[aid] for aid in ids if aid in self._attachments]

    def find_by_filename(self, doc_id: str, filename: str) -> List[Attachment]:
        """Return attachments on *doc_id* whose filename equals *filename*.

        Sorted by ``uploaded_at`` ascending.
        """
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            matches = [
                self._attachments[aid]
                for aid in ids
                if aid in self._attachments
                and self._attachments[aid].filename == filename
            ]
        matches.sort(key=lambda a: a.uploaded_at)
        return matches

    def find_by_checksum(self, checksum: str) -> List[Attachment]:
        """Return all attachments with the given *checksum* across all docs.

        Sorted by ``uploaded_at`` ascending.
        """
        with self._lock:
            matches = [
                att for att in self._attachments.values() if att.checksum == checksum
            ]
        matches.sort(key=lambda a: a.uploaded_at)
        return matches

    def total_size_for_doc(self, doc_id: str) -> int:
        """Return the sum of ``size_bytes`` for all attachments on *doc_id*."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            return sum(
                self._attachments[aid].size_bytes
                for aid in ids
                if aid in self._attachments
            )

    def all_doc_ids(self) -> List[str]:
        """Return a sorted list of doc IDs that have at least one attachment."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def largest_attachments(self, limit: int = 10) -> List[Attachment]:
        """Return attachments sorted by ``size_bytes`` desc, then ``attachment_id`` asc."""
        with self._lock:
            atts = list(self._attachments.values())
        atts.sort(key=lambda a: (-a.size_bytes, a.attachment_id))
        return atts[:limit]

    def stats(self) -> AttachmentStats:
        """Return aggregate statistics over all attachments currently held."""
        with self._lock:
            total_attachments = len(self._attachments)
            unique_docs = len(self._by_doc)
            total_size_bytes = sum(
                att.size_bytes for att in self._attachments.values()
            )
            mime_type_counts: Dict[str, int] = {}
            for att in self._attachments.values():
                mime_type_counts[att.mime_type] = (
                    mime_type_counts.get(att.mime_type, 0) + 1
                )
        return AttachmentStats(
            total_attachments=total_attachments,
            unique_docs=unique_docs,
            total_size_bytes=total_size_bytes,
            mime_type_counts=mime_type_counts,
        )
