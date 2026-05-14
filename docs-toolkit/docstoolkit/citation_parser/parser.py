"""citation_parser — extracts and parses citations/references from markdown documents.

Supports: URLs, DOIs, arXiv IDs, GitHub links, footnote refs, and inline refs.
Stdlib only — no external dependencies.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Enum
# ---------------------------------------------------------------------------

class CitationType(Enum):
    URL = "url"
    DOI = "doi"
    ARXIV = "arxiv"
    GITHUB = "github"
    FOOTNOTE = "footnote"
    INLINE_REF = "inline_ref"
    BARE_URL = "bare_url"


# ---------------------------------------------------------------------------
# Citation dataclass
# ---------------------------------------------------------------------------

@dataclass
class Citation:
    raw: str
    citation_type: CitationType
    url: Optional[str] = None
    title: Optional[str] = None
    line_num: int = 1
    identifier: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        """Basic validation based on citation type."""
        ct = self.citation_type
        if ct in (CitationType.URL, CitationType.BARE_URL, CitationType.GITHUB):
            return bool(self.url and self.url.startswith(("http://", "https://")))
        if ct == CitationType.DOI:
            if self.identifier:
                return self.identifier.startswith("10.")
            if self.url:
                return "10." in self.url
            return False
        if ct == CitationType.ARXIV:
            if self.identifier:
                # arXiv IDs are like YYMM.NNNNN
                return bool(re.match(r'^\d{4}\.\d{4,5}$', self.identifier))
            if self.url:
                return "arxiv.org" in self.url
            return False
        if ct == CitationType.FOOTNOTE:
            # Footnote refs are always considered structurally valid if they have raw text
            return bool(self.raw)
        if ct == CitationType.INLINE_REF:
            return bool(self.raw)
        return False


# ---------------------------------------------------------------------------
# CitationStats dataclass
# ---------------------------------------------------------------------------

@dataclass
class CitationStats:
    total: int = 0
    by_type: dict[str, int] = field(default_factory=dict)
    unique_urls: set[str] = field(default_factory=set)

    @property
    def domains(self) -> set[str]:
        """Return unique domains extracted from URLs."""
        result: set[str] = set()
        for url in self.unique_urls:
            try:
                parsed = urlparse(url)
                if parsed.netloc:
                    result.add(parsed.netloc)
            except Exception:
                pass
        return result


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

# GitHub URL pattern — more specific, must be matched before bare URL
_GITHUB_RE = re.compile(
    r'https?://github\.com/[\w-]+/[\w.\-]+(?:[^\s)>]*)?'
)

# arXiv patterns
# arXiv:YYMM.NNNNN or arXiv:YYMM.NNNN (case-insensitive)
_ARXIV_LABEL_RE = re.compile(r'arXiv:(\d{4}\.\d{4,5})', re.IGNORECASE)
# arxiv.org URL
_ARXIV_URL_RE = re.compile(r'https?://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:[^\s)>]*)?')

# DOI patterns (most specific first):
# Full doi.org URL: https://doi.org/10.XXXX/...
_DOI_URL_RE = re.compile(r'https?://doi\.org/(10\.\d{4,}/\S+?)(?=[\s)>\]]|$)')
# doi: prefix: doi:10.XXXX/...
_DOI_PREFIX_RE = re.compile(r'(?<![/\w])doi:(10\.\d{4,}/\S+?)(?=[\s)>\]]|$)', re.IGNORECASE)
# Standalone DOI: 10.XXXX/... (only if not preceded by / or word chars that indicate URL path)
_DOI_BARE_RE = re.compile(r'(?<![/\w])(10\.\d{4,}/[^\s)>\]]+?)(?=[\s)>\]]|$)')

# Markdown link: [text](url)
_MD_LINK_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]+)\)')

# Footnote reference definition: [^ref]: url_or_text  (at start of line)
_FOOTNOTE_DEF_RE = re.compile(r'^\s*\[\^([^\]]+)\]:\s*(.+)$', re.MULTILINE)

# Footnote reference usage: [^ref]
_FOOTNOTE_USE_RE = re.compile(r'\[\^([^\]]+)\]')

# Inline reference-style link: [text][ref]
_INLINE_REF_RE = re.compile(r'(?<!!)\[([^\]]+)\]\[([^\]]*)\]')

# Reference definition: [ref]: url  (non-footnote, at start of line)
_REF_DEF_RE = re.compile(r'^\s*\[([^\^][^\]]*)\]:\s*(\S+)', re.MULTILINE)

# Bare URL (http/https not inside a markdown link context)
_BARE_URL_RE = re.compile(r'https?://[^\s)>\]"\']+')


def _line_of(text: str, match_start: int) -> int:
    """Return 1-based line number for a character offset."""
    return text[:match_start].count('\n') + 1


def _strip_trailing_punct(url: str) -> str:
    """Strip common trailing punctuation that is unlikely to be part of a URL."""
    return url.rstrip('.,;:!?')


# ---------------------------------------------------------------------------
# CitationParser
# ---------------------------------------------------------------------------

class CitationParser:
    """Extracts and categorises citations from markdown text."""

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def parse(self, text: str) -> list[Citation]:
        """Parse *text* and return all citations found, in document order."""
        citations: list[tuple[int, Citation]] = []  # (char_offset, citation)

        # Track which character ranges are already consumed so we don't double-count.
        consumed: list[tuple[int, int]] = []

        def _overlaps(start: int, end: int) -> bool:
            for cs, ce in consumed:
                if start < ce and end > cs:
                    return True
            return False

        def _add(start: int, end: int, citation: Citation) -> None:
            consumed.append((start, end))
            citations.append((start, citation))

        # 1. Markdown links [text](url) — handle first as they take precedence.
        for m in _MD_LINK_RE.finditer(text):
            link_text = m.group(1)
            url = m.group(2).strip()
            line = _line_of(text, m.start())

            ctype, identifier = self._classify_url(url)
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=ctype,
                url=url if url.startswith(("http://", "https://")) else None,
                title=link_text or None,
                line_num=line,
                identifier=identifier,
            ))

        # 2. Footnote definitions [^ref]: ...
        for m in _FOOTNOTE_DEF_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            ref_id = m.group(1)
            content = m.group(2).strip()
            line = _line_of(text, m.start())
            url_match = _BARE_URL_RE.match(content)
            url_val = _strip_trailing_punct(url_match.group(0)) if url_match else None
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.FOOTNOTE,
                url=url_val,
                title=None,
                line_num=line,
                identifier=ref_id,
            ))

        # 3. Footnote usages [^ref] — only if not part of a definition on the same span.
        for m in _FOOTNOTE_USE_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            # Skip if this is part of a footnote def (starts with [^..]:)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.FOOTNOTE,
                url=None,
                title=None,
                line_num=line,
                identifier=m.group(1),
            ))

        # 4. Inline reference-style links [text][ref]
        for m in _INLINE_REF_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            link_text = m.group(1)
            ref = m.group(2) if m.group(2) else m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.INLINE_REF,
                url=None,
                title=link_text,
                line_num=line,
                identifier=ref,
            ))

        # 5. Reference definitions [ref]: url  (non-footnote)
        for m in _REF_DEF_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            ref_label = m.group(1)
            url = m.group(2).strip()
            line = _line_of(text, m.start())
            ctype, identifier = self._classify_url(url)
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=ctype,
                url=url if url.startswith(("http://", "https://")) else None,
                title=ref_label,
                line_num=line,
                identifier=identifier,
            ))

        # 6. Bare DOI URLs: https://doi.org/10.XXXX/...
        for m in _DOI_URL_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            doi_id = m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.DOI,
                url=m.group(0),
                title=None,
                line_num=line,
                identifier=doi_id,
            ))

        # 7. doi: prefix
        for m in _DOI_PREFIX_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            doi_id = m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.DOI,
                url=f"https://doi.org/{doi_id}",
                title=None,
                line_num=line,
                identifier=doi_id,
            ))

        # 8. Standalone bare DOI: 10.XXXX/...
        for m in _DOI_BARE_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            doi_id = m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.DOI,
                url=f"https://doi.org/{doi_id}",
                title=None,
                line_num=line,
                identifier=doi_id,
            ))

        # 9. arXiv label: arXiv:YYMM.NNNNN
        for m in _ARXIV_LABEL_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            arxiv_id = m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.ARXIV,
                url=f"https://arxiv.org/abs/{arxiv_id}",
                title=None,
                line_num=line,
                identifier=arxiv_id,
            ))

        # 10. arXiv URL: arxiv.org/abs/YYMM.NNNNN
        for m in _ARXIV_URL_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            arxiv_id = m.group(1)
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.ARXIV,
                url=m.group(0),
                title=None,
                line_num=line,
                identifier=arxiv_id,
            ))

        # 11. GitHub URLs (bare, not already inside a markdown link)
        for m in _GITHUB_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            url = _strip_trailing_punct(m.group(0))
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.GITHUB,
                url=url,
                title=None,
                line_num=line,
                identifier=None,
            ))

        # 12. Remaining bare URLs (not GitHub, not DOI, not arXiv)
        for m in _BARE_URL_RE.finditer(text):
            if _overlaps(m.start(), m.end()):
                continue
            url = _strip_trailing_punct(m.group(0))
            line = _line_of(text, m.start())
            _add(m.start(), m.end(), Citation(
                raw=m.group(0),
                citation_type=CitationType.BARE_URL,
                url=url,
                title=None,
                line_num=line,
                identifier=None,
            ))

        # Sort by document position
        citations.sort(key=lambda x: x[0])
        return [c for _, c in citations]

    def parse_urls(self, text: str) -> list[Citation]:
        """Return only URL-type citations (URL, BARE_URL, GITHUB)."""
        url_types = {CitationType.URL, CitationType.BARE_URL, CitationType.GITHUB}
        return [c for c in self.parse(text) if c.citation_type in url_types]

    def parse_dois(self, text: str) -> list[Citation]:
        """Return only DOI citations."""
        return [c for c in self.parse(text) if c.citation_type == CitationType.DOI]

    def parse_arxiv(self, text: str) -> list[Citation]:
        """Return only arXiv citations."""
        return [c for c in self.parse(text) if c.citation_type == CitationType.ARXIV]

    def stats(self, text: str) -> CitationStats:
        """Compute CitationStats for *text*."""
        citations = self.parse(text)
        by_type: dict[str, int] = {}
        unique_urls: set[str] = set()
        for c in citations:
            key = c.citation_type.value
            by_type[key] = by_type.get(key, 0) + 1
            if c.url:
                unique_urls.add(c.url)
        return CitationStats(
            total=len(citations),
            by_type=by_type,
            unique_urls=unique_urls,
        )

    def deduplicate(self, citations: list[Citation]) -> list[Citation]:
        """Remove duplicate citations by url (if present) or identifier (if present).

        Keeps the first occurrence of each unique (url or identifier) pair.
        Citations without both url and identifier are always kept.
        """
        seen_urls: set[str] = set()
        seen_ids: set[str] = set()
        result: list[Citation] = []
        for c in citations:
            key_url = c.url
            key_id = c.identifier
            if key_url and key_url in seen_urls:
                continue
            if not key_url and key_id and key_id in seen_ids:
                continue
            if key_url:
                seen_urls.add(key_url)
            if key_id:
                seen_ids.add(key_id)
            result.append(c)
        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _classify_url(url: str) -> tuple[CitationType, Optional[str]]:
        """Return (CitationType, identifier) for a URL string."""
        # arXiv URL check
        m = _ARXIV_URL_RE.match(url)
        if m:
            return CitationType.ARXIV, m.group(1)

        # DOI URL check
        m = _DOI_URL_RE.match(url)
        if m:
            return CitationType.DOI, m.group(1)

        # GitHub URL check
        if re.match(r'https?://github\.com/', url):
            return CitationType.GITHUB, None

        # Any other http/https URL
        if url.startswith(("http://", "https://")):
            return CitationType.URL, None

        return CitationType.INLINE_REF, None
