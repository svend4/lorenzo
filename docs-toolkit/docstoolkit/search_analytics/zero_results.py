from dataclasses import dataclass, field

@dataclass
class ZeroResultAlert:
    query: str
    occurrence_count: int
    last_seen_ts: str
    severity: str    # "low" (1-2x), "medium" (3-9x), "high" (10+x)

    def is_high_severity(self) -> bool:
        return self.severity == "high"


class ZeroResultMonitor:
    """Monitors and alerts on zero-result queries."""

    def __init__(self, low_threshold: int = 1, high_threshold: int = 10):
        self.low_threshold = low_threshold
        self.high_threshold = high_threshold

    def scan(self, tracker) -> list:
        """Return list[ZeroResultAlert] for zero-result queries.

        For each (query, count) from tracker.zero_result_queries():
          severity = "high" if count >= high_threshold else
                     "medium" if count >= 3 else "low"
          last_seen_ts: query the DB for most recent ts of this zero-result query

        Return sorted by occurrence_count desc.
        """
        alerts = []
        pairs = tracker.zero_result_queries()
        for query, count in pairs:
            # Get last seen ts
            row = tracker._conn.execute(
                "SELECT ts FROM query_log WHERE query=? AND result_count=0 "
                "ORDER BY ts DESC LIMIT 1",
                (query,)
            ).fetchone()
            last_ts = row["ts"] if row else ""

            if count >= self.high_threshold:
                severity = "high"
            elif count >= 3:
                severity = "medium"
            else:
                severity = "low"

            alerts.append(ZeroResultAlert(
                query=query,
                occurrence_count=count,
                last_seen_ts=last_ts,
                severity=severity,
            ))

        return sorted(alerts, key=lambda a: -a.occurrence_count)
