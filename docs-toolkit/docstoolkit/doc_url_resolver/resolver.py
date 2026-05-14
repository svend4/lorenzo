"""DocUrlResolver — map document URLs to canonical doc IDs.

A single doc may have several URLs (mirrors, shortlinks, canonical), but at
most one URL is marked primary at any time.  The resolver tracks both the
forward mapping (``url -> doc_id``) and the inverse (``doc_id -> {urls}``)
plus the elected primary per doc.

Pure stdlib, thread-safe via a single :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Optional


@dataclass
class UrlMapping:
    """A single URL mapped to a doc ID."""

    url: str
    doc_id: str
    is_primary: bool = True
    created_at: float = 0.0


@dataclass
class ResolverStats:
    """Aggregate statistics about the resolver state."""

    total_mappings: int
    unique_docs: int
    unique_urls: int
    primary_count: int


class DocUrlResolver:
    """Maintain mappings between URLs and canonical doc IDs.

    Storage layout:
      * ``_url_to_doc``    — ``url -> UrlMapping``
      * ``_doc_to_urls``   — ``doc_id -> set[str]``
      * ``_primary_url``   — ``doc_id -> primary_url`` (≤ 1 primary per doc)
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._url_to_doc: dict[str, UrlMapping] = {}
        self._doc_to_urls: dict[str, set[str]] = {}
        self._primary_url: dict[str, str] = {}

    # ---------------------------------------------------------------- mutation

    def map_url(
        self,
        url: str,
        doc_id: str,
        is_primary: bool = False,
        now: Optional[float] = None,
    ) -> UrlMapping:
        """Create or replace the mapping for ``url``.

        If ``is_primary`` is true the existing primary for the same doc is
        demoted.  If the URL was previously mapped to a different doc, that
        prior mapping is removed (and its primary cleared if it was primary).
        """
        ts = now if now is not None else time.time()
        with self._lock:
            # Remove any prior mapping for this URL (possibly different doc).
            prior = self._url_to_doc.get(url)
            if prior is not None:
                old_doc = prior.doc_id
                urls = self._doc_to_urls.get(old_doc)
                if urls is not None:
                    urls.discard(url)
                    if not urls:
                        del self._doc_to_urls[old_doc]
                if self._primary_url.get(old_doc) == url:
                    del self._primary_url[old_doc]

            mapping = UrlMapping(
                url=url, doc_id=doc_id, is_primary=is_primary, created_at=ts
            )
            self._url_to_doc[url] = mapping
            self._doc_to_urls.setdefault(doc_id, set()).add(url)

            if is_primary:
                # Demote whatever was primary before for this doc.
                prev_primary = self._primary_url.get(doc_id)
                if prev_primary is not None and prev_primary != url:
                    prev = self._url_to_doc.get(prev_primary)
                    if prev is not None:
                        prev.is_primary = False
                self._primary_url[doc_id] = url
            else:
                mapping.is_primary = False

            return mapping

    def set_primary(self, url: str) -> bool:
        """Promote ``url`` to be the primary for its doc.

        Demotes any current primary for the same doc.  Returns ``True`` if
        the mapping exists, ``False`` otherwise.
        """
        with self._lock:
            mapping = self._url_to_doc.get(url)
            if mapping is None:
                return False
            doc_id = mapping.doc_id
            prev = self._primary_url.get(doc_id)
            if prev is not None and prev != url:
                prev_mapping = self._url_to_doc.get(prev)
                if prev_mapping is not None:
                    prev_mapping.is_primary = False
            mapping.is_primary = True
            self._primary_url[doc_id] = url
            return True

    def unmap_url(self, url: str) -> bool:
        """Remove a single URL mapping.  Returns ``True`` if it existed."""
        with self._lock:
            mapping = self._url_to_doc.pop(url, None)
            if mapping is None:
                return False
            doc_id = mapping.doc_id
            urls = self._doc_to_urls.get(doc_id)
            if urls is not None:
                urls.discard(url)
                if not urls:
                    del self._doc_to_urls[doc_id]
            if self._primary_url.get(doc_id) == url:
                del self._primary_url[doc_id]
            return True

    def unmap_doc(self, doc_id: str) -> int:
        """Remove all URLs for a doc.  Returns the number removed."""
        with self._lock:
            urls = self._doc_to_urls.pop(doc_id, set())
            for u in urls:
                self._url_to_doc.pop(u, None)
            self._primary_url.pop(doc_id, None)
            return len(urls)

    # ------------------------------------------------------------------ lookup

    def resolve(self, url: str) -> Optional[str]:
        """Return the doc ID mapped to ``url`` or ``None``."""
        with self._lock:
            mapping = self._url_to_doc.get(url)
            return mapping.doc_id if mapping is not None else None

    def primary_url_for(self, doc_id: str) -> Optional[str]:
        """Return the primary URL for ``doc_id`` or ``None``."""
        with self._lock:
            return self._primary_url.get(doc_id)

    def urls_for(self, doc_id: str) -> list[str]:
        """Return sorted URLs known for ``doc_id``."""
        with self._lock:
            return sorted(self._doc_to_urls.get(doc_id, set()))

    def get_mapping(self, url: str) -> Optional[UrlMapping]:
        """Return the :class:`UrlMapping` for ``url`` or ``None``."""
        with self._lock:
            return self._url_to_doc.get(url)

    # --------------------------------------------------------------- inventory

    def all_urls(self) -> list[str]:
        """All known URLs, sorted."""
        with self._lock:
            return sorted(self._url_to_doc.keys())

    def all_doc_ids(self) -> list[str]:
        """All doc IDs that currently have at least one URL, sorted."""
        with self._lock:
            return sorted(self._doc_to_urls.keys())

    # ----------------------------------------------------------------- cleanup

    def clear(self) -> int:
        """Drop all mappings.  Returns the count of mappings cleared."""
        with self._lock:
            n = len(self._url_to_doc)
            self._url_to_doc.clear()
            self._doc_to_urls.clear()
            self._primary_url.clear()
            return n

    # ------------------------------------------------------------------- stats

    def stats(self) -> ResolverStats:
        """Snapshot of size/cardinality counters."""
        with self._lock:
            return ResolverStats(
                total_mappings=len(self._url_to_doc),
                unique_docs=len(self._doc_to_urls),
                unique_urls=len(self._url_to_doc),
                primary_count=len(self._primary_url),
            )
