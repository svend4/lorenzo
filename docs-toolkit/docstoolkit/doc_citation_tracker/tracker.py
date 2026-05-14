"""DocCitationTracker — tracks external URL citations used in documents."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Citation:
    """A single citation of a URL within a document."""

    citation_id: int
    doc_id: str
    url: str
    title: str = ""
    added_at: float = 0.0


@dataclass
class UrlStats:
    """Aggregated statistics for a single URL."""

    url: str
    doc_count: int        # number of distinct docs that cite this URL
    citation_count: int   # total citation records (can exceed doc_count)


@dataclass
class CitationStats:
    """Global statistics snapshot."""

    total_citations: int
    unique_urls: int
    unique_docs: int
    top_urls: list[tuple[str, int]]   # [(url, doc_count)] top 5 by doc_count


class DocCitationTracker:
    """Thread-safe tracker for external URL citations in documents."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._next_id: int = 1
        # All citations in insertion order, keyed by citation_id.
        self._by_id: dict[int, Citation] = {}
        # doc_id -> list of citation_ids (insertion order)
        self._by_doc: dict[str, list[int]] = {}
        # url -> set of doc_ids that cite it
        self._url_docs: dict[str, set[str]] = {}
        # url -> citation_ids (insertion order)
        self._url_citations: dict[str, list[int]] = {}

    # ------------------------------------------------------------------ add
    def add(
        self,
        doc_id: str,
        url: str,
        title: str = "",
        now: Optional[float] = None,
    ) -> Citation:
        """Add a citation and return the new Citation object.

        citation_id is auto-incremented globally. ``now`` overrides the
        timestamp (useful for testing); when omitted ``time.time()`` is used.
        """
        ts = now if now is not None else time.time()
        with self._lock:
            cid = self._next_id
            self._next_id += 1
            citation = Citation(
                citation_id=cid,
                doc_id=doc_id,
                url=url,
                title=title,
                added_at=ts,
            )
            self._by_id[cid] = citation
            self._by_doc.setdefault(doc_id, []).append(cid)
            self._url_docs.setdefault(url, set()).add(doc_id)
            self._url_citations.setdefault(url, []).append(cid)
        return citation

    # ------------------------------------------------------------------ queries
    def citations_for_doc(self, doc_id: str) -> list[Citation]:
        """Return all citations from *doc_id* in the order they were added."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, []))
        return [self._by_id[i] for i in ids if i in self._by_id]

    def docs_citing(self, url: str) -> list[str]:
        """Return a sorted list of doc_ids that cite *url*."""
        with self._lock:
            docs = set(self._url_docs.get(url, set()))
        return sorted(docs)

    def url_stats(self, url: str) -> Optional[UrlStats]:
        """Return statistics for *url*, or ``None`` if it has never been cited."""
        with self._lock:
            if url not in self._url_docs:
                return None
            doc_count = len(self._url_docs[url])
            citation_count = len(self._url_citations[url])
        return UrlStats(url=url, doc_count=doc_count, citation_count=citation_count)

    # ------------------------------------------------------------------ delete
    def delete(self, citation_id: int) -> bool:
        """Remove the citation with *citation_id*.

        Returns ``True`` if the citation existed and was removed, ``False``
        otherwise.
        """
        with self._lock:
            citation = self._by_id.pop(citation_id, None)
            if citation is None:
                return False
            # Remove from _by_doc list
            doc_list = self._by_doc.get(citation.doc_id, [])
            if citation_id in doc_list:
                doc_list.remove(citation_id)
            if not doc_list:
                self._by_doc.pop(citation.doc_id, None)

            # Remove from _url_citations list
            url_list = self._url_citations.get(citation.url, [])
            if citation_id in url_list:
                url_list.remove(citation_id)

            # If no more citations exist for this URL from this doc, remove
            # doc from _url_docs set.
            remaining_for_doc = any(
                self._by_id[i].doc_id == citation.doc_id
                for i in url_list
            )
            if not remaining_for_doc:
                doc_set = self._url_docs.get(citation.url, set())
                doc_set.discard(citation.doc_id)
                if not doc_set:
                    self._url_docs.pop(citation.url, None)
                    self._url_citations.pop(citation.url, None)

            return True

    def delete_doc_citations(self, doc_id: str) -> int:
        """Remove all citations from *doc_id*. Returns the number removed."""
        with self._lock:
            ids = list(self._by_doc.pop(doc_id, []))
            count = 0
            for cid in ids:
                citation = self._by_id.pop(cid, None)
                if citation is None:
                    continue
                count += 1
                url = citation.url
                url_list = self._url_citations.get(url, [])
                if cid in url_list:
                    url_list.remove(cid)
                doc_set = self._url_docs.get(url, set())
                doc_set.discard(doc_id)
                if not doc_set:
                    self._url_docs.pop(url, None)
                    self._url_citations.pop(url, None)
        return count

    # ------------------------------------------------------------------ top
    def top_cited_urls(self, limit: int = 10) -> list[UrlStats]:
        """Return the top *limit* URLs by doc_count, sorted descending."""
        with self._lock:
            snapshot = {
                url: (len(docs), len(self._url_citations.get(url, [])))
                for url, docs in self._url_docs.items()
            }
        result = [
            UrlStats(url=url, doc_count=dc, citation_count=cc)
            for url, (dc, cc) in snapshot.items()
        ]
        result.sort(key=lambda s: (-s.doc_count, s.url))
        return result[:limit]

    # ------------------------------------------------------------------ search
    def search_url(self, fragment: str) -> list[Citation]:
        """Return citations whose URL contains *fragment* (case-insensitive)."""
        needle = fragment.lower()
        with self._lock:
            matching = [
                c for c in self._by_id.values()
                if needle in c.url.lower()
            ]
        return sorted(matching, key=lambda c: c.citation_id)

    # ------------------------------------------------------------------ stats
    def stats(self) -> CitationStats:
        """Return a global statistics snapshot."""
        with self._lock:
            total = len(self._by_id)
            unique_urls = len(self._url_docs)
            unique_docs = len(self._by_doc)
            # top 5 by doc_count
            top_raw = sorted(
                self._url_docs.items(),
                key=lambda kv: (-len(kv[1]), kv[0]),
            )[:5]
            top_urls = [(url, len(docs)) for url, docs in top_raw]
        return CitationStats(
            total_citations=total,
            unique_urls=unique_urls,
            unique_docs=unique_docs,
            top_urls=top_urls,
        )

    # ------------------------------------------------------------------ property
    @property
    def total_citations(self) -> int:
        """Total number of currently tracked citations."""
        with self._lock:
            return len(self._by_id)
