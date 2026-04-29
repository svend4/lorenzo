"""Background jobs queue для docs-toolkit.

Долгие операции (full reindex, ingestion crawl, RAG batch) выполняются
асинхронно через worker daemon.

SQLite-based queue со статусами: queued → running → completed/failed/cancelled.

Использование:
    from docstoolkit.jobs import submit, get_status, list_jobs

    job_id = submit("index_build", {"provider": "tfidf"})
    # ... worker подбирает и выполняет ...
    status = get_status(job_id)

    # Запуск worker'а:
    docstoolkit jobs worker  # foreground
"""
from docstoolkit.jobs.queue import (
    JobQueue, Job, submit, get_status, list_jobs, cancel,
)
from docstoolkit.jobs.handlers import HANDLERS, register_handler
from docstoolkit.jobs.worker import run_worker

__all__ = [
    "JobQueue", "Job",
    "submit", "get_status", "list_jobs", "cancel",
    "HANDLERS", "register_handler",
    "run_worker",
]
