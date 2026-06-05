"""Semantic diff — sentence-, paragraph-, and word-level diffing.

Pure stdlib only: re, enum, dataclasses, difflib.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# DiffType
# ---------------------------------------------------------------------------

class DiffType(Enum):
    ADDITION = "ADDITION"
    DELETION = "DELETION"
    MODIFICATION = "MODIFICATION"
    REORDER = "REORDER"
    UNCHANGED = "UNCHANGED"


# ---------------------------------------------------------------------------
# DiffChunk
# ---------------------------------------------------------------------------

@dataclass
class DiffChunk:
    diff_type: DiffType
    old_text: str
    new_text: str
    old_pos: int
    new_pos: int
    similarity: float = 1.0

    def is_significant(self, threshold: float = 0.1) -> bool:
        """Return True if the chunk represents a meaningful change.

        A chunk is significant when its similarity is below ``1 - threshold``
        (i.e. it changed more than *threshold* fraction) OR when the type is
        not UNCHANGED.
        """
        if self.diff_type != DiffType.UNCHANGED:
            return True
        return self.similarity < (1.0 - threshold)

    def summary(self) -> str:
        """Return a short human-readable description of this chunk."""
        if self.diff_type == DiffType.ADDITION:
            n = len(self.new_text.split())
            return f"ADDED: {n} words"
        if self.diff_type == DiffType.DELETION:
            n = len(self.old_text.split())
            return f"DELETED: {n} words"
        if self.diff_type == DiffType.MODIFICATION:
            old_preview = self.old_text[:30].replace("\n", " ")
            new_preview = self.new_text[:30].replace("\n", " ")
            sim_pct = f"{self.similarity:.2f}sim"
            return f"MODIFIED: {old_preview}→{new_preview} ({sim_pct})"
        if self.diff_type == DiffType.REORDER:
            n = len(self.new_text.split())
            return f"REORDERED: {n} words"
        # UNCHANGED
        n = len(self.old_text.split())
        return f"UNCHANGED: {n} words"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tokenize(text: str) -> list[str]:
    """Lowercase word tokens, no punctuation."""
    return re.findall(r"[a-zA-Zа-яА-ЯёЁ0-9]+", text.lower())


def _jaccard(a: str, b: str) -> float:
    """Jaccard similarity of token sets for two strings."""
    set_a = set(_tokenize(a))
    set_b = set(_tokenize(b))
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


def _split_sentences(text: str) -> list[str]:
    """Split text into sentences using punctuation boundaries."""
    # Split on sentence-ending punctuation followed by whitespace or end
    raw = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s.strip() for s in raw if s.strip()]


def _split_paragraphs(text: str) -> list[str]:
    """Split text on blank lines."""
    raw = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in raw if p.strip()]


def _split_words(text: str) -> list[str]:
    """Return individual word tokens (preserving order)."""
    return _tokenize(text)


# ---------------------------------------------------------------------------
# LCS helper for word diff
# ---------------------------------------------------------------------------

def _lcs_indices(old: list[str], new: list[str]) -> list[tuple[int, int]]:
    """Return index pairs (i, j) of the longest common subsequence."""
    m, n = len(old), len(new)
    # Use space-efficient approach with backtracking table
    # For large inputs keep it O(m*n) but manageable for word-level diffs
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if old[i - 1] == new[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    # Backtrack
    pairs: list[tuple[int, int]] = []
    i, j = m, n
    while i > 0 and j > 0:
        if old[i - 1] == new[j - 1]:
            pairs.append((i - 1, j - 1))
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
    pairs.reverse()
    return pairs


# ---------------------------------------------------------------------------
# SemanticDiffer
# ---------------------------------------------------------------------------

class SemanticDiffer:
    """Compare texts at sentence, paragraph, or word granularity."""

    # Thresholds for sentence/paragraph matching
    UNCHANGED_THRESHOLD = 0.9
    MODIFICATION_THRESHOLD = 0.3

    def _match_units(
        self,
        old_units: list[str],
        new_units: list[str],
    ) -> list[DiffChunk]:
        """Greedy matching of old units to new units via Jaccard similarity.

        For each old unit we find the best unmatched new unit.  After
        matching we produce UNCHANGED / MODIFICATION / DELETION / ADDITION
        chunks.  Remaining unmatched new units become ADDITIONs.
        """
        matched_new: set[int] = set()
        # Map from old_idx -> (best_new_idx, similarity)
        best_for_old: list[tuple[int, float]] = []

        for i, old in enumerate(old_units):
            best_j = -1
            best_sim = -1.0
            for j, new in enumerate(new_units):
                if j in matched_new:
                    continue
                sim = _jaccard(old, new)
                if sim > best_sim:
                    best_sim = sim
                    best_j = j
            best_for_old.append((best_j, best_sim))

        # Greedy assignment — process old units in order
        chunks: list[DiffChunk] = []
        for i, (best_j, best_sim) in enumerate(best_for_old):
            old_text = old_units[i]
            if best_j == -1 or best_sim < self.MODIFICATION_THRESHOLD:
                # No good match — this old unit is deleted
                chunks.append(DiffChunk(
                    diff_type=DiffType.DELETION,
                    old_text=old_text,
                    new_text="",
                    old_pos=i,
                    new_pos=-1,
                    similarity=0.0,
                ))
            else:
                matched_new.add(best_j)
                new_text = new_units[best_j]
                if best_sim >= self.UNCHANGED_THRESHOLD:
                    dtype = DiffType.UNCHANGED
                else:
                    dtype = DiffType.MODIFICATION
                chunks.append(DiffChunk(
                    diff_type=dtype,
                    old_text=old_text,
                    new_text=new_text,
                    old_pos=i,
                    new_pos=best_j,
                    similarity=best_sim,
                ))

        # Remaining new units become additions
        for j, new_text in enumerate(new_units):
            if j not in matched_new:
                chunks.append(DiffChunk(
                    diff_type=DiffType.ADDITION,
                    old_text="",
                    new_text=new_text,
                    old_pos=-1,
                    new_pos=j,
                    similarity=0.0,
                ))

        return chunks

    def diff_sentences(self, old: str, new: str) -> list[DiffChunk]:
        """Diff two texts at sentence granularity."""
        old_units = _split_sentences(old)
        new_units = _split_sentences(new)
        if not old_units and not new_units:
            return []
        return self._match_units(old_units, new_units)

    def diff_paragraphs(self, old: str, new: str) -> list[DiffChunk]:
        """Diff two texts at paragraph granularity (split on blank lines)."""
        old_units = _split_paragraphs(old)
        new_units = _split_paragraphs(new)
        if not old_units and not new_units:
            return []
        return self._match_units(old_units, new_units)

    def diff_words(self, old: str, new: str) -> list[DiffChunk]:
        """Word-level LCS diff producing ADDITION and DELETION chunks only."""
        old_words = _split_words(old)
        new_words = _split_words(new)

        if not old_words and not new_words:
            return []

        lcs_pairs = _lcs_indices(old_words, new_words)

        chunks: list[DiffChunk] = []
        matched_old = {i for i, _ in lcs_pairs}
        matched_new = {j for _, j in lcs_pairs}

        # Unchanged words
        for i, j in lcs_pairs:
            chunks.append(DiffChunk(
                diff_type=DiffType.UNCHANGED,
                old_text=old_words[i],
                new_text=new_words[j],
                old_pos=i,
                new_pos=j,
                similarity=1.0,
            ))

        # Deleted words (in old but not in LCS)
        for i, word in enumerate(old_words):
            if i not in matched_old:
                chunks.append(DiffChunk(
                    diff_type=DiffType.DELETION,
                    old_text=word,
                    new_text="",
                    old_pos=i,
                    new_pos=-1,
                    similarity=0.0,
                ))

        # Added words (in new but not in LCS)
        for j, word in enumerate(new_words):
            if j not in matched_new:
                chunks.append(DiffChunk(
                    diff_type=DiffType.ADDITION,
                    old_text="",
                    new_text=word,
                    old_pos=-1,
                    new_pos=j,
                    similarity=0.0,
                ))

        # Sort by position for readability
        chunks.sort(key=lambda c: (c.old_pos if c.old_pos >= 0 else c.new_pos + 10000))
        return chunks
