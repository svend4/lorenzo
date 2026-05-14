"""E409 DocWorkflowStateV2 core implementation.

Enhanced state machine with guard conditions, transition counts and history.
Pure stdlib, thread-safe via :class:`threading.Lock`.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StateGuard:
    """A named condition that must return True for a transition to proceed.

    ``condition`` is an optional callable accepting ``(doc_id, context_dict)``
    and returning a truthy value to allow the transition. When ``condition`` is
    ``None`` the guard is treated as always passing.
    """

    name: str
    condition: object = None


@dataclass
class Transition:
    """A defined transition from one state to another via a named action.

    The transition only fires when every guard's ``condition`` returns truthy.
    """

    from_state: str
    to_state: str
    action: str
    guards: list = field(default_factory=list)


@dataclass
class StateRecord:
    """Current (or historical) state record for a document."""

    doc_id: str
    state: str
    entered_at: float = 0.0
    entered_by: str = ""
    previous_state: Optional[str] = None
    transition_count: int = 0


@dataclass
class WorkflowStatsV2:
    """Aggregate statistics for the v2 workflow state machine."""

    total_docs: int = 0
    total_transitions: int = 0
    state_counts: dict = field(default_factory=dict)
    guard_failures: int = 0


class DocWorkflowStateV2:
    """Enhanced state machine for document workflow status.

    Transitions are keyed by ``(from_state, action)``. Each transition may
    declare an ordered list of :class:`StateGuard` instances; every guard's
    ``condition`` must return truthy for the transition to fire. If any guard
    rejects the move, the transition does not happen and the internal
    ``guard_failures`` counter is incremented.
    """

    def __init__(self) -> None:
        self._transitions: dict[tuple, Transition] = {}
        self._states: dict[str, StateRecord] = {}
        self._history: dict[str, list[StateRecord]] = {}
        self._guard_failures: int = 0
        self._lock = threading.Lock()

    # ---- transition definitions -------------------------------------------------

    def define_transition(self, transition: Transition) -> None:
        """Register a transition. Replaces existing transition for same key."""
        with self._lock:
            self._transitions[(transition.from_state, transition.action)] = transition

    def remove_transition(self, from_state: str, action: str) -> bool:
        """Remove a transition. Returns True if it existed."""
        with self._lock:
            return self._transitions.pop((from_state, action), None) is not None

    def list_transitions(self) -> list[Transition]:
        """Return all transitions, sorted by ``(from_state, action)``."""
        with self._lock:
            items = sorted(
                self._transitions.items(), key=lambda kv: (kv[0][0], kv[0][1])
            )
            return [t for _, t in items]

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
                transition_count=0,
            )
            self._states[doc_id] = record
            self._history.setdefault(doc_id, [])
            return record

    def transition(
        self,
        doc_id: str,
        action: str,
        context: Optional[dict] = None,
        entered_by: str = "",
        now: Optional[float] = None,
    ) -> Optional[StateRecord]:
        """Execute a transition if all guards pass.

        Returns the new :class:`StateRecord` on success, ``None`` if the
        document is unknown, no transition is defined for
        ``(current_state, action)``, or any guard rejects. Guard rejection
        increments :attr:`_guard_failures`.
        """
        ts = now if now is not None else time.time()
        ctx = context if context is not None else {}
        with self._lock:
            current = self._states.get(doc_id)
            if current is None:
                return None
            transition = self._transitions.get((current.state, action))
            if transition is None:
                return None
            # Evaluate guards in declaration order.
            for guard in transition.guards:
                cond = guard.condition
                if cond is None:
                    continue
                try:
                    ok = bool(cond(doc_id, ctx))
                except Exception:
                    ok = False
                if not ok:
                    self._guard_failures += 1
                    return None
            # All guards passed — perform the transition.
            self._history.setdefault(doc_id, []).append(current)
            new_record = StateRecord(
                doc_id=doc_id,
                state=transition.to_state,
                entered_at=ts,
                entered_by=entered_by,
                previous_state=current.state,
                transition_count=current.transition_count + 1,
            )
            self._states[doc_id] = new_record
            return new_record

    def current_state(self, doc_id: str) -> Optional[StateRecord]:
        """Return the current StateRecord or None if unknown."""
        with self._lock:
            return self._states.get(doc_id)

    def state_of(self, doc_id: str) -> Optional[str]:
        """Return the current state name or None."""
        with self._lock:
            rec = self._states.get(doc_id)
            return rec.state if rec is not None else None

    def history_for(self, doc_id: str) -> list[StateRecord]:
        """Return past states in order; excludes the current state."""
        with self._lock:
            return list(self._history.get(doc_id, []))

    def available_actions(self, doc_id: str) -> list[str]:
        """Return sorted action names defined for the document's current state.

        Empty list if the document has no current state. Guards are not
        evaluated here — only structurally defined actions are returned.
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

    def docs_in_state(self, state: str) -> list[str]:
        """Return sorted doc_ids currently in the given state."""
        with self._lock:
            return sorted(
                doc_id
                for doc_id, rec in self._states.items()
                if rec.state == state
            )

    def stats(self) -> WorkflowStatsV2:
        """Return aggregate statistics."""
        with self._lock:
            counts: dict = {}
            for rec in self._states.values():
                counts[rec.state] = counts.get(rec.state, 0) + 1
            return WorkflowStatsV2(
                total_docs=len(self._states),
                total_transitions=len(self._transitions),
                state_counts=counts,
                guard_failures=self._guard_failures,
            )
