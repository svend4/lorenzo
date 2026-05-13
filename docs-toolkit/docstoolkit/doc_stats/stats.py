"""Document statistics engine.

Aggregated statistics over collections of documents (list of dicts) with
support for grouping, comparison, percentiles, histograms and correlation.
Uses only stdlib (`statistics`, `collections`).
"""
from __future__ import annotations

import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable


class MetricType(str, Enum):
    """Supported aggregation metric types."""

    COUNT = "count"
    SUM = "sum"
    AVG = "avg"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    STDDEV = "stddev"
    P25 = "p25"
    P50 = "p50"
    P75 = "p75"
    P90 = "p90"
    P99 = "p99"


# Percentile metric types mapped to their target percentile value.
_PERCENTILE_MAP: dict[MetricType, float] = {
    MetricType.P25: 25.0,
    MetricType.P50: 50.0,
    MetricType.P75: 75.0,
    MetricType.P90: 90.0,
    MetricType.P99: 99.0,
}


@dataclass
class DocStat:
    """Single computed statistic for one (field, metric) pair."""

    metric_type: MetricType
    value: float
    field: str


@dataclass
class GroupedStats:
    """Statistics computed for a single group.

    `stats` maps each metric field name to its dict of metric_type → value.
    """

    group_key: str
    count: int
    stats: dict[str, dict[MetricType, float]] = field(default_factory=dict)


@dataclass
class Distribution:
    """Histogram-based distribution of a numeric field."""

    field: str
    histogram: dict[str, int]
    bin_count: int
    min_value: float
    max_value: float


@dataclass
class ComparisonResult:
    """Result of comparing the same metric between two collections."""

    field: str
    metric: MetricType
    value_a: float
    value_b: float
    delta: float
    pct_change: float


def _get_field(doc: dict, dotted: str) -> Any:
    """Resolve a dotted field path against a nested dict-like document."""
    if not isinstance(doc, dict):
        return None
    cur: Any = doc
    for part in dotted.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return None
    return cur


def _to_number(value: Any) -> float | None:
    """Coerce a value to float, returning None if not numeric."""
    if value is None:
        return None
    # bool is a subclass of int — treat as non-numeric for stats purposes.
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            return None
        return float(value)
    return None


def _percentile_linear(sorted_values: list[float], p: float) -> float:
    """Linear interpolation percentile (p in [0, 100]) on a pre-sorted list."""
    if not sorted_values:
        return 0.0
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    if p <= 0:
        return float(sorted_values[0])
    if p >= 100:
        return float(sorted_values[-1])
    # 0-indexed rank using linear interpolation
    rank = (p / 100.0) * (len(sorted_values) - 1)
    low = int(math.floor(rank))
    high = int(math.ceil(rank))
    if low == high:
        return float(sorted_values[low])
    frac = rank - low
    return float(sorted_values[low] + (sorted_values[high] - sorted_values[low]) * frac)


class DocStats:
    """Compute aggregated statistics over collections of documents."""

    def __init__(self) -> None:
        # Stateless engine for now — instance kept for API symmetry.
        pass

    # ------------------------------------------------------------------ helpers

    def extract_values(self, docs: list[dict], field: str) -> list[float]:
        """Extract numeric values for `field` (dotted ok), skipping missing/non-numeric."""
        out: list[float] = []
        if not docs:
            return out
        for doc in docs:
            val = _get_field(doc, field)
            num = _to_number(val)
            if num is not None:
                out.append(num)
        return out

    # ------------------------------------------------------------------ compute

    def compute(self, docs: list[dict], field: str, metric: MetricType) -> DocStat:
        """Compute one metric for one field."""
        if metric == MetricType.COUNT:
            # COUNT counts docs where the field is present and numeric.
            values = self.extract_values(docs, field)
            return DocStat(metric_type=metric, value=float(len(values)), field=field)

        values = self.extract_values(docs, field)
        value = self._reduce(values, metric)
        return DocStat(metric_type=metric, value=value, field=field)

    def compute_many(
        self,
        docs: list[dict],
        field: str,
        metrics: list[MetricType] | None = None,
    ) -> dict[MetricType, float]:
        """Compute multiple metrics for one field in a single pass."""
        if metrics is None:
            metrics = [
                MetricType.COUNT,
                MetricType.SUM,
                MetricType.AVG,
                MetricType.MEDIAN,
                MetricType.MIN,
                MetricType.MAX,
                MetricType.STDDEV,
            ]
        values = self.extract_values(docs, field)
        out: dict[MetricType, float] = {}
        for m in metrics:
            if m == MetricType.COUNT:
                out[m] = float(len(values))
            else:
                out[m] = self._reduce(values, m)
        return out

    def _reduce(self, values: list[float], metric: MetricType) -> float:
        """Reduce a list of numeric values according to the metric type."""
        if not values:
            return 0.0
        if metric == MetricType.COUNT:
            return float(len(values))
        if metric == MetricType.SUM:
            return float(sum(values))
        if metric == MetricType.AVG:
            return float(statistics.mean(values))
        if metric == MetricType.MEDIAN:
            return float(statistics.median(values))
        if metric == MetricType.MIN:
            return float(min(values))
        if metric == MetricType.MAX:
            return float(max(values))
        if metric == MetricType.STDDEV:
            if len(values) < 2:
                return 0.0
            return float(statistics.stdev(values))
        if metric in _PERCENTILE_MAP:
            sorted_values = sorted(values)
            return _percentile_linear(sorted_values, _PERCENTILE_MAP[metric])
        return 0.0

    # ------------------------------------------------------------------ group_by

    def group_by(
        self,
        docs: list[dict],
        group_field: str,
        metric_fields: list[str],
        metrics: list[MetricType] | None = None,
    ) -> list[GroupedStats]:
        """Group documents by `group_field` and compute metrics per group."""
        if metrics is None:
            metrics = [
                MetricType.COUNT,
                MetricType.SUM,
                MetricType.AVG,
                MetricType.MIN,
                MetricType.MAX,
            ]

        buckets: dict[str, list[dict]] = defaultdict(list)
        for doc in docs or []:
            key_val = _get_field(doc, group_field)
            if key_val is None:
                continue
            buckets[str(key_val)].append(doc)

        results: list[GroupedStats] = []
        for key, group_docs in buckets.items():
            field_stats: dict[str, dict[MetricType, float]] = {}
            for mf in metric_fields:
                field_stats[mf] = self.compute_many(group_docs, mf, metrics)
            results.append(
                GroupedStats(group_key=key, count=len(group_docs), stats=field_stats)
            )
        results.sort(key=lambda g: g.group_key)
        return results

    # ------------------------------------------------------------------ count_by

    def count_by(self, docs: list[dict], field: str) -> dict[Any, int]:
        """Count docs by value of `field` (any hashable value)."""
        counter: Counter = Counter()
        for doc in docs or []:
            val = _get_field(doc, field)
            if val is None:
                continue
            try:
                counter[val] += 1
            except TypeError:
                # Unhashable value (e.g. list/dict) — coerce to string.
                counter[str(val)] += 1
        return dict(counter)

    # ------------------------------------------------------------------ distribution

    def distribution(
        self, docs: list[dict], field: str, bins: int = 10
    ) -> Distribution:
        """Build a histogram with `bins` equal-width buckets for `field`."""
        if bins < 1:
            bins = 1
        values = self.extract_values(docs, field)
        if not values:
            return Distribution(
                field=field,
                histogram={},
                bin_count=bins,
                min_value=0.0,
                max_value=0.0,
            )
        min_v = min(values)
        max_v = max(values)
        histogram: dict[str, int] = {}

        if min_v == max_v:
            label = f"[{min_v:.4g}, {max_v:.4g}]"
            histogram[label] = len(values)
            return Distribution(
                field=field,
                histogram=histogram,
                bin_count=bins,
                min_value=float(min_v),
                max_value=float(max_v),
            )

        width = (max_v - min_v) / bins
        edges = [min_v + i * width for i in range(bins + 1)]
        counts = [0] * bins
        for v in values:
            if v >= max_v:
                idx = bins - 1
            else:
                idx = int((v - min_v) / width)
                if idx < 0:
                    idx = 0
                elif idx >= bins:
                    idx = bins - 1
            counts[idx] += 1

        for i in range(bins):
            lo = edges[i]
            hi = edges[i + 1]
            label = f"[{lo:.4g}, {hi:.4g}{')' if i < bins - 1 else ']'}"
            label = f"[{lo:.4g}, {hi:.4g}" + (")" if i < bins - 1 else "]")
            histogram[label] = counts[i]

        return Distribution(
            field=field,
            histogram=histogram,
            bin_count=bins,
            min_value=float(min_v),
            max_value=float(max_v),
        )

    # ------------------------------------------------------------------ compare

    def compare(
        self,
        docs_a: list[dict],
        docs_b: list[dict],
        field: str,
        metrics: list[MetricType] | None = None,
    ) -> list[ComparisonResult]:
        """Compare the same metric on `field` between two doc collections."""
        if metrics is None:
            metrics = [
                MetricType.COUNT,
                MetricType.SUM,
                MetricType.AVG,
                MetricType.MEDIAN,
                MetricType.MIN,
                MetricType.MAX,
                MetricType.STDDEV,
            ]
        results: list[ComparisonResult] = []
        values_a = self.extract_values(docs_a, field)
        values_b = self.extract_values(docs_b, field)
        for m in metrics:
            if m == MetricType.COUNT:
                va = float(len(values_a))
                vb = float(len(values_b))
            else:
                va = self._reduce(values_a, m)
                vb = self._reduce(values_b, m)
            delta = vb - va
            if va == 0:
                pct = 0.0 if vb == 0 else float("inf")
            else:
                pct = (delta / abs(va)) * 100.0
            results.append(
                ComparisonResult(
                    field=field,
                    metric=m,
                    value_a=va,
                    value_b=vb,
                    delta=delta,
                    pct_change=pct,
                )
            )
        return results

    # ------------------------------------------------------------------ top/bottom

    def top_n(
        self, docs: list[dict], field: str, n: int = 10, reverse: bool = True
    ) -> list[dict]:
        """Return the `n` docs with highest (or lowest if reverse=False) field value."""
        if not docs or n <= 0:
            return []
        scored: list[tuple[float, int, dict]] = []
        for i, doc in enumerate(docs):
            val = _to_number(_get_field(doc, field))
            if val is None:
                continue
            scored.append((val, i, doc))
        scored.sort(key=lambda t: (t[0], -t[1] if reverse else t[1]), reverse=reverse)
        return [t[2] for t in scored[:n]]

    def bottom_n(self, docs: list[dict], field: str, n: int = 10) -> list[dict]:
        """Return the `n` docs with lowest field value (ascending)."""
        return self.top_n(docs, field, n=n, reverse=False)

    # ------------------------------------------------------------------ percentile

    def percentile(self, docs: list[dict], field: str, p: float) -> float:
        """Compute an arbitrary percentile (p in [0, 100]) for `field`."""
        values = self.extract_values(docs, field)
        if not values:
            return 0.0
        sorted_values = sorted(values)
        return _percentile_linear(sorted_values, float(p))

    # ------------------------------------------------------------------ correlation

    def correlation(
        self, docs: list[dict], field_a: str, field_b: str
    ) -> float:
        """Pearson correlation between two numeric fields. Returns 0.0 when undefined."""
        pairs: list[tuple[float, float]] = []
        for doc in docs or []:
            va = _to_number(_get_field(doc, field_a))
            vb = _to_number(_get_field(doc, field_b))
            if va is None or vb is None:
                continue
            pairs.append((va, vb))
        n = len(pairs)
        if n < 2:
            return 0.0
        mean_a = sum(p[0] for p in pairs) / n
        mean_b = sum(p[1] for p in pairs) / n
        cov = sum((p[0] - mean_a) * (p[1] - mean_b) for p in pairs)
        var_a = sum((p[0] - mean_a) ** 2 for p in pairs)
        var_b = sum((p[1] - mean_b) ** 2 for p in pairs)
        denom = math.sqrt(var_a * var_b)
        if denom == 0:
            return 0.0
        return float(cov / denom)

    # ------------------------------------------------------------------ summary

    def summary(self, docs: list[dict], field: str) -> dict:
        """Return a summary dict with count/min/max/avg/median/stddev for `field`."""
        values = self.extract_values(docs, field)
        if not values:
            return {
                "count": 0,
                "min": 0.0,
                "max": 0.0,
                "avg": 0.0,
                "median": 0.0,
                "stddev": 0.0,
            }
        return {
            "count": len(values),
            "min": float(min(values)),
            "max": float(max(values)),
            "avg": float(statistics.mean(values)),
            "median": float(statistics.median(values)),
            "stddev": float(statistics.stdev(values)) if len(values) >= 2 else 0.0,
        }
