"""Enhanced in-memory access log with aggregation, anomaly detection, and IP block list."""
import threading
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Deque, Dict, List, Optional, Set


class AccessLevel(Enum):
    """Severity level associated with an access entry."""

    INFO = "info"
    WARN = "warn"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AccessEntry:
    """Represents a single access-log record."""

    entry_id: int = 0
    subject: str = ""
    action: str = ""
    resource: str = ""
    ip_address: Optional[str] = None
    level: AccessLevel = AccessLevel.INFO
    success: bool = True
    timestamp: float = 0.0
    details: dict = field(default_factory=dict)


@dataclass
class Anomaly:
    """Anomalous behaviour detected on the log."""

    anomaly_type: str  # "high_freq", "many_failures", "unusual_resource"
    subject: str
    count: int
    time_window: float
    severity: AccessLevel


class AccessLogV2:
    """Thread-safe, bounded, in-memory access log with anomaly detection.

    Parameters
    ----------
    max_entries:
        Maximum number of retained entries.  When exceeded, the oldest
        entry is evicted (FIFO).
    """

    def __init__(self, max_entries: int = 10000) -> None:
        self._max_entries: int = int(max_entries)
        self._entries: Deque[AccessEntry] = deque(maxlen=self._max_entries)
        self._lock = threading.Lock()
        self._next_id: int = 1
        # Track *all* resources ever accessed per subject, even after eviction,
        # so that "unusual_resource" detection has a stable historical view.
        self._subject_resources: Dict[str, Set[str]] = defaultdict(set)
        self._blocked_ips: Set[str] = set()
        self._block_reasons: Dict[str, Optional[str]] = {}

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    def log(
        self,
        subject: str,
        action: str,
        resource: str,
        ip_address: Optional[str] = None,
        level: AccessLevel = AccessLevel.INFO,
        success: bool = True,
        now: float = 0.0,
        **details,
    ) -> AccessEntry:
        """Record an access entry and return it."""
        with self._lock:
            entry = AccessEntry(
                entry_id=self._next_id,
                subject=subject,
                action=action,
                resource=resource,
                ip_address=ip_address,
                level=level,
                success=success,
                timestamp=now,
                details=dict(details),
            )
            self._next_id += 1
            self._entries.append(entry)
            self._subject_resources[subject].add(resource)
            return entry

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def query(
        self,
        subject: Optional[str] = None,
        action: Optional[str] = None,
        resource: Optional[str] = None,
        level: Optional[AccessLevel] = None,
        success: Optional[bool] = None,
        ip: Optional[str] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
        limit: Optional[int] = None,
    ) -> List[AccessEntry]:
        """Return entries matching all provided filters (in insertion order)."""
        with self._lock:
            results: List[AccessEntry] = []
            for entry in self._entries:
                if subject is not None and entry.subject != subject:
                    continue
                if action is not None and entry.action != action:
                    continue
                if resource is not None and entry.resource != resource:
                    continue
                if level is not None and entry.level != level:
                    continue
                if success is not None and entry.success != success:
                    continue
                if ip is not None and entry.ip_address != ip:
                    continue
                if start is not None and entry.timestamp < start:
                    continue
                if end is not None and entry.timestamp > end:
                    continue
                results.append(entry)
                if limit is not None and len(results) >= limit:
                    break
            return results

    def count(
        self,
        subject: Optional[str] = None,
        success: Optional[bool] = None,
        start: Optional[float] = None,
        end: Optional[float] = None,
    ) -> int:
        """Return number of entries matching the given filters."""
        with self._lock:
            total = 0
            for entry in self._entries:
                if subject is not None and entry.subject != subject:
                    continue
                if success is not None and entry.success != success:
                    continue
                if start is not None and entry.timestamp < start:
                    continue
                if end is not None and entry.timestamp > end:
                    continue
                total += 1
            return total

    def recent(self, n: int = 10) -> List[AccessEntry]:
        """Return the last *n* entries in chronological order."""
        if n <= 0:
            return []
        with self._lock:
            if n >= len(self._entries):
                return list(self._entries)
            # deque supports negative indexing via list slice on the copy
            return list(self._entries)[-n:]

    def latest_for_subject(self, subject: str) -> Optional[AccessEntry]:
        """Return the most recent entry for *subject*, or ``None``."""
        with self._lock:
            for entry in reversed(self._entries):
                if entry.subject == subject:
                    return entry
            return None

    # ------------------------------------------------------------------
    # IP block list
    # ------------------------------------------------------------------

    def block_ip(self, ip: str, reason: Optional[str] = None) -> None:
        """Add *ip* to the block list."""
        with self._lock:
            self._blocked_ips.add(ip)
            self._block_reasons[ip] = reason

    def unblock_ip(self, ip: str) -> bool:
        """Remove *ip* from the block list. Returns ``True`` if it was blocked."""
        with self._lock:
            if ip in self._blocked_ips:
                self._blocked_ips.discard(ip)
                self._block_reasons.pop(ip, None)
                return True
            return False

    def is_blocked(self, ip: str) -> bool:
        """Return whether *ip* is currently blocked."""
        with self._lock:
            return ip in self._blocked_ips

    def blocked_ips(self) -> List[str]:
        """Return the current list of blocked IPs (sorted)."""
        with self._lock:
            return sorted(self._blocked_ips)

    # ------------------------------------------------------------------
    # Anomaly detection
    # ------------------------------------------------------------------

    def detect_anomalies(
        self,
        time_window: float = 300.0,
        now: float = 0.0,
        high_freq_threshold: int = 100,
        failure_threshold: int = 10,
    ) -> List[Anomaly]:
        """Detect anomalies within ``[now - time_window, now]``.

        Three families of anomalies are emitted:

        * ``high_freq`` — subject performed more than ``high_freq_threshold``
          actions inside the window.
        * ``many_failures`` — subject accumulated more than
          ``failure_threshold`` failures inside the window.
        * ``unusual_resource`` — subject accessed, inside the window, a
          resource they had never touched *before* the window started.
        """
        anomalies: List[Anomaly] = []
        start = now - time_window
        with self._lock:
            in_window_counts: Counter = Counter()
            failure_counts: Counter = Counter()
            historical_resources: Dict[str, Set[str]] = defaultdict(set)
            window_resources: Dict[str, Set[str]] = defaultdict(set)

            for entry in self._entries:
                if entry.timestamp < start:
                    historical_resources[entry.subject].add(entry.resource)
                    continue
                if entry.timestamp > now:
                    # Future entries (relative to ``now``) are ignored.
                    continue
                in_window_counts[entry.subject] += 1
                if not entry.success:
                    failure_counts[entry.subject] += 1
                window_resources[entry.subject].add(entry.resource)

            for subject, cnt in in_window_counts.items():
                if cnt > high_freq_threshold:
                    anomalies.append(
                        Anomaly(
                            anomaly_type="high_freq",
                            subject=subject,
                            count=cnt,
                            time_window=time_window,
                            severity=AccessLevel.WARN,
                        )
                    )

            for subject, cnt in failure_counts.items():
                if cnt > failure_threshold:
                    anomalies.append(
                        Anomaly(
                            anomaly_type="many_failures",
                            subject=subject,
                            count=cnt,
                            time_window=time_window,
                            severity=AccessLevel.ERROR,
                        )
                    )

            for subject, resources in window_resources.items():
                # New resources are those accessed in window but never before
                # the window — either in history within retained entries or in
                # the long-lived ``_subject_resources`` map filtered down.
                history = historical_resources.get(subject, set())
                new_resources = resources - history
                if new_resources:
                    anomalies.append(
                        Anomaly(
                            anomaly_type="unusual_resource",
                            subject=subject,
                            count=len(new_resources),
                            time_window=time_window,
                            severity=AccessLevel.WARN,
                        )
                    )

        return anomalies

    # ------------------------------------------------------------------
    # Aggregations
    # ------------------------------------------------------------------

    def aggregate_by_subject(self) -> Dict[str, int]:
        """Return ``{subject: count}`` over all retained entries."""
        with self._lock:
            counter: Counter = Counter(e.subject for e in self._entries)
            return dict(counter)

    def aggregate_by_action(self) -> Dict[str, int]:
        """Return ``{action: count}`` over all retained entries."""
        with self._lock:
            counter: Counter = Counter(e.action for e in self._entries)
            return dict(counter)

    def aggregate_by_resource(self) -> Dict[str, int]:
        """Return ``{resource: count}`` over all retained entries."""
        with self._lock:
            counter: Counter = Counter(e.resource for e in self._entries)
            return dict(counter)

    def success_rate(self, subject: Optional[str] = None) -> float:
        """Return the success ratio in ``[0.0, 1.0]``.

        For an empty log (or empty subset), the function returns ``0.0``.
        """
        with self._lock:
            total = 0
            wins = 0
            for entry in self._entries:
                if subject is not None and entry.subject != subject:
                    continue
                total += 1
                if entry.success:
                    wins += 1
            if total == 0:
                return 0.0
            return wins / total

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def clear(self) -> None:
        """Remove all entries (block list and history are preserved)."""
        with self._lock:
            self._entries.clear()

    @property
    def total_entries(self) -> int:
        """Number of entries currently retained."""
        with self._lock:
            return len(self._entries)

    def purge_older_than(self, older_than: float, now: float = 0.0) -> int:
        """Drop entries whose ``timestamp < now - older_than``.

        Returns the number of entries that were removed.
        """
        cutoff = now - older_than
        with self._lock:
            kept = [e for e in self._entries if e.timestamp >= cutoff]
            removed = len(self._entries) - len(kept)
            self._entries.clear()
            self._entries.extend(kept)
            return removed
