"""Bulletin / pin board for sticky important documents.

Stdlib-only implementation. Thread-safe via ``threading.Lock``.

Supports:
- Multiple boards per workspace
- Pin ordering (lower order shown first), with auto-assign on creation
- Time-limited pins via ``expires_at``
- Pin types (FEATURED, IMPORTANT, ANNOUNCEMENT, REMINDER, OTHER)
- Max pins per board with eviction of oldest non-IMPORTANT pin
- Reordering primitives: ``reorder``, ``move_to_top``, ``move_to_bottom``
- Cleanup of expired pins
- Per-board statistics
"""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional


class PinType(Enum):
    """Type / category of a pin on a board."""

    FEATURED = "featured"
    IMPORTANT = "important"
    ANNOUNCEMENT = "announcement"
    REMINDER = "reminder"
    OTHER = "other"


@dataclass
class Pin:
    """Single pin: links a document to a board with display metadata."""

    pin_id: str
    doc_id: str
    board_id: str
    pin_type: PinType = PinType.FEATURED
    order: int = 0
    pinned_at: float = 0.0
    expires_at: Optional[float] = None
    pinned_by: Optional[str] = None
    note: Optional[str] = None


@dataclass
class Board:
    """Bulletin board holding pinned documents."""

    board_id: str
    name: str
    pins: List[Pin] = field(default_factory=list)
    max_pins: int = 50
    created_at: float = 0.0


@dataclass
class BoardStats:
    """Aggregated statistics for a single board."""

    board_id: str
    total_pins: int
    active_pins: int
    expired_pins: int
    by_type: Dict[str, int]


class DocPinBoard:
    """Manage bulletin boards and pinned documents.

    All operations are thread-safe. ``now`` parameters allow deterministic
    testing of time-limited pins.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._boards: Dict[str, Board] = {}
        # pin_id -> Pin index for O(1) lookup
        self._pins: Dict[str, Pin] = {}

    # ------------------------------------------------------------------ boards
    def create_board(
        self,
        name: str,
        max_pins: int = 50,
        board_id: Optional[str] = None,
        now: float = 0.0,
    ) -> Board:
        """Create a new board with the given name and optional id."""
        with self._lock:
            bid = board_id if board_id else str(uuid.uuid4())
            board = Board(
                board_id=bid,
                name=name,
                pins=[],
                max_pins=max_pins,
                created_at=now,
            )
            self._boards[bid] = board
            return board

    def delete_board(self, board_id: str) -> bool:
        """Delete a board and all its pins. Returns True if deleted."""
        with self._lock:
            board = self._boards.pop(board_id, None)
            if board is None:
                return False
            for pin in board.pins:
                self._pins.pop(pin.pin_id, None)
            return True

    def get_board(self, board_id: str) -> Optional[Board]:
        """Return board or None."""
        with self._lock:
            return self._boards.get(board_id)

    def boards(self) -> List[Board]:
        """Return all boards."""
        with self._lock:
            return list(self._boards.values())

    # -------------------------------------------------------------------- pins
    def pin(
        self,
        board_id: str,
        doc_id: str,
        pin_type: PinType = PinType.FEATURED,
        expires_at: Optional[float] = None,
        note: Optional[str] = None,
        pinned_by: Optional[str] = None,
        now: float = 0.0,
    ) -> Optional[Pin]:
        """Create a pin on a board.

        Order is auto-assigned as ``max(existing_orders) + 1``.
        If ``max_pins`` would be exceeded, the oldest non-IMPORTANT pin is
        dropped. Returns the new ``Pin`` or ``None`` if the board doesn't exist.
        """
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return None

            # Eviction: drop oldest non-IMPORTANT if at capacity
            if len(board.pins) >= board.max_pins:
                evict_idx = -1
                evict_at = float("inf")
                for idx, p in enumerate(board.pins):
                    if p.pin_type == PinType.IMPORTANT:
                        continue
                    if p.pinned_at < evict_at:
                        evict_at = p.pinned_at
                        evict_idx = idx
                if evict_idx >= 0:
                    dropped = board.pins.pop(evict_idx)
                    self._pins.pop(dropped.pin_id, None)
                else:
                    # All pins are IMPORTANT — cannot evict
                    return None

            next_order = (
                max((p.order for p in board.pins), default=-1) + 1
            )
            new_pin = Pin(
                pin_id=str(uuid.uuid4()),
                doc_id=doc_id,
                board_id=board_id,
                pin_type=pin_type,
                order=next_order,
                pinned_at=now,
                expires_at=expires_at,
                pinned_by=pinned_by,
                note=note,
            )
            board.pins.append(new_pin)
            self._pins[new_pin.pin_id] = new_pin
            return new_pin

    def unpin(self, pin_id: str) -> bool:
        """Remove a single pin by id."""
        with self._lock:
            pin = self._pins.pop(pin_id, None)
            if pin is None:
                return False
            board = self._boards.get(pin.board_id)
            if board is not None:
                board.pins = [p for p in board.pins if p.pin_id != pin_id]
            return True

    def unpin_doc(self, board_id: str, doc_id: str) -> int:
        """Remove every pin of ``doc_id`` on the given board.

        Returns the number of pins removed.
        """
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return 0
            to_remove = [p for p in board.pins if p.doc_id == doc_id]
            for p in to_remove:
                self._pins.pop(p.pin_id, None)
            board.pins = [p for p in board.pins if p.doc_id != doc_id]
            return len(to_remove)

    def get_pin(self, pin_id: str) -> Optional[Pin]:
        """Return pin or None."""
        with self._lock:
            return self._pins.get(pin_id)

    # --------------------------------------------------------------- reorder
    def reorder(self, pin_id: str, new_order: int) -> bool:
        """Set a pin's display order, shifting other pins as needed."""
        with self._lock:
            pin = self._pins.get(pin_id)
            if pin is None:
                return False
            board = self._boards.get(pin.board_id)
            if board is None:
                return False

            old_order = pin.order
            if new_order == old_order:
                return True

            others = [p for p in board.pins if p.pin_id != pin_id]
            # Clamp new_order
            if new_order < 0:
                new_order = 0
            if new_order > len(others):
                new_order = len(others)

            # Sort others by current order, drop pin to new position
            others.sort(key=lambda p: p.order)
            others.insert(new_order, pin)
            # Re-number sequentially
            for i, p in enumerate(others):
                p.order = i
            return True

    def move_to_top(self, pin_id: str) -> bool:
        """Move pin to the top (order 0)."""
        return self.reorder(pin_id, 0)

    def move_to_bottom(self, pin_id: str) -> bool:
        """Move pin to the bottom (highest order)."""
        with self._lock:
            pin = self._pins.get(pin_id)
            if pin is None:
                return False
            board = self._boards.get(pin.board_id)
            if board is None:
                return False
            target = len(board.pins) - 1
        return self.reorder(pin_id, target)

    # --------------------------------------------------------------- queries
    def pins_for_board(
        self,
        board_id: str,
        now: float = 0.0,
        include_expired: bool = False,
    ) -> List[Pin]:
        """Return pins for a board sorted by order ascending."""
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return []
            result = []
            for p in board.pins:
                if not include_expired and self._is_expired(p, now):
                    continue
                result.append(p)
            result.sort(key=lambda p: p.order)
            return result

    def pins_for_doc(self, doc_id: str) -> List[Pin]:
        """Return all pins (across boards) of a particular document."""
        with self._lock:
            return [p for p in self._pins.values() if p.doc_id == doc_id]

    def pins_by_type(
        self,
        board_id: str,
        pin_type: PinType,
        now: float = 0.0,
    ) -> List[Pin]:
        """Return active pins on a board of the given type, sorted by order."""
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return []
            result = [
                p
                for p in board.pins
                if p.pin_type == pin_type and not self._is_expired(p, now)
            ]
            result.sort(key=lambda p: p.order)
            return result

    def is_pinned(self, board_id: str, doc_id: str, now: float = 0.0) -> bool:
        """True if ``doc_id`` has at least one active pin on the board."""
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return False
            for p in board.pins:
                if p.doc_id == doc_id and not self._is_expired(p, now):
                    return True
            return False

    # --------------------------------------------------------------- cleanup
    def cleanup_expired(
        self,
        board_id: Optional[str] = None,
        now: float = 0.0,
    ) -> int:
        """Remove expired pins. If ``board_id`` is None, clean every board.

        Returns the count of removed pins.
        """
        with self._lock:
            removed = 0
            if board_id is None:
                target_boards = list(self._boards.values())
            else:
                board = self._boards.get(board_id)
                if board is None:
                    return 0
                target_boards = [board]

            for board in target_boards:
                keep: List[Pin] = []
                for p in board.pins:
                    if self._is_expired(p, now):
                        self._pins.pop(p.pin_id, None)
                        removed += 1
                    else:
                        keep.append(p)
                board.pins = keep
            return removed

    # ----------------------------------------------------------------- stats
    def stats(self, board_id: str, now: float = 0.0) -> Optional[BoardStats]:
        """Return statistics for a board."""
        with self._lock:
            board = self._boards.get(board_id)
            if board is None:
                return None
            by_type: Dict[str, int] = {}
            active = 0
            expired = 0
            for p in board.pins:
                by_type[p.pin_type.value] = by_type.get(p.pin_type.value, 0) + 1
                if self._is_expired(p, now):
                    expired += 1
                else:
                    active += 1
            return BoardStats(
                board_id=board_id,
                total_pins=len(board.pins),
                active_pins=active,
                expired_pins=expired,
                by_type=by_type,
            )

    # ------------------------------------------------------------ properties
    @property
    def total_boards(self) -> int:
        with self._lock:
            return len(self._boards)

    @property
    def total_pins(self) -> int:
        with self._lock:
            return len(self._pins)

    def clear(self) -> None:
        """Remove every board and pin."""
        with self._lock:
            self._boards.clear()
            self._pins.clear()

    # ----------------------------------------------------------------- utils
    @staticmethod
    def _is_expired(pin: Pin, now: float) -> bool:
        return pin.expires_at is not None and now >= pin.expires_at
