"""Cost estimation statistics for query planning."""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class TableStats:
    table_name: str
    row_count: int
    avg_row_size: int = 100


class CostEstimator:
    """Estimates costs for various query plan operations."""

    def __init__(self, stats: dict[str, TableStats] | None = None) -> None:
        self._stats: dict[str, TableStats] = stats if stats is not None else {}

    def estimate_scan(self, table: str) -> float:
        """Estimate cost of a full table scan.

        Returns ``row_count * avg_row_size / 1000`` for known tables,
        or 1.0 for unknown tables.
        """
        if table not in self._stats:
            return 1.0
        ts = self._stats[table]
        return ts.row_count * ts.avg_row_size / 1000.0

    def estimate_filter(self, selectivity: float) -> float:
        """Estimate the cost of applying a filter.

        ``selectivity`` is a value in [0.0, 1.0].  Cost = selectivity * 10.0.
        """
        return selectivity * 10.0

    def estimate_sort(self, row_count: int) -> float:
        """Estimate the cost of sorting *row_count* rows.

        Cost = row_count * log2(row_count + 1) / 1000.
        """
        return row_count * math.log2(row_count + 1) / 1000.0

    def estimate_join(self, left_rows: int, right_rows: int) -> float:
        """Estimate the cost of a nested-loop join.

        Cost = left_rows * right_rows / 1000.
        """
        return left_rows * right_rows / 1000.0
