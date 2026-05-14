"""DocAnchorIndex implementation — inverted index over (doc_id, anchor) entries.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class AnchorRef:
    """A single anchor reference attached to a document."""

    doc_id: str
    anchor: str
    keywords: List[str] = field(default_factory=list)
    added_at: float = 0.0


@dataclass
class AnchorStats:
    """Aggregate statistics for the anchor index."""

    total_anchors: int
    unique_docs: int
    unique_keywords: int


class DocAnchorIndex:
    """Inverted index over ``(doc_id, anchor)`` entries with keyword lookup.

    Thread-safe — every public mutating or reading method acquires an
    internal :class:`threading.Lock`.
    """

    def __init__(self) -> None:
        # (doc_id, anchor) → AnchorRef
        self._anchors: Dict[Tuple[str, str], AnchorRef] = {}
        # keyword (lowercased) → set of (doc_id, anchor)
        self._by_keyword: Dict[str, Set[Tuple[str, str]]] = {}
        # doc_id → set of anchors
        self._by_doc: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    # ----------------------------------------------------------------- helpers

    @staticmethod
    def _normalize_keywords(keywords: Optional[List[str]]) -> List[str]:
        """Lowercase, strip, and dedupe (preserving order)."""
        if not keywords:
            return []
        seen: Set[str] = set()
        result: List[str] = []
        for kw in keywords:
            if not isinstance(kw, str):
                continue
            normalized = kw.strip().lower()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            result.append(normalized)
        return result

    def _unindex_keywords(
        self, key: Tuple[str, str], keywords: List[str]
    ) -> None:
        """Remove ``key`` from every keyword bucket in ``keywords``."""
        for kw in keywords:
            bucket = self._by_keyword.get(kw)
            if bucket is None:
                continue
            bucket.discard(key)
            if not bucket:
                self._by_keyword.pop(kw, None)

    def _index_keywords(
        self, key: Tuple[str, str], keywords: List[str]
    ) -> None:
        for kw in keywords:
            self._by_keyword.setdefault(kw, set()).add(key)

    # ------------------------------------------------------------------ writes

    def add_anchor(
        self,
        doc_id: str,
        anchor: str,
        keywords: Optional[List[str]] = None,
        now: Optional[float] = None,
    ) -> AnchorRef:
        """Create or replace an anchor.

        ``keywords`` are normalized to lowercase, trimmed and deduplicated.
        If ``now`` is ``None``, :func:`time.time` is called.
        """
        normalized = self._normalize_keywords(keywords)
        ts = time.time() if now is None else now
        key = (doc_id, anchor)
        with self._lock:
            existing = self._anchors.get(key)
            if existing is not None:
                self._unindex_keywords(key, existing.keywords)
            ref = AnchorRef(
                doc_id=doc_id,
                anchor=anchor,
                keywords=list(normalized),
                added_at=ts,
            )
            self._anchors[key] = ref
            self._by_doc.setdefault(doc_id, set()).add(anchor)
            self._index_keywords(key, normalized)
            return ref

    def remove_anchor(self, doc_id: str, anchor: str) -> bool:
        """Remove a single anchor.

        Returns ``True`` if something was removed, ``False`` otherwise.
        """
        key = (doc_id, anchor)
        with self._lock:
            ref = self._anchors.pop(key, None)
            if ref is None:
                return False
            self._unindex_keywords(key, ref.keywords)
            anchors = self._by_doc.get(doc_id)
            if anchors is not None:
                anchors.discard(anchor)
                if not anchors:
                    self._by_doc.pop(doc_id, None)
            return True

    def update_keywords(
        self, doc_id: str, anchor: str, keywords: List[str]
    ) -> bool:
        """Replace the keyword list for an existing anchor.

        Returns ``True`` if the anchor exists, ``False`` otherwise.
        """
        key = (doc_id, anchor)
        normalized = self._normalize_keywords(keywords)
        with self._lock:
            ref = self._anchors.get(key)
            if ref is None:
                return False
            self._unindex_keywords(key, ref.keywords)
            ref.keywords = list(normalized)
            self._index_keywords(key, normalized)
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove every anchor for ``doc_id``.

        Returns the number of anchors removed.
        """
        with self._lock:
            anchors = self._by_doc.pop(doc_id, None)
            if not anchors:
                return 0
            removed = 0
            for anchor in list(anchors):
                key = (doc_id, anchor)
                ref = self._anchors.pop(key, None)
                if ref is None:
                    continue
                self._unindex_keywords(key, ref.keywords)
                removed += 1
            return removed

    def clear_keyword(self, keyword: str) -> int:
        """Strip ``keyword`` from every anchor that carries it.

        Returns the number of anchors affected.
        """
        if not isinstance(keyword, str):
            return 0
        kw = keyword.strip().lower()
        if not kw:
            return 0
        with self._lock:
            bucket = self._by_keyword.pop(kw, None)
            if not bucket:
                return 0
            affected = 0
            for key in bucket:
                ref = self._anchors.get(key)
                if ref is None:
                    continue
                if kw in ref.keywords:
                    ref.keywords = [k for k in ref.keywords if k != kw]
                    affected += 1
            return affected

    # ------------------------------------------------------------------- reads

    def get_anchor(self, doc_id: str, anchor: str) -> Optional[AnchorRef]:
        """Return the :class:`AnchorRef` for ``(doc_id, anchor)`` or ``None``."""
        with self._lock:
            ref = self._anchors.get((doc_id, anchor))
            if ref is None:
                return None
            return AnchorRef(
                doc_id=ref.doc_id,
                anchor=ref.anchor,
                keywords=list(ref.keywords),
                added_at=ref.added_at,
            )

    def find_by_keyword(self, keyword: str) -> List[AnchorRef]:
        """Return anchors carrying ``keyword``, sorted by ``(doc_id, anchor)``.

        Lookup is case-insensitive.
        """
        if not isinstance(keyword, str):
            return []
        kw = keyword.strip().lower()
        if not kw:
            return []
        with self._lock:
            bucket = self._by_keyword.get(kw)
            if not bucket:
                return []
            refs = [self._anchors[key] for key in bucket if key in self._anchors]
            refs.sort(key=lambda r: (r.doc_id, r.anchor))
            return [
                AnchorRef(
                    doc_id=r.doc_id,
                    anchor=r.anchor,
                    keywords=list(r.keywords),
                    added_at=r.added_at,
                )
                for r in refs
            ]

    def find_by_keywords(
        self, keywords: List[str], all_match: bool = False
    ) -> List[AnchorRef]:
        """Return anchors matching ``keywords``.

        If ``all_match`` is ``True``, only anchors that carry **every** keyword
        are returned (AND). Otherwise anchors carrying **any** of the keywords
        are returned (OR). Results are sorted by ``(doc_id, anchor)``.
        """
        normalized = self._normalize_keywords(keywords)
        if not normalized:
            return []
        with self._lock:
            buckets: List[Set[Tuple[str, str]]] = []
            for kw in normalized:
                bucket = self._by_keyword.get(kw)
                if bucket is None:
                    if all_match:
                        return []
                    continue
                buckets.append(bucket)
            if not buckets:
                return []
            if all_match:
                keys = set(buckets[0])
                for b in buckets[1:]:
                    keys &= b
                    if not keys:
                        return []
            else:
                keys = set()
                for b in buckets:
                    keys |= b
            refs = [self._anchors[k] for k in keys if k in self._anchors]
            refs.sort(key=lambda r: (r.doc_id, r.anchor))
            return [
                AnchorRef(
                    doc_id=r.doc_id,
                    anchor=r.anchor,
                    keywords=list(r.keywords),
                    added_at=r.added_at,
                )
                for r in refs
            ]

    def anchors_for_doc(self, doc_id: str) -> List[AnchorRef]:
        """Return all anchors for ``doc_id``, sorted by ``anchor``."""
        with self._lock:
            anchors = self._by_doc.get(doc_id)
            if not anchors:
                return []
            refs = [self._anchors[(doc_id, a)] for a in anchors]
            refs.sort(key=lambda r: r.anchor)
            return [
                AnchorRef(
                    doc_id=r.doc_id,
                    anchor=r.anchor,
                    keywords=list(r.keywords),
                    added_at=r.added_at,
                )
                for r in refs
            ]

    def keywords_of(self, doc_id: str, anchor: str) -> List[str]:
        """Return sorted keywords of ``(doc_id, anchor)``.

        Empty list if anchor does not exist.
        """
        with self._lock:
            ref = self._anchors.get((doc_id, anchor))
            if ref is None:
                return []
            return sorted(ref.keywords)

    def all_doc_ids(self) -> List[str]:
        """Return all known doc_ids, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def all_keywords(self) -> List[str]:
        """Return all known keywords, sorted."""
        with self._lock:
            return sorted(self._by_keyword.keys())

    def stats(self) -> AnchorStats:
        """Return aggregate index statistics."""
        with self._lock:
            return AnchorStats(
                total_anchors=len(self._anchors),
                unique_docs=len(self._by_doc),
                unique_keywords=len(self._by_keyword),
            )
