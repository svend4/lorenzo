"""E359 DocChangesetStore implementation.

Thread-safe in-memory store grouping document edits into named changesets
that progress through a simple lifecycle: draft -> submitted -> merged
(with discard available from draft or submitted).
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Changeset:
    """A named bundle of document edits."""

    changeset_id: str
    title: str
    author: str
    created_at: float = 0.0
    status: str = "draft"
    description: str = ""
    submitted_at: Optional[float] = None
    merged_at: Optional[float] = None


@dataclass
class ChangesetEdit:
    """A single edit within a changeset."""

    edit_id: int
    changeset_id: str
    doc_id: str
    operation: str
    content: str = ""


@dataclass
class ChangesetStats:
    """Aggregate statistics about the store."""

    total_changesets: int
    draft_count: int
    submitted_count: int
    merged_count: int
    discarded_count: int
    total_edits: int


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


_VALID_OPERATIONS = {"add", "modify", "delete"}
_VALID_STATUSES = {"draft", "submitted", "merged", "discarded"}


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocChangesetStore:
    """In-memory thread-safe store for document changesets and their edits."""

    def __init__(self) -> None:
        self._changesets: dict[str, Changeset] = {}
        self._edits: dict[int, ChangesetEdit] = {}
        self._edits_by_cs: dict[str, list[int]] = {}
        self._next_edit_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Creation
    # ------------------------------------------------------------------

    def create_changeset(
        self,
        title: str,
        author: str,
        description: str = "",
        now: Optional[float] = None,
    ) -> Changeset:
        """Create a new changeset in ``draft`` status."""
        with self._lock:
            ts = now if now is not None else time.time()
            changeset_id = str(uuid.uuid4())
            cs = Changeset(
                changeset_id=changeset_id,
                title=title,
                author=author,
                created_at=ts,
                status="draft",
                description=description,
            )
            self._changesets[changeset_id] = cs
            self._edits_by_cs[changeset_id] = []
            return cs

    # ------------------------------------------------------------------
    # Edits
    # ------------------------------------------------------------------

    def add_edit(
        self,
        changeset_id: str,
        doc_id: str,
        operation: str,
        content: str = "",
    ) -> Optional[ChangesetEdit]:
        """Add an edit to a draft changeset.

        Returns ``None`` if the changeset does not exist, is not in ``draft``
        status, or the operation is invalid.
        """
        if operation not in _VALID_OPERATIONS:
            return None
        with self._lock:
            cs = self._changesets.get(changeset_id)
            if cs is None or cs.status != "draft":
                return None
            edit_id = self._next_edit_id
            self._next_edit_id += 1
            edit = ChangesetEdit(
                edit_id=edit_id,
                changeset_id=changeset_id,
                doc_id=doc_id,
                operation=operation,
                content=content,
            )
            self._edits[edit_id] = edit
            self._edits_by_cs[changeset_id].append(edit_id)
            return edit

    # ------------------------------------------------------------------
    # Lifecycle transitions
    # ------------------------------------------------------------------

    def submit(self, changeset_id: str, now: Optional[float] = None) -> bool:
        """Transition draft → submitted."""
        with self._lock:
            cs = self._changesets.get(changeset_id)
            if cs is None or cs.status != "draft":
                return False
            cs.status = "submitted"
            cs.submitted_at = now if now is not None else time.time()
            return True

    def merge(self, changeset_id: str, now: Optional[float] = None) -> bool:
        """Transition submitted → merged."""
        with self._lock:
            cs = self._changesets.get(changeset_id)
            if cs is None or cs.status != "submitted":
                return False
            cs.status = "merged"
            cs.merged_at = now if now is not None else time.time()
            return True

    def discard(self, changeset_id: str) -> bool:
        """Discard a changeset from ``draft`` or ``submitted``."""
        with self._lock:
            cs = self._changesets.get(changeset_id)
            if cs is None or cs.status not in {"draft", "submitted"}:
                return False
            cs.status = "discarded"
            return True

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_changeset(self, changeset_id: str) -> Optional[Changeset]:
        with self._lock:
            return self._changesets.get(changeset_id)

    def get_edit(self, edit_id: int) -> Optional[ChangesetEdit]:
        with self._lock:
            return self._edits.get(edit_id)

    def edits_for_changeset(self, changeset_id: str) -> list[ChangesetEdit]:
        with self._lock:
            ids = self._edits_by_cs.get(changeset_id, [])
            edits = [self._edits[i] for i in ids if i in self._edits]
            return sorted(edits, key=lambda e: e.edit_id)

    def changesets_by_status(self, status: str) -> list[Changeset]:
        with self._lock:
            result = [cs for cs in self._changesets.values() if cs.status == status]
            return sorted(result, key=lambda c: c.created_at)

    def changesets_by_author(self, author: str) -> list[Changeset]:
        with self._lock:
            result = [cs for cs in self._changesets.values() if cs.author == author]
            return sorted(result, key=lambda c: c.created_at)

    def changesets_for_doc(self, doc_id: str) -> list[Changeset]:
        """Return changesets that have at least one edit on ``doc_id``."""
        with self._lock:
            seen: set[str] = set()
            result: list[Changeset] = []
            for edit in self._edits.values():
                if edit.doc_id != doc_id:
                    continue
                if edit.changeset_id in seen:
                    continue
                cs = self._changesets.get(edit.changeset_id)
                if cs is None:
                    continue
                seen.add(edit.changeset_id)
                result.append(cs)
            return sorted(result, key=lambda c: c.created_at)

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------

    def delete_changeset(self, changeset_id: str) -> bool:
        """Delete a changeset and all its edits."""
        with self._lock:
            if changeset_id not in self._changesets:
                return False
            edit_ids = self._edits_by_cs.pop(changeset_id, [])
            for eid in edit_ids:
                self._edits.pop(eid, None)
            self._changesets.pop(changeset_id, None)
            return True

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> ChangesetStats:
        with self._lock:
            draft = submitted = merged = discarded = 0
            for cs in self._changesets.values():
                if cs.status == "draft":
                    draft += 1
                elif cs.status == "submitted":
                    submitted += 1
                elif cs.status == "merged":
                    merged += 1
                elif cs.status == "discarded":
                    discarded += 1
            return ChangesetStats(
                total_changesets=len(self._changesets),
                draft_count=draft,
                submitted_count=submitted,
                merged_count=merged,
                discarded_count=discarded,
                total_edits=len(self._edits),
            )
