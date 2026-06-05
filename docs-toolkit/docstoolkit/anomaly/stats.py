"""Statistical utilities for anomaly detection — pure stdlib, no external deps."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class RunningStats:
    """Online Welford's algorithm for computing mean and variance incrementally.

    Immutable: every update returns a new instance.
    """

    n: int = 0
    mean: float = 0.0
    m2: float = 0.0  # sum of squared deviations from mean

    def update(self, x: float) -> "RunningStats":
        """Return a new RunningStats that includes *x* in the running totals."""
        n = self.n + 1
        delta = x - self.mean
        mean = self.mean + delta / n
        delta2 = x - mean
        m2 = self.m2 + delta * delta2
        return RunningStats(n=n, mean=mean, m2=m2)

    def variance(self) -> float:
        """Population variance (m2 / n).  Returns 0.0 when n <= 1."""
        if self.n > 1:
            return self.m2 / self.n
        return 0.0

    def std(self) -> float:
        """Standard deviation — sqrt of variance."""
        return math.sqrt(self.variance())

    def z_score(self, x: float) -> float:
        """Standardised score of *x* relative to the running distribution.

        Returns 0.0 when std is zero (constant series or too few samples).
        """
        s = self.std()
        if s > 0:
            return (x - self.mean) / s
        return 0.0


def moving_average(values: List[float], window: int) -> List[float]:
    """Simple (uniform) moving average over a sliding window.

    The first ``window - 1`` positions are computed over the available prefix
    so the output list has the same length as *values*.
    """
    if window < 1:
        raise ValueError("window must be >= 1")
    result: List[float] = []
    for i, _ in enumerate(values):
        start = max(0, i - window + 1)
        chunk = values[start : i + 1]
        result.append(sum(chunk) / len(chunk))
    return result


def ewma(values: List[float], alpha: float = 0.3) -> List[float]:
    """Exponentially Weighted Moving Average (EWMA).

    ``alpha`` controls how quickly older observations decay.  Higher alpha
    means more weight on recent values.  Must be in (0, 1].
    """
    if not (0 < alpha <= 1):
        raise ValueError("alpha must be in (0, 1]")
    if not values:
        return []
    result: List[float] = [values[0]]
    for v in values[1:]:
        result.append(alpha * v + (1 - alpha) * result[-1])
    return result
