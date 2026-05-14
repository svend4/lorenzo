"""DocVersioningIndex — fast in-memory lookup index of document versions.

Pure stdlib, thread-safe via :class:`threading.Lock`. All data is held in
plain dicts and sets, keyed by ``(doc_id, version)`` tuples.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class VersionRef:
    """Reference to a single doc version."""

    doc_id: str
    version: str
    tag: str = ""
    created_at: float = 0.0
    parent_version: Optional[str] = None


@dataclass
class VersioningStats:
    """Aggregate statistics for a :class:`DocVersioningIndex`."""

    total_versions: int
    unique_docs: int
    unique_tags: int


class DocVersioningIndex:
    """Fast lookup index over doc versions.

    Supports adding/removing versions, tagging, walking parent chains and
    listing child versions. All public methods are thread-safe.
    """

    def __init__(self) -> None:
        self._versions: Dict[Tuple[str, str], VersionRef] = {}
        self._by_doc: Dict[str, Set[str]] = {}
        self._by_tag: Dict[str, Set[Tuple[str, str]]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------
    def add_version(
        self,
        doc_id: str,
        version: str,
        tag: str = "",
        parent_version: Optional[str] = None,
        now: Optional[float] = None,
    ) -> VersionRef:
        """Add or replace a version entry. Returns the stored :class:`VersionRef`."""
        if now is None:
            now = time.time()
        key = (doc_id, version)
        with self._lock:
            # If replacing, drop old tag membership first.
            old = self._versions.get(key)
            if old is not None and old.tag:
                bucket = self._by_tag.get(old.tag)
                if bucket is not None:
                    bucket.discard(key)
                    if not bucket:
                        self._by_tag.pop(old.tag, None)

            ref = VersionRef(
                doc_id=doc_id,
                version=version,
                tag=tag,
                created_at=now,
                parent_version=parent_version,
            )
            self._versions[key] = ref
            self._by_doc.setdefault(doc_id, set()).add(version)
            if tag:
                self._by_tag.setdefault(tag, set()).add(key)
            return ref

    def remove_version(self, doc_id: str, version: str) -> bool:
        """Remove a version. Returns ``True`` if it existed."""
        key = (doc_id, version)
        with self._lock:
            ref = self._versions.pop(key, None)
            if ref is None:
                return False
            versions = self._by_doc.get(doc_id)
            if versions is not None:
                versions.discard(version)
                if not versions:
                    self._by_doc.pop(doc_id, None)
            if ref.tag:
                bucket = self._by_tag.get(ref.tag)
                if bucket is not None:
                    bucket.discard(key)
                    if not bucket:
                        self._by_tag.pop(ref.tag, None)
            return True

    def set_tag(self, doc_id: str, version: str, tag: str) -> bool:
        """Replace the tag of an existing version. Returns ``True`` if found."""
        key = (doc_id, version)
        with self._lock:
            ref = self._versions.get(key)
            if ref is None:
                return False
            if ref.tag:
                bucket = self._by_tag.get(ref.tag)
                if bucket is not None:
                    bucket.discard(key)
                    if not bucket:
                        self._by_tag.pop(ref.tag, None)
            ref.tag = tag
            if tag:
                self._by_tag.setdefault(tag, set()).add(key)
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove all versions of ``doc_id``. Returns count cleared."""
        with self._lock:
            versions = self._by_doc.pop(doc_id, None)
            if not versions:
                return 0
            count = 0
            for version in list(versions):
                key = (doc_id, version)
                ref = self._versions.pop(key, None)
                if ref is None:
                    continue
                count += 1
                if ref.tag:
                    bucket = self._by_tag.get(ref.tag)
                    if bucket is not None:
                        bucket.discard(key)
                        if not bucket:
                            self._by_tag.pop(ref.tag, None)
            return count

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------
    def get_version(self, doc_id: str, version: str) -> Optional[VersionRef]:
        """Return the :class:`VersionRef` for ``(doc_id, version)`` or ``None``."""
        with self._lock:
            return self._versions.get((doc_id, version))

    def versions_for_doc(self, doc_id: str) -> List[VersionRef]:
        """All versions of a doc, sorted by ``created_at`` ascending."""
        with self._lock:
            versions = self._by_doc.get(doc_id)
            if not versions:
                return []
            refs = [self._versions[(doc_id, v)] for v in versions]
        refs.sort(key=lambda r: (r.created_at, r.version))
        return refs

    def latest_version(self, doc_id: str) -> Optional[VersionRef]:
        """Return version with highest ``created_at`` for ``doc_id``."""
        refs = self.versions_for_doc(doc_id)
        if not refs:
            return None
        return refs[-1]

    def version_chain(self, doc_id: str, version: str) -> List[VersionRef]:
        """Walk the parent chain from ``version`` up to root.

        Result is ordered from the requested version to its root ancestor.
        Stops on missing parents or cycles. Returns empty list if the
        requested version is not in the index.
        """
        chain: List[VersionRef] = []
        seen: Set[str] = set()
        with self._lock:
            current: Optional[str] = version
            while current is not None and current not in seen:
                ref = self._versions.get((doc_id, current))
                if ref is None:
                    break
                chain.append(ref)
                seen.add(current)
                current = ref.parent_version
        return chain

    def versions_with_tag(self, tag: str) -> List[VersionRef]:
        """All versions carrying ``tag``, sorted by (doc_id, version)."""
        with self._lock:
            keys = self._by_tag.get(tag)
            if not keys:
                return []
            refs = [self._versions[k] for k in keys]
        refs.sort(key=lambda r: (r.doc_id, r.version))
        return refs

    def tags_of_doc(self, doc_id: str) -> List[str]:
        """Sorted unique non-empty tags used by versions of ``doc_id``."""
        with self._lock:
            versions = self._by_doc.get(doc_id)
            if not versions:
                return []
            tags = {self._versions[(doc_id, v)].tag for v in versions}
        return sorted(t for t in tags if t)

    def child_versions(self, doc_id: str, version: str) -> List[VersionRef]:
        """Versions whose ``parent_version == version``, sorted by ``created_at``."""
        with self._lock:
            versions = self._by_doc.get(doc_id)
            if not versions:
                return []
            children = [
                self._versions[(doc_id, v)]
                for v in versions
                if self._versions[(doc_id, v)].parent_version == version
            ]
        children.sort(key=lambda r: (r.created_at, r.version))
        return children

    def all_doc_ids(self) -> List[str]:
        """All known doc ids, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def all_tags(self) -> List[str]:
        """All known tags, sorted."""
        with self._lock:
            return sorted(self._by_tag.keys())

    def stats(self) -> VersioningStats:
        """Aggregate statistics."""
        with self._lock:
            return VersioningStats(
                total_versions=len(self._versions),
                unique_docs=len(self._by_doc),
                unique_tags=len(self._by_tag),
            )
