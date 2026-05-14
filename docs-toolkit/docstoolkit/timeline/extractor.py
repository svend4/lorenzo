"""TimelineExtractor: regex-based date extraction from text.

Supports:
- ISO dates (YYYY-MM-DD)
- English full dates (Month DD, YYYY)
- Russian month+year (Месяц YYYY)
- Year-only (19xx / 20xx)

No external dependencies — pure stdlib.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Sequence

from docstoolkit.timeline.event import EventType, TimelineEvent

# ---------------------------------------------------------------------------
# Russian month name → number mapping
# ---------------------------------------------------------------------------

_RU_MONTH: dict[str, int] = {
    "январ": 1,
    "феврал": 2,
    "март": 3,    # prefix shares with "март" exactly; fine because regex captures stem
    "апрел": 4,
    "май": 5,
    "июн": 6,
    "июл": 7,
    "август": 8,
    "сентябр": 9,
    "октябр": 10,
    "ноябр": 11,
    "декабр": 12,
}

# английский месяц → число
_EN_MONTH: dict[str, int] = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}

# ---------------------------------------------------------------------------
# Keyword → EventType mapping (checked against context window, lower-cased)
# ---------------------------------------------------------------------------

_TYPE_KEYWORDS: list[tuple[list[str], EventType]] = [
    # RELEASE must come before ANNOUNCEMENT so "release" takes priority
    (["release", "released", "выпуск", "выпущен", "вышел", "вышла", "запуск", "version", "версия", "v1", "v2", "v3", "релиз"], EventType.RELEASE),
    (["announce", "announced", "announcement", "объяв", "анонс"], EventType.ANNOUNCEMENT),
    (["milestone", "веха", "milestone"], EventType.MILESTONE),
    (["deadline", "дедлайн", "срок", "крайний"], EventType.DEADLINE),
    (["meeting", "встреча", "митинг", "конференц"], EventType.MEETING),
    (["publication", "published", "публикац", "опубликован", "paper", "статья"], EventType.PUBLICATION),
]


def _classify_event_type(context: str) -> EventType:
    """Classify event type based on keywords in surrounding context."""
    lower = context.lower()
    for keywords, etype in _TYPE_KEYWORDS:
        for kw in keywords:
            if kw in lower:
                return etype
    return EventType.UNKNOWN


# ---------------------------------------------------------------------------
# DatePattern descriptor
# ---------------------------------------------------------------------------

@dataclass
class DatePattern:
    """Compiled regex pattern with group index metadata."""

    pattern: str
    year_group: int
    month_group: int | None
    day_group: int | None
    confidence: float


# ---------------------------------------------------------------------------
# Pre-compiled patterns (module-level for efficiency)
# ---------------------------------------------------------------------------

# ISO: 2024-01-31 or 2024-1-5
_PAT_ISO = re.compile(r"\b(\d{4})-(\d{1,2})-(\d{1,2})\b")

# English: January 31, 2024  /  January 31 2024  /  January 2024
_PAT_EN = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|December)"
    r"\s+(\d{1,2}),?\s+(\d{4})\b",
    re.IGNORECASE,
)

# Russian month + year: январе 2024 / февраль 2024
_PAT_RU = re.compile(
    r"\b(январ|феврал|март|апрел|май|июн|июл|август|сентябр|октябр|ноябр|декабр)\w*"
    r"\s+(\d{4})\b",
    re.IGNORECASE,
)

# Year only: 2024, 1999, but NOT inside a larger number
_PAT_YEAR = re.compile(r"\b(20\d{2}|19\d{2})\b")

# Dedup key: (year, month, day, description_prefix_10)
_CONTEXT_PREFIX_LEN = 10


class TimelineExtractor:
    """Extract timeline events from plain text using regex patterns.

    Usage::

        extractor = TimelineExtractor()
        events = extractor.extract(text)
    """

    def __init__(self) -> None:
        self._patterns: list[DatePattern] = [
            DatePattern(
                pattern=_PAT_ISO.pattern,
                year_group=1,
                month_group=2,
                day_group=3,
                confidence=0.95,
            ),
            DatePattern(
                pattern=_PAT_EN.pattern,
                year_group=3,
                month_group=1,
                day_group=2,
                confidence=0.9,
            ),
            DatePattern(
                pattern=_PAT_RU.pattern,
                year_group=2,
                month_group=1,
                day_group=None,
                confidence=0.8,
            ),
            DatePattern(
                pattern=_PAT_YEAR.pattern,
                year_group=1,
                month_group=None,
                day_group=None,
                confidence=0.5,
            ),
        ]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, text: str) -> list[TimelineEvent]:
        """Extract all timeline events from *text*.

        Returns a deduplicated, chronologically sorted list of
        :class:`~docstoolkit.timeline.event.TimelineEvent` objects.
        """
        if not text:
            return []

        raw_events = self._extract_raw(text)
        deduped = self._deduplicate(raw_events)
        return sorted(deduped, key=lambda e: e.sort_key())

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _extract_raw(self, text: str) -> list[TimelineEvent]:
        events: list[TimelineEvent] = []

        # ISO dates
        for m in _PAT_ISO.finditer(text):
            year = int(m.group(1))
            month = int(m.group(2))
            day = int(m.group(3))
            if not (1 <= month <= 12 and 1 <= day <= 31):
                continue
            ctx = self._context(text, m.start(), m.end())
            events.append(TimelineEvent(
                date_str=m.group(0),
                description=ctx[:200],
                event_type=_classify_event_type(ctx),
                source_text=ctx[:200],
                confidence=0.95,
                year=year,
                month=month,
                day=day,
            ))

        # English full dates
        for m in _PAT_EN.finditer(text):
            month_name = m.group(1).lower()
            day = int(m.group(2))
            year = int(m.group(3))
            month = _EN_MONTH.get(month_name)
            if month is None or not (1 <= day <= 31):
                continue
            ctx = self._context(text, m.start(), m.end())
            events.append(TimelineEvent(
                date_str=m.group(0),
                description=ctx[:200],
                event_type=_classify_event_type(ctx),
                source_text=ctx[:200],
                confidence=0.9,
                year=year,
                month=month,
                day=day,
            ))

        # Russian month + year
        for m in _PAT_RU.finditer(text):
            # Find which RU stem matches
            ru_stem = m.group(1).lower()
            month = None
            for stem, num in _RU_MONTH.items():
                if ru_stem.startswith(stem) or stem.startswith(ru_stem):
                    month = num
                    break
            year = int(m.group(2))
            if month is None:
                continue
            ctx = self._context(text, m.start(), m.end())
            events.append(TimelineEvent(
                date_str=m.group(0),
                description=ctx[:200],
                event_type=_classify_event_type(ctx),
                source_text=ctx[:200],
                confidence=0.8,
                year=year,
                month=month,
                day=None,
            ))

        # Year only — but only for positions NOT already covered by a more
        # specific pattern (we check by tracking covered ranges)
        covered = set()
        for m in _PAT_ISO.finditer(text):
            covered.update(range(m.start(), m.end()))
        for m in _PAT_EN.finditer(text):
            covered.update(range(m.start(), m.end()))
        for m in _PAT_RU.finditer(text):
            covered.update(range(m.start(), m.end()))

        for m in _PAT_YEAR.finditer(text):
            # Skip if any character of this match overlaps with a higher-conf match
            if any(pos in covered for pos in range(m.start(), m.end())):
                continue
            year = int(m.group(1))
            ctx = self._context(text, m.start(), m.end())
            events.append(TimelineEvent(
                date_str=m.group(0),
                description=ctx[:200],
                event_type=_classify_event_type(ctx),
                source_text=ctx[:200],
                confidence=0.5,
                year=year,
                month=None,
                day=None,
            ))

        return events

    @staticmethod
    def _context(text: str, start: int, end: int, window: int = 100) -> str:
        """Return up to *window* chars before and after the match."""
        ctx_start = max(0, start - window)
        ctx_end = min(len(text), end + window)
        return text[ctx_start:ctx_end]

    @staticmethod
    def _deduplicate(events: list[TimelineEvent]) -> list[TimelineEvent]:
        """Remove duplicate events at the same date with the same context prefix."""
        seen: set[tuple] = set()
        result: list[TimelineEvent] = []
        for ev in events:
            key = (
                ev.year,
                ev.month,
                ev.day,
                ev.source_text[:_CONTEXT_PREFIX_LEN],
            )
            if key not in seen:
                seen.add(key)
                result.append(ev)
        return result
