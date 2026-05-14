"""SlidingWindow: thread-safe time- or count-based sliding window."""
import threading
import time
from collections import deque
from dataclasses import dataclass
from enum import Enum


class WindowType(str, Enum):
    """Type of sliding window."""
    TIME = "time"
    COUNT = "count"


@dataclass
class WindowConfig:
    """Configuration for a SlidingWindow.

    Attributes:
        size: For TIME window, the duration in seconds. For COUNT window,
            the maximum number of items to retain.
        window_type: The type of window (TIME or COUNT).
    """
    size: float
    window_type: WindowType = WindowType.TIME


class SlidingWindow:
    """Thread-safe sliding window over (timestamp, value) pairs.

    For TIME windows, items with timestamp older than ``now - size`` are evicted.
    For COUNT windows, only the most recent ``size`` items are retained.
    """

    def __init__(self, config: WindowConfig):
        self._config = config
        self._items: "deque[tuple[float, float]]" = deque()
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _now(self, now: "float | None") -> float:
        return time.time() if now is None else now

    def _evict(self, now: float) -> None:
        """Remove items outside the window. Caller must hold the lock."""
        if self._config.window_type == WindowType.TIME:
            cutoff = now - self._config.size
            while self._items and self._items[0][0] <= cutoff:
                self._items.popleft()
        else:  # COUNT
            max_items = int(self._config.size)
            while len(self._items) > max_items:
                self._items.popleft()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, value: float = 1.0, now: "float | None" = None) -> None:
        """Append a value to the window with timestamp ``now``."""
        ts = self._now(now)
        with self._lock:
            self._items.append((ts, float(value)))
            self._evict(ts)

    def sum(self, now: "float | None" = None) -> float:
        """Total of values currently in the window."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return sum(v for _, v in self._items)

    def count(self, now: "float | None" = None) -> int:
        """Number of items currently in the window."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return len(self._items)

    def avg(self, now: "float | None" = None) -> float:
        """Average value in the window; 0.0 if empty."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            if not self._items:
                return 0.0
            total = sum(v for _, v in self._items)
            return total / len(self._items)

    def min(self, now: "float | None" = None) -> "float | None":
        """Minimum value in the window; ``None`` if empty."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            if not self._items:
                return None
            return min(v for _, v in self._items)

    def max(self, now: "float | None" = None) -> "float | None":
        """Maximum value in the window; ``None`` if empty."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            if not self._items:
                return None
            return max(v for _, v in self._items)

    def values(self, now: "float | None" = None) -> list[tuple[float, float]]:
        """Copy of (timestamp, value) pairs currently in the window."""
        ts = self._now(now)
        with self._lock:
            self._evict(ts)
            return list(self._items)

    def clear(self) -> None:
        """Remove all items from the window."""
        with self._lock:
            self._items.clear()
