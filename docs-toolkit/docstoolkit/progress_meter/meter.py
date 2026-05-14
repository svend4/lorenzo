"""Multi-step progress tracking with ETA estimation and reporting."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class Phase:
    """Represents a single phase of progress tracking."""

    name: str
    weight: float = 1.0
    total: int = 0
    done: int = 0
    started_at: float = 0.0
    ended_at: float = 0.0

    @property
    def progress(self) -> float:
        """Fractional progress within this phase (0.0–1.0)."""
        if self.total <= 0:
            return 0.0
        ratio = self.done / self.total
        if ratio < 0.0:
            return 0.0
        if ratio > 1.0:
            return 1.0
        return ratio

    @property
    def is_complete(self) -> bool:
        """True when phase has been explicitly ended."""
        return self.ended_at > 0.0

    @property
    def duration(self) -> float:
        """Duration in seconds (0 if not ended)."""
        if self.ended_at <= 0.0 or self.started_at <= 0.0:
            return 0.0
        return max(0.0, self.ended_at - self.started_at)


@dataclass
class ProgressSnapshot:
    """Immutable snapshot of overall progress at a point in time."""

    overall_progress: float
    current_phase: Optional[str]
    phases: list
    eta_seconds: float
    elapsed_seconds: float
    rate_per_second: float


class ProgressMeter:
    """Tracks progress across multiple weighted phases."""

    def __init__(self) -> None:
        self._phases: dict = {}
        self._order: list = []
        self._current: Optional[str] = None
        self._started_at: float = 0.0
        self._last_now: float = 0.0
        self._subscribers: dict = {}
        self._next_sub_id: int = 1
        self._lock = threading.RLock()

    # ---------------- phase management ----------------

    def add_phase(self, name: str, total: int, weight: float = 1.0) -> Phase:
        """Register a new phase."""
        with self._lock:
            if name in self._phases:
                return self._phases[name]
            phase = Phase(name=name, total=total, weight=weight)
            self._phases[name] = phase
            self._order.append(name)
            return phase

    def start_phase(self, name: str, now: float = 0.0) -> Optional[Phase]:
        """Mark a phase as started, becoming the current phase."""
        with self._lock:
            phase = self._phases.get(name)
            if phase is None:
                return None
            if phase.started_at <= 0.0:
                phase.started_at = now
            self._current = name
            if self._started_at <= 0.0:
                self._started_at = now
            self._last_now = max(self._last_now, now)
            self._notify(now)
            return phase

    def update(self, name: str, done: int, now: float = 0.0) -> Optional[Phase]:
        """Set the done count for a phase."""
        with self._lock:
            phase = self._phases.get(name)
            if phase is None:
                return None
            if phase.started_at <= 0.0:
                phase.started_at = now
            if self._started_at <= 0.0:
                self._started_at = now
            value = done
            if value < 0:
                value = 0
            if phase.total > 0 and value > phase.total:
                value = phase.total
            phase.done = value
            self._current = name
            self._last_now = max(self._last_now, now)
            self._notify(now)
            return phase

    def increment(self, name: str, delta: int = 1, now: float = 0.0) -> Optional[Phase]:
        """Increment done by delta units."""
        with self._lock:
            phase = self._phases.get(name)
            if phase is None:
                return None
            return self.update(name, phase.done + delta, now=now)

    def complete_phase(self, name: str, now: float = 0.0) -> Optional[Phase]:
        """Mark a phase as complete (done = total, ended_at set)."""
        with self._lock:
            phase = self._phases.get(name)
            if phase is None:
                return None
            if phase.started_at <= 0.0:
                phase.started_at = now
            if phase.total > 0:
                phase.done = phase.total
            phase.ended_at = now if now > 0.0 else max(self._last_now, phase.started_at)
            if phase.ended_at <= 0.0:
                phase.ended_at = now
            self._last_now = max(self._last_now, now)
            if self._started_at <= 0.0:
                self._started_at = phase.started_at
            self._notify(now)
            return phase

    def current_phase(self) -> Optional[Phase]:
        """Return the currently active phase, if any."""
        with self._lock:
            if self._current is None:
                return None
            return self._phases.get(self._current)

    # ---------------- snapshot / reporting ----------------

    def snapshot(self, now: float = 0.0) -> ProgressSnapshot:
        """Compute an overall progress snapshot."""
        with self._lock:
            phases = [self._phases[n] for n in self._order]

            total_weight = sum(p.weight for p in phases)
            if total_weight > 0:
                overall = sum(p.progress * p.weight for p in phases) / total_weight
            else:
                overall = 0.0

            if overall < 0.0:
                overall = 0.0
            if overall > 1.0:
                overall = 1.0

            effective_now = now if now > 0.0 else self._last_now
            if effective_now > 0.0 and self._started_at > 0.0:
                elapsed = max(0.0, effective_now - self._started_at)
            else:
                elapsed = 0.0

            total_done = sum(p.done for p in phases)
            if elapsed > 0.0:
                rate = total_done / elapsed
            else:
                rate = 0.0

            if overall >= 1.0:
                eta = 0.0
            elif overall <= 0.0 or elapsed <= 0.0:
                eta = 0.0
            else:
                # Time-based ETA from weighted progress fraction
                eta = elapsed * (1.0 - overall) / overall

            current_name: Optional[str] = self._current
            if current_name is not None:
                cur_phase = self._phases.get(current_name)
                if cur_phase is not None and cur_phase.is_complete:
                    # Find next non-complete phase
                    nxt: Optional[str] = None
                    for n in self._order:
                        if not self._phases[n].is_complete:
                            nxt = n
                            break
                    current_name = nxt

            return ProgressSnapshot(
                overall_progress=overall,
                current_phase=current_name,
                phases=list(phases),
                eta_seconds=eta,
                elapsed_seconds=elapsed,
                rate_per_second=rate,
            )

    def format(self, now: float = 0.0) -> str:
        """Render a human-readable progress line."""
        snap = self.snapshot(now=now)
        bar_width = 10
        filled = int(round(snap.overall_progress * bar_width))
        if filled < 0:
            filled = 0
        if filled > bar_width:
            filled = bar_width
        bar = "█" * filled + "░" * (bar_width - filled)
        pct = int(round(snap.overall_progress * 100))

        if snap.current_phase is not None:
            phase = self._phases.get(snap.current_phase)
            if phase is not None:
                phase_part = (
                    f"Phase '{phase.name}' ({phase.done}/{phase.total})"
                )
            else:
                phase_part = f"Phase '{snap.current_phase}'"
        else:
            phase_part = "No active phase"

        eta_part = f"ETA: {self._format_seconds(snap.eta_seconds)}"
        return f"[{bar}] {pct}% {phase_part} {eta_part}"

    @staticmethod
    def _format_seconds(seconds: float) -> str:
        if seconds <= 0:
            return "0s"
        total = int(round(seconds))
        if total < 60:
            return f"{total}s"
        minutes, sec = divmod(total, 60)
        if minutes < 60:
            return f"{minutes}m{sec}s" if sec else f"{minutes}m"
        hours, minutes = divmod(minutes, 60)
        return f"{hours}h{minutes}m"

    # ---------------- state queries ----------------

    def is_complete(self) -> bool:
        """True when every phase is complete."""
        with self._lock:
            if not self._phases:
                return False
            return all(p.is_complete for p in self._phases.values())

    def reset(self) -> None:
        """Clear all phases and subscribers state."""
        with self._lock:
            self._phases.clear()
            self._order.clear()
            self._current = None
            self._started_at = 0.0
            self._last_now = 0.0

    @property
    def phase_count(self) -> int:
        """Number of registered phases."""
        with self._lock:
            return len(self._phases)

    # ---------------- subscriptions ----------------

    def subscribe(self, callback: Callable[[ProgressSnapshot], None]) -> int:
        """Register a callback invoked on each progress update."""
        with self._lock:
            sub_id = self._next_sub_id
            self._next_sub_id += 1
            self._subscribers[sub_id] = callback
            return sub_id

    def unsubscribe(self, sub_id: int) -> bool:
        """Remove a previously registered callback."""
        with self._lock:
            return self._subscribers.pop(sub_id, None) is not None

    def _notify(self, now: float) -> None:
        if not self._subscribers:
            return
        snap = self.snapshot(now=now)
        for cb in list(self._subscribers.values()):
            try:
                cb(snap)
            except Exception:
                # Subscribers must not break the meter
                pass
