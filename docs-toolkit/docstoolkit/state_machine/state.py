"""State and Transition dataclasses for the state machine module."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Optional


@dataclass
class State:
    """Represents a single state in the state machine.

    Attributes:
        name: Unique identifier for this state.
        description: Human-readable description (optional).
        is_terminal: If True, no further transitions are allowed from this state.
        on_enter: Callable invoked when the machine enters this state.
                  Signature: on_enter(context: dict) -> None
        on_exit: Callable invoked when the machine exits this state.
                 Signature: on_exit(context: dict) -> None
    """

    name: str
    description: str = ""
    is_terminal: bool = False
    on_enter: Optional[Callable] = field(default=None, repr=False)
    on_exit: Optional[Callable] = field(default=None, repr=False)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, State):
            return self.name == other.name
        return NotImplemented


@dataclass
class Transition:
    """Describes a valid transition between states.

    Attributes:
        from_state: Name of the source state.
        event: Name of the event that triggers this transition.
        to_state: Name of the destination state.
        guard: Optional callable guard(context) -> bool.
               If provided, the transition only fires when guard returns True.
               If None, the transition is always allowed.
        action: Optional callable action(context) called during the transition,
                after on_exit of the source state and before on_enter of the
                destination state.
    """

    from_state: str
    event: str
    to_state: str
    guard: Optional[Callable] = field(default=None, repr=False)
    action: Optional[Callable] = field(default=None, repr=False)
