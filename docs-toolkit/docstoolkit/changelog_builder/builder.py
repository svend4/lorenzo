"""Builder for Keep-a-Changelog formatted changelogs from conventional commits."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date as _date
from enum import Enum
from typing import Optional


class ChangeType(Enum):
    """Category of a changelog entry, aligned with Keep-a-Changelog sections."""

    ADDED = "Added"
    CHANGED = "Changed"
    DEPRECATED = "Deprecated"
    REMOVED = "Removed"
    FIXED = "Fixed"
    SECURITY = "Security"
    OTHER = "Other"


# Mapping from conventional commit type prefix to ChangeType
_CONVENTIONAL_MAP: dict[str, ChangeType] = {
    "feat": ChangeType.ADDED,
    "fix": ChangeType.FIXED,
    "docs": ChangeType.OTHER,
    "chore": ChangeType.OTHER,
    "refactor": ChangeType.CHANGED,
    "perf": ChangeType.CHANGED,
    "style": ChangeType.OTHER,
    "test": ChangeType.OTHER,
    "revert": ChangeType.REMOVED,
    "security": ChangeType.SECURITY,
    "deprecate": ChangeType.DEPRECATED,
}

# Conventional commit header: type(scope)!: description
_CONVENTIONAL_RE = re.compile(
    r"^(?P<type>[a-zA-Z]+)"
    r"(?:\((?P<scope>[^)]+)\))?"
    r"(?P<breaking>!)?"
    r":\s*(?P<desc>.+)$"
)

# Markdown release header: ## [version] - YYYY-MM-DD  (date optional)
_RELEASE_HEADER_RE = re.compile(
    r"^##\s+\[(?P<version>[^\]]+)\](?:\s*-\s*(?P<date>\d{4}-\d{2}-\d{2}))?\s*$"
)

# Section header: ### Added / ### Fixed / etc.
_SECTION_HEADER_RE = re.compile(r"^###\s+(?P<name>.+?)\s*$")

# Bullet entry: - description
_BULLET_RE = re.compile(r"^[-*]\s+(?P<desc>.+?)\s*$")


@dataclass
class ChangeEntry:
    """A single changelog entry under a release."""

    change_type: ChangeType
    description: str
    scope: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    pr_number: Optional[int] = None


@dataclass
class Release:
    """A single released (or unreleased) version with its entries."""

    version: str
    date: str
    entries: list[ChangeEntry] = field(default_factory=list)

    @property
    def by_type(self) -> dict[ChangeType, list[ChangeEntry]]:
        """Group entries by ChangeType, preserving insertion order."""
        result: dict[ChangeType, list[ChangeEntry]] = {}
        for entry in self.entries:
            result.setdefault(entry.change_type, []).append(entry)
        return result

    @property
    def entry_count(self) -> int:
        """Total number of entries in this release."""
        return len(self.entries)

    @property
    def is_breaking(self) -> bool:
        """Whether this release contains breaking changes."""
        for entry in self.entries:
            if entry.change_type == ChangeType.REMOVED:
                return True
            if entry.description.startswith("BREAKING:"):
                return True
            if entry.description.startswith("BREAKING CHANGE"):
                return True
        return False


@dataclass
class Changelog:
    """A full changelog containing one or more releases."""

    releases: list[Release] = field(default_factory=list)

    def find_release(self, version: str) -> Optional[Release]:
        """Return the release with the given version, or None."""
        for release in self.releases:
            if release.version == version:
                return release
        return None

    @property
    def latest(self) -> Optional[Release]:
        """Return the most recent non-unreleased release, or the first release."""
        for release in self.releases:
            if release.version.lower() != "unreleased":
                return release
        if self.releases:
            return self.releases[0]
        return None

    @property
    def unreleased(self) -> Optional[Release]:
        """Return the 'Unreleased' release, if present."""
        for release in self.releases:
            if release.version.lower() == "unreleased":
                return release
        return None


class ChangelogBuilder:
    """Builder that assembles a Changelog incrementally."""

    def __init__(self) -> None:
        self._releases: list[Release] = []

    # ----- release / entry management -----

    def add_release(self, version: str, date: Optional[str] = None) -> Release:
        """Create and append a new release; returns it.

        If a release with this version already exists, returns it instead of
        creating a duplicate.
        """
        existing = self._find(version)
        if existing is not None:
            return existing
        if date is None:
            date = _date.today().isoformat()
        release = Release(version=version, date=date)
        self._releases.append(release)
        return release

    def add_entry(
        self,
        version: str,
        change_type: ChangeType,
        description: str,
        **kwargs,
    ) -> None:
        """Add an entry to the release with the given version.

        Creates the release implicitly if it does not yet exist.
        """
        release = self._find(version)
        if release is None:
            release = self.add_release(version)
        entry = ChangeEntry(
            change_type=change_type,
            description=description,
            scope=kwargs.get("scope"),
            author=kwargs.get("author"),
            date=kwargs.get("date"),
            pr_number=kwargs.get("pr_number"),
        )
        release.entries.append(entry)

    def build(self) -> Changelog:
        """Return the assembled Changelog."""
        return Changelog(releases=list(self._releases))

    # ----- conventional commit parsing -----

    def parse_conventional(self, commit_msg: str) -> Optional[ChangeEntry]:
        """Parse a single conventional-commit-style message into a ChangeEntry.

        Returns None if the message does not match the conventional format.
        """
        if not commit_msg:
            return None
        # Only consider the first line as the header
        header = commit_msg.splitlines()[0].strip()
        match = _CONVENTIONAL_RE.match(header)
        if not match:
            return None
        type_token = match.group("type").lower()
        change_type = _CONVENTIONAL_MAP.get(type_token)
        if change_type is None:
            change_type = ChangeType.OTHER
        scope = match.group("scope")
        breaking = bool(match.group("breaking"))
        description = match.group("desc").strip()

        # If body contains BREAKING CHANGE, mark breaking via description prefix
        body = "\n".join(commit_msg.splitlines()[1:])
        if "BREAKING CHANGE" in body or breaking:
            if not description.startswith("BREAKING"):
                description = f"BREAKING: {description}"

        return ChangeEntry(
            change_type=change_type,
            description=description,
            scope=scope,
        )

    def parse_commits(
        self,
        commits: list[str],
        version: str = "Unreleased",
    ) -> Release:
        """Parse a list of commit messages and append them to a release."""
        release = self._find(version)
        if release is None:
            release = self.add_release(version)
        for msg in commits:
            entry = self.parse_conventional(msg)
            if entry is not None:
                release.entries.append(entry)
        return release

    # ----- markdown rendering -----

    def to_markdown(self, changelog: Changelog) -> str:
        """Render a Changelog as Keep-a-Changelog formatted markdown."""
        lines: list[str] = ["# Changelog", ""]
        if not changelog.releases:
            return "\n".join(lines).rstrip() + "\n"

        # Preferred ordering of sections within a release
        section_order = [
            ChangeType.ADDED,
            ChangeType.CHANGED,
            ChangeType.DEPRECATED,
            ChangeType.REMOVED,
            ChangeType.FIXED,
            ChangeType.SECURITY,
            ChangeType.OTHER,
        ]

        for release in changelog.releases:
            header = f"## [{release.version}]"
            if release.date:
                header += f" - {release.date}"
            lines.append(header)
            lines.append("")

            grouped = release.by_type
            if not grouped:
                # Empty release — still keep a blank line for clarity
                continue

            for change_type in section_order:
                entries = grouped.get(change_type)
                if not entries:
                    continue
                lines.append(f"### {change_type.value}")
                for entry in entries:
                    desc = entry.description
                    prefix = ""
                    if entry.scope:
                        prefix = f"**{entry.scope}**: "
                    suffix_parts: list[str] = []
                    if entry.pr_number is not None:
                        suffix_parts.append(f"(#{entry.pr_number})")
                    if entry.author:
                        suffix_parts.append(f"@{entry.author}")
                    suffix = (" " + " ".join(suffix_parts)) if suffix_parts else ""
                    lines.append(f"- {prefix}{desc}{suffix}")
                lines.append("")

        return "\n".join(lines).rstrip() + "\n"

    # ----- markdown parsing -----

    def from_markdown(self, text: str) -> Changelog:
        """Parse Keep-a-Changelog formatted markdown back into a Changelog."""
        # Reverse-lookup: section header name -> ChangeType
        name_to_type: dict[str, ChangeType] = {ct.value: ct for ct in ChangeType}

        releases: list[Release] = []
        current_release: Optional[Release] = None
        current_type: Optional[ChangeType] = None

        for raw_line in text.splitlines():
            line = raw_line.rstrip()
            if not line:
                continue

            release_match = _RELEASE_HEADER_RE.match(line)
            if release_match:
                version = release_match.group("version")
                date = release_match.group("date") or ""
                current_release = Release(version=version, date=date)
                releases.append(current_release)
                current_type = None
                continue

            section_match = _SECTION_HEADER_RE.match(line)
            if section_match and current_release is not None:
                name = section_match.group("name").strip()
                current_type = name_to_type.get(name, ChangeType.OTHER)
                continue

            bullet_match = _BULLET_RE.match(line)
            if bullet_match and current_release is not None and current_type is not None:
                desc = bullet_match.group("desc").strip()
                scope: Optional[str] = None

                # Parse "**scope**: rest"
                scope_match = re.match(r"^\*\*(?P<scope>[^*]+)\*\*:\s*(?P<rest>.+)$", desc)
                if scope_match:
                    scope = scope_match.group("scope").strip()
                    desc = scope_match.group("rest").strip()

                # Parse trailing " @author"
                author: Optional[str] = None
                author_match = re.search(r"\s+@([A-Za-z0-9_\-]+)\s*$", desc)
                if author_match:
                    author = author_match.group(1)
                    desc = desc[: author_match.start()].rstrip()

                # Parse trailing " (#123)"
                pr_number: Optional[int] = None
                pr_match = re.search(r"\s*\(#(\d+)\)\s*$", desc)
                if pr_match:
                    pr_number = int(pr_match.group(1))
                    desc = desc[: pr_match.start()].rstrip()

                entry = ChangeEntry(
                    change_type=current_type,
                    description=desc,
                    scope=scope,
                    author=author,
                    pr_number=pr_number,
                )
                current_release.entries.append(entry)

        return Changelog(releases=releases)

    # ----- internal helpers -----

    def _find(self, version: str) -> Optional[Release]:
        for release in self._releases:
            if release.version == version:
                return release
        return None
