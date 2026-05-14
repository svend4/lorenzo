"""Metadata extractor for multi-modal assets in documents."""
from __future__ import annotations

import re
from dataclasses import dataclass

from docstoolkit.multimodal_meta.asset import AssetMetadata, AssetType

# Mapping file extensions to MIME types
_EXT_MIME: dict[str, str] = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".svg": "image/svg+xml",
    ".webp": "image/webp",
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mov": "video/quicktime",
}

# Image-like extensions for MIME detection
_IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp", ".tiff"}


def _mime_from_url(url: str) -> str:
    """Infer MIME type from a URL/path by file extension."""
    url_lower = url.lower().split("?")[0]  # strip query strings
    for ext, mime in _EXT_MIME.items():
        if url_lower.endswith(ext):
            return mime
    return ""


@dataclass
class AssetPattern:
    """A compiled pattern for detecting an asset type in text."""

    pattern: str
    asset_type: AssetType
    mime_type: str


class MetadataExtractor:
    """Extract multi-modal asset metadata from markdown/HTML documents."""

    # Markdown image: ![alt text](url)
    _MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

    # Fenced code block: matches ALL fence lines (opening + closing).
    # We use even-indexed matches (0, 2, 4, ...) as opening fences.
    _CODE_FENCE_RE = re.compile(r"^[ \t]*(?:```|~~~)(\w*)[^\S\r\n]*$", re.MULTILINE)

    # HTML tags of interest
    _HTML_IMG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
    _HTML_TABLE_RE = re.compile(r"<table\b[^>]*>", re.IGNORECASE)
    _HTML_VIDEO_RE = re.compile(r"<video\b[^>]*>", re.IGNORECASE)
    _HTML_AUDIO_RE = re.compile(r"<audio\b[^>]*>", re.IGNORECASE)

    # HTML alt attribute
    _HTML_ALT_RE = re.compile(r'\balt=["\']([^"\']*)["\']', re.IGNORECASE)

    # Markdown table: line with at least 2 pipe characters
    _MD_TABLE_LINE_RE = re.compile(r"^[^\n]*\|[^\n]*\|[^\n]*$", re.MULTILINE)
    # Separator line: |---|---| pattern
    _MD_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*[-:]+[-| :]*\s*\|?\s*$")

    def extract(self, text: str, doc_id: str = "") -> list[AssetMetadata]:
        """Extract all recognisable assets from *text*.

        Handles:
        - Markdown images ``![alt](url)``
        - Fenced code blocks `` ```lang ``
        - HTML ``<img>``, ``<table>``, ``<video>``, ``<audio>`` tags
        """
        assets: list[AssetMetadata] = []

        # --- Markdown images ---
        for m in self._MD_IMAGE_RE.finditer(text):
            alt = m.group(1)
            url = m.group(2).strip()
            mime = _mime_from_url(url)
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.IMAGE,
                mime_type=mime,
                alt_text=alt,
            ))

        # --- Fenced code blocks ---
        # All fence lines (``` or ~~~) are matched; take only even-indexed
        # matches as opening fences (0, 2, 4, …) — odd ones are closers.
        fence_matches = list(self._CODE_FENCE_RE.finditer(text))
        for i in range(0, len(fence_matches), 2):
            lang = fence_matches[i].group(1).strip().lower()
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.CODE,
                language=lang,
            ))

        # --- HTML <img> ---
        for m in self._HTML_IMG_RE.finditer(text):
            tag_text = m.group(0)
            alt_match = self._HTML_ALT_RE.search(tag_text)
            alt = alt_match.group(1) if alt_match else ""
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.IMAGE,
                mime_type="image/unknown",
                alt_text=alt,
            ))

        # --- HTML <table> ---
        for _ in self._HTML_TABLE_RE.finditer(text):
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.TABLE,
            ))

        # --- HTML <video> ---
        for _ in self._HTML_VIDEO_RE.finditer(text):
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.VIDEO,
            ))

        # --- HTML <audio> ---
        for _ in self._HTML_AUDIO_RE.finditer(text):
            assets.append(AssetMetadata(
                source_doc=doc_id,
                asset_type=AssetType.AUDIO,
            ))

        return assets

    def detect_tables(self, text: str, doc_id: str = "") -> list[AssetMetadata]:
        """Detect Markdown tables in *text*.

        A Markdown table is identified as a block where at least two
        consecutive lines contain two or more ``|`` characters.  The
        separator row (``|---|---|``) is used to confirm it is a real table
        rather than incidental pipe usage.
        """
        assets: list[AssetMetadata] = []
        lines = text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i]
            # Check if the current line looks like a table row (has at least 2 pipes)
            if line.count("|") >= 2:
                # Look ahead for a separator line to confirm this is a table
                block_start = i
                j = i + 1
                found_sep = False
                while j < len(lines) and lines[j].count("|") >= 1:
                    if self._MD_TABLE_SEP_RE.match(lines[j]):
                        found_sep = True
                    j += 1
                if found_sep:
                    assets.append(AssetMetadata(
                        source_doc=doc_id,
                        asset_type=AssetType.TABLE,
                        mime_type="text/markdown",
                    ))
                    i = j  # skip past the entire table block
                    continue
            i += 1
        return assets
