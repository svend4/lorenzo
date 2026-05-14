"""E419 DocTagSuggestion — implementation.

Suggest tags for documents based on co-occurrence with existing tags and
overall popularity.  Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TagSuggestion:
    """A suggested tag with confidence and reason."""

    tag: str
    confidence: float
    reason: str = ""


@dataclass
class SuggestionStats:
    """Aggregate statistics for the suggestion engine."""

    total_docs: int
    unique_tags: int
    total_assignments: int


def _pair(a: str, b: str) -> tuple:
    """Return canonical ordered pair (alphabetical)."""
    return (a, b) if a < b else (b, a)


class DocTagSuggestion:
    """Suggest tags based on co-occurrence and popularity.

    Tracks per-document tag sets and pairwise co-occurrence counts.
    All public methods are thread-safe.
    """

    def __init__(self) -> None:
        self._doc_tags: dict[str, set[str]] = {}
        self._tag_docs: dict[str, set[str]] = {}
        self._cooccurrence: dict[tuple, int] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers (assume lock held)
    # ------------------------------------------------------------------
    def _add_pairs(self, tags: set[str]) -> None:
        """Increment co-occurrence for all pairs in ``tags``."""
        sorted_tags = sorted(tags)
        n = len(sorted_tags)
        for i in range(n):
            for j in range(i + 1, n):
                key = (sorted_tags[i], sorted_tags[j])
                self._cooccurrence[key] = self._cooccurrence.get(key, 0) + 1

    def _remove_pairs(self, tags: set[str]) -> None:
        """Decrement co-occurrence for all pairs in ``tags``."""
        sorted_tags = sorted(tags)
        n = len(sorted_tags)
        for i in range(n):
            for j in range(i + 1, n):
                key = (sorted_tags[i], sorted_tags[j])
                if key in self._cooccurrence:
                    self._cooccurrence[key] -= 1
                    if self._cooccurrence[key] <= 0:
                        del self._cooccurrence[key]

    def _add_pairs_for_new_tag(self, new_tag: str, existing: set[str]) -> None:
        """Increment co-occurrence between ``new_tag`` and each tag in ``existing``."""
        for t in existing:
            if t == new_tag:
                continue
            key = _pair(new_tag, t)
            self._cooccurrence[key] = self._cooccurrence.get(key, 0) + 1

    def _remove_pairs_for_old_tag(self, old_tag: str, others: set[str]) -> None:
        """Decrement co-occurrence between ``old_tag`` and each tag in ``others``."""
        for t in others:
            if t == old_tag:
                continue
            key = _pair(old_tag, t)
            if key in self._cooccurrence:
                self._cooccurrence[key] -= 1
                if self._cooccurrence[key] <= 0:
                    del self._cooccurrence[key]

    # ------------------------------------------------------------------
    # Public API: mutation
    # ------------------------------------------------------------------
    def record_tags(self, doc_id: str, tags: list[str]) -> None:
        """Replace the tag set for ``doc_id`` with ``tags``.

        Updates the inverse index and co-occurrence counts accordingly.
        Duplicates in ``tags`` are collapsed; empty strings ignored.
        """
        new_set = {t for t in tags if t}
        with self._lock:
            old_set = self._doc_tags.get(doc_id, set())
            # Decrement old pairs
            if old_set:
                self._remove_pairs(old_set)
                for t in old_set:
                    docs = self._tag_docs.get(t)
                    if docs is not None:
                        docs.discard(doc_id)
                        if not docs:
                            del self._tag_docs[t]
            # Set new tags
            if new_set:
                self._doc_tags[doc_id] = new_set
                for t in new_set:
                    self._tag_docs.setdefault(t, set()).add(doc_id)
                self._add_pairs(new_set)
            else:
                # No new tags — drop record
                self._doc_tags.pop(doc_id, None)

    def clear_doc(self, doc_id: str) -> None:
        """Remove ``doc_id`` entirely and adjust co-occurrence."""
        with self._lock:
            old_set = self._doc_tags.pop(doc_id, None)
            if not old_set:
                return
            self._remove_pairs(old_set)
            for t in old_set:
                docs = self._tag_docs.get(t)
                if docs is not None:
                    docs.discard(doc_id)
                    if not docs:
                        del self._tag_docs[t]

    def add_tag(self, doc_id: str, tag: str) -> bool:
        """Add a single ``tag`` to ``doc_id``.

        Returns True if the tag was newly added, False if it was already present
        or ``tag`` is empty.
        """
        if not tag:
            return False
        with self._lock:
            existing = self._doc_tags.setdefault(doc_id, set())
            if tag in existing:
                return False
            self._add_pairs_for_new_tag(tag, existing)
            existing.add(tag)
            self._tag_docs.setdefault(tag, set()).add(doc_id)
            return True

    def remove_tag(self, doc_id: str, tag: str) -> bool:
        """Remove a single ``tag`` from ``doc_id``.

        Returns True if the tag was present and removed, False otherwise.
        """
        with self._lock:
            existing = self._doc_tags.get(doc_id)
            if not existing or tag not in existing:
                return False
            existing.discard(tag)
            others = existing  # remaining tags after removal
            self._remove_pairs_for_old_tag(tag, others)
            docs = self._tag_docs.get(tag)
            if docs is not None:
                docs.discard(doc_id)
                if not docs:
                    del self._tag_docs[tag]
            if not existing:
                del self._doc_tags[doc_id]
            return True

    # ------------------------------------------------------------------
    # Public API: queries
    # ------------------------------------------------------------------
    def popular_tags(self, limit: int = 10) -> list[tuple]:
        """Return ``[(tag, doc_count), ...]`` sorted by count desc, then tag asc."""
        with self._lock:
            items = [(t, len(docs)) for t, docs in self._tag_docs.items()]
        items.sort(key=lambda x: (-x[1], x[0]))
        if limit is None or limit < 0:
            return items
        return items[:limit]

    def cooccurring_with(self, tag: str, limit: int = 10) -> list[tuple]:
        """Return tags that co-occur with ``tag`` sorted by count desc."""
        with self._lock:
            results: list[tuple] = []
            for (a, b), count in self._cooccurrence.items():
                if a == tag:
                    results.append((b, count))
                elif b == tag:
                    results.append((a, count))
        results.sort(key=lambda x: (-x[1], x[0]))
        if limit is None or limit < 0:
            return results
        return results[:limit]

    def _suggest_from_tags(
        self,
        source_tags: set[str],
        exclude: set[str],
        limit: int,
    ) -> list[TagSuggestion]:
        """Internal helper: aggregate co-occurrence-based suggestions."""
        # confidence[candidate] = sum over source_tag s of count(s,c) / docs_with(s)
        # also track which sources contributed for the reason string
        confidence: dict[str, float] = {}
        contributors: dict[str, list[str]] = {}
        for s in source_tags:
            docs_with_s = len(self._tag_docs.get(s, set()))
            if docs_with_s == 0:
                continue
            # find all co-occurrences involving s
            for (a, b), count in self._cooccurrence.items():
                if a == s:
                    cand = b
                elif b == s:
                    cand = a
                else:
                    continue
                if cand in exclude:
                    continue
                ratio = count / docs_with_s
                confidence[cand] = confidence.get(cand, 0.0) + ratio
                contributors.setdefault(cand, []).append(s)
        # Cap confidence at 1.0
        results: list[TagSuggestion] = []
        for cand, conf in confidence.items():
            capped = min(1.0, conf)
            sources_sorted = sorted(contributors.get(cand, []))
            reason = "co-occurs with: " + ", ".join(sources_sorted)
            results.append(TagSuggestion(tag=cand, confidence=capped, reason=reason))
        results.sort(key=lambda s: (-s.confidence, s.tag))
        if limit is None or limit < 0:
            return results
        return results[:limit]

    def suggest_for_doc(self, doc_id: str, limit: int = 5) -> list[TagSuggestion]:
        """Suggest tags for ``doc_id`` based on its current tags' co-occurrence."""
        with self._lock:
            source_tags = set(self._doc_tags.get(doc_id, set()))
            exclude = set(source_tags)
            return self._suggest_from_tags(source_tags, exclude, limit)

    def suggest_for_tags(
        self,
        input_tags: list[str],
        limit: int = 5,
        exclude: Optional[list[str]] = None,
    ) -> list[TagSuggestion]:
        """Suggest tags for an arbitrary set of input tags."""
        source_tags = {t for t in input_tags if t}
        exclude_set = set(source_tags)
        if exclude:
            exclude_set.update(t for t in exclude if t)
        with self._lock:
            return self._suggest_from_tags(source_tags, exclude_set, limit)

    def tags_for_doc(self, doc_id: str) -> list[str]:
        """Return sorted tags for ``doc_id`` (empty list if unknown)."""
        with self._lock:
            return sorted(self._doc_tags.get(doc_id, set()))

    def docs_with_tag(self, tag: str) -> list[str]:
        """Return sorted doc ids for ``tag``."""
        with self._lock:
            return sorted(self._tag_docs.get(tag, set()))

    def all_tags(self) -> list[str]:
        """Return sorted list of unique tags."""
        with self._lock:
            return sorted(self._tag_docs.keys())

    def all_doc_ids(self) -> list[str]:
        """Return sorted list of doc ids."""
        with self._lock:
            return sorted(self._doc_tags.keys())

    def stats(self) -> SuggestionStats:
        """Return aggregate statistics."""
        with self._lock:
            total_docs = len(self._doc_tags)
            unique_tags = len(self._tag_docs)
            total_assignments = sum(len(s) for s in self._doc_tags.values())
        return SuggestionStats(
            total_docs=total_docs,
            unique_tags=unique_tags,
            total_assignments=total_assignments,
        )
