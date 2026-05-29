"""Online evaluation drift detection using Population Stability Index (PSI).

PSI is the standard measure of score-distribution drift used in credit risk and
ML-monitoring.  A PSI > 0.25 indicates significant drift; 0.10–0.25 is a
moderate shift worth investigating.

This module works *without* numpy or scipy — pure stdlib only.

References:
    Siddiqi, N. (2006). Credit Risk Scorecards. Wiley.
    PSI = Σ (Actual% - Expected%) × ln(Actual% / Expected%)
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional, Sequence


# ---------------------------------------------------------------------------
# PSI core
# ---------------------------------------------------------------------------

def _bin_counts(values: Sequence[float], bins: int = 10) -> List[int]:
    """Assign *values* (all in [0, 1]) to *bins* equal-width buckets."""
    counts = [0] * bins
    for v in values:
        idx = min(int(v * bins), bins - 1)
        counts[idx] += 1
    return counts


def psi(
    baseline: Sequence[float],
    current: Sequence[float],
    bins: int = 10,
    smoothing: float = 1e-6,
) -> float:
    """Compute the Population Stability Index between two score distributions.

    Parameters
    ----------
    baseline:
        Reference scores (e.g. golden-set scores from last month).  Each
        value should be in [0, 1].
    current:
        Current distribution to compare against baseline.
    bins:
        Number of equal-width bins to use.
    smoothing:
        Small constant added to each bin to avoid log(0).

    Returns
    -------
    PSI value.  Typical thresholds:

    * < 0.10 — no meaningful drift
    * 0.10–0.25 — moderate shift, monitor
    * > 0.25 — significant drift, investigate / retrain
    """
    if not baseline or not current:
        return 0.0

    n_base = len(baseline)
    n_curr = len(current)

    base_counts = _bin_counts(baseline, bins)
    curr_counts = _bin_counts(current, bins)

    psi_val = 0.0
    for b_cnt, c_cnt in zip(base_counts, curr_counts):
        b_pct = (b_cnt + smoothing) / n_base
        c_pct = (c_cnt + smoothing) / n_curr
        psi_val += (c_pct - b_pct) * math.log(c_pct / b_pct)

    return psi_val


def psi_label(value: float) -> str:
    """Return a human-readable stability label for a PSI *value*."""
    if value < 0.10:
        return "stable"
    if value < 0.25:
        return "moderate_shift"
    return "significant_drift"


# ---------------------------------------------------------------------------
# Chi-square goodness-of-fit
# ---------------------------------------------------------------------------

def chi_square_drift(
    baseline: Sequence[float],
    current: Sequence[float],
    bins: int = 10,
    smoothing: float = 0.5,
) -> tuple[float, int]:
    """Return (chi-square statistic, degrees of freedom).

    Uses Pearson's χ² goodness-of-fit to test whether *current* comes from
    the same distribution as *baseline*.

    The p-value is **not** computed (avoid scipy dependency); callers may
    use ``statistics`` or compare to tabulated critical values.

    Degrees of freedom = bins - 1.
    """
    if not baseline or not current:
        return 0.0, bins - 1

    n_base = len(baseline)
    n_curr = len(current)

    base_counts = _bin_counts(baseline, bins)
    curr_counts = _bin_counts(current, bins)

    chi2 = 0.0
    for b_cnt, c_cnt in zip(base_counts, curr_counts):
        expected = (b_cnt + smoothing) / n_base * n_curr
        diff = c_cnt - expected
        chi2 += (diff ** 2) / expected

    return chi2, bins - 1


# ---------------------------------------------------------------------------
# Drift monitor
# ---------------------------------------------------------------------------

@dataclass
class DriftWindow:
    """Sliding-window accumulator for online drift monitoring.

    Parameters
    ----------
    window_size:
        Number of recent scores to keep in the sliding window.
    psi_threshold:
        PSI value above which an alert is fired.
    bins:
        Number of histogram bins.
    """
    window_size: int = 500
    psi_threshold: float = 0.25
    bins: int = 10
    _baseline: List[float] = field(default_factory=list, repr=False)
    _window: List[float] = field(default_factory=list, repr=False)
    _alerts: List[dict] = field(default_factory=list, repr=False)

    def set_baseline(self, scores: Sequence[float]) -> None:
        """Set (or replace) the reference distribution."""
        self._baseline = list(scores)

    def add(self, score: float) -> Optional[dict]:
        """Append a new score to the sliding window.

        Returns an alert dict if PSI threshold is exceeded, None otherwise.
        """
        self._window.append(score)
        if len(self._window) > self.window_size:
            self._window.pop(0)

        if len(self._baseline) < 2 or len(self._window) < 2:
            return None

        psi_val = psi(self._baseline, self._window, bins=self.bins)
        if psi_val > self.psi_threshold:
            alert = {
                "psi": psi_val,
                "label": psi_label(psi_val),
                "window_size": len(self._window),
                "threshold": self.psi_threshold,
            }
            self._alerts.append(alert)
            return alert
        return None

    def current_psi(self) -> float:
        """Return PSI for the current window against baseline."""
        if len(self._baseline) < 2 or len(self._window) < 2:
            return 0.0
        return psi(self._baseline, self._window, bins=self.bins)

    def current_chi2(self) -> tuple[float, int]:
        """Return chi-square statistic for the current window."""
        if len(self._baseline) < 2 or len(self._window) < 2:
            return 0.0, self.bins - 1
        return chi_square_drift(self._baseline, self._window, bins=self.bins)

    def status(self) -> dict:
        """Return a summary dict of the drift monitor state."""
        psi_val = self.current_psi()
        chi2, dof = self.current_chi2()
        return {
            "psi": psi_val,
            "label": psi_label(psi_val),
            "chi2_stat": chi2,
            "chi2_dof": dof,
            "window_n": len(self._window),
            "baseline_n": len(self._baseline),
            "n_alerts": len(self._alerts),
            "is_drifting": psi_val > self.psi_threshold,
        }

    def recent_alerts(self, n: int = 10) -> List[dict]:
        """Return the *n* most recent alerts."""
        return self._alerts[-n:]
