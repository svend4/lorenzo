"""E269 Document index manager implementation."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Iterable, Optional


class IndexKind(Enum):
    """Kinds of indexes that can be registered."""

    KEYWORD = "keyword"
    METADATA = "metadata"
    FULL_TEXT = "full_text"
    TAGS = "tags"
    NUMERIC = "numeric"


@dataclass
class IndexDefinition:
    """Definition of a single index registered with the manager."""

    name: str
    kind: IndexKind
    extract_func: Callable[[str, dict], Iterable[tuple[str, Any]]]
    enabled: bool = True


@dataclass
class IndexedTerm:
    """A single posting recorded in an index."""

    index_name: str
    term: str
    value: Any
    doc_id: str


class DocIndexManager:
    """Coordinates several per-document indexes with unified query API."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._indexes: dict[str, IndexDefinition] = {}
        # postings: index_name -> term -> set of doc_ids
        self._postings: dict[str, dict[str, set[str]]] = {}
        # doc terms: doc_id -> index_name -> list of IndexedTerm
        self._doc_terms: dict[str, dict[str, list[IndexedTerm]]] = {}

    # ------------------------------------------------------------------
    # Index registration
    # ------------------------------------------------------------------
    def register_index(
        self,
        name: str,
        kind: IndexKind,
        extract_func: Callable[[str, dict], Iterable[tuple[str, Any]]],
    ) -> IndexDefinition:
        """Register a new index. Overwrites if name already exists."""
        with self._lock:
            definition = IndexDefinition(
                name=name, kind=kind, extract_func=extract_func, enabled=True
            )
            self._indexes[name] = definition
            self._postings.setdefault(name, {})
            return definition

    def unregister_index(self, name: str) -> bool:
        """Unregister an index. Returns True if it existed."""
        with self._lock:
            if name not in self._indexes:
                return False
            del self._indexes[name]
            self._postings.pop(name, None)
            for doc_map in self._doc_terms.values():
                doc_map.pop(name, None)
            return True

    def enable_index(self, name: str) -> bool:
        """Enable an index. Returns True if found."""
        with self._lock:
            definition = self._indexes.get(name)
            if definition is None:
                return False
            definition.enabled = True
            return True

    def disable_index(self, name: str) -> bool:
        """Disable an index. Returns True if found."""
        with self._lock:
            definition = self._indexes.get(name)
            if definition is None:
                return False
            definition.enabled = False
            return True

    # ------------------------------------------------------------------
    # Indexing operations
    # ------------------------------------------------------------------
    def index_doc(self, doc_id: str, doc_data: dict) -> dict[str, int]:
        """Index a document across all enabled indexes."""
        result: dict[str, int] = {}
        with self._lock:
            doc_map = self._doc_terms.setdefault(doc_id, {})
            for name, definition in self._indexes.items():
                if not definition.enabled:
                    continue
                try:
                    extracted = list(definition.extract_func(doc_id, doc_data))
                except Exception:
                    extracted = []
                postings = self._postings.setdefault(name, {})
                # Remove previous terms for this doc in this index
                old_terms = doc_map.get(name, [])
                for old in old_terms:
                    bucket = postings.get(old.term)
                    if bucket is not None:
                        bucket.discard(doc_id)
                        if not bucket:
                            del postings[old.term]
                new_terms: list[IndexedTerm] = []
                for term, value in extracted:
                    term_str = str(term)
                    postings.setdefault(term_str, set()).add(doc_id)
                    new_terms.append(
                        IndexedTerm(
                            index_name=name,
                            term=term_str,
                            value=value,
                            doc_id=doc_id,
                        )
                    )
                doc_map[name] = new_terms
                result[name] = len(new_terms)
        return result

    def unindex_doc(self, doc_id: str) -> int:
        """Remove all entries for the given document. Returns number removed."""
        with self._lock:
            doc_map = self._doc_terms.pop(doc_id, None)
            if not doc_map:
                return 0
            removed = 0
            for index_name, terms in doc_map.items():
                postings = self._postings.get(index_name, {})
                for entry in terms:
                    bucket = postings.get(entry.term)
                    if bucket is not None:
                        bucket.discard(doc_id)
                        if not bucket:
                            del postings[entry.term]
                    removed += 1
            return removed

    def reindex_doc(self, doc_id: str, doc_data: dict) -> dict[str, int]:
        """Re-index a document: unindex then index again."""
        self.unindex_doc(doc_id)
        return self.index_doc(doc_id, doc_data)

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------
    def query(self, index_name: str, term: str) -> list[str]:
        """Return doc_ids matching (index_name, term)."""
        with self._lock:
            postings = self._postings.get(index_name)
            if not postings:
                return []
            bucket = postings.get(str(term))
            if not bucket:
                return []
            return sorted(bucket)

    def query_multi(
        self, criteria: dict[str, str], mode: str = "AND"
    ) -> set[str]:
        """Query multiple indexes simultaneously with AND/OR semantics."""
        mode_upper = mode.upper()
        if mode_upper not in ("AND", "OR"):
            raise ValueError(f"Unknown mode: {mode}")
        if not criteria:
            return set()
        with self._lock:
            result: Optional[set[str]] = None
            for index_name, term in criteria.items():
                postings = self._postings.get(index_name, {})
                bucket = postings.get(str(term), set())
                bucket_copy = set(bucket)
                if result is None:
                    result = bucket_copy
                elif mode_upper == "AND":
                    result &= bucket_copy
                else:
                    result |= bucket_copy
            return result or set()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    def terms_for_index(self, index_name: str) -> list[str]:
        """List unique terms stored in an index."""
        with self._lock:
            postings = self._postings.get(index_name, {})
            return sorted(postings.keys())

    def terms_for_doc(
        self, doc_id: str, index_name: Optional[str] = None
    ) -> list[IndexedTerm]:
        """List all terms recorded for a document (optionally one index)."""
        with self._lock:
            doc_map = self._doc_terms.get(doc_id, {})
            if index_name is not None:
                return list(doc_map.get(index_name, []))
            collected: list[IndexedTerm] = []
            for terms in doc_map.values():
                collected.extend(terms)
            return collected

    def index_size(self, index_name: str) -> int:
        """Number of unique terms in an index."""
        with self._lock:
            return len(self._postings.get(index_name, {}))

    def doc_ids(self) -> list[str]:
        """List indexed document IDs."""
        with self._lock:
            return sorted(self._doc_terms.keys())

    def indexes(self) -> list[IndexDefinition]:
        """List registered index definitions."""
        with self._lock:
            return list(self._indexes.values())

    def get_index(self, name: str) -> Optional[IndexDefinition]:
        """Lookup an index definition by name."""
        with self._lock:
            return self._indexes.get(name)

    @property
    def total_indexes(self) -> int:
        """Total number of registered indexes."""
        with self._lock:
            return len(self._indexes)

    @property
    def total_indexed_docs(self) -> int:
        """Total number of indexed documents."""
        with self._lock:
            return len(self._doc_terms)

    # ------------------------------------------------------------------
    # Cleanup
    # ------------------------------------------------------------------
    def clear_index(self, index_name: str) -> int:
        """Clear all postings in a single index. Returns terms cleared."""
        with self._lock:
            postings = self._postings.get(index_name)
            if postings is None:
                return 0
            cleared = len(postings)
            self._postings[index_name] = {}
            for doc_map in self._doc_terms.values():
                doc_map.pop(index_name, None)
            return cleared

    def clear(self) -> None:
        """Reset the entire manager (indexes & postings)."""
        with self._lock:
            self._indexes.clear()
            self._postings.clear()
            self._doc_terms.clear()
