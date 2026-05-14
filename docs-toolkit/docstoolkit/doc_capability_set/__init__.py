"""E387 DocCapabilitySet — per-doc capability flags.

Public API
----------
:class:`Capability`        — a defined capability
:class:`CapabilityStats`   — aggregate statistics
:class:`DocCapabilitySet`  — main interface for capability management
"""

from .capability import Capability, CapabilityStats, DocCapabilitySet

__all__ = ["Capability", "CapabilityStats", "DocCapabilitySet"]
