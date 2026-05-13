"""E122 Document formatter — formats and normalizes document text, stdlib only.

Public API
----------
:class:`FormatRule`      — enum of available formatting rules
:class:`FormatConfig`    — configuration dataclass for DocFormatter
:class:`FormatterResult` — result of a single format() call
:class:`DocFormatter`    — main formatter class
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List


class FormatRule(Enum):
    """Enumeration of available document formatting rules."""

    STRIP_TRAILING_WHITESPACE = auto()
    NORMALIZE_HEADINGS = auto()
    COLLAPSE_BLANK_LINES = auto()
    ENSURE_FINAL_NEWLINE = auto()
    NORMALIZE_BULLETS = auto()
    FIX_HEADING_LEVELS = auto()


@dataclass
class FormatConfig:
    """Configuration for :class:`DocFormatter`.

    Attributes:
        rules:               Which rules to apply. Defaults to all rules.
        max_blank_lines:     Maximum consecutive blank lines to allow (for
                             COLLAPSE_BLANK_LINES rule).
        heading_start_level: Minimum heading level that should appear in the
                             document (for FIX_HEADING_LEVELS rule).
    """

    rules: List[FormatRule] = field(
        default_factory=lambda: list(FormatRule)
    )
    max_blank_lines: int = 2
    heading_start_level: int = 1


@dataclass
class FormatterResult:
    """Result of a :meth:`DocFormatter.format` call.

    Attributes:
        original:      The original text before formatting.
        formatted:     The text after all requested rules have been applied.
        rules_applied: The ordered list of rules that were applied.
    """

    original: str
    formatted: str
    rules_applied: List[FormatRule]

    @property
    def changed(self) -> bool:
        """True when *formatted* differs from *original*."""
        return self.original != self.formatted

    @property
    def change_count(self) -> int:
        """Number of lines that differ between *original* and *formatted*.

        Lines are compared position-by-position after splitting on ``\\n``.
        Lines that exist only in the longer version also count as changed.
        """
        orig_lines = self.original.split("\n")
        fmt_lines = self.formatted.split("\n")
        max_len = max(len(orig_lines), len(fmt_lines))
        # Pad shorter list with sentinel that never matches a real line
        _MISSING = object()
        orig_padded = orig_lines + [_MISSING] * (max_len - len(orig_lines))  # type: ignore[list-item]
        fmt_padded = fmt_lines + [_MISSING] * (max_len - len(fmt_lines))  # type: ignore[list-item]
        return sum(1 for a, b in zip(orig_padded, fmt_padded) if a != b)


class DocFormatter:
    """Format and normalize document text.

    Usage::

        formatter = DocFormatter()
        result = formatter.format("# heading\\nsome text   \\n")
        print(result.formatted)

    Or with a custom config::

        config = FormatConfig(
            rules=[FormatRule.STRIP_TRAILING_WHITESPACE],
            max_blank_lines=1,
        )
        formatter = DocFormatter(config)
    """

    def __init__(self, config: FormatConfig | None = None) -> None:
        self._config: FormatConfig = config if config is not None else FormatConfig()

    # ------------------------------------------------------------------
    # Individual rule methods (public, callable directly)
    # ------------------------------------------------------------------

    def strip_trailing_whitespace(self, text: str) -> str:
        """Remove trailing spaces and tabs from each line."""
        return re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    def normalize_headings(self, text: str) -> str:
        """Ensure a single space between the ``#`` prefix and heading text.

        A heading like ``##Title`` becomes ``## Title``.  Headings that
        already have a space (``## Title``) are left untouched.
        """
        return re.sub(r"^(#{1,6})([^ #\n])", r"\1 \2", text, flags=re.MULTILINE)

    def collapse_blank_lines(self, text: str, max_blank: int = 2) -> str:
        """Reduce runs of more than *max_blank* consecutive blank lines.

        A "blank line" is a line that contains only optional whitespace.
        """
        # Build a pattern that matches (max_blank + 1) or more consecutive
        # blank lines (each blank line is \\n followed by optional spaces).
        # We match the excess blank lines and replace the run with exactly
        # max_blank blank lines.
        blank_line = r"[ \t]*\n"
        pattern = r"(" + blank_line + r"){" + str(max_blank + 1) + r",}"

        replacement = "\n" * max_blank

        return re.sub(pattern, replacement, text)

    def ensure_final_newline(self, text: str) -> str:
        """Append a trailing ``\\n`` if *text* does not already end with one."""
        if text and not text.endswith("\n"):
            return text + "\n"
        return text

    def normalize_bullets(self, text: str) -> str:
        """Convert ``*`` and ``+`` list bullets to ``-``.

        Only unordered list items at the start of a line are converted.
        The space after the bullet marker is preserved.
        """
        return re.sub(r"^[*+]( )", r"-\1", text, flags=re.MULTILINE)

    def fix_heading_levels(self, text: str, start_level: int = 1) -> str:
        """Shift all headings so that the minimum level equals *start_level*.

        If the document's minimum heading level is already ``start_level``
        the text is returned unchanged.  If all headings are at level 3 and
        ``start_level=1`` each heading loses 2 ``#`` characters.  If
        ``start_level=2`` and the minimum is 1 each heading gains one ``#``.

        Only lines that begin with one to six ``#`` characters followed by a
        space or end-of-line are treated as headings.
        """
        heading_pattern = re.compile(r"^(#{1,6})([ \n]|$)", re.MULTILINE)
        matches = heading_pattern.findall(text)
        if not matches:
            return text

        levels = [len(hashes) for hashes, _ in matches]
        min_level = min(levels)
        shift = start_level - min_level

        if shift == 0:
            return text

        def _adjust(match: re.Match) -> str:
            hashes: str = match.group(1)
            rest: str = match.group(2)
            new_level = max(1, min(6, len(hashes) + shift))
            return "#" * new_level + rest

        return heading_pattern.sub(_adjust, text)

    # ------------------------------------------------------------------
    # Main formatting entry points
    # ------------------------------------------------------------------

    def format(self, text: str) -> FormatterResult:
        """Apply all configured rules to *text* and return a :class:`FormatterResult`.

        Rules are applied in the order they appear in :class:`FormatRule`
        (declaration order), filtered to those present in
        ``config.rules``.
        """
        rules_applied: List[FormatRule] = []
        result = text

        # Iterate in canonical enum order so behaviour is deterministic
        # regardless of the order the caller listed rules.
        for rule in FormatRule:
            if rule not in self._config.rules:
                continue
            rules_applied.append(rule)
            if rule is FormatRule.STRIP_TRAILING_WHITESPACE:
                result = self.strip_trailing_whitespace(result)
            elif rule is FormatRule.NORMALIZE_HEADINGS:
                result = self.normalize_headings(result)
            elif rule is FormatRule.COLLAPSE_BLANK_LINES:
                result = self.collapse_blank_lines(result, self._config.max_blank_lines)
            elif rule is FormatRule.ENSURE_FINAL_NEWLINE:
                result = self.ensure_final_newline(result)
            elif rule is FormatRule.NORMALIZE_BULLETS:
                result = self.normalize_bullets(result)
            elif rule is FormatRule.FIX_HEADING_LEVELS:
                result = self.fix_heading_levels(result, self._config.heading_start_level)

        return FormatterResult(
            original=text,
            formatted=result,
            rules_applied=rules_applied,
        )

    def format_batch(self, texts: list[str]) -> list[FormatterResult]:
        """Format each string in *texts* and return one result per input."""
        return [self.format(t) for t in texts]
