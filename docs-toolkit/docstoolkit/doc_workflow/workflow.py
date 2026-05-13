"""Document workflow implementation (E192).

State-machine-style workflows for documents with statuses, transitions,
role checks, optional condition guards, and audit history.
"""
from __future__ import annotations

import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Set


class WorkflowStatus(Enum):
    """All possible document workflow statuses."""

    DRAFT = "draft"
    REVIEW = "review"
    APPROVED = "approved"
    PUBLISHED = "published"
    REJECTED = "rejected"
    ARCHIVED = "archived"


_TERMINAL_STATUSES: Set[WorkflowStatus] = {
    WorkflowStatus.PUBLISHED,
    WorkflowStatus.REJECTED,
    WorkflowStatus.ARCHIVED,
}


@dataclass
class Transition:
    """A declared transition from one status to another.

    Optionally guarded by a required role and/or a callable condition that
    receives the current ``DocState`` and returns ``True`` if the transition
    is allowed.
    """

    from_status: WorkflowStatus
    to_status: WorkflowStatus
    required_role: Optional[str] = None
    condition: Optional[Callable[["DocState"], bool]] = None


@dataclass
class DocState:
    """Runtime state for a tracked document."""

    doc_id: str
    status: WorkflowStatus
    assigned_to: Optional[str] = None
    history: List[dict] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: float = 0.0
    updated_at: float = 0.0


@dataclass
class TransitionResult:
    """Outcome of a ``DocWorkflow.transition`` call."""

    success: bool
    new_status: Optional[WorkflowStatus]
    reason: str


class WorkflowDefinition:
    """Declarative set of allowed transitions for a workflow."""

    def __init__(self, name: str) -> None:
        self.name = name
        self._transitions: List[Transition] = []

    def add_transition(
        self,
        from_status: WorkflowStatus,
        to_status: WorkflowStatus,
        required_role: Optional[str] = None,
        condition: Optional[Callable[[DocState], bool]] = None,
    ) -> Transition:
        """Register a transition and return its descriptor."""
        transition = Transition(
            from_status=from_status,
            to_status=to_status,
            required_role=required_role,
            condition=condition,
        )
        self._transitions.append(transition)
        return transition

    def allowed_transitions(
        self, from_status: WorkflowStatus
    ) -> List[Transition]:
        """Return all transitions departing from ``from_status``."""
        return [t for t in self._transitions if t.from_status == from_status]

    def is_valid_transition(
        self, from_s: WorkflowStatus, to_s: WorkflowStatus
    ) -> bool:
        """Whether any declared transition links ``from_s`` to ``to_s``."""
        return any(
            t.from_status == from_s and t.to_status == to_s
            for t in self._transitions
        )

    def find_transition(
        self, from_s: WorkflowStatus, to_s: WorkflowStatus
    ) -> Optional[Transition]:
        """Return the first transition matching from/to, or ``None``."""
        for t in self._transitions:
            if t.from_status == from_s and t.to_status == to_s:
                return t
        return None

    def terminal_statuses(self) -> Set[WorkflowStatus]:
        """Statuses considered terminal (no outgoing transitions allowed)."""
        return set(_TERMINAL_STATUSES)


class DocWorkflow:
    """Tracks document states and applies transitions per a definition."""

    def __init__(self, definition: WorkflowDefinition) -> None:
        self.definition = definition
        self._docs: Dict[str, DocState] = {}
        self._lock = threading.Lock()

    def register(
        self,
        doc_id: str,
        initial_status: WorkflowStatus = WorkflowStatus.DRAFT,
        assigned_to: Optional[str] = None,
        now: float = 0.0,
    ) -> DocState:
        """Register a new document and return its state."""
        with self._lock:
            if doc_id in self._docs:
                return self._docs[doc_id]
            state = DocState(
                doc_id=doc_id,
                status=initial_status,
                assigned_to=assigned_to,
                created_at=now,
                updated_at=now,
            )
            self._docs[doc_id] = state
            return state

    def get(self, doc_id: str) -> Optional[DocState]:
        """Fetch a document state or ``None`` if unknown."""
        with self._lock:
            return self._docs.get(doc_id)

    def transition(
        self,
        doc_id: str,
        to_status: WorkflowStatus,
        actor: str,
        user_role: Optional[str] = None,
        now: float = 0.0,
    ) -> TransitionResult:
        """Attempt to move ``doc_id`` into ``to_status``."""
        with self._lock:
            state = self._docs.get(doc_id)
            if state is None:
                return TransitionResult(
                    success=False,
                    new_status=None,
                    reason="unknown_doc",
                )

            if state.status in _TERMINAL_STATUSES:
                return TransitionResult(
                    success=False,
                    new_status=state.status,
                    reason="terminal_status",
                )

            transition = self.definition.find_transition(
                state.status, to_status
            )
            if transition is None:
                return TransitionResult(
                    success=False,
                    new_status=state.status,
                    reason="invalid_transition",
                )

            if transition.required_role is not None:
                if user_role != transition.required_role:
                    return TransitionResult(
                        success=False,
                        new_status=state.status,
                        reason="role_mismatch",
                    )

            if transition.condition is not None:
                try:
                    ok = bool(transition.condition(state))
                except Exception:
                    ok = False
                if not ok:
                    return TransitionResult(
                        success=False,
                        new_status=state.status,
                        reason="condition_failed",
                    )

            from_status = state.status
            state.status = to_status
            state.updated_at = now
            state.history.append(
                {
                    "from": from_status,
                    "to": to_status,
                    "actor": actor,
                    "timestamp": now,
                    "role": user_role,
                }
            )
            return TransitionResult(
                success=True,
                new_status=to_status,
                reason="ok",
            )

    def assign(self, doc_id: str, user_id: str) -> bool:
        """Assign ``doc_id`` to ``user_id``."""
        with self._lock:
            state = self._docs.get(doc_id)
            if state is None:
                return False
            state.assigned_to = user_id
            return True

    def metadata_update(self, doc_id: str, updates: dict) -> bool:
        """Merge ``updates`` into the document's metadata dict."""
        with self._lock:
            state = self._docs.get(doc_id)
            if state is None:
                return False
            state.metadata.update(updates)
            return True

    def history(self, doc_id: str) -> List[dict]:
        """Return a copy of the transition history for ``doc_id``."""
        with self._lock:
            state = self._docs.get(doc_id)
            if state is None:
                return []
            return list(state.history)

    def docs_in_status(self, status: WorkflowStatus) -> List[DocState]:
        """List all documents currently in ``status``."""
        with self._lock:
            return [s for s in self._docs.values() if s.status == status]

    def docs_assigned_to(self, user_id: str) -> List[DocState]:
        """List documents currently assigned to ``user_id``."""
        with self._lock:
            return [
                s for s in self._docs.values() if s.assigned_to == user_id
            ]

    def is_terminal(self, doc_id: str) -> bool:
        """Whether the document exists and sits in a terminal status."""
        with self._lock:
            state = self._docs.get(doc_id)
            if state is None:
                return False
            return state.status in _TERMINAL_STATUSES

    def count_by_status(self) -> Dict[WorkflowStatus, int]:
        """Count documents per status (every status present in result)."""
        counts: Dict[WorkflowStatus, int] = {s: 0 for s in WorkflowStatus}
        with self._lock:
            for state in self._docs.values():
                counts[state.status] += 1
        return counts

    def remove(self, doc_id: str) -> bool:
        """Remove a document. Returns ``True`` if it was present."""
        with self._lock:
            if doc_id not in self._docs:
                return False
            del self._docs[doc_id]
            return True

    @property
    def total_docs(self) -> int:
        """Total number of tracked documents."""
        with self._lock:
            return len(self._docs)

    def clear(self) -> None:
        """Forget every tracked document."""
        with self._lock:
            self._docs.clear()
