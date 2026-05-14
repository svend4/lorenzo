"""HotReloadManager — live-reloading config from JSON and INI files.

Builds on :class:`~docstoolkit.config_hotreload.watcher.FileWatcher` to
reload configuration whenever a watched file changes on disk.  Supports
JSON (``.json``) and INI (``.ini``, ``.cfg``, ``.conf``) files via
stdlib only.

Dot-notation ``get`` and ``subscribe`` semantics follow the same
conventions as :class:`~docstoolkit.config_mgmt.manager.ConfigManager`.
"""

import configparser
import copy
import json
import os
import threading
from dataclasses import dataclass, field
from typing import Callable

from docstoolkit.config_hotreload.watcher import FileWatcher


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _flatten(d: dict, prefix: str = "") -> dict[str, object]:
    """Flatten a nested dict into dot-notation keys.

    Example::

        _flatten({"a": {"b": 1}}) == {"a.b": 1}
        _flatten({"x": 2})        == {"x": 2}
    """
    result: dict[str, object] = {}
    for k, v in d.items():
        full_key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            result.update(_flatten(v, full_key))
        else:
            result[full_key] = v
    return result


def _get_nested(root: dict, parts: list, default=None):
    """Traverse *root* following *parts*; return *default* on any miss."""
    node = root
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


def _deep_merge(base: dict, override: dict) -> dict:
    """Return a new dict that is *base* deep-merged with *override*."""
    result = copy.deepcopy(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)
    return result


# ---------------------------------------------------------------------------
# Dataclass
# ---------------------------------------------------------------------------

@dataclass
class ReloadConfig:
    """Configuration for :class:`HotReloadManager`.

    Attributes
    ----------
    paths:
        List of file paths to watch and load.
    interval:
        Polling interval passed to :class:`FileWatcher`.
    on_error:
        Optional callable ``on_error(path: str, exc: Exception)`` invoked
        when a file cannot be parsed.  If ``None``, the exception is
        re-raised.
    """

    paths: list[str]
    interval: float = 1.0
    on_error: Callable | None = field(default=None, compare=False)


# ---------------------------------------------------------------------------
# Manager
# ---------------------------------------------------------------------------

class HotReloadManager:
    """Load, watch, and merge JSON / INI configuration files.

    All public methods are thread-safe (protected by ``_lock``).

    Usage::

        cfg = ReloadConfig(paths=["app.json", "overrides.ini"], interval=0.5)
        mgr = HotReloadManager(cfg)
        mgr.start()

        mgr.get("database.host", "localhost")
        mgr.snapshot()

        mgr.stop()
    """

    # INI extensions recognised by configparser
    _INI_EXTS = {".ini", ".cfg", ".conf"}

    def __init__(self, config: ReloadConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
        # Per-file parsed dicts; merged on demand
        self._file_data: dict[str, dict] = {}
        # Merged view (rebuilt after every reload)
        self._merged: dict = {}
        # Change subscribers: callback(key, old_val, new_val)
        self._subscribers: list[Callable[[str, object, object], None]] = []
        # The underlying FileWatcher (created in start())
        self._watcher: FileWatcher | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _parse_json(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _parse_ini(self, path: str) -> dict:
        parser = configparser.ConfigParser()
        parser.read(path, encoding="utf-8")
        result: dict = {}
        # DEFAULT section
        if parser.defaults():
            result["DEFAULT"] = dict(parser.defaults())
        # Named sections
        for section in parser.sections():
            result[section] = dict(parser.items(section))
        return result

    def _rebuild_merged(self) -> dict:
        """Merge all file dicts in *paths* order (last wins)."""
        merged: dict = {}
        for path in self._config.paths:
            data = self._file_data.get(path)
            if data:
                merged = _deep_merge(merged, data)
        return merged

    def _notify_subscribers(self, old_merged: dict, new_merged: dict) -> None:
        """Fire subscriber callbacks for every key whose value changed."""
        old_flat = _flatten(old_merged)
        new_flat = _flatten(new_merged)
        all_keys = set(old_flat) | set(new_flat)
        for key in sorted(all_keys):
            old_val = old_flat.get(key)
            new_val = new_flat.get(key)
            if old_val != new_val:
                for cb in list(self._subscribers):
                    try:
                        cb(key, old_val, new_val)
                    except Exception:
                        pass

    def _do_reload(self, path: str) -> None:
        """Parse *path* and update the merged config (caller must hold lock)."""
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext == ".json":
                data = self._parse_json(path)
            elif ext in self._INI_EXTS:
                data = self._parse_ini(path)
            else:
                # Unknown extension: attempt JSON then INI
                try:
                    data = self._parse_json(path)
                except (json.JSONDecodeError, ValueError):
                    data = self._parse_ini(path)
            self._file_data[path] = data
        except (json.JSONDecodeError, configparser.Error, ValueError) as exc:
            # Transient parse error (e.g. file mid-write): keep last-known-good state
            if self._config.on_error is not None:
                self._config.on_error(path, exc)
            return
        except Exception as exc:
            if self._config.on_error is not None:
                self._config.on_error(path, exc)
                return
            raise

        old_merged = self._merged
        self._merged = self._rebuild_merged()
        self._notify_subscribers(old_merged, self._merged)

    def _on_file_changed(self, path: str) -> None:
        """Callback registered with FileWatcher."""
        with self._lock:
            self._do_reload(path)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def load(self, path: str) -> dict:
        """Parse *path* (JSON or INI) and return the raw dict.

        The result is also stored internally so that subsequent calls to
        :meth:`get` and :meth:`snapshot` include it.
        """
        ext = os.path.splitext(path)[1].lower()
        if ext == ".json":
            data = self._parse_json(path)
        elif ext in self._INI_EXTS:
            data = self._parse_ini(path)
        else:
            try:
                data = self._parse_json(path)
            except (json.JSONDecodeError, ValueError):
                data = self._parse_ini(path)
        with self._lock:
            self._file_data[path] = data
            self._merged = self._rebuild_merged()
        return data

    def get(self, key: str, default=None):
        """Return the value at dot-notation *key* in the merged config.

        The last file (in ``paths`` order) that contains a given key wins.
        For nested keys use ``"section.subsection.key"`` notation.

        Returns *default* if the key does not exist.
        """
        parts = key.split(".")
        with self._lock:
            return _get_nested(self._merged, parts, default)

    def snapshot(self) -> dict:
        """Return a deep copy of the current merged configuration dict."""
        with self._lock:
            return copy.deepcopy(self._merged)

    def subscribe(self, callback: Callable[[str, object, object], None]) -> None:
        """Register *callback* invoked as ``callback(key, old_val, new_val)``
        for every key whose value changes after a reload.

        Multiple callbacks may be registered.  Exceptions are silently
        swallowed.
        """
        self._subscribers.append(callback)

    def reload(self, path: str) -> None:
        """Force an immediate re-read of *path* regardless of mtime.

        Useful when you know the file has changed but the watcher has
        not fired yet, or in tests.
        """
        with self._lock:
            self._do_reload(path)

    def start(self) -> None:
        """Load all configured paths immediately, then start the FileWatcher."""
        for path in self._config.paths:
            try:
                self.load(path)
            except Exception as exc:
                if self._config.on_error is not None:
                    self._config.on_error(path, exc)
                else:
                    raise

        self._watcher = FileWatcher(
            paths=self._config.paths,
            interval=self._config.interval,
        )
        self._watcher.on_change(self._on_file_changed)
        self._watcher.start()

    def stop(self) -> None:
        """Stop the FileWatcher background thread."""
        if self._watcher is not None:
            self._watcher.stop()
            self._watcher = None
