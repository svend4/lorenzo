"""Cron expression parser and scheduler.

Supports 5-field cron expressions:

    minute  hour  day-of-month  month  day-of-week

Field syntax:
    *           — every value in the range
    N           — single number
    N-M         — inclusive range
    N,M,K       — list of values
    */K         — every K-th value starting from the field's low bound
    N-M/K       — every K-th value within the range N..M
    combinations of the above separated by commas

Day-of-week uses Sunday=0 .. Saturday=6 (both ``0`` and ``7`` mean Sunday).

Special aliases (case-insensitive):
    @yearly / @annually  -> "0 0 1 1 *"
    @monthly             -> "0 0 1 * *"
    @weekly              -> "0 0 * * 0"
    @daily / @midnight   -> "0 0 * * *"
    @hourly              -> "0 * * * *"

Only the standard library is used.
"""
from __future__ import annotations

import datetime as _dt
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable


# ---------------------------------------------------------------------------
# Exceptions / Enums
# ---------------------------------------------------------------------------


class ParseError(ValueError):
    """Raised when a cron expression cannot be parsed."""


class CronField(Enum):
    """Identifies a cron field. Values are (low, high) inclusive bounds."""

    MINUTE = (0, 59)
    HOUR = (0, 23)
    DAY_OF_MONTH = (1, 31)
    MONTH = (1, 12)
    DAY_OF_WEEK = (0, 6)

    @property
    def low(self) -> int:
        return self.value[0]

    @property
    def high(self) -> int:
        return self.value[1]


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------


@dataclass
class CronExpression:
    """Parsed cron expression with explicit value sets for each field."""

    expression: str
    minute: set[int] = field(default_factory=set)
    hour: set[int] = field(default_factory=set)
    day_of_month: set[int] = field(default_factory=set)
    month: set[int] = field(default_factory=set)
    day_of_week: set[int] = field(default_factory=set)

    # Whether the day-of-month / day-of-week fields were given as "*" (unrestricted).
    dom_restricted: bool = False
    dow_restricted: bool = False


# ---------------------------------------------------------------------------
# Special expressions
# ---------------------------------------------------------------------------


_SPECIAL: dict[str, str] = {
    "@yearly": "0 0 1 1 *",
    "@annually": "0 0 1 1 *",
    "@monthly": "0 0 1 * *",
    "@weekly": "0 0 * * 0",
    "@daily": "0 0 * * *",
    "@midnight": "0 0 * * *",
    "@hourly": "0 * * * *",
}


_MONTH_NAMES = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}

_DOW_NAMES = {
    "sun": 0, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6,
}


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


class CronParser:
    """Stateless parser/scheduler for 5-field cron expressions."""

    FIELD_ORDER = (
        CronField.MINUTE,
        CronField.HOUR,
        CronField.DAY_OF_MONTH,
        CronField.MONTH,
        CronField.DAY_OF_WEEK,
    )

    # ------------------------------------------------------------------ parse

    def parse(self, expression: str) -> CronExpression:
        """Parse a cron expression into a :class:`CronExpression`."""
        if expression is None:
            raise ParseError("expression must not be None")
        if not isinstance(expression, str):
            raise ParseError("expression must be a string")
        raw = expression.strip()
        if not raw:
            raise ParseError("expression must not be empty")

        # Special @ aliases.
        if raw.startswith("@"):
            key = raw.lower()
            if key not in _SPECIAL:
                raise ParseError(f"unknown special expression: {raw!r}")
            return self._parse_fields(raw, _SPECIAL[key])

        return self._parse_fields(raw, raw)

    def _parse_fields(self, original: str, spec: str) -> CronExpression:
        parts = spec.split()
        if len(parts) != 5:
            raise ParseError(
                f"expected 5 space-separated fields, got {len(parts)} in {spec!r}"
            )

        minute_spec, hour_spec, dom_spec, month_spec, dow_spec = parts

        # Resolve month/dow name aliases before generic parsing.
        month_spec_resolved = self._resolve_names(month_spec, _MONTH_NAMES)
        dow_spec_resolved = self._resolve_names(dow_spec, _DOW_NAMES)

        minute = self.parse_field(minute_spec, CronField.MINUTE.low, CronField.MINUTE.high)
        hour = self.parse_field(hour_spec, CronField.HOUR.low, CronField.HOUR.high)
        dom = self.parse_field(dom_spec, CronField.DAY_OF_MONTH.low, CronField.DAY_OF_MONTH.high)
        month = self.parse_field(month_spec_resolved, CronField.MONTH.low, CronField.MONTH.high)
        # Day-of-week tolerates 7 as Sunday.
        dow = self.parse_field(dow_spec_resolved, 0, 7)
        if 7 in dow:
            dow.discard(7)
            dow.add(0)

        return CronExpression(
            expression=original,
            minute=minute,
            hour=hour,
            day_of_month=dom,
            month=month,
            day_of_week=dow,
            dom_restricted=(dom_spec.strip() != "*"),
            dow_restricted=(dow_spec.strip() != "*"),
        )

    @staticmethod
    def _resolve_names(spec: str, mapping: dict[str, int]) -> str:
        """Replace alphabetic name tokens (case-insensitive) with their numeric codes."""
        out_tokens: list[str] = []
        for token in spec.split(","):
            t = token.strip()
            # Look for any name and replace via simple lowercase substitution on alpha segments.
            replaced = ""
            i = 0
            while i < len(t):
                c = t[i]
                if c.isalpha():
                    j = i
                    while j < len(t) and t[j].isalpha():
                        j += 1
                    name = t[i:j].lower()
                    if name in mapping:
                        replaced += str(mapping[name])
                    else:
                        raise ParseError(f"unknown name {t[i:j]!r} in field {spec!r}")
                    i = j
                else:
                    replaced += c
                    i += 1
            out_tokens.append(replaced)
        return ",".join(out_tokens)

    # -------------------------------------------------------------- parse_field

    def parse_field(self, spec: str, low: int, high: int) -> set[int]:
        """Parse a single cron field spec into a sorted set of integer values."""
        if spec is None or spec == "":
            raise ParseError("field must not be empty")
        if low > high:
            raise ParseError(f"invalid bounds: low={low} high={high}")

        result: set[int] = set()
        for piece in spec.split(","):
            piece = piece.strip()
            if not piece:
                raise ParseError(f"empty value in field {spec!r}")
            result |= self._parse_piece(piece, low, high)
        if not result:
            raise ParseError(f"field {spec!r} produced no values")
        return result

    def _parse_piece(self, piece: str, low: int, high: int) -> set[int]:
        # Step?
        step = 1
        body = piece
        if "/" in piece:
            body, step_part = piece.split("/", 1)
            if "/" in step_part:
                raise ParseError(f"multiple '/' in {piece!r}")
            if not step_part:
                raise ParseError(f"missing step in {piece!r}")
            try:
                step = int(step_part)
            except ValueError as e:
                raise ParseError(f"invalid step {step_part!r} in {piece!r}") from e
            if step <= 0:
                raise ParseError(f"step must be positive in {piece!r}")

        # Determine range [a, b].
        if body == "*":
            a, b = low, high
        elif "-" in body:
            lo_s, hi_s = body.split("-", 1)
            if "-" in hi_s:
                raise ParseError(f"multiple '-' in {piece!r}")
            try:
                a = int(lo_s)
                b = int(hi_s)
            except ValueError as e:
                raise ParseError(f"invalid range {body!r} in {piece!r}") from e
            if a > b:
                raise ParseError(f"range start > end in {piece!r}")
        else:
            try:
                a = int(body)
            except ValueError as e:
                raise ParseError(f"invalid number {body!r} in {piece!r}") from e
            # With explicit step, a bare number expands to a..high.
            if step != 1:
                b = high
            else:
                b = a

        if a < low or b > high:
            raise ParseError(
                f"value out of bounds [{low},{high}] in {piece!r}"
            )

        return set(range(a, b + 1, step))

    # ---------------------------------------------------------------- is_valid

    def is_valid(self, expression: str) -> bool:
        """Return True iff *expression* parses without error."""
        try:
            self.parse(expression)
        except ParseError:
            return False
        return True

    # ---------------------------------------------------------------- matches

    def matches(self, expression: str, dt: _dt.datetime) -> bool:
        """Return True iff *dt* (ignoring seconds) fires for *expression*."""
        ce = self._coerce(expression)
        return self._matches(ce, dt)

    @staticmethod
    def _matches(ce: CronExpression, dt: _dt.datetime) -> bool:
        if dt.minute not in ce.minute:
            return False
        if dt.hour not in ce.hour:
            return False
        if dt.month not in ce.month:
            return False
        dow = dt.isoweekday() % 7  # Sunday=0
        # Traditional cron rule: if both DOM and DOW are restricted, OR them.
        # If only one is restricted, only that one needs to match.
        if ce.dom_restricted and ce.dow_restricted:
            if dt.day not in ce.day_of_month and dow not in ce.day_of_week:
                return False
        elif ce.dom_restricted:
            if dt.day not in ce.day_of_month:
                return False
        elif ce.dow_restricted:
            if dow not in ce.day_of_week:
                return False
        # Otherwise: both wildcard → always match.
        return True

    # ------------------------------------------------------------- next_fire

    def next_fire(
        self,
        expression: str,
        from_dt: _dt.datetime,
    ) -> _dt.datetime:
        """Smallest datetime > *from_dt* that matches *expression*.

        Resolution is one minute; seconds/microseconds of the result are zero.
        """
        ce = self._coerce(expression)
        # Start at next whole minute after from_dt.
        cur = from_dt.replace(second=0, microsecond=0) + _dt.timedelta(minutes=1)
        return self._search(ce, cur, forward=True)

    # --------------------------------------------------------- previous_fire

    def previous_fire(
        self,
        expression: str,
        before_dt: _dt.datetime,
    ) -> _dt.datetime:
        """Largest datetime < *before_dt* that matches *expression*."""
        ce = self._coerce(expression)
        cur = before_dt.replace(second=0, microsecond=0)
        # Step strictly before before_dt.
        if before_dt.second == 0 and before_dt.microsecond == 0:
            cur = cur - _dt.timedelta(minutes=1)
        return self._search(ce, cur, forward=False)

    # ----------------------------------------------------------- next_n_fires

    def next_n_fires(
        self,
        expression: str,
        from_dt: _dt.datetime,
        n: int,
    ) -> list[_dt.datetime]:
        """Return the next *n* fire times strictly after *from_dt*."""
        if n < 0:
            raise ValueError("n must be non-negative")
        ce = self._coerce(expression)
        out: list[_dt.datetime] = []
        cursor = from_dt
        for _ in range(n):
            t = self.next_fire(ce.expression, cursor) if False else None  # placeholder
            # Use internal helper to avoid re-parsing.
            cur = cursor.replace(second=0, microsecond=0) + _dt.timedelta(minutes=1)
            t = self._search(ce, cur, forward=True)
            out.append(t)
            cursor = t
        return out

    # ----------------------------------------------------------------- search

    # Hard limit so we never iterate forever on a malformed schedule.
    _MAX_ITER = 366 * 24 * 60 * 8  # ~8 years of minutes

    def _search(
        self,
        ce: CronExpression,
        start: _dt.datetime,
        forward: bool,
    ) -> _dt.datetime:
        step = _dt.timedelta(minutes=1 if forward else -1)
        cur = start
        # Field-skipping optimisation: when a higher field doesn't match, jump.
        for _ in range(self._MAX_ITER):
            # Skip whole months quickly.
            if cur.month not in ce.month:
                cur = self._advance_month(cur, ce.month, forward)
                continue
            # Skip whole days quickly when day doesn't match.
            if not self._day_matches(ce, cur):
                cur = self._advance_day(cur, forward)
                continue
            if cur.hour not in ce.hour:
                cur = self._advance_hour(cur, ce.hour, forward)
                continue
            if cur.minute not in ce.minute:
                cur = cur + step
                continue
            return cur
        raise RuntimeError("cron search exceeded iteration limit")

    @staticmethod
    def _day_matches(ce: CronExpression, dt: _dt.datetime) -> bool:
        dow = dt.isoweekday() % 7
        if ce.dom_restricted and ce.dow_restricted:
            return dt.day in ce.day_of_month or dow in ce.day_of_week
        if ce.dom_restricted:
            return dt.day in ce.day_of_month
        if ce.dow_restricted:
            return dow in ce.day_of_week
        return True

    @staticmethod
    def _advance_month(
        cur: _dt.datetime, months: set[int], forward: bool
    ) -> _dt.datetime:
        if forward:
            # Jump to first day of next month at 00:00.
            year, month = cur.year, cur.month
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1
            return _dt.datetime(year, month, 1, 0, 0)
        # Backwards: jump to last day of previous month at 23:59.
        year, month = cur.year, cur.month
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
        last_day = CronParser._month_length(year, month)
        return _dt.datetime(year, month, last_day, 23, 59)

    @staticmethod
    def _advance_day(cur: _dt.datetime, forward: bool) -> _dt.datetime:
        if forward:
            nxt = cur.replace(hour=0, minute=0) + _dt.timedelta(days=1)
            return nxt
        prv = cur.replace(hour=23, minute=59) - _dt.timedelta(days=1)
        return prv

    @staticmethod
    def _advance_hour(
        cur: _dt.datetime, hours: set[int], forward: bool
    ) -> _dt.datetime:
        if forward:
            nxt_hour = cur.hour + 1
            if nxt_hour > 23:
                return cur.replace(hour=0, minute=0) + _dt.timedelta(days=1)
            return cur.replace(hour=nxt_hour, minute=0)
        prv_hour = cur.hour - 1
        if prv_hour < 0:
            return (cur.replace(hour=0, minute=0) - _dt.timedelta(minutes=1))
        return cur.replace(hour=prv_hour, minute=59)

    @staticmethod
    def _month_length(year: int, month: int) -> int:
        if month == 12:
            nxt = _dt.date(year + 1, 1, 1)
        else:
            nxt = _dt.date(year, month + 1, 1)
        last = nxt - _dt.timedelta(days=1)
        return last.day

    # --------------------------------------------------------------- describe

    def describe(self, expression: str) -> str:
        """Return a human-readable description of *expression*."""
        ce = self._coerce(expression)

        # Detect well-known patterns.
        original = ce.expression.strip()
        lower = original.lower()
        if lower in _SPECIAL:
            mapping = {
                "@yearly": "once a year (Jan 1 at 00:00)",
                "@annually": "once a year (Jan 1 at 00:00)",
                "@monthly": "once a month (day 1 at 00:00)",
                "@weekly": "once a week (Sunday at 00:00)",
                "@daily": "once a day at midnight",
                "@midnight": "once a day at midnight",
                "@hourly": "every hour on the hour",
            }
            return mapping[lower]

        # Pure step pattern on minute, everything else *.
        if (
            self._is_full(ce.hour, CronField.HOUR)
            and not ce.dom_restricted
            and self._is_full(ce.month, CronField.MONTH)
            and not ce.dow_restricted
        ):
            step = self._detect_step(ce.minute, CronField.MINUTE)
            if step == 1:
                return "every minute"
            if step is not None:
                return f"every {step} minutes"
            if len(ce.minute) == 1:
                m = next(iter(ce.minute))
                return f"every hour at minute {m}"

        # Daily fixed time.
        if (
            len(ce.minute) == 1
            and len(ce.hour) == 1
            and not ce.dom_restricted
            and self._is_full(ce.month, CronField.MONTH)
            and not ce.dow_restricted
        ):
            h = next(iter(ce.hour))
            m = next(iter(ce.minute))
            return f"every day at {h:02d}:{m:02d}"

        # Weekly fixed time.
        if (
            len(ce.minute) == 1
            and len(ce.hour) == 1
            and not ce.dom_restricted
            and self._is_full(ce.month, CronField.MONTH)
            and ce.dow_restricted
            and len(ce.day_of_week) == 1
        ):
            h = next(iter(ce.hour))
            m = next(iter(ce.minute))
            day_names = [
                "Sunday", "Monday", "Tuesday", "Wednesday",
                "Thursday", "Friday", "Saturday",
            ]
            d = next(iter(ce.day_of_week))
            return f"every {day_names[d]} at {h:02d}:{m:02d}"

        # Fallback: list fields.
        parts = [
            f"minute={self._fmt_set(ce.minute)}",
            f"hour={self._fmt_set(ce.hour)}",
            f"day_of_month={self._fmt_set(ce.day_of_month) if ce.dom_restricted else '*'}",
            f"month={self._fmt_set(ce.month) if not self._is_full(ce.month, CronField.MONTH) else '*'}",
            f"day_of_week={self._fmt_set(ce.day_of_week) if ce.dow_restricted else '*'}",
        ]
        return "cron(" + ", ".join(parts) + ")"

    # ---------------------------------------------------------------- helpers

    def _coerce(self, expression):
        if isinstance(expression, CronExpression):
            return expression
        return self.parse(expression)

    @staticmethod
    def _is_full(values: set[int], field_: CronField) -> bool:
        return values == set(range(field_.low, field_.high + 1))

    @staticmethod
    def _detect_step(values: set[int], field_: CronField) -> int | None:
        if not values:
            return None
        ordered = sorted(values)
        # Must start at low.
        if ordered[0] != field_.low:
            return None
        if len(ordered) == 1:
            return None
        diffs = {b - a for a, b in zip(ordered, ordered[1:])}
        if len(diffs) != 1:
            return None
        step = diffs.pop()
        # Must cover the whole range with that step.
        expected = set(range(field_.low, field_.high + 1, step))
        if expected != values:
            return None
        return step

    @staticmethod
    def _fmt_set(values: Iterable[int]) -> str:
        return "{" + ",".join(str(v) for v in sorted(values)) + "}"
