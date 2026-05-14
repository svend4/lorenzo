"""Simulated file watcher module (E146).

Public API:
    - ChangeKind
    - FileChange
    - WatchSnapshot
    - FileWatcherSim
"""

from docstoolkit.file_watcher_sim.watcher import (
    ChangeKind,
    FileChange,
    FileWatcherSim,
    WatchSnapshot,
)

__all__ = ["ChangeKind", "FileChange", "WatchSnapshot", "FileWatcherSim"]
