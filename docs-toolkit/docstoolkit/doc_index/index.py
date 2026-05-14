"""Core implementation of the in-memory document index (E136).

This module provides a lightweight, stdlib-only document index that
supports multi-field indexing with configurable per-field weights and
fast token-match scoring.

The implementation intentionally keeps a small surface area: documents
are stored as :class:`IndexedDoc` instances and a single class
(:class:`DocIndex`) maintains both the forward store (``doc_id -> doc``)
and an inverted token index used for searching.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

__all__ = [
    "IndexedDoc",
    "IndexEntry",
    "IndexConfig",
    "DocIndex",
]


_TOKEN_RE = re.compile(r"\w+", re.UNICODE)


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class IndexedDoc:
    """A document held in the index.

    Attributes
    ----------
    doc_id:
        Unique identifier for the document.
    fields:
        Mapping of field name to its (string) value, e.g.
        ``{"title": "...", "body": "...", "tags": "..."}``.
    metadata:
        Free-form metadata attached to the document. Not indexed.
    """

    doc_id: str
    fields: Dict[str, str]
    metadata: dict = field(default_factory=dict)


@dataclass
class IndexEntry:
    """A single (doc, field) hit produced by a search."""

    doc_id: str
    field: str
    score: float
    matches: int


@dataclass
class IndexConfig:
    """Configuration for a :class:`DocIndex`."""

    field_weights: Dict[str, float] = field(
        default_factory=lambda: {"title": 2.0, "body": 1.0}
    )
    case_sensitive: bool = False
    min_token_length: int = 2


# ---------------------------------------------------------------------------
# DocIndex
# ---------------------------------------------------------------------------

class DocIndex:
    """In-memory inverted index over multi-field documents.

    The inverted index has the shape::

        {token: {doc_id: {field: count}}}

    A forward map (``doc_id -> IndexedDoc``) keeps the original documents
    so callers can look them up after a search.
    """

    def __init__(self, config: Optional[IndexConfig] = None) -> None:
        self.config: IndexConfig = config if config is not None else IndexConfig()
        # token -> doc_id -> field -> count
        self._inverted: Dict[str, Dict[str, Dict[str, int]]] = {}
        self._docs: Dict[str, IndexedDoc] = {}
        # doc_id -> set of fields it carries (for fast removal)
        self._doc_fields: Dict[str, Set[str]] = {}

    # ------------------------------------------------------------------
    # Tokenisation helpers
    # ------------------------------------------------------------------

    def _tokenize(self, text: str) -> List[str]:
        """Tokenise a text snippet using the configured rules."""
        if not text:
            return []
        tokens = _TOKEN_RE.findall(text)
        if not self.config.case_sensitive:
            tokens = [t.lower() for t in tokens]
        min_len = self.config.min_token_length
        if min_len > 1:
            tokens = [t for t in tokens if len(t) >= min_len]
        return tokens

    # ------------------------------------------------------------------
    # Mutation API
    # ------------------------------------------------------------------

    def add(
        self,
        doc_id: str,
        fields: Dict[str, str],
        metadata: Optional[dict] = None,
    ) -> None:
        """Index a document, replacing any existing entry with the same id."""
        if doc_id in self._docs:
            # Replace: remove old postings first.
            self.remove(doc_id)
        doc = IndexedDoc(
            doc_id=doc_id,
            fields=dict(fields),
            metadata=dict(metadata) if metadata is not None else {},
        )
        self._docs[doc_id] = doc
        self._doc_fields[doc_id] = set(doc.fields.keys())
        for field_name, text in doc.fields.items():
            for token in self._tokenize(text or ""):
                doc_map = self._inverted.setdefault(token, {})
                field_map = doc_map.setdefault(doc_id, {})
                field_map[field_name] = field_map.get(field_name, 0) + 1

    def add_batch(self, docs: List[IndexedDoc]) -> None:
        """Index a list of :class:`IndexedDoc` objects."""
        for d in docs:
            self.add(d.doc_id, d.fields, d.metadata)

    def remove(self, doc_id: str) -> bool:
        """Remove a document. Returns ``True`` if it was present."""
        if doc_id not in self._docs:
            return False
        # Walk inverted index — only touch tokens that actually mention us.
        # We can iterate the doc's fields' tokens to find candidate tokens.
        candidate_tokens: Set[str] = set()
        for text in self._docs[doc_id].fields.values():
            for token in self._tokenize(text or ""):
                candidate_tokens.add(token)
        for token in candidate_tokens:
            doc_map = self._inverted.get(token)
            if not doc_map:
                continue
            if doc_id in doc_map:
                del doc_map[doc_id]
            if not doc_map:
                del self._inverted[token]
        del self._docs[doc_id]
        self._doc_fields.pop(doc_id, None)
        return True

    def update(self, doc_id: str, fields: Dict[str, str]) -> bool:
        """Re-index a document with new field values.

        Returns ``True`` if the document existed; ``False`` otherwise.
        Metadata is preserved across the update.
        """
        if doc_id not in self._docs:
            return False
        metadata = self._docs[doc_id].metadata
        self.add(doc_id, fields, metadata)
        return True

    def clear(self) -> None:
        """Drop all documents and reset the inverted index."""
        self._inverted.clear()
        self._docs.clear()
        self._doc_fields.clear()

    # ------------------------------------------------------------------
    # Lookup API
    # ------------------------------------------------------------------

    def get(self, doc_id: str) -> Optional[IndexedDoc]:
        """Return the :class:`IndexedDoc` for ``doc_id``, or ``None``."""
        return self._docs.get(doc_id)

    def exists(self, doc_id: str) -> bool:
        """Return ``True`` if ``doc_id`` is indexed."""
        return doc_id in self._docs

    @property
    def count(self) -> int:
        """Number of indexed documents."""
        return len(self._docs)

    @property
    def field_names(self) -> Set[str]:
        """Set of all field names seen across indexed documents."""
        names: Set[str] = set()
        for fields in self._doc_fields.values():
            names.update(fields)
        return names

    def all_doc_ids(self) -> List[str]:
        """Return the list of all indexed document ids (sorted)."""
        return sorted(self._docs.keys())

    # ------------------------------------------------------------------
    # Search API
    # ------------------------------------------------------------------

    def _field_weight(self, field_name: str) -> float:
        """Return the weight for a field, defaulting to 1.0."""
        return float(self.config.field_weights.get(field_name, 1.0))

    def _rank(
        self,
        per_doc_field: Dict[str, Dict[str, int]],
        top_k: int,
    ) -> List[IndexEntry]:
        """Convert (doc -> field -> matches) into ranked entries."""
        entries: List[IndexEntry] = []
        for doc_id, field_counts in per_doc_field.items():
            for field_name, matches in field_counts.items():
                if matches <= 0:
                    continue
                score = matches * self._field_weight(field_name)
                entries.append(
                    IndexEntry(
                        doc_id=doc_id,
                        field=field_name,
                        score=score,
                        matches=matches,
                    )
                )
        entries.sort(key=lambda e: (-e.score, e.doc_id, e.field))
        if top_k is not None and top_k >= 0:
            entries = entries[:top_k]
        return entries

    def search(self, query: str, top_k: int = 10) -> List[IndexEntry]:
        """Search across all fields.

        Each query token is matched against the inverted index, and the
        per-(doc, field) match counts are summed. The score for an
        :class:`IndexEntry` is ``total_matches * field_weight``.
        """
        tokens = self._tokenize(query or "")
        if not tokens:
            return []
        # doc_id -> field -> total match count across query tokens
        per_doc_field: Dict[str, Dict[str, int]] = {}
        for token in tokens:
            doc_map = self._inverted.get(token)
            if not doc_map:
                continue
            for doc_id, field_counts in doc_map.items():
                fmap = per_doc_field.setdefault(doc_id, {})
                for field_name, count in field_counts.items():
                    fmap[field_name] = fmap.get(field_name, 0) + count
        return self._rank(per_doc_field, top_k)

    def search_field(
        self,
        query: str,
        field: str,
        top_k: int = 10,
    ) -> List[IndexEntry]:
        """Search restricted to a single field."""
        tokens = self._tokenize(query or "")
        if not tokens:
            return []
        per_doc_field: Dict[str, Dict[str, int]] = {}
        for token in tokens:
            doc_map = self._inverted.get(token)
            if not doc_map:
                continue
            for doc_id, field_counts in doc_map.items():
                if field not in field_counts:
                    continue
                fmap = per_doc_field.setdefault(doc_id, {})
                fmap[field] = fmap.get(field, 0) + field_counts[field]
        return self._rank(per_doc_field, top_k)
