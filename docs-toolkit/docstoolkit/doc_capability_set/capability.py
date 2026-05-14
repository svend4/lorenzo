"""E387 DocCapabilitySet implementation.

Pure stdlib; thread-safe via ``threading.Lock``; dataclasses throughout.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Capability:
    """A defined capability.

    Attributes
    ----------
    name:
        Unique identifier of the capability.
    description:
        Human-readable description.
    default_enabled:
        If a doc has no explicit override, this default is reported by
        :meth:`DocCapabilitySet.is_enabled`.
    """

    name: str
    description: str = ""
    default_enabled: bool = False


@dataclass
class CapabilityStats:
    """Aggregate statistics for a :class:`DocCapabilitySet`."""

    total_capabilities: int
    total_docs: int
    total_assignments: int


class DocCapabilitySet:
    """Per-document capability flags with definable capabilities."""

    def __init__(self) -> None:
        self._capabilities: dict[str, Capability] = {}
        self._doc_caps: dict[str, dict[str, bool]] = {}
        self._lock = threading.Lock()

    # ---- capability registration -------------------------------------------------
    def define_capability(self, cap: Capability) -> None:
        """Register or replace a capability definition."""
        with self._lock:
            self._capabilities[cap.name] = cap

    def undefine_capability(self, name: str) -> bool:
        """Remove a capability definition and cascade-clear all doc overrides.

        Returns ``True`` if the capability existed.
        """
        with self._lock:
            if name not in self._capabilities:
                return False
            del self._capabilities[name]
            for doc_id, caps in list(self._doc_caps.items()):
                if name in caps:
                    del caps[name]
                if not caps:
                    del self._doc_caps[doc_id]
            return True

    def get_capability(self, name: str) -> Optional[Capability]:
        """Return the capability with this ``name`` or ``None``."""
        with self._lock:
            return self._capabilities.get(name)

    def list_capabilities(self) -> list[Capability]:
        """All defined capabilities sorted by name."""
        with self._lock:
            return [self._capabilities[n] for n in sorted(self._capabilities)]

    # ---- per-doc state -----------------------------------------------------------
    def set_capability(self, doc_id: str, name: str, enabled: bool) -> bool:
        """Set the per-doc value of a defined capability.

        Returns ``True`` if the capability is defined, otherwise ``False``
        (and no state change is made).
        """
        with self._lock:
            if name not in self._capabilities:
                return False
            caps = self._doc_caps.setdefault(doc_id, {})
            caps[name] = bool(enabled)
            return True

    def enable(self, doc_id: str, name: str) -> bool:
        """Alias for ``set_capability(doc_id, name, True)``."""
        return self.set_capability(doc_id, name, True)

    def disable(self, doc_id: str, name: str) -> bool:
        """Alias for ``set_capability(doc_id, name, False)``."""
        return self.set_capability(doc_id, name, False)

    def is_enabled(self, doc_id: str, name: str) -> bool:
        """Return effective enablement for ``doc_id`` / capability ``name``.

        Order of precedence:

        1. Per-doc override, if set.
        2. ``Capability.default_enabled`` if the capability is defined.
        3. ``False`` otherwise.
        """
        with self._lock:
            doc_caps = self._doc_caps.get(doc_id)
            if doc_caps is not None and name in doc_caps:
                return doc_caps[name]
            cap = self._capabilities.get(name)
            if cap is not None:
                return cap.default_enabled
            return False

    def clear_doc(self, doc_id: str) -> int:
        """Forget all overrides for ``doc_id``; return the number cleared."""
        with self._lock:
            caps = self._doc_caps.pop(doc_id, None)
            return len(caps) if caps else 0

    def capabilities_of(self, doc_id: str) -> dict[str, bool]:
        """A copy of the explicit ``{name: enabled}`` mapping for ``doc_id``."""
        with self._lock:
            return dict(self._doc_caps.get(doc_id, {}))

    def enabled_capabilities(self, doc_id: str) -> list[str]:
        """Sorted list of capability names effectively enabled for ``doc_id``.

        Combines per-doc overrides with capability defaults.
        """
        with self._lock:
            doc_caps = self._doc_caps.get(doc_id, {})
            result: set[str] = set()
            for name, cap in self._capabilities.items():
                if name in doc_caps:
                    if doc_caps[name]:
                        result.add(name)
                elif cap.default_enabled:
                    result.add(name)
            return sorted(result)

    def docs_with_capability(
        self, name: str, enabled: Optional[bool] = None
    ) -> list[str]:
        """Sorted list of doc IDs related to capability ``name``.

        * ``enabled=None``  — docs that have explicitly set this capability
          (either True or False).
        * ``enabled=True``  — docs where :meth:`is_enabled` is True (combines
          explicit ``True`` overrides with defaults if the capability is
          defined as ``default_enabled=True``).
        * ``enabled=False`` — docs that have explicitly disabled it.
        """
        with self._lock:
            if enabled is None:
                return sorted(
                    doc_id
                    for doc_id, caps in self._doc_caps.items()
                    if name in caps
                )
            if enabled is False:
                return sorted(
                    doc_id
                    for doc_id, caps in self._doc_caps.items()
                    if caps.get(name) is False
                )
            # enabled is True
            cap = self._capabilities.get(name)
            default_on = cap is not None and cap.default_enabled
            result: set[str] = set()
            for doc_id, caps in self._doc_caps.items():
                if name in caps:
                    if caps[name]:
                        result.add(doc_id)
                elif default_on:
                    result.add(doc_id)
            return sorted(result)

    def all_doc_ids(self) -> list[str]:
        """Sorted list of doc IDs that have any explicit capability setting."""
        with self._lock:
            return sorted(self._doc_caps)

    def stats(self) -> CapabilityStats:
        """Aggregate statistics."""
        with self._lock:
            total_caps = len(self._capabilities)
            total_docs = len(self._doc_caps)
            total_assignments = sum(len(c) for c in self._doc_caps.values())
            return CapabilityStats(
                total_capabilities=total_caps,
                total_docs=total_docs,
                total_assignments=total_assignments,
            )
