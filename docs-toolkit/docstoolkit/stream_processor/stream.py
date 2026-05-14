"""Stream — fluent lazy stream over any iterable.

All intermediate operations return a new ``Stream`` and are lazy
(implemented via generators).  Terminal operations consume the
underlying iterator and return a concrete result.

Implementation uses only the standard library: ``itertools`` and
``functools``.
"""

from __future__ import annotations

import functools
import itertools
from typing import (
    Any,
    Callable,
    Iterable,
    Iterator,
    Optional,
)

_MISSING = object()


class Stream:
    """A fluent, lazy stream over an iterable.

    Intermediate operations (``map``, ``filter``, ``take``...) return a
    new ``Stream`` without consuming the source.  Terminal operations
    (``to_list``, ``count``, ``reduce``...) materialise the result.

    A ``Stream`` is single-use: once iterated/terminated, its underlying
    iterator is exhausted.  Wrap a re-iterable source (like a list) in a
    fresh ``Stream`` if you need multiple passes.
    """

    __slots__ = ("_iterable",)

    def __init__(self, iterable: Iterable):
        if iterable is None:
            raise TypeError("Stream requires an iterable, got None")
        self._iterable = iter(iterable)

    # ------------------------------------------------------------------
    # Iterator protocol
    # ------------------------------------------------------------------
    def __iter__(self) -> Iterator:
        return self._iterable

    # ------------------------------------------------------------------
    # Intermediate (lazy) operations
    # ------------------------------------------------------------------
    def map(self, func: Callable) -> "Stream":
        """Apply ``func`` to every item."""
        return Stream(map(func, self._iterable))

    def filter(self, predicate: Callable[[Any], bool]) -> "Stream":
        """Keep items for which ``predicate`` returns truthy."""
        return Stream(filter(predicate, self._iterable))

    def flat_map(self, func: Callable) -> "Stream":
        """Apply ``func`` returning an iterable per item, then flatten."""
        return Stream(itertools.chain.from_iterable(map(func, self._iterable)))

    def take(self, n: int) -> "Stream":
        """Yield at most the first ``n`` items."""
        if n < 0:
            raise ValueError("take(n) requires n >= 0")
        return Stream(itertools.islice(self._iterable, n))

    def skip(self, n: int) -> "Stream":
        """Drop the first ``n`` items."""
        if n < 0:
            raise ValueError("skip(n) requires n >= 0")
        return Stream(itertools.islice(self._iterable, n, None))

    def distinct(self, key: Optional[Callable] = None) -> "Stream":
        """Yield items with a unique ``key`` (default: identity).

        For unhashable items, supply ``key`` returning a hashable value.
        """
        src = self._iterable

        def _gen():
            seen = set()
            for item in src:
                k = item if key is None else key(item)
                if k in seen:
                    continue
                seen.add(k)
                yield item

        return Stream(_gen())

    def sort(self, key: Optional[Callable] = None, reverse: bool = False) -> "Stream":
        """Sort items (terminal in the sense that the source is consumed)."""
        return Stream(sorted(self._iterable, key=key, reverse=reverse))

    def reverse(self) -> "Stream":
        """Reverse the stream (consumes the source)."""
        return Stream(reversed(list(self._iterable)))

    def group_by(self, key: Callable) -> "Stream":
        """Group consecutive-equal keys; yields ``(key, [items])`` tuples.

        Items are first sorted by ``key`` so groups are global.
        """
        items = sorted(self._iterable, key=key)

        def _gen():
            for k, group in itertools.groupby(items, key=key):
                yield k, list(group)

        return Stream(_gen())

    def window(self, size: int, step: int = 1) -> "Stream":
        """Sliding window of ``size`` items advancing by ``step``.

        Yields tuples.  If the underlying stream has fewer than ``size``
        items, no window is produced.
        """
        if size <= 0:
            raise ValueError("window size must be > 0")
        if step <= 0:
            raise ValueError("window step must be > 0")
        src = self._iterable

        def _gen():
            buf: list = []
            it = iter(src)
            # Fill initial window
            for _ in range(size):
                try:
                    buf.append(next(it))
                except StopIteration:
                    return
            yield tuple(buf)
            while True:
                # Advance by `step`
                try:
                    for _ in range(step):
                        new = next(it)
                        buf.append(new)
                except StopIteration:
                    return
                buf = buf[step:]
                yield tuple(buf)

        return Stream(_gen())

    def chunked(self, size: int) -> "Stream":
        """Yield fixed-size tuples (last chunk may be smaller)."""
        if size <= 0:
            raise ValueError("chunk size must be > 0")
        src = self._iterable

        def _gen():
            it = iter(src)
            while True:
                chunk = tuple(itertools.islice(it, size))
                if not chunk:
                    return
                yield chunk

        return Stream(_gen())

    def peek(self, func: Callable[[Any], None]) -> "Stream":
        """Apply side-effect ``func`` to each item without changing it."""
        src = self._iterable

        def _gen():
            for item in src:
                func(item)
                yield item

        return Stream(_gen())

    def tap(self, func: Callable[[Any], None]) -> "Stream":
        """Alias for :meth:`peek`."""
        return self.peek(func)

    def concat(self, other: Iterable) -> "Stream":
        """Chain this stream with another iterable."""
        return Stream(itertools.chain(self._iterable, other))

    def zip(self, other: Iterable) -> "Stream":
        """Pairwise zip with another iterable."""
        return Stream(zip(self._iterable, other))

    # ------------------------------------------------------------------
    # Terminal operations
    # ------------------------------------------------------------------
    def count(self) -> int:
        """Consume the stream and return the number of items."""
        n = 0
        for _ in self._iterable:
            n += 1
        return n

    def first(self) -> Any:
        """Return the first item, raising ``StopIteration`` if empty."""
        return next(self._iterable)

    def first_or_none(self) -> Optional[Any]:
        """Return the first item or ``None`` if the stream is empty."""
        return next(self._iterable, None)

    def last(self) -> Any:
        """Return the last item, raising ``StopIteration`` if empty."""
        sentinel = _MISSING
        last = sentinel
        for item in self._iterable:
            last = item
        if last is sentinel:
            raise StopIteration("last() called on empty stream")
        return last

    def any(self, predicate: Optional[Callable] = None) -> bool:
        """Return ``True`` if any item satisfies ``predicate``.

        With no predicate, returns ``True`` if any item is truthy.
        """
        if predicate is None:
            return any(self._iterable)
        return any(predicate(x) for x in self._iterable)

    def all(self, predicate: Callable) -> bool:
        """Return ``True`` if every item satisfies ``predicate``."""
        return all(predicate(x) for x in self._iterable)

    def reduce(self, func: Callable, initial: Any = _MISSING) -> Any:
        """Fold the stream with ``func``; optional ``initial`` value."""
        if initial is _MISSING:
            return functools.reduce(func, self._iterable)
        return functools.reduce(func, self._iterable, initial)

    def min(self, key: Optional[Callable] = None) -> Any:
        """Return the minimum item (optionally by ``key``)."""
        if key is None:
            return min(self._iterable)
        return min(self._iterable, key=key)

    def max(self, key: Optional[Callable] = None) -> Any:
        """Return the maximum item (optionally by ``key``)."""
        if key is None:
            return max(self._iterable)
        return max(self._iterable, key=key)

    def sum(self) -> Any:
        """Return the sum of items."""
        return sum(self._iterable)

    def to_list(self) -> list:
        """Materialise the stream into a list."""
        return list(self._iterable)

    def to_set(self) -> set:
        """Materialise the stream into a set."""
        return set(self._iterable)

    def to_dict(
        self,
        key_func: Callable,
        value_func: Optional[Callable] = None,
    ) -> dict:
        """Materialise into a dict.

        ``key_func(item)`` yields each key.  If ``value_func`` is omitted,
        the item itself is the value.
        """
        if value_func is None:
            return {key_func(item): item for item in self._iterable}
        return {key_func(item): value_func(item) for item in self._iterable}

    def for_each(self, func: Callable[[Any], None]) -> None:
        """Apply ``func`` to each item for side-effects.  Returns ``None``."""
        for item in self._iterable:
            func(item)
