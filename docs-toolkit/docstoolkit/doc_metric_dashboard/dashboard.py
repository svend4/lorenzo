"""Dashboard for aggregated document metrics.

Maintains a collection of :class:`MetricCard` instances (one per tracked
aggregate), per-card historical value series, and immutable
:class:`DashboardSnapshot` records captured at user-specified moments.

Storage:
    - ``_cards``: mapping ``card_id -> MetricCard``.
    - ``_snapshots``: mapping ``snapshot_id -> DashboardSnapshot``.
    - ``_history``: mapping ``card_id -> list[float]`` ordered oldest first.
    - :class:`threading.Lock` for safe concurrent mutation.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetricCard:
    """A single dashboard card with its current aggregate value."""

    card_id: str
    title: str
    value: float
    unit: str = ""
    trend: str = "flat"
    updated_at: float = 0.0


@dataclass
class DashboardSnapshot:
    """A snapshot of all card values captured at a single moment."""

    snapshot_id: str
    created_at: float = 0.0
    cards: dict = field(default_factory=dict)


@dataclass
class DashboardStats:
    """Aggregate statistics describing the dashboard's current state."""

    total_cards: int
    total_snapshots: int
    cards_up: int
    cards_down: int
    cards_flat: int


class DocMetricDashboard:
    """Thread-safe in-memory dashboard for aggregated document metrics."""

    def __init__(self) -> None:
        self._cards: dict = {}
        self._snapshots: dict = {}
        self._history: dict = {}
        self._lock = threading.Lock()

    # -------------------------------------------------------------------- cards

    def set_card(
        self,
        card_id: str,
        title: str,
        value: float,
        unit: str = "",
        now: Optional[float] = None,
    ) -> MetricCard:
        """Create or update a metric card; compute trend vs. previous value.

        First write for a ``card_id`` always yields ``trend="flat"``.
        Subsequent writes compare to the most recent historical value:
        greater than -> "up", less than -> "down", equal -> "flat".
        The new value is appended to that card's history.
        """
        ts = time.time() if now is None else float(now)
        new_value = float(value)
        with self._lock:
            history = self._history.get(card_id)
            if history:
                prev = history[-1]
                if new_value > prev:
                    trend = "up"
                elif new_value < prev:
                    trend = "down"
                else:
                    trend = "flat"
            else:
                trend = "flat"
                history = []
                self._history[card_id] = history
            card = MetricCard(
                card_id=card_id,
                title=title,
                value=new_value,
                unit=unit,
                trend=trend,
                updated_at=ts,
            )
            self._cards[card_id] = card
            history.append(new_value)
        return card

    def remove_card(self, card_id: str) -> bool:
        """Remove a card and its history; return ``True`` if removed."""
        with self._lock:
            if card_id not in self._cards:
                return False
            del self._cards[card_id]
            self._history.pop(card_id, None)
            return True

    def get_card(self, card_id: str) -> Optional[MetricCard]:
        """Return the :class:`MetricCard` for ``card_id`` or ``None``."""
        with self._lock:
            return self._cards.get(card_id)

    def list_cards(self) -> list:
        """Return all cards sorted by ``card_id``."""
        with self._lock:
            cards = list(self._cards.values())
        cards.sort(key=lambda c: c.card_id)
        return cards

    # ---------------------------------------------------------------- snapshots

    def take_snapshot(self, now: Optional[float] = None) -> DashboardSnapshot:
        """Capture current card values into an immutable snapshot."""
        ts = time.time() if now is None else float(now)
        snapshot_id = uuid.uuid4().hex
        with self._lock:
            cards = {cid: c.value for cid, c in self._cards.items()}
            snap = DashboardSnapshot(
                snapshot_id=snapshot_id,
                created_at=ts,
                cards=cards,
            )
            self._snapshots[snapshot_id] = snap
        return snap

    def get_snapshot(self, snapshot_id: str) -> Optional[DashboardSnapshot]:
        """Return snapshot by ID or ``None`` if unknown."""
        with self._lock:
            return self._snapshots.get(snapshot_id)

    def list_snapshots(self) -> list:
        """Return snapshots sorted by ``created_at`` descending."""
        with self._lock:
            snaps = list(self._snapshots.values())
        snaps.sort(key=lambda s: s.created_at, reverse=True)
        return snaps

    def delete_snapshot(self, snapshot_id: str) -> bool:
        """Delete a snapshot; return ``True`` if removed."""
        with self._lock:
            if snapshot_id not in self._snapshots:
                return False
            del self._snapshots[snapshot_id]
            return True

    # ------------------------------------------------------------------ history

    def history_for(
        self,
        card_id: str,
        limit: Optional[int] = None,
    ) -> list:
        """Return historical values for ``card_id``, most recent first."""
        if limit is not None and limit < 0:
            raise ValueError("limit must be non-negative")
        with self._lock:
            history = list(self._history.get(card_id, []))
        history.reverse()
        if limit is not None:
            history = history[:limit]
        return history

    def clear_history(self, card_id: str) -> int:
        """Clear history for ``card_id`` (keeping current card value).

        Returns the number of historical entries cleared.
        """
        with self._lock:
            history = self._history.get(card_id)
            if not history:
                return 0
            count = len(history)
            self._history[card_id] = []
            return count

    # ----------------------------------------------------------------- queries

    def cards_by_trend(self, trend: str) -> list:
        """Return cards matching ``trend`` sorted by ``card_id``."""
        with self._lock:
            matches = [c for c in self._cards.values() if c.trend == trend]
        matches.sort(key=lambda c: c.card_id)
        return matches

    # ------------------------------------------------------------------- stats

    def stats(self) -> DashboardStats:
        """Return :class:`DashboardStats` describing dashboard state."""
        with self._lock:
            cards = list(self._cards.values())
            total_snapshots = len(self._snapshots)
        up = sum(1 for c in cards if c.trend == "up")
        down = sum(1 for c in cards if c.trend == "down")
        flat = sum(1 for c in cards if c.trend == "flat")
        return DashboardStats(
            total_cards=len(cards),
            total_snapshots=total_snapshots,
            cards_up=up,
            cards_down=down,
            cards_flat=flat,
        )
