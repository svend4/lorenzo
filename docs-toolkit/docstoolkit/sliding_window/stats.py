"""WindowedStatistics: percentile, mean, stddev over a time-based window."""
import math

from docstoolkit.sliding_window.window import SlidingWindow, WindowConfig, WindowType


class WindowedStatistics:
    """Statistical summaries over values seen in a sliding time window."""

    def __init__(self, window_size: float = 60.0):
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        self._window = SlidingWindow(WindowConfig(size=float(window_size),
                                                 window_type=WindowType.TIME))

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def record(self, value: float, now: "float | None" = None) -> None:
        """Add a sample to the window."""
        self._window.add(float(value), now=now)

    # ------------------------------------------------------------------
    # Aggregates
    # ------------------------------------------------------------------

    def _values(self, now: "float | None") -> list[float]:
        return [v for _, v in self._window.values(now=now)]

    def percentile(self, p: float, now: "float | None" = None) -> float:
        """Linear-interpolated percentile (p in [0, 100]).

        Raises:
            ValueError: if the window is empty or ``p`` is out of range.
        """
        if p < 0 or p > 100:
            raise ValueError("p must be in [0, 100]")
        vals = sorted(self._values(now))
        if not vals:
            raise ValueError("cannot compute percentile of empty window")
        if len(vals) == 1:
            return vals[0]
        # Linear interpolation between closest ranks.
        rank = (p / 100.0) * (len(vals) - 1)
        lo = int(math.floor(rank))
        hi = int(math.ceil(rank))
        if lo == hi:
            return vals[lo]
        frac = rank - lo
        return vals[lo] + (vals[hi] - vals[lo]) * frac

    def mean(self, now: "float | None" = None) -> float:
        """Arithmetic mean; 0.0 if empty."""
        vals = self._values(now)
        if not vals:
            return 0.0
        return sum(vals) / len(vals)

    def stddev(self, now: "float | None" = None) -> float:
        """Population standard deviation; 0.0 if fewer than 2 samples."""
        vals = self._values(now)
        n = len(vals)
        if n < 2:
            return 0.0
        m = sum(vals) / n
        variance = sum((v - m) ** 2 for v in vals) / n
        return math.sqrt(variance)

    def count_in_window(self, now: "float | None" = None) -> int:
        """Number of samples currently in the window."""
        return self._window.count(now=now)

    def summary(self, now: "float | None" = None) -> dict:
        """Summary dict: count, mean, min, max, stddev, p50, p95, p99.

        For an empty window: count is 0, all stats default to 0.0 / None.
        """
        vals = sorted(self._values(now))
        n = len(vals)
        if n == 0:
            return {
                "count": 0,
                "mean": 0.0,
                "min": None,
                "max": None,
                "stddev": 0.0,
                "p50": 0.0,
                "p95": 0.0,
                "p99": 0.0,
            }
        m = sum(vals) / n
        if n >= 2:
            variance = sum((v - m) ** 2 for v in vals) / n
            sd = math.sqrt(variance)
        else:
            sd = 0.0
        return {
            "count": n,
            "mean": m,
            "min": vals[0],
            "max": vals[-1],
            "stddev": sd,
            "p50": self.percentile(50.0, now=now),
            "p95": self.percentile(95.0, now=now),
            "p99": self.percentile(99.0, now=now),
        }
