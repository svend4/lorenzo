"""Hierarchical counter built on top of :class:`CounterStore`.

Keys are encoded as ``separator``-joined path components (e.g.
``"users.active.premium"``), which allows efficient roll-ups via prefix
scans on the underlying store.
"""
from __future__ import annotations

from typing import Dict, List, Optional

from docstoolkit.dist_counter.counter import CounterError, CounterStore


class HierarchicalCounter:
    """Treat a :class:`CounterStore` as a tree of counters.

    Each hierarchical counter is identified by a list of path components
    (e.g. ``["users", "active", "premium"]``) that are joined with
    *separator* to form the underlying counter key.
    """

    def __init__(self, store: CounterStore, separator: str = "."):
        if not isinstance(separator, str) or separator == "":
            raise CounterError("separator must be a non-empty string")
        self._store = store
        self._sep = separator

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _key(self, path: List[str]) -> str:
        if not isinstance(path, list):
            raise CounterError("path must be a list of strings")
        for p in path:
            if not isinstance(p, str) or p == "":
                raise CounterError("path components must be non-empty strings")
            if self._sep in p:
                raise CounterError(
                    f"path component {p!r} contains the separator "
                    f"{self._sep!r}"
                )
        return self._sep.join(path)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def increment(self, path: List[str], delta: int = 1) -> int:
        """Increment the leaf counter at *path* by *delta* and return new value."""
        key = self._key(path)
        return self._store.increment(key, delta)

    def get(self, path: List[str]) -> int:
        """Return the value of the leaf counter at *path*, or 0 if missing."""
        key = self._key(path)
        return self._store.get(key)

    def rollup(self, path: List[str]) -> int:
        """Sum of all counters whose key falls under *path*.

        The roll-up matches:
          - the exact key at ``path``
          - any descendant key of the form ``path + separator + ...``

        It deliberately does NOT match sibling keys that merely share a
        textual prefix (e.g. ``"user"`` should not match ``"users"``).
        """
        if not path:
            return self._store.total()

        key = self._key(path)
        # Sum exact match + all descendants (key + separator + ...).
        exact = self._store.get(key)
        descendants = self._store.total(key + self._sep)
        return exact + descendants

    def children(self, path: List[str]) -> List[str]:
        """Return the *direct* children keys under *path*.

        For a *path* of ``["users", "active"]`` and store keys
        ``["users.active.premium", "users.active.free",
        "users.active.premium.us"]`` this returns
        ``["users.active.free", "users.active.premium"]``.

        With an empty *path* the direct children at the root are returned.
        """
        if path:
            key = self._key(path)
            prefix = key + self._sep
        else:
            prefix = ""

        # Collect all rows under prefix, then keep only those whose remainder
        # has no further separator (i.e. direct children).
        all_rows = self._store.list_all(prefix=prefix)
        seen: List[str] = []
        seen_set = set()
        for row in all_rows:
            remainder = row.key[len(prefix):]
            if remainder == "":
                # the key equals prefix without the trailing separator
                # — this happens when prefix is empty and a root counter
                # has been written.  Treat as a direct child.
                if row.key not in seen_set:
                    seen.append(row.key)
                    seen_set.add(row.key)
                continue
            if self._sep in remainder:
                # Not a direct child; record the *first* segment after prefix
                head = remainder.split(self._sep, 1)[0]
                child_key = prefix + head
                if child_key not in seen_set:
                    seen.append(child_key)
                    seen_set.add(child_key)
            else:
                # Direct child
                if row.key not in seen_set:
                    seen.append(row.key)
                    seen_set.add(row.key)
        seen.sort()
        return seen

    def tree(self, path: Optional[List[str]] = None) -> Dict:
        """Return a nested dict of counters under *path* (root if None).

        The result has the shape::

            {
                "<child>": {
                    "_value": <int or None>,
                    "<grandchild>": { ... },
                    ...
                },
                ...
            }

        ``_value`` is present only for leaves that actually have a counter
        row in the underlying store.
        """
        if path:
            key_prefix = self._key(path)
            scan_prefix = key_prefix + self._sep
        else:
            scan_prefix = ""

        rows = self._store.list_all(prefix=scan_prefix)
        root: Dict = {}
        for row in rows:
            remainder = row.key[len(scan_prefix):]
            if remainder == "":
                # ``row.key`` exactly equals the scan_prefix without trailing
                # separator.  We can only hit this when scan_prefix == "" and
                # row.key == "" (impossible for non-empty keys) — ignore.
                continue
            parts = remainder.split(self._sep)
            node = root
            for i, part in enumerate(parts):
                if part not in node:
                    node[part] = {}
                if i == len(parts) - 1:
                    node[part]["_value"] = int(row.value)
                node = node[part]
        return root
