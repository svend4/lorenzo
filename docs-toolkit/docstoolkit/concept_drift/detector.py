"""Concept drift detector (DDM) — pure stdlib, no external dependencies."""
from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DriftType(Enum):
    ABRUPT = "abrupt"
    GRADUAL = "gradual"
    INCREMENTAL = "incremental"
    NONE = "none"


@dataclass
class DriftEvent:
    """Describes a detected drift event."""

    drift_type: DriftType
    detected_at: int    # sample index at which drift was detected
    magnitude: float    # measure of how large the shift is
    description: str

    def is_significant(self, threshold: float = 0.5) -> bool:
        """Return True if *magnitude* exceeds *threshold*."""
        return self.magnitude > threshold


@dataclass
class DriftConfig:
    """Hyper-parameters for the DDM detector."""

    warning_threshold: float = 1.5
    drift_threshold: float = 2.0
    window_size: int = 30


class DDM:
    """Drift Detection Method (DDM).

    Monitors a sequence of binary error signals (0 or 1) and flags concept
    drift by tracking changes in the running error rate relative to its
    historical minimum.

    References
    ----------
    Gama et al. (2004) "Learning with Drift Detection."
    """

    def __init__(self, config: Optional[DriftConfig] = None) -> None:
        self._config = config or DriftConfig()
        self.reset()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def update(self, error: float) -> Optional[DriftEvent]:
        """Feed the next error observation.

        Parameters
        ----------
        error:
            Binary or continuous error value (0 = correct, 1 = wrong).

        Returns
        -------
        :class:`DriftEvent` if drift was detected, ``None`` otherwise.
        """
        self._n += 1

        # Online mean update (Welford-style incremental)
        # p  = running mean of errors
        # s  = running std of errors  (approximated via Bernoulli: sqrt(p*(1-p)/n))
        self._p += (error - self._p) / self._n
        # Bernoulli standard deviation of the mean
        p = self._p
        if p <= 0 or p >= 1:
            s = 0.0
        else:
            s = math.sqrt(p * (1.0 - p) / self._n)
        self._s = s

        # Update minima
        if self._p_min is None or (self._p + self._s) < (self._p_min + self._s_min):
            self._p_min = self._p
            self._s_min = self._s

        # Guard against undefined minima
        if self._p_min is None:
            return None

        combined = self._p + self._s
        min_combined = self._p_min + self._s_min

        cfg = self._config

        # DRIFT level
        if combined > min_combined + cfg.drift_threshold * self._s_min:
            magnitude = (
                (combined - min_combined) / self._s_min
                if self._s_min > 0
                else combined - min_combined
            )
            event = DriftEvent(
                drift_type=DriftType.ABRUPT,
                detected_at=self._n,
                magnitude=magnitude,
                description=(
                    f"DDM DRIFT at sample {self._n}: "
                    f"p={self._p:.4f}, s={self._s:.4f}, "
                    f"p_min={self._p_min:.4f}, s_min={self._s_min:.4f}"
                ),
            )
            # Reset minima so the detector can track the new concept
            self._p_min = self._p
            self._s_min = self._s
            return event

        # WARNING level — not returned as a DriftEvent (internal signal only)
        # (callers that need warning can inspect stats directly)

        return None

    def reset(self) -> None:
        """Reset all internal state."""
        self._n: int = 0
        self._p: float = 0.0
        self._s: float = 0.0
        self._p_min: Optional[float] = None
        self._s_min: float = 0.0

    def sample_count(self) -> int:
        """Return the total number of samples seen since the last reset."""
        return self._n
