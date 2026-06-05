"""Document metadata extractor — size, complexity, structure (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class Complexity(Enum):
    """Document complexity levels."""

    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    VERY_COMPLEX = "very_complex"


@dataclass
class DocMetadata:
    """Computed metadata for a single document."""

    char_count: int = 0
    word_count: int = 0
    line_count: int = 0
    paragraph_count: int = 0
    heading_count: int = 0
    link_count: int = 0
    image_count: int = 0
    code_block_count: int = 0
    list_item_count: int = 0
    table_count: int = 0
    complexity: Complexity = Complexity.TRIVIAL
    avg_paragraph_length: float = 0.0
    heading_depth: int = 0
    has_frontmatter: bool = False
    has_toc: bool = False


# Pre-compiled regex patterns
_HEADING_RE = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)
_IMAGE_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
_LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\([^)]+\)")
_CODE_FENCE_RE = re.compile(r"^```", re.MULTILINE)
_LIST_BULLET_RE = re.compile(r"^[ \t]*[\*\-\+]\s+", re.MULTILINE)
_LIST_NUM_RE = re.compile(r"^[ \t]*\d+\.\s+", re.MULTILINE)
_TABLE_SEP_RE = re.compile(r"\|\s*:?-+:?\s*\|")
_FRONTMATTER_RE = re.compile(r"\A---\s*\n.*?\n---\s*(\n|$)", re.DOTALL)

_TOC_KEYWORDS = ("table of contents", "содержание", "оглавление", "toc")


class MetadataExtractor:
    """Extracts structural metadata from Markdown-like documents."""

    def extract(self, text: str) -> DocMetadata:
        """Compute metadata for a single document string."""
        if text is None:
            text = ""

        meta = DocMetadata()
        meta.char_count = len(text)
        meta.word_count = self._count_words(text)
        meta.line_count = self._count_lines(text)

        # Frontmatter handling — strip before structural detection
        meta.has_frontmatter = self._has_frontmatter(text)
        body = self._strip_frontmatter(text) if meta.has_frontmatter else text

        # Paragraph counting on the body
        paragraphs = self._split_paragraphs(body)
        meta.paragraph_count = len(paragraphs)
        if meta.paragraph_count > 0:
            total_para_words = sum(self._count_words(p) for p in paragraphs)
            meta.avg_paragraph_length = total_para_words / meta.paragraph_count
        else:
            meta.avg_paragraph_length = 0.0

        # Headings
        headings = _HEADING_RE.findall(body)
        meta.heading_count = len(headings)
        if headings:
            meta.heading_depth = max(len(h[0]) for h in headings)
        else:
            meta.heading_depth = 0

        # Links / images — count images first so links exclude them
        meta.image_count = len(_IMAGE_RE.findall(body))
        meta.link_count = len(_LINK_RE.findall(body))

        # Code fences — count opening fences (every 2nd fence is an opener)
        fence_count = len(_CODE_FENCE_RE.findall(body))
        meta.code_block_count = fence_count // 2 + (fence_count % 2)
        # Simpler: number of opening fences = ceil(fence_count / 2) when unbalanced,
        # but typically docs are balanced so it's fence_count // 2.
        # Use ceil to handle unbalanced cases.
        meta.code_block_count = (fence_count + 1) // 2 if fence_count else 0

        # List items
        meta.list_item_count = (
            len(_LIST_BULLET_RE.findall(body)) + len(_LIST_NUM_RE.findall(body))
        )

        # Tables — count separator rows
        meta.table_count = len(_TABLE_SEP_RE.findall(body))

        # TOC detection — heading text contains TOC keyword
        meta.has_toc = self._has_toc(headings)

        # Complexity
        meta.complexity = self._compute_complexity(meta)

        return meta

    def extract_batch(self, texts: list[str]) -> list[DocMetadata]:
        """Extract metadata for a list of documents."""
        return [self.extract(t) for t in texts]

    def compare(self, meta_a: DocMetadata, meta_b: DocMetadata) -> dict[str, Any]:
        """Return a dict of per-field deltas (b - a) for numeric fields, plus markers."""
        result: dict[str, Any] = {}
        a_dict = asdict(meta_a)
        b_dict = asdict(meta_b)
        for key in a_dict:
            a_val = a_dict[key]
            b_val = b_dict[key]
            if key == "complexity":
                # Stored as Complexity enum on dataclass; asdict gives enum
                a_c = meta_a.complexity
                b_c = meta_b.complexity
                result[key] = {
                    "a": a_c.value,
                    "b": b_c.value,
                    "changed": a_c != b_c,
                }
            elif isinstance(a_val, bool):
                result[key] = {"a": a_val, "b": b_val, "changed": a_val != b_val}
            elif isinstance(a_val, (int, float)):
                result[key] = b_val - a_val
            else:
                result[key] = {"a": a_val, "b": b_val, "changed": a_val != b_val}
        return result

    def summarize(self, meta: DocMetadata) -> str:
        """Return a human-readable summary string."""
        parts = [
            f"Document: {meta.word_count} words, {meta.char_count} chars, "
            f"{meta.line_count} lines",
            f"Structure: {meta.paragraph_count} paragraphs, "
            f"{meta.heading_count} headings (depth {meta.heading_depth})",
            f"Content: {meta.link_count} links, {meta.image_count} images, "
            f"{meta.code_block_count} code blocks, "
            f"{meta.list_item_count} list items, {meta.table_count} tables",
            f"Complexity: {meta.complexity.value} "
            f"(avg paragraph: {meta.avg_paragraph_length:.1f} words)",
        ]
        flags = []
        if meta.has_frontmatter:
            flags.append("frontmatter")
        if meta.has_toc:
            flags.append("toc")
        if flags:
            parts.append("Flags: " + ", ".join(flags))
        return "\n".join(parts)

    # ----- internal helpers -----

    @staticmethod
    def _count_words(text: str) -> int:
        if not text:
            return 0
        # Split on whitespace; filter empties
        return len([w for w in text.split() if w])

    @staticmethod
    def _count_lines(text: str) -> int:
        if not text:
            return 0
        # Count newlines + 1 for final line if non-empty
        # If text ends with \n, last "line" is empty — don't count it
        if text.endswith("\n"):
            return text.count("\n")
        return text.count("\n") + 1

    @staticmethod
    def _has_frontmatter(text: str) -> bool:
        if not text:
            return False
        return bool(_FRONTMATTER_RE.match(text))

    @staticmethod
    def _strip_frontmatter(text: str) -> str:
        return _FRONTMATTER_RE.sub("", text, count=1)

    @staticmethod
    def _split_paragraphs(text: str) -> list[str]:
        if not text or not text.strip():
            return []
        # Paragraphs separated by blank line(s)
        chunks = re.split(r"\n\s*\n", text.strip())
        return [c for c in chunks if c.strip()]

    @staticmethod
    def _has_toc(headings: list[tuple[str, str]]) -> bool:
        for _, htext in headings:
            low = htext.strip().lower()
            for kw in _TOC_KEYWORDS:
                if kw in low:
                    return True
        return False

    @staticmethod
    def _compute_complexity(meta: DocMetadata) -> Complexity:
        score = (
            (meta.word_count / 200.0)
            + (meta.heading_count * 2)
            + (meta.code_block_count * 3)
            + (meta.table_count * 3)
            + (meta.link_count / 5.0)
        )
        if score < 5:
            return Complexity.TRIVIAL
        if score < 15:
            return Complexity.SIMPLE
        if score < 40:
            return Complexity.MODERATE
        if score < 100:
            return Complexity.COMPLEX
        return Complexity.VERY_COMPLEX
