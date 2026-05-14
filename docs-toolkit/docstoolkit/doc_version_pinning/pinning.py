"""Implementation of E328 DocVersionPinning.

The :class:`DocVersionPinning` manages :class:`VersionPin` records that bind
documents to particular versions for selected scopes (global / user / context).
Each (doc_id, scope, scope_id) tuple holds at most one pin — re-pinning the
same tuple replaces the previous pin.

Resolution priority (highest first):
    1. context pin matching context_id
    2. user pin matching user_id
    3. global pin
    4. None (no pin)
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class VersionPin:
    """A single version pin record."""

    pin_id: str
    doc_id: str
    version: str
    scope: str = "global"
    scope_id: str = ""
    pinned_at: float = 0.0
    pinned_by: str = ""
    reason: str = ""


@dataclass
class PinningStats:
    """Aggregate statistics for the pinning store."""

    total_pins: int = 0
    unique_docs: int = 0
    unique_users: int = 0
    global_pins: int = 0
    user_pins: int = 0
    context_pins: int = 0


class DocVersionPinning:
    """Thread-safe registry of document version pins with scoped resolution."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pins: dict[str, VersionPin] = {}
        self._by_doc: dict[str, list[str]] = {}
        self._lookup: dict[tuple, str] = {}

    # ------------------------------------------------------------------ pin

    def pin(
        self,
        doc_id: str,
        version: str,
        scope: str = "global",
        scope_id: str = "",
        pinned_by: str = "",
        reason: str = "",
        now: Optional[float] = None,
    ) -> VersionPin:
        """Create or replace a pin for ``(doc_id, scope, scope_id)``.

        If an existing pin exists for the same tuple it is removed before
        the new pin is inserted.
        """
        if now is None:
            now = time.time()
        key = (doc_id, scope, scope_id)
        with self._lock:
            # Remove previous pin (if any) for this exact tuple.
            old_pin_id = self._lookup.get(key)
            if old_pin_id is not None:
                self._remove_pin_unlocked(old_pin_id)

            pin_id = str(uuid.uuid4())
            pin = VersionPin(
                pin_id=pin_id,
                doc_id=doc_id,
                version=version,
                scope=scope,
                scope_id=scope_id,
                pinned_at=now,
                pinned_by=pinned_by,
                reason=reason,
            )
            self._pins[pin_id] = pin
            self._by_doc.setdefault(doc_id, []).append(pin_id)
            self._lookup[key] = pin_id
            return pin

    # ---------------------------------------------------------------- unpin

    def unpin(self, pin_id: str) -> bool:
        """Remove a pin by ``pin_id``. Returns True if it existed."""
        with self._lock:
            if pin_id not in self._pins:
                return False
            self._remove_pin_unlocked(pin_id)
            return True

    def unpin_doc(
        self,
        doc_id: str,
        scope: str = "global",
        scope_id: str = "",
    ) -> bool:
        """Remove a pin by tuple. Returns True if it existed."""
        key = (doc_id, scope, scope_id)
        with self._lock:
            pin_id = self._lookup.get(key)
            if pin_id is None:
                return False
            self._remove_pin_unlocked(pin_id)
            return True

    def _remove_pin_unlocked(self, pin_id: str) -> None:
        """Remove a pin from all internal indexes (caller holds the lock)."""
        pin = self._pins.pop(pin_id, None)
        if pin is None:
            return
        bucket = self._by_doc.get(pin.doc_id)
        if bucket is not None:
            try:
                bucket.remove(pin_id)
            except ValueError:
                pass
            if not bucket:
                del self._by_doc[pin.doc_id]
        key = (pin.doc_id, pin.scope, pin.scope_id)
        if self._lookup.get(key) == pin_id:
            del self._lookup[key]

    # ------------------------------------------------------------------ get

    def get_pin(self, pin_id: str) -> Optional[VersionPin]:
        """Return a pin by id, or None."""
        with self._lock:
            return self._pins.get(pin_id)

    # -------------------------------------------------------------- resolve

    def resolve(
        self,
        doc_id: str,
        user_id: Optional[str] = None,
        context_id: Optional[str] = None,
    ) -> Optional[str]:
        """Return the pinned version using priority: context > user > global."""
        with self._lock:
            if context_id is not None:
                pid = self._lookup.get((doc_id, "context", context_id))
                if pid is not None:
                    return self._pins[pid].version
            if user_id is not None:
                pid = self._lookup.get((doc_id, "user", user_id))
                if pid is not None:
                    return self._pins[pid].version
            pid = self._lookup.get((doc_id, "global", ""))
            if pid is not None:
                return self._pins[pid].version
            return None

    # ------------------------------------------------------------- listings

    def pins_for_doc(self, doc_id: str) -> list[VersionPin]:
        """Return pins for a document, sorted by (scope, scope_id, pin_id)."""
        with self._lock:
            ids = list(self._by_doc.get(doc_id, ()))
            pins = [self._pins[pid] for pid in ids if pid in self._pins]
        pins.sort(key=lambda p: (p.scope, p.scope_id, p.pin_id))
        return pins

    def pins_for_user(self, user_id: str) -> list[VersionPin]:
        """Return user-scope pins for a user, sorted by doc_id."""
        with self._lock:
            pins = [
                p
                for p in self._pins.values()
                if p.scope == "user" and p.scope_id == user_id
            ]
        pins.sort(key=lambda p: p.doc_id)
        return pins

    def all_pins(self) -> list[VersionPin]:
        """Return every pin, sorted by (doc_id, scope, scope_id)."""
        with self._lock:
            pins = list(self._pins.values())
        pins.sort(key=lambda p: (p.doc_id, p.scope, p.scope_id))
        return pins

    # ----------------------------------------------------------------- stats

    def stats(self) -> PinningStats:
        """Compute aggregate statistics."""
        with self._lock:
            total = len(self._pins)
            docs = set()
            users = set()
            global_pins = 0
            user_pins = 0
            context_pins = 0
            for p in self._pins.values():
                docs.add(p.doc_id)
                if p.scope == "global":
                    global_pins += 1
                elif p.scope == "user":
                    user_pins += 1
                    if p.scope_id:
                        users.add(p.scope_id)
                elif p.scope == "context":
                    context_pins += 1
            return PinningStats(
                total_pins=total,
                unique_docs=len(docs),
                unique_users=len(users),
                global_pins=global_pins,
                user_pins=user_pins,
                context_pins=context_pins,
            )
