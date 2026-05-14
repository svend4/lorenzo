"""Full-text search across gzip-compressed archived documents.

The :class:`DocArchiveSearch` keeps each document compressed in memory and
decompresses on demand.  Decompressed payloads are placed in a bounded LRU
cache so subsequent searches over the same corpus stay fast.

Only the standard library is used (``gzip``, ``re``, ``threading``,
``collections.OrderedDict``).
"""
from __future__ import annotations

import gzip
import re
import threading
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class ArchiveEntry:
    """A single compressed document stored in the archive."""

    doc_id: str
    compressed_data: bytes
    original_size: int
    archived_at: float
    metadata: dict = field(default_factory=dict)


@dataclass
class SearchMatch:
    """A document that matched a query."""

    doc_id: str
    score: int  # number of individual matches inside the document
    excerpts: list  # list[str] – context around each match (best effort)


@dataclass
class SearchOptions:
    """Knobs that control how :meth:`DocArchiveSearch.search` behaves."""

    case_sensitive: bool = False
    whole_word: bool = False
    max_excerpts_per_doc: int = 3
    excerpt_chars: int = 100


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------


class DocArchiveSearch:
    """Archive documents (gzip) and search across them on demand."""

    def __init__(self, cache_size: int = 100) -> None:
        if cache_size < 0:
            raise ValueError("cache_size must be non-negative")
        self._cache_size = cache_size
        self._entries: "dict[str, ArchiveEntry]" = {}
        # OrderedDict acts as an LRU cache: most-recently-used at the right.
        self._cache: "OrderedDict[str, str]" = OrderedDict()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ archive
    def archive(
        self,
        doc_id: str,
        content: str,
        metadata: dict = None,
        now: float = 0.0,
    ) -> ArchiveEntry:
        """Compress *content* and store it under *doc_id*."""
        if not isinstance(doc_id, str) or not doc_id:
            raise ValueError("doc_id must be a non-empty string")
        if not isinstance(content, str):
            raise TypeError("content must be a string")

        meta = dict(metadata) if metadata else {}
        encoded = content.encode("utf-8")
        compressed = gzip.compress(encoded)
        entry = ArchiveEntry(
            doc_id=doc_id,
            compressed_data=compressed,
            original_size=len(encoded),
            archived_at=float(now),
            metadata=meta,
        )
        with self._lock:
            self._entries[doc_id] = entry
            # Invalidate any cached decompressed copy because we just replaced it
            if doc_id in self._cache:
                self._cache.pop(doc_id, None)
        return entry

    def unarchive(self, doc_id: str) -> bool:
        """Remove *doc_id* from the archive.  Returns True on success."""
        with self._lock:
            removed = self._entries.pop(doc_id, None) is not None
            self._cache.pop(doc_id, None)
            return removed

    # ------------------------------------------------------------------ content
    def get_content(self, doc_id: str) -> Optional[str]:
        """Return decompressed content for *doc_id*, caching the result."""
        with self._lock:
            if doc_id in self._cache:
                # Mark recently used.
                self._cache.move_to_end(doc_id)
                return self._cache[doc_id]
            entry = self._entries.get(doc_id)
            if entry is None:
                return None
            content = gzip.decompress(entry.compressed_data).decode("utf-8")
            if self._cache_size > 0:
                self._cache[doc_id] = content
                self._cache.move_to_end(doc_id)
                while len(self._cache) > self._cache_size:
                    self._cache.popitem(last=False)
            return content

    # ------------------------------------------------------------------ search
    def _build_pattern(self, query: str, options: SearchOptions) -> "re.Pattern":
        pattern = re.escape(query)
        if options.whole_word:
            pattern = rf"\b{pattern}\b"
        flags = 0 if options.case_sensitive else re.IGNORECASE
        return re.compile(pattern, flags)

    def search(self, query: str, options: SearchOptions = None) -> list:
        """Return :class:`SearchMatch` for every document containing *query*."""
        if not isinstance(query, str):
            raise TypeError("query must be a string")
        opts = options if options is not None else SearchOptions()
        if not query:
            return []
        regex = self._build_pattern(query, opts)
        return self._search_with_regex(regex, opts)

    def search_regex(self, pattern: str, options: SearchOptions = None) -> list:
        """Search using a raw regular expression *pattern*."""
        if not isinstance(pattern, str):
            raise TypeError("pattern must be a string")
        opts = options if options is not None else SearchOptions()
        flags = 0 if opts.case_sensitive else re.IGNORECASE
        try:
            regex = re.compile(pattern, flags)
        except re.error as exc:
            raise ValueError(f"invalid regex: {exc}") from exc
        return self._search_with_regex(regex, opts)

    def _search_with_regex(self, regex: "re.Pattern", opts: SearchOptions) -> list:
        results: list = []
        with self._lock:
            doc_ids = list(self._entries.keys())
        for doc_id in doc_ids:
            content = self.get_content(doc_id)
            if content is None:
                continue
            matches = list(regex.finditer(content))
            if not matches:
                continue
            excerpts: list = []
            for m in matches[: max(0, opts.max_excerpts_per_doc)]:
                excerpts.append(self.excerpt(content, m.start(), opts.excerpt_chars))
            results.append(
                SearchMatch(doc_id=doc_id, score=len(matches), excerpts=excerpts)
            )
        # Highest score first, deterministic tie-break on doc_id.
        results.sort(key=lambda r: (-r.score, r.doc_id))
        return results

    # ------------------------------------------------------------------ count
    def count_matches(
        self, query: str, doc_id: str = None, case_sensitive: bool = False
    ) -> int:
        """Count occurrences of *query* in a single document or the whole archive."""
        if not isinstance(query, str) or not query:
            return 0
        flags = 0 if case_sensitive else re.IGNORECASE
        regex = re.compile(re.escape(query), flags)
        if doc_id is not None:
            content = self.get_content(doc_id)
            if content is None:
                return 0
            return len(regex.findall(content))
        total = 0
        with self._lock:
            ids = list(self._entries.keys())
        for did in ids:
            content = self.get_content(did)
            if content is None:
                continue
            total += len(regex.findall(content))
        return total

    # ------------------------------------------------------------------ excerpt
    def excerpt(self, content: str, position: int, chars: int = 100) -> str:
        """Return a window of *chars* characters centred on *position*."""
        if not isinstance(content, str):
            raise TypeError("content must be a string")
        if chars <= 0:
            return ""
        if position < 0:
            position = 0
        if position > len(content):
            position = len(content)
        half = chars // 2
        start = max(0, position - half)
        end = min(len(content), position + (chars - half))
        snippet = content[start:end]
        if start > 0:
            snippet = "..." + snippet
        if end < len(content):
            snippet = snippet + "..."
        return snippet

    # ------------------------------------------------------------------ misc
    def exists(self, doc_id: str) -> bool:
        with self._lock:
            return doc_id in self._entries

    def metadata(self, doc_id: str) -> Optional[dict]:
        with self._lock:
            entry = self._entries.get(doc_id)
            return dict(entry.metadata) if entry is not None else None

    def list_doc_ids(self) -> list:
        with self._lock:
            return sorted(self._entries.keys())

    def total_compressed_size(self) -> int:
        with self._lock:
            return sum(len(e.compressed_data) for e in self._entries.values())

    def total_original_size(self) -> int:
        with self._lock:
            return sum(e.original_size for e in self._entries.values())

    @property
    def compression_ratio(self) -> float:
        original = self.total_original_size()
        if original == 0:
            return 0.0
        return self.total_compressed_size() / original

    def cache_size_used(self) -> int:
        with self._lock:
            return len(self._cache)

    def clear_cache(self) -> int:
        with self._lock:
            count = len(self._cache)
            self._cache.clear()
            return count

    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
            self._cache.clear()

    @property
    def doc_count(self) -> int:
        with self._lock:
            return len(self._entries)
