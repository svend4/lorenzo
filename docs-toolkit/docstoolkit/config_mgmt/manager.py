"""ConfigManager — merges multiple ConfigSource instances with deep merge."""
import copy
from docstoolkit.config_mgmt.source import ConfigSource


def _deep_merge(base: dict, override: dict) -> dict:
    """Recursively merge *override* into *base*.

    * If both values for a key are dicts, merge recursively.
    * Otherwise the *override* value wins.

    Neither *base* nor *override* is mutated; a new dict is returned.
    """
    result = copy.deepcopy(base)
    for key, val in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(val, dict)
        ):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = copy.deepcopy(val)
    return result


def _set_nested(root: dict, parts: list, value) -> None:
    """Write *value* into *root* dict at the dot-notation path *parts*."""
    node = root
    for part in parts[:-1]:
        if part not in node or not isinstance(node[part], dict):
            node[part] = {}
        node = node[part]
    node[parts[-1]] = value


def _get_nested(root: dict, parts: list, default=None):
    """Traverse *root* following *parts*; return *default* on any miss."""
    node = root
    for part in parts:
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node


class ConfigManager:
    """Aggregates multiple :class:`~docstoolkit.config_mgmt.source.ConfigSource`
    objects and exposes a unified config dict with typed accessor helpers.

    Sources are merged in registration order: later sources override
    earlier ones (last-wins shallow at scalar level, recursive for dicts).

    Usage::

        mgr = ConfigManager([DictSource({"db": {"host": "localhost"}})])
        mgr.add_source(EnvSource(prefix="APP"))
        mgr.load()
        mgr.get("db.host")          # "localhost" (or env override)
        mgr.get_int("db.port", 5432)
    """

    def __init__(self, sources: list = None) -> None:
        self._sources: list[ConfigSource] = list(sources) if sources else []
        self._config: dict = {}

    # ------------------------------------------------------------------
    # Source management
    # ------------------------------------------------------------------

    def add_source(self, source: ConfigSource) -> None:
        """Append *source* to the end of the source list (highest priority so far)."""
        self._sources.append(source)

    # ------------------------------------------------------------------
    # Loading / merging
    # ------------------------------------------------------------------

    def load(self) -> None:
        """Re-read every source and rebuild the merged config dict.

        Later sources override earlier ones via deep merge.
        """
        merged: dict = {}
        for source in self._sources:
            data = source.load()
            merged = _deep_merge(merged, data)
        self._config = merged

    # ------------------------------------------------------------------
    # Accessors
    # ------------------------------------------------------------------

    def get(self, key: str, default=None):
        """Return value at dot-notation *key*, or *default* if absent.

        Example::

            mgr.get("database.host", "localhost")
        """
        parts = key.split(".")
        return _get_nested(self._config, parts, default)

    def get_int(self, key: str, default: int = 0) -> int:
        """Return config value coerced to ``int``.

        Falls back to *default* if the key is missing.  Raises
        ``ValueError`` / ``TypeError`` if present but not convertible.
        """
        val = self.get(key)
        if val is None:
            return default
        return int(val)

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Return config value coerced to ``float``."""
        val = self.get(key)
        if val is None:
            return default
        return float(val)

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Return config value coerced to ``bool``.

        Truthy string values: ``"1"``, ``"true"``, ``"yes"``, ``"on"``
        (case-insensitive).  All other strings are falsy.  Non-string
        values are passed through :func:`bool` directly.
        """
        val = self.get(key)
        if val is None:
            return default
        if isinstance(val, bool):
            return val
        if isinstance(val, str):
            return val.strip().lower() in {"1", "true", "yes", "on"}
        return bool(val)

    def get_list(self, key: str, separator: str = ",", default: list = None) -> list:
        """Return config value as a list.

        * If the stored value is already a ``list``, it is returned as-is.
        * If the stored value is a string, it is split by *separator*;
          leading/trailing whitespace is stripped from each element.
        * If the key is absent, *default* is returned (empty list when
          *default* is ``None``).
        """
        if default is None:
            default = []
        val = self.get(key)
        if val is None:
            return default
        if isinstance(val, list):
            return val
        return [item.strip() for item in str(val).split(separator)]

    # ------------------------------------------------------------------
    # In-memory override
    # ------------------------------------------------------------------

    def set(self, key: str, value) -> None:
        """Set *value* at dot-notation *key* in the in-memory config.

        This does **not** persist to any source; it only affects the
        current merged dict until the next :meth:`load` call.
        """
        parts = key.split(".")
        _set_nested(self._config, parts, value)

    # ------------------------------------------------------------------
    # Inspection
    # ------------------------------------------------------------------

    def all(self) -> dict:
        """Return a deep copy of the full merged configuration dict."""
        return copy.deepcopy(self._config)
