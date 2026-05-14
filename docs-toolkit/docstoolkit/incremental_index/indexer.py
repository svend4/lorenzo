"""Incremental indexer orchestrator for docs-toolkit (E32)."""
from __future__ import annotations

from dataclasses import dataclass, field

from docstoolkit.incremental_index.change import ChangeDetector, DocumentChange
from docstoolkit.incremental_index.queue import IndexJob, IndexQueue


@dataclass
class IndexConfig:
    batch_size: int = 10
    auto_detect: bool = True


@dataclass
class IndexStats:
    added: int = 0
    modified: int = 0
    deleted: int = 0
    skipped: int = 0

    def total_processed(self) -> int:
        """Return the total number of processed (non-skipped) documents."""
        return self.added + self.modified + self.deleted


class IncrementalIndexer:
    """Orchestrates change detection and job queuing for incremental indexing."""

    def __init__(
        self,
        config: IndexConfig | None = None,
        queue: IndexQueue | None = None,
        detector: ChangeDetector | None = None,
    ) -> None:
        self.config = config or IndexConfig()
        self.queue = queue or IndexQueue()
        self.detector = detector or ChangeDetector()

    def submit(self, doc_id: str, content: str, priority: int = 5) -> DocumentChange:
        """Detect change for a document and enqueue a job if content has changed."""
        change = self.detector.detect(doc_id, content)
        if change.is_content_change():
            self.queue.enqueue(change, priority=priority)
        return change

    def submit_batch(self, docs: dict[str, str]) -> IndexStats:
        """Submit multiple documents and return aggregated IndexStats."""
        stats = IndexStats()
        for doc_id, content in docs.items():
            change = self.submit(doc_id, content)
            ct = change.change_type
            from docstoolkit.incremental_index.change import ChangeType
            if ct == ChangeType.ADDED:
                stats.added += 1
            elif ct == ChangeType.MODIFIED:
                stats.modified += 1
            elif ct == ChangeType.DELETED:
                stats.deleted += 1
            else:
                stats.skipped += 1
        return stats

    def process_batch(self, handler: callable | None = None) -> IndexStats:
        """Dequeue up to config.batch_size jobs and process them.

        If handler is provided, it is called with each IndexJob.
        - handler returns True or None  → job is marked done
        - handler returns False         → job is marked failed
        - handler raises an exception   → job is marked failed with error message
        """
        from docstoolkit.incremental_index.change import ChangeType

        jobs = self.queue.dequeue(self.config.batch_size)
        stats = IndexStats()
        for job in jobs:
            ct = job.change_type
            success = True
            error_msg = ""
            if handler is not None:
                try:
                    result = handler(job)
                    if result is False:
                        success = False
                except Exception as exc:
                    success = False
                    error_msg = str(exc)

            if success:
                self.queue.complete(job.job_id)
            else:
                self.queue.fail(job.job_id, error_msg)

            if ct == ChangeType.ADDED:
                stats.added += 1
            elif ct == ChangeType.MODIFIED:
                stats.modified += 1
            elif ct == ChangeType.DELETED:
                stats.deleted += 1
            else:
                stats.skipped += 1

        return stats

    def pending_count(self) -> int:
        """Return the number of pending jobs in the queue."""
        return self.queue.pending_count()
