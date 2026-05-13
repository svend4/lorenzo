"""Event sourcing primitives for docs-toolkit.

Provides an append-only :class:`EventStore` backed by SQLite, an immutable
:class:`DomainEvent` record, and a :class:`EventSourcedAggregate` façade for
building event-sourced domain objects entirely with the standard library.

Quick-start::

    from docstoolkit.event_sourcing import (
        DomainEvent, EventStore,
        AggregateState, EventApplier, EventSourcedAggregate,
    )

    class CounterApplier(EventApplier):
        def apply(self, state, event):
            state.state["count"] = state.state.get("count", 0) + event.payload.get("delta", 1)
            return state

    store = EventStore()
    agg   = EventSourcedAggregate("c1", "Counter", CounterApplier(), store)
    agg.append_event("counter.incremented", {"delta": 1})
    agg.append_event("counter.incremented", {"delta": 2})
    print(agg.current_state().state)   # {'count': 3}
"""
from docstoolkit.event_sourcing.event import DomainEvent
from docstoolkit.event_sourcing.store import EventStore, VersionConflictError
from docstoolkit.event_sourcing.aggregate import (
    AggregateState,
    EventApplier,
    EventSourcedAggregate,
)

__all__ = [
    "DomainEvent",
    "EventStore",
    "VersionConflictError",
    "AggregateState",
    "EventApplier",
    "EventSourcedAggregate",
]
