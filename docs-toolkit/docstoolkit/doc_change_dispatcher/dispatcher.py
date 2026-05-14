"""E405 DocChangeDispatcher implementation.

Pure stdlib, thread-safe dispatcher that delivers document change events to
registered handlers. Callbacks fire OUTSIDE the internal lock to avoid
deadlocks and contention.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Handler:
    """A registered handler."""

    handler_id: str
    change_type: str
    callback: object = None
    priority: int = 0
    enabled: bool = True


@dataclass
class DispatchResult:
    """Outcome of dispatching one change."""

    doc_id: str
    change_type: str
    delivered_count: int = 0
    failed_count: int = 0
    handlers_invoked: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass
class DispatcherStats:
    """Aggregate statistics for the dispatcher."""

    total_handlers: int
    enabled_handlers: int
    total_dispatches: int
    total_deliveries: int
    total_failures: int


class DocChangeDispatcher:
    """Thread-safe dispatcher for document change events.

    Handlers are registered against an exact ``change_type`` or the wildcard
    ``"*"`` which matches every change type. Higher ``priority`` values are
    invoked first. Handler callbacks are executed OUTSIDE the internal lock
    so that long-running or recursive callbacks do not block other operations.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._handlers: dict[str, Handler] = {}
        self._total_dispatches: int = 0
        self._total_deliveries: int = 0
        self._total_failures: int = 0

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------
    def register_handler(
        self,
        change_type: str,
        callback,
        priority: int = 0,
    ) -> Handler:
        """Register a new handler. Returns the Handler object."""
        handler = Handler(
            handler_id=uuid.uuid4().hex,
            change_type=change_type,
            callback=callback,
            priority=priority,
            enabled=True,
        )
        with self._lock:
            self._handlers[handler.handler_id] = handler
        return handler

    def unregister_handler(self, handler_id: str) -> bool:
        """Remove a handler. Returns True if it existed."""
        with self._lock:
            if handler_id in self._handlers:
                del self._handlers[handler_id]
                return True
            return False

    def enable_handler(self, handler_id: str) -> bool:
        """Enable a handler. Returns True if it existed."""
        with self._lock:
            h = self._handlers.get(handler_id)
            if h is None:
                return False
            h.enabled = True
            return True

    def disable_handler(self, handler_id: str) -> bool:
        """Disable a handler. Returns True if it existed."""
        with self._lock:
            h = self._handlers.get(handler_id)
            if h is None:
                return False
            h.enabled = False
            return True

    def get_handler(self, handler_id: str) -> Optional[Handler]:
        """Look up a handler by id."""
        with self._lock:
            return self._handlers.get(handler_id)

    def list_handlers(self) -> list[Handler]:
        """All handlers sorted by (-priority, handler_id)."""
        with self._lock:
            handlers = list(self._handlers.values())
        handlers.sort(key=lambda h: (-h.priority, h.handler_id))
        return handlers

    # ------------------------------------------------------------------
    # Matching
    # ------------------------------------------------------------------
    def matching_handlers(self, change_type: str) -> list[Handler]:
        """Enabled handlers matching change_type, sorted by priority (desc)."""
        with self._lock:
            matched = [
                h
                for h in self._handlers.values()
                if h.enabled and (h.change_type == change_type or h.change_type == "*")
            ]
        matched.sort(key=lambda h: (-h.priority, h.handler_id))
        return matched

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------
    def dispatch(
        self,
        doc_id: str,
        change_type: str,
        payload: Optional[dict] = None,
    ) -> DispatchResult:
        """Dispatch a change event to all matching enabled handlers.

        Callbacks fire OUTSIDE the lock. Exceptions raised by a callback are
        captured in the result and do not prevent other handlers from running.
        """
        # Snapshot matching handlers under the lock, then release before
        # invoking any callbacks.
        with self._lock:
            matched = [
                h
                for h in self._handlers.values()
                if h.enabled and (h.change_type == change_type or h.change_type == "*")
            ]
        matched.sort(key=lambda h: (-h.priority, h.handler_id))

        result = DispatchResult(doc_id=doc_id, change_type=change_type)

        for handler in matched:
            result.handlers_invoked.append(handler.handler_id)
            cb = handler.callback
            try:
                if cb is not None:
                    cb(doc_id, change_type, payload)
                result.delivered_count += 1
            except Exception as exc:  # noqa: BLE001 — capture all
                result.failed_count += 1
                result.errors.append(f"{handler.handler_id}: {exc!r}")

        with self._lock:
            self._total_dispatches += 1
            self._total_deliveries += result.delivered_count
            self._total_failures += result.failed_count

        return result

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------
    def clear_handlers(self) -> int:
        """Remove all handlers. Returns number cleared."""
        with self._lock:
            count = len(self._handlers)
            self._handlers.clear()
            return count

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------
    def stats(self) -> DispatcherStats:
        """Snapshot of aggregate counters."""
        with self._lock:
            total = len(self._handlers)
            enabled = sum(1 for h in self._handlers.values() if h.enabled)
            return DispatcherStats(
                total_handlers=total,
                enabled_handlers=enabled,
                total_dispatches=self._total_dispatches,
                total_deliveries=self._total_deliveries,
                total_failures=self._total_failures,
            )
