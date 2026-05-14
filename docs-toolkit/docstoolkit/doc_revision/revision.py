"""Revision (numbered version) manager with diff between revisions, blame info, and rollback."""

from __future__ import annotations

import difflib
import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Revision:
    revision_id: int
    doc_id: str
    content: str
    created_at: float
    author: Optional[str] = None
    message: Optional[str] = None
    parent_revision_id: Optional[int] = None


@dataclass
class BlameLine:
    line_num: int  # 1-based
    line: str
    revision_id: int
    author: Optional[str] = None
    timestamp: float = 0.0


@dataclass
class RevisionDiff:
    from_revision: int
    to_revision: int
    unified_diff: str
    lines_added: int
    lines_removed: int
    lines_changed: int


@dataclass
class RevisionStats:
    total_docs: int
    total_revisions: int
    revisions_per_doc: dict
    authors: set


class DocRevision:
    """Manages numbered revisions for documents with diff, blame, and rollback."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._revisions: dict[int, Revision] = {}
        self._doc_revisions: dict[str, list[int]] = {}
        self._next_id: int = 1

    def create_revision(
        self,
        doc_id: str,
        content: str,
        author: Optional[str] = None,
        message: Optional[str] = None,
        now: float = 0.0,
    ) -> Revision:
        with self._lock:
            rev_id = self._next_id
            self._next_id += 1
            parent_id = None
            if doc_id in self._doc_revisions and self._doc_revisions[doc_id]:
                parent_id = self._doc_revisions[doc_id][-1]
            rev = Revision(
                revision_id=rev_id,
                doc_id=doc_id,
                content=content,
                created_at=now,
                author=author,
                message=message,
                parent_revision_id=parent_id,
            )
            self._revisions[rev_id] = rev
            self._doc_revisions.setdefault(doc_id, []).append(rev_id)
            return rev

    def get_revision(self, revision_id: int) -> Optional[Revision]:
        with self._lock:
            return self._revisions.get(revision_id)

    def revisions_for_doc(self, doc_id: str, limit: Optional[int] = None) -> list[Revision]:
        with self._lock:
            ids = self._doc_revisions.get(doc_id, [])
            # newest first
            revs = [self._revisions[i] for i in reversed(ids)]
            if limit is not None:
                revs = revs[:limit]
            return revs

    def latest_revision(self, doc_id: str) -> Optional[Revision]:
        with self._lock:
            ids = self._doc_revisions.get(doc_id, [])
            if not ids:
                return None
            return self._revisions[ids[-1]]

    def revision_count(self, doc_id: str) -> int:
        with self._lock:
            return len(self._doc_revisions.get(doc_id, []))

    def _build_diff(self, rev_a: Revision, rev_b: Revision) -> RevisionDiff:
        lines_a = rev_a.content.splitlines(keepends=False)
        lines_b = rev_b.content.splitlines(keepends=False)
        ud = difflib.unified_diff(
            lines_a,
            lines_b,
            fromfile=f"revision_{rev_a.revision_id}",
            tofile=f"revision_{rev_b.revision_id}",
            lineterm="",
        )
        unified_diff = "\n".join(ud)

        # Use SequenceMatcher for accurate add/remove/change counts
        sm = difflib.SequenceMatcher(a=lines_a, b=lines_b)
        added = 0
        removed = 0
        changed = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "insert":
                added += j2 - j1
            elif tag == "delete":
                removed += i2 - i1
            elif tag == "replace":
                a_len = i2 - i1
                b_len = j2 - j1
                common = min(a_len, b_len)
                changed += common
                if b_len > a_len:
                    added += b_len - a_len
                elif a_len > b_len:
                    removed += a_len - b_len

        return RevisionDiff(
            from_revision=rev_a.revision_id,
            to_revision=rev_b.revision_id,
            unified_diff=unified_diff,
            lines_added=added,
            lines_removed=removed,
            lines_changed=changed,
        )

    def diff(self, rev_a: int, rev_b: int) -> Optional[RevisionDiff]:
        with self._lock:
            ra = self._revisions.get(rev_a)
            rb = self._revisions.get(rev_b)
            if ra is None or rb is None:
                return None
            return self._build_diff(ra, rb)

    def diff_to_latest(self, doc_id: str, rev: int) -> Optional[RevisionDiff]:
        with self._lock:
            ids = self._doc_revisions.get(doc_id, [])
            if not ids:
                return None
            ra = self._revisions.get(rev)
            if ra is None or ra.doc_id != doc_id:
                return None
            rb = self._revisions[ids[-1]]
            return self._build_diff(ra, rb)

    def blame(self, doc_id: str, revision_id: Optional[int] = None) -> list[BlameLine]:
        with self._lock:
            ids = self._doc_revisions.get(doc_id, [])
            if not ids:
                return []
            if revision_id is None:
                target_id = ids[-1]
            else:
                target = self._revisions.get(revision_id)
                if target is None or target.doc_id != doc_id:
                    return []
                target_id = revision_id

            # Build chronological list of revisions up to and including target_id
            chronological: list[Revision] = []
            for rid in ids:
                chronological.append(self._revisions[rid])
                if rid == target_id:
                    break

            target_rev = self._revisions[target_id]
            target_lines = target_rev.content.splitlines(keepends=False)

            # For each line at each index in target, find earliest revision
            # where line at that index equals the target line.
            blame_lines: list[BlameLine] = []
            for idx, line in enumerate(target_lines):
                introducing_rev: Optional[Revision] = None
                for rev in chronological:
                    rev_lines = rev.content.splitlines(keepends=False)
                    if idx < len(rev_lines) and rev_lines[idx] == line:
                        introducing_rev = rev
                        break
                if introducing_rev is None:
                    introducing_rev = target_rev
                blame_lines.append(
                    BlameLine(
                        line_num=idx + 1,
                        line=line,
                        revision_id=introducing_rev.revision_id,
                        author=introducing_rev.author,
                        timestamp=introducing_rev.created_at,
                    )
                )
            return blame_lines

    def rollback(
        self,
        doc_id: str,
        to_revision_id: int,
        author: Optional[str] = None,
        now: float = 0.0,
    ) -> Optional[Revision]:
        with self._lock:
            target = self._revisions.get(to_revision_id)
            if target is None or target.doc_id != doc_id:
                return None
            ids = self._doc_revisions.get(doc_id, [])
            if not ids:
                return None
            rev_id = self._next_id
            self._next_id += 1
            parent_id = ids[-1]
            new_rev = Revision(
                revision_id=rev_id,
                doc_id=doc_id,
                content=target.content,
                created_at=now,
                author=author,
                message=f"Rollback to revision {to_revision_id}",
                parent_revision_id=parent_id,
            )
            self._revisions[rev_id] = new_rev
            self._doc_revisions[doc_id].append(rev_id)
            return new_rev

    def restore_to(self, doc_id: str, to_revision_id: int) -> bool:
        with self._lock:
            target = self._revisions.get(to_revision_id)
            if target is None or target.doc_id != doc_id:
                return False
            ids = self._doc_revisions.get(doc_id, [])
            if to_revision_id not in ids:
                return False
            cutoff = ids.index(to_revision_id)
            to_drop = ids[cutoff + 1 :]
            for rid in to_drop:
                self._revisions.pop(rid, None)
            self._doc_revisions[doc_id] = ids[: cutoff + 1]
            return True

    def delete_revision(self, revision_id: int) -> bool:
        with self._lock:
            rev = self._revisions.pop(revision_id, None)
            if rev is None:
                return False
            ids = self._doc_revisions.get(rev.doc_id, [])
            if revision_id in ids:
                ids.remove(revision_id)
            if not ids:
                self._doc_revisions.pop(rev.doc_id, None)
            return True

    def delete_doc(self, doc_id: str) -> int:
        with self._lock:
            ids = self._doc_revisions.pop(doc_id, [])
            for rid in ids:
                self._revisions.pop(rid, None)
            return len(ids)

    def authors_for_doc(self, doc_id: str) -> set:
        with self._lock:
            ids = self._doc_revisions.get(doc_id, [])
            authors = set()
            for rid in ids:
                rev = self._revisions.get(rid)
                if rev and rev.author is not None:
                    authors.add(rev.author)
            return authors

    def revisions_by_author(self, author: str) -> list[Revision]:
        with self._lock:
            return [rev for rev in self._revisions.values() if rev.author == author]

    def stats(self) -> RevisionStats:
        with self._lock:
            revisions_per_doc = {
                doc_id: len(ids) for doc_id, ids in self._doc_revisions.items()
            }
            authors = {
                rev.author for rev in self._revisions.values() if rev.author is not None
            }
            return RevisionStats(
                total_docs=len(self._doc_revisions),
                total_revisions=len(self._revisions),
                revisions_per_doc=revisions_per_doc,
                authors=authors,
            )

    @property
    def total_revisions(self) -> int:
        with self._lock:
            return len(self._revisions)

    def clear(self) -> None:
        with self._lock:
            self._revisions.clear()
            self._doc_revisions.clear()
            self._next_id = 1


__all__ = [
    "Revision",
    "BlameLine",
    "RevisionDiff",
    "RevisionStats",
    "DocRevision",
]
