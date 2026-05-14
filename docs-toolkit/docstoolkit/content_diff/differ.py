"""Content diff — line-level and section-level document diffing.

Pure stdlib only: difflib, re, dataclasses, enum.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# ChangeType
# ---------------------------------------------------------------------------

class ChangeType(Enum):
    ADDED = "ADDED"
    REMOVED = "REMOVED"
    UNCHANGED = "UNCHANGED"
    MODIFIED = "MODIFIED"


# ---------------------------------------------------------------------------
# LineChange
# ---------------------------------------------------------------------------

@dataclass
class LineChange:
    """Represents a single line in a diff result."""
    line_num_old: Optional[int]
    line_num_new: Optional[int]
    content: str
    change_type: ChangeType


# ---------------------------------------------------------------------------
# SectionChange
# ---------------------------------------------------------------------------

@dataclass
class SectionChange:
    """Changes grouped under a single markdown heading section."""
    heading: str
    changes: list[LineChange] = field(default_factory=list)
    change_type: ChangeType = ChangeType.UNCHANGED


# ---------------------------------------------------------------------------
# DiffResult
# ---------------------------------------------------------------------------

@dataclass
class DiffResult:
    """Structured result of a line-level diff operation."""
    changes: list[LineChange] = field(default_factory=list)

    @property
    def added_count(self) -> int:
        return sum(1 for c in self.changes if c.change_type == ChangeType.ADDED)

    @property
    def removed_count(self) -> int:
        return sum(1 for c in self.changes if c.change_type == ChangeType.REMOVED)

    @property
    def unchanged_count(self) -> int:
        return sum(1 for c in self.changes if c.change_type == ChangeType.UNCHANGED)

    @property
    def similarity(self) -> float:
        """Ratio of unchanged lines to total lines (0.0–1.0)."""
        total = len(self.changes)
        if total == 0:
            return 1.0
        return self.unchanged_count / total

    @property
    def has_changes(self) -> bool:
        return self.added_count > 0 or self.removed_count > 0

    @property
    def summary(self) -> str:
        return f"+{self.added_count}/-{self.removed_count} lines"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _split_into_sections(text: str) -> list[tuple[str, list[str]]]:
    """Split *text* into ``(heading, lines)`` pairs.

    Lines before the first heading are collected under the empty string heading
    ``""``.  Each subsequent ``#``-prefixed line starts a new section.
    """
    sections: list[tuple[str, list[str]]] = []
    current_heading = ""
    current_lines: list[str] = []

    for line in text.splitlines():
        if re.match(r"^#{1,6}\s", line):
            sections.append((current_heading, current_lines))
            current_heading = line.strip()
            current_lines = []
        else:
            current_lines.append(line)

    sections.append((current_heading, current_lines))
    return sections


# ---------------------------------------------------------------------------
# ContentDiffer
# ---------------------------------------------------------------------------

class ContentDiffer:
    """Compare two text documents and produce structured diff output."""

    # ------------------------------------------------------------------
    # diff
    # ------------------------------------------------------------------
    def diff(self, old_text: str, new_text: str) -> DiffResult:
        """Line-level diff of *old_text* vs *new_text*.

        Uses ``difflib.SequenceMatcher`` opcodes to classify every line as
        ADDED, REMOVED, or UNCHANGED.
        """
        old_lines = old_text.splitlines()
        new_lines = new_text.splitlines()

        matcher = difflib.SequenceMatcher(None, old_lines, new_lines, autojunk=False)
        line_changes: list[LineChange] = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == "equal":
                for offset, (old_ln, new_ln) in enumerate(
                    zip(range(i1, i2), range(j1, j2))
                ):
                    line_changes.append(LineChange(
                        line_num_old=old_ln + 1,
                        line_num_new=new_ln + 1,
                        content=old_lines[old_ln],
                        change_type=ChangeType.UNCHANGED,
                    ))
            elif tag == "insert":
                for new_ln in range(j1, j2):
                    line_changes.append(LineChange(
                        line_num_old=None,
                        line_num_new=new_ln + 1,
                        content=new_lines[new_ln],
                        change_type=ChangeType.ADDED,
                    ))
            elif tag == "delete":
                for old_ln in range(i1, i2):
                    line_changes.append(LineChange(
                        line_num_old=old_ln + 1,
                        line_num_new=None,
                        content=old_lines[old_ln],
                        change_type=ChangeType.REMOVED,
                    ))
            elif tag == "replace":
                # Emit removed lines first, then added lines
                for old_ln in range(i1, i2):
                    line_changes.append(LineChange(
                        line_num_old=old_ln + 1,
                        line_num_new=None,
                        content=old_lines[old_ln],
                        change_type=ChangeType.REMOVED,
                    ))
                for new_ln in range(j1, j2):
                    line_changes.append(LineChange(
                        line_num_old=None,
                        line_num_new=new_ln + 1,
                        content=new_lines[new_ln],
                        change_type=ChangeType.ADDED,
                    ))

        return DiffResult(changes=line_changes)

    # ------------------------------------------------------------------
    # diff_sections
    # ------------------------------------------------------------------
    def diff_sections(self, old_text: str, new_text: str) -> list[SectionChange]:
        """Diff *old_text* vs *new_text* grouped by markdown heading sections.

        Each ``#``-prefixed line starts a new section.  Changes within each
        section are collected as ``LineChange`` objects.  The overall
        ``SectionChange.change_type`` is:

        * ``UNCHANGED`` — no lines added or removed inside the section
        * ``ADDED``     — section heading exists only in new text
        * ``REMOVED``   — section heading exists only in old text
        * ``MODIFIED``  — section exists in both but has line-level changes
        """
        old_sections = _split_into_sections(old_text)
        new_sections = _split_into_sections(new_text)

        old_map: dict[str, list[str]] = {}
        for heading, lines in old_sections:
            old_map.setdefault(heading, []).extend(lines)

        new_map: dict[str, list[str]] = {}
        for heading, lines in new_sections:
            new_map.setdefault(heading, []).extend(lines)

        # Preserve order: old headings first, then new-only headings
        seen: set[str] = set()
        ordered_headings: list[str] = []
        for heading, _ in old_sections:
            if heading not in seen:
                seen.add(heading)
                ordered_headings.append(heading)
        for heading, _ in new_sections:
            if heading not in seen:
                seen.add(heading)
                ordered_headings.append(heading)

        result: list[SectionChange] = []

        for heading in ordered_headings:
            in_old = heading in old_map
            in_new = heading in new_map

            if in_old and not in_new:
                # Whole section removed
                old_lines = old_map[heading]
                changes = [
                    LineChange(
                        line_num_old=idx + 1,
                        line_num_new=None,
                        content=line,
                        change_type=ChangeType.REMOVED,
                    )
                    for idx, line in enumerate(old_lines)
                ]
                result.append(SectionChange(
                    heading=heading,
                    changes=changes,
                    change_type=ChangeType.REMOVED,
                ))
            elif in_new and not in_old:
                # Whole section added
                new_lines = new_map[heading]
                changes = [
                    LineChange(
                        line_num_old=None,
                        line_num_new=idx + 1,
                        content=line,
                        change_type=ChangeType.ADDED,
                    )
                    for idx, line in enumerate(new_lines)
                ]
                result.append(SectionChange(
                    heading=heading,
                    changes=changes,
                    change_type=ChangeType.ADDED,
                ))
            else:
                # Section exists in both — diff its lines
                section_diff = self.diff(
                    "\n".join(old_map[heading]),
                    "\n".join(new_map[heading]),
                )
                has_change = section_diff.has_changes
                result.append(SectionChange(
                    heading=heading,
                    changes=section_diff.changes,
                    change_type=ChangeType.MODIFIED if has_change else ChangeType.UNCHANGED,
                ))

        return result

    # ------------------------------------------------------------------
    # unified_diff
    # ------------------------------------------------------------------
    def unified_diff(
        self,
        old_text: str,
        new_text: str,
        context: int = 3,
    ) -> str:
        """Return a unified diff string (similar to ``diff -u``)."""
        old_lines = old_text.splitlines(keepends=True)
        new_lines = new_text.splitlines(keepends=True)
        result = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="old",
            tofile="new",
            n=context,
        )
        return "".join(result)

    # ------------------------------------------------------------------
    # is_similar
    # ------------------------------------------------------------------
    def is_similar(
        self,
        old_text: str,
        new_text: str,
        threshold: float = 0.8,
    ) -> bool:
        """Return True if the two texts are at least *threshold* similar.

        Uses ``difflib.SequenceMatcher.ratio()`` for character-level
        similarity.
        """
        ratio = difflib.SequenceMatcher(None, old_text, new_text).ratio()
        return ratio >= threshold

    # ------------------------------------------------------------------
    # extract_changes
    # ------------------------------------------------------------------
    def extract_changes(self, old_text: str, new_text: str) -> dict[str, list[str]]:
        """Return a dict with ``"added"`` and ``"removed"`` line lists."""
        result = self.diff(old_text, new_text)
        added = [c.content for c in result.changes if c.change_type == ChangeType.ADDED]
        removed = [c.content for c in result.changes if c.change_type == ChangeType.REMOVED]
        return {"added": added, "removed": removed}
