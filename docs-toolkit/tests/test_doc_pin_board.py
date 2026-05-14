"""Tests for ``docstoolkit.doc_pin_board``."""

from __future__ import annotations

import pytest

from docstoolkit.doc_pin_board import (
    Board,
    BoardStats,
    DocPinBoard,
    Pin,
    PinType,
)


# ----------------------------------------------------------------- fixtures
@pytest.fixture
def board_manager() -> DocPinBoard:
    return DocPinBoard()


@pytest.fixture
def board(board_manager: DocPinBoard) -> Board:
    return board_manager.create_board("Main", max_pins=10, now=100.0)


# ----------------------------------------------------------------- PinType
class TestPinType:
    def test_members(self):
        assert PinType.FEATURED.value == "featured"
        assert PinType.IMPORTANT.value == "important"
        assert PinType.ANNOUNCEMENT.value == "announcement"
        assert PinType.REMINDER.value == "reminder"
        assert PinType.OTHER.value == "other"

    def test_distinct(self):
        assert len({p.value for p in PinType}) == 5


# --------------------------------------------------------------------- Pin
class TestPinDataclass:
    def test_create_pin(self):
        p = Pin(pin_id="p1", doc_id="d1", board_id="b1")
        assert p.pin_id == "p1"
        assert p.doc_id == "d1"
        assert p.board_id == "b1"
        assert p.pin_type == PinType.FEATURED
        assert p.order == 0
        assert p.pinned_at == 0.0
        assert p.expires_at is None
        assert p.pinned_by is None
        assert p.note is None

    def test_pin_with_all_fields(self):
        p = Pin(
            pin_id="p1",
            doc_id="d1",
            board_id="b1",
            pin_type=PinType.IMPORTANT,
            order=5,
            pinned_at=123.0,
            expires_at=456.0,
            pinned_by="alice",
            note="must read",
        )
        assert p.pin_type == PinType.IMPORTANT
        assert p.order == 5
        assert p.pinned_at == 123.0
        assert p.expires_at == 456.0
        assert p.pinned_by == "alice"
        assert p.note == "must read"


# ------------------------------------------------------------------- Board
class TestBoard:
    def test_create_board_defaults(self):
        b = Board(board_id="b1", name="Main")
        assert b.board_id == "b1"
        assert b.name == "Main"
        assert b.pins == []
        assert b.max_pins == 50
        assert b.created_at == 0.0

    def test_board_with_pins(self):
        p = Pin(pin_id="p1", doc_id="d1", board_id="b1")
        b = Board(board_id="b1", name="Main", pins=[p])
        assert b.pins == [p]


# -------------------------------------------------------------- BoardStats
class TestBoardStats:
    def test_create_stats(self):
        s = BoardStats(
            board_id="b1",
            total_pins=4,
            active_pins=3,
            expired_pins=1,
            by_type={"featured": 2, "important": 2},
        )
        assert s.board_id == "b1"
        assert s.total_pins == 4
        assert s.active_pins == 3
        assert s.expired_pins == 1
        assert s.by_type == {"featured": 2, "important": 2}


# ------------------------------------------------------------ CreateBoard
class TestCreateBoard:
    def test_create_default(self, board_manager: DocPinBoard):
        b = board_manager.create_board("First")
        assert b.name == "First"
        assert b.max_pins == 50
        assert b.board_id

    def test_create_with_custom_id(self, board_manager: DocPinBoard):
        b = board_manager.create_board("X", board_id="custom-id")
        assert b.board_id == "custom-id"

    def test_create_with_max_pins(self, board_manager: DocPinBoard):
        b = board_manager.create_board("X", max_pins=3)
        assert b.max_pins == 3

    def test_create_sets_created_at(self, board_manager: DocPinBoard):
        b = board_manager.create_board("X", now=42.0)
        assert b.created_at == 42.0

    def test_create_two_boards_have_unique_ids(self, board_manager: DocPinBoard):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        assert b1.board_id != b2.board_id

    def test_create_increases_total_boards(self, board_manager: DocPinBoard):
        board_manager.create_board("A")
        board_manager.create_board("B")
        assert board_manager.total_boards == 2


# ----------------------------------------------------------- DeleteBoard
class TestDeleteBoard:
    def test_delete_existing(self, board_manager: DocPinBoard, board: Board):
        assert board_manager.delete_board(board.board_id) is True

    def test_delete_missing(self, board_manager: DocPinBoard):
        assert board_manager.delete_board("nope") is False

    def test_delete_removes_board(self, board_manager: DocPinBoard, board: Board):
        board_manager.delete_board(board.board_id)
        assert board_manager.get_board(board.board_id) is None

    def test_delete_removes_pins(self, board_manager: DocPinBoard, board: Board):
        p = board_manager.pin(board.board_id, "doc1")
        assert p is not None
        board_manager.delete_board(board.board_id)
        assert board_manager.get_pin(p.pin_id) is None
        assert board_manager.total_pins == 0


# -------------------------------------------------------------------- Pin
class TestPin:
    def test_pin_basic(self, board_manager: DocPinBoard, board: Board):
        p = board_manager.pin(board.board_id, "doc1")
        assert p is not None
        assert p.doc_id == "doc1"
        assert p.board_id == board.board_id
        assert p.pin_type == PinType.FEATURED

    def test_pin_assigns_order_zero_first(self, board_manager, board):
        p = board_manager.pin(board.board_id, "doc1")
        assert p.order == 0

    def test_pin_order_increments(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        assert (p1.order, p2.order, p3.order) == (0, 1, 2)

    def test_pin_with_type(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1", pin_type=PinType.IMPORTANT)
        assert p.pin_type == PinType.IMPORTANT

    def test_pin_with_expires(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1", expires_at=200.0)
        assert p.expires_at == 200.0

    def test_pin_with_note_and_user(self, board_manager, board):
        p = board_manager.pin(
            board.board_id, "d1", note="hello", pinned_by="alice"
        )
        assert p.note == "hello"
        assert p.pinned_by == "alice"

    def test_pin_with_now(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1", now=99.0)
        assert p.pinned_at == 99.0

    def test_pin_missing_board(self, board_manager: DocPinBoard):
        assert board_manager.pin("nope", "d1") is None

    def test_pin_unique_ids(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        assert p1.pin_id != p2.pin_id

    def test_pin_appears_on_board(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert p in board.pins


# ----------------------------------------------------------------- Unpin
class TestUnpin:
    def test_unpin_existing(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert board_manager.unpin(p.pin_id) is True

    def test_unpin_removes_from_board(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        board_manager.unpin(p.pin_id)
        assert p not in board.pins

    def test_unpin_removes_from_index(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        board_manager.unpin(p.pin_id)
        assert board_manager.get_pin(p.pin_id) is None

    def test_unpin_missing(self, board_manager: DocPinBoard):
        assert board_manager.unpin("nope") is False


# -------------------------------------------------------------- UnpinDoc
class TestUnpinDoc:
    def test_unpin_doc_zero(self, board_manager, board):
        assert board_manager.unpin_doc(board.board_id, "nope") == 0

    def test_unpin_doc_one(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        assert board_manager.unpin_doc(board.board_id, "d1") == 1

    def test_unpin_doc_multiple(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        board_manager.pin(board.board_id, "d1", pin_type=PinType.IMPORTANT)
        board_manager.pin(board.board_id, "d2")
        assert board_manager.unpin_doc(board.board_id, "d1") == 2
        assert board_manager.is_pinned(board.board_id, "d1") is False
        assert board_manager.is_pinned(board.board_id, "d2") is True

    def test_unpin_doc_missing_board(self, board_manager):
        assert board_manager.unpin_doc("nope", "d1") == 0


# --------------------------------------------------------------- Reorder
class TestReorder:
    def test_reorder_same(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert board_manager.reorder(p.pin_id, p.order) is True

    def test_reorder_move_forward(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        board_manager.reorder(p1.pin_id, 2)
        # After moving p1 to the end, orders are p2=0, p3=1, p1=2
        assert p2.order == 0
        assert p3.order == 1
        assert p1.order == 2

    def test_reorder_move_back(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        board_manager.reorder(p3.pin_id, 0)
        assert p3.order == 0
        assert p1.order == 1
        assert p2.order == 2

    def test_reorder_clamp_high(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        board_manager.reorder(p1.pin_id, 99)
        assert p1.order == 1
        assert p2.order == 0

    def test_reorder_clamp_low(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        board_manager.reorder(p2.pin_id, -5)
        assert p2.order == 0
        assert p1.order == 1

    def test_reorder_missing(self, board_manager):
        assert board_manager.reorder("nope", 0) is False


# ------------------------------------------------------------- MoveToTop
class TestMoveToTop:
    def test_move_to_top(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        board_manager.move_to_top(p3.pin_id)
        assert p3.order == 0
        assert p1.order == 1
        assert p2.order == 2

    def test_move_to_top_already_top(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        board_manager.pin(board.board_id, "d2")
        assert board_manager.move_to_top(p1.pin_id) is True
        assert p1.order == 0

    def test_move_to_top_missing(self, board_manager):
        assert board_manager.move_to_top("nope") is False


# ---------------------------------------------------------- MoveToBottom
class TestMoveToBottom:
    def test_move_to_bottom(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        board_manager.move_to_bottom(p1.pin_id)
        assert p1.order == 2
        assert p2.order == 0
        assert p3.order == 1

    def test_move_to_bottom_already_last(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        assert board_manager.move_to_bottom(p2.pin_id) is True
        assert p2.order == 1

    def test_move_to_bottom_missing(self, board_manager):
        assert board_manager.move_to_bottom("nope") is False


# -------------------------------------------------------- PinsForBoard
class TestPinsForBoard:
    def test_empty_board(self, board_manager, board):
        assert board_manager.pins_for_board(board.board_id) == []

    def test_missing_board(self, board_manager):
        assert board_manager.pins_for_board("nope") == []

    def test_sorted_by_order(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1")
        p2 = board_manager.pin(board.board_id, "d2")
        p3 = board_manager.pin(board.board_id, "d3")
        board_manager.move_to_top(p3.pin_id)
        pins = board_manager.pins_for_board(board.board_id)
        assert [p.pin_id for p in pins] == [p3.pin_id, p1.pin_id, p2.pin_id]

    def test_excludes_expired_by_default(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=50.0)
        board_manager.pin(board.board_id, "d2")
        pins = board_manager.pins_for_board(board.board_id, now=100.0)
        assert len(pins) == 1
        assert pins[0].doc_id == "d2"

    def test_include_expired(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=50.0)
        board_manager.pin(board.board_id, "d2")
        pins = board_manager.pins_for_board(
            board.board_id, now=100.0, include_expired=True
        )
        assert len(pins) == 2


# ---------------------------------------------------------- PinsForDoc
class TestPinsForDoc:
    def test_no_pins(self, board_manager):
        assert board_manager.pins_for_doc("d1") == []

    def test_one_pin(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert board_manager.pins_for_doc("d1") == [p]

    def test_across_boards(self, board_manager):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        p1 = board_manager.pin(b1.board_id, "doc")
        p2 = board_manager.pin(b2.board_id, "doc")
        pins = board_manager.pins_for_doc("doc")
        assert {p.pin_id for p in pins} == {p1.pin_id, p2.pin_id}


# ---------------------------------------------------------- PinsByType
class TestPinsByType:
    def test_filter_by_type(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1", pin_type=PinType.FEATURED)
        p2 = board_manager.pin(board.board_id, "d2", pin_type=PinType.IMPORTANT)
        p3 = board_manager.pin(board.board_id, "d3", pin_type=PinType.IMPORTANT)
        important = board_manager.pins_by_type(board.board_id, PinType.IMPORTANT)
        assert {p.pin_id for p in important} == {p2.pin_id, p3.pin_id}
        featured = board_manager.pins_by_type(board.board_id, PinType.FEATURED)
        assert [p.pin_id for p in featured] == [p1.pin_id]

    def test_empty_when_no_match(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", pin_type=PinType.FEATURED)
        assert board_manager.pins_by_type(board.board_id, PinType.REMINDER) == []

    def test_missing_board(self, board_manager):
        assert board_manager.pins_by_type("nope", PinType.FEATURED) == []

    def test_excludes_expired(self, board_manager, board):
        board_manager.pin(
            board.board_id, "d1", pin_type=PinType.FEATURED, expires_at=10.0
        )
        result = board_manager.pins_by_type(
            board.board_id, PinType.FEATURED, now=100.0
        )
        assert result == []


# ------------------------------------------------------------- GetPin
class TestGetPin:
    def test_existing(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert board_manager.get_pin(p.pin_id) is p

    def test_missing(self, board_manager):
        assert board_manager.get_pin("nope") is None


# ------------------------------------------------------------ GetBoard
class TestGetBoard:
    def test_existing(self, board_manager, board):
        assert board_manager.get_board(board.board_id) is board

    def test_missing(self, board_manager):
        assert board_manager.get_board("nope") is None


# -------------------------------------------------------------- Boards
class TestBoards:
    def test_empty(self, board_manager):
        assert board_manager.boards() == []

    def test_multiple(self, board_manager):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        result = board_manager.boards()
        assert {b.board_id for b in result} == {b1.board_id, b2.board_id}


# ----------------------------------------------------------- IsPinned
class TestIsPinned:
    def test_true(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        assert board_manager.is_pinned(board.board_id, "d1") is True

    def test_false(self, board_manager, board):
        assert board_manager.is_pinned(board.board_id, "d1") is False

    def test_missing_board(self, board_manager):
        assert board_manager.is_pinned("nope", "d1") is False

    def test_false_when_expired(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=10.0)
        assert board_manager.is_pinned(board.board_id, "d1", now=100.0) is False

    def test_true_when_not_yet_expired(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=200.0)
        assert board_manager.is_pinned(board.board_id, "d1", now=100.0) is True


# ----------------------------------------------------- CleanupExpired
class TestCleanupExpired:
    def test_cleanup_specific_board(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=10.0)
        board_manager.pin(board.board_id, "d2")
        removed = board_manager.cleanup_expired(board.board_id, now=50.0)
        assert removed == 1
        assert len(board.pins) == 1

    def test_cleanup_no_expired(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        assert board_manager.cleanup_expired(board.board_id, now=50.0) == 0

    def test_cleanup_missing_board(self, board_manager):
        assert board_manager.cleanup_expired("nope", now=50.0) == 0

    def test_cleanup_all_boards(self, board_manager):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        board_manager.pin(b1.board_id, "d1", expires_at=10.0)
        board_manager.pin(b2.board_id, "d2", expires_at=20.0)
        board_manager.pin(b2.board_id, "d3")
        removed = board_manager.cleanup_expired(now=100.0)
        assert removed == 2
        assert board_manager.total_pins == 1

    def test_cleanup_removes_from_index(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1", expires_at=10.0)
        board_manager.cleanup_expired(board.board_id, now=100.0)
        assert board_manager.get_pin(p.pin_id) is None


# --------------------------------------------------------------- Stats
class TestStats:
    def test_missing_board(self, board_manager):
        assert board_manager.stats("nope") is None

    def test_empty_board(self, board_manager, board):
        s = board_manager.stats(board.board_id)
        assert s.total_pins == 0
        assert s.active_pins == 0
        assert s.expired_pins == 0
        assert s.by_type == {}

    def test_count_by_type(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", pin_type=PinType.FEATURED)
        board_manager.pin(board.board_id, "d2", pin_type=PinType.FEATURED)
        board_manager.pin(board.board_id, "d3", pin_type=PinType.IMPORTANT)
        s = board_manager.stats(board.board_id)
        assert s.by_type["featured"] == 2
        assert s.by_type["important"] == 1
        assert s.total_pins == 3
        assert s.active_pins == 3
        assert s.expired_pins == 0

    def test_active_vs_expired(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=10.0)
        board_manager.pin(board.board_id, "d2")
        s = board_manager.stats(board.board_id, now=100.0)
        assert s.total_pins == 2
        assert s.active_pins == 1
        assert s.expired_pins == 1


# --------------------------------------------------------- TotalBoards
class TestTotalBoards:
    def test_initial(self, board_manager):
        assert board_manager.total_boards == 0

    def test_after_create(self, board_manager):
        board_manager.create_board("A")
        board_manager.create_board("B")
        assert board_manager.total_boards == 2

    def test_after_delete(self, board_manager):
        b = board_manager.create_board("A")
        board_manager.delete_board(b.board_id)
        assert board_manager.total_boards == 0


# ----------------------------------------------------------- TotalPins
class TestTotalPins:
    def test_initial(self, board_manager):
        assert board_manager.total_pins == 0

    def test_after_pin(self, board_manager, board):
        board_manager.pin(board.board_id, "d1")
        board_manager.pin(board.board_id, "d2")
        assert board_manager.total_pins == 2

    def test_after_unpin(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        board_manager.unpin(p.pin_id)
        assert board_manager.total_pins == 0


# ------------------------------------------------------------- MaxPins
class TestMaxPins:
    def test_evicts_oldest_non_important(self, board_manager):
        b = board_manager.create_board("X", max_pins=2)
        p1 = board_manager.pin(b.board_id, "d1", now=1.0)
        p2 = board_manager.pin(b.board_id, "d2", now=2.0)
        p3 = board_manager.pin(b.board_id, "d3", now=3.0)
        assert p3 is not None
        ids = {p.pin_id for p in b.pins}
        # p1 was oldest non-important and should be evicted
        assert p1.pin_id not in ids
        assert p2.pin_id in ids
        assert p3.pin_id in ids

    def test_skips_important_when_evicting(self, board_manager):
        b = board_manager.create_board("X", max_pins=2)
        p1 = board_manager.pin(
            b.board_id, "d1", pin_type=PinType.IMPORTANT, now=1.0
        )
        p2 = board_manager.pin(b.board_id, "d2", now=2.0)
        p3 = board_manager.pin(b.board_id, "d3", now=3.0)
        ids = {p.pin_id for p in b.pins}
        # important pin retained, p2 dropped
        assert p1.pin_id in ids
        assert p2.pin_id not in ids
        assert p3.pin_id in ids

    def test_all_important_blocks_new_pin(self, board_manager):
        b = board_manager.create_board("X", max_pins=2)
        board_manager.pin(b.board_id, "d1", pin_type=PinType.IMPORTANT, now=1.0)
        board_manager.pin(b.board_id, "d2", pin_type=PinType.IMPORTANT, now=2.0)
        result = board_manager.pin(b.board_id, "d3", now=3.0)
        assert result is None
        assert len(b.pins) == 2

    def test_under_limit_no_eviction(self, board_manager):
        b = board_manager.create_board("X", max_pins=5)
        for i in range(3):
            board_manager.pin(b.board_id, f"d{i}")
        assert len(b.pins) == 3


# --------------------------------------------------------------- Clear
class TestClear:
    def test_clear_empty(self, board_manager):
        board_manager.clear()
        assert board_manager.total_boards == 0
        assert board_manager.total_pins == 0

    def test_clear_removes_everything(self, board_manager):
        b = board_manager.create_board("A")
        board_manager.pin(b.board_id, "d1")
        board_manager.pin(b.board_id, "d2")
        board_manager.clear()
        assert board_manager.total_boards == 0
        assert board_manager.total_pins == 0
        assert board_manager.boards() == []


# ----------------------------------------------------------- EdgeCases
class TestEdgeCases:
    def test_same_doc_pinned_twice_on_same_board(self, board_manager, board):
        p1 = board_manager.pin(board.board_id, "d1", pin_type=PinType.FEATURED)
        p2 = board_manager.pin(board.board_id, "d1", pin_type=PinType.IMPORTANT)
        assert p1.pin_id != p2.pin_id
        assert len(board_manager.pins_for_doc("d1")) == 2

    def test_same_doc_pinned_on_two_boards(self, board_manager):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        board_manager.pin(b1.board_id, "shared")
        board_manager.pin(b2.board_id, "shared")
        assert board_manager.is_pinned(b1.board_id, "shared")
        assert board_manager.is_pinned(b2.board_id, "shared")

    def test_unpin_doc_does_not_affect_other_boards(self, board_manager):
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        board_manager.pin(b1.board_id, "d1")
        board_manager.pin(b2.board_id, "d1")
        board_manager.unpin_doc(b1.board_id, "d1")
        assert not board_manager.is_pinned(b1.board_id, "d1")
        assert board_manager.is_pinned(b2.board_id, "d1")

    def test_expires_at_zero_is_not_expired_when_pinned_negative(
        self, board_manager, board
    ):
        # expires_at=0 means: now >= 0 → expired
        board_manager.pin(board.board_id, "d1", expires_at=0.0)
        assert not board_manager.is_pinned(board.board_id, "d1", now=0.0)

    def test_expires_at_none_never_expires(self, board_manager, board):
        board_manager.pin(board.board_id, "d1", expires_at=None)
        assert board_manager.is_pinned(board.board_id, "d1", now=1e18)

    def test_reorder_across_boards_not_allowed(self, board_manager):
        # reorder uses only the pin's own board
        b1 = board_manager.create_board("A")
        b2 = board_manager.create_board("B")
        p1 = board_manager.pin(b1.board_id, "d1")
        p2 = board_manager.pin(b1.board_id, "d2")
        board_manager.pin(b2.board_id, "d3")
        board_manager.move_to_bottom(p1.pin_id)
        # p1 moved to bottom of b1 (which has 2 pins)
        assert p1.order == 1
        assert p2.order == 0

    def test_pinned_at_zero_default(self, board_manager, board):
        p = board_manager.pin(board.board_id, "d1")
        assert p.pinned_at == 0.0
