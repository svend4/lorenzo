"""Fluent builder for StateMachine instances."""
from __future__ import annotations

from typing import Callable, Optional

from docstoolkit.state_machine.state import State, Transition
from docstoolkit.state_machine.machine import StateMachine, StateMachineConfig


class StateMachineBuilder:
    """Fluent builder that constructs a :class:`StateMachine`.

    Example::

        sm = (
            StateMachineBuilder("idle")
            .state("idle", description="Waiting for work")
            .state("running", description="Processing")
            .state("done", is_terminal=True)
            .transition("idle", "start", "running")
            .transition("running", "finish", "done")
            .build()
        )
        sm.trigger("start")
        sm.trigger("finish")
        assert sm.is_terminal()
    """

    def __init__(
        self,
        initial_state: str,
        allow_self_transitions: bool = False,
    ) -> None:
        self._initial_state = initial_state
        self._allow_self_transitions = allow_self_transitions
        self._states: list[State] = []
        self._transitions: list[Transition] = []

    # ------------------------------------------------------------------
    # Builder methods (return self for chaining)
    # ------------------------------------------------------------------

    def state(
        self,
        name: str,
        description: str = "",
        is_terminal: bool = False,
        on_enter: Optional[Callable] = None,
        on_exit: Optional[Callable] = None,
    ) -> "StateMachineBuilder":
        """Add a state definition.

        Returns:
            self, enabling fluent chaining.
        """
        self._states.append(
            State(
                name=name,
                description=description,
                is_terminal=is_terminal,
                on_enter=on_enter,
                on_exit=on_exit,
            )
        )
        return self

    def transition(
        self,
        from_state: str,
        event: str,
        to_state: str,
        guard: Optional[Callable] = None,
        action: Optional[Callable] = None,
    ) -> "StateMachineBuilder":
        """Add a transition definition.

        Returns:
            self, enabling fluent chaining.
        """
        self._transitions.append(
            Transition(
                from_state=from_state,
                event=event,
                to_state=to_state,
                guard=guard,
                action=action,
            )
        )
        return self

    def allow_self_transitions(
        self, value: bool = True
    ) -> "StateMachineBuilder":
        """Enable or disable self-transitions for the machine being built.

        Returns:
            self, enabling fluent chaining.
        """
        self._allow_self_transitions = value
        return self

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build(self) -> StateMachine:
        """Construct and return the configured :class:`StateMachine`.

        Raises:
            ValueError: Propagated from :class:`StateMachine` if states or
                        transitions are invalid.
        """
        config = StateMachineConfig(
            initial_state=self._initial_state,
            allow_self_transitions=self._allow_self_transitions,
        )
        machine = StateMachine(config)
        for state in self._states:
            machine.add_state(state)
        for transition in self._transitions:
            machine.add_transition(transition)
        return machine
