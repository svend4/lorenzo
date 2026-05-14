"""Timeline container for TimelineEvent objects."""
from __future__ import annotations

from docstoolkit.timeline.event import EventType, TimelineEvent


class Timeline:
    """Container for a collection of :class:`TimelineEvent` objects.

    Events are stored in insertion order; sorted views are computed on demand.
    """

    def __init__(self, events: list[TimelineEvent] | None = None) -> None:
        self._events: list[TimelineEvent] = list(events) if events else []

    # ------------------------------------------------------------------
    # Mutation
    # ------------------------------------------------------------------

    def add(self, event: TimelineEvent) -> None:
        """Append a single event to the timeline."""
        self._events.append(event)

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def events_in_year(self, year: int) -> list[TimelineEvent]:
        """Return all events whose *year* matches exactly."""
        return [e for e in self._events if e.year == year]

    def events_in_range(self, start_year: int, end_year: int) -> list[TimelineEvent]:
        """Return events where start_year <= year <= end_year.

        Events with year=None are excluded.
        """
        return [
            e for e in self._events
            if e.year is not None and start_year <= e.year <= end_year
        ]

    def by_type(self, event_type: EventType) -> list[TimelineEvent]:
        """Return all events of a given :class:`EventType`."""
        return [e for e in self._events if e.event_type == event_type]

    def sorted_events(self) -> list[TimelineEvent]:
        """Return all events sorted chronologically by sort_key()."""
        return sorted(self._events, key=lambda e: e.sort_key())

    # ------------------------------------------------------------------
    # Presentation
    # ------------------------------------------------------------------

    def summary(self) -> str:
        """Return a one-line summary: 'N events, years Y1–Y2'.

        If there are no events with a known year, omits the year range.
        """
        n = len(self._events)
        years = sorted(e.year for e in self._events if e.year is not None)
        if not years:
            return f"{n} events"
        if years[0] == years[-1]:
            return f"{n} events, year {years[0]}"
        return f"{n} events, years {years[0]}–{years[-1]}"

    def to_markdown(self) -> str:
        """Render the timeline as Markdown grouped by year.

        Each event is rendered as::

            - YYYY-MM-DD: description

        Unknown month/day components are replaced by ``??``.
        Events without a year go into an ``Unknown year`` group.
        """
        if not self._events:
            return ""

        # Group by year
        groups: dict[int | None, list[TimelineEvent]] = {}
        for ev in self.sorted_events():
            groups.setdefault(ev.year, []).append(ev)

        lines: list[str] = []

        # Known years first, then None
        known_years = sorted(y for y in groups if y is not None)
        year_order: list[int | None] = list(known_years)
        if None in groups:
            year_order.append(None)

        for year in year_order:
            heading = str(year) if year is not None else "Unknown year"
            lines.append(f"## {heading}")
            lines.append("")
            for ev in groups[year]:
                year_str = str(ev.year) if ev.year is not None else "????"
                month_str = f"{ev.month:02d}" if ev.month is not None else "??"
                day_str = f"{ev.day:02d}" if ev.day is not None else "??"
                date_label = f"{year_str}-{month_str}-{day_str}"
                lines.append(f"- {date_label}: {ev.description}")
            lines.append("")

        return "\n".join(lines).rstrip() + "\n"
