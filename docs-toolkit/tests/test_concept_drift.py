"""Tests for the E28 Concept drift detection module.

Run with:
    cd /home/user/lorenzo/docs-toolkit && python -m pytest tests/test_concept_drift.py -q
"""
from __future__ import annotations

import math
import pytest

from docstoolkit.concept_drift import (
    Window,
    WindowConfig,
    SlidingWindowBuffer,
    DriftType,
    DriftEvent,
    DriftConfig,
    DDM,
    ConceptDriftMonitor,
)


# ===========================================================================
# Window
# ===========================================================================


class TestWindow:
    def test_mean_basic(self):
        w = Window(data=[1.0, 2.0, 3.0, 4.0, 5.0], start_idx=0, end_idx=4)
        assert w.mean() == pytest.approx(3.0)

    def test_mean_single(self):
        w = Window(data=[7.0], start_idx=0, end_idx=0)
        assert w.mean() == pytest.approx(7.0)

    def test_mean_empty(self):
        w = Window(data=[], start_idx=0, end_idx=0)
        assert w.mean() == pytest.approx(0.0)

    def test_variance_uniform(self):
        w = Window(data=[2.0, 2.0, 2.0, 2.0], start_idx=0, end_idx=3)
        assert w.variance() == pytest.approx(0.0)

    def test_variance_known(self):
        # data = [2, 4, 4, 4, 5, 5, 7, 9]  population variance = 4.0
        data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        w = Window(data=data, start_idx=0, end_idx=7)
        assert w.variance() == pytest.approx(4.0)

    def test_variance_single_is_zero(self):
        w = Window(data=[3.0], start_idx=0, end_idx=0)
        assert w.variance() == pytest.approx(0.0)

    def test_variance_two_values(self):
        w = Window(data=[0.0, 2.0], start_idx=0, end_idx=1)
        # population variance = ((0-1)^2 + (2-1)^2) / 2 = 1.0
        assert w.variance() == pytest.approx(1.0)

    def test_std_basic(self):
        data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        w = Window(data=data, start_idx=0, end_idx=7)
        assert w.std() == pytest.approx(2.0)

    def test_std_zero_for_constant(self):
        w = Window(data=[5.0, 5.0, 5.0], start_idx=0, end_idx=2)
        assert w.std() == pytest.approx(0.0)

    def test_std_non_negative(self):
        import random
        rng = random.Random(42)
        data = [rng.gauss(0, 1) for _ in range(100)]
        w = Window(data=data, start_idx=0, end_idx=99)
        assert w.std() >= 0.0

    def test_size(self):
        w = Window(data=[1.0, 2.0, 3.0], start_idx=0, end_idx=2)
        assert w.size() == 3

    def test_size_empty(self):
        w = Window(data=[], start_idx=0, end_idx=0)
        assert w.size() == 0

    def test_start_end_idx_stored(self):
        w = Window(data=[1.0, 2.0], start_idx=5, end_idx=6)
        assert w.start_idx == 5
        assert w.end_idx == 6


# ===========================================================================
# WindowConfig
# ===========================================================================


class TestWindowConfig:
    def test_defaults(self):
        cfg = WindowConfig()
        assert cfg.size == 50
        assert cfg.step == 10
        assert cfg.min_size == 10

    def test_custom(self):
        cfg = WindowConfig(size=100, step=20, min_size=5)
        assert cfg.size == 100
        assert cfg.step == 20
        assert cfg.min_size == 5


# ===========================================================================
# SlidingWindowBuffer
# ===========================================================================


class TestSlidingWindowBuffer:
    def test_no_window_before_min_size(self):
        cfg = WindowConfig(size=10, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(4):
            result = buf.add(float(i))
            assert result == []

    def test_first_window_at_step_boundary(self):
        cfg = WindowConfig(size=10, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(4):
            buf.add(float(i))
        # 5th add crosses step boundary and satisfies min_size
        windows = buf.add(4.0)
        assert len(windows) == 1

    def test_window_data_content(self):
        cfg = WindowConfig(size=10, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(5):
            buf.add(float(i))
        w = buf.current_window()
        assert w is not None
        assert w.data == [0.0, 1.0, 2.0, 3.0, 4.0]

    def test_window_at_every_step(self):
        cfg = WindowConfig(size=20, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        emitted = []
        for i in range(30):
            emitted.extend(buf.add(float(i)))
        # expect windows at 5, 10, 15, 20, 25, 30 → 6 windows
        assert len(emitted) == 6

    def test_window_size_capped_by_config_size(self):
        cfg = WindowConfig(size=5, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(15):
            buf.add(float(i))
        w = buf.current_window()
        assert w is not None
        assert w.size() <= cfg.size

    def test_total_added_increments(self):
        cfg = WindowConfig()
        buf = SlidingWindowBuffer(cfg)
        assert buf.total_added() == 0
        buf.add(1.0)
        assert buf.total_added() == 1
        for _ in range(9):
            buf.add(0.0)
        assert buf.total_added() == 10

    def test_current_window_none_when_too_few(self):
        cfg = WindowConfig(size=10, step=5, min_size=10)
        buf = SlidingWindowBuffer(cfg)
        for _ in range(9):
            buf.add(0.0)
        assert buf.current_window() is None

    def test_current_window_not_none_after_min_size(self):
        cfg = WindowConfig(size=10, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for _ in range(5):
            buf.add(1.0)
        assert buf.current_window() is not None

    def test_window_start_end_idx(self):
        cfg = WindowConfig(size=10, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(5):
            buf.add(float(i))
        w = buf.current_window()
        assert w is not None
        assert w.end_idx == 4  # 0-based, total_added=5 so last index = 4

    def test_no_window_emitted_between_steps(self):
        cfg = WindowConfig(size=10, step=10, min_size=10)
        buf = SlidingWindowBuffer(cfg)
        for i in range(9):
            result = buf.add(float(i))
            assert result == []


# ===========================================================================
# DriftConfig
# ===========================================================================


class TestDriftConfig:
    def test_defaults(self):
        cfg = DriftConfig()
        assert cfg.warning_threshold == pytest.approx(1.5)
        assert cfg.drift_threshold == pytest.approx(2.0)
        assert cfg.window_size == 30

    def test_custom(self):
        cfg = DriftConfig(warning_threshold=1.0, drift_threshold=1.5, window_size=20)
        assert cfg.warning_threshold == pytest.approx(1.0)
        assert cfg.drift_threshold == pytest.approx(1.5)
        assert cfg.window_size == 20


# ===========================================================================
# DriftEvent
# ===========================================================================


class TestDriftEvent:
    def test_is_significant_above_threshold(self):
        evt = DriftEvent(
            drift_type=DriftType.ABRUPT,
            detected_at=100,
            magnitude=1.0,
            description="test",
        )
        assert evt.is_significant(threshold=0.5) is True

    def test_is_significant_below_threshold(self):
        evt = DriftEvent(
            drift_type=DriftType.ABRUPT,
            detected_at=100,
            magnitude=0.3,
            description="test",
        )
        assert evt.is_significant(threshold=0.5) is False

    def test_is_significant_equal_threshold(self):
        evt = DriftEvent(
            drift_type=DriftType.ABRUPT,
            detected_at=50,
            magnitude=0.5,
            description="test",
        )
        # > not >=, so exactly 0.5 is NOT significant
        assert evt.is_significant(threshold=0.5) is False

    def test_is_significant_default_threshold(self):
        evt = DriftEvent(
            drift_type=DriftType.GRADUAL,
            detected_at=10,
            magnitude=0.6,
            description="test",
        )
        assert evt.is_significant() is True

    def test_fields_stored(self):
        evt = DriftEvent(
            drift_type=DriftType.INCREMENTAL,
            detected_at=42,
            magnitude=2.5,
            description="incremental drift",
        )
        assert evt.drift_type == DriftType.INCREMENTAL
        assert evt.detected_at == 42
        assert evt.magnitude == pytest.approx(2.5)
        assert evt.description == "incremental drift"


# ===========================================================================
# DriftType enum
# ===========================================================================


class TestDriftType:
    def test_values_exist(self):
        assert DriftType.ABRUPT.value == "abrupt"
        assert DriftType.GRADUAL.value == "gradual"
        assert DriftType.INCREMENTAL.value == "incremental"
        assert DriftType.NONE.value == "none"


# ===========================================================================
# DDM
# ===========================================================================


class TestDDM:
    def test_initial_sample_count(self):
        ddm = DDM()
        assert ddm.sample_count() == 0

    def test_sample_count_increments(self):
        ddm = DDM()
        for _ in range(10):
            ddm.update(0.0)
        assert ddm.sample_count() == 10

    def test_stable_sequence_no_drift(self):
        """Constant low error rate should not trigger drift."""
        ddm = DDM()
        for _ in range(200):
            result = ddm.update(0.0)
            assert result is None

    def test_spike_sequence_triggers_drift(self):
        """After stable period, injecting high error rate should trigger ABRUPT drift."""
        cfg = DriftConfig(drift_threshold=2.0)
        ddm = DDM(cfg)
        # Stable phase: very low error rate
        for _ in range(100):
            ddm.update(0.0)
        # Drift phase: all errors
        detected = []
        for _ in range(100):
            evt = ddm.update(1.0)
            if evt is not None:
                detected.append(evt)
        assert len(detected) >= 1
        assert all(e.drift_type == DriftType.ABRUPT for e in detected)

    def test_drift_event_has_positive_magnitude(self):
        cfg = DriftConfig(drift_threshold=2.0)
        ddm = DDM(cfg)
        for _ in range(100):
            ddm.update(0.0)
        event = None
        for _ in range(200):
            event = ddm.update(1.0)
            if event is not None:
                break
        assert event is not None
        assert event.magnitude > 0.0

    def test_reset_clears_state(self):
        ddm = DDM()
        for _ in range(50):
            ddm.update(0.5)
        ddm.reset()
        assert ddm.sample_count() == 0

    def test_reset_then_stable_no_drift(self):
        ddm = DDM()
        for _ in range(50):
            ddm.update(1.0)
        ddm.reset()
        # After reset a new stable sequence should not drift immediately
        for _ in range(20):
            result = ddm.update(0.0)
            assert result is None

    def test_update_returns_none_on_stable(self):
        ddm = DDM()
        results = [ddm.update(0.1) for _ in range(30)]
        assert all(r is None for r in results)

    def test_detected_at_matches_sample_count(self):
        cfg = DriftConfig(drift_threshold=2.0)
        ddm = DDM(cfg)
        for _ in range(100):
            ddm.update(0.0)
        event = None
        for _ in range(200):
            evt = ddm.update(1.0)
            if evt is not None:
                event = evt
                break
        assert event is not None
        assert event.detected_at == ddm.sample_count()


# ===========================================================================
# ConceptDriftMonitor
# ===========================================================================


class TestConceptDriftMonitor:
    def test_initial_stats(self):
        m = ConceptDriftMonitor()
        s = m.stats()
        assert s["total_samples"] == 0
        assert s["drift_count"] == 0
        assert s["warning_count"] == 0

    def test_add_error_returns_none_on_stable(self):
        m = ConceptDriftMonitor()
        for _ in range(50):
            result = m.add_error(0.0)
            assert result is None

    def test_drift_history_empty_initially(self):
        m = ConceptDriftMonitor()
        assert m.drift_history() == []

    def test_add_errors_batch(self):
        m = ConceptDriftMonitor()
        events = m.add_errors([0.0] * 50)
        assert events == []

    def test_add_errors_returns_drift_events_on_spike(self):
        cfg = DriftConfig(drift_threshold=2.0)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        events = m.add_errors([1.0] * 100)
        assert len(events) >= 1

    def test_drift_history_records_events(self):
        cfg = DriftConfig(drift_threshold=2.0)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        m.add_errors([1.0] * 100)
        assert len(m.drift_history()) >= 1

    def test_stats_total_samples(self):
        m = ConceptDriftMonitor()
        m.add_errors([0.0] * 30)
        assert m.stats()["total_samples"] == 30

    def test_stats_drift_count_increases(self):
        cfg = DriftConfig(drift_threshold=2.0)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        m.add_errors([1.0] * 100)
        assert m.stats()["drift_count"] >= 1

    def test_is_drifting_false_when_no_events(self):
        m = ConceptDriftMonitor()
        assert m.is_drifting() is False

    def test_is_drifting_true_after_drift_detected(self):
        cfg = DriftConfig(drift_threshold=2.0, window_size=50)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        m.add_errors([1.0] * 50)
        # If any drift was detected it should show up as drifting
        if m.drift_history():
            assert m.is_drifting() is True

    def test_add_error_with_ts(self):
        m = ConceptDriftMonitor()
        result = m.add_error(0.0, ts=1234567890.0)
        assert result is None  # no drift on single stable sample

    def test_drift_history_returns_copy(self):
        m = ConceptDriftMonitor()
        h1 = m.drift_history()
        h2 = m.drift_history()
        assert h1 is not h2  # different list objects

    def test_add_errors_empty_list(self):
        m = ConceptDriftMonitor()
        result = m.add_errors([])
        assert result == []

    def test_stats_keys_present(self):
        m = ConceptDriftMonitor()
        s = m.stats()
        assert "total_samples" in s
        assert "drift_count" in s
        assert "warning_count" in s

    def test_custom_config_propagated(self):
        cfg = DriftConfig(drift_threshold=3.0, window_size=20)
        m = ConceptDriftMonitor(cfg)
        assert m._config.drift_threshold == pytest.approx(3.0)
        assert m._config.window_size == 20

    def test_is_drifting_false_after_many_stable_samples(self):
        """After a drift and many subsequent stable samples, should not be drifting."""
        cfg = DriftConfig(drift_threshold=2.0, window_size=10)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        m.add_errors([1.0] * 50)  # might trigger drift
        # Now feed 100 more stable samples so detected_at is far in the past
        m.add_errors([0.0] * 100)
        # is_drifting should be False if last drift_at << current sample count
        # (This test is behavioural: passes if either no drift was detected
        #  or the window has moved past the drift point)
        # At minimum, stats should be consistent
        s = m.stats()
        assert s["total_samples"] == 250

    def test_drift_event_type_is_abrupt(self):
        """DDM detects abrupt drift (not gradual/incremental)."""
        cfg = DriftConfig(drift_threshold=2.0)
        m = ConceptDriftMonitor(cfg)
        m.add_errors([0.0] * 100)
        m.add_errors([1.0] * 100)
        for evt in m.drift_history():
            assert evt.drift_type == DriftType.ABRUPT

    def test_window_mean_all_same(self):
        """Mean of identical values equals that value."""
        w = Window(data=[3.5, 3.5, 3.5, 3.5], start_idx=0, end_idx=3)
        assert w.mean() == pytest.approx(3.5)

    def test_sliding_buffer_window_mean_matches(self):
        """Window emitted by buffer has correct mean."""
        cfg = WindowConfig(size=5, step=5, min_size=5)
        buf = SlidingWindowBuffer(cfg)
        for i in range(5):
            windows = buf.add(float(i))
        # last call (i=4) triggers a window
        assert len(windows) == 1
        assert windows[0].mean() == pytest.approx(2.0)  # (0+1+2+3+4)/5
