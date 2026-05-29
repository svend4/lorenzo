"""Tests for docstoolkit.online_eval.drift — PSI drift detection."""
from __future__ import annotations

import math

import pytest

from docstoolkit.online_eval import psi, psi_label, chi_square_drift, DriftWindow
from docstoolkit.online_eval.drift import _bin_counts


# ---------------------------------------------------------------------------
# _bin_counts helper
# ---------------------------------------------------------------------------

class TestBinCounts:
    def test_empty_returns_zeros(self):
        counts = _bin_counts([], bins=5)
        assert counts == [0, 0, 0, 0, 0]

    def test_all_zeros_go_to_first_bin(self):
        counts = _bin_counts([0.0, 0.0, 0.0], bins=5)
        assert counts[0] == 3

    def test_all_ones_go_to_last_bin(self):
        counts = _bin_counts([1.0, 1.0], bins=5)
        assert counts[-1] == 2

    def test_values_spread_across_bins(self):
        scores = [0.05, 0.15, 0.25, 0.35, 0.45,
                  0.55, 0.65, 0.75, 0.85, 0.95]
        counts = _bin_counts(scores, bins=10)
        assert sum(counts) == 10
        assert all(c == 1 for c in counts)

    def test_len_matches_bins(self):
        counts = _bin_counts([0.1, 0.5, 0.9], bins=7)
        assert len(counts) == 7


# ---------------------------------------------------------------------------
# psi()
# ---------------------------------------------------------------------------

class TestPSI:
    def test_identical_distributions_near_zero(self):
        scores = [i / 100 for i in range(101)]
        val = psi(scores, scores)
        assert val < 0.01

    def test_completely_different_distributions_high_psi(self):
        low_scores = [0.05] * 100   # all near 0
        high_scores = [0.95] * 100  # all near 1
        val = psi(low_scores, high_scores)
        assert val > 0.25

    def test_empty_baseline_returns_zero(self):
        assert psi([], [0.5, 0.6]) == 0.0

    def test_empty_current_returns_zero(self):
        assert psi([0.5, 0.6], []) == 0.0

    def test_returns_float(self):
        val = psi([0.2, 0.3, 0.4], [0.2, 0.3, 0.4])
        assert isinstance(val, float)

    def test_non_negative(self):
        import random
        rng = random.Random(1)
        base = [rng.random() for _ in range(200)]
        curr = [rng.random() for _ in range(200)]
        assert psi(base, curr) >= 0.0

    def test_20pct_shift_above_zero_one(self):
        """Artificial 20% shift in score distribution should raise PSI."""
        base = [0.3 + 0.1 * (i % 5) for i in range(100)]
        shifted = [min(1.0, s + 0.20) for s in base]
        val = psi(base, shifted)
        assert val > 0.01


# ---------------------------------------------------------------------------
# psi_label()
# ---------------------------------------------------------------------------

class TestPSILabel:
    def test_stable(self):
        assert psi_label(0.05) == "stable"

    def test_stable_boundary(self):
        assert psi_label(0.09) == "stable"

    def test_moderate_shift(self):
        assert psi_label(0.15) == "moderate_shift"

    def test_moderate_upper_boundary(self):
        assert psi_label(0.24) == "moderate_shift"

    def test_significant_drift(self):
        assert psi_label(0.26) == "significant_drift"

    def test_exactly_0_25(self):
        assert psi_label(0.25) == "significant_drift"


# ---------------------------------------------------------------------------
# chi_square_drift()
# ---------------------------------------------------------------------------

class TestChiSquareDrift:
    def test_returns_tuple(self):
        result = chi_square_drift([0.1, 0.5], [0.1, 0.5])
        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_dof_is_bins_minus_1(self):
        _, dof = chi_square_drift([0.5] * 10, [0.5] * 10, bins=10)
        assert dof == 9

    def test_identical_distributions_low_chi2(self):
        scores = [i / 50 for i in range(50)] * 2
        chi2, _ = chi_square_drift(scores, scores)
        assert chi2 < 5.0  # not significant

    def test_empty_inputs_return_zero(self):
        chi2, dof = chi_square_drift([], [])
        assert chi2 == 0.0

    def test_shifted_distribution_higher_chi2(self):
        base = [0.2] * 100
        shifted = [0.8] * 100
        chi2_base, _ = chi_square_drift(base, base)
        chi2_shift, _ = chi_square_drift(base, shifted)
        assert chi2_shift > chi2_base


# ---------------------------------------------------------------------------
# DriftWindow
# ---------------------------------------------------------------------------

class TestDriftWindow:
    def _make_window(self, baseline, **kw):
        w = DriftWindow(**kw)
        w.set_baseline(baseline)
        return w

    def test_status_before_any_scores(self):
        w = DriftWindow()
        w.set_baseline([0.5, 0.6, 0.7])
        status = w.status()
        assert status["psi"] == 0.0
        assert status["window_n"] == 0

    def test_no_alert_for_stable_distribution(self):
        base = [0.3 + 0.01 * i for i in range(100)]
        w = self._make_window(base, psi_threshold=0.25)
        # Add many scores so the window is representative before checking alerts
        alerts_after_warmup = []
        for score in base:
            w.add(score)  # build up window without checking
        # Now add a few more scores from same distribution
        for score in [0.35, 0.40, 0.45, 0.50, 0.38]:
            alert = w.add(score)
            if alert is not None:
                alerts_after_warmup.append(alert)
        # With a full window from the same distribution there should be no alerts
        assert len(alerts_after_warmup) == 0

    def test_alert_fired_for_large_drift(self):
        base = [0.05] * 200
        w = self._make_window(base, psi_threshold=0.10, window_size=100)
        alerts = []
        for score in [0.95] * 100:
            a = w.add(score)
            if a:
                alerts.append(a)
        assert len(alerts) > 0

    def test_current_psi_increases_with_drift(self):
        base = [0.3] * 100
        w = self._make_window(base)
        for score in [0.3] * 50:
            w.add(score)
        psi_stable = w.current_psi()

        w2 = self._make_window(base)
        for score in [0.9] * 50:
            w2.add(score)
        psi_drifted = w2.current_psi()

        assert psi_drifted > psi_stable

    def test_window_size_respected(self):
        base = [0.5] * 100
        w = self._make_window(base, window_size=10)
        for i in range(20):
            w.add(float(i) / 20)
        assert w.status()["window_n"] <= 10

    def test_status_has_expected_keys(self):
        w = DriftWindow()
        w.set_baseline([0.5] * 10)
        w.add(0.5)
        status = w.status()
        for key in ("psi", "label", "chi2_stat", "chi2_dof",
                    "window_n", "baseline_n", "n_alerts", "is_drifting"):
            assert key in status

    def test_recent_alerts_limited(self):
        base = [0.1] * 200
        w = self._make_window(base, psi_threshold=0.01, window_size=50)
        for score in [0.9] * 50:
            w.add(score)
        alerts = w.recent_alerts(n=3)
        assert len(alerts) <= 3

    def test_is_drifting_true_when_psi_exceeds_threshold(self):
        base = [0.1] * 200
        w = self._make_window(base, psi_threshold=0.10, window_size=100)
        for score in [0.9] * 100:
            w.add(score)
        status = w.status()
        assert status["is_drifting"] is True

    def test_chi2_dof_matches_bins(self):
        base = [0.5] * 50
        w = self._make_window(base, bins=8)
        for score in [0.5] * 20:
            w.add(score)
        _, dof = w.current_chi2()
        assert dof == 7  # bins - 1
