"""Tests for docstoolkit.doc_undo_stack."""
from __future__ import annotations

import pytest

from docstoolkit.doc_undo_stack import Command, DocUndoStack, StackState


# ---------------------------------------------------------------------------
# Helpers: simple counter object used as a do/undo target
# ---------------------------------------------------------------------------
class Counter:
    def __init__(self, value: int = 0) -> None:
        self.value = value

    def inc(self) -> None:
        self.value += 1

    def dec(self) -> None:
        self.value -= 1

    def add(self, n: int):
        def _do():
            self.value += n

        def _undo():
            self.value -= n

        return _do, _undo


# ---------------------------------------------------------------------------
class TestCommand:
    def test_create_minimal(self):
        cmd = Command(
            command_id="c1",
            description="d",
            do_func=lambda: None,
            undo_func=lambda: None,
        )
        assert cmd.command_id == "c1"
        assert cmd.description == "d"
        assert cmd.executed is False
        assert cmd.created_at == 0.0
        assert cmd.group_id is None

    def test_create_with_all_fields(self):
        f = lambda: 1
        g = lambda: 2
        cmd = Command(
            command_id="x",
            description="desc",
            do_func=f,
            undo_func=g,
            executed=True,
            created_at=123.0,
            group_id="grp",
        )
        assert cmd.executed is True
        assert cmd.created_at == 123.0
        assert cmd.group_id == "grp"
        assert cmd.do_func is f
        assert cmd.undo_func is g

    def test_callables_invokable(self):
        c = Counter()
        cmd = Command("id", "desc", c.inc, c.dec)
        cmd.do_func()
        assert c.value == 1
        cmd.undo_func()
        assert c.value == 0


# ---------------------------------------------------------------------------
class TestStackState:
    def test_fields(self):
        s = StackState(
            applied_count=3,
            undone_count=2,
            total_commands=5,
            can_undo=True,
            can_redo=True,
        )
        assert s.applied_count == 3
        assert s.undone_count == 2
        assert s.total_commands == 5
        assert s.can_undo is True
        assert s.can_redo is True

    def test_empty_state(self):
        s = StackState(
            applied_count=0,
            undone_count=0,
            total_commands=0,
            can_undo=False,
            can_redo=False,
        )
        assert s.can_undo is False
        assert s.can_redo is False


# ---------------------------------------------------------------------------
class TestDo:
    def test_do_executes_function(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        assert c.value == 1

    def test_do_returns_command(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("inc", c.inc, c.dec)
        assert isinstance(cmd, Command)
        assert cmd.description == "inc"
        assert cmd.executed is True

    def test_do_pushes_to_applied(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        assert stack.applied_count == 1

    def test_do_assigns_unique_ids(self):
        stack = DocUndoStack()
        c = Counter()
        cmd1 = stack.do("a", c.inc, c.dec)
        cmd2 = stack.do("b", c.inc, c.dec)
        assert cmd1.command_id != cmd2.command_id

    def test_do_records_now(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("inc", c.inc, c.dec, now=42.5)
        assert cmd.created_at == 42.5

    def test_do_with_group_id(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("inc", c.inc, c.dec, group_id="grp1")
        assert cmd.group_id == "grp1"


# ---------------------------------------------------------------------------
class TestRegister:
    def test_register_does_not_execute(self):
        stack = DocUndoStack()
        c = Counter()
        stack.register("inc", c.inc, c.dec)
        assert c.value == 0

    def test_register_pushes_to_applied(self):
        stack = DocUndoStack()
        c = Counter()
        stack.register("inc", c.inc, c.dec)
        assert stack.applied_count == 1

    def test_register_returns_command_not_executed(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.register("inc", c.inc, c.dec)
        assert cmd.executed is False

    def test_register_with_group(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.register("inc", c.inc, c.dec, group_id="g", now=10.0)
        assert cmd.group_id == "g"
        assert cmd.created_at == 10.0


# ---------------------------------------------------------------------------
class TestUndo:
    def test_undo_empty_returns_none(self):
        stack = DocUndoStack()
        assert stack.undo() is None

    def test_undo_calls_undo_func(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        stack.undo()
        assert c.value == 0

    def test_undo_returns_command(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        cmd = stack.undo()
        assert isinstance(cmd, Command)
        assert cmd.description == "inc"

    def test_undo_moves_to_undone_stack(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        stack.undo()
        assert stack.applied_count == 0
        assert stack.undone_count == 1

    def test_undo_marks_not_executed(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        cmd = stack.undo()
        assert cmd.executed is False


# ---------------------------------------------------------------------------
class TestRedo:
    def test_redo_empty_returns_none(self):
        stack = DocUndoStack()
        assert stack.redo() is None

    def test_redo_after_undo_calls_do_func(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        stack.undo()
        assert c.value == 0
        stack.redo()
        assert c.value == 1

    def test_redo_moves_to_applied(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        stack.undo()
        stack.redo()
        assert stack.applied_count == 1
        assert stack.undone_count == 0

    def test_redo_marks_executed(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("inc", c.inc, c.dec)
        stack.undo()
        cmd = stack.redo()
        assert cmd.executed is True


# ---------------------------------------------------------------------------
class TestUndoRedoSequence:
    def test_multi_undo_then_redo(self):
        stack = DocUndoStack()
        c = Counter()
        for _ in range(5):
            stack.do("inc", c.inc, c.dec)
        assert c.value == 5
        for _ in range(3):
            stack.undo()
        assert c.value == 2
        for _ in range(3):
            stack.redo()
        assert c.value == 5

    def test_order_lifo(self):
        stack = DocUndoStack()
        c = Counter()
        do1, undo1 = c.add(1)
        do2, undo2 = c.add(10)
        do3, undo3 = c.add(100)
        stack.do("a", do1, undo1)
        stack.do("b", do2, undo2)
        stack.do("c", do3, undo3)
        assert c.value == 111
        stack.undo()
        assert c.value == 11
        stack.undo()
        assert c.value == 1
        stack.redo()
        assert c.value == 11

    def test_full_undo_full_redo(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.undo()
        assert stack.undo() is None
        assert c.value == 0
        stack.redo()
        stack.redo()
        assert stack.redo() is None
        assert c.value == 2


# ---------------------------------------------------------------------------
class TestNewDoClearsRedo:
    def test_do_clears_redo_stack(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        assert stack.undone_count == 1
        stack.do("c", c.inc, c.dec)
        assert stack.undone_count == 0

    def test_register_clears_redo_stack(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        assert stack.undone_count == 1
        stack.register("b", c.inc, c.dec)
        assert stack.undone_count == 0

    def test_redo_does_not_clear_redo(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.undo()
        assert stack.undone_count == 2
        stack.redo()
        # one moved out of undone — not because of "clear"
        assert stack.undone_count == 1


# ---------------------------------------------------------------------------
class TestUndoGroup:
    def test_undo_group_returns_count(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.do("c", c.inc, c.dec, group_id="other")
        n = stack.undo_group("g")
        assert n == 2

    def test_undo_group_runs_undo_funcs(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.do("c", c.inc, c.dec, group_id="other")
        assert c.value == 3
        stack.undo_group("g")
        assert c.value == 1

    def test_undo_group_only_targets_group(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="other")
        stack.undo_group("g")
        assert stack.applied_count == 1
        assert stack.applied_history()[0].group_id == "other"

    def test_undo_group_missing_returns_zero(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        assert stack.undo_group("nonexistent") == 0

    def test_undo_group_moves_to_undone(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.undo_group("g")
        assert stack.undone_count == 2


# ---------------------------------------------------------------------------
class TestRedoGroup:
    def test_redo_group_returns_count(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.undo_group("g")
        n = stack.redo_group("g")
        assert n == 2

    def test_redo_group_runs_do_funcs(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.undo_group("g")
        assert c.value == 0
        stack.redo_group("g")
        assert c.value == 2

    def test_redo_group_missing_returns_zero(self):
        stack = DocUndoStack()
        assert stack.redo_group("none") == 0

    def test_redo_group_moves_to_applied(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.undo_group("g")
        stack.redo_group("g")
        assert stack.applied_count == 1
        assert stack.undone_count == 0


# ---------------------------------------------------------------------------
class TestPeekUndo:
    def test_peek_undo_empty(self):
        stack = DocUndoStack()
        assert stack.peek_undo() is None

    def test_peek_undo_returns_top(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        cmd = stack.peek_undo()
        assert cmd.description == "b"

    def test_peek_undo_does_not_modify(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.peek_undo()
        assert stack.applied_count == 1
        assert c.value == 1


# ---------------------------------------------------------------------------
class TestPeekRedo:
    def test_peek_redo_empty(self):
        stack = DocUndoStack()
        assert stack.peek_redo() is None

    def test_peek_redo_returns_top(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        cmd = stack.peek_redo()
        assert cmd.description == "b"

    def test_peek_redo_does_not_modify(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        stack.peek_redo()
        assert stack.undone_count == 1


# ---------------------------------------------------------------------------
class TestCanUndoRedo:
    def test_can_undo_empty(self):
        stack = DocUndoStack()
        assert stack.can_undo() is False

    def test_can_undo_after_do(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        assert stack.can_undo() is True

    def test_can_redo_empty(self):
        stack = DocUndoStack()
        assert stack.can_redo() is False

    def test_can_redo_after_undo(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        assert stack.can_redo() is True

    def test_can_redo_cleared_by_new_do(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        stack.do("b", c.inc, c.dec)
        assert stack.can_redo() is False


# ---------------------------------------------------------------------------
class TestClear:
    def test_clear_empties_both(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.clear()
        assert stack.applied_count == 0
        assert stack.undone_count == 0

    def test_clear_when_empty(self):
        stack = DocUndoStack()
        stack.clear()
        assert stack.applied_count == 0


# ---------------------------------------------------------------------------
class TestClearRedo:
    def test_clear_redo_returns_count(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.undo()
        n = stack.clear_redo()
        assert n == 2

    def test_clear_redo_empties_undone(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        stack.clear_redo()
        assert stack.undone_count == 0

    def test_clear_redo_keeps_applied(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.clear_redo()
        assert stack.applied_count == 1

    def test_clear_redo_empty_returns_zero(self):
        stack = DocUndoStack()
        assert stack.clear_redo() == 0


# ---------------------------------------------------------------------------
class TestState:
    def test_state_empty(self):
        stack = DocUndoStack()
        s = stack.state()
        assert s.applied_count == 0
        assert s.undone_count == 0
        assert s.total_commands == 0
        assert s.can_undo is False
        assert s.can_redo is False

    def test_state_after_operations(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        s = stack.state()
        assert s.applied_count == 1
        assert s.undone_count == 1
        assert s.total_commands == 2
        assert s.can_undo is True
        assert s.can_redo is True


# ---------------------------------------------------------------------------
class TestAppliedHistory:
    def test_empty(self):
        stack = DocUndoStack()
        assert stack.applied_history() == []

    def test_most_recent_first(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.do("c", c.inc, c.dec)
        hist = stack.applied_history()
        assert [cmd.description for cmd in hist] == ["c", "b", "a"]

    def test_limit(self):
        stack = DocUndoStack()
        c = Counter()
        for ch in "abcd":
            stack.do(ch, c.inc, c.dec)
        hist = stack.applied_history(limit=2)
        assert [cmd.description for cmd in hist] == ["d", "c"]


# ---------------------------------------------------------------------------
class TestUndoneHistory:
    def test_empty(self):
        stack = DocUndoStack()
        assert stack.undone_history() == []

    def test_most_recent_first(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()  # b → undone
        stack.undo()  # a → undone (top)
        hist = stack.undone_history()
        assert [cmd.description for cmd in hist] == ["a", "b"]

    def test_limit(self):
        stack = DocUndoStack()
        c = Counter()
        for ch in "abc":
            stack.do(ch, c.inc, c.dec)
        for _ in range(3):
            stack.undo()
        hist = stack.undone_history(limit=1)
        assert len(hist) == 1


# ---------------------------------------------------------------------------
class TestFindCommand:
    def test_find_in_applied(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("a", c.inc, c.dec)
        found = stack.find_command(cmd.command_id)
        assert found is cmd

    def test_find_in_undone(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("a", c.inc, c.dec)
        stack.undo()
        found = stack.find_command(cmd.command_id)
        assert found is cmd

    def test_find_missing(self):
        stack = DocUndoStack()
        assert stack.find_command("nope") is None


# ---------------------------------------------------------------------------
class TestFindByGroup:
    def test_find_by_group_empty(self):
        stack = DocUndoStack()
        assert stack.find_by_group("g") == []

    def test_find_by_group_applied_only(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="other")
        stack.do("c", c.inc, c.dec, group_id="g")
        results = stack.find_by_group("g")
        assert [cmd.description for cmd in results] == ["a", "c"]

    def test_find_by_group_across_stacks(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec, group_id="g")
        stack.do("b", c.inc, c.dec, group_id="g")
        stack.undo()  # b → undone
        results = stack.find_by_group("g")
        descs = [cmd.description for cmd in results]
        assert "a" in descs
        assert "b" in descs


# ---------------------------------------------------------------------------
class TestMaxHistory:
    def test_drops_oldest_applied(self):
        stack = DocUndoStack(max_history=3)
        c = Counter()
        for ch in "abcd":
            stack.do(ch, c.inc, c.dec)
        assert stack.applied_count == 3
        hist = stack.applied_history()
        descs = [cmd.description for cmd in hist]
        # newest 3 should remain: d, c, b
        assert descs == ["d", "c", "b"]

    def test_default_capacity(self):
        stack = DocUndoStack()
        # default is 100; just exercise a large run
        c = Counter()
        for _ in range(150):
            stack.do("x", c.inc, c.dec)
        assert stack.applied_count == 100

    def test_invalid_capacity_raises(self):
        with pytest.raises(ValueError):
            DocUndoStack(max_history=0)

    def test_redo_respects_capacity(self):
        stack = DocUndoStack(max_history=2)
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.undo()
        # now 0 applied, 2 undone
        stack.redo()
        stack.redo()
        assert stack.applied_count == 2


# ---------------------------------------------------------------------------
class TestProperties:
    def test_applied_count_property(self):
        stack = DocUndoStack()
        c = Counter()
        assert stack.applied_count == 0
        stack.do("a", c.inc, c.dec)
        assert stack.applied_count == 1

    def test_undone_count_property(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        assert stack.undone_count == 0
        stack.undo()
        assert stack.undone_count == 1

    def test_total_commands_property(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        assert stack.total_commands == 2


# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_undo_when_only_redo_available_returns_none(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.undo()
        # applied is empty, undone has 1
        assert stack.undo() is None

    def test_redo_when_only_applied_available_returns_none(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        assert stack.redo() is None

    def test_unique_ids_under_many_operations(self):
        stack = DocUndoStack()
        c = Counter()
        ids = set()
        for _ in range(50):
            cmd = stack.do("x", c.inc, c.dec)
            ids.add(cmd.command_id)
        assert len(ids) == 50

    def test_now_param_optional(self):
        stack = DocUndoStack()
        c = Counter()
        cmd = stack.do("a", c.inc, c.dec)
        assert cmd.created_at == 0.0

    def test_group_with_register(self):
        stack = DocUndoStack()
        c = Counter()
        stack.register("a", c.inc, c.dec, group_id="g")
        stack.register("b", c.inc, c.dec, group_id="g")
        assert len(stack.find_by_group("g")) == 2

    def test_state_after_clear(self):
        stack = DocUndoStack()
        c = Counter()
        stack.do("a", c.inc, c.dec)
        stack.do("b", c.inc, c.dec)
        stack.undo()
        stack.clear()
        s = stack.state()
        assert s.total_commands == 0
        assert s.can_undo is False
        assert s.can_redo is False
