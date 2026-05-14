"""Append-only event store for document events with stream-based querying.

Provides:

* :class:`DocEvent` — immutable document event with global id and per-stream
  sequence number.
* :class:`StreamInfo` — metadata snapshot for a single stream.
* :class:`EventStoreStats` — aggregate statistics for the whole store.
* :class:`DocEventStore` — thread-safe, append-only event store with
  stream-scoped and global read operations.

Stdlib only; no third-party dependencies.

Quick-start::

    from docstoolkit.doc_event_store import DocEventStore

    store = DocEventStore()
    e = store.append("doc:42", "created", {"title": "Hello"})
    e2 = store.append("doc:42", "updated", {"title": "Hello World"})

    print(store.read_stream("doc:42"))
    print(store.latest("doc:42"))
    print(store.stats())
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Domain objects
# ---------------------------------------------------------------------------


@dataclass
class DocEvent:
    """A single immutable document event.

    Attributes:
        event_id:   Global auto-increment identifier (starts at 1).
        stream_id:  Logical stream identifier, e.g. ``"doc:123"``.
        event_type: Free-form event label, e.g. ``"created"``.
        payload:    Arbitrary dict attached to the event.
        timestamp:  Unix timestamp of the event (float seconds).
        sequence:   Per-stream sequence number (starts at 1, strictly
                    monotonically increasing within a stream).
    """

    event_id: int
    stream_id: str
    event_type: str
    payload: dict
    timestamp: float
    sequence: int


@dataclass
class StreamInfo:
    """Metadata snapshot for a single stream.

    Attributes:
        stream_id:       Stream identifier.
        event_count:     Number of live events in the stream.
        first_at:        Timestamp of the first event.
        last_at:         Timestamp of the most recent event.
        latest_sequence: Sequence number of the most recent event.
    """

    stream_id: str
    event_count: int
    first_at: float
    last_at: float
    latest_sequence: int


@dataclass
class EventStoreStats:
    """Aggregate statistics for the whole store.

    Attributes:
        total_events:  Total number of events across all streams.
        total_streams: Number of distinct streams.
        event_types:   Sorted list of unique event types seen so far.
    """

    total_events: int
    total_streams: int
    event_types: List[str]


# ---------------------------------------------------------------------------
# Store
# ---------------------------------------------------------------------------


class DocEventStore:
    """Thread-safe, append-only event store for document events.

    All public methods are safe to call from multiple threads concurrently.
    Internal state is protected by a single :class:`threading.Lock`.

    Example::

        store = DocEventStore()
        store.append("doc:1", "created", {"author": "alice"})
        store.append("doc:1", "updated", {"title": "New Title"})
        info = store.stream_info("doc:1")
        print(info.event_count)  # 2
    """

    def __init__(self) -> None:
        self._lock: threading.Lock = threading.Lock()

        # global ordered event list (append-only under normal operation;
        # compacted only by truncate_stream)
        self._events: List[DocEvent] = []

        # event_id -> DocEvent for O(1) point reads (entries removed on truncate)
        self._event_index: Dict[int, DocEvent] = {}

        # stream_id -> list of DocEvent (in sequence order)
        self._streams: Dict[str, List[DocEvent]] = {}

        # stream_id -> next sequence number
        self._stream_seq: Dict[str, int] = {}

        # all event types ever seen (set maintained for fast stats)
        self._event_types: set = set()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def append(
        self,
        stream_id: str,
        event_type: str,
        payload: Optional[dict] = None,
        now: Optional[float] = None,
    ) -> DocEvent:
        """Append an event to *stream_id* and return the created :class:`DocEvent`.

        Args:
            stream_id:  The stream to append to.
            event_type: A label for the kind of event.
            payload:    Optional dict of event data (defaults to ``{}``).
            now:        Override the timestamp (defaults to
                        :func:`time.time`).

        Returns:
            The newly created :class:`DocEvent`.
        """
        if payload is None:
            payload = {}
        ts = now if now is not None else time.time()

        with self._lock:
            event_id = len(self._events) + 1
            seq = self._stream_seq.get(stream_id, 0) + 1

            event = DocEvent(
                event_id=event_id,
                stream_id=stream_id,
                event_type=event_type,
                payload=payload,
                timestamp=ts,
                sequence=seq,
            )

            self._events.append(event)
            self._event_index[event_id] = event
            self._stream_seq[stream_id] = seq
            if stream_id not in self._streams:
                self._streams[stream_id] = []
            self._streams[stream_id].append(event)
            self._event_types.add(event_type)

        return event

    # ------------------------------------------------------------------
    # Point reads
    # ------------------------------------------------------------------

    def get_event(self, event_id: int) -> Optional[DocEvent]:
        """Return the event with the given global *event_id*, or ``None``."""
        with self._lock:
            return self._event_index.get(event_id)

    def latest(self, stream_id: str) -> Optional[DocEvent]:
        """Return the most recent event in *stream_id*, or ``None``."""
        with self._lock:
            stream = self._streams.get(stream_id)
            if not stream:
                return None
            return stream[-1]

    # ------------------------------------------------------------------
    # Stream reads
    # ------------------------------------------------------------------

    def read_stream(
        self,
        stream_id: str,
        from_seq: int = 1,
        limit: Optional[int] = None,
    ) -> List[DocEvent]:
        """Return events for *stream_id* ordered by sequence.

        Args:
            stream_id: The stream to read.
            from_seq:  Include only events with ``sequence >= from_seq``
                       (default ``1`` = from the beginning).
            limit:     Maximum number of events to return (``None`` = all).

        Returns:
            A new list of :class:`DocEvent` objects.
        """
        with self._lock:
            stream = self._streams.get(stream_id, [])
            # sequence is 1-based and monotonically increasing within stream
            result = [e for e in stream if e.sequence >= from_seq]
            if limit is not None:
                result = result[:limit]
            return list(result)

    def read_all(
        self,
        from_event_id: int = 1,
        limit: Optional[int] = None,
    ) -> List[DocEvent]:
        """Return all events across all streams ordered by global *event_id*.

        Args:
            from_event_id: Include only events with ``event_id >= from_event_id``
                           (default ``1`` = from the beginning).
            limit:         Maximum number of events to return (``None`` = all).

        Returns:
            A new list of :class:`DocEvent` objects.
        """
        with self._lock:
            result = [e for e in self._events if e.event_id >= from_event_id]
            if limit is not None:
                result = result[:limit]
            return list(result)

    # ------------------------------------------------------------------
    # Stream metadata
    # ------------------------------------------------------------------

    def stream_info(self, stream_id: str) -> Optional[StreamInfo]:
        """Return a :class:`StreamInfo` snapshot for *stream_id*, or ``None``.

        Returns ``None`` if the stream has never received any events.
        """
        with self._lock:
            stream = self._streams.get(stream_id)
            if not stream:
                return None
            return StreamInfo(
                stream_id=stream_id,
                event_count=len(stream),
                first_at=stream[0].timestamp,
                last_at=stream[-1].timestamp,
                latest_sequence=stream[-1].sequence,
            )

    def streams(self) -> List[str]:
        """Return a sorted list of all stream identifiers."""
        with self._lock:
            return sorted(self._streams.keys())

    # ------------------------------------------------------------------
    # Cross-stream reads
    # ------------------------------------------------------------------

    def events_by_type(
        self,
        event_type: str,
        limit: Optional[int] = None,
    ) -> List[DocEvent]:
        """Return events of *event_type* across all streams, ordered by event_id.

        Args:
            event_type: The event type to filter on.
            limit:      Maximum number of events to return (``None`` = all).

        Returns:
            A new list of :class:`DocEvent` objects.
        """
        with self._lock:
            result = [e for e in self._events if e.event_type == event_type]
            if limit is not None:
                result = result[:limit]
            return list(result)

    # ------------------------------------------------------------------
    # Maintenance
    # ------------------------------------------------------------------

    def truncate_stream(self, stream_id: str, keep_last: int) -> int:
        """Remove all but the last *keep_last* events from *stream_id*.

        The global ``_events`` list is also updated so that removed events are
        no longer returned by :meth:`read_all` or :meth:`get_event`.

        Args:
            stream_id: The stream to truncate.
            keep_last: Number of tail events to retain (must be >= 0).

        Returns:
            The number of events removed.  Returns ``0`` if the stream does
            not exist or has fewer events than *keep_last*.

        Raises:
            ValueError: If *keep_last* is negative.
        """
        if keep_last < 0:
            raise ValueError("keep_last must be >= 0")

        with self._lock:
            stream = self._streams.get(stream_id)
            if not stream:
                return 0

            total = len(stream)
            to_remove = max(0, total - keep_last)
            if to_remove == 0:
                return 0

            removed = stream[:to_remove]
            removed_ids = {e.event_id for e in removed}

            # Trim the stream list
            self._streams[stream_id] = stream[to_remove:]

            # Rebuild _events without removed entries
            self._events = [e for e in self._events if e.event_id not in removed_ids]

            # Remove from point-lookup index
            for eid in removed_ids:
                self._event_index.pop(eid, None)

            return to_remove

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> EventStoreStats:
        """Return an :class:`EventStoreStats` snapshot."""
        with self._lock:
            return EventStoreStats(
                total_events=len(self._events),
                total_streams=len(self._streams),
                event_types=sorted(self._event_types),
            )

    @property
    def total_events(self) -> int:
        """Total number of events in the store."""
        with self._lock:
            return len(self._events)

    @property
    def total_streams(self) -> int:
        """Total number of distinct streams in the store."""
        with self._lock:
            return len(self._streams)
