"""Doc pinner module for docs-toolkit.

Public API
----------
- ``PinScope``         — USER / GROUP / GLOBAL
- ``PinState``         — ACTIVE / EXPIRED / OVERRIDDEN
- ``Pin``              — pin record
- ``ResolutionResult`` — outcome of resolving a doc version
- ``DocPinner``        — central pin manager
"""

from docstoolkit.doc_pinner.pinner import (
    PinScope,
    PinState,
    Pin,
    ResolutionResult,
    DocPinner,
)

__all__ = [
    "PinScope",
    "PinState",
    "Pin",
    "ResolutionResult",
    "DocPinner",
]
