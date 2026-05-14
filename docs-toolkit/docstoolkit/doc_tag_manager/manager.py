"""E288 DocTagManager — tag management for documents.

Thread-safe, pure stdlib implementation.

Public API
----------
:class:`TagInfo`          — metadata about a single tag
:class:`DocTags`          — tags associated with a document
:class:`TagManagerStats`  — aggregate statistics for the tag store
:class:`DocTagManager`    — main interface for tag CRUD and querying
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class TagInfo:
    """Metadata about a single tag."""

    tag: str
    doc_count: int
    aliases: list[str] = field(default_factory=list)
    parent: Optional[str] = None


@dataclass
class DocTags:
    """Tags associated with a single document."""

    doc_id: str
    tags: list[str]   # sorted
    tag_count: int


@dataclass
class TagManagerStats:
    """Aggregate statistics for the entire tag store."""

    total_tags: int         # unique tags that are in use
    total_docs: int         # documents that have at least one tag
    total_assignments: int  # sum of all tag assignments across all docs


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------


class DocTagManager:
    """Tag management for documents.

    Thread-safe via a single :class:`threading.Lock`.  All public methods
    acquire the lock for their entire duration so callers need not worry about
    concurrent access.

    Alias resolution
    ~~~~~~~~~~~~~~~~
    When :meth:`register_alias` maps ``alias`` → ``canonical``, any subsequent
    :meth:`add_tag` / :meth:`add_tags` call that supplies the *alias* will
    silently store the *canonical* tag instead.  The alias itself is never
    stored as a tag on any document.

    Tag hierarchy
    ~~~~~~~~~~~~~
    :meth:`set_parent` establishes a parent → child relationship.
    :meth:`ancestors_of` walks the chain from ``tag`` upward and returns
    ``[parent, grandparent, …]`` in order.  Cycles are detected and ignored
    (iteration stops when a previously-seen tag would be visited again).
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # doc_id -> set of canonical tags
        self._doc_tags: dict[str, set[str]] = {}
        # canonical tag -> set of doc_ids
        self._tag_docs: dict[str, set[str]] = {}
        # alias -> canonical
        self._aliases: dict[str, str] = {}
        # tag -> parent tag (for hierarchy)
        self._parents: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock held)
    # ------------------------------------------------------------------

    def _resolve(self, tag: str) -> str:
        """Return the canonical form of *tag*, following alias chain."""
        visited: set[str] = set()
        current = tag
        while current in self._aliases:
            if current in visited:
                break
            visited.add(current)
            current = self._aliases[current]
        return current

    def _ensure_tag_set(self, tag: str) -> None:
        """Make sure *tag* has an entry in _tag_docs."""
        if tag not in self._tag_docs:
            self._tag_docs[tag] = set()

    # ------------------------------------------------------------------
    # Single-tag mutation
    # ------------------------------------------------------------------

    def add_tag(self, doc_id: str, tag: str) -> bool:
        """Add *tag* to *doc_id*.

        Aliases are resolved before storage.

        Returns
        -------
        bool
            ``True`` if the tag was newly added, ``False`` if it was already
            present.
        """
        with self._lock:
            canonical = self._resolve(tag)
            doc_set = self._doc_tags.setdefault(doc_id, set())
            if canonical in doc_set:
                return False
            doc_set.add(canonical)
            self._ensure_tag_set(canonical)
            self._tag_docs[canonical].add(doc_id)
            return True

    def add_tags(self, doc_id: str, tags: list[str]) -> int:
        """Add multiple *tags* to *doc_id*.

        Returns
        -------
        int
            The number of tags that were newly added (not already present).
        """
        with self._lock:
            doc_set = self._doc_tags.setdefault(doc_id, set())
            added = 0
            for tag in tags:
                canonical = self._resolve(tag)
                if canonical not in doc_set:
                    doc_set.add(canonical)
                    self._ensure_tag_set(canonical)
                    self._tag_docs[canonical].add(doc_id)
                    added += 1
            return added

    def remove_tag(self, doc_id: str, tag: str) -> bool:
        """Remove *tag* from *doc_id*.

        Alias resolution is applied so callers can pass either an alias or the
        canonical name.

        Returns
        -------
        bool
            ``True`` if the tag was present and has been removed.
        """
        with self._lock:
            canonical = self._resolve(tag)
            doc_set = self._doc_tags.get(doc_id)
            if doc_set is None or canonical not in doc_set:
                return False
            doc_set.discard(canonical)
            self._tag_docs[canonical].discard(doc_id)
            return True

    def remove_all_tags(self, doc_id: str) -> int:
        """Remove all tags from *doc_id*.

        Returns
        -------
        int
            The number of tags removed.
        """
        with self._lock:
            doc_set = self._doc_tags.pop(doc_id, set())
            for tag in doc_set:
                self._tag_docs[tag].discard(doc_id)
            return len(doc_set)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def has_tag(self, doc_id: str, tag: str) -> bool:
        """Return ``True`` if *doc_id* has *tag* (alias-resolved)."""
        with self._lock:
            canonical = self._resolve(tag)
            return canonical in self._doc_tags.get(doc_id, set())

    def tags_for_doc(self, doc_id: str) -> list[str]:
        """Return a sorted list of tags assigned to *doc_id*."""
        with self._lock:
            return sorted(self._doc_tags.get(doc_id, set()))

    def docs_with_tag(self, tag: str) -> list[str]:
        """Return a sorted list of doc_ids that carry *tag* (alias-resolved)."""
        with self._lock:
            canonical = self._resolve(tag)
            return sorted(self._tag_docs.get(canonical, set()))

    def docs_with_all_tags(self, tags: list[str]) -> list[str]:
        """Return sorted doc_ids that have **all** of the given *tags*."""
        with self._lock:
            if not tags:
                return []
            canonicals = [self._resolve(t) for t in tags]
            sets = [self._tag_docs.get(c, set()) for c in canonicals]
            result = sets[0].copy()
            for s in sets[1:]:
                result &= s
            return sorted(result)

    def docs_with_any_tag(self, tags: list[str]) -> list[str]:
        """Return sorted, deduplicated doc_ids that have **any** of the given *tags*."""
        with self._lock:
            result: set[str] = set()
            for tag in tags:
                canonical = self._resolve(tag)
                result |= self._tag_docs.get(canonical, set())
            return sorted(result)

    # ------------------------------------------------------------------
    # Bulk mutation
    # ------------------------------------------------------------------

    def rename_tag(self, old_tag: str, new_tag: str) -> int:
        """Rename *old_tag* to *new_tag* globally.

        All documents that carry *old_tag* will instead carry *new_tag* after
        this call.  If a document already has *new_tag* it will not be
        duplicated.

        Returns
        -------
        int
            The number of documents that were affected (had *old_tag*).
        """
        with self._lock:
            old_docs = self._tag_docs.pop(old_tag, set())
            affected = 0
            if old_docs:
                # Merge into new_tag's doc set
                new_docs = self._tag_docs.setdefault(new_tag, set())
                for doc_id in old_docs:
                    doc_set = self._doc_tags.get(doc_id, set())
                    doc_set.discard(old_tag)
                    if new_tag not in doc_set:
                        doc_set.add(new_tag)
                        new_docs.add(doc_id)
                    affected += 1
            # Always update hierarchy and alias references
            if old_tag in self._parents:
                self._parents[new_tag] = self._parents.pop(old_tag)
            for child, parent in list(self._parents.items()):
                if parent == old_tag:
                    self._parents[child] = new_tag
            for alias, canonical in list(self._aliases.items()):
                if canonical == old_tag:
                    self._aliases[alias] = new_tag
            return affected

    # ------------------------------------------------------------------
    # Alias management
    # ------------------------------------------------------------------

    def register_alias(self, alias: str, canonical: str) -> None:
        """Register *alias* as an alternative name for *canonical*.

        After registration, :meth:`add_tag` with *alias* will store the
        *canonical* tag.
        """
        with self._lock:
            self._aliases[alias] = canonical

    # ------------------------------------------------------------------
    # Hierarchy management
    # ------------------------------------------------------------------

    def set_parent(self, tag: str, parent: str) -> None:
        """Declare that *tag* is a child of *parent* in the tag hierarchy."""
        with self._lock:
            self._parents[tag] = parent

    def ancestors_of(self, tag: str) -> list[str]:
        """Return ordered ancestors of *tag*: ``[parent, grandparent, …]``.

        Cycles are silently broken — iteration stops when a tag that has
        already appeared in the chain would be visited again.
        """
        with self._lock:
            ancestors: list[str] = []
            visited: set[str] = {tag}
            current = self._parents.get(tag)
            while current is not None:
                if current in visited:
                    break
                ancestors.append(current)
                visited.add(current)
                current = self._parents.get(current)
            return ancestors

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------

    def tag_info(self, tag: str) -> Optional[TagInfo]:
        """Return :class:`TagInfo` for *tag*, or ``None`` if unknown.

        A tag is considered *known* when it has at least one document, at least
        one alias pointing to it, or has a registered parent.
        """
        with self._lock:
            doc_count = len(self._tag_docs.get(tag, set()))
            aliases = [a for a, c in self._aliases.items() if c == tag]
            parent = self._parents.get(tag)
            children_registered = any(p == tag for p in self._parents.values())
            if doc_count == 0 and not aliases and parent is None and not children_registered:
                # Also return None if tag has no registered alias itself
                # (not the canonical of anything, no parent, unused)
                return None
            return TagInfo(
                tag=tag,
                doc_count=doc_count,
                aliases=sorted(aliases),
                parent=parent,
            )

    def all_tags(self) -> list[str]:
        """Return a sorted list of all tags currently in use (have ≥1 doc)."""
        with self._lock:
            return sorted(
                tag for tag, docs in self._tag_docs.items() if docs
            )

    def get_doc_tags(self, doc_id: str) -> DocTags:
        """Return :class:`DocTags` for *doc_id*.

        If the document has no tags the returned object will have an empty
        ``tags`` list and ``tag_count == 0``.
        """
        with self._lock:
            tags = sorted(self._doc_tags.get(doc_id, set()))
            return DocTags(doc_id=doc_id, tags=tags, tag_count=len(tags))

    def stats(self) -> TagManagerStats:
        """Return aggregate :class:`TagManagerStats`."""
        with self._lock:
            total_tags = sum(1 for docs in self._tag_docs.values() if docs)
            total_docs = sum(1 for tags in self._doc_tags.values() if tags)
            total_assignments = sum(
                len(tags) for tags in self._doc_tags.values()
            )
            return TagManagerStats(
                total_tags=total_tags,
                total_docs=total_docs,
                total_assignments=total_assignments,
            )
