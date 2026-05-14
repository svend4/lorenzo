"""Middleware pipeline for query pre-processing."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Callable


class QueryMiddleware(ABC):
    """Abstract base class for query middleware.

    Subclasses must implement :meth:`process`.
    """

    @abstractmethod
    def process(self, query: str, next_fn: Callable[[str], str]) -> str:
        """Process the query and pass it to *next_fn*.

        Args:
            query: The current query string.
            next_fn: Callable that accepts the (possibly modified) query
                     and returns the final processed string from downstream
                     middleware.

        Returns:
            The processed query string.
        """


class NormalizationMiddleware(QueryMiddleware):
    """Normalizes a query by lowercasing and stripping leading/trailing whitespace."""

    def process(self, query: str, next_fn: Callable[[str], str]) -> str:
        normalized = query.strip().lower()
        return next_fn(normalized)


class TruncationMiddleware(QueryMiddleware):
    """Truncates the query to a maximum number of characters.

    Args:
        max_length: Maximum number of characters to keep. Defaults to 500.
    """

    def __init__(self, max_length: int = 500) -> None:
        self.max_length = max_length

    def process(self, query: str, next_fn: Callable[[str], str]) -> str:
        truncated = query[: self.max_length]
        return next_fn(truncated)


class MiddlewarePipeline:
    """Chains multiple :class:`QueryMiddleware` instances together.

    Middleware is applied in the order it was added.  The last middleware
    passes the query to an identity function that returns it unchanged.

    Args:
        middlewares: Optional initial list of middleware instances.
    """

    def __init__(self, middlewares: list[QueryMiddleware] | None = None) -> None:
        self._middlewares: list[QueryMiddleware] = list(middlewares) if middlewares else []

    def add(self, middleware: QueryMiddleware) -> None:
        """Append a middleware to the end of the pipeline."""
        self._middlewares.append(middleware)

    def run(self, query: str) -> str:
        """Pass *query* through all middleware in order.

        Each middleware's ``process`` is called with the query and a
        *next_fn* that invokes the remainder of the pipeline.  If the
        pipeline is empty, the query is returned unchanged.

        Returns:
            The processed query string.
        """
        def _build_chain(index: int) -> Callable[[str], str]:
            if index >= len(self._middlewares):
                # Terminal: return query unchanged.
                return lambda q: q
            middleware = self._middlewares[index]
            next_fn = _build_chain(index + 1)
            return lambda q: middleware.process(q, next_fn)

        return _build_chain(0)(query)
