"""Document query log — records search queries, computes stats and trends."""
from docstoolkit.doc_query_log.log import (
    DocQueryLog,
    QueryEntry,
    QueryStats,
    Trend,
)

__all__ = [
    "DocQueryLog",
    "QueryEntry",
    "QueryStats",
    "Trend",
]
