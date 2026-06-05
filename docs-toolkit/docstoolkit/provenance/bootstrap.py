"""Bootstrap confidence intervals for similarity statistics."""
import random
import math
from dataclasses import dataclass


@dataclass
class BootstrapCI:
    point_estimate: float
    ci_low: float
    ci_high: float
    n_samples: int
    confidence_level: float = 0.95


def _percentile(sorted_data: list[float], p: float) -> float:
    """Return the p-th percentile (0 < p < 1) of a sorted list."""
    n = len(sorted_data)
    if n == 0:
        return 0.0
    if n == 1:
        return sorted_data[0]
    idx = p * (n - 1)
    lo = int(idx)
    hi = lo + 1
    if hi >= n:
        return sorted_data[-1]
    frac = idx - lo
    return sorted_data[lo] * (1 - frac) + sorted_data[hi] * frac


def _compute_statistic(values: list[float], statistic: str) -> float:
    if not values:
        return 0.0
    if statistic == "mean":
        return sum(values) / len(values)
    elif statistic == "max":
        return max(values)
    elif statistic == "median":
        s = sorted(values)
        n = len(s)
        mid = n // 2
        if n % 2 == 0:
            return (s[mid - 1] + s[mid]) / 2.0
        return s[mid]
    else:
        raise ValueError(f"Unknown statistic: {statistic!r}. Use 'mean', 'max', or 'median'.")


def bootstrap_ci(
    values: list[float],
    *,
    statistic: str = "mean",
    n_bootstrap: int = 200,
    confidence_level: float = 0.95,
    seed: int | None = None,
) -> BootstrapCI:
    """Bootstrap confidence interval for a statistic on a list of values.

    Algorithm:
    1. If values is empty: return BootstrapCI(0.0, 0.0, 0.0, 0)
    2. Compute point_estimate = statistic(values)
    3. For n_bootstrap iterations:
       - resample len(values) items with replacement
       - compute statistic on resample
       - append to bootstrap_stats
    4. Sort bootstrap_stats
    5. alpha = (1 - confidence_level) / 2
    6. ci_low = percentile(bootstrap_stats, alpha)
    7. ci_high = percentile(bootstrap_stats, 1-alpha)

    Pure stdlib, no numpy.
    """
    if not values:
        return BootstrapCI(
            point_estimate=0.0,
            ci_low=0.0,
            ci_high=0.0,
            n_samples=0,
            confidence_level=confidence_level,
        )

    rng = random.Random(seed)
    n = len(values)
    point_estimate = _compute_statistic(values, statistic)

    bootstrap_stats: list[float] = []
    for _ in range(n_bootstrap):
        resample = [rng.choice(values) for _ in range(n)]
        bootstrap_stats.append(_compute_statistic(resample, statistic))

    bootstrap_stats.sort()
    alpha = (1 - confidence_level) / 2
    ci_low = _percentile(bootstrap_stats, alpha)
    ci_high = _percentile(bootstrap_stats, 1 - alpha)

    return BootstrapCI(
        point_estimate=point_estimate,
        ci_low=ci_low,
        ci_high=ci_high,
        n_samples=n_bootstrap,
        confidence_level=confidence_level,
    )
