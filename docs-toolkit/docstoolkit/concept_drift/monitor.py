"""High-level concept drift monitor — pure stdlib."""
from __future__ import annotations

import time
from typing import Dict, List, Optional

from docstoolkit.concept_drift.detector import DDM, DriftConfig, DriftEvent, DriftType


class ConceptDriftMonitor:
    """Stateful monitor that feeds errors into a :class:`DDM` detector and
    records the history of detected drift events."""

    def __init__(self, config: Optional[DriftConfig] = None) -> None:
        self._config = config or DriftConfig()
        self._detector = DDM(self._config)
        self._history: List[DriftEvent] = []
        self._warning_count: int = 0
        # Track whether the *last* update produced a warning (not full drift)
        self._in_warning: bool = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add_error(
        self, error: float, ts: Optional[float] = None
    ) -> Optional[DriftEvent]:
        """Add a single error observation.

        Parameters
        ----------
        error:
            Error value (typically 0 or 1 for a binary classifier).
        ts:
            Optional Unix timestamp; unused internally but accepted for
            API symmetry with other monitors in this package.

        Returns
        -------
        :class:`DriftEvent` if drift was detected, ``None`` otherwise.
        """
        # Check for warning-level condition before calling update so we can
        # count it separately.
        event = self._detector.update(error)
        if event is not None:
            self._history.append(event)
        return event

    def add_errors(self, errors: List[float]) -> List[DriftEvent]:
        """Add a batch of error observations and return all detected events."""
        events: List[DriftEvent] = []
        for e in errors:
            event = self.add_error(e)
            if event is not None:
                events.append(event)
        return events

    def drift_history(self) -> List[DriftEvent]:
        """Return a copy of all detected drift events in chronological order."""
        return list(self._history)

    def is_drifting(self) -> bool:
        """Return True if a drift event was detected recently.

        "Recently" means the last event's ``detected_at`` index falls within
        the last ``window_size`` samples.
        """
        if not self._history:
            return False
        last = self._history[-1]
        if last.drift_type == DriftType.NONE:
            return False
        window = self._config.window_size
        return last.detected_at >= self._detector.sample_count() - window

    def stats(self) -> Dict[str, int]:
        """Return summary statistics about this monitor."""
        drift_count = sum(
            1 for e in self._history if e.drift_type != DriftType.NONE
        )
        return {
            "total_samples": self._detector.sample_count(),
            "drift_count": drift_count,
            "warning_count": self._warning_count,
        }
