"""E407 DocVersionDiff implementation.

Stores document versions and computes diffs between any two versions of the
same document. Pure stdlib (``difflib``, ``threading``, ``time``,
``dataclasses``). Thread-safe via a single :class:`threading.Lock`.
"""
from __future__ import annotations

import difflib
import threading
import time
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class VersionContent:
    """Content of a single document version."""

    doc_id: str
    version: str
    content: str
    created_at: float = 0.0


@dataclass
class DiffSummary:
    """Summary of differences between two versions."""

    doc_id: str
    from_version: str
    to_version: str
    added_lines: int
    removed_lines: int
    changed_lines: int
    unified_diff: str = ""
    similarity: float = 0.0


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class DocVersionDiff:
    """Storage and diff computation for document versions."""

    def __init__(self) -> None:
        self._versions: dict[tuple[str, str], VersionContent] = {}
        self._by_doc: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ store

    def store_version(
        self,
        doc_id: str,
        version: str,
        content: str,
        now: Optional[float] = None,
    ) -> VersionContent:
        """Store (or overwrite) a version's content. Returns the stored value."""
        ts = time.time() if now is None else now
        vc = VersionContent(
            doc_id=doc_id, version=version, content=content, created_at=ts
        )
        with self._lock:
            self._versions[(doc_id, version)] = vc
            self._by_doc.setdefault(doc_id, set()).add(version)
        return vc

    def get_version(self, doc_id: str, version: str) -> Optional[VersionContent]:
        """Return stored content or ``None`` if missing."""
        with self._lock:
            return self._versions.get((doc_id, version))

    def versions_for(self, doc_id: str) -> list[str]:
        """Return sorted list of known versions for ``doc_id``."""
        with self._lock:
            return sorted(self._by_doc.get(doc_id, set()))

    def delete_version(self, doc_id: str, version: str) -> bool:
        """Delete a single version. Returns True if it existed."""
        with self._lock:
            key = (doc_id, version)
            if key not in self._versions:
                return False
            del self._versions[key]
            vs = self._by_doc.get(doc_id)
            if vs is not None:
                vs.discard(version)
                if not vs:
                    del self._by_doc[doc_id]
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove all versions of a document. Returns count removed."""
        with self._lock:
            versions = list(self._by_doc.get(doc_id, set()))
            count = 0
            for v in versions:
                if self._versions.pop((doc_id, v), None) is not None:
                    count += 1
            self._by_doc.pop(doc_id, None)
            return count

    def all_doc_ids(self) -> list[str]:
        """Return a sorted list of all known doc ids."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def latest_version_for(self, doc_id: str) -> Optional[str]:
        """Return the version with the highest ``created_at`` for the doc."""
        with self._lock:
            versions = self._by_doc.get(doc_id)
            if not versions:
                return None
            best_v: Optional[str] = None
            best_ts = float("-inf")
            for v in versions:
                vc = self._versions.get((doc_id, v))
                if vc is None:
                    continue
                if vc.created_at > best_ts:
                    best_ts = vc.created_at
                    best_v = v
            return best_v

    # ------------------------------------------------------------------ diff

    def compute_diff(
        self,
        doc_id: str,
        from_version: str,
        to_version: str,
    ) -> Optional[DiffSummary]:
        """Compute diff between two stored versions.

        Returns ``None`` if either version is missing.
        """
        with self._lock:
            a = self._versions.get((doc_id, from_version))
            b = self._versions.get((doc_id, to_version))
        if a is None or b is None:
            return None

        old_lines = a.content.splitlines()
        new_lines = b.content.splitlines()

        unified = "\n".join(
            difflib.unified_diff(
                old_lines,
                new_lines,
                fromfile=f"{doc_id}@{from_version}",
                tofile=f"{doc_id}@{to_version}",
                lineterm="",
            )
        )

        added = 0
        removed = 0
        changed = 0
        # Count by walking unified diff lines, skipping headers/hunks.
        prev_sign: Optional[str] = None
        for line in unified.splitlines():
            if not line:
                prev_sign = None
                continue
            if line.startswith("+++") or line.startswith("---"):
                prev_sign = None
                continue
            if line.startswith("@@"):
                prev_sign = None
                continue
            if line.startswith("+"):
                added += 1
                if prev_sign == "-":
                    changed += 1
                prev_sign = "+"
            elif line.startswith("-"):
                removed += 1
                if prev_sign == "+":
                    changed += 1
                prev_sign = "-"
            else:
                prev_sign = None

        similarity = difflib.SequenceMatcher(
            a=a.content, b=b.content, autojunk=False
        ).ratio()

        return DiffSummary(
            doc_id=doc_id,
            from_version=from_version,
            to_version=to_version,
            added_lines=added,
            removed_lines=removed,
            changed_lines=changed,
            unified_diff=unified,
            similarity=similarity,
        )

    def compute_diff_to_latest(
        self, doc_id: str, from_version: str
    ) -> Optional[DiffSummary]:
        """Diff from ``from_version`` to the latest-stored version of ``doc_id``."""
        latest = self.latest_version_for(doc_id)
        if latest is None:
            return None
        return self.compute_diff(doc_id, from_version, latest)

    # ------------------------------------------------------------------ stats

    def stats(self) -> dict:
        """Return aggregate stats about stored versions."""
        with self._lock:
            total_versions = len(self._versions)
            unique_docs = len(self._by_doc)
            total_chars = sum(len(vc.content) for vc in self._versions.values())
            return {
                "total_versions": total_versions,
                "unique_docs": unique_docs,
                "total_content_chars": total_chars,
            }
