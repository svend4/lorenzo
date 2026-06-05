"""Advanced rule-based document tagger.

Stdlib only. Compared to :mod:`docstoolkit.doc_tagger`, this module adds
hierarchical tags (parent/child), aliases, suggestion confidence, learning
from explicit feedback, and co-occurrence statistics.
"""
from __future__ import annotations

import re
import threading
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------


@dataclass
class TagDefinition:
    """Definition of a single tag."""

    tag: str
    parent: Optional[str] = None
    aliases: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    description: str = ""
    usage_count: int = 0


@dataclass
class TagSuggestion:
    """A suggested tag with confidence and provenance."""

    tag: str
    confidence: float
    source: str  # "keyword", "ancestor", "co-occurrence"


@dataclass
class TaggingFeedback:
    """Record of a user's accept/reject decision."""

    doc_id: str
    tag: str
    accepted: bool
    timestamp: float


# ---------------------------------------------------------------------------
# DocTaggerV2
# ---------------------------------------------------------------------------


class DocTaggerV2:
    """Advanced tagger with hierarchies, aliases, and feedback learning."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._tags: dict[str, TagDefinition] = {}
        # alias (lowercased) -> canonical tag
        self._alias_index: dict[str, str] = {}
        # tag -> list[TaggingFeedback]
        self._feedback: dict[str, list[TaggingFeedback]] = defaultdict(list)
        # co-occurrence counts: tag -> Counter[other_tag]
        self._cooc: dict[str, Counter] = defaultdict(Counter)
        # doc_id -> tags previously recorded
        self._doc_tags: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # Tag definitions
    # ------------------------------------------------------------------
    def define_tag(
        self,
        tag: str,
        parent: str = None,
        aliases: list[str] = None,
        keywords: list[str] = None,
        description: str = "",
    ) -> TagDefinition:
        if not tag or not tag.strip():
            raise ValueError("tag must be non-empty")
        with self._lock:
            if tag in self._tags:
                # Update existing
                defn = self._tags[tag]
                if parent is not None:
                    self._set_parent_unlocked(tag, parent)
                if aliases:
                    for a in aliases:
                        self._add_alias_unlocked(tag, a)
                if keywords:
                    for k in keywords:
                        if k not in defn.keywords:
                            defn.keywords.append(k)
                if description:
                    defn.description = description
                return defn

            defn = TagDefinition(
                tag=tag,
                parent=None,
                aliases=[],
                keywords=list(keywords) if keywords else [],
                description=description,
                usage_count=0,
            )
            self._tags[tag] = defn
            if parent:
                self._set_parent_unlocked(tag, parent)
            if aliases:
                for a in aliases:
                    self._add_alias_unlocked(tag, a)
            return defn

    def remove_tag(self, tag: str) -> bool:
        with self._lock:
            defn = self._tags.pop(tag, None)
            if defn is None:
                return False
            # remove aliases from index
            for a in defn.aliases:
                self._alias_index.pop(a.lower(), None)
            self._alias_index.pop(tag.lower(), None)
            # detach children (set their parent to None)
            for other in self._tags.values():
                if other.parent == tag:
                    other.parent = None
            # remove feedback and co-occurrence entries
            self._feedback.pop(tag, None)
            self._cooc.pop(tag, None)
            for counter in self._cooc.values():
                if tag in counter:
                    del counter[tag]
            return True

    def add_keyword(self, tag: str, keyword: str) -> bool:
        if not keyword:
            return False
        with self._lock:
            defn = self._tags.get(tag)
            if defn is None:
                return False
            if keyword in defn.keywords:
                return False
            defn.keywords.append(keyword)
            return True

    def add_alias(self, tag: str, alias: str) -> bool:
        with self._lock:
            return self._add_alias_unlocked(tag, alias)

    def _add_alias_unlocked(self, tag: str, alias: str) -> bool:
        if not alias:
            return False
        defn = self._tags.get(tag)
        if defn is None:
            return False
        low = alias.lower()
        if low in self._alias_index and self._alias_index[low] != tag:
            return False
        if alias in defn.aliases:
            return False
        defn.aliases.append(alias)
        self._alias_index[low] = tag
        return True

    def set_parent(self, tag: str, parent: str) -> bool:
        with self._lock:
            return self._set_parent_unlocked(tag, parent)

    def _set_parent_unlocked(self, tag: str, parent: str) -> bool:
        defn = self._tags.get(tag)
        if defn is None:
            return False
        if parent is None or parent == "":
            defn.parent = None
            return True
        if parent not in self._tags:
            return False
        if parent == tag:
            return False
        # Cycle detection: walk up from `parent`. If we hit `tag` it would
        # create a cycle.
        cursor: Optional[str] = parent
        visited: set[str] = set()
        while cursor is not None:
            if cursor == tag:
                return False
            if cursor in visited:
                return False  # existing cycle, bail
            visited.add(cursor)
            parent_defn = self._tags.get(cursor)
            cursor = parent_defn.parent if parent_defn else None
        defn.parent = parent
        return True

    # ------------------------------------------------------------------
    # Lookup
    # ------------------------------------------------------------------
    def tag_definition(self, tag: str) -> Optional[TagDefinition]:
        return self._tags.get(tag)

    def all_tags(self) -> list[str]:
        return sorted(self._tags.keys())

    @property
    def total_tags(self) -> int:
        return len(self._tags)

    def resolve_alias(self, input_tag: str) -> Optional[str]:
        if not input_tag:
            return None
        with self._lock:
            if input_tag in self._tags:
                return input_tag
            return self._alias_index.get(input_tag.lower())

    # ------------------------------------------------------------------
    # Hierarchy
    # ------------------------------------------------------------------
    def ancestors(self, tag: str) -> list[str]:
        if tag not in self._tags:
            return []
        result: list[str] = []
        visited: set[str] = set()
        cursor: Optional[str] = self._tags[tag].parent
        while cursor is not None and cursor not in visited:
            visited.add(cursor)
            result.append(cursor)
            parent_defn = self._tags.get(cursor)
            cursor = parent_defn.parent if parent_defn else None
        return result

    def descendants(self, tag: str) -> list[str]:
        if tag not in self._tags:
            return []
        result: list[str] = []
        # BFS over children
        stack = [tag]
        seen: set[str] = set()
        while stack:
            current = stack.pop()
            for child_name, child_defn in self._tags.items():
                if child_defn.parent == current and child_name not in seen:
                    seen.add(child_name)
                    result.append(child_name)
                    stack.append(child_name)
        return sorted(result)

    def siblings(self, tag: str) -> list[str]:
        defn = self._tags.get(tag)
        if defn is None:
            return []
        parent = defn.parent
        result = [
            name
            for name, d in self._tags.items()
            if d.parent == parent and name != tag
        ]
        return sorted(result)

    # ------------------------------------------------------------------
    # Tagging
    # ------------------------------------------------------------------
    def tag_text(
        self,
        text: str,
        max_tags: int = 10,
        min_confidence: float = 0.3,
    ) -> list[TagSuggestion]:
        suggestions = self._suggest_from_keywords(text)
        suggestions = [s for s in suggestions if s.confidence >= min_confidence]
        suggestions.sort(key=lambda s: (-s.confidence, s.tag))
        if max_tags > 0:
            suggestions = suggestions[:max_tags]
        # Record usage_count for accepted suggestions (called on tag_text use).
        with self._lock:
            for s in suggestions:
                defn = self._tags.get(s.tag)
                if defn is not None:
                    defn.usage_count += 1
        return suggestions

    def tag_text_with_ancestors(
        self,
        text: str,
        max_tags: int = 10,
        min_confidence: float = 0.3,
    ) -> list[TagSuggestion]:
        base = self._suggest_from_keywords(text)
        base = [s for s in base if s.confidence >= min_confidence]
        seen: dict[str, TagSuggestion] = {}
        for s in base:
            if s.tag not in seen or seen[s.tag].confidence < s.confidence:
                seen[s.tag] = s
            # Add ancestors
            for ancestor in self.ancestors(s.tag):
                anc_conf = max(s.confidence * 0.5, min_confidence)
                if ancestor in seen:
                    if seen[ancestor].confidence < anc_conf and seen[ancestor].source == "ancestor":
                        seen[ancestor] = TagSuggestion(
                            tag=ancestor,
                            confidence=anc_conf,
                            source="ancestor",
                        )
                else:
                    seen[ancestor] = TagSuggestion(
                        tag=ancestor, confidence=anc_conf, source="ancestor"
                    )
        result = sorted(seen.values(), key=lambda s: (-s.confidence, s.tag))
        if max_tags > 0:
            result = result[:max_tags]
        with self._lock:
            for s in result:
                defn = self._tags.get(s.tag)
                if defn is not None:
                    defn.usage_count += 1
        return result

    def suggested_tags(self, text: str, max_tags: int = 10) -> list[str]:
        return [s.tag for s in self.tag_text(text, max_tags=max_tags)]

    def _suggest_from_keywords(self, text: str) -> list[TagSuggestion]:
        if not text:
            return []
        lowered = text.lower()
        suggestions: list[TagSuggestion] = []
        for defn in self._tags.values():
            if not defn.keywords:
                continue
            total = len(defn.keywords)
            hits = 0
            for kw in defn.keywords:
                if not kw:
                    continue
                pattern = r"(?<!\w)" + re.escape(kw.lower()) + r"(?!\w)"
                if re.search(pattern, lowered):
                    hits += 1
            if hits == 0:
                continue
            confidence = hits / total if total else 0.0
            suggestions.append(
                TagSuggestion(tag=defn.tag, confidence=confidence, source="keyword")
            )
        return suggestions

    # ------------------------------------------------------------------
    # Feedback
    # ------------------------------------------------------------------
    def record_feedback(
        self,
        doc_id: str,
        tag: str,
        accepted: bool,
        now: float = 0.0,
    ) -> TaggingFeedback:
        fb = TaggingFeedback(
            doc_id=doc_id, tag=tag, accepted=accepted, timestamp=now
        )
        with self._lock:
            self._feedback[tag].append(fb)
        return fb

    def acceptance_rate(self, tag: str) -> float:
        entries = self._feedback.get(tag, [])
        if not entries:
            return 0.0
        accepted = sum(1 for fb in entries if fb.accepted)
        return accepted / len(entries)

    # ------------------------------------------------------------------
    # Co-occurrence
    # ------------------------------------------------------------------
    def record_doc_tags(self, doc_id: str, tags: list[str]) -> None:
        with self._lock:
            unique = list({t for t in tags if t})
            self._doc_tags[doc_id] = unique
            for i, t1 in enumerate(unique):
                for t2 in unique[i + 1 :]:
                    self._cooc[t1][t2] += 1
                    self._cooc[t2][t1] += 1

    def co_occurring(self, tag: str, top_k: int = 5) -> list[tuple[str, int]]:
        counter = self._cooc.get(tag)
        if not counter:
            return []
        items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
        if top_k > 0:
            items = items[:top_k]
        return items

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------
    def clear(self) -> None:
        with self._lock:
            self._tags.clear()
            self._alias_index.clear()
            self._feedback.clear()
            self._cooc.clear()
            self._doc_tags.clear()
