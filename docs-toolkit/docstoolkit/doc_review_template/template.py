"""E404 DocReviewTemplate — review checklist template manager.

Thread-safe, stdlib-only, dataclass-based review template manager.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ChecklistItem:
    """A single checklist item within a review template."""

    item_id: str
    text: str
    required: bool = True
    weight: float = 1.0
    order: int = 0


@dataclass
class ReviewTemplate:
    """A review checklist template."""

    template_id: str
    name: str
    description: str = ""
    items: list[ChecklistItem] = field(default_factory=list)
    created_at: float = 0.0


@dataclass
class TemplateStats:
    """Aggregate template statistics."""

    total_templates: int
    total_items: int
    avg_items_per_template: float


class DocReviewTemplate:
    """In-memory, thread-safe review checklist template manager."""

    def __init__(self) -> None:
        self._templates: dict[str, ReviewTemplate] = {}
        self._assignments: dict[str, str] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- create
    def create_template(
        self,
        template_id: str,
        name: str,
        items: list[ChecklistItem],
        description: str = "",
        now: Optional[float] = None,
    ) -> ReviewTemplate:
        """Create a new review template.

        Items are stored sorted by ``order``. Returns the created template.
        """
        if now is None:
            now = time.time()
        sorted_items = sorted(list(items), key=lambda i: i.order)
        template = ReviewTemplate(
            template_id=template_id,
            name=name,
            description=description,
            items=sorted_items,
            created_at=now,
        )
        with self._lock:
            self._templates[template_id] = template
        return template

    # ---------------------------------------------------------------- update
    def update_template(
        self,
        template_id: str,
        name: Optional[str] = None,
        items: Optional[list[ChecklistItem]] = None,
        description: Optional[str] = None,
    ) -> Optional[ReviewTemplate]:
        """Partially update a template. Returns the template, or None if missing."""
        with self._lock:
            t = self._templates.get(template_id)
            if t is None:
                return None
            if name is not None:
                t.name = name
            if description is not None:
                t.description = description
            if items is not None:
                t.items = sorted(list(items), key=lambda i: i.order)
            return t

    # ---------------------------------------------------------------- delete
    def delete_template(self, template_id: str) -> bool:
        """Remove a template and drop any doc assignments to it.

        Returns True if the template existed.
        """
        with self._lock:
            if template_id not in self._templates:
                return False
            self._templates.pop(template_id, None)
            stale = [d for d, t in self._assignments.items() if t == template_id]
            for d in stale:
                self._assignments.pop(d, None)
            return True

    # ---------------------------------------------------------------- get
    def get_template(self, template_id: str) -> Optional[ReviewTemplate]:
        """Return the template with the given id, or None."""
        with self._lock:
            return self._templates.get(template_id)

    # ---------------------------------------------------------------- list
    def list_templates(self) -> list[ReviewTemplate]:
        """Return all templates sorted by name."""
        with self._lock:
            items = list(self._templates.values())
        items.sort(key=lambda t: t.name)
        return items

    # ---------------------------------------------------------------- items
    def add_item(self, template_id: str, item: ChecklistItem) -> bool:
        """Append an item to a template and re-sort by order.

        Returns True on success, False if template missing.
        """
        with self._lock:
            t = self._templates.get(template_id)
            if t is None:
                return False
            t.items.append(item)
            t.items.sort(key=lambda i: i.order)
            return True

    def remove_item(self, template_id: str, item_id: str) -> bool:
        """Remove an item by id from a template. Returns True if removed."""
        with self._lock:
            t = self._templates.get(template_id)
            if t is None:
                return False
            for idx, it in enumerate(t.items):
                if it.item_id == item_id:
                    t.items.pop(idx)
                    return True
            return False

    def items_of(
        self,
        template_id: str,
        required_only: bool = False,
    ) -> list[ChecklistItem]:
        """Return items of a template sorted by order.

        If ``required_only`` is True, only items with ``required=True`` are returned.
        Returns [] if the template does not exist.
        """
        with self._lock:
            t = self._templates.get(template_id)
            if t is None:
                return []
            items = list(t.items)
        if required_only:
            items = [i for i in items if i.required]
        items.sort(key=lambda i: i.order)
        return items

    def total_weight(self, template_id: str) -> float:
        """Return the sum of item weights for a template (0.0 if missing)."""
        with self._lock:
            t = self._templates.get(template_id)
            if t is None:
                return 0.0
            return float(sum(i.weight for i in t.items))

    # ---------------------------------------------------------------- assign
    def assign(self, doc_id: str, template_id: str) -> bool:
        """Assign a template to a doc. Returns True if template exists."""
        with self._lock:
            if template_id not in self._templates:
                return False
            self._assignments[doc_id] = template_id
            return True

    def template_for_doc(self, doc_id: str) -> Optional[ReviewTemplate]:
        """Return the template assigned to a doc, or None."""
        with self._lock:
            tid = self._assignments.get(doc_id)
            if tid is None:
                return None
            return self._templates.get(tid)

    def docs_using(self, template_id: str) -> list[str]:
        """Return sorted list of doc ids assigned to the given template."""
        with self._lock:
            docs = [d for d, t in self._assignments.items() if t == template_id]
        docs.sort()
        return docs

    def unassign(self, doc_id: str) -> bool:
        """Remove the assignment for a doc. Returns True if there was one."""
        with self._lock:
            return self._assignments.pop(doc_id, None) is not None

    def clear_assignments(self) -> int:
        """Remove all doc assignments. Returns the number cleared."""
        with self._lock:
            n = len(self._assignments)
            self._assignments.clear()
            return n

    # ---------------------------------------------------------------- stats
    def stats(self) -> TemplateStats:
        """Return aggregate template statistics."""
        with self._lock:
            total_templates = len(self._templates)
            total_items = sum(len(t.items) for t in self._templates.values())
        avg = (total_items / total_templates) if total_templates else 0.0
        return TemplateStats(
            total_templates=total_templates,
            total_items=total_items,
            avg_items_per_template=avg,
        )
