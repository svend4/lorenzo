"""DocSnapshotManager — pure-stdlib, thread-safe point-in-time document snapshots."""

from __future__ import annotations

import difflib
import threading
import time
from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4


@dataclass
class Snapshot:
    """A single point-in-time capture of a document."""

    snapshot_id: str        # auto-generated: f"snap_{uuid4().hex[:12]}"
    doc_id: str
    version: int            # per-doc auto-increment starting at 1
    content: str
    metadata: dict
    created_at: float
    label: str = ""         # optional human label


@dataclass
class SnapshotDiff:
    """Diff between two versions of the same document."""

    doc_id: str
    from_version: int
    to_version: int
    lines_added: int
    lines_removed: int
    diff_lines: list[str]   # unified diff lines


@dataclass
class SnapshotStats:
    """Aggregate statistics across the manager."""

    total_snapshots: int
    total_docs: int
    avg_versions_per_doc: float


class DocSnapshotManager:
    """Thread-safe in-memory manager for document snapshots.

    Each call to :meth:`take` stores a new ``Snapshot`` for *doc_id* with an
    auto-incrementing version number (per document, starting at 1).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # doc_id -> list[Snapshot] in insertion order (version ascending)
        self._store: dict[str, list[Snapshot]] = {}
        # snapshot_id -> Snapshot (for O(1) lookup)
        self._by_id: dict[str, Snapshot] = {}

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def take(
        self,
        doc_id: str,
        content: str,
        metadata: dict | None = None,
        label: str = "",
        now: Optional[float] = None,
    ) -> Snapshot:
        """Create a new snapshot for *doc_id*.

        The *version* field is the next integer for this document (1-based).
        *metadata* defaults to an empty dict when not provided.
        *now* overrides the timestamp (useful in tests).
        """
        if metadata is None:
            metadata = {}
        created_at = now if now is not None else time.time()
        with self._lock:
            existing = self._store.setdefault(doc_id, [])
            version = len(existing) + 1
            snap = Snapshot(
                snapshot_id=f"snap_{uuid4().hex[:12]}",
                doc_id=doc_id,
                version=version,
                content=content,
                metadata=dict(metadata),
                created_at=created_at,
                label=label,
            )
            existing.append(snap)
            self._by_id[snap.snapshot_id] = snap
        return snap

    def restore(
        self,
        doc_id: str,
        version: int,
        now: Optional[float] = None,
    ) -> Optional[Snapshot]:
        """Create a new snapshot whose content is copied from *version*.

        Returns ``None`` if *version* does not exist for *doc_id*.
        """
        source = self.get_version(doc_id, version)
        if source is None:
            return None
        return self.take(
            doc_id=doc_id,
            content=source.content,
            metadata=dict(source.metadata),
            label=f"restore_v{version}",
            now=now,
        )

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get(self, snapshot_id: str) -> Optional[Snapshot]:
        """Return a snapshot by its unique *snapshot_id*, or ``None``."""
        with self._lock:
            return self._by_id.get(snapshot_id)

    def get_version(self, doc_id: str, version: int) -> Optional[Snapshot]:
        """Return the snapshot at *version* for *doc_id*, or ``None``."""
        with self._lock:
            snaps = self._store.get(doc_id, [])
            # versions are 1-based and contiguous *unless* some were deleted;
            # do a linear scan to be safe after deletions.
            for s in snaps:
                if s.version == version:
                    return s
            return None

    def latest(self, doc_id: str) -> Optional[Snapshot]:
        """Return the most recent snapshot for *doc_id*, or ``None``."""
        with self._lock:
            snaps = self._store.get(doc_id, [])
            return snaps[-1] if snaps else None

    def history(self, doc_id: str, limit: int | None = None) -> list[Snapshot]:
        """Return snapshots for *doc_id* sorted newest-first.

        *limit* caps the number of results when provided.
        """
        with self._lock:
            snaps = list(reversed(self._store.get(doc_id, [])))
        if limit is not None:
            snaps = snaps[:limit]
        return snaps

    # ------------------------------------------------------------------
    # Diff
    # ------------------------------------------------------------------

    def diff(
        self,
        doc_id: str,
        from_version: int,
        to_version: int,
    ) -> Optional[SnapshotDiff]:
        """Compute a unified diff between two versions.

        Returns ``None`` if either version doesn't exist for *doc_id*.

        *lines_added* counts lines in the diff that start with ``'+'`` but
        **not** ``'++'+'+'``.  *lines_removed* is the equivalent for ``'-'``.
        """
        snap_a = self.get_version(doc_id, from_version)
        snap_b = self.get_version(doc_id, to_version)
        if snap_a is None or snap_b is None:
            return None

        lines_a = snap_a.content.splitlines(keepends=True)
        lines_b = snap_b.content.splitlines(keepends=True)
        diff = list(
            difflib.unified_diff(
                lines_a,
                lines_b,
                fromfile=f"v{from_version}",
                tofile=f"v{to_version}",
            )
        )
        lines_added = sum(
            1 for ln in diff if ln.startswith("+") and not ln.startswith("+++")
        )
        lines_removed = sum(
            1 for ln in diff if ln.startswith("-") and not ln.startswith("---")
        )
        return SnapshotDiff(
            doc_id=doc_id,
            from_version=from_version,
            to_version=to_version,
            lines_added=lines_added,
            lines_removed=lines_removed,
            diff_lines=diff,
        )

    # ------------------------------------------------------------------
    # Delete / prune
    # ------------------------------------------------------------------

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete a single snapshot by *snapshot_id*.

        Returns ``True`` if the snapshot existed and was removed.
        """
        with self._lock:
            snap = self._by_id.pop(snapshot_id, None)
            if snap is None:
                return False
            doc_snaps = self._store.get(snap.doc_id, [])
            try:
                doc_snaps.remove(snap)
            except ValueError:
                pass
            if not doc_snaps:
                self._store.pop(snap.doc_id, None)
        return True

    def delete_doc_snapshots(self, doc_id: str) -> int:
        """Delete all snapshots for *doc_id*.

        Returns the number of snapshots removed.
        """
        with self._lock:
            snaps = self._store.pop(doc_id, [])
            for s in snaps:
                self._by_id.pop(s.snapshot_id, None)
        return len(snaps)

    def prune(self, doc_id: str, keep_last: int) -> int:
        """Keep only the *keep_last* newest snapshots for *doc_id*.

        Returns the number of snapshots removed.
        """
        if keep_last < 0:
            keep_last = 0
        with self._lock:
            snaps = self._store.get(doc_id, [])
            to_remove = snaps[:-keep_last] if keep_last > 0 else list(snaps)
            for s in to_remove:
                self._by_id.pop(s.snapshot_id, None)
            if keep_last > 0:
                self._store[doc_id] = snaps[len(to_remove):]
            else:
                self._store.pop(doc_id, None)
        return len(to_remove)

    # ------------------------------------------------------------------
    # Stats / properties
    # ------------------------------------------------------------------

    def stats(self) -> SnapshotStats:
        """Return aggregate statistics for the manager."""
        with self._lock:
            total_docs = len(self._store)
            total_snapshots = sum(len(v) for v in self._store.values())
        avg = total_snapshots / total_docs if total_docs > 0 else 0.0
        return SnapshotStats(
            total_snapshots=total_snapshots,
            total_docs=total_docs,
            avg_versions_per_doc=avg,
        )

    @property
    def total_snapshots(self) -> int:
        """Total number of snapshots currently stored."""
        with self._lock:
            return sum(len(v) for v in self._store.values())
