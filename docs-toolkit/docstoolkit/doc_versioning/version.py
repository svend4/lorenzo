"""Semantic versioning for documentation files."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):
    """Classification of a change between two document versions."""

    MAJOR = "MAJOR"   # structural / semantic change
    MINOR = "MINOR"   # content addition
    PATCH = "PATCH"   # typo / formatting fix
    NONE = "NONE"     # no change


@dataclass
class DocVersion:
    """Immutable semantic version triple for a document."""

    major: int
    minor: int
    patch: int

    # ------------------------------------------------------------------
    # String representation
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:  # pragma: no cover
        return f"DocVersion({self.major}, {self.minor}, {self.patch})"

    # ------------------------------------------------------------------
    # Comparison helpers (needed for sorting in history)
    # ------------------------------------------------------------------

    def _tuple(self) -> tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DocVersion):
            return NotImplemented
        return self._tuple() == other._tuple()

    def __lt__(self, other: DocVersion) -> bool:
        return self._tuple() < other._tuple()

    def __le__(self, other: DocVersion) -> bool:
        return self._tuple() <= other._tuple()

    def __gt__(self, other: DocVersion) -> bool:
        return self._tuple() > other._tuple()

    def __ge__(self, other: DocVersion) -> bool:
        return self._tuple() >= other._tuple()

    def __hash__(self) -> int:
        return hash(self._tuple())

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def bump(self, change_type: ChangeType) -> "DocVersion":
        """Return a new DocVersion incremented according to *change_type*.

        Rules
        -----
        MAJOR  → major+1, minor reset to 0, patch reset to 0
        MINOR  → minor+1, patch reset to 0
        PATCH  → patch+1
        NONE   → unchanged copy
        """
        if change_type is ChangeType.MAJOR:
            return DocVersion(self.major + 1, 0, 0)
        if change_type is ChangeType.MINOR:
            return DocVersion(self.major, self.minor + 1, 0)
        if change_type is ChangeType.PATCH:
            return DocVersion(self.major, self.minor, self.patch + 1)
        # NONE
        return DocVersion(self.major, self.minor, self.patch)

    def is_compatible_with(self, other: "DocVersion") -> bool:
        """Return True when *self* and *other* share the same major version."""
        return self.major == other.major

    # ------------------------------------------------------------------
    # Constructors
    # ------------------------------------------------------------------

    @classmethod
    def parse(cls, s: str) -> "DocVersion":
        """Parse a version string of the form ``"major.minor.patch"``."""
        parts = s.strip().split(".")
        if len(parts) != 3:
            raise ValueError(f"Invalid version string: {s!r}")
        try:
            major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError as exc:
            raise ValueError(f"Invalid version string: {s!r}") from exc
        return cls(major, minor, patch)

    @classmethod
    def initial(cls) -> "DocVersion":
        """Return the canonical initial version ``0.1.0``."""
        return cls(0, 1, 0)
