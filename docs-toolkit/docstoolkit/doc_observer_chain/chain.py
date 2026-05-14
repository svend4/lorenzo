"""E411 DocObserverChain — chained observer notifications for doc events.

Observers are registered against a specific ``event_type`` and invoked
in order (lower ``order`` first, ties broken by ``observer_id``). Each
callback receives the current (possibly merged) payload, and may return
a ``dict`` whose entries are merged into the payload before the next
observer sees it (chain semantics). Exceptions from callbacks are
recorded as errors and do not interrupt the chain.

This module is intentionally stdlib-only and thread-safe.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Observer:
    """A registered observer in the chain."""

    observer_id: str
    event_type: str
    callback: object = None
    order: int = 0
    enabled: bool = True


@dataclass
class NotifyResult:
    """Outcome of notifying observers for a single event."""

    event_type: str
    doc_id: str
    observers_invoked: List[str] = field(default_factory=list)
    final_payload: dict = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)


@dataclass
class ChainStats:
    """Aggregate statistics for a :class:`DocObserverChain`."""

    total_observers: int
    enabled_observers: int
    total_notifications: int
    total_callbacks: int
    total_errors: int


class DocObserverChain:
    """Manage and notify ordered observers for document events."""

    def __init__(self) -> None:
        self._observers: Dict[str, Observer] = {}
        self._total_notifications: int = 0
        self._total_callbacks: int = 0
        self._total_errors: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register_observer(
        self,
        event_type: str,
        callback,
        order: int = 0,
    ) -> Observer:
        """Register a new observer for ``event_type``.

        ``callback`` must be callable as ``callback(event_type, doc_id, payload)``.
        Returns the freshly-created :class:`Observer`.
        """
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("event_type must be a non-empty string")
        if not callable(callback):
            raise ValueError("callback must be callable")
        if not isinstance(order, int):
            raise ValueError("order must be an int")
        observer_id = uuid.uuid4().hex
        observer = Observer(
            observer_id=observer_id,
            event_type=event_type,
            callback=callback,
            order=order,
            enabled=True,
        )
        with self._lock:
            self._observers[observer_id] = observer
        return observer

    def unregister_observer(self, observer_id: str) -> bool:
        with self._lock:
            if observer_id in self._observers:
                del self._observers[observer_id]
                return True
            return False

    def enable_observer(self, observer_id: str) -> bool:
        with self._lock:
            obs = self._observers.get(observer_id)
            if obs is None:
                return False
            obs.enabled = True
            return True

    def disable_observer(self, observer_id: str) -> bool:
        with self._lock:
            obs = self._observers.get(observer_id)
            if obs is None:
                return False
            obs.enabled = False
            return True

    def get_observer(self, observer_id: str) -> Optional[Observer]:
        with self._lock:
            return self._observers.get(observer_id)

    def list_observers(self, event_type: Optional[str] = None) -> List[Observer]:
        """List all observers, optionally filtered by ``event_type``.

        Returned list is sorted by ``(order, observer_id)``.
        """
        with self._lock:
            if event_type is None:
                items = list(self._observers.values())
            else:
                items = [o for o in self._observers.values() if o.event_type == event_type]
        items.sort(key=lambda o: (o.order, o.observer_id))
        return items

    def clear_observers(self) -> int:
        """Remove all observers; return the number cleared."""
        with self._lock:
            n = len(self._observers)
            self._observers.clear()
            return n

    # ------------------------------------------------------------------
    # Notification
    # ------------------------------------------------------------------
    def notify(
        self,
        event_type: str,
        doc_id: str,
        payload: Optional[dict] = None,
    ) -> NotifyResult:
        """Notify all enabled observers registered for ``event_type``.

        Observers are collected under the lock and invoked OUTSIDE the
        lock in deterministic order. Each callback receives the current
        (possibly merged) payload. If a callback returns a ``dict`` its
        entries are merged into the payload before the next observer
        sees it. Exceptions are captured as error strings and processing
        continues.
        """
        if not isinstance(event_type, str) or not event_type:
            raise ValueError("event_type must be a non-empty string")
        if not isinstance(doc_id, str) or not doc_id:
            raise ValueError("doc_id must be a non-empty string")
        if payload is None:
            current_payload: dict = {}
        elif isinstance(payload, dict):
            current_payload = dict(payload)
        else:
            raise TypeError("payload must be a dict or None")

        # Collect a stable snapshot of enabled matching observers.
        with self._lock:
            self._total_notifications += 1
            snapshot = [
                o
                for o in self._observers.values()
                if o.event_type == event_type and o.enabled
            ]
        snapshot.sort(key=lambda o: (o.order, o.observer_id))

        result = NotifyResult(
            event_type=event_type,
            doc_id=doc_id,
            final_payload=current_payload,
            observers_invoked=[],
            errors=[],
        )

        callbacks_run = 0
        errors_count = 0

        for obs in snapshot:
            callbacks_run += 1
            result.observers_invoked.append(obs.observer_id)
            try:
                returned = obs.callback(event_type, doc_id, current_payload)
            except Exception as exc:  # noqa: BLE001 — observer-level boundary
                errors_count += 1
                result.errors.append(
                    f"{obs.observer_id}: {type(exc).__name__}: {exc}"
                )
                continue
            if returned is None:
                continue
            if isinstance(returned, dict):
                current_payload.update(returned)
                continue
            # Non-dict, non-None return: treat as a programming error
            # but do not break the chain.
            errors_count += 1
            result.errors.append(
                f"{obs.observer_id}: TypeError: callback returned non-dict "
                f"{type(returned).__name__}"
            )

        result.final_payload = current_payload

        # Update aggregate counters under lock.
        with self._lock:
            self._total_callbacks += callbacks_run
            self._total_errors += errors_count

        return result

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------
    def stats(self) -> ChainStats:
        with self._lock:
            total = len(self._observers)
            enabled = sum(1 for o in self._observers.values() if o.enabled)
            return ChainStats(
                total_observers=total,
                enabled_observers=enabled,
                total_notifications=self._total_notifications,
                total_callbacks=self._total_callbacks,
                total_errors=self._total_errors,
            )


__all__ = [
    "ChainStats",
    "DocObserverChain",
    "NotifyResult",
    "Observer",
]
