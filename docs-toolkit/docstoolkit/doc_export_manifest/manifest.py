"""E368 DocExportManifest implementation."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ManifestEntry:
    """A single artifact entry in an export manifest."""

    path: str
    doc_id: str
    format: str
    size_bytes: int = 0
    checksum: str = ""


@dataclass
class ExportManifest:
    """Full manifest for a single export run."""

    manifest_id: str
    created_at: float = 0.0
    description: str = ""
    entries: list[ManifestEntry] = field(default_factory=list)


@dataclass
class ManifestStats:
    """Aggregate statistics across all manifests."""

    total_manifests: int
    total_entries: int
    total_size_bytes: int
    unique_docs: int


class DocExportManifest:
    """Main interface for managing export manifests."""

    def __init__(self) -> None:
        self._manifests: dict[str, ExportManifest] = {}
        self._lock = threading.Lock()

    def create_manifest(
        self, description: str = "", now: Optional[float] = None
    ) -> ExportManifest:
        """Create a new empty manifest with a UUID."""
        with self._lock:
            manifest_id = str(uuid.uuid4())
            created_at = now if now is not None else time.time()
            manifest = ExportManifest(
                manifest_id=manifest_id,
                created_at=created_at,
                description=description,
                entries=[],
            )
            self._manifests[manifest_id] = manifest
            return manifest

    def add_entry(self, manifest_id: str, entry: ManifestEntry) -> bool:
        """Append an entry to the manifest. Returns True if manifest existed."""
        with self._lock:
            manifest = self._manifests.get(manifest_id)
            if manifest is None:
                return False
            manifest.entries.append(entry)
            return True

    def remove_entry(self, manifest_id: str, path: str) -> bool:
        """Remove an entry by path. Returns True if entry existed."""
        with self._lock:
            manifest = self._manifests.get(manifest_id)
            if manifest is None:
                return False
            for i, entry in enumerate(manifest.entries):
                if entry.path == path:
                    manifest.entries.pop(i)
                    return True
            return False

    def get_manifest(self, manifest_id: str) -> Optional[ExportManifest]:
        """Retrieve a manifest by id."""
        with self._lock:
            return self._manifests.get(manifest_id)

    def delete_manifest(self, manifest_id: str) -> bool:
        """Delete a manifest. Returns True if it existed."""
        with self._lock:
            if manifest_id in self._manifests:
                del self._manifests[manifest_id]
                return True
            return False

    def list_manifests(self) -> list[ExportManifest]:
        """List all manifests sorted by created_at."""
        with self._lock:
            return sorted(self._manifests.values(), key=lambda m: m.created_at)

    def entries_for_doc(self, doc_id: str) -> list[ManifestEntry]:
        """Return all entries with given doc_id across all manifests, sorted by path."""
        with self._lock:
            result: list[ManifestEntry] = []
            for manifest in self._manifests.values():
                for entry in manifest.entries:
                    if entry.doc_id == doc_id:
                        result.append(entry)
            return sorted(result, key=lambda e: e.path)

    def find_by_checksum(self, checksum: str) -> list[ManifestEntry]:
        """Return all entries matching the given checksum across all manifests."""
        with self._lock:
            result: list[ManifestEntry] = []
            for manifest in self._manifests.values():
                for entry in manifest.entries:
                    if entry.checksum == checksum:
                        result.append(entry)
            return result

    def find_by_path(self, path: str) -> list[ManifestEntry]:
        """Return all entries with the exact path across all manifests."""
        with self._lock:
            result: list[ManifestEntry] = []
            for manifest in self._manifests.values():
                for entry in manifest.entries:
                    if entry.path == path:
                        result.append(entry)
            return result

    def total_size_of(self, manifest_id: str) -> int:
        """Sum of size_bytes for the manifest. Returns 0 if manifest is missing."""
        with self._lock:
            manifest = self._manifests.get(manifest_id)
            if manifest is None:
                return 0
            return sum(entry.size_bytes for entry in manifest.entries)

    def clear(self) -> int:
        """Remove all manifests; return the count of removed manifests."""
        with self._lock:
            count = len(self._manifests)
            self._manifests.clear()
            return count

    def stats(self) -> ManifestStats:
        """Compute aggregate statistics."""
        with self._lock:
            total_manifests = len(self._manifests)
            total_entries = 0
            total_size_bytes = 0
            unique_docs: set[str] = set()
            for manifest in self._manifests.values():
                total_entries += len(manifest.entries)
                for entry in manifest.entries:
                    total_size_bytes += entry.size_bytes
                    unique_docs.add(entry.doc_id)
            return ManifestStats(
                total_manifests=total_manifests,
                total_entries=total_entries,
                total_size_bytes=total_size_bytes,
                unique_docs=len(unique_docs),
            )
