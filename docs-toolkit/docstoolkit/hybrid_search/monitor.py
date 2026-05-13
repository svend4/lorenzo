"""Search latency monitoring for hybrid search backends."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SearchLatency:
    """Record of a single search operation's latency."""

    backend: str
    query: str
    duration_ms: float
    result_count: int


class HybridSearchMonitor:
    """Monitor for tracking search latency across backends."""

    def __init__(self):
        self._records: list[SearchLatency] = []

    def record(self, latency: SearchLatency) -> None:
        """Record a search latency entry."""
        self._records.append(latency)

    def avg_latency(self, backend: str = None) -> float:
        """Return average latency in milliseconds.

        Args:
            backend: if given, filter to this backend only.
                     If None, compute overall average across all backends.

        Returns:
            Average duration_ms, or 0.0 if no matching records.
        """
        if backend is not None:
            records = [r for r in self._records if r.backend == backend]
        else:
            records = self._records

        if not records:
            return 0.0
        return sum(r.duration_ms for r in records) / len(records)

    def slowest_queries(self, n: int = 5) -> list[SearchLatency]:
        """Return the n slowest queries by duration_ms, descending."""
        sorted_records = sorted(self._records, key=lambda r: r.duration_ms, reverse=True)
        return sorted_records[:n]

    def stats(self) -> dict:
        """Return aggregate statistics.

        Returns dict with:
        - total_queries: int
        - avg_latency_ms: float
        - per_backend: dict[str, dict] with total, avg_latency_ms per backend
        """
        total = len(self._records)
        overall_avg = self.avg_latency()

        # Group by backend
        backend_groups: dict[str, list[SearchLatency]] = {}
        for r in self._records:
            backend_groups.setdefault(r.backend, []).append(r)

        per_backend: dict[str, dict] = {}
        for backend_name, records in backend_groups.items():
            avg = sum(r.duration_ms for r in records) / len(records)
            per_backend[backend_name] = {
                "total": len(records),
                "avg_latency_ms": avg,
            }

        return {
            "total_queries": total,
            "avg_latency_ms": overall_avg,
            "per_backend": per_backend,
        }
