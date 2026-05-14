"""E198 Composable filter chain — pipeline of document filters.

The chain runs filters in three phases (PRE, MAIN, POST) and within
each phase by priority (lower first, stable). Filters may transform the
document, drop it (by returning ``None``), or raise (which marks the
result as an error and stops processing).

This module is intentionally stdlib-only and thread-safe.
"""
from __future__ import annotations

import copy
import threading
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional


class FilterPhase(Enum):
    """Execution phases of the chain (ordered)."""

    PRE = "pre"
    MAIN = "main"
    POST = "post"


# Type alias for filter functions.
FilterFunc = Callable[[dict], Optional[dict]]


@dataclass
class ChainFilter:
    """A single filter step within a :class:`DocFilterChain`."""

    name: str
    func: FilterFunc
    phase: FilterPhase = FilterPhase.MAIN
    priority: int = 0
    enabled: bool = True


@dataclass
class FilterContext:
    """Mutable processing context passed alongside the document."""

    original: dict
    current: dict
    history: List[str] = field(default_factory=list)
    dropped: bool = False
    dropped_by: Optional[str] = None


@dataclass
class ChainResult:
    """Outcome of processing one document through the chain."""

    final: Optional[dict]
    context: FilterContext
    success: bool
    error: Optional[str] = None


@dataclass
class BatchResult:
    """Aggregate results for a batch of documents."""

    results: List[ChainResult]
    processed_count: int
    dropped_count: int
    error_count: int


# Phase ordering used by :meth:`DocFilterChain.process`.
_PHASE_ORDER = (FilterPhase.PRE, FilterPhase.MAIN, FilterPhase.POST)


class DocFilterChain:
    """Composable filter chain processing documents through PRE/MAIN/POST phases."""

    def __init__(self) -> None:
        self._filters: List[ChainFilter] = []
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Filter management
    # ------------------------------------------------------------------
    def add_filter(
        self,
        name: str,
        func: FilterFunc,
        phase: FilterPhase = FilterPhase.MAIN,
        priority: int = 0,
    ) -> ChainFilter:
        """Register a new filter under ``name``.

        Raises :class:`ValueError` if a filter with the same name exists.
        """
        if not isinstance(name, str) or not name:
            raise ValueError("filter name must be a non-empty string")
        if not callable(func):
            raise ValueError("filter func must be callable")
        if not isinstance(phase, FilterPhase):
            raise ValueError("phase must be a FilterPhase value")
        with self._lock:
            for existing in self._filters:
                if existing.name == name:
                    raise ValueError(f"filter {name!r} already exists")
            cf = ChainFilter(name=name, func=func, phase=phase, priority=priority)
            self._filters.append(cf)
            return cf

    def remove_filter(self, name: str) -> bool:
        with self._lock:
            for i, cf in enumerate(self._filters):
                if cf.name == name:
                    del self._filters[i]
                    return True
            return False

    def enable_filter(self, name: str) -> bool:
        with self._lock:
            for cf in self._filters:
                if cf.name == name:
                    cf.enabled = True
                    return True
            return False

    def disable_filter(self, name: str) -> bool:
        with self._lock:
            for cf in self._filters:
                if cf.name == name:
                    cf.enabled = False
                    return True
            return False

    def set_priority(self, name: str, priority: int) -> bool:
        with self._lock:
            for cf in self._filters:
                if cf.name == name:
                    cf.priority = priority
                    return True
            return False

    def move_filter(self, name: str, phase: FilterPhase) -> bool:
        if not isinstance(phase, FilterPhase):
            raise ValueError("phase must be a FilterPhase value")
        with self._lock:
            for cf in self._filters:
                if cf.name == name:
                    cf.phase = phase
                    return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._filters.clear()

    # ------------------------------------------------------------------
    # Introspection
    # ------------------------------------------------------------------
    @property
    def filter_count(self) -> int:
        with self._lock:
            return len(self._filters)

    def filters_in_phase(self, phase: FilterPhase) -> List[ChainFilter]:
        if not isinstance(phase, FilterPhase):
            raise ValueError("phase must be a FilterPhase value")
        with self._lock:
            return [cf for cf in self._filters if cf.phase == phase]

    def total_phases(self) -> int:
        with self._lock:
            return len({cf.phase for cf in self._filters})

    def list_filters(self, enabled_only: bool = False) -> List[ChainFilter]:
        with self._lock:
            if enabled_only:
                return [cf for cf in self._filters if cf.enabled]
            return list(self._filters)

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    def _ordered_snapshot(self) -> List[ChainFilter]:
        """Return a stably ordered snapshot of enabled filters."""
        with self._lock:
            indexed = list(enumerate(self._filters))
        phase_index = {p: i for i, p in enumerate(_PHASE_ORDER)}
        indexed.sort(key=lambda pair: (phase_index[pair[1].phase], pair[1].priority, pair[0]))
        return [cf for _, cf in indexed if cf.enabled]

    def process(self, doc: dict) -> ChainResult:
        if not isinstance(doc, dict):
            raise TypeError("doc must be a dict")

        original = copy.deepcopy(doc)
        current = copy.deepcopy(doc)
        context = FilterContext(original=original, current=current)

        for cf in self._ordered_snapshot():
            try:
                # Work on an isolated copy so filters cannot mutate the live state directly.
                candidate = copy.deepcopy(context.current)
                result = cf.func(candidate)
            except Exception as exc:  # noqa: BLE001 — chain-level boundary
                context.dropped = True
                context.dropped_by = cf.name
                return ChainResult(
                    final=None,
                    context=context,
                    success=False,
                    error=f"{type(exc).__name__}: {exc}",
                )

            if result is None:
                context.dropped = True
                context.dropped_by = cf.name
                context.history.append(cf.name)
                return ChainResult(final=None, context=context, success=True)

            if not isinstance(result, dict):
                context.dropped = True
                context.dropped_by = cf.name
                return ChainResult(
                    final=None,
                    context=context,
                    success=False,
                    error=f"filter {cf.name!r} returned non-dict {type(result).__name__}",
                )

            context.current = result
            context.history.append(cf.name)

        return ChainResult(final=context.current, context=context, success=True)

    def process_batch(self, docs: List[dict]) -> BatchResult:
        if not isinstance(docs, list):
            raise TypeError("docs must be a list of dicts")
        results: List[ChainResult] = []
        processed = 0
        dropped = 0
        errors = 0
        for d in docs:
            res = self.process(d)
            results.append(res)
            if not res.success:
                errors += 1
            elif res.context.dropped:
                dropped += 1
            else:
                processed += 1
        return BatchResult(
            results=results,
            processed_count=processed,
            dropped_count=dropped,
            error_count=errors,
        )


__all__ = [
    "BatchResult",
    "ChainFilter",
    "ChainResult",
    "DocFilterChain",
    "FilterContext",
    "FilterPhase",
]
