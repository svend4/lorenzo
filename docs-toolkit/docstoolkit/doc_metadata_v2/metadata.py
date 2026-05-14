"""Doc metadata v2 — persistent metadata storage with extractor plugins.

Differs from doc_metadata (E139), which computes structural metadata.
v2 focuses on storing structured fields (frontmatter, inline tags, custom
extractors) per-document with confidence and source tracking.
"""
from __future__ import annotations

import re
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


@dataclass
class MetadataField:
    """A single metadata value with provenance information."""

    name: str
    value: Any
    source: str  # "frontmatter", "inline_tag", "extractor:<name>", "manual"
    confidence: float = 1.0


@dataclass
class ExtractorDef:
    """An extractor plugin definition."""

    name: str
    extract: Callable[[str], dict]
    enabled: bool = True
    priority: int = 0


@dataclass
class MetadataRecord:
    """Per-document metadata record."""

    doc_id: str
    fields: dict[str, MetadataField] = field(default_factory=dict)
    updated_at: float = 0.0


# Pre-compiled regex patterns
_FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*(\n|$)", re.DOTALL)
_INLINE_TAG_RE = re.compile(r"(?:^|\s)#([A-Za-z][A-Za-z0-9_\-]*)")


def _parse_scalar(raw: str) -> Any:
    """Parse a YAML-ish scalar value."""
    s = raw.strip()
    if not s:
        return ""
    # Strip surrounding quotes
    if (s.startswith('"') and s.endswith('"') and len(s) >= 2) or (
        s.startswith("'") and s.endswith("'") and len(s) >= 2
    ):
        return s[1:-1]
    low = s.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if low in ("null", "none", "~"):
        return None
    # Numeric?
    try:
        if "." in s:
            return float(s)
        return int(s)
    except ValueError:
        pass
    # List inline: [a, b, c]
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        if not inner:
            return []
        items = [p.strip() for p in inner.split(",")]
        return [_parse_scalar(it) for it in items if it != ""]
    return s


def _frontmatter_extractor(text: str) -> dict:
    """Built-in: extract --- ... --- block at start of doc."""
    if not text:
        return {}
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return {}
    block = m.group(1)
    out: dict[str, Any] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        if not key:
            continue
        out[key] = _parse_scalar(value)
    return out


def _inline_tags_extractor(text: str) -> dict:
    """Built-in: extract #tag-name occurrences."""
    if not text:
        return {}
    found: list[str] = []
    seen: set[str] = set()
    for m in _INLINE_TAG_RE.finditer(text):
        tag = m.group(1)
        if tag not in seen:
            seen.add(tag)
            found.append(tag)
    if not found:
        return {}
    return {"tags": found}


class DocMetadataV2:
    """Persistent metadata store with pluggable extractors."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._records: dict[str, MetadataRecord] = {}
        self._extractors: dict[str, ExtractorDef] = {}
        # Register built-in extractors
        self.register_extractor("frontmatter", _frontmatter_extractor, priority=100)
        self.register_extractor("inline_tags", _inline_tags_extractor, priority=50)

    # ---------- extraction ----------

    def extract(
        self, doc_id: str, content: str, now: float = 0.0
    ) -> MetadataRecord:
        """Run all enabled extractors against content for doc_id."""
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                record = MetadataRecord(doc_id=doc_id, fields={}, updated_at=now)
                self._records[doc_id] = record

            # Higher priority extractors run first; first-set field wins.
            extractors = sorted(
                self._extractors.values(),
                key=lambda e: (-e.priority, e.name),
            )
            for ext in extractors:
                if not ext.enabled:
                    continue
                try:
                    result = ext.extract(content) or {}
                except Exception:
                    continue
                if not isinstance(result, dict):
                    continue
                source = f"extractor:{ext.name}"
                for field_name, value in result.items():
                    if not isinstance(field_name, str):
                        continue
                    # First-wins: don't override existing fields.
                    if field_name in record.fields:
                        continue
                    record.fields[field_name] = MetadataField(
                        name=field_name,
                        value=value,
                        source=source,
                        confidence=1.0,
                    )
            record.updated_at = now
            return record

    # ---------- field operations ----------

    def set_field(
        self,
        doc_id: str,
        field_name: str,
        value: Any,
        source: str = "manual",
        confidence: float = 1.0,
        now: float = 0.0,
    ) -> MetadataField:
        """Set a field manually, overriding any existing value."""
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                record = MetadataRecord(doc_id=doc_id, fields={}, updated_at=now)
                self._records[doc_id] = record
            mf = MetadataField(
                name=field_name,
                value=value,
                source=source,
                confidence=confidence,
            )
            record.fields[field_name] = mf
            record.updated_at = now
            return mf

    def get_field(self, doc_id: str, field_name: str) -> Optional[MetadataField]:
        """Return the MetadataField for a doc/field combo, or None."""
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return None
            return record.fields.get(field_name)

    def get_value(self, doc_id: str, field_name: str, default: Any = None) -> Any:
        """Return the value for a doc/field combo, or default if missing."""
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return default
            mf = record.fields.get(field_name)
            if mf is None:
                return default
            return mf.value

    def remove_field(self, doc_id: str, field_name: str) -> bool:
        """Remove a single field; return True if removed."""
        with self._lock:
            record = self._records.get(doc_id)
            if record is None:
                return False
            if field_name not in record.fields:
                return False
            del record.fields[field_name]
            return True

    # ---------- records ----------

    def record_for(self, doc_id: str) -> Optional[MetadataRecord]:
        """Return the metadata record for a doc, or None."""
        with self._lock:
            return self._records.get(doc_id)

    def all_records(self) -> list[MetadataRecord]:
        """Return all metadata records."""
        with self._lock:
            return list(self._records.values())

    # ---------- extractor management ----------

    def register_extractor(
        self,
        name: str,
        extract_func: Callable[[str], dict],
        priority: int = 0,
    ) -> ExtractorDef:
        """Register an extractor (or replace existing with same name)."""
        ext = ExtractorDef(
            name=name,
            extract=extract_func,
            enabled=True,
            priority=priority,
        )
        with self._lock:
            self._extractors[name] = ext
            return ext

    def unregister_extractor(self, name: str) -> bool:
        """Remove an extractor by name. Returns True if removed."""
        with self._lock:
            if name not in self._extractors:
                return False
            del self._extractors[name]
            return True

    def enable_extractor(self, name: str) -> bool:
        """Enable a registered extractor."""
        with self._lock:
            ext = self._extractors.get(name)
            if ext is None:
                return False
            ext.enabled = True
            return True

    def disable_extractor(self, name: str) -> bool:
        """Disable a registered extractor (kept registered)."""
        with self._lock:
            ext = self._extractors.get(name)
            if ext is None:
                return False
            ext.enabled = False
            return True

    def list_extractors(self) -> list[ExtractorDef]:
        """Return all registered extractors, highest priority first."""
        with self._lock:
            return sorted(
                self._extractors.values(),
                key=lambda e: (-e.priority, e.name),
            )

    # ---------- direct extraction helpers ----------

    def extract_frontmatter(self, content: str) -> dict:
        """Extract YAML-ish frontmatter block from content."""
        return _frontmatter_extractor(content)

    def extract_inline_tags(self, content: str) -> dict:
        """Extract #inline-tag occurrences from content."""
        return _inline_tags_extractor(content)

    # ---------- doc lifecycle ----------

    def delete_doc(self, doc_id: str) -> bool:
        """Delete all metadata for a doc; True if existed."""
        with self._lock:
            if doc_id not in self._records:
                return False
            del self._records[doc_id]
            return True

    def docs_with_field(
        self, field_name: str, value: Any = None
    ) -> list[str]:
        """Return doc_ids that have field_name (optionally matching value)."""
        with self._lock:
            out: list[str] = []
            for doc_id, record in self._records.items():
                mf = record.fields.get(field_name)
                if mf is None:
                    continue
                if value is None or mf.value == value:
                    out.append(doc_id)
            return out

    # ---------- aggregates ----------

    @property
    def total_docs(self) -> int:
        """Number of documents tracked."""
        with self._lock:
            return len(self._records)

    def total_fields(self) -> int:
        """Total number of fields across all docs."""
        with self._lock:
            return sum(len(r.fields) for r in self._records.values())

    def unique_field_names(self) -> set[str]:
        """Set of distinct field names across all docs."""
        with self._lock:
            out: set[str] = set()
            for r in self._records.values():
                out.update(r.fields.keys())
            return out

    def clear(self) -> None:
        """Remove all records (but keep extractors registered)."""
        with self._lock:
            self._records.clear()
