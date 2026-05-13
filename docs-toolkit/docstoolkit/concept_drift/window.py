"""Sliding window utilities for concept drift detection — pure stdlib."""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class WindowConfig:
    """Configuration for sliding window behaviour."""

    size: int = 50
    step: int = 10
    min_size: int = 10


@dataclass
class Window:
    """A snapshot of a contiguous slice of a data stream."""

    data: list
    start_idx: int
    end_idx: int

    def mean(self) -> float:
        """Arithmetic mean of the window data."""
        if not self.data:
            return 0.0
        return sum(self.data) / len(self.data)

    def variance(self) -> float:
        """Population variance of the window data."""
        if len(self.data) < 2:
            return 0.0
        mu = self.mean()
        return sum((x - mu) ** 2 for x in self.data) / len(self.data)

    def std(self) -> float:
        """Population standard deviation of the window data."""
        return math.sqrt(self.variance())

    def size(self) -> int:
        """Number of data points in the window."""
        return len(self.data)


class SlidingWindowBuffer:
    """Accumulates streaming values and emits complete windows at step boundaries."""

    def __init__(self, config: WindowConfig) -> None:
        self._config = config
        self._buffer: List[float] = []
        self._total: int = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def add(self, value: float) -> List[Window]:
        """Add *value* to the buffer.

        Returns a list of newly completed :class:`Window` objects.  A window
        is considered complete whenever the total number of added values
        crosses a step boundary *and* at least ``config.min_size`` values
        have been buffered.
        """
        self._buffer.append(value)
        self._total += 1

        windows: List[Window] = []

        # Emit a window when we hit a step boundary and have enough data
        if (
            self._total % self._config.step == 0
            and len(self._buffer) >= self._config.min_size
        ):
            # Take the last `size` values (or fewer if buffer is smaller)
            window_data = list(self._buffer[-self._config.size :])
            start = self._total - len(window_data)
            end = self._total - 1
            windows.append(Window(data=window_data, start_idx=start, end_idx=end))

            # Trim buffer to keep only the last `size` values
            if len(self._buffer) > self._config.size:
                self._buffer = self._buffer[-self._config.size :]

        return windows

    def current_window(self) -> Optional[Window]:
        """Return a :class:`Window` over all currently buffered data, or ``None``
        if the buffer holds fewer than ``min_size`` values."""
        if len(self._buffer) < self._config.min_size:
            return None
        data = list(self._buffer)
        start = self._total - len(data)
        end = self._total - 1
        return Window(data=data, start_idx=start, end_idx=end)

    def total_added(self) -> int:
        """Total number of values ever added to this buffer."""
        return self._total
