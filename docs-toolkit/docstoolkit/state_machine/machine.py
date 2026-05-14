"""Core StateMachine implementation."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from docstoolkit.state_machine.state import State, Transition


class TransitionError(Exception):
    """Raised when a requested transition cannot be performed.

    This can happen when:
    - No transition is registered for the (current_state, event) pair.
    - All matching transitions have guards that return False.
    - The current state is terminal.
    - A self-transition is attempted but ``allow_self_transitions`` is False.
    """


@dataclass
class StateMachineConfig:
    """Configuration for a :class:`StateMachine`.

    Attributes:
        initial_state: Name of the state the machine starts in (and resets to).
        allow_self_transitions: Whether transitions from a state back to itself
                                are permitted.  Defaults to ``False``.
    """

    initial_state: str
    allow_self_transitions: bool = False


class StateMachine:
    """Finite-state machine with guards, actions, and lifecycle hooks.

    Usage::

        cfg = StateMachineConfig(initial_state="idle")
        sm = StateMachine(cfg)
        sm.add_state(State("idle"))
        sm.add_state(State("running"))
        sm.add_transition(Transition("idle", "start", "running"))
        sm.trigger("start")
        assert sm.current_state == "running"
    """

    def __init__(self, config: StateMachineConfig) -> None:
        self._config = config
        self._states: dict[str, State] = {}
        self._transitions: list[Transition] = []
        self._current_state: str = config.initial_state
        self._history: list[tuple[str, str, str]] = []

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def add_state(self, state: State) -> None:
        """Register *state* with the machine.

        Raises:
            ValueError: If a state with the same name is already registered.
        """
        if state.name in self._states:
            raise ValueError(f"State '{state.name}' is already registered.")
        self._states[state.name] = state

    def add_transition(self, transition: Transition) -> None:
        """Register *transition* with the machine.

        Raises:
            ValueError: If the from_state or to_state has not been registered,
                        or if a self-transition is added while
                        ``allow_self_transitions`` is False.
        """
        if transition.from_state not in self._states:
            raise ValueError(
                f"Unknown from_state '{transition.from_state}'. "
                "Register the state before adding transitions."
            )
        if transition.to_state not in self._states:
            raise ValueError(
                f"Unknown to_state '{transition.to_state}'. "
                "Register the state before adding transitions."
            )
        if (
            transition.from_state == transition.to_state
            and not self._config.allow_self_transitions
        ):
            raise ValueError(
                f"Self-transition on state '{transition.from_state}' is not allowed. "
                "Set allow_self_transitions=True in StateMachineConfig."
            )
        self._transitions.append(transition)

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def current_state(self) -> str:
        """Name of the current state."""
        return self._current_state

    @property
    def history(self) -> list[tuple[str, str, str]]:
        """Ordered list of completed transitions as (from_state, event, to_state)."""
        return list(self._history)

    # ------------------------------------------------------------------
    # Querying
    # ------------------------------------------------------------------

    def can_trigger(self, event: str, context: Optional[dict] = None) -> bool:
        """Return True if *event* can be triggered from the current state.

        Takes guards and terminal-state restrictions into account.
        """
        if context is None:
            context = {}
        if self.is_terminal():
            return False
        return self._find_transition(event, context) is not None

    def available_events(self, context: Optional[dict] = None) -> list[str]:
        """Return a deduplicated list of events that can currently be triggered.

        Events are returned in the order their first matching transition was
        registered.
        """
        if context is None:
            context = {}
        if self.is_terminal():
            return []
        seen: set[str] = set()
        result: list[str] = []
        for t in self._transitions:
            if t.from_state != self._current_state:
                continue
            if t.event in seen:
                continue
            if t.guard is None or t.guard(context):
                seen.add(t.event)
                result.append(t.event)
        return result

    def is_terminal(self) -> bool:
        """Return True if the current state is marked as terminal."""
        state = self._states.get(self._current_state)
        return state is not None and state.is_terminal

    # ------------------------------------------------------------------
    # Triggering
    # ------------------------------------------------------------------

    def trigger(self, event: str, context: Optional[dict] = None) -> str:
        """Fire *event* and advance the machine to the next state.

        Steps executed (in order):

        1. Verify the current state is not terminal.
        2. Find the first transition matching (current_state, event) whose
           guard (if any) returns True.
        3. Call ``on_exit`` of the current state.
        4. Call the transition's ``action`` (if any).
        5. Call ``on_enter`` of the new state.
        6. Record the transition in :attr:`history`.
        7. Update :attr:`current_state`.

        Args:
            event: Name of the event to fire.
            context: Arbitrary mapping passed to guards, actions, and hooks.
                     Defaults to an empty dict.

        Returns:
            The name of the new (current) state.

        Raises:
            TransitionError: If the current state is terminal, or if no valid
                             transition exists for the given event.
        """
        if context is None:
            context = {}

        if self.is_terminal():
            raise TransitionError(
                f"State '{self._current_state}' is terminal; no transitions allowed."
            )

        transition = self._find_transition(event, context)
        if transition is None:
            raise TransitionError(
                f"No valid transition from state '{self._current_state}' "
                f"on event '{event}'."
            )

        from_state_name = self._current_state
        from_state = self._states[from_state_name]
        to_state = self._states[transition.to_state]

        # Lifecycle: exit
        if from_state.on_exit is not None:
            from_state.on_exit(context)

        # Transition action
        if transition.action is not None:
            transition.action(context)

        # Lifecycle: enter
        if to_state.on_enter is not None:
            to_state.on_enter(context)

        # Commit
        self._history.append((from_state_name, event, transition.to_state))
        self._current_state = transition.to_state

        return self._current_state

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self) -> None:
        """Return to the initial state and clear the transition history."""
        self._current_state = self._config.initial_state
        self._history = []

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _find_transition(
        self, event: str, context: dict
    ) -> Optional[Transition]:
        """Return the first matching transition, or None."""
        for t in self._transitions:
            if t.from_state != self._current_state:
                continue
            if t.event != event:
                continue
            if t.guard is None or t.guard(context):
                return t
        return None
