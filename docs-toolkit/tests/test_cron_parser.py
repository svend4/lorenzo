"""Tests for docstoolkit.cron_parser."""
from __future__ import annotations

import datetime as dt

import pytest

from docstoolkit.cron_parser import (
    CronExpression,
    CronField,
    CronParser,
    ParseError,
)


@pytest.fixture
def parser() -> CronParser:
    return CronParser()


# ---------------------------------------------------------------------------
# CronField
# ---------------------------------------------------------------------------


class TestCronField:
    def test_minute_bounds(self):
        assert CronField.MINUTE.low == 0
        assert CronField.MINUTE.high == 59

    def test_hour_bounds(self):
        assert CronField.HOUR.low == 0
        assert CronField.HOUR.high == 23

    def test_day_of_month_bounds(self):
        assert CronField.DAY_OF_MONTH.low == 1
        assert CronField.DAY_OF_MONTH.high == 31

    def test_month_bounds(self):
        assert CronField.MONTH.low == 1
        assert CronField.MONTH.high == 12

    def test_day_of_week_bounds(self):
        assert CronField.DAY_OF_WEEK.low == 0
        assert CronField.DAY_OF_WEEK.high == 6

    def test_enum_members(self):
        names = {f.name for f in CronField}
        assert names == {
            "MINUTE",
            "HOUR",
            "DAY_OF_MONTH",
            "MONTH",
            "DAY_OF_WEEK",
        }


# ---------------------------------------------------------------------------
# CronExpression dataclass
# ---------------------------------------------------------------------------


class TestCronExpression:
    def test_round_trip_fields(self, parser: CronParser):
        ce = parser.parse("*/15 9 * * *")
        assert isinstance(ce, CronExpression)
        assert ce.expression == "*/15 9 * * *"
        assert ce.minute == {0, 15, 30, 45}
        assert ce.hour == {9}
        assert ce.day_of_month == set(range(1, 32))
        assert ce.month == set(range(1, 13))
        assert ce.day_of_week == set(range(0, 7))

    def test_dom_restricted_flag(self, parser: CronParser):
        ce = parser.parse("0 0 15 * *")
        assert ce.dom_restricted is True
        assert ce.dow_restricted is False

    def test_dow_restricted_flag(self, parser: CronParser):
        ce = parser.parse("0 0 * * 1")
        assert ce.dom_restricted is False
        assert ce.dow_restricted is True


# ---------------------------------------------------------------------------
# parse_field — star
# ---------------------------------------------------------------------------


class TestParseStar:
    def test_star_minute(self, parser: CronParser):
        assert parser.parse_field("*", 0, 59) == set(range(0, 60))

    def test_star_hour(self, parser: CronParser):
        assert parser.parse_field("*", 0, 23) == set(range(0, 24))

    def test_star_month(self, parser: CronParser):
        assert parser.parse_field("*", 1, 12) == set(range(1, 13))


# ---------------------------------------------------------------------------
# parse_field — single number
# ---------------------------------------------------------------------------


class TestParseNumber:
    def test_zero(self, parser: CronParser):
        assert parser.parse_field("0", 0, 59) == {0}

    def test_high_bound(self, parser: CronParser):
        assert parser.parse_field("59", 0, 59) == {59}

    def test_mid(self, parser: CronParser):
        assert parser.parse_field("30", 0, 59) == {30}


# ---------------------------------------------------------------------------
# parse_field — range
# ---------------------------------------------------------------------------


class TestParseRange:
    def test_simple_range(self, parser: CronParser):
        assert parser.parse_field("1-5", 0, 59) == {1, 2, 3, 4, 5}

    def test_full_range_equivalent_to_star(self, parser: CronParser):
        assert parser.parse_field("0-59", 0, 59) == set(range(0, 60))

    def test_single_value_range(self, parser: CronParser):
        assert parser.parse_field("3-3", 0, 59) == {3}


# ---------------------------------------------------------------------------
# parse_field — list
# ---------------------------------------------------------------------------


class TestParseList:
    def test_three_values(self, parser: CronParser):
        assert parser.parse_field("1,3,5", 0, 59) == {1, 3, 5}

    def test_unordered(self, parser: CronParser):
        assert parser.parse_field("9,2,7", 0, 59) == {2, 7, 9}

    def test_duplicates_collapse(self, parser: CronParser):
        assert parser.parse_field("4,4,4", 0, 59) == {4}

    def test_list_with_range(self, parser: CronParser):
        assert parser.parse_field("1,3-5,9", 0, 59) == {1, 3, 4, 5, 9}


# ---------------------------------------------------------------------------
# parse_field — step
# ---------------------------------------------------------------------------


class TestParseStep:
    def test_every_5_minutes(self, parser: CronParser):
        assert parser.parse_field("*/5", 0, 59) == {
            0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55
        }

    def test_every_15_minutes(self, parser: CronParser):
        assert parser.parse_field("*/15", 0, 59) == {0, 15, 30, 45}

    def test_every_3_hours(self, parser: CronParser):
        assert parser.parse_field("*/3", 0, 23) == {0, 3, 6, 9, 12, 15, 18, 21}

    def test_step_starting_at_number(self, parser: CronParser):
        # "5/10" expands to 5, 15, 25, 35, 45, 55 (numbers >= 5, step 10, ≤ high)
        assert parser.parse_field("5/10", 0, 59) == {5, 15, 25, 35, 45, 55}


# ---------------------------------------------------------------------------
# parse_field — range with step
# ---------------------------------------------------------------------------


class TestParseRangeStep:
    def test_zero_to_30_step_5(self, parser: CronParser):
        assert parser.parse_field("0-30/5", 0, 59) == {0, 5, 10, 15, 20, 25, 30}

    def test_1_to_10_step_3(self, parser: CronParser):
        assert parser.parse_field("1-10/3", 0, 59) == {1, 4, 7, 10}

    def test_combination_complex(self, parser: CronParser):
        # "1,3-5,*/10" → {1,3,4,5,0,10,20,30,40,50}
        out = parser.parse_field("1,3-5,*/10", 0, 59)
        assert out == {0, 1, 3, 4, 5, 10, 20, 30, 40, 50}


# ---------------------------------------------------------------------------
# Invalid inputs
# ---------------------------------------------------------------------------


class TestParseInvalid:
    def test_empty_string(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("")

    def test_too_few_fields(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("* * * *")

    def test_too_many_fields(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("* * * * * *")

    def test_out_of_range_minute(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("60 * * * *")

    def test_out_of_range_hour(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("* 24 * * *")

    def test_out_of_range_dom_low(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("* * 0 * *")

    def test_out_of_range_month_high(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("* * * 13 *")

    def test_negative_number(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("-1", 0, 59)

    def test_bad_range(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("5-3", 0, 59)

    def test_zero_step(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("*/0", 0, 59)

    def test_non_numeric(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("abc", 0, 59)

    def test_unknown_special(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse("@bogus")

    def test_none(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse(None)  # type: ignore[arg-type]

    def test_empty_list_element(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("1,,2", 0, 59)


# ---------------------------------------------------------------------------
# Special expressions
# ---------------------------------------------------------------------------


class TestParseSpecial:
    def test_yearly(self, parser: CronParser):
        ce = parser.parse("@yearly")
        assert ce.minute == {0}
        assert ce.hour == {0}
        assert ce.day_of_month == {1}
        assert ce.month == {1}

    def test_annually_alias(self, parser: CronParser):
        a = parser.parse("@annually")
        b = parser.parse("@yearly")
        assert a.minute == b.minute and a.month == b.month

    def test_monthly(self, parser: CronParser):
        ce = parser.parse("@monthly")
        assert ce.minute == {0} and ce.hour == {0} and ce.day_of_month == {1}
        assert ce.month == set(range(1, 13))

    def test_weekly(self, parser: CronParser):
        ce = parser.parse("@weekly")
        assert ce.day_of_week == {0}
        assert ce.dow_restricted is True

    def test_daily(self, parser: CronParser):
        ce = parser.parse("@daily")
        assert ce.minute == {0} and ce.hour == {0}

    def test_hourly(self, parser: CronParser):
        ce = parser.parse("@hourly")
        assert ce.minute == {0}
        assert ce.hour == set(range(0, 24))

    def test_case_insensitive(self, parser: CronParser):
        ce = parser.parse("@DAILY")
        assert ce.hour == {0}

    def test_midnight_alias(self, parser: CronParser):
        a = parser.parse("@midnight")
        b = parser.parse("@daily")
        assert a.minute == b.minute and a.hour == b.hour


# ---------------------------------------------------------------------------
# is_valid
# ---------------------------------------------------------------------------


class TestIsValid:
    def test_valid_simple(self, parser: CronParser):
        assert parser.is_valid("* * * * *") is True

    def test_valid_complex(self, parser: CronParser):
        assert parser.is_valid("*/5 0-12 1,15 1-6 1-5") is True

    def test_valid_special(self, parser: CronParser):
        assert parser.is_valid("@hourly") is True

    def test_invalid_garbage(self, parser: CronParser):
        assert parser.is_valid("not a cron") is False

    def test_invalid_field(self, parser: CronParser):
        assert parser.is_valid("* * 99 * *") is False

    def test_invalid_empty(self, parser: CronParser):
        assert parser.is_valid("") is False


# ---------------------------------------------------------------------------
# matches
# ---------------------------------------------------------------------------


class TestMatches:
    def test_match_every_minute(self, parser: CronParser):
        assert parser.matches("* * * * *", dt.datetime(2026, 5, 1, 12, 34))

    def test_match_specific_minute(self, parser: CronParser):
        assert parser.matches("30 * * * *", dt.datetime(2026, 5, 1, 12, 30))
        assert not parser.matches("30 * * * *", dt.datetime(2026, 5, 1, 12, 29))

    def test_match_hour_only(self, parser: CronParser):
        assert parser.matches("0 9 * * *", dt.datetime(2026, 5, 1, 9, 0))
        assert not parser.matches("0 9 * * *", dt.datetime(2026, 5, 1, 8, 0))

    def test_match_dom(self, parser: CronParser):
        assert parser.matches("0 0 15 * *", dt.datetime(2026, 5, 15, 0, 0))
        assert not parser.matches("0 0 15 * *", dt.datetime(2026, 5, 16, 0, 0))

    def test_match_month(self, parser: CronParser):
        assert parser.matches("0 0 1 1 *", dt.datetime(2026, 1, 1, 0, 0))
        assert not parser.matches("0 0 1 1 *", dt.datetime(2026, 2, 1, 0, 0))

    def test_match_dow_monday(self, parser: CronParser):
        # 2026-05-04 is a Monday.
        assert dt.date(2026, 5, 4).isoweekday() == 1
        assert parser.matches("0 0 * * 1", dt.datetime(2026, 5, 4, 0, 0))
        assert not parser.matches("0 0 * * 1", dt.datetime(2026, 5, 5, 0, 0))

    def test_match_dow_sunday_zero(self, parser: CronParser):
        # 2026-05-03 is a Sunday.
        assert parser.matches("0 0 * * 0", dt.datetime(2026, 5, 3, 0, 0))

    def test_match_dow_sunday_seven(self, parser: CronParser):
        assert parser.matches("0 0 * * 7", dt.datetime(2026, 5, 3, 0, 0))

    def test_match_dom_or_dow(self, parser: CronParser):
        # When BOTH DOM and DOW restricted, either match triggers.
        # 2026-05-01 is a Friday (DOW=5), DOM=1.
        # "0 0 1 * 0" → DOM=1 matches even though Sunday(0) doesn't.
        assert parser.matches("0 0 1 * 0", dt.datetime(2026, 5, 1, 0, 0))
        # Sunday 2026-05-03: DOW matches, DOM=3 doesn't, still triggers.
        assert parser.matches("0 0 1 * 0", dt.datetime(2026, 5, 3, 0, 0))

    def test_match_wildcards_only(self, parser: CronParser):
        ce = parser.parse("* * * * *")
        for h in (0, 5, 12, 23):
            assert parser.matches("* * * * *", dt.datetime(2026, 5, 1, h, 0))


# ---------------------------------------------------------------------------
# next_fire
# ---------------------------------------------------------------------------


class TestNextFire:
    def test_every_minute(self, parser: CronParser):
        nxt = parser.next_fire("* * * * *", dt.datetime(2026, 5, 1, 12, 0, 0))
        assert nxt == dt.datetime(2026, 5, 1, 12, 1, 0)

    def test_every_5_minutes(self, parser: CronParser):
        nxt = parser.next_fire("*/5 * * * *", dt.datetime(2026, 5, 1, 12, 1, 0))
        assert nxt == dt.datetime(2026, 5, 1, 12, 5, 0)

    def test_daily_at_9(self, parser: CronParser):
        nxt = parser.next_fire("0 9 * * *", dt.datetime(2026, 5, 1, 10, 0, 0))
        assert nxt == dt.datetime(2026, 5, 2, 9, 0, 0)

    def test_strict_inequality(self, parser: CronParser):
        # If from_dt exactly matches, next_fire must be the FOLLOWING fire.
        nxt = parser.next_fire("0 9 * * *", dt.datetime(2026, 5, 1, 9, 0, 0))
        assert nxt == dt.datetime(2026, 5, 2, 9, 0, 0)

    def test_skip_to_next_month(self, parser: CronParser):
        # Last day of February in non-leap year: previous DOM=30 jumps to March 30.
        nxt = parser.next_fire("0 0 30 * *", dt.datetime(2026, 2, 15, 0, 0))
        assert nxt == dt.datetime(2026, 3, 30, 0, 0)

    def test_specific_month(self, parser: CronParser):
        nxt = parser.next_fire("0 0 1 7 *", dt.datetime(2026, 5, 1, 0, 0))
        assert nxt == dt.datetime(2026, 7, 1, 0, 0)

    def test_specific_month_wraps_year(self, parser: CronParser):
        nxt = parser.next_fire("0 0 1 3 *", dt.datetime(2026, 5, 1, 0, 0))
        assert nxt == dt.datetime(2027, 3, 1, 0, 0)

    def test_weekly_monday_9am(self, parser: CronParser):
        # 2026-05-01 is Friday; next Monday is 2026-05-04.
        nxt = parser.next_fire("0 9 * * 1", dt.datetime(2026, 5, 1, 12, 0))
        assert nxt == dt.datetime(2026, 5, 4, 9, 0)


# ---------------------------------------------------------------------------
# previous_fire
# ---------------------------------------------------------------------------


class TestPreviousFire:
    def test_every_minute(self, parser: CronParser):
        prv = parser.previous_fire("* * * * *", dt.datetime(2026, 5, 1, 12, 30, 0))
        assert prv == dt.datetime(2026, 5, 1, 12, 29, 0)

    def test_every_15_minutes(self, parser: CronParser):
        prv = parser.previous_fire("*/15 * * * *", dt.datetime(2026, 5, 1, 12, 20, 0))
        assert prv == dt.datetime(2026, 5, 1, 12, 15, 0)

    def test_daily_at_9_before_morning(self, parser: CronParser):
        prv = parser.previous_fire("0 9 * * *", dt.datetime(2026, 5, 1, 8, 0))
        assert prv == dt.datetime(2026, 4, 30, 9, 0)

    def test_strict_inequality(self, parser: CronParser):
        prv = parser.previous_fire("0 9 * * *", dt.datetime(2026, 5, 1, 9, 0, 0))
        assert prv == dt.datetime(2026, 4, 30, 9, 0)

    def test_specific_month_wraps_year_back(self, parser: CronParser):
        prv = parser.previous_fire("0 0 1 6 *", dt.datetime(2026, 5, 1, 0, 0))
        assert prv == dt.datetime(2025, 6, 1, 0, 0)


# ---------------------------------------------------------------------------
# next_n_fires
# ---------------------------------------------------------------------------


class TestNextNFires:
    def test_zero(self, parser: CronParser):
        assert parser.next_n_fires("* * * * *", dt.datetime(2026, 5, 1, 12, 0), 0) == []

    def test_three_daily(self, parser: CronParser):
        out = parser.next_n_fires("0 0 * * *", dt.datetime(2026, 5, 1, 0, 0), 3)
        assert out == [
            dt.datetime(2026, 5, 2, 0, 0),
            dt.datetime(2026, 5, 3, 0, 0),
            dt.datetime(2026, 5, 4, 0, 0),
        ]

    def test_five_quarter_hours(self, parser: CronParser):
        out = parser.next_n_fires("*/15 * * * *", dt.datetime(2026, 5, 1, 12, 0), 5)
        # First fire strictly after 12:00 is 12:15.
        assert out == [
            dt.datetime(2026, 5, 1, 12, 15),
            dt.datetime(2026, 5, 1, 12, 30),
            dt.datetime(2026, 5, 1, 12, 45),
            dt.datetime(2026, 5, 1, 13, 0),
            dt.datetime(2026, 5, 1, 13, 15),
        ]

    def test_monotonic_increasing(self, parser: CronParser):
        out = parser.next_n_fires("*/7 * * * *", dt.datetime(2026, 5, 1, 0, 0), 20)
        for a, b in zip(out, out[1:]):
            assert a < b

    def test_negative_n_raises(self, parser: CronParser):
        with pytest.raises(ValueError):
            parser.next_n_fires("* * * * *", dt.datetime(2026, 5, 1), -1)


# ---------------------------------------------------------------------------
# describe
# ---------------------------------------------------------------------------


class TestDescribe:
    def test_every_minute(self, parser: CronParser):
        assert parser.describe("* * * * *") == "every minute"

    def test_every_5_minutes(self, parser: CronParser):
        assert parser.describe("*/5 * * * *") == "every 5 minutes"

    def test_every_15_minutes(self, parser: CronParser):
        assert parser.describe("*/15 * * * *") == "every 15 minutes"

    def test_daily_specific_time(self, parser: CronParser):
        assert parser.describe("30 9 * * *") == "every day at 09:30"

    def test_weekly_monday(self, parser: CronParser):
        assert parser.describe("0 9 * * 1") == "every Monday at 09:00"

    def test_special_hourly(self, parser: CronParser):
        assert parser.describe("@hourly") == "every hour on the hour"

    def test_special_daily(self, parser: CronParser):
        assert parser.describe("@daily") == "once a day at midnight"

    def test_fallback_complex(self, parser: CronParser):
        s = parser.describe("0 0 1,15 * *")
        assert "minute=" in s and "day_of_month=" in s


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------


class TestEdgeCases:
    def test_feb_29_skips_non_leap(self, parser: CronParser):
        # Next Feb 29 after 2026-01-01 is 2028-02-29.
        nxt = parser.next_fire("0 0 29 2 *", dt.datetime(2026, 1, 1, 0, 0))
        assert nxt == dt.datetime(2028, 2, 29, 0, 0)

    def test_feb_29_leap_year_match(self, parser: CronParser):
        assert parser.matches("0 0 29 2 *", dt.datetime(2028, 2, 29, 0, 0))

    def test_year_boundary_forward(self, parser: CronParser):
        # Next match after Dec 31 23:59 is Jan 1 00:00 of next year.
        nxt = parser.next_fire("0 0 * * *", dt.datetime(2026, 12, 31, 23, 59))
        assert nxt == dt.datetime(2027, 1, 1, 0, 0)

    def test_year_boundary_backward(self, parser: CronParser):
        prv = parser.previous_fire("0 0 * * *", dt.datetime(2027, 1, 1, 0, 0))
        assert prv == dt.datetime(2026, 12, 31, 0, 0)

    def test_dom_31_skips_short_months(self, parser: CronParser):
        # After April 1 (April has 30 days), the next 31st is May 31.
        nxt = parser.next_fire("0 0 31 * *", dt.datetime(2026, 4, 1, 0, 0))
        assert nxt == dt.datetime(2026, 5, 31, 0, 0)

    def test_month_name_alias(self, parser: CronParser):
        ce = parser.parse("0 0 * jan-mar *")
        assert ce.month == {1, 2, 3}

    def test_dow_name_alias(self, parser: CronParser):
        ce = parser.parse("0 0 * * mon-fri")
        assert ce.day_of_week == {1, 2, 3, 4, 5}

    def test_seven_means_sunday(self, parser: CronParser):
        ce = parser.parse("0 0 * * 7")
        assert ce.day_of_week == {0}

    def test_whitespace_tolerated(self, parser: CronParser):
        ce = parser.parse("   *   *   *   *   *   ")
        assert ce.minute == set(range(0, 60))

    def test_invalid_after_valid_in_list(self, parser: CronParser):
        with pytest.raises(ParseError):
            parser.parse_field("1,xx,3", 0, 59)

    def test_parser_is_idempotent(self, parser: CronParser):
        ce1 = parser.parse("*/5 * * * *")
        ce2 = parser.parse("*/5 * * * *")
        assert ce1.minute == ce2.minute
