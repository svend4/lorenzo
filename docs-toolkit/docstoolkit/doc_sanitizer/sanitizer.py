"""Document sanitizer implementation.

Strips dangerous HTML, normalizes links, escapes content, and removes
scripts/styles/comments from markdown documents. Uses only stdlib
``html`` and ``re`` modules.
"""

from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# Regex patterns (compiled once)
# ---------------------------------------------------------------------------

_RE_HTML_TAG = re.compile(r"<[^>]+>")
_RE_SCRIPT = re.compile(
    r"<script\b[^>]*>.*?</script\s*>", re.DOTALL | re.IGNORECASE
)
_RE_SCRIPT_SELF_CLOSING = re.compile(
    r"<script\b[^>]*/>", re.IGNORECASE
)
_RE_STYLE = re.compile(
    r"<style\b[^>]*>.*?</style\s*>", re.DOTALL | re.IGNORECASE
)
_RE_STYLE_SELF_CLOSING = re.compile(
    r"<style\b[^>]*/>", re.IGNORECASE
)
_RE_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
_RE_MD_IMAGE = re.compile(r"!\[[^\]]*\]\([^)]*\)")
_RE_MD_LINK = re.compile(r"\[([^\]]*)\]\(([^)]*)\)")
# Tag-name extractor for keep-allowed mode
_RE_TAG_NAME = re.compile(r"<\s*/?\s*([a-zA-Z][a-zA-Z0-9]*)")
# Protocol detector (scheme:)
_RE_PROTOCOL = re.compile(r"^\s*([a-zA-Z][a-zA-Z0-9+.\-]*):")


# ---------------------------------------------------------------------------
# Enums and dataclasses
# ---------------------------------------------------------------------------


class SanitizationRule(Enum):
    """Available sanitization rules."""

    STRIP_HTML = "strip_html"
    ESCAPE_HTML = "escape_html"
    REMOVE_SCRIPTS = "remove_scripts"
    REMOVE_STYLE = "remove_style"
    NORMALIZE_LINKS = "normalize_links"
    STRIP_IMAGES = "strip_images"
    REMOVE_COMMENTS = "remove_comments"


@dataclass
class SanitizerConfig:
    """Configuration for ``DocSanitizer``."""

    rules: list[SanitizationRule] = field(
        default_factory=lambda: [
            SanitizationRule.REMOVE_SCRIPTS,
            SanitizationRule.REMOVE_STYLE,
            SanitizationRule.REMOVE_COMMENTS,
        ]
    )
    allowed_protocols: set[str] = field(
        default_factory=lambda: {"http", "https", "mailto"}
    )
    allowed_html_tags: set[str] = field(default_factory=set)
    strip_data_urls: bool = True


@dataclass
class SanitizationResult:
    """Result of a sanitization pass."""

    original: str
    sanitized: str
    removed_items: list[str] = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """Whether the document was modified."""
        return self.original != self.sanitized


# ---------------------------------------------------------------------------
# DocSanitizer
# ---------------------------------------------------------------------------


class DocSanitizer:
    """Apply configured sanitization rules to markdown text."""

    def __init__(self, config: SanitizerConfig | None = None) -> None:
        self.config = config if config is not None else SanitizerConfig()

    # -- Individual rule methods -------------------------------------------

    def strip_html(self, text: str) -> str:
        """Remove all HTML tags from ``text``."""
        return _RE_HTML_TAG.sub("", text)

    def strip_html_keep_allowed(self, text: str, allowed: set[str]) -> str:
        """Remove HTML tags except those in ``allowed`` (case-insensitive)."""
        allowed_lower = {tag.lower() for tag in allowed}

        def replace(match: re.Match[str]) -> str:
            tag_match = _RE_TAG_NAME.match(match.group(0))
            if tag_match is None:
                return ""
            tag_name = tag_match.group(1).lower()
            if tag_name in allowed_lower:
                return match.group(0)
            return ""

        return _RE_HTML_TAG.sub(replace, text)

    def escape_html(self, text: str) -> str:
        """Escape HTML special characters via ``html.escape``."""
        return html.escape(text, quote=True)

    def remove_scripts(self, text: str) -> str:
        """Strip ``<script>...</script>`` blocks and self-closing scripts."""
        text = _RE_SCRIPT.sub("", text)
        text = _RE_SCRIPT_SELF_CLOSING.sub("", text)
        return text

    def remove_style(self, text: str) -> str:
        """Strip ``<style>...</style>`` blocks and self-closing styles."""
        text = _RE_STYLE.sub("", text)
        text = _RE_STYLE_SELF_CLOSING.sub("", text)
        return text

    def remove_comments(self, text: str) -> str:
        """Strip ``<!-- ... -->`` HTML comments."""
        return _RE_COMMENT.sub("", text)

    def strip_images(self, text: str) -> str:
        """Remove markdown image syntax ``![alt](src)``."""
        return _RE_MD_IMAGE.sub("", text)

    def is_safe_url(self, url: str, allowed_protocols: set[str]) -> bool:
        """Return ``True`` when ``url`` uses an allowed protocol.

        Relative URLs and fragments are considered safe.  Data URLs are
        rejected when ``config.strip_data_urls`` is enabled (default).
        """
        if url is None:
            return False
        stripped = url.strip()
        if stripped == "":
            return True

        # Data URLs
        if stripped.lower().startswith("data:"):
            return not self.config.strip_data_urls

        proto_match = _RE_PROTOCOL.match(stripped)
        if proto_match is None:
            # Relative paths, anchors, etc. — safe
            return True
        protocol = proto_match.group(1).lower()
        allowed_lower = {p.lower() for p in allowed_protocols}
        return protocol in allowed_lower

    def normalize_links(self, text: str, allowed_protocols: set[str]) -> str:
        """Replace markdown link URLs using disallowed protocols with ``#``."""

        def replace(match: re.Match[str]) -> str:
            link_text = match.group(1)
            url = match.group(2)
            if self.is_safe_url(url, allowed_protocols):
                return match.group(0)
            return f"[{link_text}](#)"

        return _RE_MD_LINK.sub(replace, text)

    # -- Pipeline ----------------------------------------------------------

    def sanitize(self, text: str) -> SanitizationResult:
        """Apply every configured rule to ``text``."""
        original = text
        current = text
        removed: list[str] = []

        for rule in self.config.rules:
            before = current
            if rule is SanitizationRule.REMOVE_SCRIPTS:
                current = self.remove_scripts(current)
                if before != current:
                    removed.append("scripts")
            elif rule is SanitizationRule.REMOVE_STYLE:
                current = self.remove_style(current)
                if before != current:
                    removed.append("style blocks")
            elif rule is SanitizationRule.REMOVE_COMMENTS:
                current = self.remove_comments(current)
                if before != current:
                    removed.append("html comments")
            elif rule is SanitizationRule.STRIP_HTML:
                if self.config.allowed_html_tags:
                    current = self.strip_html_keep_allowed(
                        current, self.config.allowed_html_tags
                    )
                else:
                    current = self.strip_html(current)
                if before != current:
                    removed.append("html tags")
            elif rule is SanitizationRule.ESCAPE_HTML:
                current = self.escape_html(current)
                if before != current:
                    removed.append("escaped html")
            elif rule is SanitizationRule.NORMALIZE_LINKS:
                current = self.normalize_links(
                    current, self.config.allowed_protocols
                )
                if before != current:
                    removed.append("unsafe links")
            elif rule is SanitizationRule.STRIP_IMAGES:
                current = self.strip_images(current)
                if before != current:
                    removed.append("images")

        return SanitizationResult(
            original=original, sanitized=current, removed_items=removed
        )

    def sanitize_batch(self, texts: list[str]) -> list[SanitizationResult]:
        """Sanitize a list of texts and return the results."""
        return [self.sanitize(item) for item in texts]
