"""Config source adapters — each source exposes load() -> dict."""
import configparser
import json
import os
from abc import ABC, abstractmethod
from pathlib import Path


class ConfigSource(ABC):
    """Abstract base for all configuration sources."""

    @abstractmethod
    def load(self) -> dict:
        """Return a (possibly nested) dict of configuration values."""


# ---------------------------------------------------------------------------
# DictSource
# ---------------------------------------------------------------------------

class DictSource(ConfigSource):
    """Wraps a plain in-memory dict."""

    def __init__(self, data: dict) -> None:
        self._data = data

    def load(self) -> dict:
        return dict(self._data)


# ---------------------------------------------------------------------------
# EnvSource
# ---------------------------------------------------------------------------

class EnvSource(ConfigSource):
    """Reads os.environ, strips *prefix*, lowercases keys,
    and converts ``A__B__C`` → nested dict ``{"a": {"b": {"c": value}}}``.

    Parameters
    ----------
    prefix:
        Optional prefix that variable names must start with.  The prefix
        itself (plus the separator that follows it) is stripped before the
        remaining key is processed.  An empty string means "all variables".
    separator:
        Segment separator used to build nesting.  Default ``"__"``
        (double-underscore).
    """

    def __init__(self, prefix: str = "", separator: str = "__") -> None:
        self._prefix = prefix
        self._separator = separator

    # ------------------------------------------------------------------
    # internal helpers
    # ------------------------------------------------------------------

    def _set_nested(self, root: dict, parts: list, value: str) -> None:
        """Write *value* into *root* at the path described by *parts*."""
        node = root
        for part in parts[:-1]:
            if part not in node or not isinstance(node[part], dict):
                node[part] = {}
            node = node[part]
        node[parts[-1]] = value

    # ------------------------------------------------------------------

    def load(self) -> dict:
        result: dict = {}
        prefix = self._prefix
        sep = self._separator

        for raw_key, value in os.environ.items():
            # Prefix filtering
            if prefix:
                if not raw_key.startswith(prefix):
                    continue
                # Strip prefix; also strip a single separator that
                # immediately follows the prefix (e.g. "APP__DB" → "DB").
                remainder = raw_key[len(prefix):]
                if remainder.startswith(sep):
                    remainder = remainder[len(sep):]
            else:
                remainder = raw_key

            if not remainder:
                continue

            # Lowercase and split into path segments
            parts = remainder.lower().split(sep)
            # Filter out empty parts (e.g. from a trailing separator)
            parts = [p for p in parts if p]
            if not parts:
                continue

            self._set_nested(result, parts, value)

        return result


# ---------------------------------------------------------------------------
# JsonFileSource
# ---------------------------------------------------------------------------

class JsonFileSource(ConfigSource):
    """Loads configuration from a JSON file.

    * Raises ``FileNotFoundError`` if the file does not exist at load time.
    * Calls ``load()`` re-reads the file each invocation (live-reload
      semantics).
    """

    def __init__(self, path) -> None:
        self._path = Path(path)

    def load(self) -> dict:
        if not self._path.exists():
            raise FileNotFoundError(f"Config file not found: {self._path}")
        with self._path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, dict):
            raise ValueError(
                f"JSON config must be a top-level object (dict), got "
                f"{type(data).__name__}: {self._path}"
            )
        return data


# ---------------------------------------------------------------------------
# IniFileSource
# ---------------------------------------------------------------------------

class IniFileSource(ConfigSource):
    """Loads configuration from an INI file using :mod:`configparser`.

    * Sections become top-level dict keys.
    * The ``[DEFAULT]`` section (if any) is merged into every section by
      ``configparser`` automatically — behaviour consistent with the stdlib.
    * All values are strings (as delivered by ``configparser``).
    """

    def __init__(self, path) -> None:
        self._path = Path(path)

    def load(self) -> dict:
        if not self._path.exists():
            raise FileNotFoundError(f"Config file not found: {self._path}")
        parser = configparser.ConfigParser()
        parser.read(str(self._path), encoding="utf-8")

        result: dict = {}
        for section in parser.sections():
            result[section] = dict(parser[section])
        return result
