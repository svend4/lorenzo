"""E373 DocFormatConverter — pluggable format conversion registry.

Pure stdlib, thread-safe via :class:`threading.Lock`, dataclasses throughout.
"""

from __future__ import annotations

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ConversionPath:
    """A single registered conversion route between two formats."""

    from_format: str
    to_format: str
    converter: object = None
    description: str = ""


@dataclass
class ConversionResult:
    """Outcome of a conversion attempt."""

    from_format: str
    to_format: str
    content: str = ""
    success: bool = True
    error: str = ""
    chain: list[str] = field(default_factory=list)


@dataclass
class ConverterStats:
    """Aggregate statistics."""

    total_paths: int
    total_conversions: int
    success_count: int
    failure_count: int


class DocFormatConverter:
    """Pluggable format-conversion registry with multi-hop BFS chaining."""

    _MAX_HOPS = 5

    def __init__(self) -> None:
        self._paths: dict[tuple, ConversionPath] = {}
        self._total_conversions: int = 0
        self._success_count: int = 0
        self._failure_count: int = 0
        self._lock = threading.Lock()

    # --------------------------------------------------------------- registry

    def register_path(self, path: ConversionPath) -> None:
        """Register a new conversion path or replace an existing one."""
        with self._lock:
            self._paths[(path.from_format, path.to_format)] = path

    def unregister_path(self, from_format: str, to_format: str) -> bool:
        """Remove a registered path. Returns True if it existed."""
        with self._lock:
            key = (from_format, to_format)
            if key in self._paths:
                del self._paths[key]
                return True
            return False

    def get_path(
        self, from_format: str, to_format: str
    ) -> Optional[ConversionPath]:
        """Return the registered path or None."""
        with self._lock:
            return self._paths.get((from_format, to_format))

    def list_paths(self) -> list[ConversionPath]:
        """Return all paths sorted by (from_format, to_format)."""
        with self._lock:
            return sorted(
                self._paths.values(),
                key=lambda p: (p.from_format, p.to_format),
            )

    # ------------------------------------------------------------------- BFS

    def _find_chain_locked(
        self, from_format: str, to_format: str
    ) -> Optional[list[str]]:
        """BFS for the shortest chain of formats. Assumes the lock is held."""
        if from_format == to_format:
            return [from_format]
        # Direct path?
        if (from_format, to_format) in self._paths:
            return [from_format, to_format]

        # Build adjacency.
        adjacency: dict[str, list[str]] = {}
        for src, dst in self._paths.keys():
            adjacency.setdefault(src, []).append(dst)

        if from_format not in adjacency:
            return None

        # BFS with hop limit.
        visited = {from_format}
        # Queue stores (current_format, path_so_far).
        queue: deque = deque([(from_format, [from_format])])
        while queue:
            current, path = queue.popleft()
            # Number of hops used so far == len(path) - 1.
            if len(path) - 1 >= self._MAX_HOPS:
                continue
            for nxt in sorted(adjacency.get(current, [])):
                if nxt in visited:
                    continue
                new_path = path + [nxt]
                if nxt == to_format:
                    return new_path
                visited.add(nxt)
                queue.append((nxt, new_path))
        return None

    def find_chain(
        self, from_format: str, to_format: str
    ) -> Optional[list[str]]:
        """Return the shortest BFS chain of formats, or None."""
        with self._lock:
            return self._find_chain_locked(from_format, to_format)

    def can_convert(self, from_format: str, to_format: str) -> bool:
        """True if a direct or chained path exists."""
        with self._lock:
            return self._find_chain_locked(from_format, to_format) is not None

    # --------------------------------------------------------------- convert

    def convert(
        self, content: str, from_format: str, to_format: str
    ) -> ConversionResult:
        """Convert content from one format to another.

        If no direct path is registered, BFS is used (max 5 hops). Each
        intermediate converter is invoked in turn.
        """
        with self._lock:
            self._total_conversions += 1

            if from_format == to_format:
                self._success_count += 1
                return ConversionResult(
                    from_format=from_format,
                    to_format=to_format,
                    content=content,
                    success=True,
                    error="",
                    chain=[from_format],
                )

            chain = self._find_chain_locked(from_format, to_format)
            if chain is None:
                self._failure_count += 1
                return ConversionResult(
                    from_format=from_format,
                    to_format=to_format,
                    content="",
                    success=False,
                    error=(
                        f"no conversion path from {from_format!r} "
                        f"to {to_format!r}"
                    ),
                    chain=[],
                )

            # Walk the chain, applying each converter.
            current_content = content
            for i in range(len(chain) - 1):
                src = chain[i]
                dst = chain[i + 1]
                path = self._paths.get((src, dst))
                if path is None:
                    # Should not happen since chain came from registry.
                    self._failure_count += 1
                    return ConversionResult(
                        from_format=from_format,
                        to_format=to_format,
                        content="",
                        success=False,
                        error=f"missing path {src!r}->{dst!r}",
                        chain=chain,
                    )
                conv = path.converter
                if conv is None:
                    # Identity passthrough when no callable supplied.
                    continue
                try:
                    current_content = conv(current_content)
                except Exception as exc:  # noqa: BLE001
                    self._failure_count += 1
                    return ConversionResult(
                        from_format=from_format,
                        to_format=to_format,
                        content="",
                        success=False,
                        error=f"{src}->{dst}: {exc}",
                        chain=chain,
                    )

            self._success_count += 1
            return ConversionResult(
                from_format=from_format,
                to_format=to_format,
                content=current_content,
                success=True,
                error="",
                chain=chain,
            )

    # --------------------------------------------------------- introspection

    def available_targets(self, from_format: str) -> list[str]:
        """Return formats directly reachable from from_format, sorted."""
        with self._lock:
            return sorted(
                dst for (src, dst) in self._paths.keys() if src == from_format
            )

    def available_sources(self, to_format: str) -> list[str]:
        """Return formats that can directly convert to to_format, sorted."""
        with self._lock:
            return sorted(
                src for (src, dst) in self._paths.keys() if dst == to_format
            )

    # ----------------------------------------------------------------- misc

    def clear(self) -> int:
        """Remove all registered paths. Returns number cleared."""
        with self._lock:
            count = len(self._paths)
            self._paths.clear()
            return count

    def stats(self) -> ConverterStats:
        """Return aggregate statistics."""
        with self._lock:
            return ConverterStats(
                total_paths=len(self._paths),
                total_conversions=self._total_conversions,
                success_count=self._success_count,
                failure_count=self._failure_count,
            )
