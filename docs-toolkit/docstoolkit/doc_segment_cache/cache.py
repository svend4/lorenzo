"""E353 DocSegmentCache — implementation."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Segment:
    """A single cached document segment."""

    doc_id: str
    segment_id: str
    content: str
    stored_at: float = 0.0
    byte_size: int = 0
    hit_count: int = 0


@dataclass
class SegmentStats:
    """Aggregate statistics across the cache."""

    total_segments: int
    unique_docs: int
    total_size_bytes: int
    total_hits: int


class DocSegmentCache:
    """Keyed cache for partial document data, indexed by (doc_id, segment_id)."""

    def __init__(self) -> None:
        self._segments: Dict[Tuple[str, str], Segment] = {}
        self._by_doc: Dict[str, Set[str]] = {}
        self._lock = threading.Lock()

    # ----- mutation -----

    def store(
        self,
        doc_id: str,
        segment_id: str,
        content: str,
        now: Optional[float] = None,
    ) -> Segment:
        """Create or replace a segment. Returns the stored Segment."""
        ts = now if now is not None else time.time()
        byte_size = len(content.encode("utf-8"))
        seg = Segment(
            doc_id=doc_id,
            segment_id=segment_id,
            content=content,
            stored_at=ts,
            byte_size=byte_size,
            hit_count=0,
        )
        key = (doc_id, segment_id)
        with self._lock:
            self._segments[key] = seg
            self._by_doc.setdefault(doc_id, set()).add(segment_id)
        return seg

    def delete(self, doc_id: str, segment_id: str) -> bool:
        """Remove a single segment. Returns True if it existed."""
        key = (doc_id, segment_id)
        with self._lock:
            if key not in self._segments:
                return False
            del self._segments[key]
            ids = self._by_doc.get(doc_id)
            if ids is not None:
                ids.discard(segment_id)
                if not ids:
                    del self._by_doc[doc_id]
            return True

    def delete_doc(self, doc_id: str) -> int:
        """Remove all segments belonging to doc_id. Returns count removed."""
        with self._lock:
            ids = self._by_doc.pop(doc_id, set())
            for sid in ids:
                self._segments.pop((doc_id, sid), None)
            return len(ids)

    def clear(self) -> int:
        """Remove all segments. Returns total count removed."""
        with self._lock:
            count = len(self._segments)
            self._segments.clear()
            self._by_doc.clear()
            return count

    # ----- reads -----

    def get(self, doc_id: str, segment_id: str) -> Optional[str]:
        """Return content of segment, incrementing hit_count. None if missing."""
        key = (doc_id, segment_id)
        with self._lock:
            seg = self._segments.get(key)
            if seg is None:
                return None
            seg.hit_count += 1
            return seg.content

    def peek(self, doc_id: str, segment_id: str) -> Optional[Segment]:
        """Return Segment object without modifying hit_count. None if missing."""
        key = (doc_id, segment_id)
        with self._lock:
            return self._segments.get(key)

    def exists(self, doc_id: str, segment_id: str) -> bool:
        with self._lock:
            return (doc_id, segment_id) in self._segments

    def segments_for_doc(self, doc_id: str) -> List[Segment]:
        """Return all segments for doc_id, sorted by segment_id."""
        with self._lock:
            ids = self._by_doc.get(doc_id, set())
            segs = [self._segments[(doc_id, sid)] for sid in ids]
        segs.sort(key=lambda s: s.segment_id)
        return segs

    def total_size_for_doc(self, doc_id: str) -> int:
        """Sum of byte_size across all segments of a doc. 0 if none."""
        with self._lock:
            ids = self._by_doc.get(doc_id, set())
            return sum(self._segments[(doc_id, sid)].byte_size for sid in ids)

    def most_accessed(self, limit: int = 10) -> List[Segment]:
        """Top segments sorted by hit_count desc, then (doc_id, segment_id) asc."""
        with self._lock:
            segs = list(self._segments.values())
        segs.sort(key=lambda s: (-s.hit_count, s.doc_id, s.segment_id))
        return segs[:limit]

    def all_doc_ids(self) -> List[str]:
        """Sorted unique doc IDs that currently have segments."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> SegmentStats:
        """Compute aggregate stats."""
        with self._lock:
            total_segments = len(self._segments)
            unique_docs = len(self._by_doc)
            total_size_bytes = sum(s.byte_size for s in self._segments.values())
            total_hits = sum(s.hit_count for s in self._segments.values())
        return SegmentStats(
            total_segments=total_segments,
            unique_docs=unique_docs,
            total_size_bytes=total_size_bytes,
            total_hits=total_hits,
        )
