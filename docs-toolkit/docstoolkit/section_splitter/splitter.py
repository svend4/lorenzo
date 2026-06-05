"""section_splitter — splits markdown documents into logical sections (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r'^(#{1,6})\s+(.*)')


def _heading_level(line: str) -> tuple[int, str]:
    """Return (level, text) if *line* is a markdown heading, else (0, '')."""
    m = _HEADING_RE.match(line)
    if m:
        return len(m.group(1)), m.group(2).strip()
    return 0, ''


def _word_count(text: str) -> int:
    return len(text.split())


# ---------------------------------------------------------------------------
# Section dataclass
# ---------------------------------------------------------------------------

@dataclass
class Section:
    """A logical section of a markdown document."""

    heading: str
    level: int
    content: str
    line_start: int
    line_end: int
    subsections: list['Section'] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def word_count(self) -> int:
        """Number of words in the section body."""
        return _word_count(self.content)

    @property
    def is_empty(self) -> bool:
        """True if content is empty or whitespace only."""
        return not self.content.strip()


# ---------------------------------------------------------------------------
# SplitConfig dataclass
# ---------------------------------------------------------------------------

@dataclass
class SplitConfig:
    """Configuration for SectionSplitter."""

    max_level: int = 6
    include_preamble: bool = True
    min_words: int = 0


# ---------------------------------------------------------------------------
# SectionSplitter
# ---------------------------------------------------------------------------

class SectionSplitter:
    """Splits markdown text into logical sections."""

    def __init__(self, config: Optional[SplitConfig] = None) -> None:
        self.config = config or SplitConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def split(self, text: str) -> list[Section]:
        """Return a flat list of top-level sections.

        A new section begins at every heading whose level is within
        ``config.max_level``.  The preamble (content before the first
        heading) is included when ``config.include_preamble`` is True.
        Sections with fewer words than ``config.min_words`` are skipped.
        """
        lines = text.splitlines(keepends=False)
        cfg = self.config
        sections: list[Section] = []

        # Each "pending" section is: (heading, level, line_start, body_lines_list)
        current_heading = ''
        current_level = 0
        current_start = 1  # 1-based
        current_body: list[str] = []

        def _flush(end_line: int) -> None:
            body = '\n'.join(current_body)
            wc = _word_count(body)
            if current_level == 0 and not cfg.include_preamble:
                return
            if wc < cfg.min_words and not (current_level == 0 and not body.strip()):
                # Still skip preamble check: only skip non-preamble? Actually
                # min_words applies to all sections including preamble.
                return
            if wc < cfg.min_words:
                return
            sections.append(Section(
                heading=current_heading,
                level=current_level,
                content=body,
                line_start=current_start,
                line_end=end_line,
            ))

        for i, line in enumerate(lines):
            lineno = i + 1  # 1-based
            lvl, heading_text = _heading_level(line)
            if lvl > 0 and lvl <= cfg.max_level:
                # Close previous section
                _flush(lineno - 1 if current_body else lineno - 1)
                # Start new section
                current_heading = heading_text
                current_level = lvl
                current_start = lineno
                current_body = []
            else:
                current_body.append(line)

        # Flush last section
        _flush(len(lines) if lines else 1)

        return sections

    def split_hierarchical(self, text: str) -> list[Section]:
        """Return a nested list of sections with subsections populated.

        Each heading becomes a subsection of the nearest preceding heading
        with a strictly lower level number.  Only top-level sections
        (those with no parent) are in the returned list; their children
        are in ``subsections``.
        """
        flat = self.split(text)
        if not flat:
            return []

        # Build tree using a stack.
        # stack contains sections whose subtree is still open.
        result: list[Section] = []
        # stack items: Section objects at increasing levels
        stack: list[Section] = []

        for sec in flat:
            if sec.level == 0:
                # Preamble: always top-level
                result.append(sec)
                # Don't push preamble onto the heading stack
                continue

            # Pop stack entries whose level >= current section's level
            while stack and stack[-1].level >= sec.level:
                stack.pop()

            if stack:
                stack[-1].subsections.append(sec)
            else:
                result.append(sec)

            stack.append(sec)

        return result

    def split_by_level(self, text: str, level: int) -> list[Section]:
        """Return sections that start with a heading of exactly *level*.

        Headings at other levels are treated as body text.
        """
        cfg = self.config
        lines = text.splitlines(keepends=False)
        sections: list[Section] = []

        current_heading = ''
        current_level_val = 0
        current_start = 1
        current_body: list[str] = []
        in_section = False

        def _flush(end_line: int) -> None:
            if not in_section and not cfg.include_preamble:
                return
            body = '\n'.join(current_body)
            wc = _word_count(body)
            if wc < cfg.min_words:
                return
            sections.append(Section(
                heading=current_heading,
                level=current_level_val,
                content=body,
                line_start=current_start,
                line_end=end_line,
            ))

        for i, line in enumerate(lines):
            lineno = i + 1
            lvl, heading_text = _heading_level(line)
            if lvl == level:
                _flush(lineno - 1 if current_body or in_section else lineno - 1)
                current_heading = heading_text
                current_level_val = lvl
                current_start = lineno
                current_body = []
                in_section = True
            else:
                current_body.append(line)

        _flush(len(lines) if lines else 1)

        return sections

    def flatten(self, sections: list[Section]) -> list[Section]:
        """Flatten a nested section tree into a depth-first list."""
        result: list[Section] = []
        for sec in sections:
            result.append(sec)
            if sec.subsections:
                result.extend(self.flatten(sec.subsections))
        return result

    def find_section(
        self, sections: list[Section], heading: str
    ) -> Optional[Section]:
        """Find a section by heading text (case-insensitive, recursive)."""
        target = heading.lower()
        for sec in sections:
            if sec.heading.lower() == target:
                return sec
            found = self.find_section(sec.subsections, heading)
            if found is not None:
                return found
        return None

    def to_dict(self, section: Section) -> dict:
        """Return a serializable dict for *section* (no subsections recursion)."""
        return {
            'heading': section.heading,
            'level': section.level,
            'content': section.content,
            'word_count': section.word_count,
        }
