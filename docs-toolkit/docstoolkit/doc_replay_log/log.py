"""E361 DocReplayLog — replay event log for state reconstruction.

Pure stdlib implementation, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class ReplayEvent:
    """A single event in the replay log."""

    event_id: int
    stream_id: str
    event_type: str
    payload: dict = field(default_factory=dict)
    recorded_at: float = 0.0


@dataclass
class Checkpoint:
    """A named checkpoint for fast-forward replay."""

    name: str
    event_id: int
    created_at: float = 0.0


@dataclass
class ReplayStats:
    """Aggregate statistics about a :class:`DocReplayLog`."""

    total_events: int
    unique_streams: int
    unique_event_types: int
    checkpoint_count: int


class DocReplayLog:
    """Replay-style append-only event log.

    Stores events in a global ordered list with secondary per-stream indices
    for efficient stream replay.
    """

    def __init__(self) -> None:
        self._events: List[ReplayEvent] = []
        self._by_stream: Dict[str, List[int]] = {}
        self._checkpoints: Dict[str, Checkpoint] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Append / lookup
    # ------------------------------------------------------------------
    def append(
        self,
        stream_id: str,
        event_type: str,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> ReplayEvent:
        """Append a new event to the log and return it."""
        if not isinstance(stream_id, str) or not stream_id:
            raise ValueError("stream_id must be a non-empty string")
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("event_type must be a non-empty string")
        if payload is None:
            payload = {}
        if not isinstance(payload, dict):
            raise TypeError("payload must be a dict")
        ts = now if now is not None else time.time()

        with self._lock:
            event = ReplayEvent(
                event_id=self._next_id,
                stream_id=stream_id,
                event_type=event_type,
                payload=dict(payload),
                recorded_at=ts,
            )
            self._next_id += 1
            idx = len(self._events)
            self._events.append(event)
            self._by_stream.setdefault(stream_id, []).append(idx)
            return event

    def get_event(self, event_id: int) -> Optional[ReplayEvent]:
        """Return the event with the given id or :data:`None`."""
        with self._lock:
            # Linear scan is fine; ids are monotonic so we could binary-search,
            # but truncation may leave gaps so be safe.
            for ev in self._events:
                if ev.event_id == event_id:
                    return ev
            return None

    # ------------------------------------------------------------------
    # Replay
    # ------------------------------------------------------------------
    def replay_stream(
        self,
        stream_id: str,
        from_event_id: int = 1,
        limit: Optional[int] = None,
    ) -> List[ReplayEvent]:
        """Return events for ``stream_id`` with ``event_id >= from_event_id``."""
        with self._lock:
            indices = self._by_stream.get(stream_id, [])
            out: List[ReplayEvent] = []
            for i in indices:
                ev = self._events[i]
                if ev.event_id >= from_event_id:
                    out.append(ev)
            out.sort(key=lambda e: e.event_id)
            if limit is not None:
                out = out[:limit]
            return out

    def replay_all(
        self,
        from_event_id: int = 1,
        limit: Optional[int] = None,
    ) -> List[ReplayEvent]:
        """Return all events with ``event_id >= from_event_id`` sorted asc."""
        with self._lock:
            out = [ev for ev in self._events if ev.event_id >= from_event_id]
            out.sort(key=lambda e: e.event_id)
            if limit is not None:
                out = out[:limit]
            return out

    def replay_to(
        self,
        callback: Callable[[ReplayEvent], None],
        from_event_id: int = 1,
        stream_id: Optional[str] = None,
        until_event_id: Optional[int] = None,
    ) -> int:
        """Invoke ``callback`` for each matching event, return how many."""
        if callback is None or not callable(callback):
            raise TypeError("callback must be callable")
        with self._lock:
            if stream_id is not None:
                events = [self._events[i] for i in self._by_stream.get(stream_id, [])]
            else:
                events = list(self._events)
        events.sort(key=lambda e: e.event_id)
        count = 0
        for ev in events:
            if ev.event_id < from_event_id:
                continue
            if until_event_id is not None and ev.event_id > until_event_id:
                continue
            callback(ev)
            count += 1
        return count

    # ------------------------------------------------------------------
    # Checkpoints
    # ------------------------------------------------------------------
    def create_checkpoint(
        self, name: str, now: Optional[float] = None
    ) -> Checkpoint:
        """Create a checkpoint at the current latest event id."""
        if not isinstance(name, str) or not name:
            raise ValueError("checkpoint name must be a non-empty string")
        ts = now if now is not None else time.time()
        with self._lock:
            last_id = self._events[-1].event_id if self._events else 0
            cp = Checkpoint(name=name, event_id=last_id, created_at=ts)
            self._checkpoints[name] = cp
            return cp

    def get_checkpoint(self, name: str) -> Optional[Checkpoint]:
        """Return the checkpoint with the given name or :data:`None`."""
        with self._lock:
            return self._checkpoints.get(name)

    def delete_checkpoint(self, name: str) -> bool:
        """Delete a checkpoint. Returns :data:`True` if it existed."""
        with self._lock:
            return self._checkpoints.pop(name, None) is not None

    def replay_from_checkpoint(
        self, name: str, callback: Callable[[ReplayEvent], None]
    ) -> int:
        """Replay events recorded after the named checkpoint."""
        if callback is None or not callable(callback):
            raise TypeError("callback must be callable")
        with self._lock:
            cp = self._checkpoints.get(name)
            if cp is None:
                raise KeyError(f"checkpoint not found: {name}")
            target_after = cp.event_id
            events = sorted(
                (ev for ev in self._events if ev.event_id > target_after),
                key=lambda e: e.event_id,
            )
        count = 0
        for ev in events:
            callback(ev)
            count += 1
        return count

    def list_checkpoints(self) -> List[Checkpoint]:
        """Return checkpoints sorted by event_id descending."""
        with self._lock:
            cps = list(self._checkpoints.values())
        cps.sort(key=lambda c: c.event_id, reverse=True)
        return cps

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------
    def events_by_type(
        self, event_type: str, limit: Optional[int] = None
    ) -> List[ReplayEvent]:
        """Return all events of a given type, sorted by event_id."""
        with self._lock:
            out = [ev for ev in self._events if ev.event_type == event_type]
        out.sort(key=lambda e: e.event_id)
        if limit is not None:
            out = out[:limit]
        return out

    def truncate_before(self, event_id: int) -> int:
        """Remove events with ``event_id < event_id``. Returns count removed."""
        with self._lock:
            keep: List[ReplayEvent] = []
            removed = 0
            for ev in self._events:
                if ev.event_id < event_id:
                    removed += 1
                else:
                    keep.append(ev)
            self._events = keep
            # Rebuild secondary index
            self._by_stream = {}
            for i, ev in enumerate(self._events):
                self._by_stream.setdefault(ev.stream_id, []).append(i)
            return removed

    def stats(self) -> ReplayStats:
        """Return aggregate statistics."""
        with self._lock:
            streams = {ev.stream_id for ev in self._events}
            types = {ev.event_type for ev in self._events}
            return ReplayStats(
                total_events=len(self._events),
                unique_streams=len(streams),
                unique_event_types=len(types),
                checkpoint_count=len(self._checkpoints),
            )
