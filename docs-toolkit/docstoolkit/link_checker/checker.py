"""Link extractor and validator for markdown documents (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class LinkType(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"
    ANCHOR = "anchor"
    IMAGE = "image"
    FOOTNOTE = "footnote"


class LinkStatus(Enum):
    UNKNOWN = "unknown"
    VALID = "valid"
    BROKEN = "broken"
    SKIPPED = "skipped"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Link:
    url: str
    text: str
    line_num: int
    link_type: LinkType
    status: LinkStatus = LinkStatus.UNKNOWN


@dataclass
class CheckResult:
    links: list[Link] = field(default_factory=list)

    @property
    def valid_count(self) -> int:
        return sum(1 for lnk in self.links if lnk.status == LinkStatus.VALID)

    @property
    def broken_count(self) -> int:
        return sum(1 for lnk in self.links if lnk.status == LinkStatus.BROKEN)

    @property
    def unknown_count(self) -> int:
        return sum(1 for lnk in self.links if lnk.status == LinkStatus.UNKNOWN)

    @property
    def skipped_count(self) -> int:
        return sum(1 for lnk in self.links if lnk.status == LinkStatus.SKIPPED)

    def by_type(self, link_type: LinkType) -> list[Link]:
        return [lnk for lnk in self.links if lnk.link_type == link_type]

    @property
    def external_links(self) -> list[Link]:
        return self.by_type(LinkType.EXTERNAL)

    @property
    def internal_links(self) -> list[Link]:
        return self.by_type(LinkType.INTERNAL)


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Image: ![alt](url)  — must be checked before standard link pattern
_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]*)\)')

# Standard inline link: [text](url)
_INLINE_RE = re.compile(r'(?<!!)\[([^\]]*)\]\(([^)]*)\)')

# Reference-style link usage: [text][ref]  (ref is non-empty, non-image)
_REF_LINK_RE = re.compile(r'(?<!!)\[([^\]]+)\]\[([^\]]*)\]')

# Footnote/reference definition: [ref]: url  at start of line
_REF_DEF_RE = re.compile(r'^\s*\[([^\]]+)\]:\s*(\S+)', re.MULTILINE)


def _classify_inline(url: str) -> LinkType:
    """Classify a plain (non-image) inline link by its URL."""
    if url.startswith(('http://', 'https://')):
        return LinkType.EXTERNAL
    if url.startswith('#'):
        return LinkType.ANCHOR
    return LinkType.INTERNAL


def _line_of_match(text: str, match_start: int) -> int:
    """Return 1-based line number for a character offset in *text*."""
    return text[:match_start].count('\n') + 1


# ---------------------------------------------------------------------------
# LinkExtractor
# ---------------------------------------------------------------------------

class LinkExtractor:
    """Pure-extraction class — no HTTP, no filesystem access."""

    def extract(self, text: str) -> list[Link]:
        """Extract all markdown links from *text* and return them in document order."""
        links: list[Link] = []

        # Collect all matches with their start positions so we can sort them.
        found: list[tuple[int, Link]] = []

        # 1. Images — must come before inline so we can skip image spans.
        image_spans: list[tuple[int, int]] = []
        for m in _IMAGE_RE.finditer(text):
            alt_text = m.group(1)
            url = m.group(2).strip()
            line = _line_of_match(text, m.start())
            found.append((m.start(), Link(url=url, text=alt_text, line_num=line,
                                          link_type=LinkType.IMAGE)))
            image_spans.append((m.start(), m.end()))

        def _in_image_span(start: int) -> bool:
            for s, e in image_spans:
                if s <= start < e:
                    return True
            return False

        # 2. Inline links [text](url) — skip if inside an image span.
        for m in _INLINE_RE.finditer(text):
            if _in_image_span(m.start()):
                continue
            link_text = m.group(1)
            url = m.group(2).strip()
            line = _line_of_match(text, m.start())
            ltype = _classify_inline(url)
            found.append((m.start(), Link(url=url, text=link_text, line_num=line,
                                          link_type=ltype)))

        # 3. Reference-style link usages: [text][ref]
        #    We store the ref as the URL; caller can resolve if needed.
        ref_def_positions: dict[str, str] = {}  # ref_label -> url (from definitions)
        for m in _REF_DEF_RE.finditer(text):
            ref_def_positions[m.group(1).lower()] = m.group(2)

        for m in _REF_LINK_RE.finditer(text):
            # Make sure we are not inside an image span.
            if _in_image_span(m.start()):
                continue
            link_text = m.group(1)
            ref = m.group(2) if m.group(2) else m.group(1)  # empty [] → use link text
            line = _line_of_match(text, m.start())
            # Resolve url from definition if available, else keep ref as url placeholder.
            url = ref_def_positions.get(ref.lower(), ref)
            found.append((m.start(), Link(url=url, text=link_text, line_num=line,
                                          link_type=LinkType.FOOTNOTE)))

        # 4. Reference definitions themselves (bare [ref]: url lines) as FOOTNOTE.
        for m in _REF_DEF_RE.finditer(text):
            line = _line_of_match(text, m.start())
            url = m.group(2)
            ref_label = m.group(1)
            found.append((m.start(), Link(url=url, text=ref_label, line_num=line,
                                          link_type=LinkType.FOOTNOTE)))

        # Sort by document position and deduplicate (ref usages + def can overlap).
        found.sort(key=lambda x: x[0])
        # Deduplicate by (start_pos) — take first occurrence at each position.
        seen_positions: set[int] = set()
        for pos, lnk in found:
            if pos not in seen_positions:
                seen_positions.add(pos)
                links.append(lnk)

        return links

    def extract_external(self, text: str) -> list[Link]:
        return [lnk for lnk in self.extract(text) if lnk.link_type == LinkType.EXTERNAL]

    def extract_internal(self, text: str) -> list[Link]:
        return [lnk for lnk in self.extract(text) if lnk.link_type == LinkType.INTERNAL]


# ---------------------------------------------------------------------------
# LinkValidator
# ---------------------------------------------------------------------------

class LinkValidator:
    def __init__(self, base_path: str = ".") -> None:
        self.base_path = base_path

    def validate_internal(self, links: list[Link], existing_files: list[str]) -> list[Link]:
        """Mark INTERNAL links VALID if their url is in *existing_files*, BROKEN otherwise."""
        existing_set = set(existing_files)
        for lnk in links:
            if lnk.link_type == LinkType.INTERNAL:
                # Strip leading ./ for comparison flexibility.
                url_norm = lnk.url.lstrip('./')
                if lnk.url in existing_set or url_norm in existing_set:
                    lnk.status = LinkStatus.VALID
                else:
                    lnk.status = LinkStatus.BROKEN
        return links

    def validate_anchors(self, links: list[Link], text: str) -> list[Link]:
        """Mark ANCHOR links VALID if a matching heading exists in *text*."""
        # Collect all headings from text and normalise to anchor IDs.
        heading_re = re.compile(r'^#{1,6}\s+(.+)$', re.MULTILINE)
        anchors: set[str] = set()
        for m in heading_re.finditer(text):
            heading = m.group(1).strip()
            anchor_id = _heading_to_anchor(heading)
            anchors.add(anchor_id)

        for lnk in links:
            if lnk.link_type == LinkType.ANCHOR:
                # URL is like "#some-anchor"
                anchor = lnk.url.lstrip('#').lower()
                if anchor in anchors:
                    lnk.status = LinkStatus.VALID
                else:
                    lnk.status = LinkStatus.BROKEN
        return links

    def skip_external(self, links: list[Link]) -> list[Link]:
        """Mark all EXTERNAL links as SKIPPED."""
        for lnk in links:
            if lnk.link_type == LinkType.EXTERNAL:
                lnk.status = LinkStatus.SKIPPED
        return links


def _heading_to_anchor(heading: str) -> str:
    """Convert a markdown heading string to a GitHub-style anchor id."""
    # Lowercase, keep alphanumeric + spaces + hyphens, replace spaces with hyphens.
    anchor = heading.lower()
    anchor = re.sub(r'[^\w\s-]', '', anchor)
    anchor = re.sub(r'\s+', '-', anchor.strip())
    return anchor


# ---------------------------------------------------------------------------
# LinkChecker (facade)
# ---------------------------------------------------------------------------

class LinkChecker:
    """Combines LinkExtractor and LinkValidator into a single convenience API."""

    def __init__(self, base_path: str = ".") -> None:
        self._extractor = LinkExtractor()
        self._validator = LinkValidator(base_path=base_path)

    def check(self, text: str, existing_files: Optional[list[str]] = None) -> CheckResult:
        """Extract all links from *text* and validate them.

        - INTERNAL links: checked against *existing_files* (if provided).
        - ANCHOR links: checked against headings in *text*.
        - EXTERNAL links: marked SKIPPED (no HTTP requests).
        - IMAGE / FOOTNOTE links: left as UNKNOWN.
        """
        links = self._extractor.extract(text)

        if existing_files is not None:
            self._validator.validate_internal(links, existing_files)

        self._validator.validate_anchors(links, text)
        self._validator.skip_external(links)

        return CheckResult(links=links)

    def check_batch(self, texts: list[str]) -> list[CheckResult]:
        """Run check() on each text and return results in the same order."""
        return [self.check(text) for text in texts]
