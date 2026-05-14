"""DocBatchProcessor module — E297.

Processes documents in configurable batches with progress tracking and
error handling.  Pure stdlib, thread-safe.

Quick start::

    from docstoolkit.doc_batch_processor import (
        BatchJob, BatchResult, DocBatchProcessor,
    )

    proc = DocBatchProcessor(batch_size=5, max_errors=2)
    job  = proc.create_job("my-job", list(range(20)))
    result = proc.run_job(job.job_id, lambda x: x * 2)
    print(result.succeeded, result.failed)

Public API
----------
- ``BatchJob``          — dataclass: job state and counters.
- ``BatchResult``       — dataclass: summary returned by :meth:`~DocBatchProcessor.run_job`.
- ``DocBatchProcessor`` — main class: create/run/inspect/cancel/delete jobs.
"""

from docstoolkit.doc_batch_processor.processor import (
    BatchJob,
    BatchResult,
    DocBatchProcessor,
)

__all__ = [
    "BatchJob",
    "BatchResult",
    "DocBatchProcessor",
]
