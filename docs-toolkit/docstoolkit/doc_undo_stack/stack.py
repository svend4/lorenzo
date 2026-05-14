"""Generic undo/redo command stack.

Implements a command-pattern undo/redo stack with optional grouping of
related commands, capacity (max_history) enforcement that drops the oldest
applied commands, and thread-safe operations via threading.Lock.

Unlike doc_history, this module is generic: each command stores explicit
do/undo callables rather than per-document edit content.
"""
from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Command:
    """A single undoable command (do/undo callables)."""

    command_id: str
    description: str
    do_func: Callable[[], Any]
    undo_func: Callable[[], Any]
    executed: bool = False
    created_at: float = 0.0
    group_id: Optional[str] = None


@dataclass
class StackState:
    """Snapshot of the undo/redo stack state."""

    applied_count: int
    undone_count: int
    total_commands: int
    can_undo: bool
    can_redo: bool


class DocUndoStack:
    """Thread-safe generic undo/redo stack.

    Maintains two stacks: applied (commands that have been executed) and
    undone (commands available for redo). Pushing a new command via do or
    register clears the undone stack.
    """

    def __init__(self, max_history: int = 100) -> None:
        if max_history < 1:
            raise ValueError("max_history must be >= 1")
        self._max_history = max_history
        self._applied: List[Command] = []
        self._undone: List[Command] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _push_applied(self, cmd: Command) -> None:
        """Push to applied stack, trimming oldest if over capacity."""
        self._applied.append(cmd)
        if len(self._applied) > self._max_history:
            # drop oldest applied commands
            overflow = len(self._applied) - self._max_history
            del self._applied[:overflow]

    # ------------------------------------------------------------------
    # Command creation
    # ------------------------------------------------------------------
    def do(
        self,
        description: str,
        do_func: Callable[[], Any],
        undo_func: Callable[[], Any],
        group_id: Optional[str] = None,
        now: float = 0.0,
    ) -> Command:
        """Execute do_func and push the command onto the applied stack.

        Clears the redo (undone) stack.
        """
        with self._lock:
            cmd = Command(
                command_id=str(uuid.uuid4()),
                description=description,
                do_func=do_func,
                undo_func=undo_func,
                executed=False,
                created_at=now,
                group_id=group_id,
            )
            # Execute
            do_func()
            cmd.executed = True
            self._push_applied(cmd)
            # New action invalidates redo stack
            self._undone.clear()
            return cmd

    def register(
        self,
        description: str,
        do_func: Callable[[], Any],
        undo_func: Callable[[], Any],
        group_id: Optional[str] = None,
        now: float = 0.0,
    ) -> Command:
        """Register a command without executing do_func.

        The caller is responsible for having already applied the effect.
        Clears the redo (undone) stack.
        """
        with self._lock:
            cmd = Command(
                command_id=str(uuid.uuid4()),
                description=description,
                do_func=do_func,
                undo_func=undo_func,
                executed=False,
                created_at=now,
                group_id=group_id,
            )
            self._push_applied(cmd)
            self._undone.clear()
            return cmd

    # ------------------------------------------------------------------
    # Undo / redo
    # ------------------------------------------------------------------
    def undo(self, now: float = 0.0) -> Optional[Command]:
        """Pop the most recent applied command, call its undo_func."""
        with self._lock:
            if not self._applied:
                return None
            cmd = self._applied.pop()
            cmd.undo_func()
            cmd.executed = False
            cmd.created_at = now if now else cmd.created_at
            self._undone.append(cmd)
            return cmd

    def redo(self, now: float = 0.0) -> Optional[Command]:
        """Pop the most recent undone command, call its do_func."""
        with self._lock:
            if not self._undone:
                return None
            cmd = self._undone.pop()
            cmd.do_func()
            cmd.executed = True
            cmd.created_at = now if now else cmd.created_at
            # Capacity-aware push
            self._push_applied(cmd)
            return cmd

    def undo_group(self, group_id: str, now: float = 0.0) -> int:
        """Undo every applied command with the given group_id.

        Commands are undone in reverse order of how they appear in the
        applied stack (most recent first). Returns the number of commands
        undone.
        """
        with self._lock:
            # iterate applied from top (end) to bottom (start)
            count = 0
            # Build list of indices to remove (in descending order)
            indices = [
                i
                for i in range(len(self._applied) - 1, -1, -1)
                if self._applied[i].group_id == group_id
            ]
            for i in indices:
                cmd = self._applied.pop(i)
                cmd.undo_func()
                cmd.executed = False
                cmd.created_at = now if now else cmd.created_at
                self._undone.append(cmd)
                count += 1
            return count

    def redo_group(self, group_id: str, now: float = 0.0) -> int:
        """Redo every undone command with the given group_id.

        Returns the number of commands re-applied.
        """
        with self._lock:
            count = 0
            indices = [
                i
                for i in range(len(self._undone) - 1, -1, -1)
                if self._undone[i].group_id == group_id
            ]
            for i in indices:
                cmd = self._undone.pop(i)
                cmd.do_func()
                cmd.executed = True
                cmd.created_at = now if now else cmd.created_at
                self._push_applied(cmd)
                count += 1
            return count

    # ------------------------------------------------------------------
    # Peek / can_*
    # ------------------------------------------------------------------
    def peek_undo(self) -> Optional[Command]:
        """Return the next command to be undone, without modifying state."""
        with self._lock:
            if not self._applied:
                return None
            return self._applied[-1]

    def peek_redo(self) -> Optional[Command]:
        """Return the next command to be redone, without modifying state."""
        with self._lock:
            if not self._undone:
                return None
            return self._undone[-1]

    def can_undo(self) -> bool:
        """Return True if there is at least one applied command."""
        with self._lock:
            return bool(self._applied)

    def can_redo(self) -> bool:
        """Return True if there is at least one undone command."""
        with self._lock:
            return bool(self._undone)

    # ------------------------------------------------------------------
    # Bulk operations
    # ------------------------------------------------------------------
    def clear(self) -> None:
        """Clear both applied and undone stacks."""
        with self._lock:
            self._applied.clear()
            self._undone.clear()

    def clear_redo(self) -> int:
        """Clear the undone (redo) stack. Returns number cleared."""
        with self._lock:
            n = len(self._undone)
            self._undone.clear()
            return n

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------
    def state(self) -> StackState:
        """Return a snapshot of the current stack state."""
        with self._lock:
            return StackState(
                applied_count=len(self._applied),
                undone_count=len(self._undone),
                total_commands=len(self._applied) + len(self._undone),
                can_undo=bool(self._applied),
                can_redo=bool(self._undone),
            )

    def applied_history(self, limit: Optional[int] = None) -> List[Command]:
        """Return applied commands, most recent first."""
        with self._lock:
            history = list(reversed(self._applied))
            if limit is not None:
                history = history[:limit]
            return history

    def undone_history(self, limit: Optional[int] = None) -> List[Command]:
        """Return undone commands, most recent first."""
        with self._lock:
            history = list(reversed(self._undone))
            if limit is not None:
                history = history[:limit]
            return history

    def find_command(self, command_id: str) -> Optional[Command]:
        """Find a command by id in either stack."""
        with self._lock:
            for cmd in self._applied:
                if cmd.command_id == command_id:
                    return cmd
            for cmd in self._undone:
                if cmd.command_id == command_id:
                    return cmd
            return None

    def find_by_group(self, group_id: str) -> List[Command]:
        """Return all commands in the given group (applied first, then undone).

        Order within each stack is from oldest to newest.
        """
        with self._lock:
            results = [c for c in self._applied if c.group_id == group_id]
            results.extend(c for c in self._undone if c.group_id == group_id)
            return results

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------
    @property
    def applied_count(self) -> int:
        with self._lock:
            return len(self._applied)

    @property
    def undone_count(self) -> int:
        with self._lock:
            return len(self._undone)

    @property
    def total_commands(self) -> int:
        with self._lock:
            return len(self._applied) + len(self._undone)
