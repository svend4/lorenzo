"""E363 DocLinkValidator implementation.

A thread-safe, pure-stdlib utility that records the outcome of validating
hyperlinks found in documents.  The validator does *not* perform any
network I/O itself — callers obtain the validity verdict elsewhere and
record it via :meth:`DocLinkValidator.record_check`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class LinkCheck:
    """Result of a single link validation."""

    url: str
    doc_id: str
    checked_at: float = 0.0
    valid: bool = True
    error: str = ""
    link_type: str = "external"  # "external", "internal", "anchor", "mailto"


@dataclass
class ValidatorStats:
    """Aggregate statistics over recorded link checks."""

    total_checks: int
    valid_count: int
    invalid_count: int
    unique_urls: int


class DocLinkValidator:
    """Thread-safe registry of link-validation results.

    The validator keeps an ordered list of :class:`LinkCheck` records plus
    two secondary indexes (``url`` → indices, ``doc_id`` → indices) for
    fast lookup.  All public methods acquire an internal lock so that
    concurrent callers can record checks safely.
    """

    def __init__(self) -> None:
        self._checks: List[LinkCheck] = []
        self._by_url: Dict[str, List[int]] = {}
        self._by_doc: Dict[str, List[int]] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    def classify_link(self, url: str) -> str:
        """Classify ``url`` into one of the four link types."""
        if url.startswith("mailto:"):
            return "mailto"
        if url.startswith("#"):
            return "anchor"
        if url.startswith("/"):
            return "internal"
        if "://" not in url:
            return "internal"
        return "external"

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record_check(
        self,
        url: str,
        doc_id: str,
        valid: bool,
        error: str = "",
        now: Optional[float] = None,
    ) -> LinkCheck:
        """Record a validation outcome and return the stored :class:`LinkCheck`."""
        ts = time.time() if now is None else float(now)
        link_type = self.classify_link(url)
        check = LinkCheck(
            url=url,
            doc_id=doc_id,
            checked_at=ts,
            valid=bool(valid),
            error=error,
            link_type=link_type,
        )
        with self._lock:
            idx = len(self._checks)
            self._checks.append(check)
            self._by_url.setdefault(url, []).append(idx)
            self._by_doc.setdefault(doc_id, []).append(idx)
        return check

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def checks_for_url(self, url: str) -> List[LinkCheck]:
        """Return all checks for ``url`` sorted by ``checked_at`` descending."""
        with self._lock:
            indices = list(self._by_url.get(url, []))
            items = [self._checks[i] for i in indices]
        items.sort(key=lambda c: c.checked_at, reverse=True)
        return items

    def checks_for_doc(self, doc_id: str) -> List[LinkCheck]:
        """Return all checks for ``doc_id`` sorted by ``checked_at`` descending."""
        with self._lock:
            indices = list(self._by_doc.get(doc_id, []))
            items = [self._checks[i] for i in indices]
        items.sort(key=lambda c: c.checked_at, reverse=True)
        return items

    def latest_for_url(self, url: str) -> Optional[LinkCheck]:
        """Return the most recent check for ``url`` or ``None`` if absent."""
        with self._lock:
            indices = self._by_url.get(url)
            if not indices:
                return None
            items = [self._checks[i] for i in indices]
        items.sort(key=lambda c: c.checked_at, reverse=True)
        return items[0]

    def _latest_per_url(self) -> List[LinkCheck]:
        """Return the latest check for every URL (snapshot, no sort)."""
        with self._lock:
            urls = list(self._by_url.keys())
            indices_map = {u: list(self._by_url[u]) for u in urls}
            checks_snapshot = list(self._checks)

        latest: List[LinkCheck] = []
        for url in urls:
            items = [checks_snapshot[i] for i in indices_map[url]]
            items.sort(key=lambda c: c.checked_at, reverse=True)
            latest.append(items[0])
        return latest

    def invalid_links(self) -> List[LinkCheck]:
        """Return latest-per-URL checks that are invalid, sorted by URL."""
        result = [c for c in self._latest_per_url() if not c.valid]
        result.sort(key=lambda c: c.url)
        return result

    def valid_links(self) -> List[LinkCheck]:
        """Return latest-per-URL checks that are valid, sorted by URL."""
        result = [c for c in self._latest_per_url() if c.valid]
        result.sort(key=lambda c: c.url)
        return result

    def unique_urls(self) -> List[str]:
        """Return all URLs ever checked, sorted alphabetically."""
        with self._lock:
            urls = list(self._by_url.keys())
        urls.sort()
        return urls

    def broken_urls(self) -> List[str]:
        """Return URLs whose latest check is invalid, sorted alphabetically."""
        urls = [c.url for c in self._latest_per_url() if not c.valid]
        urls.sort()
        return urls

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear_checks_for_doc(self, doc_id: str) -> int:
        """Remove all checks associated with ``doc_id`` and return the count."""
        with self._lock:
            indices = self._by_doc.pop(doc_id, [])
            if not indices:
                return 0
            removed = set(indices)
            count = len(removed)
            new_checks: List[LinkCheck] = []
            old_to_new: Dict[int, int] = {}
            for old_idx, check in enumerate(self._checks):
                if old_idx in removed:
                    continue
                old_to_new[old_idx] = len(new_checks)
                new_checks.append(check)
            self._checks = new_checks

            # Rebuild url index using the surviving indices.
            new_by_url: Dict[str, List[int]] = {}
            for url, idxs in self._by_url.items():
                surviving = [old_to_new[i] for i in idxs if i in old_to_new]
                if surviving:
                    new_by_url[url] = surviving
            self._by_url = new_by_url

            # Rebuild doc index using the surviving indices.
            new_by_doc: Dict[str, List[int]] = {}
            for did, idxs in self._by_doc.items():
                surviving = [old_to_new[i] for i in idxs if i in old_to_new]
                if surviving:
                    new_by_doc[did] = surviving
            self._by_doc = new_by_doc

            return count

    def clear_all(self) -> int:
        """Remove all recorded checks and return the count cleared."""
        with self._lock:
            count = len(self._checks)
            self._checks = []
            self._by_url = {}
            self._by_doc = {}
            return count

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> ValidatorStats:
        """Return aggregate :class:`ValidatorStats` for the current state."""
        with self._lock:
            total = len(self._checks)
            valid = sum(1 for c in self._checks if c.valid)
            invalid = total - valid
            unique = len(self._by_url)
        return ValidatorStats(
            total_checks=total,
            valid_count=valid,
            invalid_count=invalid,
            unique_urls=unique,
        )
