"""Notification router: dispatch events to registered handlers by channel.

Key concepts
------------
- ``HandlerConfig``    — binds a callable to a channel, with optional event_type and filter
- ``NotificationRouter`` — registry + dispatcher; tracks every delivery attempt
- ``DeliveryRecord``   — immutable result of one handler invocation
- ``DeliveryStatus``   — SENT | FAILED | FILTERED
"""

from __future__ import annotations

import time
import traceback
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from uuid import uuid4


# ---------------------------------------------------------------------------
# Public enums / dataclasses
# ---------------------------------------------------------------------------

class DeliveryStatus(str, Enum):
    SENT = "sent"
    FAILED = "failed"
    FILTERED = "filtered"  # handler's filter_fn returned False


@dataclass
class Notification:
    """Represents a single notification event to be routed."""

    event_type: str
    channel: str
    payload: dict = field(default_factory=dict)
    notification_id: str = field(default_factory=lambda: uuid4().hex[:12])
    timestamp: float = field(default_factory=time.time)


@dataclass
class DeliveryRecord:
    """Immutable record of one delivery attempt."""

    notification_id: str
    channel: str
    handler_name: str
    status: DeliveryStatus
    error: str = ""


@dataclass
class HandlerConfig:
    """Configuration for a single notification handler.

    Parameters
    ----------
    name:
        Unique identifier for this handler.  Duplicate names overwrite.
    channel:
        The notification channel this handler listens on (e.g. ``"email"``,
        ``"webhook"``, ``"log"``).
    handler:
        Callable invoked with the ``Notification`` when delivery is attempted.
    event_types:
        Optional whitelist of event types.  ``None`` means *all* event types.
    filter_fn:
        Optional predicate; if it returns ``False`` the notification is
        recorded as ``FILTERED`` and ``handler`` is not called.
    """

    name: str
    channel: str
    handler: Callable[[Notification], None]
    event_types: list[str] | None = None
    filter_fn: Callable[[Notification], bool] | None = None


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

class NotificationRouter:
    """Route notifications to registered handlers.

    Parameters
    ----------
    now_fn:
        Optional callable returning a ``float`` (epoch seconds).  Used to
        stamp ``Notification.timestamp`` when creating notifications via
        :meth:`send`.  Defaults to :func:`time.time`.
    """

    def __init__(self, now_fn: Callable[[], float] | None = None) -> None:
        self._now_fn: Callable[[], float] = now_fn if now_fn is not None else time.time
        # Ordered dict preserves insertion order; duplicate names overwrite.
        self._handlers: dict[str, HandlerConfig] = {}
        self._history: list[DeliveryRecord] = []

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, config: HandlerConfig) -> None:
        """Register a handler.  Duplicate names overwrite the previous entry."""
        self._handlers[config.name] = config

    def unregister(self, name: str) -> bool:
        """Remove handler by name.

        Returns
        -------
        bool
            ``True`` if the handler existed and was removed, ``False`` otherwise.
        """
        if name in self._handlers:
            del self._handlers[name]
            return True
        return False

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def send(
        self,
        event_type: str,
        channel: str,
        payload: dict | None = None,
    ) -> list[DeliveryRecord]:
        """Create a :class:`Notification` and route it to matching handlers.

        Matching logic
        ~~~~~~~~~~~~~~
        A handler is *eligible* when **both** conditions hold:

        1. ``handler.channel == channel``
        2. ``handler.event_types is None``  **or**
           ``event_type in handler.event_types``

        For eligible handlers the filter is applied:

        * If ``filter_fn`` is not ``None`` and returns ``False``, the record
          status is ``FILTERED`` and the handler callable is **not** invoked.
        * Otherwise the handler callable is called.  An exception results in
          ``FAILED`` (error message stored); other handlers are still called.

        Returns
        -------
        list[DeliveryRecord]
            One record per eligible handler, in registration order.
        """
        notif = Notification(
            event_type=event_type,
            channel=channel,
            payload=payload if payload is not None else {},
            timestamp=self._now_fn(),
        )
        return self.send_notification(notif)

    def send_notification(self, notif: Notification) -> list[DeliveryRecord]:
        """Route a pre-built :class:`Notification` object.

        This is the low-level dispatch method; :meth:`send` delegates here
        after constructing the ``Notification``.
        """
        records: list[DeliveryRecord] = []

        for config in self._handlers.values():
            # Channel filter
            if config.channel != notif.channel:
                continue

            # Event-type filter
            if config.event_types is not None and notif.event_type not in config.event_types:
                continue

            # Per-handler predicate filter
            if config.filter_fn is not None:
                try:
                    passes = config.filter_fn(notif)
                except Exception:
                    passes = False

                if not passes:
                    record = DeliveryRecord(
                        notification_id=notif.notification_id,
                        channel=notif.channel,
                        handler_name=config.name,
                        status=DeliveryStatus.FILTERED,
                    )
                    records.append(record)
                    self._history.append(record)
                    continue

            # Invoke handler
            try:
                config.handler(notif)
                record = DeliveryRecord(
                    notification_id=notif.notification_id,
                    channel=notif.channel,
                    handler_name=config.name,
                    status=DeliveryStatus.SENT,
                )
            except Exception as exc:
                record = DeliveryRecord(
                    notification_id=notif.notification_id,
                    channel=notif.channel,
                    handler_name=config.name,
                    status=DeliveryStatus.FAILED,
                    error=str(exc),
                )

            records.append(record)
            self._history.append(record)

        return records

    # ------------------------------------------------------------------
    # History / introspection
    # ------------------------------------------------------------------

    def history(
        self,
        notification_id: str | None = None,
        channel: str | None = None,
        status: DeliveryStatus | None = None,
    ) -> list[DeliveryRecord]:
        """Return delivery history, optionally filtered.

        All provided criteria are combined with AND logic.
        """
        result = self._history
        if notification_id is not None:
            result = [r for r in result if r.notification_id == notification_id]
        if channel is not None:
            result = [r for r in result if r.channel == channel]
        if status is not None:
            result = [r for r in result if r.status == status]
        return list(result)

    def handler_names(self) -> list[str]:
        """Return names of all currently registered handlers."""
        return list(self._handlers.keys())

    def clear_history(self) -> None:
        """Discard all stored :class:`DeliveryRecord` entries."""
        self._history.clear()
