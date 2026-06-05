"""DocLinkAnchor — named anchors within documents.

A purely in-memory implementation backed by simple ``dict`` indexes
and protected by a ``threading.Lock``.  No third-party dependencies.

Each anchor identifies a named location inside a document (for example
``"section-1"`` or ``"intro"``) at a particular ``position`` (typically
a line number or character offset).  The manager supports creation,
lookup, link resolution (with use counting) and per-document queries.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class Anchor:
    """A single named anchor inside a document."""

    doc_id: str
    anchor_id: str
    position: int
    title: str = ""
    created_at: float = 0.0


@dataclass
class AnchorStats:
    """Aggregate statistics for the anchor store."""

    total_anchors: int
    unique_docs: int
    total_uses: int


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocLinkAnchor:
    """Thread-safe in-memory store for document anchors."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # (doc_id, anchor_id) -> Anchor
        self._anchors: dict[tuple[str, str], Anchor] = {}
        # doc_id -> set of anchor_ids
        self._by_doc: dict[str, set[str]] = {}
        # (doc_id, anchor_id) -> use count
        self._use_counts: dict[tuple[str, str], int] = {}

    # ---- helpers --------------------------------------------------------

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    # ---- mutation -------------------------------------------------------

    def register(
        self,
        doc_id: str,
        anchor_id: str,
        position: int,
        title: str = "",
        now: Optional[float] = None,
    ) -> Anchor:
        """Create or replace an anchor and return it."""
        ts = self._now(now)
        key = (doc_id, anchor_id)
        with self._lock:
            anchor = Anchor(
                doc_id=doc_id,
                anchor_id=anchor_id,
                position=position,
                title=title,
                created_at=ts,
            )
            self._anchors[key] = anchor
            self._by_doc.setdefault(doc_id, set()).add(anchor_id)
            # Replacing an existing anchor preserves its use count;
            # registering a brand-new anchor starts at zero.
            self._use_counts.setdefault(key, 0)
            return anchor

    def unregister(self, doc_id: str, anchor_id: str) -> bool:
        """Remove an anchor; return True iff it existed."""
        key = (doc_id, anchor_id)
        with self._lock:
            if key not in self._anchors:
                return False
            del self._anchors[key]
            self._use_counts.pop(key, None)
            anchors = self._by_doc.get(doc_id)
            if anchors is not None:
                anchors.discard(anchor_id)
                if not anchors:
                    del self._by_doc[doc_id]
            return True

    def clear_doc(self, doc_id: str) -> int:
        """Remove every anchor of ``doc_id`` and return the count cleared."""
        with self._lock:
            anchors = self._by_doc.pop(doc_id, None)
            if not anchors:
                return 0
            count = 0
            for anchor_id in list(anchors):
                key = (doc_id, anchor_id)
                if key in self._anchors:
                    del self._anchors[key]
                    count += 1
                self._use_counts.pop(key, None)
            return count

    # ---- lookups --------------------------------------------------------

    def get(self, doc_id: str, anchor_id: str) -> Optional[Anchor]:
        """Return the anchor or ``None`` without touching its use counter."""
        with self._lock:
            return self._anchors.get((doc_id, anchor_id))

    def resolve_link(
        self, doc_id: str, anchor_id: str
    ) -> Optional[Anchor]:
        """Like :meth:`get` but also increments the use counter."""
        key = (doc_id, anchor_id)
        with self._lock:
            anchor = self._anchors.get(key)
            if anchor is None:
                return None
            self._use_counts[key] = self._use_counts.get(key, 0) + 1
            return anchor

    def anchors_for_doc(self, doc_id: str) -> list[Anchor]:
        """Return all anchors of ``doc_id`` sorted by position (ascending)."""
        with self._lock:
            anchor_ids = self._by_doc.get(doc_id)
            if not anchor_ids:
                return []
            items = [
                self._anchors[(doc_id, aid)]
                for aid in anchor_ids
                if (doc_id, aid) in self._anchors
            ]
            items.sort(key=lambda a: (a.position, a.anchor_id))
            return items

    def anchor_at_position(
        self, doc_id: str, position: int
    ) -> Optional[Anchor]:
        """Return the anchor at the exact ``position`` (or ``None``)."""
        with self._lock:
            anchor_ids = self._by_doc.get(doc_id)
            if not anchor_ids:
                return None
            for aid in anchor_ids:
                anchor = self._anchors.get((doc_id, aid))
                if anchor is not None and anchor.position == position:
                    return anchor
            return None

    # ---- usage ----------------------------------------------------------

    def use_count(self, doc_id: str, anchor_id: str) -> int:
        """Return the resolved-link counter for the anchor (0 if missing)."""
        with self._lock:
            return self._use_counts.get((doc_id, anchor_id), 0)

    def most_used(
        self, limit: int = 10
    ) -> list[tuple[tuple[str, str], int]]:
        """Return ``[((doc_id, anchor_id), count), ...]`` sorted desc.

        Only anchors with at least one resolution are reported.
        """
        with self._lock:
            items = [
                (key, count)
                for key, count in self._use_counts.items()
                if count > 0 and key in self._anchors
            ]
            items.sort(key=lambda kv: (-kv[1], kv[0]))
            if limit is not None and limit >= 0:
                items = items[:limit]
            return items

    # ---- aggregates -----------------------------------------------------

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of doc ids that currently hold anchors."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> AnchorStats:
        """Return aggregate statistics over the whole store."""
        with self._lock:
            return AnchorStats(
                total_anchors=len(self._anchors),
                unique_docs=len(self._by_doc),
                total_uses=sum(self._use_counts.values()),
            )
