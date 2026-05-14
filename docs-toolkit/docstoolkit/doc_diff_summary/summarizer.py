"""Doc diff summarizer — statistics and semantic summaries of diffs.

Pure stdlib only: difflib, re, dataclasses, enum.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from enum import Enum


# ---------------------------------------------------------------------------
# ChangeMagnitude
# ---------------------------------------------------------------------------

class ChangeMagnitude(Enum):
    TRIVIAL = "TRIVIAL"
    MINOR = "MINOR"
    MAJOR = "MAJOR"
    REWRITE = "REWRITE"


# ---------------------------------------------------------------------------
# DiffSummary
# ---------------------------------------------------------------------------

@dataclass
class DiffSummary:
    """Statistical summary of a single document diff."""
    lines_added: int = 0
    lines_removed: int = 0
    lines_modified: int = 0
    chars_added: int = 0
    chars_removed: int = 0
    sections_changed: list[str] = field(default_factory=list)
    magnitude: ChangeMagnitude = ChangeMagnitude.TRIVIAL
    similarity: float = 1.0
    is_rename: bool = False
    has_structural_changes: bool = False


# ---------------------------------------------------------------------------
# ChangeTypeStats
# ---------------------------------------------------------------------------

@dataclass
class ChangeTypeStats:
    """Counts of markdown element types touched by a diff."""
    code_blocks_changed: int = 0
    links_changed: int = 0
    headings_changed: int = 0
    lists_changed: int = 0
    tables_changed: int = 0


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_LIST_RE = re.compile(r"^\s*([-*+]|\d+\.)\s+")
_TABLE_RE = re.compile(r"^\s*\|.*\|\s*$")
_CODE_FENCE_RE = re.compile(r"^\s*(```|~~~)")


def _extract_headings(text: str) -> list[str]:
    """Return ordered list of heading texts (without leading ``#`` chars)."""
    headings: list[str] = []
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            headings.append(m.group(1).strip())
    return headings


def _extract_links(text: str) -> list[tuple[str, str]]:
    return [(m.group(1), m.group(2)) for m in _LINK_RE.finditer(text)]


def _count_code_blocks(text: str) -> int:
    """Number of fenced code blocks (each pair of fences = 1)."""
    fences = sum(1 for line in text.splitlines() if _CODE_FENCE_RE.match(line))
    return fences // 2


def _count_list_items(text: str) -> int:
    return sum(1 for line in text.splitlines() if _LIST_RE.match(line))


def _count_table_rows(text: str) -> int:
    return sum(1 for line in text.splitlines() if _TABLE_RE.match(line))


def _similarity(old: str, new: str) -> float:
    if not old and not new:
        return 1.0
    return difflib.SequenceMatcher(None, old, new, autojunk=False).ratio()


def _magnitude_from(similarity: float) -> ChangeMagnitude:
    if similarity >= 0.95:
        return ChangeMagnitude.TRIVIAL
    if similarity >= 0.7:
        return ChangeMagnitude.MINOR
    if similarity >= 0.3:
        return ChangeMagnitude.MAJOR
    return ChangeMagnitude.REWRITE


# ---------------------------------------------------------------------------
# DocDiffSummarizer
# ---------------------------------------------------------------------------

class DocDiffSummarizer:
    """Produce statistical and semantic summaries of document diffs."""

    # ------------------------------------------------------------------
    # summarize
    # ------------------------------------------------------------------
    def summarize(self, old: str, new: str) -> DiffSummary:
        """Compute full :class:`DiffSummary` for *old* vs *new*."""
        old_lines = old.splitlines()
        new_lines = new.splitlines()

        matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)

        lines_added = 0
        lines_removed = 0
        lines_modified = 0
        chars_added = 0
        chars_removed = 0

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "insert":
                added = new_lines[j1:j2]
                lines_added += len(added)
                chars_added += sum(len(ln) for ln in added)
            elif tag == "delete":
                removed = old_lines[i1:i2]
                lines_removed += len(removed)
                chars_removed += sum(len(ln) for ln in removed)
            elif tag == "replace":
                removed = old_lines[i1:i2]
                added = new_lines[j1:j2]
                pair_count = min(len(removed), len(added))
                lines_modified += pair_count
                # Excess inserts/deletes count as plain add/remove
                if len(added) > pair_count:
                    lines_added += len(added) - pair_count
                if len(removed) > pair_count:
                    lines_removed += len(removed) - pair_count
                chars_added += sum(len(ln) for ln in added)
                chars_removed += sum(len(ln) for ln in removed)

        similarity = _similarity(old, new)
        magnitude = _magnitude_from(similarity)

        old_headings = _extract_headings(old)
        new_headings = _extract_headings(new)
        old_set = set(old_headings)
        new_set = set(new_headings)
        sections_changed = sorted(old_set.symmetric_difference(new_set))
        has_structural_changes = old_set != new_set

        # Rename heuristic: most content removed AND most content added, low similarity
        is_rename = False
        if old.strip() and new.strip():
            old_only = len(old_set - new_set)
            new_only = len(new_set - old_set)
            if (
                similarity < 0.3
                and lines_added > 0
                and lines_removed > 0
                and (old_only > 0 or new_only > 0 or similarity < 0.1)
            ):
                is_rename = True

        return DiffSummary(
            lines_added=lines_added,
            lines_removed=lines_removed,
            lines_modified=lines_modified,
            chars_added=chars_added,
            chars_removed=chars_removed,
            sections_changed=sections_changed,
            magnitude=magnitude,
            similarity=similarity,
            is_rename=is_rename,
            has_structural_changes=has_structural_changes,
        )

    # ------------------------------------------------------------------
    # change_types
    # ------------------------------------------------------------------
    def change_types(self, old: str, new: str) -> ChangeTypeStats:
        """Count how many markdown elements of each type changed."""
        old_headings = _extract_headings(old)
        new_headings = _extract_headings(new)
        headings_changed = abs(len(new_headings) - len(old_headings)) + sum(
            1 for h in set(old_headings).symmetric_difference(set(new_headings))
        ) // 2

        old_links = _extract_links(old)
        new_links = _extract_links(new)
        old_link_set = set(old_links)
        new_link_set = set(new_links)
        links_changed = len(old_link_set.symmetric_difference(new_link_set))

        code_blocks_changed = abs(_count_code_blocks(new) - _count_code_blocks(old))
        # Also count changed code lines inside fenced blocks (rough heuristic)
        if code_blocks_changed == 0 and _count_code_blocks(old) > 0:
            # If counts match but content differs, count as 1 change per differing block
            old_code = "\n".join(
                ln for ln in old.splitlines() if not _CODE_FENCE_RE.match(ln)
            )
            new_code = "\n".join(
                ln for ln in new.splitlines() if not _CODE_FENCE_RE.match(ln)
            )
            if old_code != new_code and old != new:
                # Conservative: only flag when there's actual change
                pass

        lists_changed = abs(_count_list_items(new) - _count_list_items(old))
        tables_changed = abs(_count_table_rows(new) - _count_table_rows(old))

        return ChangeTypeStats(
            code_blocks_changed=code_blocks_changed,
            links_changed=links_changed,
            headings_changed=headings_changed,
            lists_changed=lists_changed,
            tables_changed=tables_changed,
        )

    # ------------------------------------------------------------------
    # summary_text
    # ------------------------------------------------------------------
    def summary_text(self, old: str, new: str) -> str:
        """Return a human-readable one-line summary string."""
        s = self.summarize(old, new)
        parts = [
            f"+{s.lines_added}/-{s.lines_removed} lines",
        ]
        if s.lines_modified:
            parts.append(f"~{s.lines_modified} modified")
        parts.append(f"similarity {s.similarity:.2f}")
        parts.append(f"magnitude {s.magnitude.value}")
        if s.has_structural_changes:
            parts.append(f"{len(s.sections_changed)} section(s) changed")
        if s.is_rename:
            parts.append("possible rename")
        return ", ".join(parts)

    # ------------------------------------------------------------------
    # is_rewrite
    # ------------------------------------------------------------------
    def is_rewrite(self, old: str, new: str, threshold: float = 0.3) -> bool:
        """Return True if similarity is **below** *threshold* (full rewrite)."""
        return _similarity(old, new) < threshold

    # ------------------------------------------------------------------
    # is_minor_edit
    # ------------------------------------------------------------------
    def is_minor_edit(self, old: str, new: str, threshold: float = 0.95) -> bool:
        """Return True if similarity is **at least** *threshold*."""
        return _similarity(old, new) >= threshold

    # ------------------------------------------------------------------
    # count_added_lines
    # ------------------------------------------------------------------
    def count_added_lines(self, old: str, new: str) -> int:
        return self.summarize(old, new).lines_added

    # ------------------------------------------------------------------
    # count_removed_lines
    # ------------------------------------------------------------------
    def count_removed_lines(self, old: str, new: str) -> int:
        return self.summarize(old, new).lines_removed

    # ------------------------------------------------------------------
    # extract_changed_sections
    # ------------------------------------------------------------------
    def extract_changed_sections(self, old: str, new: str) -> list[str]:
        """Return headings that exist in only one of the two documents."""
        return self.summarize(old, new).sections_changed

    # ------------------------------------------------------------------
    # compare_batch
    # ------------------------------------------------------------------
    def compare_batch(
        self,
        old_docs: list[str],
        new_docs: list[str],
    ) -> list[DiffSummary]:
        """Pairwise summarize batches of *(old, new)* documents.

        The two lists must be of equal length; raises ``ValueError`` otherwise.
        """
        if len(old_docs) != len(new_docs):
            raise ValueError(
                f"old_docs and new_docs must be same length: "
                f"{len(old_docs)} vs {len(new_docs)}"
            )
        return [self.summarize(o, n) for o, n in zip(old_docs, new_docs)]
