"""Event-sourced aggregate support: AggregateState, EventApplier, EventSourcedAggregate."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from docstoolkit.event_sourcing.event import DomainEvent
from docstoolkit.event_sourcing.store import EventStore


@dataclass
class AggregateState:
    """Mutable snapshot of an aggregate's current state.

    Attributes:
        aggregate_id:   Unique identifier for this aggregate instance.
        aggregate_type: Class/type name of the aggregate.
        state:          Arbitrary key-value state dictionary.
        version:        The version number of the last applied event (0 = empty).
    """

    aggregate_id: str
    aggregate_type: str
    state: dict = field(default_factory=dict)
    version: int = 0


class EventApplier(ABC):
    """Strategy interface that knows how to fold a :class:`DomainEvent` into
    an :class:`AggregateState`.

    Implement :meth:`apply` in a subclass to define the state-transition logic
    for your aggregate.
    """

    @abstractmethod
    def apply(self, state: AggregateState, event: DomainEvent) -> AggregateState:
        """Return a new (or mutated) :class:`AggregateState` after applying *event*."""


class EventSourcedAggregate:
    """High-level façade for appending and replaying domain events.

    Parameters
    ----------
    aggregate_id:
        Unique identifier for this aggregate instance.
    aggregate_type:
        Human-readable type name (e.g. ``"Order"``, ``"User"``).
    applier:
        An :class:`EventApplier` that knows how to fold events into state.
    store:
        The :class:`EventStore` to read/write from.  Defaults to a fresh
        in-memory store if *None*.
    """

    def __init__(
        self,
        aggregate_id: str,
        aggregate_type: str,
        applier: EventApplier,
        store: "EventStore | None" = None,
    ) -> None:
        self._aggregate_id = aggregate_id
        self._aggregate_type = aggregate_type
        self._applier = applier
        self._store = store if store is not None else EventStore()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append_event(
        self,
        event_type: str,
        payload: dict,
        metadata: "dict | None" = None,
    ) -> DomainEvent:
        """Create, persist, and return a new :class:`DomainEvent`.

        The version is automatically set to ``latest_version + 1``.

        Parameters
        ----------
        event_type:
            Name of the event to record.
        payload:
            Event-specific data.
        metadata:
            Optional extra metadata.  Defaults to ``{}``.
        """
        next_version = self._store.latest_version(self._aggregate_id) + 1
        event = DomainEvent(
            event_type=event_type,
            aggregate_id=self._aggregate_id,
            aggregate_type=self._aggregate_type,
            payload=payload,
            version=next_version,
            metadata=metadata or {},
        )
        self._store.append(event)
        return event

    # ------------------------------------------------------------------
    # Read / replay
    # ------------------------------------------------------------------

    def rebuild_state(self, from_version: int = 1) -> AggregateState:
        """Replay all events (from *from_version* onwards) and return the
        resulting :class:`AggregateState`.

        Each event is applied in version order via :meth:`EventApplier.apply`.
        """
        events = self._store.get_events(self._aggregate_id, from_version=from_version)
        state = AggregateState(
            aggregate_id=self._aggregate_id,
            aggregate_type=self._aggregate_type,
        )
        for event in events:
            state = self._applier.apply(state, event)
            state.version = event.version
        return state

    def current_state(self) -> AggregateState:
        """Convenience wrapper: rebuild state from version 1 (full replay)."""
        return self.rebuild_state(from_version=1)

    def event_count(self) -> int:
        """Number of events stored for this aggregate."""
        return len(self._store.get_events(self._aggregate_id))
