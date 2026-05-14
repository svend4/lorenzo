"""E315 DocLinkGraph — directed hyperlink graph between documents.

Pure stdlib. Thread-safe via :class:`threading.Lock`. Dataclasses throughout.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DocLink:
    """A directed link from one document to another."""

    from_doc: str
    to_doc: str
    anchor: str = ""
    link_type: str = "internal"
    added_at: float = 0.0


@dataclass
class LinkGraphStats:
    """Aggregate statistics about the link graph."""

    total_links: int
    unique_sources: int   # docs that have at least one outgoing link
    unique_targets: int   # docs that receive at least one incoming link
    orphan_count: int     # isolated nodes: added via add_node with no in/out links


class DocLinkGraph:
    """Directed hyperlink graph between documents.

    Internal storage
    ----------------
    _links  : dict[(from_doc, to_doc), DocLink]  — one link per ordered pair
    _out    : dict[str, set[str]]                — from_doc  → set of to_doc
    _in     : dict[str, set[str]]                — to_doc    → set of from_doc
    _nodes  : set[str]                           — all known doc IDs
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._links: dict[tuple, DocLink] = {}
        self._out: dict[str, set[str]] = {}
        self._in: dict[str, set[str]] = {}
        self._nodes: set[str] = set()

    # ------------------------------------------------------------------
    # Nodes
    # ------------------------------------------------------------------

    def add_node(self, doc_id: str) -> None:
        """Register a document node without any links. No-op if already present."""
        with self._lock:
            self._ensure_node(doc_id)

    def remove_node(self, doc_id: str) -> int:
        """Remove a document and all its incoming + outgoing links.

        Returns the number of links that were removed.
        """
        with self._lock:
            if doc_id not in self._nodes:
                return 0

            removed = 0

            # collect pairs to delete
            pairs_to_remove: list[tuple[str, str]] = []

            for to_doc in list(self._out.get(doc_id, set())):
                pairs_to_remove.append((doc_id, to_doc))

            for from_doc in list(self._in.get(doc_id, set())):
                pairs_to_remove.append((from_doc, doc_id))

            # deduplicate (self-loop would appear in both)
            seen: set[tuple] = set()
            for pair in pairs_to_remove:
                if pair not in seen:
                    seen.add(pair)
                    self._remove_link_unsafe(*pair)
                    removed += 1

            # remove node itself
            self._nodes.discard(doc_id)
            self._out.pop(doc_id, None)
            self._in.pop(doc_id, None)

            return removed

    def all_nodes(self) -> list[str]:
        """Return sorted list of all known document IDs."""
        with self._lock:
            return sorted(self._nodes)

    # ------------------------------------------------------------------
    # Links
    # ------------------------------------------------------------------

    def add_link(
        self,
        from_doc: str,
        to_doc: str,
        anchor: str = "",
        link_type: str = "internal",
        now: Optional[float] = None,
    ) -> DocLink:
        """Add or update the link from_doc → to_doc.

        Re-adding an existing pair updates anchor and link_type.
        Both nodes are registered automatically.
        """
        with self._lock:
            self._ensure_node(from_doc)
            self._ensure_node(to_doc)

            added_at = now if now is not None else time.time()
            key = (from_doc, to_doc)

            if key in self._links:
                # update in place
                existing = self._links[key]
                existing.anchor = anchor
                existing.link_type = link_type
                return existing

            link = DocLink(
                from_doc=from_doc,
                to_doc=to_doc,
                anchor=anchor,
                link_type=link_type,
                added_at=added_at,
            )
            self._links[key] = link
            self._out[from_doc].add(to_doc)
            self._in[to_doc].add(from_doc)
            return link

    def remove_link(self, from_doc: str, to_doc: str) -> bool:
        """Remove the link from_doc → to_doc. Returns True if it existed."""
        with self._lock:
            return self._remove_link_unsafe(from_doc, to_doc)

    def get_link(self, from_doc: str, to_doc: str) -> Optional[DocLink]:
        """Return the DocLink for from_doc → to_doc, or None if absent."""
        with self._lock:
            return self._links.get((from_doc, to_doc))

    def has_link(self, from_doc: str, to_doc: str) -> bool:
        """True iff a direct link from_doc → to_doc exists."""
        with self._lock:
            return (from_doc, to_doc) in self._links

    # ------------------------------------------------------------------
    # Traversal helpers
    # ------------------------------------------------------------------

    def outgoing(self, doc_id: str) -> list[DocLink]:
        """All links whose source is doc_id, sorted by to_doc."""
        with self._lock:
            targets = self._out.get(doc_id, set())
            return sorted(
                (self._links[(doc_id, t)] for t in targets),
                key=lambda lnk: lnk.to_doc,
            )

    def incoming(self, doc_id: str) -> list[DocLink]:
        """All links whose target is doc_id, sorted by from_doc."""
        with self._lock:
            sources = self._in.get(doc_id, set())
            return sorted(
                (self._links[(s, doc_id)] for s in sources),
                key=lambda lnk: lnk.from_doc,
            )

    def out_degree(self, doc_id: str) -> int:
        """Number of outgoing links from doc_id."""
        with self._lock:
            return len(self._out.get(doc_id, set()))

    def in_degree(self, doc_id: str) -> int:
        """Number of incoming links to doc_id."""
        with self._lock:
            return len(self._in.get(doc_id, set()))

    def all_links(self) -> list[DocLink]:
        """All links sorted by (from_doc, to_doc)."""
        with self._lock:
            return sorted(self._links.values(), key=lambda lnk: (lnk.from_doc, lnk.to_doc))

    def most_linked_to(self, limit: int = 10) -> list[tuple[str, int]]:
        """Top ``limit`` docs by incoming link count.

        Sorted by in_degree descending, then doc_id ascending.
        Only includes docs that have at least one incoming link.
        """
        with self._lock:
            counts = [
                (doc_id, len(self._in.get(doc_id, set())))
                for doc_id in self._nodes
            ]
            counts = [(d, c) for d, c in counts if c > 0]
            counts.sort(key=lambda x: (-x[1], x[0]))
            return counts[:limit]

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> LinkGraphStats:
        """Return aggregate statistics about the current graph state."""
        with self._lock:
            total_links = len(self._links)
            unique_sources = sum(1 for doc in self._nodes if self._out.get(doc))
            unique_targets = sum(1 for doc in self._nodes if self._in.get(doc))
            orphan_count = sum(
                1
                for doc in self._nodes
                if not self._out.get(doc) and not self._in.get(doc)
            )
            return LinkGraphStats(
                total_links=total_links,
                unique_sources=unique_sources,
                unique_targets=unique_targets,
                orphan_count=orphan_count,
            )

    # ------------------------------------------------------------------
    # Private helpers (must be called with lock held)
    # ------------------------------------------------------------------

    def _ensure_node(self, doc_id: str) -> None:
        """Register doc_id if not already present. Lock must be held."""
        if doc_id not in self._nodes:
            self._nodes.add(doc_id)
            self._out.setdefault(doc_id, set())
            self._in.setdefault(doc_id, set())

    def _remove_link_unsafe(self, from_doc: str, to_doc: str) -> bool:
        """Remove a link without acquiring the lock. Returns True if removed."""
        key = (from_doc, to_doc)
        if key not in self._links:
            return False
        del self._links[key]
        self._out.get(from_doc, set()).discard(to_doc)
        self._in.get(to_doc, set()).discard(from_doc)
        return True
