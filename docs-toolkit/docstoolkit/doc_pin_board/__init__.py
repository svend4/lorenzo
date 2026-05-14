"""Doc pin board module for docs-toolkit.

Public API
----------
- ``PinType``     — FEATURED / IMPORTANT / ANNOUNCEMENT / REMINDER / OTHER
- ``Pin``         — pin record
- ``Board``       — bulletin board
- ``BoardStats``  — board statistics
- ``DocPinBoard`` — central pin board manager
"""

from docstoolkit.doc_pin_board.pin_board import (
    PinType,
    Pin,
    Board,
    BoardStats,
    DocPinBoard,
)

__all__ = [
    "PinType",
    "Pin",
    "Board",
    "BoardStats",
    "DocPinBoard",
]
