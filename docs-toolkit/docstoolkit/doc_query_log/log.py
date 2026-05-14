"""In-memory query log analyzer for document search systems.

Records search queries with metadata (user, latency, result count, selected
result), computes aggregate statistics, finds trending queries, and surfaces
zero-result queries.  Uses only the standard library (``threading``,
``collections``) and is safe for concurrent use.
"""
from collections import Counter, deque
from dataclasses import dataclass, field
from threading import Lock
from typing import Optional


@dataclass
class QueryEntry:
    """A single recorded search query."""

    query_id: int = 0
    query: str = ""
    user_id: Optional[str] = None
    result_count: int = 0
    timestamp: float = 0.0
    selected_result: Optional[str] = None
    latency_ms: float = 0.0


@dataclass
class QueryStats:
    """Aggregate statistics over a set of query entries."""

    total_queries: int = 0
    unique_queries: int = 0
    zero_result_count: int = 0
    avg_results: float = 0.0
    avg_latency_ms: float = 0.0
    top_queries: list = field(default_factory=list)   # list[tuple[str, int]]
    top_users: list = field(default_factory=list)     # list[tuple[str, int]]


@dataclass
class Trend:
    """Change in popularity of a query between two time windows."""

    query: str = ""
    recent_count: int = 0
    older_count: int = 0
    growth_rate: float = 0.0


class DocQueryLog:
    """Thread-safe, bounded, in-memory document query log.

    Parameters
    ----------
    max_entries:
        Maximum number of entries kept.  When the log is full, the oldest
        entry is evicted (FIFO).
    """

    def __init__(self, max_entries: int = 100_000) -> None:
        if max_entries <= 0:
            raise ValueError("max_entries must be > 0")
        self._max_entries = max_entries
        self._entries: "deque[QueryEntry]" = deque(maxlen=max_entries)
        self._lock = Lock()
        self._next_id = 1

    # ------------------------------------------------------------------
    # Recording
    # ------------------------------------------------------------------

    def log(
        self,
        query: str,
        result_count: int = 0,
        user_id: Optional[str] = None,
        selected_result: Optional[str] = None,
        latency_ms: float = 0.0,
        now: float = 0.0,
    ) -> QueryEntry:
        """Append a new query entry and return it."""
        with self._lock:
            entry = QueryEntry(
                query_id=self._next_id,
                query=query,
                user_id=user_id,
                result_count=result_count,
                timestamp=now,
                selected_result=selected_result,
                latency_ms=latency_ms,
            )
            self._next_id += 1
            self._entries.append(entry)
            return entry

    def record_selection(self, query_id: int, selected_result: str) -> bool:
        """Set ``selected_result`` on an existing entry.

        Returns ``True`` if found, ``False`` otherwise.
        """
        with self._lock:
            for entry in self._entries:
                if entry.query_id == query_id:
                    entry.selected_result = selected_result
                    return True
            return False

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------

    def recent(self, n: int = 10) -> list:
        """Return the last ``n`` entries in reverse-chronological order."""
        with self._lock:
            snap = list(self._entries)
        if n <= 0:
            return []
        return list(reversed(snap[-n:]))

    def queries_by_user(self, user_id: str) -> list:
        """Return all entries for *user_id* (in insertion order)."""
        with self._lock:
            return [e for e in self._entries if e.user_id == user_id]

    def queries_for_query(self, query: str, case_sensitive: bool = False) -> list:
        """Return all entries whose ``query`` matches *query*."""
        needle = query if case_sensitive else query.lower()
        with self._lock:
            entries = list(self._entries)
        if case_sensitive:
            return [e for e in entries if e.query == needle]
        return [e for e in entries if e.query.lower() == needle]

    def zero_result_queries(self, limit: Optional[int] = None) -> list:
        """Return entries with ``result_count == 0``."""
        with self._lock:
            zeros = [e for e in self._entries if e.result_count == 0]
        if limit is not None and limit >= 0:
            return zeros[:limit]
        return zeros

    def count_query(self, query: str, case_sensitive: bool = False) -> int:
        """Return number of entries matching *query*."""
        return len(self.queries_for_query(query, case_sensitive=case_sensitive))

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def top_queries(
        self,
        top_k: int = 10,
        since: Optional[float] = None,
        now: float = 0.0,
    ) -> list:
        """Return the ``top_k`` most-frequent queries as ``(query, count)``.

        If *since* is given, only entries with ``timestamp >= since`` are
        considered.  ``now`` is accepted for API symmetry with other
        time-aware methods but is not used directly here.
        """
        del now  # unused, kept for symmetry
        with self._lock:
            entries = list(self._entries)
        counter: "Counter[str]" = Counter()
        for e in entries:
            if since is not None and e.timestamp < since:
                continue
            counter[e.query] += 1
        if top_k <= 0:
            return []
        return counter.most_common(top_k)

    def top_users(self, top_k: int = 10) -> list:
        """Return the ``top_k`` most active users as ``(user_id, count)``."""
        with self._lock:
            entries = list(self._entries)
        counter: "Counter[str]" = Counter()
        for e in entries:
            if e.user_id is None:
                continue
            counter[e.user_id] += 1
        if top_k <= 0:
            return []
        return counter.most_common(top_k)

    def click_through_rate(self, query: Optional[str] = None) -> float:
        """Fraction of (matching) entries that have a ``selected_result``.

        If *query* is given, the rate is computed only over entries with
        that exact query (case-insensitive).
        """
        with self._lock:
            entries = list(self._entries)
        if query is not None:
            needle = query.lower()
            entries = [e for e in entries if e.query.lower() == needle]
        if not entries:
            return 0.0
        clicked = sum(1 for e in entries if e.selected_result)
        return clicked / len(entries)

    def avg_results_for(self, query: str) -> float:
        """Average ``result_count`` for the given query (case-insensitive)."""
        entries = self.queries_for_query(query, case_sensitive=False)
        if not entries:
            return 0.0
        return sum(e.result_count for e in entries) / len(entries)

    def find_trends(
        self,
        recent_window: float = 86_400.0,
        older_window: float = 86_400.0,
        now: float = 0.0,
    ) -> list:
        """Return trends comparing a recent window with an older one.

        The "recent" window is ``[now - recent_window, now]`` and the
        "older" window is
        ``[now - recent_window - older_window, now - recent_window)``.
        """
        recent_start = now - recent_window
        older_start = recent_start - older_window
        with self._lock:
            entries = list(self._entries)

        recent: "Counter[str]" = Counter()
        older: "Counter[str]" = Counter()
        for e in entries:
            ts = e.timestamp
            if recent_start <= ts <= now:
                recent[e.query] += 1
            elif older_start <= ts < recent_start:
                older[e.query] += 1

        trends: list = []
        seen = set()
        for q, rc in recent.items():
            oc = older.get(q, 0)
            growth = (rc - oc) / max(oc, 1)
            trends.append(Trend(query=q, recent_count=rc, older_count=oc, growth_rate=growth))
            seen.add(q)
        for q, oc in older.items():
            if q in seen:
                continue
            growth = (0 - oc) / max(oc, 1)
            trends.append(Trend(query=q, recent_count=0, older_count=oc, growth_rate=growth))

        trends.sort(key=lambda t: t.growth_rate, reverse=True)
        return trends

    def stats(self, now: float = 0.0) -> QueryStats:
        """Return aggregate statistics over the whole log."""
        del now  # accepted for API symmetry
        with self._lock:
            entries = list(self._entries)
        total = len(entries)
        if total == 0:
            return QueryStats()
        query_counter: "Counter[str]" = Counter(e.query for e in entries)
        user_counter: "Counter[str]" = Counter(
            e.user_id for e in entries if e.user_id is not None
        )
        zero = sum(1 for e in entries if e.result_count == 0)
        avg_results = sum(e.result_count for e in entries) / total
        avg_latency = sum(e.latency_ms for e in entries) / total
        return QueryStats(
            total_queries=total,
            unique_queries=len(query_counter),
            zero_result_count=zero,
            avg_results=avg_results,
            avg_latency_ms=avg_latency,
            top_queries=query_counter.most_common(10),
            top_users=user_counter.most_common(10),
        )

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all entries (id counter is preserved)."""
        with self._lock:
            self._entries.clear()

    @property
    def total_queries(self) -> int:
        """Total number of entries currently stored."""
        with self._lock:
            return len(self._entries)

    def purge_older_than(self, older_than: float, now: float = 0.0) -> int:
        """Remove entries whose timestamp is older than ``now - older_than``.

        Returns the number of entries removed.
        """
        cutoff = now - older_than
        with self._lock:
            keep = [e for e in self._entries if e.timestamp >= cutoff]
            removed = len(self._entries) - len(keep)
            self._entries.clear()
            self._entries.extend(keep)
            return removed
