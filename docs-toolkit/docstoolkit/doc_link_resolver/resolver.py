"""DocLinkResolver — resolves wiki-style, markdown, anchor and reference links between documents."""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class LinkStyle(Enum):
    """Style of an internal document link."""

    WIKI = "wiki"
    MARKDOWN = "markdown"
    ANCHOR = "anchor"
    REFERENCE = "reference"


@dataclass
class LinkResolution:
    """Result of resolving a single link occurrence."""

    original: str
    target_doc_id: Optional[str]
    anchor: Optional[str]
    is_resolved: bool
    style: LinkStyle
    error: Optional[str] = None


@dataclass
class LinkExtraction:
    """Collection of raw links and their resolutions for a source document."""

    source_doc_id: str
    links: list = field(default_factory=list)  # list[tuple[str, int]]
    resolutions: list = field(default_factory=list)  # list[LinkResolution]


# Regex patterns.
_WIKI_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")
# Reference must be matched before markdown so [text][ref] doesn't grab as markdown.
_REFERENCE_RE = re.compile(r"\[([^\]]+)\]\[([^\]]+)\]")
_MARKDOWN_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


class DocLinkResolver:
    """Resolves internal document references to canonical doc IDs.

    Supports wiki-style ``[[Page]]``, markdown ``[text](url)``,
    in-doc anchors ``#section`` and reference-style ``[text][ref]``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        # doc_id -> {"title": str, "aliases": list[str]}
        self._docs: dict = {}
        # lowercased title/alias -> doc_id (for fast reverse lookup)
        self._title_index: dict = {}
        # doc_id -> set of anchor ids
        self._anchors: dict = {}
        # ref name (lowercased) -> (doc_id, anchor or None)
        self._references: dict = {}

    # ------------------------------------------------------------------ docs

    def register_doc(
        self,
        doc_id: str,
        title: Optional[str] = None,
        aliases: Optional[list] = None,
    ) -> bool:
        """Register a document. Returns False if doc_id already exists."""
        if not doc_id:
            return False
        with self._lock:
            if doc_id in self._docs:
                return False
            t = title if title is not None else doc_id
            a = list(aliases) if aliases else []
            self._docs[doc_id] = {"title": t, "aliases": a}
            self._title_index[t.lower()] = doc_id
            self._title_index[doc_id.lower()] = doc_id
            for alias in a:
                self._title_index[alias.lower()] = doc_id
            self._anchors.setdefault(doc_id, set())
            return True

    def unregister_doc(self, doc_id: str) -> bool:
        """Remove a document and its associated indices."""
        with self._lock:
            if doc_id not in self._docs:
                return False
            meta = self._docs.pop(doc_id)
            # Clean title index entries pointing to this doc_id
            keys_to_remove = [
                k for k, v in self._title_index.items() if v == doc_id
            ]
            for k in keys_to_remove:
                del self._title_index[k]
            self._anchors.pop(doc_id, None)
            # Drop references targeting this doc
            ref_keys = [
                k for k, (did, _) in self._references.items() if did == doc_id
            ]
            for k in ref_keys:
                del self._references[k]
            _ = meta
            return True

    def add_alias(self, doc_id: str, alias: str) -> bool:
        """Attach an additional alias to an existing document."""
        if not alias:
            return False
        with self._lock:
            if doc_id not in self._docs:
                return False
            if alias in self._docs[doc_id]["aliases"]:
                return False
            self._docs[doc_id]["aliases"].append(alias)
            self._title_index[alias.lower()] = doc_id
            return True

    # ----------------------------------------------------------- resolution

    def resolve_wiki(self, text: str) -> Optional[str]:
        """Resolve ``[[Page]]`` text — accepts either the raw target or full ``[[...]]`` form."""
        if not text:
            return None
        s = text.strip()
        m = _WIKI_RE.match(s)
        if m:
            target = m.group(1).strip()
        else:
            # raw target name passed
            target = s
        if not target:
            return None
        # Strip embedded anchor if present.
        if "#" in target:
            target = target.split("#", 1)[0].strip()
            if not target:
                return None
        with self._lock:
            return self._title_index.get(target.lower())

    def resolve_markdown(
        self, url: str, current_doc_id: Optional[str] = None
    ) -> Optional[str]:
        """Resolve a markdown URL such as ``foo.md``, ``../foo.md`` or ``/abs/foo.md``."""
        if not url:
            return None
        u = url.strip()
        if not u:
            return None
        # Pure anchor: refers to current doc.
        if u.startswith("#"):
            if current_doc_id and current_doc_id in self._docs:
                return current_doc_id
            return None
        # Strip anchor portion.
        anchor = None
        if "#" in u:
            u, anchor = u.split("#", 1)
            _ = anchor
        if not u:
            if current_doc_id and current_doc_id in self._docs:
                return current_doc_id
            return None
        # External URL.
        if u.startswith(("http://", "https://", "mailto:", "ftp://")):
            return None
        # Normalise path components: strip leading "./" or "/" and parent ".." segments.
        parts = [p for p in u.replace("\\", "/").split("/") if p and p != "."]
        # Process ".." parents (we just keep the basename for matching).
        cleaned = []
        for p in parts:
            if p == "..":
                if cleaned:
                    cleaned.pop()
            else:
                cleaned.append(p)
        if not cleaned:
            return None
        # Strip .md/.markdown suffix from final.
        last = cleaned[-1]
        for suffix in (".md", ".markdown"):
            if last.lower().endswith(suffix):
                last = last[: -len(suffix)]
                break
        cleaned[-1] = last
        # Try the full path as doc_id (without extension) then progressively shorter forms.
        candidates = ["/".join(cleaned), last]
        with self._lock:
            for cand in candidates:
                if cand in self._docs:
                    return cand
                hit = self._title_index.get(cand.lower())
                if hit:
                    return hit
        return None

    def resolve_anchor(
        self, anchor: str, current_doc_id: Optional[str] = None
    ) -> Optional[tuple]:
        """Resolve an anchor like ``#intro`` or ``doc-id#intro`` to ``(doc_id, anchor_id)``."""
        if not anchor:
            return None
        a = anchor.strip()
        if not a:
            return None
        if a.startswith("#"):
            anchor_id = a[1:].strip()
            doc_id = current_doc_id
        elif "#" in a:
            doc_part, anchor_id = a.split("#", 1)
            doc_part = doc_part.strip()
            anchor_id = anchor_id.strip()
            with self._lock:
                if doc_part in self._docs:
                    doc_id = doc_part
                else:
                    doc_id = self._title_index.get(doc_part.lower())
        else:
            return None
        if not anchor_id or not doc_id:
            return None
        with self._lock:
            if doc_id not in self._docs:
                return None
            anchors = self._anchors.get(doc_id, set())
            if anchor_id in anchors:
                return (doc_id, anchor_id)
        return None

    def resolve_reference(self, ref: str) -> Optional[str]:
        """Resolve a custom reference label registered via :meth:`register_reference`."""
        if not ref:
            return None
        with self._lock:
            entry = self._references.get(ref.strip().lower())
            if not entry:
                return None
            return entry[0]

    def register_reference(
        self, ref_name: str, doc_id: str, anchor: Optional[str] = None
    ) -> bool:
        """Register a reference label pointing to a (doc_id, optional anchor) target."""
        if not ref_name or not doc_id:
            return False
        with self._lock:
            if doc_id not in self._docs:
                return False
            self._references[ref_name.strip().lower()] = (doc_id, anchor)
            return True

    def register_anchor(
        self,
        doc_id: str,
        anchor_id: str,
        anchor_text: Optional[str] = None,
    ) -> bool:
        """Register an anchor inside a registered document."""
        if not anchor_id:
            return False
        with self._lock:
            if doc_id not in self._docs:
                return False
            self._anchors.setdefault(doc_id, set()).add(anchor_id)
            _ = anchor_text
            return True

    # ------------------------------------------------------- bulk operations

    def extract_links(
        self, content: str, source_doc_id: str = "doc"
    ) -> LinkExtraction:
        """Extract all link occurrences and their resolutions from ``content``."""
        extraction = LinkExtraction(source_doc_id=source_doc_id, links=[], resolutions=[])
        if not content:
            return extraction

        # Collect (offset, kind, match) so we can resolve in order without overlaps.
        # Reference style first since [text][ref] would also satisfy markdown regex partially.
        seen_spans: list = []

        def _overlaps(start: int, end: int) -> bool:
            for s, e in seen_spans:
                if start < e and end > s:
                    return True
            return False

        # Wiki
        for m in _WIKI_RE.finditer(content):
            seen_spans.append((m.start(), m.end()))
            raw_text = m.group(0)
            target = m.group(1).strip()
            extraction.links.append((raw_text, m.start()))
            anchor = None
            if "#" in target:
                target, anchor = target.split("#", 1)
                target = target.strip()
                anchor = anchor.strip() or None
            doc_id = self.resolve_wiki(target) if target else None
            res = LinkResolution(
                original=raw_text,
                target_doc_id=doc_id,
                anchor=anchor,
                is_resolved=doc_id is not None,
                style=LinkStyle.WIKI,
                error=None if doc_id else "wiki target not registered",
            )
            extraction.resolutions.append(res)

        # Reference style
        for m in _REFERENCE_RE.finditer(content):
            if _overlaps(m.start(), m.end()):
                continue
            seen_spans.append((m.start(), m.end()))
            raw_text = m.group(0)
            ref_name = m.group(2).strip()
            extraction.links.append((raw_text, m.start()))
            doc_id = self.resolve_reference(ref_name)
            anchor = None
            if doc_id is not None:
                with self._lock:
                    entry = self._references.get(ref_name.lower())
                if entry:
                    anchor = entry[1]
            res = LinkResolution(
                original=raw_text,
                target_doc_id=doc_id,
                anchor=anchor,
                is_resolved=doc_id is not None,
                style=LinkStyle.REFERENCE,
                error=None if doc_id else "reference not registered",
            )
            extraction.resolutions.append(res)

        # Markdown
        for m in _MARKDOWN_RE.finditer(content):
            if _overlaps(m.start(), m.end()):
                continue
            seen_spans.append((m.start(), m.end()))
            raw_text = m.group(0)
            url = m.group(2).strip()
            extraction.links.append((raw_text, m.start()))

            anchor = None
            style = LinkStyle.MARKDOWN
            doc_id: Optional[str] = None
            err: Optional[str] = None

            if not url:
                err = "empty url"
            elif url.startswith("#"):
                style = LinkStyle.ANCHOR
                anchor = url[1:].strip() or None
                doc_id = source_doc_id if source_doc_id in self._docs else None
                if doc_id is None:
                    err = "source doc not registered"
                elif anchor and anchor not in self._anchors.get(doc_id, set()):
                    # Resolution still considered unresolved when anchor missing.
                    err = "anchor not registered"
                    doc_id = None
            elif url.startswith(("http://", "https://", "mailto:", "ftp://")):
                err = "external url"
            else:
                if "#" in url:
                    base, anchor = url.split("#", 1)
                    anchor = anchor.strip() or None
                    url_for_lookup = base
                else:
                    url_for_lookup = url
                doc_id = self.resolve_markdown(url_for_lookup, current_doc_id=source_doc_id)
                if doc_id is None and url_for_lookup:
                    err = "markdown target not registered"
                elif doc_id is not None and anchor is not None:
                    if anchor not in self._anchors.get(doc_id, set()):
                        err = "anchor not registered"
                        doc_id = None

            res = LinkResolution(
                original=raw_text,
                target_doc_id=doc_id,
                anchor=anchor,
                is_resolved=doc_id is not None,
                style=style,
                error=err,
            )
            extraction.resolutions.append(res)

        # Sort by offset to preserve document order
        order = sorted(range(len(extraction.links)), key=lambda i: extraction.links[i][1])
        extraction.links = [extraction.links[i] for i in order]
        extraction.resolutions = [extraction.resolutions[i] for i in order]
        return extraction

    def resolve_all_links(
        self, content: str, source_doc_id: str = "doc"
    ) -> list:
        """Return all link resolutions for ``content`` in document order."""
        return self.extract_links(content, source_doc_id=source_doc_id).resolutions

    def broken_links(
        self, content: str, source_doc_id: str = "doc"
    ) -> list:
        """Return only unresolved link resolutions."""
        return [r for r in self.resolve_all_links(content, source_doc_id) if not r.is_resolved]

    # ------------------------------------------------------- generators

    def link_to(
        self,
        source: str,
        target: str,
        style: LinkStyle = LinkStyle.MARKDOWN,
    ) -> str:
        """Generate link syntax for an existing document.

        ``source`` is the display text and ``target`` is a registered doc_id (or title/alias).
        Falls back to producing a link with the target as both label and target if not found.
        """
        with self._lock:
            if target in self._docs:
                doc_id = target
            else:
                doc_id = self._title_index.get(target.lower(), target)
        if style == LinkStyle.WIKI:
            title = None
            with self._lock:
                if doc_id in self._docs:
                    title = self._docs[doc_id]["title"]
            label = title or doc_id
            if source and source != label:
                return f"[[{label}|{source}]]"
            return f"[[{label}]]"
        if style == LinkStyle.ANCHOR:
            return f"[{source}](#{doc_id})"
        if style == LinkStyle.REFERENCE:
            return f"[{source}][{doc_id}]"
        return f"[{source}]({doc_id}.md)"

    # ------------------------------------------------------- lookups

    def title_for(self, doc_id: str) -> Optional[str]:
        with self._lock:
            entry = self._docs.get(doc_id)
            return entry["title"] if entry else None

    def id_for_title(self, title: str) -> Optional[str]:
        if not title:
            return None
        with self._lock:
            return self._title_index.get(title.lower())

    def aliases_for(self, doc_id: str) -> list:
        with self._lock:
            entry = self._docs.get(doc_id)
            if not entry:
                return []
            return list(entry["aliases"])

    @property
    def total_docs(self) -> int:
        with self._lock:
            return len(self._docs)

    def clear(self) -> None:
        with self._lock:
            self._docs.clear()
            self._title_index.clear()
            self._anchors.clear()
            self._references.clear()
