"""Batch link validator for documentation with caching and skip-list (stdlib only)."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class LinkStatus(Enum):
    VALID = "valid"
    BROKEN = "broken"
    REDIRECT = "redirect"
    UNKNOWN = "unknown"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class LinkRef:
    url: str
    source_doc_id: str
    line_num: int = 0
    link_text: str = ""


@dataclass
class CheckResult:
    url: str
    status: LinkStatus
    checked_at: float = 0.0
    error: Optional[str] = None
    final_url: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class CheckReport:
    total_links: int = 0
    valid_count: int = 0
    broken_count: int = 0
    unknown_count: int = 0
    by_doc: dict[str, list[CheckResult]] = field(default_factory=dict)
    broken_links: list[LinkRef] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Default stub checker
# ---------------------------------------------------------------------------

def stub_checker(url: str) -> CheckResult:
    """Default checker that returns VALID for everything except urls beginning with 'broken:'."""
    if url.startswith("broken:"):
        return CheckResult(url=url, status=LinkStatus.BROKEN, error="stub broken")
    return CheckResult(url=url, status=LinkStatus.VALID)


# ---------------------------------------------------------------------------
# Markdown link regex
# ---------------------------------------------------------------------------

_INLINE_LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------

class DocLinkCheck:
    """Validates internal/external doc links in batch with cache, parallelism, and reports."""

    def __init__(
        self,
        checker: Optional[Callable[[str], CheckResult]] = None,
        cache_ttl: float = 3600.0,
    ) -> None:
        self._checker: Callable[[str], CheckResult] = checker or stub_checker
        self._cache_ttl: float = float(cache_ttl)
        self._lock = threading.Lock()
        # doc_id -> list[LinkRef]
        self._docs: dict[str, list[LinkRef]] = {}
        # url -> (CheckResult, expires_at)
        self._cache: dict[str, tuple[CheckResult, float]] = {}
        # set of skipped URLs
        self._skip: set[str] = set()
        # total number of checker invocations (not cache hits)
        self._checks_run: int = 0

    # ------------------------------------------------------------------
    # Extraction
    # ------------------------------------------------------------------

    def extract_links(self, content: str) -> list[str]:
        """Extract URLs from inline markdown links [text](url)."""
        urls: list[str] = []
        for m in _INLINE_LINK_RE.finditer(content):
            url = m.group(2).strip()
            if url:
                urls.append(url)
        return urls

    def _extract_link_refs(self, doc_id: str, content: str) -> list[LinkRef]:
        refs: list[LinkRef] = []
        for m in _INLINE_LINK_RE.finditer(content):
            url = m.group(2).strip()
            if not url:
                continue
            text = m.group(1)
            line_num = content[: m.start()].count('\n') + 1
            refs.append(LinkRef(url=url, source_doc_id=doc_id, line_num=line_num, link_text=text))
        return refs

    # ------------------------------------------------------------------
    # Doc registration
    # ------------------------------------------------------------------

    def register_doc(self, doc_id: str, content: str) -> int:
        """Extract links from *content* and store them under *doc_id*. Returns count."""
        refs = self._extract_link_refs(doc_id, content)
        with self._lock:
            self._docs[doc_id] = refs
        return len(refs)

    def unregister_doc(self, doc_id: str) -> bool:
        with self._lock:
            if doc_id in self._docs:
                del self._docs[doc_id]
                return True
            return False

    def links_for_doc(self, doc_id: str) -> list[LinkRef]:
        with self._lock:
            return list(self._docs.get(doc_id, []))

    # ------------------------------------------------------------------
    # Skip list
    # ------------------------------------------------------------------

    def skip_url(self, url: str) -> bool:
        with self._lock:
            if url in self._skip:
                return False
            self._skip.add(url)
            return True

    def unskip_url(self, url: str) -> bool:
        with self._lock:
            if url in self._skip:
                self._skip.remove(url)
                return True
            return False

    def is_skipped(self, url: str) -> bool:
        with self._lock:
            return url in self._skip

    # ------------------------------------------------------------------
    # Cache access
    # ------------------------------------------------------------------

    def cached_result(self, url: str, now: float = 0.0) -> Optional[CheckResult]:
        with self._lock:
            entry = self._cache.get(url)
            if entry is None:
                return None
            result, expires_at = entry
            if now >= expires_at:
                return None
            return result

    def clear_cache(self) -> int:
        with self._lock:
            n = len(self._cache)
            self._cache.clear()
            return n

    def set_checker(self, checker: Callable[[str], CheckResult]) -> None:
        with self._lock:
            self._checker = checker

    # ------------------------------------------------------------------
    # Checking
    # ------------------------------------------------------------------

    def check_link(self, url: str, now: float = 0.0, force: bool = False) -> CheckResult:
        # Skipped URLs short-circuit, no checker call, no caching.
        with self._lock:
            if url in self._skip:
                return CheckResult(url=url, status=LinkStatus.SKIPPED, checked_at=now)

            if not force:
                entry = self._cache.get(url)
                if entry is not None:
                    result, expires_at = entry
                    if now < expires_at:
                        return result

            checker = self._checker

        # Call checker outside the lock to allow parallelism.
        result = checker(url)
        if result.checked_at == 0.0:
            result.checked_at = now

        with self._lock:
            self._cache[url] = (result, now + self._cache_ttl)
            self._checks_run += 1

        return result

    def check_doc(self, doc_id: str, now: float = 0.0, force: bool = False) -> list[CheckResult]:
        refs = self.links_for_doc(doc_id)
        results: list[CheckResult] = []
        for ref in refs:
            results.append(self.check_link(ref.url, now=now, force=force))
        return results

    def check_all_links(self, now: float = 0.0, force: bool = False) -> CheckReport:
        with self._lock:
            doc_ids = list(self._docs.keys())
            doc_refs: dict[str, list[LinkRef]] = {d: list(self._docs[d]) for d in doc_ids}

        report = CheckReport()
        for doc_id in doc_ids:
            doc_results: list[CheckResult] = []
            for ref in doc_refs[doc_id]:
                result = self.check_link(ref.url, now=now, force=force)
                doc_results.append(result)
                report.total_links += 1
                if result.status == LinkStatus.VALID:
                    report.valid_count += 1
                elif result.status == LinkStatus.BROKEN:
                    report.broken_count += 1
                    report.broken_links.append(ref)
                elif result.status == LinkStatus.UNKNOWN:
                    report.unknown_count += 1
            report.by_doc[doc_id] = doc_results
        return report

    def broken_links_for_doc(self, doc_id: str) -> list[LinkRef]:
        """Return refs whose cached status is BROKEN (no checker call)."""
        broken: list[LinkRef] = []
        with self._lock:
            refs = list(self._docs.get(doc_id, []))
            for ref in refs:
                entry = self._cache.get(ref.url)
                if entry is None:
                    continue
                result, _expires = entry
                if result.status == LinkStatus.BROKEN:
                    broken.append(ref)
        return broken

    # ------------------------------------------------------------------
    # Stats / lifecycle
    # ------------------------------------------------------------------

    @property
    def total_links(self) -> int:
        with self._lock:
            return sum(len(refs) for refs in self._docs.values())

    @property
    def total_docs(self) -> int:
        with self._lock:
            return len(self._docs)

    @property
    def total_checks_run(self) -> int:
        with self._lock:
            return self._checks_run

    def clear(self) -> None:
        with self._lock:
            self._docs.clear()
            self._cache.clear()
            self._skip.clear()
            self._checks_run = 0
