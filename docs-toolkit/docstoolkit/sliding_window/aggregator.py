"""WindowAggregator: bucketed sliding-window aggregation."""
import threading
import time


class WindowAggregator:
    """Sliding window split into fixed time buckets for cheap aggregation.

    The window of ``window_size`` seconds is divided into ``bucket_count``
    buckets of equal duration. Each bucket records ``[start_time, sum, count]``.
    Buckets older than ``now - window_size`` are considered expired and
    excluded from aggregates.
    """

    def __init__(self, window_size: float = 60.0, bucket_count: int = 10):
        if window_size <= 0:
            raise ValueError("window_size must be positive")
        if bucket_count <= 0:
            raise ValueError("bucket_count must be positive")
        self._window_size = float(window_size)
        self._bucket_count = int(bucket_count)
        self._bucket_duration = self._window_size / self._bucket_count
        # Each bucket is [start_time, sum, count]
        self._buckets: list[list] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _now(self, now: "float | None") -> float:
        return time.time() if now is None else now

    def _bucket_start(self, ts: float) -> float:
        """Quantise ``ts`` to the start of its bucket."""
        return (ts // self._bucket_duration) * self._bucket_duration

    def _evict(self, now: float) -> None:
        """Drop buckets whose start is at or before ``now - window_size``."""
        cutoff = now - self._window_size
        self._buckets = [b for b in self._buckets if b[0] > cutoff]

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def window_size(self) -> float:
        return self._window_size

    @property
    def bucket_count(self) -> int:
        return self._bucket_count

    def record(self, value: float = 1.0, now: "float | None" = None) -> None:
        """Add ``value`` to the bucket containing ``now``."""
        ts = self._now(now)
        bucket_start = self._bucket_start(ts)
        with self._lock:
            self._evict(ts)
            # Find existing bucket
            for bucket in self._buckets:
                if bucket[0] == bucket_start:
                    bucket[1] += float(value)
                    bucket[2] += 1
                    return
            # Create new bucket
            self._buckets.append([bucket_start, float(value), 1])

    def total(self, now: "float | None" = None) -> float:
        """Sum of values across non-expired buckets."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return sum(b[1] for b in self._buckets)

    def count(self, now: "float | None" = None) -> int:
        """Total number of recorded events across non-expired buckets."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return sum(b[2] for b in self._buckets)

    def rate(self, now: "float | None" = None) -> float:
        """Total per second (``total / window_size``)."""
        return self.total(now) / self._window_size

    def buckets(self, now: "float | None" = None) -> list[tuple[float, float, int]]:
        """Copy of non-expired buckets as (start, sum, count) tuples."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return [(b[0], b[1], b[2]) for b in self._buckets]

    def clear(self) -> None:
        """Remove all buckets."""
        with self._lock:
            self._buckets.clear()
