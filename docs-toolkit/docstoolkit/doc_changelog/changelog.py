"""DocChangelog — automated changelog generation from document changes."""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional


class ChangeType(Enum):
    """Type of document change."""

    ADDED = "Added"
    MODIFIED = "Modified"
    REMOVED = "Removed"
    RENAMED = "Renamed"
    MOVED = "Moved"


@dataclass
class DocChangeEntry:
    """One document change entry."""

    doc_id: str
    change_type: ChangeType
    description: str
    timestamp: float = 0.0
    author: Optional[str] = None
    tags: list[str] = field(default_factory=list)


@dataclass
class Release:
    """A released set of document change entries."""

    version: str
    released_at: float
    entries: list[DocChangeEntry] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class ChangelogConfig:
    """Configuration for the document changelog."""

    group_by_type: bool = True
    include_authors: bool = False
    date_format: str = "%Y-%m-%d"
    unreleased_label: str = "Unreleased"


# Canonical ordering used when grouping entries by change type.
_CHANGE_TYPE_ORDER = [
    ChangeType.ADDED,
    ChangeType.MODIFIED,
    ChangeType.REMOVED,
    ChangeType.RENAMED,
    ChangeType.MOVED,
]


class DocChangelog:
    """Automated changelog tracker for document changes."""

    def __init__(self, config: Optional[ChangelogConfig] = None) -> None:
        self._config = config if config is not None else ChangelogConfig()
        self._lock = threading.Lock()
        # Releases stored in insertion (tagging) order.
        self._releases: list[Release] = []
        # Pending unreleased entries (oldest -> newest).
        self._unreleased: list[DocChangeEntry] = []

    # ------------------------------------------------------------------ config
    @property
    def config(self) -> ChangelogConfig:
        return self._config

    # ------------------------------------------------------------------ record
    def record(
        self,
        doc_id: str,
        change_type: ChangeType,
        description: str,
        author: Optional[str] = None,
        tags: Optional[list[str]] = None,
        now: float = 0.0,
    ) -> DocChangeEntry:
        """Record a new unreleased change entry."""
        ts = now if now else time.time()
        entry = DocChangeEntry(
            doc_id=doc_id,
            change_type=change_type,
            description=description,
            timestamp=ts,
            author=author,
            tags=list(tags) if tags else [],
        )
        with self._lock:
            self._unreleased.append(entry)
        return entry

    # ------------------------------------------------------------------ tag
    def tag_release(
        self,
        version: str,
        now: float = 0.0,
        notes: Optional[str] = None,
    ) -> Optional[Release]:
        """Turn currently unreleased entries into a versioned Release.

        Returns the new Release, or None if there are no pending entries
        or the version already exists.
        """
        with self._lock:
            if not self._unreleased:
                return None
            for existing in self._releases:
                if existing.version == version:
                    return None
            ts = now if now else time.time()
            release = Release(
                version=version,
                released_at=ts,
                entries=list(self._unreleased),
                notes=notes,
            )
            self._releases.append(release)
            self._unreleased = []
            return release

    # ------------------------------------------------------------------ queries
    def releases(self) -> list[Release]:
        """Return all releases newest-first. Includes an Unreleased pseudo-release
        if there are pending entries."""
        with self._lock:
            result: list[Release] = []
            if self._unreleased:
                result.append(
                    Release(
                        version=self._config.unreleased_label,
                        released_at=0.0,
                        entries=list(self._unreleased),
                        notes=None,
                    )
                )
            # Released entries newest -> oldest (last tagged first)
            for r in reversed(self._releases):
                result.append(r)
            return result

    def release(self, version: str) -> Optional[Release]:
        """Find a release by version. Also matches the unreleased label."""
        with self._lock:
            if version == self._config.unreleased_label and self._unreleased:
                return Release(
                    version=self._config.unreleased_label,
                    released_at=0.0,
                    entries=list(self._unreleased),
                    notes=None,
                )
            for r in self._releases:
                if r.version == version:
                    return r
            return None

    def latest_release(self) -> Optional[Release]:
        """Return the most-recently-tagged release (excluding Unreleased)."""
        with self._lock:
            if not self._releases:
                return None
            return self._releases[-1]

    def entries_for_doc(self, doc_id: str) -> list[DocChangeEntry]:
        """Return all entries (across releases + unreleased) for a doc."""
        with self._lock:
            result: list[DocChangeEntry] = []
            for r in self._releases:
                for entry in r.entries:
                    if entry.doc_id == doc_id:
                        result.append(entry)
            for entry in self._unreleased:
                if entry.doc_id == doc_id:
                    result.append(entry)
            return result

    def entries_for_release(self, version: str) -> list[DocChangeEntry]:
        """Return entries for a specific release version (or unreleased)."""
        with self._lock:
            if version == self._config.unreleased_label:
                return list(self._unreleased)
            for r in self._releases:
                if r.version == version:
                    return list(r.entries)
            return []

    def entries_since(self, release_version: str) -> list[DocChangeEntry]:
        """Return entries that occurred AFTER the given release.

        Includes entries in releases tagged after `release_version` plus pending
        unreleased entries. Returns empty list if version not found.
        """
        with self._lock:
            idx = -1
            for i, r in enumerate(self._releases):
                if r.version == release_version:
                    idx = i
                    break
            if idx == -1:
                return []
            result: list[DocChangeEntry] = []
            for r in self._releases[idx + 1 :]:
                result.extend(r.entries)
            result.extend(self._unreleased)
            return result

    # ------------------------------------------------------------------ markdown
    def to_markdown(self, version: Optional[str] = None) -> str:
        """Render the changelog as markdown.

        If `version` is provided, only that release is rendered (no top header).
        Otherwise the full changelog is rendered with newest releases first.
        """
        if version is not None:
            rel = self.release(version)
            if rel is None:
                return ""
            return self._render_release(rel).rstrip() + "\n"

        with self._lock:
            unreleased_snapshot = list(self._unreleased)
            releases_snapshot = list(self._releases)

        parts: list[str] = ["# Changelog", ""]

        if unreleased_snapshot:
            pseudo = Release(
                version=self._config.unreleased_label,
                released_at=0.0,
                entries=unreleased_snapshot,
                notes=None,
            )
            parts.append(self._render_release(pseudo))

        for r in reversed(releases_snapshot):
            parts.append(self._render_release(r))

        return "\n".join(parts).rstrip() + "\n"

    # ------------------------------------------------------------------ notes
    def add_release_notes(self, version: str, notes: str) -> bool:
        """Attach (or replace) notes for a specific release."""
        with self._lock:
            for r in self._releases:
                if r.version == version:
                    r.notes = notes
                    return True
            return False

    # ------------------------------------------------------------------ stats
    @property
    def entry_count(self) -> int:
        """Total number of entries (released + unreleased)."""
        with self._lock:
            total = len(self._unreleased)
            for r in self._releases:
                total += len(r.entries)
            return total

    @property
    def release_count(self) -> int:
        """Number of tagged releases (not counting unreleased)."""
        with self._lock:
            return len(self._releases)

    def unreleased_count(self) -> int:
        """Number of currently pending unreleased entries."""
        with self._lock:
            return len(self._unreleased)

    def clear(self) -> None:
        """Wipe all releases and unreleased entries."""
        with self._lock:
            self._releases = []
            self._unreleased = []

    # ------------------------------------------------------------------ helpers
    def _format_timestamp(self, ts: float) -> str:
        if ts <= 0:
            return ""
        try:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            return dt.strftime(self._config.date_format)
        except (ValueError, OSError, OverflowError):
            return ""

    def _render_release(self, release: Release) -> str:
        is_unreleased = release.version == self._config.unreleased_label
        date_str = self._format_timestamp(release.released_at)

        if is_unreleased:
            header = f"## [{release.version}]"
        elif date_str:
            header = f"## [{release.version}] - {date_str}"
        else:
            header = f"## [{release.version}]"

        lines: list[str] = [header, ""]

        if release.notes:
            lines.append(release.notes)
            lines.append("")

        if not release.entries:
            return "\n".join(lines).rstrip() + "\n\n"

        if self._config.group_by_type:
            grouped: dict[ChangeType, list[DocChangeEntry]] = {}
            for e in release.entries:
                grouped.setdefault(e.change_type, []).append(e)
            for ctype in _CHANGE_TYPE_ORDER:
                bucket = grouped.get(ctype)
                if not bucket:
                    continue
                lines.append(f"### {ctype.value}")
                for entry in bucket:
                    lines.append(self._format_entry(entry))
                lines.append("")
        else:
            for entry in release.entries:
                lines.append(self._format_entry(entry))
            lines.append("")

        return "\n".join(lines).rstrip() + "\n\n"

    def _format_entry(self, entry: DocChangeEntry) -> str:
        base = f"- {entry.description} ({entry.doc_id})"
        if self._config.include_authors and entry.author:
            base += f" @{entry.author}"
        return base
