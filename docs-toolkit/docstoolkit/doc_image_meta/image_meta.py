"""Image metadata extraction for markdown docs (E221).

Extracts image references of the form ``![alt](url "title")`` from markdown
documents, tracks per-doc usage, validates alt text, and computes
image-to-doc relationships.

Stdlib only: ``re`` and ``threading``.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Optional


# Markdown image: ![alt](url "title")
# alt: group 1 (may be empty)
# url: group 2 (any non-")" chars, non-greedy)
# title: group 3 (optional, in double quotes after whitespace)
_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]*)")?\)')


@dataclass
class ImageRef:
    """A single image reference inside a markdown doc."""

    url: str
    alt_text: str = ""
    title: str = ""
    is_remote: bool = False
    line_num: int = 0


@dataclass
class ImageReport:
    """Result of scanning a single document for image references."""

    doc_id: str
    images: list[ImageRef] = field(default_factory=list)

    @property
    def image_count(self) -> int:
        return len(self.images)

    @property
    def missing_alt_count(self) -> int:
        return sum(1 for img in self.images if not img.alt_text)

    @property
    def remote_count(self) -> int:
        return sum(1 for img in self.images if img.is_remote)

    @property
    def local_count(self) -> int:
        return sum(1 for img in self.images if not img.is_remote)

    @property
    def unique_urls(self) -> set[str]:
        return {img.url for img in self.images}


@dataclass
class ImageUsage:
    """Aggregated usage info for a single image URL across docs."""

    url: str
    doc_ids: set[str] = field(default_factory=set)
    usage_count: int = 0


def _is_remote(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")


class DocImageMeta:
    """Indexes image references across multiple markdown documents."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # doc_id -> list[ImageRef]
        self._doc_refs: dict[str, list[ImageRef]] = {}
        # url -> ImageUsage (doc_ids + total usage_count across docs)
        self._usage: dict[str, ImageUsage] = {}

    # ---- core extraction ----

    def extract_images(self, content: str) -> list[ImageRef]:
        """Return all image refs found in ``content`` (does not mutate state)."""
        refs: list[ImageRef] = []
        if not content:
            return refs
        # Determine the line number for each match using the offset of the start.
        # Precompute prefix line counts via splitlines positions.
        # Simpler approach: iterate matches and count newlines in content[:start].
        for m in _IMAGE_RE.finditer(content):
            alt = m.group(1) or ""
            url = m.group(2) or ""
            title = m.group(3) or ""
            line_num = content.count("\n", 0, m.start()) + 1
            refs.append(
                ImageRef(
                    url=url,
                    alt_text=alt,
                    title=title,
                    is_remote=_is_remote(url),
                    line_num=line_num,
                )
            )
        return refs

    # ---- scanning / state mutation ----

    def scan(self, doc_id: str, content: str) -> ImageReport:
        """Scan a single doc, updating the internal usage index.

        Re-scanning the same ``doc_id`` replaces all previous entries for that doc.
        """
        refs = self.extract_images(content)
        with self._lock:
            # Remove any previous contribution of this doc to the usage index.
            self._remove_doc_locked(doc_id)
            # Insert the new refs.
            self._doc_refs[doc_id] = list(refs)
            for ref in refs:
                u = self._usage.get(ref.url)
                if u is None:
                    u = ImageUsage(url=ref.url)
                    self._usage[ref.url] = u
                u.doc_ids.add(doc_id)
                u.usage_count += 1
        return ImageReport(doc_id=doc_id, images=refs)

    def scan_batch(self, docs: dict[str, str]) -> list[ImageReport]:
        """Scan many docs; returns one ``ImageReport`` per input doc."""
        return [self.scan(doc_id, content) for doc_id, content in docs.items()]

    # ---- queries ----

    def usage(self, url: str) -> Optional[ImageUsage]:
        with self._lock:
            u = self._usage.get(url)
            if u is None:
                return None
            return ImageUsage(
                url=u.url,
                doc_ids=set(u.doc_ids),
                usage_count=u.usage_count,
            )

    def all_usage(self) -> list[ImageUsage]:
        with self._lock:
            return [
                ImageUsage(url=u.url, doc_ids=set(u.doc_ids), usage_count=u.usage_count)
                for u in self._usage.values()
            ]

    def unused_images(self, used_urls: set[str]) -> list[str]:
        """Return URLs known to this index but not present in ``used_urls``."""
        with self._lock:
            return [url for url in self._usage.keys() if url not in used_urls]

    def docs_using(self, url: str) -> list[str]:
        with self._lock:
            u = self._usage.get(url)
            if u is None:
                return []
            return sorted(u.doc_ids)

    def validate_alt(self, report: ImageReport) -> list[ImageRef]:
        """Return images in ``report`` with empty alt text."""
        return [img for img in report.images if not img.alt_text]

    def top_used(self, top_k: int = 10) -> list[ImageUsage]:
        with self._lock:
            usages = [
                ImageUsage(url=u.url, doc_ids=set(u.doc_ids), usage_count=u.usage_count)
                for u in self._usage.values()
            ]
        usages.sort(key=lambda x: (-x.usage_count, x.url))
        if top_k < 0:
            top_k = 0
        return usages[:top_k]

    def remove_doc(self, doc_id: str) -> int:
        """Remove all refs associated with ``doc_id``. Returns number removed."""
        with self._lock:
            return self._remove_doc_locked(doc_id)

    def _remove_doc_locked(self, doc_id: str) -> int:
        refs = self._doc_refs.pop(doc_id, None)
        if not refs:
            return 0
        removed = 0
        # Decrement usage counts per ref, drop entry if it falls to 0.
        for ref in refs:
            u = self._usage.get(ref.url)
            if u is None:
                continue
            u.usage_count -= 1
            removed += 1
            # The doc may have multiple refs to the same URL; only drop doc_id
            # once that doc's last ref to this URL is gone.
            still_has_url = any(
                other.url == ref.url
                for other in self._doc_refs.get(doc_id, [])
            )
            if not still_has_url:
                u.doc_ids.discard(doc_id)
            if u.usage_count <= 0 or not u.doc_ids:
                self._usage.pop(ref.url, None)
        return removed

    def total_unique_urls(self) -> int:
        with self._lock:
            return len(self._usage)

    def total_doc_image_refs(self) -> int:
        with self._lock:
            return sum(len(refs) for refs in self._doc_refs.values())

    def clear(self) -> None:
        with self._lock:
            self._doc_refs.clear()
            self._usage.clear()

    def image_stats(self) -> dict:
        with self._lock:
            total = 0
            remote = 0
            local = 0
            missing_alt = 0
            for refs in self._doc_refs.values():
                for ref in refs:
                    total += 1
                    if ref.is_remote:
                        remote += 1
                    else:
                        local += 1
                    if not ref.alt_text:
                        missing_alt += 1
            return {
                "total": total,
                "remote": remote,
                "local": local,
                "missing_alt": missing_alt,
                "unique_urls": len(self._usage),
                "docs": len(self._doc_refs),
            }
