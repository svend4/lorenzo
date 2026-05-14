"""Layered settings with cascade resolution.

Resolution order (highest to lowest priority):
    RUNTIME -> USER -> ENV -> FILE -> DEFAULTS
"""
from __future__ import annotations

import threading
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Optional


class LayerName(Enum):
    DEFAULTS = "defaults"
    FILE = "file"
    ENV = "env"
    USER = "user"
    RUNTIME = "runtime"


# Priority order: higher index = higher priority
_PRIORITY = [
    LayerName.DEFAULTS,
    LayerName.FILE,
    LayerName.ENV,
    LayerName.USER,
    LayerName.RUNTIME,
]


@dataclass
class Setting:
    key: str
    value: Any
    layer: LayerName
    source: Optional[str] = None


def _coerce(new_value: Any, existing_value: Any) -> Any:
    """Coerce a (typically string) env value to the type of existing_value."""
    if existing_value is None:
        return new_value
    if isinstance(new_value, type(existing_value)) and not isinstance(existing_value, bool):
        # Already correct type (but bool is subtype of int, careful)
        return new_value
    if not isinstance(new_value, str):
        return new_value
    target_type = type(existing_value)
    try:
        if target_type is bool:
            low = new_value.strip().lower()
            if low in ("true", "1", "yes", "on"):
                return True
            if low in ("false", "0", "no", "off", ""):
                return False
            return new_value
        if target_type is int:
            return int(new_value)
        if target_type is float:
            return float(new_value)
        if target_type is str:
            return new_value
    except (ValueError, TypeError):
        return new_value
    return new_value


class SettingsLayer:
    """Layered settings with cascade resolution and subscription support."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._layers: dict[LayerName, dict[str, Any]] = {
            layer: {} for layer in LayerName
        }
        self._sources: dict[LayerName, dict[str, Optional[str]]] = {
            layer: {} for layer in LayerName
        }
        self._subs: dict[int, tuple[str, Callable[[str, Any, Any], None]]] = {}
        self._next_sub_id = 1

    # ---- Defaults layer ----
    def set_default(self, key: str, value: Any) -> None:
        with self._lock:
            self._layers[LayerName.DEFAULTS][key] = value

    def set_defaults(self, values: dict) -> None:
        with self._lock:
            for k, v in values.items():
                self._layers[LayerName.DEFAULTS][k] = v

    # ---- File layer ----
    def load_file_layer(self, values: dict, source: Optional[str] = None) -> None:
        notifications: list[tuple[str, Any, Any]] = []
        with self._lock:
            for key, raw_value in values.items():
                old_effective = self._resolve_locked(key)
                # Coerce against existing (defaults) value if applicable
                existing = self._layers[LayerName.DEFAULTS].get(key)
                value = _coerce(raw_value, existing) if existing is not None else raw_value
                self._layers[LayerName.FILE][key] = value
                self._sources[LayerName.FILE][key] = source
                new_effective = self._resolve_locked(key)
                if old_effective != new_effective:
                    notifications.append((key, old_effective, new_effective))
            subs = list(self._subs.values())
        self._fire(subs, notifications)

    # ---- Env layer ----
    def load_env_layer(self, env: dict, prefix: str = "") -> None:
        notifications: list[tuple[str, Any, Any]] = []
        with self._lock:
            for raw_key, raw_value in env.items():
                if prefix and not raw_key.startswith(prefix):
                    continue
                stripped = raw_key[len(prefix):] if prefix else raw_key
                key = stripped.lower()
                if not key:
                    continue
                old_effective = self._resolve_locked(key)
                # Try coerce against existing lower-priority layer (file/defaults)
                existing = None
                for lower in (LayerName.FILE, LayerName.DEFAULTS):
                    if key in self._layers[lower]:
                        existing = self._layers[lower][key]
                        break
                value = _coerce(raw_value, existing) if existing is not None else raw_value
                self._layers[LayerName.ENV][key] = value
                self._sources[LayerName.ENV][key] = raw_key
                new_effective = self._resolve_locked(key)
                if old_effective != new_effective:
                    notifications.append((key, old_effective, new_effective))
            subs = list(self._subs.values())
        self._fire(subs, notifications)

    # ---- User layer ----
    def set_user(self, key: str, value: Any) -> None:
        with self._lock:
            old_effective = self._resolve_locked(key)
            self._layers[LayerName.USER][key] = value
            new_effective = self._resolve_locked(key)
            changed = old_effective != new_effective
            subs = list(self._subs.values()) if changed else []
            note = [(key, old_effective, new_effective)] if changed else []
        self._fire(subs, note)

    # ---- Runtime layer ----
    def set_runtime(self, key: str, value: Any) -> None:
        with self._lock:
            old_effective = self._resolve_locked(key)
            self._layers[LayerName.RUNTIME][key] = value
            new_effective = self._resolve_locked(key)
            changed = old_effective != new_effective
            subs = list(self._subs.values()) if changed else []
            note = [(key, old_effective, new_effective)] if changed else []
        self._fire(subs, note)

    # ---- Resolution ----
    def _resolve_locked(self, key: str) -> Any:
        for layer in reversed(_PRIORITY):
            if key in self._layers[layer]:
                return self._layers[layer][key]
        return None

    def _resolve_layer_locked(self, key: str) -> Optional[LayerName]:
        for layer in reversed(_PRIORITY):
            if key in self._layers[layer]:
                return layer
        return None

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            layer = self._resolve_layer_locked(key)
            if layer is None:
                return default
            return self._layers[layer][key]

    def get_layer(self, key: str) -> Optional[LayerName]:
        with self._lock:
            return self._resolve_layer_locked(key)

    def get_setting(self, key: str) -> Optional[Setting]:
        with self._lock:
            layer = self._resolve_layer_locked(key)
            if layer is None:
                return None
            return Setting(
                key=key,
                value=self._layers[layer][key],
                layer=layer,
                source=self._sources[layer].get(key),
            )

    def has(self, key: str) -> bool:
        with self._lock:
            return self._resolve_layer_locked(key) is not None

    def all_keys(self) -> set[str]:
        with self._lock:
            keys: set[str] = set()
            for layer in LayerName:
                keys.update(self._layers[layer].keys())
            return keys

    def effective_settings(self) -> dict[str, Any]:
        with self._lock:
            keys: set[str] = set()
            for layer in LayerName:
                keys.update(self._layers[layer].keys())
            return {k: self._resolve_locked(k) for k in keys}

    def layer_values(self, layer: LayerName) -> dict[str, Any]:
        with self._lock:
            return dict(self._layers[layer])

    # ---- Clearing ----
    def clear_layer(self, layer: LayerName) -> int:
        notifications: list[tuple[str, Any, Any]] = []
        with self._lock:
            keys = list(self._layers[layer].keys())
            count = len(keys)
            old_values = {k: self._resolve_locked(k) for k in keys}
            self._layers[layer].clear()
            self._sources[layer].clear()
            for k in keys:
                new_val = self._resolve_locked(k)
                if old_values[k] != new_val:
                    notifications.append((k, old_values[k], new_val))
            subs = list(self._subs.values())
        self._fire(subs, notifications)
        return count

    def clear_all(self) -> None:
        with self._lock:
            for layer in LayerName:
                self._layers[layer].clear()
                self._sources[layer].clear()

    # ---- Subscriptions ----
    def subscribe(self, key: str, callback: Callable[[str, Any, Any], None]) -> int:
        with self._lock:
            sub_id = self._next_sub_id
            self._next_sub_id += 1
            self._subs[sub_id] = (key, callback)
            return sub_id

    def unsubscribe(self, sub_id: int) -> bool:
        with self._lock:
            if sub_id in self._subs:
                del self._subs[sub_id]
                return True
            return False

    def _fire(
        self,
        subs: list[tuple[str, Callable[[str, Any, Any], None]]],
        notifications: list[tuple[str, Any, Any]],
    ) -> None:
        for key, old, new in notifications:
            for sub_key, cb in subs:
                if sub_key == key or sub_key == "*":
                    try:
                        cb(key, old, new)
                    except Exception:
                        pass

    # ---- Export/Import ----
    def export(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            return {
                layer.value: dict(self._layers[layer])
                for layer in LayerName
            }

    def import_(self, data: dict[str, dict[str, Any]]) -> None:
        with self._lock:
            for layer in LayerName:
                self._layers[layer].clear()
                self._sources[layer].clear()
            for layer_name, values in data.items():
                try:
                    layer = LayerName(layer_name)
                except ValueError:
                    continue
                for k, v in values.items():
                    self._layers[layer][k] = v
