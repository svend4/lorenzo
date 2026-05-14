"""E323 DocWorkflowState core implementation.

A small state machine for document workflow status. Pure stdlib, thread-safe.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StateTransition:
    """A defined transition from one state to another via a named action."""

    from_state: str
    to_state: str
    action: str


@dataclass
class StateRecord:
    """Current (or historical) state record for a document."""

    doc_id: str
    state: str
    entered_at: float = 0.0
    entered_by: str = ""
    previous_state: Optional[str] = None


@dataclass
class WorkflowStats:
    """Aggregate statistics for the workflow state machine."""

    total_docs: int = 0
    total_transitions: int = 0
    state_counts: dict = field(default_factory=dict)


class DocWorkflowState:
    """State machine for document workflow status.

    Transitions are defined as ``(from_state, action) -> to_state``. Each
    document has a current :class:`StateRecord` and a history of previous
    records preserved in insertion order.
    """

    def __init__(self) -> None:
        self._transitions: dict[tuple, str] = {}
        self._states: dict[str, StateRecord] = {}
        self._history: dict[str, list[StateRecord]] = {}
        self._lock = threading.Lock()

    # ---- transition definitions -------------------------------------------------

    def define_transition(self, from_state: str, action: str, to_state: str) -> None:
        """Register a transition. Replaces existing transition for same (from_state, action)."""
        with self._lock:
            self._transitions[(from_state, action)] = to_state

    def remove_transition(self, from_state: str, action: str) -> bool:
        """Remove a transition. Returns True if it existed."""
        with self._lock:
            return self._transitions.pop((from_state, action), None) is not None

    def list_transitions(self) -> list[StateTransition]:
        """Return all transitions, sorted by (from_state, action)."""
        with self._lock:
            items = sorted(self._transitions.items(), key=lambda kv: (kv[0][0], kv[0][1]))
            return [
                StateTransition(from_state=fs, to_state=ts, action=act)
                for (fs, act), ts in items
            ]

    # ---- state management -------------------------------------------------------

    def set_initial_state(
        self,
        doc_id: str,
        state: str,
        entered_by: str = "",
        now: Optional[float] = None,
    ) -> StateRecord:
        """Create the initial state record for a document (no previous_state)."""
        ts = now if now is not None else time.time()
        with self._lock:
            record = StateRecord(
                doc_id=doc_id,
                state=state,
                entered_at=ts,
                entered_by=entered_by,
                previous_state=None,
            )
            self._states[doc_id] = record
            self._history.setdefault(doc_id, [])
            return record

    def transition(
        self,
        doc_id: str,
        action: str,
        entered_by: str = "",
        now: Optional[float] = None,
    ) -> Optional[StateRecord]:
        """Execute a transition for a document via the given action.

        Returns the new :class:`StateRecord` on success, ``None`` if the
        document has no current state or no transition is defined for the
        ``(current_state, action)`` pair.
        """
        ts = now if now is not None else time.time()
        with self._lock:
            current = self._states.get(doc_id)
            if current is None:
                return None
            to_state = self._transitions.get((current.state, action))
            if to_state is None:
                return None
            # Append previous record to history.
            self._history.setdefault(doc_id, []).append(current)
            new_record = StateRecord(
                doc_id=doc_id,
                state=to_state,
                entered_at=ts,
                entered_by=entered_by,
                previous_state=current.state,
            )
            self._states[doc_id] = new_record
            return new_record

    def current_state(self, doc_id: str) -> Optional[StateRecord]:
        """Return the current StateRecord or None if unknown."""
        with self._lock:
            return self._states.get(doc_id)

    def state_of(self, doc_id: str) -> Optional[str]:
        """Convenience: return the current state name or None."""
        with self._lock:
            rec = self._states.get(doc_id)
            return rec.state if rec is not None else None

    def history_for(self, doc_id: str) -> list[StateRecord]:
        """Return past states in order; excludes the current state."""
        with self._lock:
            return list(self._history.get(doc_id, []))

    def docs_in_state(self, state: str) -> list[str]:
        """Return sorted doc_ids currently in the given state."""
        with self._lock:
            return sorted(
                doc_id
                for doc_id, rec in self._states.items()
                if rec.state == state
            )

    def available_actions(self, doc_id: str) -> list[str]:
        """Return sorted action names available for the document's current state.

        Empty list if the document has no current state.
        """
        with self._lock:
            current = self._states.get(doc_id)
            if current is None:
                return []
            return sorted(
                action
                for (fs, action) in self._transitions
                if fs == current.state
            )

    def all_states(self) -> list[str]:
        """Return sorted unique state names from transitions and current states."""
        with self._lock:
            states: set = set()
            for (fs, _), ts in self._transitions.items():
                states.add(fs)
                states.add(ts)
            for rec in self._states.values():
                states.add(rec.state)
            return sorted(states)

    def stats(self) -> WorkflowStats:
        """Return aggregate statistics."""
        with self._lock:
            counts: dict = {}
            for rec in self._states.values():
                counts[rec.state] = counts.get(rec.state, 0) + 1
            return WorkflowStats(
                total_docs=len(self._states),
                total_transitions=len(self._transitions),
                state_counts=counts,
            )
