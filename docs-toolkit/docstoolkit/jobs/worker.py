"""Worker daemon — выполняет jobs из очереди."""
import time
import traceback

from docstoolkit.jobs.queue import JobQueue
from docstoolkit.jobs.handlers import HANDLERS


def run_worker(*, max_jobs: int = 0, poll_interval: float = 1.0,
               handler_filter: str = "", verbose: bool = True):
    """Foreground worker loop.

    max_jobs: 0 = бесконечно. Иначе остановиться после N выполненных.
    poll_interval: секунд между опросами очереди когда нет работы.
    handler_filter: выполнять только handler с этим именем.
    """
    queue = JobQueue()
    if verbose:
        print(f"# Worker started")
        print(f"  handlers available: {sorted(HANDLERS)}")
        print(f"  max_jobs: {max_jobs or '∞'}, poll: {poll_interval}s")
        print()

    processed = 0
    try:
        while True:
            job = queue.claim_next()
            if not job:
                if max_jobs and processed >= max_jobs:
                    break
                time.sleep(poll_interval)
                continue

            if handler_filter and job.handler != handler_filter:
                # «Не наш» — вернём в очередь
                queue.cancel(job.id)  # cancelled, чтобы не зацикливаться
                if verbose:
                    print(f"  [skip] {job.id} {job.handler} (filter: {handler_filter})")
                continue

            handler = HANDLERS.get(job.handler)
            if not handler:
                queue.fail(job.id, f"Handler '{job.handler}' не зарегистрирован")
                if verbose:
                    print(f"  ❌ {job.id} {job.handler}: handler не найден")
                continue

            if verbose:
                print(f"  ▶ {job.id} {job.handler}")

            def progress_cb(pct, msg=""):
                queue.update_progress(job.id, pct, msg)
                if verbose and msg:
                    print(f"      [{pct}%] {msg}")

            try:
                result = handler(job.args, progress_cb=progress_cb)
                queue.complete(job.id, result)
                if verbose:
                    print(f"  ✅ {job.id} done")
            except Exception as e:
                tb = traceback.format_exc()
                queue.fail(job.id, f"{e}\n{tb}")
                if verbose:
                    print(f"  ❌ {job.id} failed: {e}")

            processed += 1
            if max_jobs and processed >= max_jobs:
                break

    except KeyboardInterrupt:
        if verbose:
            print(f"\n👋 Worker stopped (processed {processed})")
    finally:
        queue.close()
    return processed
