"""Tests for ``docstoolkit.doc_pin_board`` (E306 — per-user pinning)."""

from __future__ import annotations

import threading
import time

import pytest

from docstoolkit.doc_pin_board import DocPinBoard, PinBoardStats, PinnedDoc


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def board() -> DocPinBoard:
    return DocPinBoard()


# ---------------------------------------------------------------------------
# PinnedDoc dataclass
# ---------------------------------------------------------------------------


class TestPinnedDocDataclass:
    def test_required_fields(self):
        p = PinnedDoc(user_id="alice", doc_id="d1")
        assert p.user_id == "alice"
        assert p.doc_id == "d1"

    def test_default_pinned_at(self):
        p = PinnedDoc(user_id="u", doc_id="d")
        assert p.pinned_at == 0.0

    def test_default_position(self):
        p = PinnedDoc(user_id="u", doc_id="d")
        assert p.position == 0

    def test_default_note(self):
        p = PinnedDoc(user_id="u", doc_id="d")
        assert p.note == ""

    def test_custom_fields(self):
        p = PinnedDoc(
            user_id="bob",
            doc_id="d2",
            pinned_at=123.4,
            position=7,
            note="important",
        )
        assert p.pinned_at == 123.4
        assert p.position == 7
        assert p.note == "important"


# ---------------------------------------------------------------------------
# PinBoardStats dataclass
# ---------------------------------------------------------------------------


class TestPinBoardStatsDataclass:
    def test_fields(self):
        s = PinBoardStats(
            total_pins=10,
            unique_users=3,
            unique_docs=8,
            avg_pins_per_user=3.33,
        )
        assert s.total_pins == 10
        assert s.unique_users == 3
        assert s.unique_docs == 8
        assert s.avg_pins_per_user == 3.33

    def test_zero_values(self):
        s = PinBoardStats(
            total_pins=0, unique_users=0, unique_docs=0, avg_pins_per_user=0.0
        )
        assert s.total_pins == 0


# ---------------------------------------------------------------------------
# Construction / empty state
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_empty_all_users(self, board: DocPinBoard):
        assert board.all_users() == []

    def test_empty_all_pinned_docs(self, board: DocPinBoard):
        assert board.all_pinned_docs() == []

    def test_empty_stats(self, board: DocPinBoard):
        s = board.stats()
        assert s.total_pins == 0
        assert s.unique_users == 0
        assert s.unique_docs == 0
        assert s.avg_pins_per_user == 0.0

    def test_empty_pins_for_unknown_user(self, board: DocPinBoard):
        assert board.pins_for_user("nobody") == []


# ---------------------------------------------------------------------------
# pin
# ---------------------------------------------------------------------------


class TestPin:
    def test_new_pin_returns_true(self, board: DocPinBoard):
        assert board.pin("alice", "d1") is True

    def test_duplicate_pin_returns_false(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.pin("alice", "d1") is False

    def test_first_pin_position_zero(self, board: DocPinBoard):
        board.pin("alice", "d1")
        p = board.get_pin("alice", "d1")
        assert p is not None
        assert p.position == 0

    def test_second_pin_position_one(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        assert board.get_pin("alice", "d2").position == 1

    def test_timestamp_set(self, board: DocPinBoard):
        board.pin("alice", "d1", now=500.0)
        p = board.get_pin("alice", "d1")
        assert p.pinned_at == 500.0

    def test_note_stored(self, board: DocPinBoard):
        board.pin("alice", "d1", note="my note")
        assert board.get_pin("alice", "d1").note == "my note"

    def test_different_users_same_doc_both_pin(self, board: DocPinBoard):
        assert board.pin("alice", "d1") is True
        assert board.pin("bob", "d1") is True

    def test_position_independent_per_user(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("bob", "d1")
        assert board.get_pin("bob", "d1").position == 0


# ---------------------------------------------------------------------------
# unpin
# ---------------------------------------------------------------------------


class TestUnpin:
    def test_unpin_existing_returns_true(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.unpin("alice", "d1") is True

    def test_unpin_missing_returns_false(self, board: DocPinBoard):
        assert board.unpin("alice", "nope") is False

    def test_unpin_removes_pin(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.unpin("alice", "d1")
        assert board.get_pin("alice", "d1") is None

    def test_unpin_reassigns_positions(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        board.unpin("alice", "d2")
        # d1 stays 0, d3 drops to 1
        assert board.get_pin("alice", "d1").position == 0
        assert board.get_pin("alice", "d3").position == 1

    def test_unpin_middle_positions_sequential(self, board: DocPinBoard):
        for i in range(5):
            board.pin("u", f"d{i}")
        board.unpin("u", "d2")
        pins = board.pins_for_user("u")
        positions = [p.position for p in pins]
        assert positions == list(range(len(positions)))

    def test_unpin_last_removes_user(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.unpin("alice", "d1")
        assert "alice" not in board.all_users()


# ---------------------------------------------------------------------------
# is_pinned
# ---------------------------------------------------------------------------


class TestIsPinned:
    def test_true_after_pin(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.is_pinned("alice", "d1") is True

    def test_false_before_pin(self, board: DocPinBoard):
        assert board.is_pinned("alice", "d1") is False

    def test_false_after_unpin(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.unpin("alice", "d1")
        assert board.is_pinned("alice", "d1") is False

    def test_not_pinned_for_different_user(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.is_pinned("bob", "d1") is False


# ---------------------------------------------------------------------------
# get_pin
# ---------------------------------------------------------------------------


class TestGetPin:
    def test_returns_pinned_doc(self, board: DocPinBoard):
        board.pin("alice", "d1", now=42.0)
        p = board.get_pin("alice", "d1")
        assert isinstance(p, PinnedDoc)
        assert p.doc_id == "d1"
        assert p.pinned_at == 42.0

    def test_returns_none_for_missing(self, board: DocPinBoard):
        assert board.get_pin("alice", "nope") is None

    def test_returns_none_for_unknown_user(self, board: DocPinBoard):
        assert board.get_pin("ghost", "d1") is None


# ---------------------------------------------------------------------------
# pins_for_user
# ---------------------------------------------------------------------------


class TestPinsForUser:
    def test_empty_for_unknown_user(self, board: DocPinBoard):
        assert board.pins_for_user("ghost") == []

    def test_single_pin(self, board: DocPinBoard):
        board.pin("alice", "d1")
        pins = board.pins_for_user("alice")
        assert len(pins) == 1
        assert pins[0].doc_id == "d1"

    def test_sorted_by_position(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        pins = board.pins_for_user("alice")
        assert [p.position for p in pins] == [0, 1, 2]

    def test_isolation_between_users(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("bob", "d3")
        assert len(board.pins_for_user("alice")) == 2
        assert len(board.pins_for_user("bob")) == 1

    def test_order_after_move(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        board.move_pin("alice", "d3", 0)
        pins = board.pins_for_user("alice")
        assert pins[0].doc_id == "d3"


# ---------------------------------------------------------------------------
# users_who_pinned
# ---------------------------------------------------------------------------


class TestUsersWhoPinned:
    def test_empty_when_no_pins(self, board: DocPinBoard):
        assert board.users_who_pinned("d1") == []

    def test_single_user(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.users_who_pinned("d1") == ["alice"]

    def test_multiple_users_sorted(self, board: DocPinBoard):
        board.pin("charlie", "d1")
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        assert board.users_who_pinned("d1") == ["alice", "bob", "charlie"]

    def test_only_users_who_pinned_that_doc(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("bob", "d2")
        assert board.users_who_pinned("d1") == ["alice"]


# ---------------------------------------------------------------------------
# move_pin
# ---------------------------------------------------------------------------


class TestMovePin:
    def test_move_to_start(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        board.move_pin("alice", "d3", 0)
        pins = board.pins_for_user("alice")
        assert pins[0].doc_id == "d3"
        assert pins[1].doc_id == "d1"
        assert pins[2].doc_id == "d2"

    def test_move_to_end(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        board.move_pin("alice", "d1", 2)
        pins = board.pins_for_user("alice")
        assert pins[0].doc_id == "d2"
        assert pins[1].doc_id == "d3"
        assert pins[2].doc_id == "d1"

    def test_clamp_negative_to_zero(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.move_pin("alice", "d2", -5)
        pins = board.pins_for_user("alice")
        assert pins[0].doc_id == "d2"

    def test_clamp_high_to_last(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        board.move_pin("alice", "d1", 999)
        pins = board.pins_for_user("alice")
        assert pins[-1].doc_id == "d1"

    def test_positions_sequential_after_move(self, board: DocPinBoard):
        for i in range(4):
            board.pin("alice", f"d{i}")
        board.move_pin("alice", "d0", 2)
        pins = board.pins_for_user("alice")
        assert [p.position for p in pins] == [0, 1, 2, 3]

    def test_returns_false_if_pin_not_found(self, board: DocPinBoard):
        assert board.move_pin("alice", "nope", 0) is False

    def test_returns_true_on_success(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        assert board.move_pin("alice", "d2", 0) is True


# ---------------------------------------------------------------------------
# update_note
# ---------------------------------------------------------------------------


class TestUpdateNote:
    def test_updates_note(self, board: DocPinBoard):
        board.pin("alice", "d1", note="old")
        board.update_note("alice", "d1", "new")
        assert board.get_pin("alice", "d1").note == "new"

    def test_returns_true_when_found(self, board: DocPinBoard):
        board.pin("alice", "d1")
        assert board.update_note("alice", "d1", "x") is True

    def test_returns_false_when_not_found(self, board: DocPinBoard):
        assert board.update_note("alice", "nope", "x") is False

    def test_empty_note(self, board: DocPinBoard):
        board.pin("alice", "d1", note="something")
        board.update_note("alice", "d1", "")
        assert board.get_pin("alice", "d1").note == ""


# ---------------------------------------------------------------------------
# unpin_all
# ---------------------------------------------------------------------------


class TestUnpinAll:
    def test_count_returned(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("alice", "d3")
        assert board.unpin_all("alice") == 3

    def test_zero_for_unknown_user(self, board: DocPinBoard):
        assert board.unpin_all("ghost") == 0

    def test_user_removed_from_all_users(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.unpin_all("alice")
        assert "alice" not in board.all_users()

    def test_does_not_affect_other_users(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        board.unpin_all("alice")
        assert board.is_pinned("bob", "d1") is True

    def test_pins_removed_from_store(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.unpin_all("alice")
        assert board.get_pin("alice", "d1") is None
        assert board.get_pin("alice", "d2") is None


# ---------------------------------------------------------------------------
# all_users
# ---------------------------------------------------------------------------


class TestAllUsers:
    def test_empty(self, board: DocPinBoard):
        assert board.all_users() == []

    def test_sorted(self, board: DocPinBoard):
        board.pin("charlie", "d1")
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        assert board.all_users() == ["alice", "bob", "charlie"]

    def test_only_users_with_pins(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        board.unpin_all("alice")
        assert board.all_users() == ["bob"]

    def test_no_duplicates(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        assert board.all_users() == ["alice"]


# ---------------------------------------------------------------------------
# all_pinned_docs
# ---------------------------------------------------------------------------


class TestAllPinnedDocs:
    def test_empty(self, board: DocPinBoard):
        assert board.all_pinned_docs() == []

    def test_sorted_unique(self, board: DocPinBoard):
        board.pin("alice", "doc_c")
        board.pin("bob", "doc_a")
        board.pin("charlie", "doc_b")
        board.pin("alice", "doc_a")  # doc_a pinned by two users
        assert board.all_pinned_docs() == ["doc_a", "doc_b", "doc_c"]

    def test_removed_after_unpin(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        board.unpin("alice", "d1")
        board.unpin("bob", "d1")
        assert board.all_pinned_docs() == []


# ---------------------------------------------------------------------------
# stats
# ---------------------------------------------------------------------------


class TestStats:
    def test_empty_stats(self, board: DocPinBoard):
        s = board.stats()
        assert s.total_pins == 0
        assert s.unique_users == 0
        assert s.unique_docs == 0
        assert s.avg_pins_per_user == 0.0

    def test_total_pins(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("bob", "d1")
        assert board.stats().total_pins == 3

    def test_unique_users(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("bob", "d1")
        assert board.stats().unique_users == 2

    def test_unique_docs(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("bob", "d1")  # d1 shared
        assert board.stats().unique_docs == 2

    def test_avg_pins_per_user(self, board: DocPinBoard):
        board.pin("alice", "d1")
        board.pin("alice", "d2")
        board.pin("bob", "d1")
        s = board.stats()
        # 3 total / 2 users = 1.5
        assert s.avg_pins_per_user == pytest.approx(1.5)

    def test_avg_zero_when_no_users(self, board: DocPinBoard):
        assert board.stats().avg_pins_per_user == 0.0


# ---------------------------------------------------------------------------
# Thread safety
# ---------------------------------------------------------------------------


class TestThreadSafety:
    def test_concurrent_pin_calls(self, board: DocPinBoard):
        """Multiple threads pinning distinct docs for the same user must
        all succeed and leave a consistent state."""
        errors: list[Exception] = []
        n_threads = 20
        n_docs_per_thread = 10

        def worker(thread_idx: int) -> None:
            try:
                for i in range(n_docs_per_thread):
                    doc_id = f"doc_{thread_idx}_{i}"
                    board.pin(f"user_{thread_idx}", doc_id)
            except Exception as exc:
                errors.append(exc)

        threads = [
            threading.Thread(target=worker, args=(t,)) for t in range(n_threads)
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert errors == [], f"Exceptions in threads: {errors}"
        s = board.stats()
        assert s.total_pins == n_threads * n_docs_per_thread
        assert s.unique_users == n_threads

    def test_concurrent_pin_and_unpin(self, board: DocPinBoard):
        """Interleaved pin/unpin from different threads should not corrupt
        internal structures."""
        for i in range(50):
            board.pin("shared_user", f"doc_{i}")

        errors: list[Exception] = []

        def pinner() -> None:
            try:
                for i in range(50, 100):
                    board.pin("shared_user", f"doc_{i}")
            except Exception as exc:
                errors.append(exc)

        def unpinner() -> None:
            try:
                for i in range(50):
                    board.unpin("shared_user", f"doc_{i}")
            except Exception as exc:
                errors.append(exc)

        t1 = threading.Thread(target=pinner)
        t2 = threading.Thread(target=unpinner)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert errors == [], f"Exceptions in threads: {errors}"
        # Positions must be sequential with no gaps
        pins = board.pins_for_user("shared_user")
        positions = sorted(p.position for p in pins)
        assert positions == list(range(len(pins)))
