"""Tests for ``docstoolkit.doc_pin_timeline`` (E435 — time-bounded pinning)."""

from __future__ import annotations

import threading

import pytest

from docstoolkit.doc_pin_timeline import (
    DocPinTimeline,
    TimedPin,
    TimelineStats,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def tl() -> DocPinTimeline:
    return DocPinTimeline()


# ---------------------------------------------------------------------------
# TimedPin dataclass
# ---------------------------------------------------------------------------


class TestTimedPin:
    def test_required_fields(self):
        p = TimedPin(pin_id="x", doc_id="d1")
        assert p.pin_id == "x"
        assert p.doc_id == "d1"

    def test_default_pinned_by(self):
        p = TimedPin(pin_id="x", doc_id="d")
        assert p.pinned_by == ""

    def test_default_pinned_at(self):
        p = TimedPin(pin_id="x", doc_id="d")
        assert p.pinned_at == 0.0

    def test_default_expires_at_none(self):
        p = TimedPin(pin_id="x", doc_id="d")
        assert p.expires_at is None

    def test_default_priority(self):
        p = TimedPin(pin_id="x", doc_id="d")
        assert p.priority == 0

    def test_default_note(self):
        p = TimedPin(pin_id="x", doc_id="d")
        assert p.note == ""

    def test_custom_fields(self):
        p = TimedPin(
            pin_id="abc",
            doc_id="d2",
            pinned_by="alice",
            pinned_at=100.0,
            expires_at=200.0,
            priority=5,
            note="hello",
        )
        assert p.pinned_by == "alice"
        assert p.pinned_at == 100.0
        assert p.expires_at == 200.0
        assert p.priority == 5
        assert p.note == "hello"


# ---------------------------------------------------------------------------
# TimelineStats dataclass
# ---------------------------------------------------------------------------


class TestTimelineStats:
    def test_construction(self):
        s = TimelineStats(
            total_pins=3,
            expired_count=2,
            unique_docs=4,
            permanent_count=1,
        )
        assert s.total_pins == 3
        assert s.expired_count == 2
        assert s.unique_docs == 4
        assert s.permanent_count == 1


# ---------------------------------------------------------------------------
# pin() — basic
# ---------------------------------------------------------------------------


class TestPin:
    def test_pin_returns_timed_pin(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert isinstance(p, TimedPin)

    def test_pin_id_is_unique(self, tl: DocPinTimeline):
        a = tl.pin("d1")
        b = tl.pin("d1")
        assert a.pin_id != b.pin_id

    def test_pin_id_is_hex(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert isinstance(p.pin_id, str)
        assert len(p.pin_id) == 32  # uuid4 hex
        int(p.pin_id, 16)  # parses as hex

    def test_pin_default_permanent(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert p.expires_at is None

    def test_pin_explicit_expires_at(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=500.0, now=100.0)
        assert p.expires_at == 500.0

    def test_pin_duration_overrides_expires_at(self, tl: DocPinTimeline):
        p = tl.pin(
            "d1",
            expires_at=999.0,
            duration_seconds=10.0,
            now=100.0,
        )
        assert p.expires_at == 110.0

    def test_pin_duration_alone(self, tl: DocPinTimeline):
        p = tl.pin("d1", duration_seconds=30.0, now=50.0)
        assert p.expires_at == 80.0

    def test_pin_records_pinned_at(self, tl: DocPinTimeline):
        p = tl.pin("d1", now=42.0)
        assert p.pinned_at == 42.0

    def test_pin_records_pinned_by(self, tl: DocPinTimeline):
        p = tl.pin("d1", pinned_by="alice")
        assert p.pinned_by == "alice"

    def test_pin_records_priority(self, tl: DocPinTimeline):
        p = tl.pin("d1", priority=7)
        assert p.priority == 7

    def test_pin_records_note(self, tl: DocPinTimeline):
        p = tl.pin("d1", note="important")
        assert p.note == "important"

    def test_pin_stored_in_index(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert tl.get_pin(p.pin_id) is p or tl.get_pin(p.pin_id) == p

    def test_pin_uses_default_now(self, tl: DocPinTimeline):
        # When now is omitted, pinned_at is set to time.time() — just check
        # it's positive.
        p = tl.pin("d1")
        assert p.pinned_at > 0.0


# ---------------------------------------------------------------------------
# unpin()
# ---------------------------------------------------------------------------


class TestUnpin:
    def test_unpin_existing(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert tl.unpin(p.pin_id) is True

    def test_unpin_missing(self, tl: DocPinTimeline):
        assert tl.unpin("nope") is False

    def test_unpin_removes_pin(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        tl.unpin(p.pin_id)
        assert tl.get_pin(p.pin_id) is None

    def test_unpin_removes_doc_index(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        tl.unpin(p.pin_id)
        assert tl.all_doc_ids() == []

    def test_unpin_one_keeps_others(self, tl: DocPinTimeline):
        p1 = tl.pin("d1")
        p2 = tl.pin("d1")
        tl.unpin(p1.pin_id)
        assert tl.get_pin(p2.pin_id) is not None
        assert tl.is_pinned("d1") is True


# ---------------------------------------------------------------------------
# unpin_all_for_doc()
# ---------------------------------------------------------------------------


class TestUnpinAllForDoc:
    def test_unpin_all_returns_count(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d1")
        tl.pin("d1")
        assert tl.unpin_all_for_doc("d1") == 3

    def test_unpin_all_missing_doc(self, tl: DocPinTimeline):
        assert tl.unpin_all_for_doc("nope") == 0

    def test_unpin_all_removes_doc(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d1")
        tl.unpin_all_for_doc("d1")
        assert tl.is_pinned("d1") is False

    def test_unpin_all_other_doc_untouched(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d2")
        tl.unpin_all_for_doc("d1")
        assert tl.is_pinned("d2") is True


# ---------------------------------------------------------------------------
# get_pin()
# ---------------------------------------------------------------------------


class TestGetPin:
    def test_get_existing(self, tl: DocPinTimeline):
        p = tl.pin("d1", note="x")
        got = tl.get_pin(p.pin_id)
        assert got is not None
        assert got.doc_id == "d1"

    def test_get_missing(self, tl: DocPinTimeline):
        assert tl.get_pin("nope") is None


# ---------------------------------------------------------------------------
# is_pinned()
# ---------------------------------------------------------------------------


class TestIsPinned:
    def test_not_pinned_initially(self, tl: DocPinTimeline):
        assert tl.is_pinned("d1") is False

    def test_pinned_after_pin(self, tl: DocPinTimeline):
        tl.pin("d1")
        assert tl.is_pinned("d1") is True

    def test_not_pinned_when_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=100.0, now=50.0)
        assert tl.is_pinned("d1", now=200.0) is False

    def test_pinned_with_one_active_among_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=100.0, now=50.0)         # expires
        tl.pin("d1", expires_at=1000.0, now=50.0)        # still valid
        assert tl.is_pinned("d1", now=200.0) is True

    def test_permanent_always_pinned(self, tl: DocPinTimeline):
        tl.pin("d1")
        assert tl.is_pinned("d1", now=10**12) is True


# ---------------------------------------------------------------------------
# active_pins()
# ---------------------------------------------------------------------------


class TestActivePins:
    def test_empty(self, tl: DocPinTimeline):
        assert tl.active_pins() == []

    def test_all_active(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d2")
        assert len(tl.active_pins()) == 2

    def test_excludes_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d2")
        active = tl.active_pins(now=100.0)
        assert len(active) == 1
        assert active[0].doc_id == "d2"

    def test_sorted_by_priority_desc(self, tl: DocPinTimeline):
        tl.pin("d1", priority=1, now=10.0)
        tl.pin("d2", priority=5, now=10.0)
        tl.pin("d3", priority=3, now=10.0)
        out = tl.active_pins(now=20.0)
        assert [p.doc_id for p in out] == ["d2", "d3", "d1"]

    def test_priority_tie_broken_by_pinned_at(self, tl: DocPinTimeline):
        tl.pin("d1", priority=5, now=20.0)
        tl.pin("d2", priority=5, now=10.0)
        out = tl.active_pins(now=30.0)
        assert [p.doc_id for p in out] == ["d2", "d1"]


# ---------------------------------------------------------------------------
# pins_for_doc()
# ---------------------------------------------------------------------------


class TestPinsForDoc:
    def test_empty_for_unknown(self, tl: DocPinTimeline):
        assert tl.pins_for_doc("nope") == []

    def test_returns_only_for_doc(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d2")
        assert len(tl.pins_for_doc("d1")) == 1

    def test_excludes_expired_by_default(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d1")
        out = tl.pins_for_doc("d1", now=100.0)
        assert len(out) == 1

    def test_include_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d1")
        out = tl.pins_for_doc("d1", now=100.0, include_expired=True)
        assert len(out) == 2

    def test_sorted_priority_first(self, tl: DocPinTimeline):
        tl.pin("d1", priority=1, now=10.0)
        tl.pin("d1", priority=9, now=10.0)
        out = tl.pins_for_doc("d1", now=20.0)
        assert out[0].priority == 9


# ---------------------------------------------------------------------------
# expired_pins()
# ---------------------------------------------------------------------------


class TestExpiredPins:
    def test_empty(self, tl: DocPinTimeline):
        assert tl.expired_pins() == []

    def test_returns_only_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d2")
        out = tl.expired_pins(now=100.0)
        assert len(out) == 1
        assert out[0].doc_id == "d1"

    def test_sorted_ascending_expires_at(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=30.0, now=1.0)
        tl.pin("d2", expires_at=10.0, now=1.0)
        tl.pin("d3", expires_at=20.0, now=1.0)
        out = tl.expired_pins(now=100.0)
        assert [p.doc_id for p in out] == ["d2", "d3", "d1"]

    def test_permanent_never_expired(self, tl: DocPinTimeline):
        tl.pin("d1")
        assert tl.expired_pins(now=10**12) == []


# ---------------------------------------------------------------------------
# expiring_soon()
# ---------------------------------------------------------------------------


class TestExpiringSoon:
    def test_empty(self, tl: DocPinTimeline):
        assert tl.expiring_soon(60.0) == []

    def test_includes_pins_within_window(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=110.0, now=100.0)
        out = tl.expiring_soon(within_seconds=20.0, now=100.0)
        assert len(out) == 1

    def test_excludes_pins_outside_window(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=1000.0, now=100.0)
        out = tl.expiring_soon(within_seconds=20.0, now=100.0)
        assert out == []

    def test_excludes_already_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=50.0, now=10.0)
        out = tl.expiring_soon(within_seconds=100.0, now=100.0)
        assert out == []

    def test_excludes_permanent(self, tl: DocPinTimeline):
        tl.pin("d1")
        out = tl.expiring_soon(within_seconds=100.0, now=100.0)
        assert out == []

    def test_sorted_asc(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=115.0, now=100.0)
        tl.pin("d2", expires_at=105.0, now=100.0)
        tl.pin("d3", expires_at=110.0, now=100.0)
        out = tl.expiring_soon(within_seconds=30.0, now=100.0)
        assert [p.doc_id for p in out] == ["d2", "d3", "d1"]


# ---------------------------------------------------------------------------
# extend()
# ---------------------------------------------------------------------------


class TestExtend:
    def test_extend_missing(self, tl: DocPinTimeline):
        assert tl.extend("nope", 60.0) is False

    def test_extend_timed_pin(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=200.0, now=100.0)
        tl.extend(p.pin_id, additional_seconds=50.0, now=150.0)
        assert tl.get_pin(p.pin_id).expires_at == 250.0

    def test_extend_permanent_sets_expires_at(self, tl: DocPinTimeline):
        p = tl.pin("d1", now=100.0)
        assert tl.get_pin(p.pin_id).expires_at is None
        tl.extend(p.pin_id, additional_seconds=30.0, now=200.0)
        assert tl.get_pin(p.pin_id).expires_at == 230.0

    def test_extend_returns_true(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=200.0, now=100.0)
        assert tl.extend(p.pin_id, 10.0, now=150.0) is True


# ---------------------------------------------------------------------------
# make_permanent()
# ---------------------------------------------------------------------------


class TestMakePermanent:
    def test_missing(self, tl: DocPinTimeline):
        assert tl.make_permanent("nope") is False

    def test_makes_permanent(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=200.0, now=100.0)
        tl.make_permanent(p.pin_id)
        assert tl.get_pin(p.pin_id).expires_at is None

    def test_returns_true(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=200.0, now=100.0)
        assert tl.make_permanent(p.pin_id) is True

    def test_already_permanent_still_true(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        assert tl.make_permanent(p.pin_id) is True


# ---------------------------------------------------------------------------
# purge_expired()
# ---------------------------------------------------------------------------


class TestPurgeExpired:
    def test_purge_empty(self, tl: DocPinTimeline):
        assert tl.purge_expired() == 0

    def test_purge_count(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d2", expires_at=20.0, now=1.0)
        tl.pin("d3")
        assert tl.purge_expired(now=100.0) == 2

    def test_purge_removes_pins(self, tl: DocPinTimeline):
        p = tl.pin("d1", expires_at=10.0, now=1.0)
        tl.purge_expired(now=100.0)
        assert tl.get_pin(p.pin_id) is None

    def test_purge_keeps_active(self, tl: DocPinTimeline):
        p = tl.pin("d1")
        tl.pin("d2", expires_at=10.0, now=1.0)
        tl.purge_expired(now=100.0)
        assert tl.get_pin(p.pin_id) is not None

    def test_purge_cleans_by_doc_index(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.purge_expired(now=100.0)
        assert tl.all_doc_ids() == []


# ---------------------------------------------------------------------------
# clear_all()
# ---------------------------------------------------------------------------


class TestClearAll:
    def test_clear_empty(self, tl: DocPinTimeline):
        assert tl.clear_all() == 0

    def test_clear_returns_count(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d2")
        tl.pin("d3")
        assert tl.clear_all() == 3

    def test_clear_removes_all(self, tl: DocPinTimeline):
        tl.pin("d1")
        tl.pin("d2")
        tl.clear_all()
        assert tl.active_pins() == []
        assert tl.all_doc_ids() == []


# ---------------------------------------------------------------------------
# all_doc_ids()
# ---------------------------------------------------------------------------


class TestAllDocIds:
    def test_empty(self, tl: DocPinTimeline):
        assert tl.all_doc_ids() == []

    def test_unique_sorted(self, tl: DocPinTimeline):
        tl.pin("zzz")
        tl.pin("aaa")
        tl.pin("aaa")
        tl.pin("mmm")
        assert tl.all_doc_ids() == ["aaa", "mmm", "zzz"]

    def test_excludes_docs_only_expired(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d2")
        assert tl.all_doc_ids(now=100.0) == ["d2"]


# ---------------------------------------------------------------------------
# stats()
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty(self, tl: DocPinTimeline):
        s = tl.stats()
        assert s.total_pins == 0
        assert s.expired_count == 0
        assert s.unique_docs == 0
        assert s.permanent_count == 0

    def test_counts(self, tl: DocPinTimeline):
        tl.pin("d1")                                         # permanent
        tl.pin("d2", expires_at=100.0, now=50.0)             # active
        tl.pin("d2", expires_at=10.0, now=1.0)               # expired
        s = tl.stats(now=80.0)
        # active pins on d1 (perm) + d2(100) = 2; expired = 1
        assert s.total_pins == 2
        assert s.expired_count == 1
        assert s.unique_docs == 2          # d1 and d2 have active pins
        assert s.permanent_count == 1

    def test_unique_docs_active_only(self, tl: DocPinTimeline):
        tl.pin("d1", expires_at=10.0, now=1.0)
        tl.pin("d2")
        s = tl.stats(now=100.0)
        assert s.unique_docs == 1


# ---------------------------------------------------------------------------
# Thread-safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_pin(self):
        tl = DocPinTimeline()
        N = 200

        def worker(i: int):
            tl.pin(f"d{i}")

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert tl.stats().total_pins == N
        assert len(tl.all_doc_ids()) == N

    def test_concurrent_pin_same_doc(self):
        tl = DocPinTimeline()
        N = 100

        def worker():
            tl.pin("shared")

        threads = [threading.Thread(target=worker) for _ in range(N)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert tl.stats().total_pins == N
        assert tl.all_doc_ids() == ["shared"]

    def test_concurrent_unpin(self):
        tl = DocPinTimeline()
        pins = [tl.pin(f"d{i}") for i in range(100)]

        def worker(pin_id: str):
            tl.unpin(pin_id)

        threads = [threading.Thread(target=worker, args=(p.pin_id,)) for p in pins]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert tl.stats().total_pins == 0

    def test_concurrent_mixed_ops(self):
        tl = DocPinTimeline()

        def writer():
            for i in range(50):
                tl.pin(f"d{i}")

        def reader():
            for _ in range(50):
                tl.active_pins()
                tl.all_doc_ids()
                tl.stats()

        threads = [
            threading.Thread(target=writer),
            threading.Thread(target=writer),
            threading.Thread(target=reader),
            threading.Thread(target=reader),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        # two writer threads each add 50 pins
        assert tl.stats().total_pins == 100
