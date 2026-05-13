"""Document-level metadata extraction — stdlib only."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field

from docstoolkit.metadata_extractor.extractor import MetadataExtractor


@dataclass
class DocumentMetadata:
    """Metadata record for a single document."""

    doc_id: str
    title: str = ""
    author: str = ""
    created_at: float = 0.0
    word_count: int = 0
    char_count: int = 0
    language: str = "unknown"
    tags: list[str] = field(default_factory=list)
    custom: dict = field(default_factory=dict)


class DocumentMetadataExtractor:
    """Extract high-level metadata from document text."""

    _RE_CAPS: re.Pattern = re.compile(r"\b[A-Z]{3,}\b")
    _extractor: MetadataExtractor = MetadataExtractor()

    def extract(self, doc_id: str, text: str) -> DocumentMetadata:
        """Derive a :class:`DocumentMetadata` from *doc_id* and *text*."""
        word_count = len(text.split())
        char_count = len(text)

        language = self._detect_language(text)
        title = self._extract_title(text)
        author = self._extract_author(text)
        tags = self._extract_tags(text)

        return DocumentMetadata(
            doc_id=doc_id,
            title=title,
            author=author,
            word_count=word_count,
            char_count=char_count,
            language=language,
            tags=tags,
        )

    # -----------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------

    @staticmethod
    def _detect_language(text: str) -> str:
        """Detect language: 'ru' if Cyrillic > 20 % of alpha chars, else 'en'.

        Returns 'unknown' when the text contains no alphabetic characters.
        """
        alpha_chars = [c for c in text if c.isalpha()]
        if not alpha_chars:
            return "unknown"
        cyrillic_count = sum(
            1 for c in alpha_chars if "Ѐ" <= c <= "ӿ"
        )
        ratio = cyrillic_count / len(alpha_chars)
        return "ru" if ratio > 0.20 else "en"

    @staticmethod
    def _extract_title(text: str) -> str:
        """Return the first non-empty line, truncated to 100 characters."""
        for line in text.splitlines():
            stripped = line.strip()
            if stripped:
                return stripped[:100]
        return ""

    def _extract_author(self, text: str) -> str:
        """Return the first email address found in *text*, or empty string."""
        emails = self._extractor.extract_emails(text)
        return emails[0].value if emails else ""

    def _extract_tags(self, text: str) -> list[str]:
        """Return all-caps words (≥ 3 chars) that appear at least twice."""
        matches = self._RE_CAPS.findall(text)
        counts = Counter(matches)
        return sorted(word for word, cnt in counts.items() if cnt >= 2)
