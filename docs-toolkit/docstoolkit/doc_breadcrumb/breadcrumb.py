"""Breadcrumb navigation from document hierarchies."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class BreadcrumbSeparator(Enum):
    """Visual separator between crumbs."""

    SLASH = " / "
    ARROW = " → "
    CHEVRON = " > "
    PIPE = " | "


@dataclass
class Crumb:
    """Single breadcrumb entry."""

    doc_id: str
    title: str
    is_root: bool = False
    is_current: bool = False


@dataclass
class Breadcrumb:
    """A full breadcrumb trail from root to target."""

    crumbs: list[Crumb] = field(default_factory=list)
    target_doc_id: str = ""

    @property
    def depth(self) -> int:
        return len(self.crumbs)

    def to_string(
        self, separator: BreadcrumbSeparator = BreadcrumbSeparator.SLASH
    ) -> str:
        return separator.value.join(c.title for c in self.crumbs)

    def to_markdown(self) -> str:
        parts: list[str] = []
        for c in self.crumbs:
            if c.is_current:
                parts.append(c.title)
            else:
                parts.append(f"[{c.title}](#{c.doc_id})")
        return " / ".join(parts)


class DocBreadcrumb:
    """Manage document hierarchies and produce breadcrumbs."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._parent: dict[str, Optional[str]] = {}
        self._titles: dict[str, str] = {}
        self._aliases: dict[str, str] = {}
        self._default_separator: BreadcrumbSeparator = BreadcrumbSeparator.SLASH

    # ---- registration ----

    def register_title(self, doc_id: str, title: str) -> None:
        with self._lock:
            self._titles[doc_id] = title
            # ensure doc is known
            if doc_id not in self._parent:
                self._parent[doc_id] = None

    def set_parent(self, doc_id: str, parent_id: Optional[str]) -> bool:
        if doc_id == parent_id:
            return False
        with self._lock:
            if parent_id is not None:
                # cycle check: parent_id must not be a descendant of doc_id
                if self._is_descendant_locked(parent_id, doc_id):
                    return False
            self._parent[doc_id] = parent_id
            if parent_id is not None and parent_id not in self._parent:
                self._parent[parent_id] = None
            return True

    def unset_parent(self, doc_id: str) -> bool:
        with self._lock:
            if doc_id not in self._parent:
                return False
            self._parent[doc_id] = None
            return True

    def add_alias(self, alias: str, canonical_doc_id: str) -> bool:
        with self._lock:
            if alias == canonical_doc_id:
                return False
            if alias in self._aliases and self._aliases[alias] != canonical_doc_id:
                # still allow overwrite, but track distinctly — simpler: overwrite
                pass
            self._aliases[alias] = canonical_doc_id
            return True

    def resolve_alias(self, alias_or_id: str) -> str:
        with self._lock:
            return self._aliases.get(alias_or_id, alias_or_id)

    def set_separator(self, separator: BreadcrumbSeparator) -> None:
        with self._lock:
            self._default_separator = separator

    # ---- traversal helpers (locked) ----

    def _is_descendant_locked(self, candidate: str, root: str) -> bool:
        """Return True if `candidate` is a descendant of `root` (or equal)."""
        if candidate == root:
            return True
        # walk up from candidate, see if root is an ancestor
        seen: set[str] = set()
        node: Optional[str] = candidate
        while node is not None and node not in seen:
            seen.add(node)
            p = self._parent.get(node)
            if p == root:
                return True
            node = p
        return False

    def _ancestors_locked(self, doc_id: str) -> list[str]:
        result: list[str] = []
        seen: set[str] = set()
        node = self._parent.get(doc_id)
        while node is not None and node not in seen:
            result.append(node)
            seen.add(node)
            node = self._parent.get(node)
        return result

    def _path_to_locked(self, doc_id: str) -> list[str]:
        anc = self._ancestors_locked(doc_id)
        anc.reverse()
        anc.append(doc_id)
        return anc

    def _title_locked(self, doc_id: str) -> str:
        return self._titles.get(doc_id, doc_id)

    # ---- public queries ----

    def breadcrumb(self, doc_id: str) -> Optional[Breadcrumb]:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            if canonical not in self._parent and canonical not in self._titles:
                return None
            path = self._path_to_locked(canonical)
            crumbs: list[Crumb] = []
            for i, did in enumerate(path):
                crumbs.append(
                    Crumb(
                        doc_id=did,
                        title=self._title_locked(did),
                        is_root=(i == 0),
                        is_current=(did == canonical),
                    )
                )
            return Breadcrumb(crumbs=crumbs, target_doc_id=canonical)

    def path_to(self, doc_id: str) -> list[str]:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            if canonical not in self._parent and canonical not in self._titles:
                return []
            return self._path_to_locked(canonical)

    def ancestors(self, doc_id: str) -> list[str]:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            if canonical not in self._parent and canonical not in self._titles:
                return []
            return self._ancestors_locked(canonical)

    def roots(self) -> list[str]:
        with self._lock:
            return [did for did, p in self._parent.items() if p is None]

    def children(self, doc_id: str) -> list[str]:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            return [did for did, p in self._parent.items() if p == canonical]

    def descendants(self, doc_id: str) -> list[str]:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            result: list[str] = []
            stack: list[str] = [
                did for did, p in self._parent.items() if p == canonical
            ]
            seen: set[str] = set()
            while stack:
                node = stack.pop(0)
                if node in seen:
                    continue
                seen.add(node)
                result.append(node)
                for did, p in self._parent.items():
                    if p == node and did not in seen:
                        stack.append(did)
            return result

    def depth(self, doc_id: str) -> int:
        with self._lock:
            canonical = self._aliases.get(doc_id, doc_id)
            if canonical not in self._parent and canonical not in self._titles:
                return -1
            return len(self._ancestors_locked(canonical))

    def is_ancestor_of(self, maybe_ancestor: str, doc_id: str) -> bool:
        with self._lock:
            anc_canon = self._aliases.get(maybe_ancestor, maybe_ancestor)
            doc_canon = self._aliases.get(doc_id, doc_id)
            if anc_canon == doc_canon:
                return False
            return anc_canon in self._ancestors_locked(doc_canon)

    def breadcrumbs_for_all(self) -> dict[str, Breadcrumb]:
        with self._lock:
            ids = set(self._parent.keys()) | set(self._titles.keys())
        result: dict[str, Breadcrumb] = {}
        for did in ids:
            bc = self.breadcrumb(did)
            if bc is not None:
                result[did] = bc
        return result

    @property
    def total_docs(self) -> int:
        with self._lock:
            return len(set(self._parent.keys()) | set(self._titles.keys()))

    def clear(self) -> None:
        with self._lock:
            self._parent.clear()
            self._titles.clear()
            self._aliases.clear()
            self._default_separator = BreadcrumbSeparator.SLASH
