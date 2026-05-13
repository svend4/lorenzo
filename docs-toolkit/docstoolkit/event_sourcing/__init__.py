"""Event sourcing primitives for docs-toolkit (E84).

Provides:

* :class:`Event` — immutable domain event with auto-generated id/timestamp.
* :class:`EventEnvelope` — wraps an :class:`Event` with a global sequence.
* :class:`EventStore` — append-only SQLite-backed event store.
* :class:`Projection` — accumulates state by replaying events.
* :class:`ReplayEngine` — reads events from an :class:`EventStore` and runs
  them through a :class:`Projection`.

Quick-start::

    from docstoolkit.event_sourcing import (
        Event, EventStore, Projection, ReplayEngine,
    )

    store = EventStore()
    store.append(Event(aggregate_id="c1", event_type="counter.incremented",
                       payload={"delta": 1}, version=1))
    store.append(Event(aggregate_id="c1", event_type="counter.incremented",
                       payload={"delta": 2}, version=2))

    proj = Projection("counter")
    proj.apply_typed(
        "counter.incremented",
        lambda s, e: s.update({"total": s.get("total", 0) + e.payload["delta"]}),
    )
    engine = ReplayEngine(store)
    state = engine.replay_aggregate("c1", proj)
    print(state)   # {'total': 3}
"""
from docstoolkit.event_sourcing.event import Event, EventEnvelope
from docstoolkit.event_sourcing.store import EventStore
from docstoolkit.event_sourcing.replay import Projection, ReplayEngine

__all__ = ["Event", "EventEnvelope", "EventStore", "Projection", "ReplayEngine"]
