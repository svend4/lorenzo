"""Advanced document diff implementation.

Provides token-level, word-level, line-level, sentence-level, paragraph-level
diffs, plus structural diff (headings, paragraphs, code blocks) and inline
HTML / Markdown rendering.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


class DiffGranularity(str, Enum):
    """Granularity level for diff operations."""

    CHAR = "char"
    WORD = "word"
    LINE = "line"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"


class DiffOp(str, Enum):
    """Type of diff operation."""

    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"
    REPLACE = "replace"


@dataclass
class DiffChunk:
    """A single diff operation: equal, insert, delete, or replace."""

    op: DiffOp
    old_text: str = ""
    new_text: str = ""
    old_start: int = 0
    new_start: int = 0


@dataclass
class StructuralDiff:
    """Structural-level differences between two documents."""

    headings_added: list[str] = field(default_factory=list)
    headings_removed: list[str] = field(default_factory=list)
    headings_changed: list[tuple[str, str]] = field(default_factory=list)
    paragraphs_added: int = 0
    paragraphs_removed: int = 0
    code_blocks_added: int = 0
    code_blocks_removed: int = 0


@dataclass
class WordDiffStats:
    """Statistics from word-level diff."""

    words_added: int = 0
    words_removed: int = 0
    words_unchanged: int = 0
    ratio: float = 0.0


# --- Tokenizers -----------------------------------------------------------

_WORD_RE = re.compile(r"\S+|\s+")
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
_PARA_SPLIT = re.compile(r"\n\n+")
_HEADING_RE = re.compile(r"^(#+)\s+(.*)$", re.MULTILINE)
_CODE_FENCE_RE = re.compile(r"^```", re.MULTILINE)


def _tokenize(text: str, granularity: DiffGranularity) -> list[str]:
    if granularity == DiffGranularity.CHAR:
        return list(text)
    if granularity == DiffGranularity.WORD:
        return _WORD_RE.findall(text)
    if granularity == DiffGranularity.LINE:
        return text.splitlines(keepends=True)
    if granularity == DiffGranularity.SENTENCE:
        if not text:
            return []
        return _SENT_SPLIT.split(text)
    if granularity == DiffGranularity.PARAGRAPH:
        if not text:
            return []
        return _PARA_SPLIT.split(text)
    raise ValueError(f"Unknown granularity: {granularity}")


def _join_tokens(tokens: Iterable[str], granularity: DiffGranularity) -> str:
    if granularity == DiffGranularity.CHAR:
        return "".join(tokens)
    if granularity == DiffGranularity.WORD:
        return "".join(tokens)
    if granularity == DiffGranularity.LINE:
        return "".join(tokens)
    if granularity == DiffGranularity.SENTENCE:
        return " ".join(tokens)
    if granularity == DiffGranularity.PARAGRAPH:
        return "\n\n".join(tokens)
    raise ValueError(f"Unknown granularity: {granularity}")


def _extract_headings(text: str) -> list[str]:
    return [m.group(2).strip() for m in _HEADING_RE.finditer(text)]


def _count_paragraphs(text: str) -> int:
    if not text.strip():
        return 0
    return len([p for p in _PARA_SPLIT.split(text) if p.strip()])


def _count_code_blocks(text: str) -> int:
    # Each pair of ``` fences forms one block; count fences and divide by 2.
    fences = _CODE_FENCE_RE.findall(text)
    return len(fences) // 2


# --- Main class -----------------------------------------------------------

class DocDiffV2:
    """Advanced document diff engine."""

    # Generic dispatch ----------------------------------------------------
    def diff(
        self,
        old: str,
        new: str,
        granularity: DiffGranularity = DiffGranularity.WORD,
    ) -> list[DiffChunk]:
        """Compute diff at the requested granularity."""
        if granularity == DiffGranularity.CHAR:
            return self.diff_chars(old, new)
        if granularity == DiffGranularity.WORD:
            return self.diff_words(old, new)
        if granularity == DiffGranularity.LINE:
            return self.diff_lines(old, new)
        if granularity == DiffGranularity.SENTENCE:
            return self.diff_sentences(old, new)
        if granularity == DiffGranularity.PARAGRAPH:
            return self.diff_paragraphs(old, new)
        raise ValueError(f"Unknown granularity: {granularity}")

    # Specific granularities ---------------------------------------------
    def diff_chars(self, old: str, new: str) -> list[DiffChunk]:
        return self._diff_tokens(old, new, DiffGranularity.CHAR)

    def diff_words(self, old: str, new: str) -> list[DiffChunk]:
        return self._diff_tokens(old, new, DiffGranularity.WORD)

    def diff_lines(self, old: str, new: str) -> list[DiffChunk]:
        return self._diff_tokens(old, new, DiffGranularity.LINE)

    def diff_sentences(self, old: str, new: str) -> list[DiffChunk]:
        return self._diff_tokens(old, new, DiffGranularity.SENTENCE)

    def diff_paragraphs(self, old: str, new: str) -> list[DiffChunk]:
        return self._diff_tokens(old, new, DiffGranularity.PARAGRAPH)

    def _diff_tokens(
        self,
        old: str,
        new: str,
        granularity: DiffGranularity,
    ) -> list[DiffChunk]:
        old_tokens = _tokenize(old, granularity)
        new_tokens = _tokenize(new, granularity)
        sm = difflib.SequenceMatcher(a=old_tokens, b=new_tokens, autojunk=False)
        chunks: list[DiffChunk] = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            old_text = _join_tokens(old_tokens[i1:i2], granularity)
            new_text = _join_tokens(new_tokens[j1:j2], granularity)
            try:
                op = DiffOp(tag)
            except ValueError:
                op = DiffOp.EQUAL
            chunks.append(
                DiffChunk(
                    op=op,
                    old_text=old_text,
                    new_text=new_text,
                    old_start=i1,
                    new_start=j1,
                )
            )
        return chunks

    # Stats ---------------------------------------------------------------
    def word_stats(self, old: str, new: str) -> WordDiffStats:
        old_words = [t for t in _tokenize(old, DiffGranularity.WORD) if t.strip()]
        new_words = [t for t in _tokenize(new, DiffGranularity.WORD) if t.strip()]
        sm = difflib.SequenceMatcher(a=old_words, b=new_words, autojunk=False)
        added = 0
        removed = 0
        unchanged = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                unchanged += i2 - i1
            elif tag == "insert":
                added += j2 - j1
            elif tag == "delete":
                removed += i2 - i1
            elif tag == "replace":
                removed += i2 - i1
                added += j2 - j1
        return WordDiffStats(
            words_added=added,
            words_removed=removed,
            words_unchanged=unchanged,
            ratio=sm.ratio(),
        )

    # Structural ----------------------------------------------------------
    def structural_diff(self, old: str, new: str) -> StructuralDiff:
        old_headings = _extract_headings(old)
        new_headings = _extract_headings(new)
        old_set = set(old_headings)
        new_set = set(new_headings)

        added = [h for h in new_headings if h not in old_set]
        removed = [h for h in old_headings if h not in new_set]

        # Detect "changed" headings: find pairs by position where strings differ
        # but both have same index up to length of shorter list AND both
        # are not in the other set.
        changed: list[tuple[str, str]] = []
        # Use SequenceMatcher to align headings and pull out 'replace' opcodes.
        sm = difflib.SequenceMatcher(a=old_headings, b=new_headings, autojunk=False)
        replaced_old: list[str] = []
        replaced_new: list[str] = []
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "replace":
                replaced_old.extend(old_headings[i1:i2])
                replaced_new.extend(new_headings[j1:j2])
        # Pair up replaced headings 1:1
        for a, b in zip(replaced_old, replaced_new):
            changed.append((a, b))

        # Recompute pure added / removed to exclude the changed pairs
        changed_old_set = {a for a, _ in changed}
        changed_new_set = {b for _, b in changed}
        added = [h for h in new_headings if h not in old_set and h not in changed_new_set]
        removed = [h for h in old_headings if h not in new_set and h not in changed_old_set]

        old_para = _count_paragraphs(old)
        new_para = _count_paragraphs(new)
        para_added = max(0, new_para - old_para)
        para_removed = max(0, old_para - new_para)

        old_cb = _count_code_blocks(old)
        new_cb = _count_code_blocks(new)
        cb_added = max(0, new_cb - old_cb)
        cb_removed = max(0, old_cb - new_cb)

        return StructuralDiff(
            headings_added=added,
            headings_removed=removed,
            headings_changed=changed,
            paragraphs_added=para_added,
            paragraphs_removed=para_removed,
            code_blocks_added=cb_added,
            code_blocks_removed=cb_removed,
        )

    # Rendering -----------------------------------------------------------
    def inline_html(
        self,
        old: str,
        new: str,
        granularity: DiffGranularity = DiffGranularity.WORD,
    ) -> str:
        chunks = self.diff(old, new, granularity)
        parts: list[str] = []
        for c in chunks:
            if c.op == DiffOp.EQUAL:
                parts.append(c.new_text)
            elif c.op == DiffOp.INSERT:
                parts.append(f"<ins>{c.new_text}</ins>")
            elif c.op == DiffOp.DELETE:
                parts.append(f"<del>{c.old_text}</del>")
            elif c.op == DiffOp.REPLACE:
                parts.append(f"<del>{c.old_text}</del><ins>{c.new_text}</ins>")
        return "".join(parts)

    def inline_markdown(
        self,
        old: str,
        new: str,
        granularity: DiffGranularity = DiffGranularity.WORD,
    ) -> str:
        chunks = self.diff(old, new, granularity)
        parts: list[str] = []
        for c in chunks:
            if c.op == DiffOp.EQUAL:
                parts.append(c.new_text)
            elif c.op == DiffOp.INSERT:
                parts.append(f"+{c.new_text}")
            elif c.op == DiffOp.DELETE:
                parts.append(f"-{c.old_text}")
            elif c.op == DiffOp.REPLACE:
                parts.append(f"-{c.old_text}+{c.new_text}")
        return "".join(parts)

    # Summary -------------------------------------------------------------
    def summary(self, old: str, new: str) -> dict:
        ws = self.word_stats(old, new)
        sd = self.structural_diff(old, new)
        line_chunks = self.diff_lines(old, new)
        lines_added = sum(
            1 for c in line_chunks if c.op in (DiffOp.INSERT, DiffOp.REPLACE)
        )
        lines_removed = sum(
            1 for c in line_chunks if c.op in (DiffOp.DELETE, DiffOp.REPLACE)
        )
        return {
            "words_added": ws.words_added,
            "words_removed": ws.words_removed,
            "words_unchanged": ws.words_unchanged,
            "ratio": ws.ratio,
            "headings_added": len(sd.headings_added),
            "headings_removed": len(sd.headings_removed),
            "headings_changed": len(sd.headings_changed),
            "paragraphs_added": sd.paragraphs_added,
            "paragraphs_removed": sd.paragraphs_removed,
            "code_blocks_added": sd.code_blocks_added,
            "code_blocks_removed": sd.code_blocks_removed,
            "lines_added": lines_added,
            "lines_removed": lines_removed,
            "old_length": len(old),
            "new_length": len(new),
        }
