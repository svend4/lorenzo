"""E422 DocSubscriptionFilter — filter rules on subscription events.

This module provides a small, thread-safe registry of filter rules that can be
applied to subscription event delivery. Each :class:`SubFilter` belongs to a
single subscriber and defines a glob pattern over document identifiers plus an
optional whitelist of event types. The :class:`DocSubscriptionFilter` aggregator
holds many such filters and answers questions of the form: "given this
``(subscriber_id, doc_id, event_type)`` triple, which of the subscriber's
enabled filters match?".

Pure stdlib, no third-party dependencies. All public mutations are protected
by an :class:`threading.Lock` instance, so the registry is safe to share across
threads.
"""
from __future__ import annotations

import fnmatch
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SubFilter:
    """A single subscription filter rule.

    Attributes
    ----------
    filter_id:
        Unique identifier of the filter within a :class:`DocSubscriptionFilter`.
    subscriber_id:
        Identifier of the subscriber that owns this filter.
    doc_pattern:
        ``fnmatch``-style glob applied to ``doc_id`` values. Defaults to
        ``"*"`` which matches every document.
    event_types:
        Whitelist of event types accepted by this filter. An empty list means
        "accept any event type".
    priority:
        Higher values sort first in :meth:`DocSubscriptionFilter.list_filters`.
    enabled:
        When ``False`` the filter is kept in the registry but ignored by
        :meth:`DocSubscriptionFilter.matches`.
    """

    filter_id: str
    subscriber_id: str
    doc_pattern: str = "*"
    event_types: list[str] = field(default_factory=list)
    priority: int = 0
    enabled: bool = True


@dataclass
class FilterMatchResult:
    """Outcome of a filter evaluation."""

    matched: bool
    matching_filters: list[str] = field(default_factory=list)


@dataclass
class SubFilterStats:
    """Aggregate statistics over a :class:`DocSubscriptionFilter` instance."""

    total_filters: int
    enabled_filters: int
    total_evaluations: int
    total_matches: int


class DocSubscriptionFilter:
    """Thread-safe registry of subscription filter rules."""

    def __init__(self) -> None:
        self._filters: dict[str, SubFilter] = {}
        self._by_subscriber: dict[str, list[str]] = {}
        self._total_evaluations: int = 0
        self._total_matches: int = 0
        self._lock = threading.Lock()

    # ------------------------------------------------------------------ CRUD

    def add_filter(self, filter_obj: SubFilter) -> None:
        """Register *filter_obj* in the registry.

        Raises
        ------
        TypeError
            If *filter_obj* is not a :class:`SubFilter` instance.
        ValueError
            If a filter with the same ``filter_id`` is already registered, or
            if either ``filter_id`` or ``subscriber_id`` is empty.
        """
        if not isinstance(filter_obj, SubFilter):
            raise TypeError("filter_obj must be a SubFilter instance")
        if not filter_obj.filter_id:
            raise ValueError("filter_id must be non-empty")
        if not filter_obj.subscriber_id:
            raise ValueError("subscriber_id must be non-empty")
        with self._lock:
            if filter_obj.filter_id in self._filters:
                raise ValueError(
                    f"filter_id {filter_obj.filter_id!r} already registered"
                )
            self._filters[filter_obj.filter_id] = filter_obj
            self._by_subscriber.setdefault(filter_obj.subscriber_id, []).append(
                filter_obj.filter_id
            )

    def remove_filter(self, filter_id: str) -> bool:
        """Remove the filter identified by *filter_id*.

        Returns
        -------
        bool
            ``True`` if a filter was removed, ``False`` if no such filter
            existed.
        """
        with self._lock:
            existing = self._filters.pop(filter_id, None)
            if existing is None:
                return False
            ids = self._by_subscriber.get(existing.subscriber_id)
            if ids is not None:
                try:
                    ids.remove(filter_id)
                except ValueError:
                    pass
                if not ids:
                    self._by_subscriber.pop(existing.subscriber_id, None)
            return True

    def enable_filter(self, filter_id: str) -> bool:
        """Mark a filter as enabled. Returns ``True`` if state actually changed."""
        with self._lock:
            f = self._filters.get(filter_id)
            if f is None or f.enabled:
                return False
            f.enabled = True
            return True

    def disable_filter(self, filter_id: str) -> bool:
        """Mark a filter as disabled. Returns ``True`` if state actually changed."""
        with self._lock:
            f = self._filters.get(filter_id)
            if f is None or not f.enabled:
                return False
            f.enabled = False
            return True

    def get_filter(self, filter_id: str) -> Optional[SubFilter]:
        """Return the filter identified by *filter_id*, or ``None``."""
        with self._lock:
            return self._filters.get(filter_id)

    # ----------------------------------------------------------------- views

    def list_filters(self) -> list[SubFilter]:
        """Return all filters sorted by ``(-priority, filter_id)``."""
        with self._lock:
            values = list(self._filters.values())
        return sorted(values, key=lambda f: (-f.priority, f.filter_id))

    def filters_for_subscriber(
        self, subscriber_id: str, active_only: bool = True
    ) -> list[SubFilter]:
        """Return filters owned by *subscriber_id* sorted by ``(-priority, filter_id)``.

        Parameters
        ----------
        subscriber_id:
            Owner whose filters to return.
        active_only:
            When ``True`` (default) only enabled filters are returned.
        """
        with self._lock:
            ids = list(self._by_subscriber.get(subscriber_id, ()))
            values = [self._filters[fid] for fid in ids if fid in self._filters]
        if active_only:
            values = [f for f in values if f.enabled]
        return sorted(values, key=lambda f: (-f.priority, f.filter_id))

    # ----------------------------------------------------------------- match

    @staticmethod
    def _filter_accepts(
        f: SubFilter, doc_id: str, event_type: str
    ) -> bool:
        if not f.enabled:
            return False
        if not fnmatch.fnmatchcase(doc_id, f.doc_pattern):
            return False
        if f.event_types and event_type not in f.event_types:
            return False
        return True

    def matches(
        self, subscriber_id: str, doc_id: str, event_type: str
    ) -> FilterMatchResult:
        """Find subscriber's enabled filters that accept ``(doc_id, event_type)``.

        The evaluation counter is always incremented; the match counter is
        incremented only when at least one filter matched. Returned filter
        ids are sorted by ``(-priority, filter_id)``.
        """
        with self._lock:
            self._total_evaluations += 1
            ids = list(self._by_subscriber.get(subscriber_id, ()))
            candidates = [self._filters[fid] for fid in ids if fid in self._filters]
            matching = [
                f for f in candidates if self._filter_accepts(f, doc_id, event_type)
            ]
            matching.sort(key=lambda f: (-f.priority, f.filter_id))
            matching_ids = [f.filter_id for f in matching]
            if matching_ids:
                self._total_matches += 1
        return FilterMatchResult(
            matched=bool(matching_ids), matching_filters=matching_ids
        )

    def would_match(
        self, filter_obj: SubFilter, doc_id: str, event_type: str
    ) -> bool:
        """Check whether *filter_obj* would accept the event, without registering it.

        Does **not** require the filter to be in the registry and does **not**
        update statistics. Disabled filters never match.
        """
        if not isinstance(filter_obj, SubFilter):
            raise TypeError("filter_obj must be a SubFilter instance")
        return self._filter_accepts(filter_obj, doc_id, event_type)

    # ----------------------------------------------------------------- bulk

    def clear_subscriber(self, subscriber_id: str) -> int:
        """Remove every filter owned by *subscriber_id*. Returns count removed."""
        with self._lock:
            ids = self._by_subscriber.pop(subscriber_id, None)
            if not ids:
                return 0
            count = 0
            for fid in ids:
                if self._filters.pop(fid, None) is not None:
                    count += 1
            return count

    def clear_all(self) -> int:
        """Drop every registered filter. Returns count removed."""
        with self._lock:
            count = len(self._filters)
            self._filters.clear()
            self._by_subscriber.clear()
            return count

    # ----------------------------------------------------------------- stats

    def stats(self) -> SubFilterStats:
        """Return a snapshot of aggregate statistics."""
        with self._lock:
            total = len(self._filters)
            enabled = sum(1 for f in self._filters.values() if f.enabled)
            return SubFilterStats(
                total_filters=total,
                enabled_filters=enabled,
                total_evaluations=self._total_evaluations,
                total_matches=self._total_matches,
            )
