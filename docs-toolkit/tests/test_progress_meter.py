"""Tests for docstoolkit.progress_meter."""

import pytest

from docstoolkit.progress_meter import Phase, ProgressMeter, ProgressSnapshot


class TestPhase:
    def test_progress_zero_total(self):
        p = Phase(name="x", total=0)
        assert p.progress == 0.0

    def test_progress_half(self):
        p = Phase(name="x", total=100, done=50)
        assert p.progress == 0.5

    def test_progress_full(self):
        p = Phase(name="x", total=10, done=10)
        assert p.progress == 1.0

    def test_progress_clamped_above_one(self):
        p = Phase(name="x", total=10, done=25)
        assert p.progress == 1.0

    def test_progress_clamped_below_zero(self):
        p = Phase(name="x", total=10, done=-5)
        assert p.progress == 0.0

    def test_is_complete_false_by_default(self):
        p = Phase(name="x", total=10)
        assert p.is_complete is False

    def test_is_complete_true_when_ended(self):
        p = Phase(name="x", total=10, ended_at=5.0)
        assert p.is_complete is True

    def test_duration_zero_when_not_ended(self):
        p = Phase(name="x", started_at=1.0)
        assert p.duration == 0.0

    def test_duration_computed(self):
        p = Phase(name="x", started_at=1.0, ended_at=4.5)
        assert p.duration == pytest.approx(3.5)

    def test_duration_zero_when_only_ended(self):
        p = Phase(name="x", ended_at=4.0)
        assert p.duration == 0.0


class TestProgressSnapshot:
    def test_snapshot_fields(self):
        snap = ProgressSnapshot(
            overall_progress=0.5,
            current_phase="x",
            phases=[],
            eta_seconds=10.0,
            elapsed_seconds=10.0,
            rate_per_second=1.0,
        )
        assert snap.overall_progress == 0.5
        assert snap.current_phase == "x"
        assert snap.eta_seconds == 10.0
        assert snap.elapsed_seconds == 10.0
        assert snap.rate_per_second == 1.0
        assert snap.phases == []


class TestAddPhase:
    def test_add_single_phase(self):
        m = ProgressMeter()
        p = m.add_phase("a", total=10)
        assert p.name == "a"
        assert p.total == 10
        assert p.weight == 1.0

    def test_add_phase_custom_weight(self):
        m = ProgressMeter()
        p = m.add_phase("a", total=10, weight=2.5)
        assert p.weight == 2.5

    def test_add_phase_count(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=5)
        assert m.phase_count == 2

    def test_add_phase_duplicate_returns_existing(self):
        m = ProgressMeter()
        first = m.add_phase("a", total=10)
        second = m.add_phase("a", total=99)
        assert first is second
        assert m.phase_count == 1


class TestStartPhase:
    def test_start_existing(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.start_phase("a", now=1.0)
        assert p is not None
        assert p.started_at == 1.0

    def test_start_unknown_returns_none(self):
        m = ProgressMeter()
        assert m.start_phase("missing", now=1.0) is None

    def test_start_sets_current(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        cur = m.current_phase()
        assert cur is not None
        assert cur.name == "a"


class TestUpdate:
    def test_update_sets_done(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.update("a", done=4, now=1.0)
        assert p is not None
        assert p.done == 4

    def test_update_unknown(self):
        m = ProgressMeter()
        assert m.update("missing", done=4) is None

    def test_update_clamps_above_total(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.update("a", done=999, now=1.0)
        assert p.done == 10

    def test_update_clamps_below_zero(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.update("a", done=-5, now=1.0)
        assert p.done == 0

    def test_update_sets_started_at_if_missing(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.update("a", done=1, now=2.0)
        assert p.started_at == 2.0


class TestIncrement:
    def test_increment_by_default_one(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=2, now=1.0)
        p = m.increment("a", now=2.0)
        assert p.done == 3

    def test_increment_custom_delta(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.increment("a", delta=5, now=1.0)
        assert p.done == 5

    def test_increment_unknown(self):
        m = ProgressMeter()
        assert m.increment("missing", delta=1) is None

    def test_increment_clamps_to_total(self):
        m = ProgressMeter()
        m.add_phase("a", total=3)
        m.increment("a", delta=2, now=1.0)
        p = m.increment("a", delta=10, now=2.0)
        assert p.done == 3


class TestCompletePhase:
    def test_complete_sets_done_and_ended(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        p = m.complete_phase("a", now=5.0)
        assert p.done == 10
        assert p.ended_at == 5.0
        assert p.is_complete is True

    def test_complete_unknown(self):
        m = ProgressMeter()
        assert m.complete_phase("missing", now=1.0) is None

    def test_complete_sets_started_if_missing(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        p = m.complete_phase("a", now=5.0)
        assert p.started_at == 5.0


class TestCurrentPhase:
    def test_no_current_phase(self):
        m = ProgressMeter()
        assert m.current_phase() is None

    def test_current_after_start(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        assert m.current_phase().name == "a"

    def test_current_switches_on_update(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=10)
        m.start_phase("a", now=1.0)
        m.update("b", done=1, now=2.0)
        assert m.current_phase().name == "b"


class TestSnapshot:
    def test_snapshot_empty(self):
        m = ProgressMeter()
        snap = m.snapshot(now=1.0)
        assert snap.overall_progress == 0.0
        assert snap.current_phase is None

    def test_snapshot_overall_single_phase(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=5, now=1.0)
        snap = m.snapshot(now=2.0)
        assert snap.overall_progress == pytest.approx(0.5)

    def test_snapshot_weighted_overall(self):
        m = ProgressMeter()
        m.add_phase("a", total=10, weight=1.0)
        m.add_phase("b", total=10, weight=3.0)
        m.update("a", done=10, now=1.0)
        m.update("b", done=0, now=1.0)
        snap = m.snapshot(now=2.0)
        # weighted: (1.0*1 + 0*3) / 4 = 0.25
        assert snap.overall_progress == pytest.approx(0.25)

    def test_snapshot_elapsed(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        m.update("a", done=5, now=6.0)
        snap = m.snapshot(now=6.0)
        assert snap.elapsed_seconds == pytest.approx(5.0)

    def test_snapshot_rate(self):
        m = ProgressMeter()
        m.add_phase("a", total=100)
        m.start_phase("a", now=1.0)
        m.update("a", done=50, now=6.0)
        snap = m.snapshot(now=6.0)
        # 50 units / 5 seconds = 10/s
        assert snap.rate_per_second == pytest.approx(10.0)


class TestSnapshotEta:
    def test_eta_zero_when_complete(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        m.complete_phase("a", now=5.0)
        snap = m.snapshot(now=5.0)
        assert snap.eta_seconds == 0.0

    def test_eta_zero_when_no_progress(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        snap = m.snapshot(now=5.0)
        assert snap.eta_seconds == 0.0

    def test_eta_decreases_as_progress_increases(self):
        m = ProgressMeter()
        m.add_phase("a", total=100)
        m.start_phase("a", now=1.0)
        m.update("a", done=10, now=11.0)
        snap_a = m.snapshot(now=11.0)
        m.update("a", done=50, now=51.0)
        snap_b = m.snapshot(now=51.0)
        # As we get closer to completion, ETA should decrease
        assert snap_b.eta_seconds < snap_a.eta_seconds

    def test_eta_positive_during_progress(self):
        m = ProgressMeter()
        m.add_phase("a", total=100)
        m.start_phase("a", now=1.0)
        m.update("a", done=25, now=11.0)
        snap = m.snapshot(now=11.0)
        assert snap.eta_seconds > 0


class TestFormat:
    def test_format_contains_bar_chars(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=5, now=1.0)
        out = m.format(now=2.0)
        assert "█" in out
        assert "░" in out

    def test_format_contains_percentage(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=4, now=1.0)
        out = m.format(now=2.0)
        assert "40%" in out

    def test_format_contains_phase_name(self):
        m = ProgressMeter()
        m.add_phase("Indexing", total=10)
        m.update("Indexing", done=3, now=1.0)
        out = m.format(now=2.0)
        assert "Indexing" in out

    def test_format_contains_eta_label(self):
        m = ProgressMeter()
        m.add_phase("a", total=100)
        m.start_phase("a", now=0.0)
        m.update("a", done=25, now=10.0)
        out = m.format(now=10.0)
        assert "ETA" in out

    def test_format_bar_width_ten(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=5, now=1.0)
        out = m.format(now=2.0)
        # Count bar chars between [ and ]
        bar = out[out.index("[") + 1 : out.index("]")]
        assert len(bar) == 10

    def test_format_full_bar_at_100(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        m.complete_phase("a", now=2.0)
        out = m.format(now=2.0)
        assert "100%" in out
        assert "█" * 10 in out

    def test_format_done_total_in_output(self):
        m = ProgressMeter()
        m.add_phase("X", total=500)
        m.update("X", done=200, now=1.0)
        out = m.format(now=2.0)
        assert "200/500" in out


class TestIsComplete:
    def test_not_complete_when_empty(self):
        m = ProgressMeter()
        assert m.is_complete() is False

    def test_not_complete_with_pending(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.update("a", done=5, now=1.0)
        assert m.is_complete() is False

    def test_complete_after_all_phases_done(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=5)
        m.complete_phase("a", now=1.0)
        m.complete_phase("b", now=2.0)
        assert m.is_complete() is True


class TestReset:
    def test_reset_clears_phases(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=5)
        m.reset()
        assert m.phase_count == 0
        assert m.current_phase() is None

    def test_can_add_after_reset(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.reset()
        m.add_phase("a", total=20)
        assert m.phase_count == 1


class TestPhaseCount:
    def test_zero(self):
        assert ProgressMeter().phase_count == 0

    def test_grows(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        assert m.phase_count == 1
        m.add_phase("b", total=10)
        assert m.phase_count == 2


class TestSubscribe:
    def test_subscribe_returns_id(self):
        m = ProgressMeter()
        sub_id = m.subscribe(lambda s: None)
        assert isinstance(sub_id, int)

    def test_subscriber_fires_on_update(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        events = []
        m.subscribe(lambda s: events.append(s))
        m.update("a", done=3, now=1.0)
        assert len(events) == 1
        assert isinstance(events[0], ProgressSnapshot)

    def test_subscriber_fires_on_increment(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        events = []
        m.subscribe(lambda s: events.append(s))
        m.increment("a", delta=1, now=1.0)
        assert len(events) == 1

    def test_subscriber_fires_on_complete(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        events = []
        m.subscribe(lambda s: events.append(s))
        m.complete_phase("a", now=1.0)
        assert len(events) == 1

    def test_subscriber_exception_does_not_break(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)

        def bad(snap):
            raise RuntimeError("boom")

        m.subscribe(bad)
        # Should not raise
        m.update("a", done=1, now=1.0)


class TestUnsubscribe:
    def test_unsubscribe_known(self):
        m = ProgressMeter()
        sub_id = m.subscribe(lambda s: None)
        assert m.unsubscribe(sub_id) is True

    def test_unsubscribe_unknown(self):
        m = ProgressMeter()
        assert m.unsubscribe(999) is False

    def test_callback_not_fired_after_unsubscribe(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        events = []
        sid = m.subscribe(lambda s: events.append(s))
        m.unsubscribe(sid)
        m.update("a", done=1, now=1.0)
        assert events == []


class TestMultiplePhases:
    def test_overall_progress_equal_weights(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=10)
        m.update("a", done=10, now=1.0)
        m.update("b", done=0, now=1.0)
        snap = m.snapshot(now=2.0)
        assert snap.overall_progress == pytest.approx(0.5)

    def test_overall_progress_complete(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=10)
        m.complete_phase("a", now=1.0)
        m.complete_phase("b", now=2.0)
        snap = m.snapshot(now=3.0)
        assert snap.overall_progress == pytest.approx(1.0)

    def test_phases_order_preserved(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.add_phase("b", total=10)
        m.add_phase("c", total=10)
        snap = m.snapshot(now=1.0)
        names = [p.name for p in snap.phases]
        assert names == ["a", "b", "c"]


class TestEdgeCases:
    def test_zero_phases_snapshot(self):
        m = ProgressMeter()
        snap = m.snapshot(now=5.0)
        assert snap.overall_progress == 0.0
        assert snap.phases == []
        assert snap.current_phase is None
        assert snap.eta_seconds == 0.0

    def test_zero_total_phase_treated_as_zero_progress(self):
        m = ProgressMeter()
        m.add_phase("a", total=0)
        snap = m.snapshot(now=1.0)
        assert snap.overall_progress == 0.0

    def test_no_work_done(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.start_phase("a", now=1.0)
        snap = m.snapshot(now=5.0)
        assert snap.overall_progress == 0.0
        assert snap.rate_per_second == 0.0

    def test_format_without_phases(self):
        m = ProgressMeter()
        out = m.format(now=1.0)
        # Should produce some bar even with no phases
        assert "[" in out and "]" in out
        assert "0%" in out

    def test_phase_count_after_reset(self):
        m = ProgressMeter()
        m.add_phase("a", total=10)
        m.reset()
        assert m.phase_count == 0

    def test_subscribers_persist_across_reset(self):
        # Reset clears phase state but subscribers remain registered
        m = ProgressMeter()
        events = []
        m.subscribe(lambda s: events.append(s))
        m.add_phase("a", total=10)
        m.reset()
        m.add_phase("a", total=5)
        m.update("a", done=1, now=1.0)
        assert len(events) == 1
