"""DocLayoutStore — document layout/template position storage.

Manages :class:`DocLayout` objects, each of which contains an ordered list
of :class:`LayoutBlock` items positioned within a document.

Stdlib only. Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LayoutBlock:
    """A positioned block within a document layout.

    Attributes
    ----------
    block_id:
        Unique identifier for the block within its layout.
    block_type:
        Kind of block, e.g. ``"header"``, ``"section"``, ``"footer"``,
        ``"image"``.
    position:
        Ordering index; lower values appear earlier in the layout.
    properties:
        Arbitrary, type-specific metadata for the block.
    """

    block_id: str
    block_type: str
    position: int
    properties: dict = field(default_factory=dict)


@dataclass
class DocLayout:
    """A complete layout description for a document.

    Attributes
    ----------
    doc_id:
        Identifier of the document this layout belongs to.
    layout_id:
        UUID assigned at creation time.
    name:
        Optional human-readable label.
    blocks:
        Ordered list of :class:`LayoutBlock`, sorted by ``position``.
    created_at:
        Unix timestamp when the layout was created.
    updated_at:
        Unix timestamp of the most recent modification.
    """

    doc_id: str
    layout_id: str
    name: str = ""
    blocks: list[LayoutBlock] = field(default_factory=list)
    created_at: float = 0.0
    updated_at: float = 0.0


@dataclass
class LayoutStats:
    """Aggregate statistics for the layout store.

    Attributes
    ----------
    total_layouts:
        Total number of stored layouts.
    total_blocks:
        Sum of block counts across all layouts.
    unique_docs:
        Number of distinct documents that have at least one layout.
    """

    total_layouts: int
    total_blocks: int
    unique_docs: int


class DocLayoutStore:
    """Thread-safe store for document layouts.

    Internal storage
    ----------------
    ``_layouts`` : dict[str, DocLayout]      — layout_id → DocLayout
    ``_by_doc``  : dict[str, list[str]]      — doc_id → list of layout_ids
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()
        self._layouts: dict[str, DocLayout] = {}
        self._by_doc: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock held)
    # ------------------------------------------------------------------

    @staticmethod
    def _sort_blocks(blocks: list[LayoutBlock]) -> list[LayoutBlock]:
        return sorted(blocks, key=lambda b: (b.position, b.block_id))

    @staticmethod
    def _now(now: Optional[float]) -> float:
        return now if now is not None else time.time()

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def create_layout(
        self,
        doc_id: str,
        name: str = "",
        blocks: Optional[list[LayoutBlock]] = None,
        now: Optional[float] = None,
    ) -> DocLayout:
        """Create and store a new layout for ``doc_id``.

        Parameters
        ----------
        doc_id:
            Identifier of the document the layout belongs to.
        name:
            Optional human-readable label.
        blocks:
            Initial blocks for the layout.  The list is copied so the
            caller may mutate the original afterwards.
        now:
            Override timestamp (Unix seconds).  When ``None`` the current
            wall-clock time is used.

        Returns
        -------
        DocLayout
            The newly created layout.
        """
        ts = self._now(now)
        initial_blocks = self._sort_blocks(list(blocks)) if blocks else []
        layout_id = str(uuid.uuid4())
        layout = DocLayout(
            doc_id=doc_id,
            layout_id=layout_id,
            name=name,
            blocks=initial_blocks,
            created_at=ts,
            updated_at=ts,
        )
        with self._lock:
            self._layouts[layout_id] = layout
            self._by_doc.setdefault(doc_id, []).append(layout_id)
        return layout

    def update_layout(
        self,
        layout_id: str,
        name: Optional[str] = None,
        blocks: Optional[list[LayoutBlock]] = None,
        now: Optional[float] = None,
    ) -> Optional[DocLayout]:
        """Partially update an existing layout.

        Returns the updated :class:`DocLayout` or ``None`` if not found.
        Updates ``updated_at`` whenever a field changes.
        """
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return None
            changed = False
            if name is not None and name != layout.name:
                layout.name = name
                changed = True
            if blocks is not None:
                layout.blocks = self._sort_blocks(list(blocks))
                changed = True
            if changed:
                layout.updated_at = self._now(now)
            return layout

    def add_block(
        self,
        layout_id: str,
        block: LayoutBlock,
        now: Optional[float] = None,
    ) -> bool:
        """Append ``block`` to the layout and re-sort by position.

        Returns ``True`` if the layout was found, ``False`` otherwise.
        """
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return False
            layout.blocks.append(block)
            layout.blocks = self._sort_blocks(layout.blocks)
            layout.updated_at = self._now(now)
            return True

    def remove_block(
        self,
        layout_id: str,
        block_id: str,
        now: Optional[float] = None,
    ) -> bool:
        """Remove the block with ``block_id`` from the layout.

        Returns ``True`` if the block existed and was removed,
        ``False`` if the layout or the block was not found.
        """
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return False
            for idx, b in enumerate(layout.blocks):
                if b.block_id == block_id:
                    del layout.blocks[idx]
                    layout.updated_at = self._now(now)
                    return True
            return False

    def move_block(
        self,
        layout_id: str,
        block_id: str,
        new_position: int,
        now: Optional[float] = None,
    ) -> bool:
        """Update ``block``'s position and re-sort the layout.

        Returns ``True`` on success, ``False`` if the layout or block
        was not found.
        """
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return False
            for b in layout.blocks:
                if b.block_id == block_id:
                    b.position = new_position
                    layout.blocks = self._sort_blocks(layout.blocks)
                    layout.updated_at = self._now(now)
                    return True
            return False

    def delete_layout(self, layout_id: str) -> bool:
        """Remove the layout from the store.

        Returns ``True`` if the layout existed, ``False`` otherwise.
        """
        with self._lock:
            layout = self._layouts.pop(layout_id, None)
            if layout is None:
                return False
            doc_layouts = self._by_doc.get(layout.doc_id)
            if doc_layouts is not None:
                if layout_id in doc_layouts:
                    doc_layouts.remove(layout_id)
                if not doc_layouts:
                    del self._by_doc[layout.doc_id]
            return True

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_layout(self, layout_id: str) -> Optional[DocLayout]:
        """Return the layout with ``layout_id`` or ``None`` if absent."""
        with self._lock:
            return self._layouts.get(layout_id)

    def layouts_for_doc(self, doc_id: str) -> list[DocLayout]:
        """Return all layouts for ``doc_id`` sorted by ``created_at``."""
        with self._lock:
            ids = self._by_doc.get(doc_id, [])
            layouts = [self._layouts[lid] for lid in ids if lid in self._layouts]
            return sorted(layouts, key=lambda lay: (lay.created_at, lay.layout_id))

    def blocks_of(
        self,
        layout_id: str,
        block_type: Optional[str] = None,
    ) -> list[LayoutBlock]:
        """Return the layout's blocks sorted by position.

        When ``block_type`` is provided, only blocks of that type are
        returned.  Returns an empty list when the layout is unknown.
        """
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return []
            blocks = self._sort_blocks(layout.blocks)
            if block_type is not None:
                blocks = [b for b in blocks if b.block_type == block_type]
            return blocks

    def block_count(self, layout_id: str) -> int:
        """Return the number of blocks in the layout (0 if not found)."""
        with self._lock:
            layout = self._layouts.get(layout_id)
            if layout is None:
                return 0
            return len(layout.blocks)

    def all_doc_ids(self) -> list[str]:
        """Return all known document IDs, sorted."""
        with self._lock:
            return sorted(self._by_doc.keys())

    def stats(self) -> LayoutStats:
        """Return aggregate statistics for the store."""
        with self._lock:
            total_layouts = len(self._layouts)
            total_blocks = sum(len(lay.blocks) for lay in self._layouts.values())
            unique_docs = len(self._by_doc)
            return LayoutStats(
                total_layouts=total_layouts,
                total_blocks=total_blocks,
                unique_docs=unique_docs,
            )
