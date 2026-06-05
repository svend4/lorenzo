"""E384 DocPathResolver implementation.

Hierarchical document path resolver with thread-safe operations.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PathMapping:
    """A single path-to-doc mapping."""

    path: str
    doc_id: str
    created_at: float = 0.0


@dataclass
class PathResolverStats:
    """Aggregate statistics for the resolver."""

    total_mappings: int
    unique_paths: int
    unique_docs: int
    total_segments: int


class DocPathResolver:
    """Resolve hierarchical document paths to doc IDs."""

    def __init__(self) -> None:
        self._path_to_doc: dict[str, PathMapping] = {}
        self._doc_to_paths: dict[str, set[str]] = {}
        self._lock = threading.Lock()

    # ---------------------------------------------------------------- helpers

    @staticmethod
    def _normalize(path: str) -> str:
        """Strip trailing slashes (except root); ensure leading slash; collapse multiple slashes."""
        if not isinstance(path, str):
            raise TypeError("path must be a string")
        if path == "":
            return "/"
        # Collapse multiple slashes
        while "//" in path:
            path = path.replace("//", "/")
        # Ensure leading slash
        if not path.startswith("/"):
            path = "/" + path
        # Strip trailing slash (except root)
        if len(path) > 1 and path.endswith("/"):
            path = path.rstrip("/")
            if path == "":
                path = "/"
        return path

    @staticmethod
    def segments_of(path: str) -> list[str]:
        """Split path into segments (excluding empty)."""
        normalized = DocPathResolver._normalize(path)
        return [s for s in normalized.split("/") if s]

    # ---------------------------------------------------------------- mapping

    def map_path(
        self, path: str, doc_id: str, now: Optional[float] = None
    ) -> PathMapping:
        """Normalize path and create or replace a mapping."""
        normalized = self._normalize(path)
        ts = now if now is not None else time.time()
        mapping = PathMapping(path=normalized, doc_id=doc_id, created_at=ts)
        with self._lock:
            # If path is already mapped, remove old reverse-link
            existing = self._path_to_doc.get(normalized)
            if existing is not None:
                old_doc = existing.doc_id
                if old_doc in self._doc_to_paths:
                    self._doc_to_paths[old_doc].discard(normalized)
                    if not self._doc_to_paths[old_doc]:
                        del self._doc_to_paths[old_doc]
            self._path_to_doc[normalized] = mapping
            self._doc_to_paths.setdefault(doc_id, set()).add(normalized)
        return mapping

    def unmap_path(self, path: str) -> bool:
        """Remove a path mapping. Return True if existed."""
        normalized = self._normalize(path)
        with self._lock:
            existing = self._path_to_doc.pop(normalized, None)
            if existing is None:
                return False
            doc_id = existing.doc_id
            if doc_id in self._doc_to_paths:
                self._doc_to_paths[doc_id].discard(normalized)
                if not self._doc_to_paths[doc_id]:
                    del self._doc_to_paths[doc_id]
            return True

    def unmap_doc(self, doc_id: str) -> int:
        """Remove all paths pointing to doc_id. Return count removed."""
        with self._lock:
            paths = self._doc_to_paths.pop(doc_id, set())
            count = 0
            for p in paths:
                if p in self._path_to_doc:
                    del self._path_to_doc[p]
                    count += 1
            return count

    # ---------------------------------------------------------------- queries

    def resolve(self, path: str) -> Optional[str]:
        """Return doc_id for the normalized path, or None."""
        normalized = self._normalize(path)
        with self._lock:
            mapping = self._path_to_doc.get(normalized)
            return mapping.doc_id if mapping is not None else None

    def paths_for(self, doc_id: str) -> list[str]:
        """Return sorted paths pointing to doc_id."""
        with self._lock:
            return sorted(self._doc_to_paths.get(doc_id, set()))

    def children_of(self, parent_path: str) -> list[str]:
        """Return sorted paths that are direct children (one level deeper) of parent_path."""
        normalized_parent = self._normalize(parent_path)
        parent_segments = self.segments_of(normalized_parent)
        parent_depth = len(parent_segments)
        with self._lock:
            paths = list(self._path_to_doc.keys())
        result: list[str] = []
        for p in paths:
            if p == normalized_parent:
                continue
            p_segs = self.segments_of(p)
            if len(p_segs) != parent_depth + 1:
                continue
            # Check that p starts with parent
            if normalized_parent == "/":
                # root: any single-segment path qualifies
                result.append(p)
            else:
                if p.startswith(normalized_parent + "/"):
                    result.append(p)
        return sorted(result)

    def descendants_of(self, parent_path: str) -> list[str]:
        """Return sorted paths under parent_path (deeper than parent_path)."""
        normalized_parent = self._normalize(parent_path)
        with self._lock:
            paths = list(self._path_to_doc.keys())
        result: list[str] = []
        for p in paths:
            if p == normalized_parent:
                continue
            if normalized_parent == "/":
                # everything that is not "/" is a descendant
                if p != "/":
                    result.append(p)
            else:
                if p.startswith(normalized_parent + "/"):
                    result.append(p)
        return sorted(result)

    def parent_of(self, path: str) -> Optional[str]:
        """Return normalized parent path, or None if root or no parent."""
        normalized = self._normalize(path)
        if normalized == "/":
            return None
        segs = self.segments_of(normalized)
        if len(segs) == 0:
            return None
        if len(segs) == 1:
            return "/"
        return "/" + "/".join(segs[:-1])

    def all_paths(self) -> list[PathMapping]:
        """Return all mappings sorted by path."""
        with self._lock:
            mappings = list(self._path_to_doc.values())
        return sorted(mappings, key=lambda m: m.path)

    def clear(self) -> int:
        """Clear everything. Return count of mappings removed."""
        with self._lock:
            count = len(self._path_to_doc)
            self._path_to_doc.clear()
            self._doc_to_paths.clear()
            return count

    def stats(self) -> PathResolverStats:
        """Compute aggregate statistics."""
        with self._lock:
            total_mappings = len(self._path_to_doc)
            unique_paths = len(self._path_to_doc)
            unique_docs = len(self._doc_to_paths)
            total_segments = 0
            for p in self._path_to_doc.keys():
                total_segments += len([s for s in p.split("/") if s])
        return PathResolverStats(
            total_mappings=total_mappings,
            unique_paths=unique_paths,
            unique_docs=unique_docs,
            total_segments=total_segments,
        )
