"""Projection and ReplayEngine for the E84 event sourcing module."""
from docstoolkit.event_sourcing.event import Event
from docstoolkit.event_sourcing.store import EventStore


class Projection:
    """A named projection that accumulates state by replaying events.

    A projection can register two kinds of handlers:

    * **Generic handlers** (via :meth:`apply`): invoked for every event.
    * **Typed handlers** (via :meth:`apply_typed`): invoked only when the
      event's ``event_type`` matches.

    During :meth:`replay`, typed handlers run **before** generic handlers
    for any given event.

    Parameters
    ----------
    name:
        Human-readable name of the projection.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        self.state: dict = {}
        self._generic_handlers: list = []
        self._typed_handlers: dict = {}

    def apply(self, handler) -> None:
        """Register a generic *handler(state, event)* for every event."""
        self._generic_handlers.append(handler)

    def apply_typed(self, event_type: str, handler) -> None:
        """Register a *handler(state, event)* only for events of *event_type*."""
        self._typed_handlers.setdefault(event_type, []).append(handler)

    def replay(self, events: list) -> dict:
        """Replay *events* into ``self.state`` and return it.

        For each event, typed handlers run first (in registration order),
        then any generic handlers.
        """
        for event in events:
            for handler in self._typed_handlers.get(event.event_type, []):
                handler(self.state, event)
            for handler in self._generic_handlers:
                handler(self.state, event)
        return self.state


class ReplayEngine:
    """Replay events from an :class:`EventStore` through a :class:`Projection`.

    Parameters
    ----------
    store:
        The event store to read from.
    """

    def __init__(self, store: EventStore) -> None:
        self.store = store

    def replay_aggregate(
        self, aggregate_id: str, projection: Projection
    ) -> dict:
        """Replay all events for *aggregate_id* through *projection*."""
        envelopes = self.store.get_events(aggregate_id)
        events = [env.event for env in envelopes]
        return projection.replay(events)

    def replay_all(self, projection: Projection) -> dict:
        """Replay every event in the store through *projection*, in sequence."""
        events: list = []
        batch_size = 1000
        cursor = 0
        while True:
            envelopes = self.store.get_all(
                from_sequence=cursor, limit=batch_size
            )
            if not envelopes:
                break
            for env in envelopes:
                events.append(env.event)
            cursor = envelopes[-1].sequence + 1
            if len(envelopes) < batch_size:
                break
        return projection.replay(events)
