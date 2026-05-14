"""Metric types and data structures for the metrics aggregator."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class MetricType(Enum):
    """Type of a metric, following Prometheus conventions."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


@dataclass
class MetricSample:
    """A single recorded metric sample.

    Attributes:
        name:        Metric name (e.g. "http_requests_total").
        value:       Numeric value of the measurement.
        labels:      Key/value label set for this sample.
        ts:          Unix timestamp when the sample was recorded.
        metric_type: Kind of metric this sample belongs to.
    """

    name: str
    value: float
    labels: dict[str, str] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)
    metric_type: MetricType = MetricType.GAUGE


@dataclass
class MetricFamily:
    """A named collection of samples sharing a common metric type.

    Attributes:
        name:        Metric name shared by all samples in this family.
        metric_type: Kind of metric (COUNTER, GAUGE, …).
        description: Human-readable description / help string.
        samples:     Ordered list of recorded samples (oldest first).
    """

    name: str
    metric_type: MetricType
    description: str = ""
    samples: list[MetricSample] = field(default_factory=list)

    def add_sample(self, value: float, labels: Optional[dict] = None) -> None:
        """Append a new sample with the given value and optional labels.

        A fresh timestamp is assigned automatically.

        Args:
            value:  Measurement value to record.
            labels: Optional label dict; defaults to empty dict.
        """
        self.samples.append(
            MetricSample(
                name=self.name,
                value=value,
                labels=labels if labels is not None else {},
                ts=time.time(),
                metric_type=self.metric_type,
            )
        )

    def latest(self) -> Optional[float]:
        """Return the value of the most recently added sample, or None.

        Returns:
            The last recorded value, or ``None`` if no samples exist.
        """
        if not self.samples:
            return None
        return self.samples[-1].value
