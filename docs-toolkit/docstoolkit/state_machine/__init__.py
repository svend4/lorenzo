"""State machine module for docs-toolkit (E77).

Provides a pure-stdlib finite-state machine with guards, actions, lifecycle
hooks, and a fluent builder API.

Quick start::

    from docstoolkit.state_machine import (
        StateMachineBuilder, StateMachine, StateMachineConfig,
        State, Transition, TransitionError,
    )

    sm = (
        StateMachineBuilder("idle")
        .state("idle")
        .state("running")
        .state("done", is_terminal=True)
        .transition("idle", "start", "running")
        .transition("running", "finish", "done")
        .build()
    )

    sm.trigger("start")
    sm.trigger("finish")
    assert sm.is_terminal()
"""
from docstoolkit.state_machine.state import State, Transition
from docstoolkit.state_machine.machine import (
    TransitionError,
    StateMachineConfig,
    StateMachine,
)
from docstoolkit.state_machine.builder import StateMachineBuilder

__all__ = [
    "State",
    "Transition",
    "TransitionError",
    "StateMachineConfig",
    "StateMachine",
    "StateMachineBuilder",
]
