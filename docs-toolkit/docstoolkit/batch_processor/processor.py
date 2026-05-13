"""BatchProcessor — configurable batch processing with parallelism (E107).

Applies a callable to a list of items in configurable batches, with support
for parallel execution via ``ThreadPoolExecutor``, per-item error handling,
progress callbacks, and result aggregation.

Uses only the Python standard library.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import Any, Callable, Optional, TypeVar

T = TypeVar("T")


@dataclass
class BatchConfig:
    """Configuration for :class:`BatchProcessor`.

    Attributes:
        batch_size:         number of items per batch (default 10).
        max_workers:        thread count; 1 = sequential, >1 = ThreadPoolExecutor.
        on_error:           ``"skip"`` | ``"raise"`` | ``"collect"``.
                            - ``skip``    — record failure, continue processing.
                            - ``raise``   — re-raise the first exception immediately.
                            - ``collect`` — same as ``skip`` but error stored in
                              :attr:`ItemResult.error` (actually the same behaviour;
                              both modes store the error — the distinction is that
                              ``collect`` is an explicit contract that callers rely on
                              error storage).
        progress_callback:  optional ``(done: int, total: int) -> None`` called
                            once after each batch, with the cumulative *done* count.
    """

    batch_size: int = 10
    max_workers: int = 1
    on_error: str = "skip"
    progress_callback: Optional[Callable[[int, int], None]] = None


@dataclass
class ItemResult:
    """Result for a single processed item.

    Attributes:
        index:   original position in the input list.
        item:    the original input value.
        output:  return value of the processing function (``None`` on failure).
        error:   exception raised during processing, or ``None`` on success.
        success: ``True`` if no exception was raised.
    """

    index: int
    item: Any
    output: Any = None
    error: Optional[Exception] = None
    success: bool = True


@dataclass
class BatchResult:
    """Aggregated result of a :meth:`BatchProcessor.process` call.

    Attributes:
        results: all :class:`ItemResult` objects in original input order.
    """

    results: list[ItemResult] = field(default_factory=list)

    @property
    def successful(self) -> list[ItemResult]:
        """Return all results where processing succeeded."""
        return [r for r in self.results if r.success]

    @property
    def failed(self) -> list[ItemResult]:
        """Return all results where processing failed."""
        return [r for r in self.results if not r.success]

    @property
    def success_count(self) -> int:
        """Number of successfully processed items."""
        return sum(1 for r in self.results if r.success)

    @property
    def failure_count(self) -> int:
        """Number of items that failed processing."""
        return sum(1 for r in self.results if not r.success)

    @property
    def outputs(self) -> list[Any]:
        """Return outputs of successful items in original (index) order."""
        return [r.output for r in sorted(self.successful, key=lambda r: r.index)]


class BatchProcessor:
    """Process items in configurable batches with optional parallelism.

    Example::

        config = BatchConfig(batch_size=5, max_workers=4, on_error="collect")
        processor = BatchProcessor(config)
        result = processor.process(items, lambda x: x * 2)
        print(result.success_count, result.failure_count)
        print(result.outputs)

    Args:
        config: :class:`BatchConfig` instance; if ``None`` a default config
                (batch_size=10, max_workers=1, on_error="skip") is used.
    """

    def __init__(self, config: Optional[BatchConfig] = None) -> None:
        self._config = config if config is not None else BatchConfig()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def process(
        self, items: list[Any], fn: Callable[[Any], Any]
    ) -> BatchResult:
        """Apply *fn* to each item, processing in batches of ``config.batch_size``.

        Error handling is controlled by ``config.on_error``:

        - ``"skip"``    — failed items are recorded with ``success=False``; processing
                          continues.
        - ``"raise"``   — the first exception encountered is re-raised immediately.
        - ``"collect"`` — identical to ``"skip"``; the exception is stored in
                          :attr:`ItemResult.error` for later inspection.

        ``config.progress_callback(done, total)`` is called once after each batch
        completes, where *done* is the cumulative count of processed items (both
        successes and failures) and *total* is ``len(items)``.

        Args:
            items: input list; order is preserved in results.
            fn:    callable applied to each item.

        Returns:
            :class:`BatchResult` with all :class:`ItemResult` objects in
            original input order.

        Raises:
            Exception: only when ``on_error="raise"`` and *fn* raises.
        """
        batches = self.process_batches(items, fn)
        all_results: list[ItemResult] = []
        for batch in batches:
            all_results.extend(batch)
        # Restore original order (process_batches preserves it, but be explicit)
        all_results.sort(key=lambda r: r.index)
        return BatchResult(results=all_results)

    def process_batches(
        self, items: list[Any], fn: Callable[[Any], Any]
    ) -> list[list[ItemResult]]:
        """Like :meth:`process` but returns a list of per-batch result lists.

        Each inner list contains one :class:`ItemResult` per item in that
        batch, in original order.

        Args:
            items: input list.
            fn:    callable applied to each item.

        Returns:
            A list of batches, each batch being a ``list[ItemResult]``.

        Raises:
            Exception: only when ``on_error="raise"`` and *fn* raises.
        """
        total = len(items)
        chunks = self.chunk(items)
        batch_results: list[list[ItemResult]] = []
        done = 0

        for chunk in chunks:
            # Compute global indices for this chunk
            start_index = done  # chunk position in the original list
            batch = self._process_chunk(chunk, start_index, fn)
            batch_results.append(batch)
            done += len(chunk)
            if self._config.progress_callback is not None:
                self._config.progress_callback(done, total)

        return batch_results

    def chunk(self, items: list[Any], size: Optional[int] = None) -> list[list[Any]]:
        """Split *items* into chunks of *size*.

        Args:
            items: list to split.
            size:  chunk size; defaults to ``config.batch_size``.

        Returns:
            A list of non-empty sublists. Returns ``[[]]`` (a list containing
            one empty list) when *items* is empty, preserving the contract that
            the return is always a list of lists.
            Actually returns ``[]`` for empty input to keep behaviour sane.
        """
        effective_size = size if size is not None else self._config.batch_size
        if not items:
            return []
        return [
            items[i : i + effective_size]
            for i in range(0, len(items), effective_size)
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _process_chunk(
        self,
        chunk: list[Any],
        start_index: int,
        fn: Callable[[Any], Any],
    ) -> list[ItemResult]:
        """Process a single chunk, respecting ``max_workers`` and ``on_error``.

        Args:
            chunk:       the sub-list of items to process.
            start_index: global index of the first item in *chunk*.
            fn:          callable to apply to each item.

        Returns:
            List of :class:`ItemResult`, one per item in *chunk*, in order.
        """
        if self._config.max_workers <= 1:
            return self._process_chunk_sequential(chunk, start_index, fn)
        return self._process_chunk_parallel(chunk, start_index, fn)

    def _process_chunk_sequential(
        self,
        chunk: list[Any],
        start_index: int,
        fn: Callable[[Any], Any],
    ) -> list[ItemResult]:
        """Sequential (single-threaded) chunk processing."""
        results: list[ItemResult] = []
        for offset, item in enumerate(chunk):
            idx = start_index + offset
            result = self._apply(idx, item, fn)
            results.append(result)
        return results

    def _process_chunk_parallel(
        self,
        chunk: list[Any],
        start_index: int,
        fn: Callable[[Any], Any],
    ) -> list[ItemResult]:
        """Parallel chunk processing using ThreadPoolExecutor.

        All items in the chunk are submitted to the pool; results are
        collected as futures complete, then re-sorted into original order.
        """
        index_map: dict[int, Any] = {}  # future_id -> ItemResult placeholder

        with ThreadPoolExecutor(max_workers=self._config.max_workers) as pool:
            future_to_idx: dict = {}
            for offset, item in enumerate(chunk):
                idx = start_index + offset
                future = pool.submit(self._apply, idx, item, fn)
                future_to_idx[future] = idx

            # Collect results as they complete
            results_dict: dict[int, ItemResult] = {}
            for future in as_completed(future_to_idx):
                # _apply itself never raises; it wraps exceptions internally
                # (except when on_error="raise", where it re-raises)
                item_result: ItemResult = future.result()
                results_dict[item_result.index] = item_result

        # Return in original order
        return [results_dict[start_index + i] for i in range(len(chunk))]

    def _apply(
        self, index: int, item: Any, fn: Callable[[Any], Any]
    ) -> ItemResult:
        """Apply *fn* to a single item, wrapping errors per ``on_error`` policy.

        When ``on_error="raise"`` the original exception propagates; the
        caller is responsible for re-raising it up the call stack.

        Args:
            index: original position in the input list.
            item:  the item to process.
            fn:    callable to apply.

        Returns:
            :class:`ItemResult`.

        Raises:
            Exception: when ``on_error="raise"`` and *fn* raises.
        """
        try:
            output = fn(item)
            return ItemResult(index=index, item=item, output=output, success=True)
        except Exception as exc:  # noqa: BLE001
            if self._config.on_error == "raise":
                raise
            # "skip" and "collect" both store the error; the distinction is
            # purely semantic / contractual for callers.
            return ItemResult(
                index=index,
                item=item,
                output=None,
                error=exc,
                success=False,
            )
