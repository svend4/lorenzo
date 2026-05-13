"""Batch processor module — E107.

Processes items in configurable batches with support for parallelism
(``ThreadPoolExecutor``), per-item error handling, progress callbacks,
and result aggregation.  Pure stdlib — no third-party dependencies.

Quick start::

    from docstoolkit.batch_processor import (
        BatchConfig, BatchProcessor, BatchResult, ItemResult,
    )

    config = BatchConfig(batch_size=5, max_workers=4, on_error="collect")
    processor = BatchProcessor(config)

    result = processor.process(range(20), lambda x: x ** 2)
    print(result.success_count)  # 20
    print(result.outputs[:5])    # [0, 1, 4, 9, 16]

Public API
----------
- ``BatchConfig``    — dataclass: batch_size, max_workers, on_error, progress_callback.
- ``ItemResult``     — dataclass: index, item, output, error, success.
- ``BatchResult``    — dataclass: results list + successful/failed/outputs properties.
- ``BatchProcessor`` — main processor: process(), process_batches(), chunk().
"""

from docstoolkit.batch_processor.processor import (
    BatchConfig,
    BatchProcessor,
    BatchResult,
    ItemResult,
)

__all__ = [
    "BatchConfig",
    "ItemResult",
    "BatchResult",
    "BatchProcessor",
]
