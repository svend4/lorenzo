from dataclasses import dataclass, field
from datetime import datetime, timedelta

@dataclass
class QueryTrend:
    query: str
    count_recent: int      # count in recent window
    count_previous: int    # count in previous window
    change_pct: float      # (recent - previous) / previous * 100, or 0 if previous=0

    def is_rising(self) -> bool:
        return self.change_pct > 10.0

    def is_falling(self) -> bool:
        return self.change_pct < -10.0

@dataclass
class TrendReport:
    window_hours: int
    rising: list = field(default_factory=list)    # list[QueryTrend]
    falling: list = field(default_factory=list)   # list[QueryTrend]
    new_queries: list = field(default_factory=list)  # appeared in recent, 0 in previous

    def total_trends(self) -> int:
        return len(self.rising) + len(self.falling) + len(self.new_queries)


class TrendAnalyzer:
    """Analyzes query trends from QueryTracker."""

    def analyze(
        self,
        tracker,                    # QueryTracker
        window_hours: int = 24,
    ) -> TrendReport:
        """Compare recent window vs previous window of same duration.

        Recent: now - window_hours to now
        Previous: now - 2*window_hours to now - window_hours

        For each query: compute count in each window.
        Rising: count_recent > count_previous * 1.1 (and count_recent > 0)
        Falling: count_recent < count_previous * 0.9 (and count_previous > 0)
        New: count_previous = 0 and count_recent > 0

        Use SQLite query directly: tracker._conn.execute(...)
        """
        now = datetime.now()
        recent_start = (now - timedelta(hours=window_hours)).isoformat(timespec='seconds')
        prev_start = (now - timedelta(hours=window_hours * 2)).isoformat(timespec='seconds')
        prev_end = recent_start

        # Count per query in recent window
        recent_rows = tracker._conn.execute(
            "SELECT query, COUNT(*) as cnt FROM query_log "
            "WHERE ts >= ? GROUP BY query",
            (recent_start,)
        ).fetchall()
        recent_counts = {r["query"]: r["cnt"] for r in recent_rows}

        # Count per query in previous window
        prev_rows = tracker._conn.execute(
            "SELECT query, COUNT(*) as cnt FROM query_log "
            "WHERE ts >= ? AND ts < ? GROUP BY query",
            (prev_start, prev_end)
        ).fetchall()
        prev_counts = {r["query"]: r["cnt"] for r in prev_rows}

        all_queries = set(recent_counts) | set(prev_counts)
        rising, falling, new_queries = [], [], []

        for q in all_queries:
            rc = recent_counts.get(q, 0)
            pc = prev_counts.get(q, 0)
            change_pct = (rc - pc) / pc * 100 if pc > 0 else 0.0
            trend = QueryTrend(q, rc, pc, change_pct)

            if pc == 0 and rc > 0:
                new_queries.append(trend)
            elif trend.is_rising():
                rising.append(trend)
            elif trend.is_falling():
                falling.append(trend)

        return TrendReport(
            window_hours=window_hours,
            rising=rising,
            falling=falling,
            new_queries=new_queries,
        )
