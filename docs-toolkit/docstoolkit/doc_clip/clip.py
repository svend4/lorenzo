"""Implementation of DocClip — extracting and managing text clips from docs."""

from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Clip:
    """A single text clip extracted from a document."""

    clip_id: str
    doc_id: str
    text: str
    start: int = 0
    end: int = 0
    created_at: float = 0.0
    note: Optional[str] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class ClipCollection:
    """A named collection grouping clip ids."""

    name: str
    clip_ids: List[str] = field(default_factory=list)
    created_at: float = 0.0


class DocClip:
    """Manages clips extracted from documents and their collections.

    Thread-safe: protected by an internal ``threading.Lock``.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._clips: Dict[str, Clip] = {}
        self._collections: Dict[str, ClipCollection] = {}

    # ----- creation -----------------------------------------------------
    def clip(
        self,
        doc_id: str,
        text: str,
        start: int = 0,
        end: int = 0,
        note: Optional[str] = None,
        tags: Optional[List[str]] = None,
        now: float = 0.0,
    ) -> Clip:
        """Create a clip from explicit text."""
        with self._lock:
            clip_id = uuid.uuid4().hex
            c = Clip(
                clip_id=clip_id,
                doc_id=doc_id,
                text=text,
                start=start,
                end=end,
                created_at=now,
                note=note,
                tags=list(tags) if tags else [],
            )
            self._clips[clip_id] = c
            return c

    def clip_from_doc(
        self,
        doc_id: str,
        source_text: str,
        start: int,
        end: int,
        note: Optional[str] = None,
        tags: Optional[List[str]] = None,
        now: float = 0.0,
    ) -> Optional[Clip]:
        """Create a clip by slicing ``source_text[start:end]``.

        Returns ``None`` when offsets are invalid.
        """
        if source_text is None:
            return None
        if start < 0 or end < 0:
            return None
        if end < start:
            return None
        if start > len(source_text) or end > len(source_text):
            return None
        text = source_text[start:end]
        return self.clip(
            doc_id=doc_id,
            text=text,
            start=start,
            end=end,
            note=note,
            tags=tags,
            now=now,
        )

    # ----- retrieval ----------------------------------------------------
    def get(self, clip_id: str) -> Optional[Clip]:
        with self._lock:
            return self._clips.get(clip_id)

    def update_note(self, clip_id: str, note: str) -> bool:
        with self._lock:
            c = self._clips.get(clip_id)
            if c is None:
                return False
            c.note = note
            return True

    def add_tag(self, clip_id: str, tag: str) -> bool:
        with self._lock:
            c = self._clips.get(clip_id)
            if c is None:
                return False
            if tag in c.tags:
                return False
            c.tags.append(tag)
            return True

    def remove_tag(self, clip_id: str, tag: str) -> bool:
        with self._lock:
            c = self._clips.get(clip_id)
            if c is None:
                return False
            if tag not in c.tags:
                return False
            c.tags.remove(tag)
            return True

    def delete(self, clip_id: str) -> bool:
        with self._lock:
            if clip_id not in self._clips:
                return False
            del self._clips[clip_id]
            # remove from all collections
            for coll in self._collections.values():
                if clip_id in coll.clip_ids:
                    coll.clip_ids.remove(clip_id)
            return True

    def clips_for_doc(self, doc_id: str) -> List[Clip]:
        with self._lock:
            return [c for c in self._clips.values() if c.doc_id == doc_id]

    def clips_with_tag(self, tag: str) -> List[Clip]:
        with self._lock:
            return [c for c in self._clips.values() if tag in c.tags]

    def search_clips(self, query: str, case_sensitive: bool = False) -> List[Clip]:
        """Substring search across ``text`` and ``note``."""
        with self._lock:
            if not query:
                return []
            if case_sensitive:
                needle = query
                results = []
                for c in self._clips.values():
                    if needle in c.text:
                        results.append(c)
                        continue
                    if c.note is not None and needle in c.note:
                        results.append(c)
                return results
            needle = query.lower()
            results = []
            for c in self._clips.values():
                if needle in c.text.lower():
                    results.append(c)
                    continue
                if c.note is not None and needle in c.note.lower():
                    results.append(c)
            return results

    # ----- collections --------------------------------------------------
    def create_collection(
        self,
        name: str,
        clip_ids: Optional[List[str]] = None,
        now: float = 0.0,
    ) -> ClipCollection:
        with self._lock:
            if name in self._collections:
                return self._collections[name]
            ids: List[str] = []
            if clip_ids:
                for cid in clip_ids:
                    if cid in self._clips and cid not in ids:
                        ids.append(cid)
            coll = ClipCollection(name=name, clip_ids=ids, created_at=now)
            self._collections[name] = coll
            return coll

    def add_to_collection(self, name: str, clip_id: str) -> bool:
        with self._lock:
            coll = self._collections.get(name)
            if coll is None:
                return False
            if clip_id not in self._clips:
                return False
            if clip_id in coll.clip_ids:
                return False
            coll.clip_ids.append(clip_id)
            return True

    def remove_from_collection(self, name: str, clip_id: str) -> bool:
        with self._lock:
            coll = self._collections.get(name)
            if coll is None:
                return False
            if clip_id not in coll.clip_ids:
                return False
            coll.clip_ids.remove(clip_id)
            return True

    def collections_for_clip(self, clip_id: str) -> List[ClipCollection]:
        with self._lock:
            return [c for c in self._collections.values() if clip_id in c.clip_ids]

    def get_collection(self, name: str) -> Optional[ClipCollection]:
        with self._lock:
            return self._collections.get(name)

    def delete_collection(self, name: str) -> bool:
        with self._lock:
            if name not in self._collections:
                return False
            del self._collections[name]
            return True

    def export_collection(self, name: str) -> str:
        """Concatenate clip texts in the collection separated by a divider."""
        with self._lock:
            coll = self._collections.get(name)
            if coll is None:
                return ""
            parts: List[str] = []
            for cid in coll.clip_ids:
                c = self._clips.get(cid)
                if c is not None:
                    parts.append(c.text)
            return "\n---\n".join(parts)

    # ----- properties ---------------------------------------------------
    @property
    def total_clips(self) -> int:
        with self._lock:
            return len(self._clips)

    @property
    def total_collections(self) -> int:
        with self._lock:
            return len(self._collections)

    def clear(self) -> None:
        with self._lock:
            self._clips.clear()
            self._collections.clear()
