"""ConversationMemory — high-level facade for managing a single conversation."""
from __future__ import annotations

from typing import Optional

from docstoolkit.conv_memory.store import ConversationStore
from docstoolkit.conv_memory.turn import ConversationTurn, Role
from docstoolkit.conv_memory.window import MemoryWindow, WindowStrategy


class ConversationMemory:
    """High-level interface for a single conversation session.

    Parameters
    ----------
    session_id:
        Explicit session ID to use.  If ``None``, a new session is created
        automatically with an auto-generated ID.
    window:
        Windowing strategy applied when :meth:`context` is called with
        ``apply_window=True``.  Defaults to ``LAST_N`` with size 10.
    store:
        Backing store.  If ``None``, a fresh in-memory
        :class:`ConversationStore` is created.
    """

    def __init__(
        self,
        session_id: Optional[str] = None,
        window: Optional[MemoryWindow] = None,
        store: Optional[ConversationStore] = None,
    ) -> None:
        self._store = store if store is not None else ConversationStore()
        self._window = window if window is not None else MemoryWindow(
            strategy=WindowStrategy.LAST_N, size=10
        )
        self._session_id = self._store.new_session(session_id)

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def add(self, role: Role, content: str, **metadata) -> ConversationTurn:
        """Create and persist a new turn, returning it."""
        turn = ConversationTurn(role=role, content=content, metadata=dict(metadata))
        self._store.add_turn(self._session_id, turn)
        return turn

    def context(self, apply_window: bool = True) -> list[ConversationTurn]:
        """Return conversation turns, optionally filtered by the window strategy."""
        turns = self._store.get_turns(self._session_id)
        if apply_window:
            return self._window.apply(turns)
        return turns

    def last_n(self, n: int) -> list[ConversationTurn]:
        """Return the last *n* turns in chronological order."""
        return self._store.get_turns(self._session_id, limit=n)

    def questions(self) -> list[ConversationTurn]:
        """Return all turns identified as questions."""
        return [t for t in self._store.get_turns(self._session_id) if t.is_question()]

    def clear(self) -> int:
        """Delete the current session (and all its turns).

        Returns the number of turns deleted.  The session ID is permanently
        gone after this call; the object should not be reused.
        """
        return self._store.delete_session(self._session_id)

    def session_id(self) -> str:
        """Return the current session ID."""
        return self._session_id
