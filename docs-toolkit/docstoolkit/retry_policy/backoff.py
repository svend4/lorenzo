"""Backoff strategies for retry policy."""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import Enum


class BackoffStrategy(Enum):
    FIXED = "fixed"
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    JITTER = "jitter"


@dataclass
class BackoffConfig:
    strategy: BackoffStrategy = BackoffStrategy.EXPONENTIAL
    base_delay: float = 1.0
    max_delay: float = 60.0
    multiplier: float = 2.0
    jitter_range: float = 0.5


class BackoffCalculator:
    """Computes delay for a given retry attempt (0-based)."""

    def __init__(self, config: BackoffConfig | None = None) -> None:
        self.config = config if config is not None else BackoffConfig()

    def delay(self, attempt: int) -> float:
        """Return delay in seconds for the given 0-based attempt index."""
        cfg = self.config
        strategy = cfg.strategy

        if strategy is BackoffStrategy.FIXED:
            raw = cfg.base_delay

        elif strategy is BackoffStrategy.LINEAR:
            raw = cfg.base_delay * (attempt + 1)

        elif strategy is BackoffStrategy.EXPONENTIAL:
            raw = cfg.base_delay * (cfg.multiplier ** attempt)

        elif strategy is BackoffStrategy.JITTER:
            exp = cfg.base_delay * (cfg.multiplier ** attempt)
            noise = random.uniform(-cfg.jitter_range, cfg.jitter_range) * cfg.base_delay
            raw = max(0.0, exp + noise)

        else:  # pragma: no cover
            raw = cfg.base_delay

        return min(raw, cfg.max_delay)
