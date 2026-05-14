"""Implementation of the doc pinner.

The :class:`DocPinner` manages :class:`Pin` records that bind documents to
particular versions for selected scopes (user / group / global) with optional
expiration. :meth:`DocPinner.resolve` returns the highest-priority pin that
matches a request, falling back to a caller-supplied default version.

Resolution priority (highest first):
    1. USER pin matching user_id
    2. GROUP pin matching group_id
    3. GLOBAL pin
    4. default version (no pin used)
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class PinScope(Enum):
    """Scope of a pin record."""

    USER = "user"
    GROUP = "group"
    GLOBAL = "global"


class PinState(Enum):
    """State of a resolution outcome."""

    ACTIVE = "active"
    EXPIRED = "expired"
    OVERRIDDEN = "overridden"


@dataclass
class Pin:
    """A pinned version record."""

    pin_id: str
    doc_id: str
    version: str
    scope: PinScope
    target: Optional[str] = None
    created_at: float = 0.0
    expires_at: Optional[float] = None
    reason: Optional[str] = None

    def is_expired(self, now: float) -> bool:
        """Return True if the pin has expired at ``now``."""
        if self.expires_at is None:
            return False
        return now >= self.expires_at


@dataclass
class ResolutionResult:
    """Outcome of :meth:`DocPinner.resolve`."""

    doc_id: str
    resolved_version: str
    pin_used: Optional[Pin] = None
    state: PinState = PinState.ACTIVE


class DocPinner:
    """Thread-safe registry of document pins with scoped resolution."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pins: dict[str, Pin] = {}
        self._counter = 0

    # ------------------------------------------------------------------ pin

    def pin(
        self,
        doc_id: str,
        version: str,
        scope: PinScope = PinScope.GLOBAL,
        target: Optional[str] = None,
        expires_at: Optional[float] = None,
        reason: Optional[str] = None,
        now: float = 0.0,
    ) -> Pin:
        """Create and store a new pin, returning it."""
        if scope in (PinScope.USER, PinScope.GROUP) and target is None:
            raise ValueError(f"scope {scope.value!r} requires a target")
        if scope is PinScope.GLOBAL and target is not None:
            # Be lenient — silently drop target for GLOBAL pins.
            target = None

        with self._lock:
            self._counter += 1
            pin_id = f"pin-{self._counter}"
            p = Pin(
                pin_id=pin_id,
                doc_id=doc_id,
                version=version,
                scope=scope,
                target=target,
                created_at=now,
                expires_at=expires_at,
                reason=reason,
            )
            self._pins[pin_id] = p
            return p

    # ---------------------------------------------------------------- unpin

    def unpin(self, pin_id: str) -> bool:
        """Remove a pin by id. Returns True if found."""
        with self._lock:
            return self._pins.pop(pin_id, None) is not None

    # -------------------------------------------------------------- resolve

    def resolve(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        group_id: Optional[str] = None,
        default_version: str = "latest",
        now: float = 0.0,
    ) -> ResolutionResult:
        """Resolve the effective version for ``doc_id``.

        Returns a :class:`ResolutionResult` with the winning pin, or with
        ``default_version`` and ``pin_used=None`` when no pin matches.
        """
        with self._lock:
            user_pin: Optional[Pin] = None
            group_pin: Optional[Pin] = None
            global_pin: Optional[Pin] = None

            for p in self._pins.values():
                if p.doc_id != doc_id:
                    continue
                if p.is_expired(now):
                    continue
                if p.scope is PinScope.USER and user_id is not None and p.target == user_id:
                    if user_pin is None or p.created_at >= user_pin.created_at:
                        user_pin = p
                elif p.scope is PinScope.GROUP and group_id is not None and p.target == group_id:
                    if group_pin is None or p.created_at >= group_pin.created_at:
                        group_pin = p
                elif p.scope is PinScope.GLOBAL:
                    if global_pin is None or p.created_at >= global_pin.created_at:
                        global_pin = p

            if user_pin is not None:
                return ResolutionResult(
                    doc_id=doc_id,
                    resolved_version=user_pin.version,
                    pin_used=user_pin,
                    state=PinState.ACTIVE,
                )
            if group_pin is not None:
                return ResolutionResult(
                    doc_id=doc_id,
                    resolved_version=group_pin.version,
                    pin_used=group_pin,
                    state=PinState.ACTIVE,
                )
            if global_pin is not None:
                return ResolutionResult(
                    doc_id=doc_id,
                    resolved_version=global_pin.version,
                    pin_used=global_pin,
                    state=PinState.ACTIVE,
                )
            return ResolutionResult(
                doc_id=doc_id,
                resolved_version=default_version,
                pin_used=None,
                state=PinState.ACTIVE,
            )

    # ------------------------------------------------------------- listings

    def list_pins(
        self,
        doc_id: Optional[str] = None,
        scope: Optional[PinScope] = None,
        now: float = 0.0,
    ) -> list[Pin]:
        """Return active pins matching the given filters."""
        with self._lock:
            result: list[Pin] = []
            for p in self._pins.values():
                if p.is_expired(now):
                    continue
                if doc_id is not None and p.doc_id != doc_id:
                    continue
                if scope is not None and p.scope is not scope:
                    continue
                result.append(p)
            return result

    def pins_for_user(self, user_id: str, now: float = 0.0) -> list[Pin]:
        """Return active USER pins for ``user_id``."""
        with self._lock:
            return [
                p
                for p in self._pins.values()
                if p.scope is PinScope.USER
                and p.target == user_id
                and not p.is_expired(now)
            ]

    def pins_for_group(self, group_id: str, now: float = 0.0) -> list[Pin]:
        """Return active GROUP pins for ``group_id``."""
        with self._lock:
            return [
                p
                for p in self._pins.values()
                if p.scope is PinScope.GROUP
                and p.target == group_id
                and not p.is_expired(now)
            ]

    def global_pins(self, now: float = 0.0) -> list[Pin]:
        """Return active GLOBAL pins."""
        with self._lock:
            return [
                p
                for p in self._pins.values()
                if p.scope is PinScope.GLOBAL and not p.is_expired(now)
            ]

    # ----------------------------------------------------------- maintenance

    def cleanup_expired(self, now: float = 0.0) -> int:
        """Remove expired pins; returns the count removed."""
        with self._lock:
            expired_ids = [
                pid for pid, p in self._pins.items() if p.is_expired(now)
            ]
            for pid in expired_ids:
                del self._pins[pid]
            return len(expired_ids)

    def clear(self) -> None:
        """Remove all pins."""
        with self._lock:
            self._pins.clear()

    def pin_count(self, now: float = 0.0) -> int:
        """Number of active (non-expired) pins."""
        with self._lock:
            return sum(1 for p in self._pins.values() if not p.is_expired(now))

    @property
    def total_pins(self) -> int:
        """Total number of pin records (including expired)."""
        with self._lock:
            return len(self._pins)
