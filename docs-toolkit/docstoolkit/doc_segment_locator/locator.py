"""E386 DocSegmentLocator — locate segments by position within documents.

Pure stdlib implementation. Thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class Segment:
    """A single segment with a half-open range [start, end)."""

    segment_id: str
    doc_id: str
    start: int
    end: int
    label: str = ""
    metadata: dict = field(default_factory=dict)


@dataclass
class LocatorStats:
    """Aggregate statistics over all stored segments."""

    total_segments: int
    unique_docs: int
    total_length: int


class DocSegmentLocator:
    """Locate segments by position, range, or label within documents."""

    def __init__(self) -> None:
        self._segments: Dict[Tuple[str, str], Segment] = {}
        self._by_doc: Dict[str, List[str]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # registration / removal
    # ------------------------------------------------------------------
    def register_segment(
        self,
        doc_id: str,
        segment_id: str,
        start: int,
        end: int,
        label: str = "",
        metadata: Optional[dict] = None,
    ) -> Segment:
        """Register a new segment.

        Raises
        ------
        ValueError
            If ``start < 0`` or ``end <= start``.
        """

        if start < 0:
            raise ValueError(f"start must be >= 0, got {start}")
        if end <= start:
            raise ValueError(f"end must be > start, got start={start}, end={end}")

        seg = Segment(
            segment_id=segment_id,
            doc_id=doc_id,
            start=start,
            end=end,
            label=label,
            metadata=dict(metadata) if metadata else {},
        )
        key = (doc_id, segment_id)
        with self._lock:
            if key not in self._segments:
                self._by_doc.setdefault(doc_id, []).append(segment_id)
            self._segments[key] = seg
        return seg

    def remove_segment(self, doc_id: str, segment_id: str) -> bool:
        """Remove a segment. Returns True if removed."""

        key = (doc_id, segment_id)
        with self._lock:
            if key not in self._segments:
                return False
            del self._segments[key]
            ids = self._by_doc.get(doc_id, [])
            if segment_id in ids:
                ids.remove(segment_id)
            if not ids and doc_id in self._by_doc:
                del self._by_doc[doc_id]
            return True

    def get_segment(self, doc_id: str, segment_id: str) -> Optional[Segment]:
        """Return the segment or None if missing."""

        with self._lock:
            return self._segments.get((doc_id, segment_id))

    # ------------------------------------------------------------------
    # queries
    # ------------------------------------------------------------------
    def _doc_segments(self, doc_id: str) -> List[Segment]:
        ids = self._by_doc.get(doc_id, [])
        return [self._segments[(doc_id, sid)] for sid in ids]

    def segments_for_doc(self, doc_id: str) -> List[Segment]:
        """All segments for ``doc_id`` sorted by start."""

        with self._lock:
            segs = self._doc_segments(doc_id)
        return sorted(segs, key=lambda s: (s.start, s.end, s.segment_id))

    def segments_at(self, doc_id: str, position: int) -> List[Segment]:
        """Segments where ``start <= position < end``, sorted by start."""

        with self._lock:
            segs = [s for s in self._doc_segments(doc_id) if s.start <= position < s.end]
        return sorted(segs, key=lambda s: (s.start, s.end, s.segment_id))

    def segments_in_range(self, doc_id: str, start: int, end: int) -> List[Segment]:
        """Segments that overlap the half-open range [start, end)."""

        with self._lock:
            segs = [
                s
                for s in self._doc_segments(doc_id)
                if s.start < end and s.end > start
            ]
        return sorted(segs, key=lambda s: (s.start, s.end, s.segment_id))

    def segments_by_label(self, doc_id: str, label: str) -> List[Segment]:
        """Segments with exact label match, sorted by start."""

        with self._lock:
            segs = [s for s in self._doc_segments(doc_id) if s.label == label]
        return sorted(segs, key=lambda s: (s.start, s.end, s.segment_id))

    def find_overlapping(self, doc_id: str) -> List[Tuple[Segment, Segment]]:
        """Return deduplicated overlapping pairs within ``doc_id``."""

        with self._lock:
            segs = sorted(
                self._doc_segments(doc_id),
                key=lambda s: (s.start, s.end, s.segment_id),
            )
        pairs: List[Tuple[Segment, Segment]] = []
        for i, a in enumerate(segs):
            for b in segs[i + 1 :]:
                if b.start >= a.end:
                    continue
                if a.start < b.end and a.end > b.start:
                    pairs.append((a, b))
        return pairs

    # ------------------------------------------------------------------
    # mutations
    # ------------------------------------------------------------------
    def clear_doc(self, doc_id: str) -> int:
        """Remove all segments for ``doc_id``. Returns count cleared."""

        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
            for sid in ids:
                self._segments.pop((doc_id, sid), None)
            if doc_id in self._by_doc:
                del self._by_doc[doc_id]
            return len(ids)

    def merge_adjacent(self, doc_id: str, label: str) -> int:
        """Merge same-label segments where ``end`` of one equals ``start`` of next.

        Returns the number of merges performed.
        """

        merges = 0
        with self._lock:
            segs = sorted(
                [s for s in self._doc_segments(doc_id) if s.label == label],
                key=lambda s: (s.start, s.end, s.segment_id),
            )
            i = 0
            while i < len(segs) - 1:
                cur = segs[i]
                nxt = segs[i + 1]
                if cur.end == nxt.start:
                    # extend cur, drop nxt
                    cur.end = nxt.end
                    # remove nxt from storage
                    self._segments.pop((doc_id, nxt.segment_id), None)
                    ids = self._by_doc.get(doc_id, [])
                    if nxt.segment_id in ids:
                        ids.remove(nxt.segment_id)
                    segs.pop(i + 1)
                    merges += 1
                    # do not advance i; cur may merge with new next
                else:
                    i += 1
        return merges

    def total_coverage(self, doc_id: str) -> int:
        """Sum of unique covered positions across all segments of ``doc_id``."""

        with self._lock:
            ranges = [(s.start, s.end) for s in self._doc_segments(doc_id)]
        if not ranges:
            return 0
        ranges.sort()
        covered = 0
        cur_start, cur_end = ranges[0]
        for start, end in ranges[1:]:
            if start <= cur_end:
                if end > cur_end:
                    cur_end = end
            else:
                covered += cur_end - cur_start
                cur_start, cur_end = start, end
        covered += cur_end - cur_start
        return covered

    def all_doc_ids(self) -> List[str]:
        """Sorted list of document ids that have segments."""

        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> LocatorStats:
        """Aggregate statistics."""

        with self._lock:
            total = len(self._segments)
            docs = len(self._by_doc)
            length = sum(s.end - s.start for s in self._segments.values())
        return LocatorStats(total_segments=total, unique_docs=docs, total_length=length)
