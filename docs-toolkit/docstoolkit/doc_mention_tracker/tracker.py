"""E292 DocMentionTracker — track @mentions and cross-references between documents.

Thread-safe, pure stdlib implementation.

Public API
----------
:class:`Mention`           — a single recorded mention with id, source, target, type,
                              context snippet, position, and timestamp
:class:`MentionStats`      — aggregate statistics for the mention store
:class:`DocMentionTracker` — main interface: add, extract, query, and delete mentions
"""

from __future__ import annotations

import re
import threading
import time
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Compiled patterns used by extract_and_add
# ---------------------------------------------------------------------------

USER_RE = re.compile(r'@(\w+)')
DOC_RE = re.compile(r'\[\[([^\]]+)\]\]')
TAG_RE = re.compile(r'#(\w+)')

_CONTEXT_RADIUS = 40  # chars on each side of a match


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class Mention:
    """A single recorded mention."""

    mention_id: int       # auto-increment, unique per tracker instance
    source_doc: str       # document that contains the mention
    target: str           # mentioned entity (@user word, [[doc]] title, or #tag word)
    mention_type: str     # "user", "doc", or "tag"
    context: str          # surrounding text snippet (up to 100 chars total)
    position: int         # character offset of the match start in source_doc content
    timestamp: float


@dataclass
class MentionStats:
    """Aggregate statistics for the entire mention store."""

    total_mentions: int
    unique_targets: int
    unique_sources: int
    type_counts: dict[str, int]  # mention_type -> count


# ---------------------------------------------------------------------------
# Tracker
# ---------------------------------------------------------------------------


class DocMentionTracker:
    """Tracks @mentions and cross-references between documents.

    Thread-safe via a single :class:`threading.Lock`.  All public methods
    acquire the lock for their entire duration.

    Mention IDs
    ~~~~~~~~~~~
    Each call to :meth:`add` (including those made internally by
    :meth:`extract_and_add`) assigns a monotonically increasing integer id
    starting from 1.

    Extraction patterns (used by :meth:`extract_and_add`)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    * ``@word``          → ``mention_type="user"``,  ``target=word``
    * ``[[word]]``       → ``mention_type="doc"``,   ``target=word``
    * ``[[multi word]]`` → ``mention_type="doc"``,   ``target=multi word``
    * ``#word``          → ``mention_type="tag"``,   ``target=word``

    Context snippet
    ~~~~~~~~~~~~~~~
    For each match the context is built as the 40 characters immediately
    before the match, the full match text, and the 40 characters immediately
    after.  Indices are clamped to the bounds of the content string so the
    result is always a valid substring.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._next_id: int = 1
        # mention_id -> Mention
        self._mentions: dict[int, Mention] = {}
        # source_doc -> list[mention_id]
        self._by_source: dict[str, list[int]] = {}
        # target -> list[mention_id]
        self._by_target: dict[str, list[int]] = {}

    # ------------------------------------------------------------------
    # Internal helpers (must be called with lock held)
    # ------------------------------------------------------------------

    def _store(self, mention: Mention) -> None:
        """Insert *mention* into all internal indexes."""
        self._mentions[mention.mention_id] = mention
        self._by_source.setdefault(mention.source_doc, []).append(mention.mention_id)
        self._by_target.setdefault(mention.target, []).append(mention.mention_id)

    def _build_context(self, content: str, start: int, end: int) -> str:
        """Return a context snippet of up to 100 chars around *content[start:end]*."""
        ctx_start = max(0, start - _CONTEXT_RADIUS)
        ctx_end = min(len(content), end + _CONTEXT_RADIUS)
        snippet = content[ctx_start:ctx_end]
        # Enforce the 100-char hard limit: keep as much suffix as possible.
        if len(snippet) > 100:
            snippet = snippet[:100]
        return snippet

    # ------------------------------------------------------------------
    # Core mutation
    # ------------------------------------------------------------------

    def add(
        self,
        source_doc: str,
        target: str,
        mention_type: str,
        context: str = "",
        position: int = 0,
        now: Optional[float] = None,
    ) -> Mention:
        """Record a single mention and return the resulting :class:`Mention`.

        Parameters
        ----------
        source_doc:
            The document that contains the mention.
        target:
            The mentioned entity (user name, doc title, or tag word).
        mention_type:
            One of ``"user"``, ``"doc"``, or ``"tag"`` (or any custom string).
        context:
            Optional surrounding text snippet (up to 100 chars recommended).
        position:
            Character offset of the mention within the source document.
        now:
            Optional timestamp override (defaults to ``time.time()``).
        """
        with self._lock:
            ts = now if now is not None else time.time()
            mention = Mention(
                mention_id=self._next_id,
                source_doc=source_doc,
                target=target,
                mention_type=mention_type,
                context=context,
                position=position,
                timestamp=ts,
            )
            self._next_id += 1
            self._store(mention)
            return mention

    def extract_and_add(
        self,
        source_doc: str,
        content: str,
        now: Optional[float] = None,
    ) -> list[Mention]:
        """Parse *content* and record every mention found.

        Scans for the three supported patterns in a single pass over the
        content and records one :class:`Mention` per match.  Returns the
        newly created mentions in the order they appear in *content*.

        Parameters
        ----------
        source_doc:
            Name / identifier of the document being parsed.
        content:
            Raw text to scan for mention patterns.
        now:
            Optional timestamp override applied to every mention created.
        """
        ts = now if now is not None else time.time()

        # Gather all matches with their type information before acquiring the
        # lock so regex work happens outside the critical section.
        raw: list[tuple[int, int, str, str]] = []  # (start, end, target, mtype)

        for m in USER_RE.finditer(content):
            raw.append((m.start(), m.end(), m.group(1), "user"))
        for m in DOC_RE.finditer(content):
            raw.append((m.start(), m.end(), m.group(1), "doc"))
        for m in TAG_RE.finditer(content):
            raw.append((m.start(), m.end(), m.group(1), "tag"))

        # Sort by start position so ids are assigned in document order.
        raw.sort(key=lambda x: x[0])

        added: list[Mention] = []
        with self._lock:
            for start, end, target, mtype in raw:
                context = self._build_context(content, start, end)
                mention = Mention(
                    mention_id=self._next_id,
                    source_doc=source_doc,
                    target=target,
                    mention_type=mtype,
                    context=context,
                    position=start,
                    timestamp=ts,
                )
                self._next_id += 1
                self._store(mention)
                added.append(mention)

        return added

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def mentions_of(
        self,
        target: str,
        mention_type: Optional[str] = None,
    ) -> list[Mention]:
        """Return mentions of *target*, optionally filtered by *mention_type*.

        Results are ordered newest-first (by timestamp, then by descending id
        for ties).
        """
        with self._lock:
            ids = self._by_target.get(target, [])
            result = [
                self._mentions[i]
                for i in ids
                if i in self._mentions
                and (mention_type is None or self._mentions[i].mention_type == mention_type)
            ]
        result.sort(key=lambda m: (m.timestamp, m.mention_id), reverse=True)
        return result

    def mentions_from(
        self,
        source_doc: str,
        mention_type: Optional[str] = None,
    ) -> list[Mention]:
        """Return mentions made by *source_doc*, optionally filtered by *mention_type*.

        Results are ordered newest-first.
        """
        with self._lock:
            ids = self._by_source.get(source_doc, [])
            result = [
                self._mentions[i]
                for i in ids
                if i in self._mentions
                and (mention_type is None or self._mentions[i].mention_type == mention_type)
            ]
        result.sort(key=lambda m: (m.timestamp, m.mention_id), reverse=True)
        return result

    def targets_mentioned_by(self, source_doc: str) -> list[str]:
        """Return sorted unique targets mentioned in *source_doc*."""
        with self._lock:
            ids = self._by_source.get(source_doc, [])
            targets = {
                self._mentions[i].target
                for i in ids
                if i in self._mentions
            }
        return sorted(targets)

    def sources_mentioning(self, target: str) -> list[str]:
        """Return sorted unique source docs that mention *target*."""
        with self._lock:
            ids = self._by_target.get(target, [])
            sources = {
                self._mentions[i].source_doc
                for i in ids
                if i in self._mentions
            }
        return sorted(sources)

    def top_mentioned(
        self,
        limit: int = 10,
        mention_type: Optional[str] = None,
    ) -> list[tuple[str, int]]:
        """Return ``[(target, count)]`` sorted by count descending.

        Parameters
        ----------
        limit:
            Maximum number of entries to return.
        mention_type:
            If given, only mentions of this type contribute to the counts.
        """
        with self._lock:
            counts: dict[str, int] = {}
            for mention in self._mentions.values():
                if mention_type is not None and mention.mention_type != mention_type:
                    continue
                counts[mention.target] = counts.get(mention.target, 0) + 1
        ranked = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
        return ranked[:limit]

    # ------------------------------------------------------------------
    # Deletion
    # ------------------------------------------------------------------

    def delete(self, mention_id: int) -> bool:
        """Delete mention by id.

        Returns
        -------
        bool
            ``True`` if the mention existed and was removed, ``False`` otherwise.
        """
        with self._lock:
            mention = self._mentions.pop(mention_id, None)
            if mention is None:
                return False
            src_list = self._by_source.get(mention.source_doc, [])
            if mention_id in src_list:
                src_list.remove(mention_id)
            tgt_list = self._by_target.get(mention.target, [])
            if mention_id in tgt_list:
                tgt_list.remove(mention_id)
            return True

    def clear_source(self, source_doc: str) -> int:
        """Delete all mentions from *source_doc*.

        Returns
        -------
        int
            The number of mentions removed.
        """
        with self._lock:
            ids = self._by_source.pop(source_doc, [])
            count = 0
            for mid in ids:
                mention = self._mentions.pop(mid, None)
                if mention is not None:
                    tgt_list = self._by_target.get(mention.target, [])
                    if mid in tgt_list:
                        tgt_list.remove(mid)
                    count += 1
            return count

    # ------------------------------------------------------------------
    # Aggregate statistics
    # ------------------------------------------------------------------

    def stats(self) -> MentionStats:
        """Return aggregate :class:`MentionStats` for the current state."""
        with self._lock:
            mentions = list(self._mentions.values())

        type_counts: dict[str, int] = {}
        targets: set[str] = set()
        sources: set[str] = set()
        for m in mentions:
            type_counts[m.mention_type] = type_counts.get(m.mention_type, 0) + 1
            targets.add(m.target)
            sources.add(m.source_doc)

        return MentionStats(
            total_mentions=len(mentions),
            unique_targets=len(targets),
            unique_sources=len(sources),
            type_counts=type_counts,
        )

    # ------------------------------------------------------------------
    # Property
    # ------------------------------------------------------------------

    @property
    def total_mentions(self) -> int:
        """Total number of mentions currently stored."""
        with self._lock:
            return len(self._mentions)
