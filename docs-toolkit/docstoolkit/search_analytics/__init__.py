"""Search analytics: query tracking, trends, and zero-result monitoring."""
from docstoolkit.search_analytics.tracker import QueryTracker, QueryRecord
from docstoolkit.search_analytics.trends import TrendAnalyzer, TrendReport, QueryTrend
from docstoolkit.search_analytics.zero_results import ZeroResultMonitor, ZeroResultAlert

__all__ = [
    "QueryTracker", "QueryRecord",
    "TrendAnalyzer", "TrendReport", "QueryTrend",
    "ZeroResultMonitor", "ZeroResultAlert",
]
