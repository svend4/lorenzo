"""Reporter utilities: build and export metrics reports."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from docstoolkit.metrics_agg.aggregator import MetricsAggregator


@dataclass
class MetricsReport:
    """A snapshot of aggregated metric data.

    Attributes:
        generated_at: Unix timestamp when the report was produced.
        metrics:      Mapping of metric name → aggregated stat dict.
                      Each value contains keys ``count``, ``mean``,
                      ``min``, ``max``, and ``samples`` (list of
                      serialisable dicts).
    """

    generated_at: float
    metrics: dict[str, dict] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Formatting
    # ------------------------------------------------------------------

    def to_text(self) -> str:
        """Render the report in a simple Prometheus-like text format.

        Each sample produces one line::

            metric_name{label=value,...} <value> <ts>

        If a sample has no labels the ``{}`` block is omitted.

        Returns:
            Multi-line string with one line per sample, ending with
            a trailing newline (or empty string if there are no samples).
        """
        lines: list[str] = []
        for _metric_name, meta in self.metrics.items():
            for sample in meta.get("samples", []):
                name = sample["name"]
                labels: dict = sample.get("labels", {})
                value = sample["value"]
                ts = sample["ts"]
                if labels:
                    label_str = ",".join(
                        f'{k}={v}' for k, v in sorted(labels.items())
                    )
                    lines.append(f"{name}{{{label_str}}} {value} {ts}")
                else:
                    lines.append(f"{name} {value} {ts}")
        return "\n".join(lines) + ("\n" if lines else "")


class MetricsReporter:
    """Builds :class:`MetricsReport` objects from a :class:`MetricsAggregator`.

    Args:
        aggregator: The aggregator whose data is reported.
    """

    def __init__(self, aggregator: MetricsAggregator) -> None:
        self._agg = aggregator

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def report(self, names: Optional[list[str]] = None) -> MetricsReport:
        """Generate a :class:`MetricsReport`.

        For each requested metric name the report includes:
        ``count``, ``mean``, ``min``, ``max``, and a ``samples`` list
        of serialisable dicts (``name``, ``value``, ``labels``, ``ts``,
        ``metric_type``).

        Args:
            names: Metric names to include.  ``None`` → all recorded
                   names.

        Returns:
            A fresh :class:`MetricsReport` snapshot.
        """
        if names is None:
            names = self._agg.names()

        metrics_data: dict[str, dict] = {}
        for name in names:
            samples = [s for s in self._agg._samples if s.name == name]
            values = [s.value for s in samples]
            count = len(values)
            mean_val = sum(values) / count if count else 0.0
            min_val = min(values) if count else 0.0
            max_val = max(values) if count else 0.0
            metrics_data[name] = {
                "count": count,
                "mean": mean_val,
                "min": min_val,
                "max": max_val,
                "samples": [
                    {
                        "name": s.name,
                        "value": s.value,
                        "labels": dict(s.labels),
                        "ts": s.ts,
                        "metric_type": s.metric_type.value,
                    }
                    for s in samples
                ],
            }

        return MetricsReport(generated_at=time.time(), metrics=metrics_data)

    def export_json(self, path: "str | Path") -> None:
        """Write the current report to *path* as JSON.

        Produces a report for all recorded metrics and serialises it
        with :func:`json.dump` (indented for human readability).

        Args:
            path: Destination file path (will be created or overwritten).
        """
        rpt = self.report()
        payload = {
            "generated_at": rpt.generated_at,
            "metrics": rpt.metrics,
        }
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
