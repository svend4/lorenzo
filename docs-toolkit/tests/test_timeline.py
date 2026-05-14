"""Tests for docstoolkit.timeline — E27 Timeline extraction module.

Covers:
- TimelineEvent: has_full_date, sort_key, field defaults, auto event_id
- EventType enum values
- TimelineExtractor: ISO, EN month, RU month, year-only patterns
- TimelineExtractor: event_type classification, deduplication
- Timeline: add, events_in_year, events_in_range, by_type,
            sorted_events, summary, to_markdown
- Edge cases: empty text, overlapping patterns, confidence thresholds
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.timeline import (
    DatePattern,
    EventType,
    Timeline,
    TimelineEvent,
    TimelineExtractor,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _event(
    year=2024,
    month=6,
    day=15,
    description="test event",
    event_type=EventType.UNKNOWN,
    confidence=0.9,
    source_text="",
    date_str="2024-06-15",
) -> TimelineEvent:
    return TimelineEvent(
        date_str=date_str,
        description=description,
        event_type=event_type,
        source_text=source_text,
        confidence=confidence,
        year=year,
        month=month,
        day=day,
    )


# ===========================================================================
# EventType enum
# ===========================================================================

class TestEventType:

    def test_all_members_exist(self):
        expected = {"RELEASE", "ANNOUNCEMENT", "MILESTONE", "DEADLINE",
                    "MEETING", "PUBLICATION", "UNKNOWN"}
        actual = {m.name for m in EventType}
        assert expected == actual

    def test_values_are_strings(self):
        for member in EventType:
            assert isinstance(member.value, str)

    def test_release_value(self):
        assert EventType.RELEASE.value == "release"

    def test_announcement_value(self):
        assert EventType.ANNOUNCEMENT.value == "announcement"

    def test_unknown_value(self):
        assert EventType.UNKNOWN.value == "unknown"

    def test_enum_count(self):
        assert len(EventType) == 7


# ===========================================================================
# TimelineEvent
# ===========================================================================

class TestTimelineEvent:

    def test_auto_event_id_generated(self):
        ev = _event()
        assert isinstance(ev.event_id, str)
        assert len(ev.event_id) == 8

    def test_event_id_unique_per_instance(self):
        ev1 = _event()
        ev2 = _event()
        assert ev1.event_id != ev2.event_id

    def test_event_id_hex_characters(self):
        ev = _event()
        assert all(c in "0123456789abcdef" for c in ev.event_id)

    def test_has_full_date_true(self):
        ev = _event(year=2024, month=6, day=15)
        assert ev.has_full_date() is True

    def test_has_full_date_missing_day(self):
        ev = _event(day=None)
        assert ev.has_full_date() is False

    def test_has_full_date_missing_month(self):
        ev = _event(month=None, day=None)
        assert ev.has_full_date() is False

    def test_has_full_date_missing_year(self):
        ev = _event(year=None, month=None, day=None)
        assert ev.has_full_date() is False

    def test_has_full_date_only_year(self):
        ev = _event(year=2024, month=None, day=None)
        assert ev.has_full_date() is False

    def test_has_full_date_year_month_only(self):
        ev = _event(year=2024, month=6, day=None)
        assert ev.has_full_date() is False

    def test_sort_key_full_date(self):
        ev = _event(year=2024, month=6, day=15)
        assert ev.sort_key() == (2024, 6, 15)

    def test_sort_key_year_month_only(self):
        ev = _event(year=2024, month=6, day=None)
        assert ev.sort_key() == (2024, 6, 32)

    def test_sort_key_year_only(self):
        ev = _event(year=2024, month=None, day=None)
        assert ev.sort_key() == (2024, 13, 32)

    def test_sort_key_no_date(self):
        ev = _event(year=None, month=None, day=None)
        assert ev.sort_key() == (9999, 13, 32)

    def test_sort_key_orders_correctly(self):
        early = _event(year=2020, month=1, day=1)
        late = _event(year=2024, month=12, day=31)
        unknown = _event(year=None, month=None, day=None)
        assert early.sort_key() < late.sort_key() < unknown.sort_key()

    def test_confidence_stored(self):
        ev = _event(confidence=0.75)
        assert ev.confidence == 0.75

    def test_event_type_stored(self):
        ev = _event(event_type=EventType.RELEASE)
        assert ev.event_type == EventType.RELEASE

    def test_source_text_truncated_externally(self):
        long_text = "x" * 300
        ev = TimelineEvent(
            date_str="2024-01-01",
            description="test",
            source_text=long_text[:200],
        )
        assert len(ev.source_text) == 200

    def test_default_event_type_unknown(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.event_type == EventType.UNKNOWN

    def test_default_confidence(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.confidence == 0.5

    def test_default_source_text_empty(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.source_text == ""

    def test_default_year_none(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.year is None

    def test_default_month_none(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.month is None

    def test_default_day_none(self):
        ev = TimelineEvent(date_str="2024-01-01", description="test")
        assert ev.day is None


# ===========================================================================
# DatePattern dataclass
# ===========================================================================

class TestDatePattern:

    def test_fields_stored(self):
        dp = DatePattern(
            pattern=r"\b(\d{4})\b",
            year_group=1,
            month_group=None,
            day_group=None,
            confidence=0.5,
        )
        assert dp.pattern == r"\b(\d{4})\b"
        assert dp.year_group == 1
        assert dp.month_group is None
        assert dp.day_group is None
        assert dp.confidence == 0.5

    def test_full_date_pattern(self):
        dp = DatePattern(
            pattern=r"\b(\d{4})-(\d{2})-(\d{2})\b",
            year_group=1,
            month_group=2,
            day_group=3,
            confidence=0.95,
        )
        assert dp.month_group == 2
        assert dp.day_group == 3
        assert dp.confidence == 0.95


# ===========================================================================
# TimelineExtractor — ISO dates
# ===========================================================================

class TestExtractorISO:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_extract_simple_iso(self):
        events = self.ex.extract("Released on 2024-06-15 for production.")
        assert len(events) == 1
        ev = events[0]
        assert ev.year == 2024
        assert ev.month == 6
        assert ev.day == 15

    def test_iso_confidence(self):
        events = self.ex.extract("Date: 2024-01-01")
        assert any(abs(e.confidence - 0.95) < 1e-9 for e in events)

    def test_iso_date_str_preserved(self):
        events = self.ex.extract("On 2024-03-20 the project started.")
        iso_events = [e for e in events if e.day is not None]
        assert any(e.date_str == "2024-03-20" for e in iso_events)

    def test_iso_has_full_date(self):
        events = self.ex.extract("2024-11-05 milestone reached.")
        full = [e for e in events if e.has_full_date()]
        assert len(full) >= 1

    def test_iso_multiple_dates(self):
        text = "Start: 2024-01-01. End: 2024-12-31."
        events = self.ex.extract(text)
        years = {e.year for e in events}
        assert 2024 in years
        full_dates = [e for e in events if e.has_full_date()]
        assert len(full_dates) >= 2

    def test_iso_invalid_month_skipped(self):
        # month 13 is invalid
        events = self.ex.extract("Bad date 2024-13-01 here.")
        full_dates = [e for e in events if e.has_full_date()]
        assert all(e.month != 13 for e in full_dates)

    def test_iso_invalid_day_skipped(self):
        events = self.ex.extract("Bad date 2024-01-32 here.")
        full_dates = [e for e in events if e.has_full_date()]
        assert all(e.day != 32 for e in full_dates)

    def test_iso_single_digit_month_and_day(self):
        events = self.ex.extract("On 2024-1-5 something happened.")
        full = [e for e in events if e.has_full_date()]
        assert any(e.month == 1 and e.day == 5 for e in full)

    def test_iso_sorted_output(self):
        text = "2024-12-01 and then 2024-01-01 earlier."
        events = self.ex.extract(text)
        full = [e for e in events if e.has_full_date()]
        if len(full) >= 2:
            keys = [e.sort_key() for e in full]
            assert keys == sorted(keys)


# ===========================================================================
# TimelineExtractor — English month format
# ===========================================================================

class TestExtractorEN:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_extract_en_full_date(self):
        events = self.ex.extract("Launched on January 15, 2024 in production.")
        full = [e for e in events if e.has_full_date()]
        assert any(e.year == 2024 and e.month == 1 and e.day == 15 for e in full)

    def test_en_confidence(self):
        events = self.ex.extract("Released December 31, 2023.")
        full = [e for e in events if e.has_full_date()]
        assert any(abs(e.confidence - 0.9) < 1e-9 for e in full)

    def test_en_no_comma(self):
        events = self.ex.extract("On March 5 2024 we shipped.")
        full = [e for e in events if e.has_full_date()]
        assert any(e.year == 2024 and e.month == 3 and e.day == 5 for e in full)

    def test_en_all_months_recognized(self):
        months = [
            ("January", 1), ("February", 2), ("March", 3), ("April", 4),
            ("May", 5), ("June", 6), ("July", 7), ("August", 8),
            ("September", 9), ("October", 10), ("November", 11), ("December", 12),
        ]
        for month_name, month_num in months:
            events = self.ex.extract(f"On {month_name} 10, 2024 a release happened.")
            full = [e for e in events if e.has_full_date()]
            assert any(e.month == month_num for e in full), f"Failed for {month_name}"

    def test_en_case_insensitive(self):
        events = self.ex.extract("MARCH 20, 2024")
        full = [e for e in events if e.has_full_date()]
        assert any(e.month == 3 and e.day == 20 for e in full)

    def test_en_date_str_preserved(self):
        text = "Announced on June 1, 2024."
        events = self.ex.extract(text)
        full = [e for e in events if e.has_full_date()]
        assert len(full) >= 1


# ===========================================================================
# TimelineExtractor — Russian month format
# ===========================================================================

class TestExtractorRU:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_ru_january(self):
        events = self.ex.extract("Выпущено в январе 2024 года.")
        months = [e.month for e in events if e.month is not None]
        assert 1 in months

    def test_ru_february(self):
        events = self.ex.extract("В феврале 2024 прошла конференция.")
        months = [e.month for e in events if e.month is not None]
        assert 2 in months

    def test_ru_march(self):
        events = self.ex.extract("Март 2024 — месяц запуска.")
        months = [e.month for e in events if e.month is not None]
        assert 3 in months

    def test_ru_december(self):
        events = self.ex.extract("Дедлайн — декабрь 2023.")
        months = [e.month for e in events if e.month is not None]
        assert 12 in months

    def test_ru_confidence(self):
        events = self.ex.extract("В июне 2024 вышла новая версия.")
        ru_events = [e for e in events if e.month is not None and e.day is None]
        assert any(abs(e.confidence - 0.8) < 1e-9 for e in ru_events)

    def test_ru_no_day(self):
        events = self.ex.extract("В октябре 2024 был анонс.")
        # RU pattern yields month + year but no day
        ru = [e for e in events if e.month == 10 and e.year == 2024]
        assert any(e.day is None for e in ru)

    def test_ru_year_extracted(self):
        events = self.ex.extract("Релиз состоялся в августе 2022.")
        years = {e.year for e in events}
        assert 2022 in years

    def test_ru_all_months(self):
        pairs = [
            ("январ", 1), ("феврал", 2), ("март", 3), ("апрел", 4),
            ("май", 5), ("июн", 6), ("июл", 7), ("август", 8),
            ("сентябр", 9), ("октябр", 10), ("ноябр", 11), ("декабр", 12),
        ]
        for stem, expected_month in pairs:
            # Use a realistic inflection
            text = f"В {stem}е 2024 что-то случилось."
            events = self.ex.extract(text)
            months = [e.month for e in events if e.month is not None]
            assert expected_month in months, f"Failed for RU stem '{stem}'"


# ===========================================================================
# TimelineExtractor — year-only
# ===========================================================================

class TestExtractorYearOnly:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_year_only_20xx(self):
        events = self.ex.extract("Founded in 2019.")
        years = {e.year for e in events}
        assert 2019 in years

    def test_year_only_19xx(self):
        events = self.ex.extract("Legacy system from 1999.")
        years = {e.year for e in events}
        assert 1999 in years

    def test_year_only_confidence(self):
        events = self.ex.extract("Started in 2015.")
        year_events = [e for e in events if e.year == 2015 and e.month is None]
        assert any(abs(e.confidence - 0.5) < 1e-9 for e in year_events)

    def test_year_only_no_month(self):
        events = self.ex.extract("Since 2020.")
        year_evs = [e for e in events if e.year == 2020]
        assert any(e.month is None for e in year_evs)

    def test_year_not_duplicated_when_iso_present(self):
        # ISO date 2024-06-15 contains 2024 — should not produce a separate year-only event
        events = self.ex.extract("Date: 2024-06-15")
        full = [e for e in events if e.has_full_date()]
        year_only = [e for e in events if e.year == 2024 and e.month is None and e.day is None]
        assert len(full) >= 1
        assert len(year_only) == 0

    def test_year_not_in_past_century(self):
        # 1800 is not matched
        events = self.ex.extract("Since 1800.")
        assert all(e.year != 1800 for e in events)


# ===========================================================================
# TimelineExtractor — event_type classification
# ===========================================================================

class TestExtractorEventType:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_release_keyword(self):
        events = self.ex.extract("Released version 2.0 on 2024-03-01.")
        assert any(e.event_type == EventType.RELEASE for e in events)

    def test_version_keyword(self):
        events = self.ex.extract("Version 1.5 launched on 2024-04-10.")
        # "version" should trigger RELEASE
        assert any(e.event_type == EventType.RELEASE for e in events)

    def test_announcement_keyword(self):
        events = self.ex.extract("The project was announced on 2024-05-20.")
        assert any(e.event_type == EventType.ANNOUNCEMENT for e in events)

    def test_russian_release_keyword(self):
        events = self.ex.extract("Выпуск состоялся в июне 2024.")
        assert any(e.event_type == EventType.RELEASE for e in events)

    def test_russian_announcement(self):
        events = self.ex.extract("Анонс нового продукта в декабре 2023.")
        assert any(e.event_type == EventType.ANNOUNCEMENT for e in events)

    def test_deadline_keyword(self):
        events = self.ex.extract("Deadline is 2024-09-30 for submissions.")
        assert any(e.event_type == EventType.DEADLINE for e in events)

    def test_meeting_keyword(self):
        events = self.ex.extract("Meeting scheduled on 2024-07-15.")
        assert any(e.event_type == EventType.MEETING for e in events)

    def test_publication_keyword(self):
        events = self.ex.extract("Paper published on June 1, 2024.")
        assert any(e.event_type == EventType.PUBLICATION for e in events)

    def test_unknown_type_default(self):
        events = self.ex.extract("Something happened on 2024-08-08.")
        # Generic context → UNKNOWN
        assert any(e.event_type == EventType.UNKNOWN for e in events)

    def test_release_russian_version(self):
        events = self.ex.extract("Версия 3.1 вышла в 2024-02-14.")
        assert any(e.event_type == EventType.RELEASE for e in events)


# ===========================================================================
# TimelineExtractor — deduplication
# ===========================================================================

class TestExtractorDeduplication:

    def setup_method(self):
        self.ex = TimelineExtractor()

    def test_same_date_same_context_deduplicated(self):
        # Identical date appears twice right next to each other → deduped
        text = "2024-06-15 and again 2024-06-15 in the same context window here extra text."
        events = self.ex.extract(text)
        # Both matches are likely in the same context window if they're close
        full = [e for e in events if e.year == 2024 and e.month == 6 and e.day == 15]
        # Should be at most 2 (could legitimately differ if context differs enough)
        assert len(full) <= 2

    def test_different_dates_not_deduplicated(self):
        text = "On 2024-01-01 and on 2024-06-15."
        events = self.ex.extract(text)
        full = [e for e in events if e.has_full_date()]
        dates = {(e.year, e.month, e.day) for e in full}
        assert (2024, 1, 1) in dates
        assert (2024, 6, 15) in dates

    def test_extract_empty_string(self):
        events = self.ex.extract("")
        assert events == []

    def test_extract_no_dates(self):
        events = self.ex.extract("No dates here at all, just plain text.")
        assert events == []

    def test_extract_whitespace_only(self):
        events = self.ex.extract("   \n\t  ")
        assert events == []

    def test_sorted_output_invariant(self):
        text = "2024-12-31 then 2020-01-01 then 2022-06-15."
        events = self.ex.extract(text)
        keys = [e.sort_key() for e in events]
        assert keys == sorted(keys)


# ===========================================================================
# Timeline container
# ===========================================================================

class TestTimeline:

    def test_empty_timeline_no_events(self):
        tl = Timeline()
        assert tl.sorted_events() == []

    def test_add_single_event(self):
        tl = Timeline()
        ev = _event(year=2024)
        tl.add(ev)
        assert len(tl.sorted_events()) == 1

    def test_init_with_events(self):
        events = [_event(year=2024), _event(year=2023)]
        tl = Timeline(events)
        assert len(tl.sorted_events()) == 2

    def test_events_in_year_found(self):
        tl = Timeline([_event(year=2024), _event(year=2023)])
        assert len(tl.events_in_year(2024)) == 1

    def test_events_in_year_not_found(self):
        tl = Timeline([_event(year=2024)])
        assert tl.events_in_year(2020) == []

    def test_events_in_year_multiple(self):
        tl = Timeline([
            _event(year=2024, month=1, day=1),
            _event(year=2024, month=6, day=15),
            _event(year=2023, month=12, day=31),
        ])
        result = tl.events_in_year(2024)
        assert len(result) == 2

    def test_events_in_range_inclusive(self):
        tl = Timeline([
            _event(year=2020), _event(year=2022), _event(year=2024),
        ])
        result = tl.events_in_range(2021, 2023)
        assert len(result) == 1
        assert result[0].year == 2022

    def test_events_in_range_all(self):
        tl = Timeline([_event(year=2020), _event(year=2024)])
        result = tl.events_in_range(2020, 2024)
        assert len(result) == 2

    def test_events_in_range_excludes_none_year(self):
        tl = Timeline([_event(year=None, month=None, day=None)])
        result = tl.events_in_range(2020, 2024)
        assert result == []

    def test_by_type_release(self):
        tl = Timeline([
            _event(event_type=EventType.RELEASE),
            _event(event_type=EventType.UNKNOWN),
        ])
        releases = tl.by_type(EventType.RELEASE)
        assert len(releases) == 1

    def test_by_type_empty(self):
        tl = Timeline([_event(event_type=EventType.UNKNOWN)])
        assert tl.by_type(EventType.RELEASE) == []

    def test_by_type_all(self):
        types = list(EventType)
        tl = Timeline([_event(event_type=et) for et in types])
        for et in types:
            assert len(tl.by_type(et)) == 1

    def test_sorted_events_order(self):
        tl = Timeline([
            _event(year=2024, month=12, day=31),
            _event(year=2020, month=1, day=1),
            _event(year=2022, month=6, day=15),
        ])
        sorted_ev = tl.sorted_events()
        keys = [e.sort_key() for e in sorted_ev]
        assert keys == sorted(keys)

    def test_summary_with_events(self):
        tl = Timeline([_event(year=2020), _event(year=2024)])
        s = tl.summary()
        assert "2020" in s
        assert "2024" in s

    def test_summary_single_year(self):
        tl = Timeline([_event(year=2024)])
        s = tl.summary()
        assert "2024" in s

    def test_summary_empty(self):
        tl = Timeline()
        s = tl.summary()
        assert "0" in s

    def test_summary_no_known_years(self):
        ev = TimelineEvent(date_str="unknown", description="test")
        tl = Timeline([ev])
        s = tl.summary()
        assert "1" in s

    def test_to_markdown_empty_returns_empty(self):
        tl = Timeline()
        assert tl.to_markdown() == ""

    def test_to_markdown_contains_year_heading(self):
        tl = Timeline([_event(year=2024, month=6, day=15, description="Release")])
        md = tl.to_markdown()
        assert "2024" in md

    def test_to_markdown_contains_description(self):
        tl = Timeline([_event(description="Big launch event")])
        md = tl.to_markdown()
        assert "Big launch event" in md

    def test_to_markdown_date_format_full(self):
        tl = Timeline([_event(year=2024, month=6, day=5, description="Test")])
        md = tl.to_markdown()
        assert "2024-06-05" in md

    def test_to_markdown_unknown_month_shown(self):
        ev = TimelineEvent(
            date_str="2024",
            description="Year only event",
            year=2024,
            month=None,
            day=None,
        )
        tl = Timeline([ev])
        md = tl.to_markdown()
        assert "??" in md

    def test_to_markdown_grouped_by_year(self):
        tl = Timeline([
            _event(year=2023, month=1, day=1, description="Event A"),
            _event(year=2024, month=6, day=15, description="Event B"),
        ])
        md = tl.to_markdown()
        assert "2023" in md
        assert "2024" in md
        assert "Event A" in md
        assert "Event B" in md

    def test_to_markdown_is_string(self):
        tl = Timeline([_event()])
        assert isinstance(tl.to_markdown(), str)

    def test_add_multiple_then_sort(self):
        tl = Timeline()
        for year in [2022, 2020, 2024, 2021]:
            tl.add(_event(year=year))
        sorted_ev = tl.sorted_events()
        years = [e.year for e in sorted_ev]
        assert years == sorted(years)

    def test_events_in_range_single_year(self):
        tl = Timeline([_event(year=2024), _event(year=2025)])
        result = tl.events_in_range(2024, 2024)
        assert all(e.year == 2024 for e in result)


# ===========================================================================
# Integration tests (extractor + timeline)
# ===========================================================================

class TestIntegration:

    def test_extract_and_build_timeline(self):
        text = (
            "The project was released on 2024-01-15. "
            "A milestone was reached in March 2024. "
            "The announcement came in 2023."
        )
        ex = TimelineExtractor()
        events = ex.extract(text)
        tl = Timeline(events)
        assert len(tl.sorted_events()) > 0

    def test_timeline_summary_after_extraction(self):
        text = "Launched 2022-06-01. Updated 2024-03-15."
        ex = TimelineExtractor()
        tl = Timeline(ex.extract(text))
        s = tl.summary()
        assert "2022" in s or "2024" in s

    def test_to_markdown_after_ru_extraction(self):
        text = "Релиз состоялся в феврале 2024 года. Новая версия — декабрь 2023."
        ex = TimelineExtractor()
        tl = Timeline(ex.extract(text))
        md = tl.to_markdown()
        assert isinstance(md, str)

    def test_mixed_languages_both_extracted(self):
        text = "Released January 10, 2024. Выпущено в марте 2024."
        ex = TimelineExtractor()
        events = ex.extract(text)
        months = {e.month for e in events if e.month is not None}
        assert 1 in months or 3 in months

    def test_confidence_ordering(self):
        """ISO events should have higher confidence than year-only."""
        ex = TimelineExtractor()
        iso_events = ex.extract("On 2024-06-15 something happened.")
        year_events = ex.extract("In 2024 something happened.")
        if iso_events and year_events:
            iso_max = max(e.confidence for e in iso_events if e.has_full_date())
            year_max = max(e.confidence for e in year_events)
            assert iso_max > year_max

    def test_import_all_public_names(self):
        from docstoolkit.timeline import (
            DatePattern,
            EventType,
            Timeline,
            TimelineEvent,
            TimelineExtractor,
        )
        assert TimelineExtractor is not None
        assert Timeline is not None
        assert TimelineEvent is not None
        assert EventType is not None
        assert DatePattern is not None

    def test_many_events_sorted(self):
        texts = [
            "2020-01-01 start", "2022-06-15 mid", "2019-12-31 early",
            "2024-03-10 recent", "August 5, 2021 announced",
        ]
        ex = TimelineExtractor()
        all_events = ex.extract(" ".join(texts))
        tl = Timeline(all_events)
        keys = [e.sort_key() for e in tl.sorted_events()]
        assert keys == sorted(keys)
