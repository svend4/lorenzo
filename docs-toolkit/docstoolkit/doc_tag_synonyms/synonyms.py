"""DocTagSynonyms — tag synonym groups for normalized search.

Maintains groups of synonymous tags where every group has a canonical
representative and any number of synonyms.  Useful for query expansion
and tag normalization.

Stdlib only.  Thread-safe via :class:`threading.Lock`.
"""
from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SynonymGroup:
    """A group of synonymous tags.

    Attributes
    ----------
    group_id:
        Unique identifier (UUID) for the group.
    canonical:
        The canonical name for this group.
    synonyms:
        Additional tags that are synonymous with ``canonical``.
    created_at:
        Wall-clock creation time, seconds since epoch.
    """

    group_id: str
    canonical: str
    synonyms: list[str] = field(default_factory=list)
    created_at: float = 0.0


@dataclass
class SynonymStats:
    """Aggregate statistics for a :class:`DocTagSynonyms` instance.

    Attributes
    ----------
    total_groups:
        Number of synonym groups.
    total_synonyms:
        Total number of synonym entries across all groups (excluding
        canonicals).
    unique_canonicals:
        Number of distinct canonical tags (equal to ``total_groups``
        when every canonical is unique).
    """

    total_groups: int
    total_synonyms: int
    unique_canonicals: int


class DocTagSynonyms:
    """Manage groups of synonymous tags.

    A tag — whether the canonical or a synonym — may belong to at most
    one group.  Attempting to add a tag that already exists in another
    group raises :class:`ValueError`.
    """

    def __init__(self) -> None:
        self._groups: dict[str, SynonymGroup] = {}
        self._tag_to_group: dict[str, str] = {}
        self._lock = threading.Lock()

    # ------------------------------------------------------------------
    # Group management
    # ------------------------------------------------------------------
    def create_group(
        self,
        canonical: str,
        synonyms: Optional[list[str]] = None,
        now: Optional[float] = None,
    ) -> SynonymGroup:
        """Create a new synonym group.

        Parameters
        ----------
        canonical:
            Canonical tag for the group.  Must not be already mapped to
            any other group.
        synonyms:
            Optional list of synonyms to register together with the
            canonical.  Each synonym must also be free of any prior
            mapping; duplicates within ``synonyms`` are silently
            collapsed.
        now:
            Optional override for ``created_at`` (useful for tests).

        Raises
        ------
        ValueError
            If ``canonical`` or any of ``synonyms`` is already mapped to
            an existing group.
        """
        if not canonical:
            raise ValueError("canonical must be a non-empty string")
        syns = list(synonyms) if synonyms else []
        with self._lock:
            if canonical in self._tag_to_group:
                raise ValueError(f"tag {canonical!r} already mapped to a group")
            seen: set[str] = set()
            cleaned: list[str] = []
            for s in syns:
                if not s or s == canonical or s in seen:
                    continue
                if s in self._tag_to_group:
                    raise ValueError(f"tag {s!r} already mapped to a group")
                seen.add(s)
                cleaned.append(s)
            ts = float(now) if now is not None else time.time()
            gid = uuid.uuid4().hex
            group = SynonymGroup(
                group_id=gid,
                canonical=canonical,
                synonyms=cleaned,
                created_at=ts,
            )
            self._groups[gid] = group
            self._tag_to_group[canonical] = gid
            for s in cleaned:
                self._tag_to_group[s] = gid
            return group

    def delete_group(self, group_id: str) -> bool:
        """Delete a group by id.  Returns ``True`` if it existed."""
        with self._lock:
            group = self._groups.pop(group_id, None)
            if group is None:
                return False
            self._tag_to_group.pop(group.canonical, None)
            for s in group.synonyms:
                self._tag_to_group.pop(s, None)
            return True

    # ------------------------------------------------------------------
    # Synonym management
    # ------------------------------------------------------------------
    def add_synonym(self, group_id: str, synonym: str) -> bool:
        """Add ``synonym`` to the group identified by ``group_id``.

        Returns
        -------
        bool
            ``True`` if the synonym was newly added; ``False`` if it
            already existed in the same group.

        Raises
        ------
        ValueError
            If the synonym is already mapped to a different group.
        KeyError
            If ``group_id`` is unknown.
        """
        if not synonym:
            raise ValueError("synonym must be a non-empty string")
        with self._lock:
            group = self._groups.get(group_id)
            if group is None:
                raise KeyError(group_id)
            if synonym == group.canonical or synonym in group.synonyms:
                return False
            existing = self._tag_to_group.get(synonym)
            if existing is not None and existing != group_id:
                raise ValueError(
                    f"tag {synonym!r} already mapped to group {existing!r}"
                )
            group.synonyms.append(synonym)
            self._tag_to_group[synonym] = group_id
            return True

    def remove_synonym(self, group_id: str, synonym: str) -> bool:
        """Remove ``synonym`` from a group.

        Returns ``True`` if it was present and removed; ``False`` if the
        synonym was not in the group.  The canonical itself cannot be
        removed via this method.
        """
        with self._lock:
            group = self._groups.get(group_id)
            if group is None:
                return False
            if synonym == group.canonical:
                return False
            if synonym not in group.synonyms:
                return False
            group.synonyms.remove(synonym)
            self._tag_to_group.pop(synonym, None)
            return True

    def move_synonym(self, synonym: str, new_group_id: str) -> bool:
        """Move ``synonym`` from its current group to ``new_group_id``.

        Returns ``True`` if the move took place; ``False`` if the
        synonym is unknown, already in ``new_group_id``, or the
        destination group does not exist.  Canonicals cannot be moved.
        """
        with self._lock:
            target = self._groups.get(new_group_id)
            if target is None:
                return False
            current_id = self._tag_to_group.get(synonym)
            if current_id is None:
                return False
            current = self._groups.get(current_id)
            if current is None:
                return False
            if synonym == current.canonical:
                return False
            if current_id == new_group_id:
                return False
            current.synonyms.remove(synonym)
            target.synonyms.append(synonym)
            self._tag_to_group[synonym] = new_group_id
            return True

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------
    def get_group(self, group_id: str) -> Optional[SynonymGroup]:
        """Return the group with the given id, or ``None``."""
        with self._lock:
            return self._groups.get(group_id)

    def find_group(self, tag: str) -> Optional[SynonymGroup]:
        """Find the group containing ``tag`` (canonical or synonym)."""
        with self._lock:
            gid = self._tag_to_group.get(tag)
            if gid is None:
                return None
            return self._groups.get(gid)

    def canonical_of(self, tag: str) -> Optional[str]:
        """Return the canonical for ``tag``, or ``None`` if unknown."""
        with self._lock:
            gid = self._tag_to_group.get(tag)
            if gid is None:
                return None
            group = self._groups.get(gid)
            return group.canonical if group else None

    def synonyms_of(self, tag: str) -> list[str]:
        """Return the sorted list of synonyms in ``tag``'s group.

        The result excludes ``tag`` itself; if ``tag`` is unknown an
        empty list is returned.
        """
        with self._lock:
            gid = self._tag_to_group.get(tag)
            if gid is None:
                return []
            group = self._groups.get(gid)
            if group is None:
                return []
            members = [group.canonical, *group.synonyms]
            return sorted(m for m in members if m != tag)

    def is_synonym(self, tag1: str, tag2: str) -> bool:
        """Return ``True`` when both tags belong to the same group."""
        with self._lock:
            g1 = self._tag_to_group.get(tag1)
            g2 = self._tag_to_group.get(tag2)
            return g1 is not None and g1 == g2

    def expand(self, tag: str) -> list[str]:
        """Return the canonical plus all synonyms for ``tag`` (sorted).

        If ``tag`` is not part of any group, ``[tag]`` is returned.
        """
        with self._lock:
            gid = self._tag_to_group.get(tag)
            if gid is None:
                return [tag]
            group = self._groups.get(gid)
            if group is None:
                return [tag]
            return sorted({group.canonical, *group.synonyms})

    def expand_query(self, tags: list[str]) -> list[str]:
        """Expand every tag in ``tags`` and return the sorted unique union."""
        out: set[str] = set()
        with self._lock:
            for tag in tags:
                gid = self._tag_to_group.get(tag)
                if gid is None:
                    out.add(tag)
                    continue
                group = self._groups.get(gid)
                if group is None:
                    out.add(tag)
                    continue
                out.add(group.canonical)
                out.update(group.synonyms)
        return sorted(out)

    # ------------------------------------------------------------------
    # Listings & maintenance
    # ------------------------------------------------------------------
    def list_groups(self) -> list[SynonymGroup]:
        """Return every group, sorted by canonical name."""
        with self._lock:
            return sorted(self._groups.values(), key=lambda g: g.canonical)

    def all_tags(self) -> list[str]:
        """Return the sorted union of every canonical and synonym."""
        with self._lock:
            return sorted(self._tag_to_group.keys())

    def clear(self) -> int:
        """Remove every group; return the number of groups removed."""
        with self._lock:
            n = len(self._groups)
            self._groups.clear()
            self._tag_to_group.clear()
            return n

    def stats(self) -> SynonymStats:
        """Return aggregate :class:`SynonymStats`."""
        with self._lock:
            total_groups = len(self._groups)
            total_synonyms = sum(len(g.synonyms) for g in self._groups.values())
            unique_canonicals = len({g.canonical for g in self._groups.values()})
            return SynonymStats(
                total_groups=total_groups,
                total_synonyms=total_synonyms,
                unique_canonicals=unique_canonicals,
            )
