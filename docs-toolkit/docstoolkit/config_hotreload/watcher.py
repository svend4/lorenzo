"""FileWatcher — poll-based file change detection using os.stat.

No external dependencies; uses only stdlib ``os``, ``threading``, and
``time``.  Change detection is based on mtime *and* size so a file that
is overwritten with equal-length content at a different time is still
detected.
"""

import os
import threading
import time
from typing import Callable


class FileWatcher:
    """Watch a list of paths for changes by polling ``os.stat`` every
    *interval* seconds.

    Parameters
    ----------
    paths:
        Absolute or relative file paths to monitor.
    interval:
        Polling interval in seconds (default 1.0).

    Usage::

        watcher = FileWatcher(["/etc/app.json"], interval=0.5)
        watcher.on_change(lambda p: print(f"changed: {p}"))
        watcher.start()
        ...
        watcher.stop()
    """

    def __init__(self, paths: list[str], interval: float = 1.0) -> None:
        self._paths: list[str] = list(paths)
        self._interval: float = interval
        self._callbacks: list[Callable[[str], None]] = []
        self._snapshots: dict[str, tuple] = {}  # path -> (mtime, size)
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()

        # Take an initial snapshot so only *future* changes are reported.
        for path in self._paths:
            self._snapshots[path] = self._stat(path)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _stat(path: str) -> tuple:
        """Return ``(mtime, size)`` for *path*, or ``(0, 0)`` if absent."""
        try:
            s = os.stat(path)
            return (s.st_mtime, s.st_size)
        except OSError:
            return (0, 0)

    def _poll_once(self) -> list[str]:
        """Compare current stat to stored snapshot.

        Returns a list of paths that have changed and updates the
        internal snapshot for each changed path.
        """
        changed: list[str] = []
        for path in self._paths:
            current = self._stat(path)
            if current != self._snapshots.get(path):
                self._snapshots[path] = current
                changed.append(path)
        return changed

    def _run(self) -> None:
        """Background thread target: poll until stop event is set."""
        while not self._stop_event.is_set():
            changed = self._poll_once()
            for path in changed:
                for cb in list(self._callbacks):
                    try:
                        cb(path)
                    except Exception:
                        pass
            self._stop_event.wait(self._interval)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def on_change(self, callback: Callable[[str], None]) -> None:
        """Register *callback* to be called with the path of any changed file.

        Multiple callbacks may be registered; they are called in
        registration order.  Exceptions raised inside a callback are
        silently swallowed so that one bad callback cannot break others.
        """
        self._callbacks.append(callback)

    def start(self) -> None:
        """Start the background polling thread (daemon, safe to not join)."""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run, daemon=True, name="FileWatcher")
        self._thread.start()

    def stop(self) -> None:
        """Signal the polling thread to stop and wait for it to finish."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=self._interval * 2 + 1)
            self._thread = None

    def check_once(self) -> list[str]:
        """Synchronously check for changes and return a list of changed paths.

        Also updates internal snapshots, so the same change will not be
        reported twice on consecutive calls.

        Useful for deterministic testing without a background thread.
        """
        return self._poll_once()
