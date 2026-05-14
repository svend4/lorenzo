"""Timeline extraction module for docs-toolkit.

Extracts structured timeline events from plain text using pure-stdlib regex.

Supports:
- ISO dates (2024-01-31)
- English full dates (January 31, 2024)
- Russian month+year (январь 2024)
- Year-only (2024, 1999)

Usage::

    from docstoolkit.timeline import TimelineExtractor, Timeline, TimelineEvent, EventType

    extractor = TimelineExtractor()
    events = extractor.extract(text)

    tl = Timeline(events)
    print(tl.summary())
    print(tl.to_markdown())
"""
from docstoolkit.timeline.event import EventType, TimelineEvent
from docstoolkit.timeline.extractor import DatePattern, TimelineExtractor
from docstoolkit.timeline.timeline import Timeline

__all__ = [
    # event
    "EventType",
    "TimelineEvent",
    # extractor
    "DatePattern",
    "TimelineExtractor",
    # timeline
    "Timeline",
]
