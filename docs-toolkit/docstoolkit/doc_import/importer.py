"""DocImporter — import documents from various textual formats.

Stdlib-only implementation supporting JSON, JSONL, CSV, TSV, XML, plain text
and markdown. Returns ``list[dict]``. Counterpart to :mod:`doc_export`.
"""
from __future__ import annotations

import csv
import io
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class ImportFormat(Enum):
    """Supported import formats."""

    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    TSV = "tsv"
    XML = "xml"
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"
    AUTO = "auto"


class ImportError(Exception):
    """Raised when a document import fails (in strict mode)."""


@dataclass
class ImportConfig:
    """Configuration for :class:`DocImporter`."""

    format: ImportFormat = ImportFormat.AUTO
    delimiter: str = ","
    has_header: bool = True
    encoding: str = "utf-8"
    strict: bool = False


@dataclass
class ImportStats:
    """Per-import statistics."""

    docs_imported: int = 0
    docs_skipped: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        total = self.docs_imported + self.docs_skipped
        if total == 0:
            return 0.0
        return self.docs_imported / total


@dataclass
class ImportResult:
    """Result of an import operation."""

    docs: list[dict]
    stats: ImportStats
    format: ImportFormat


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def _xml_element_to_dict(elem: ET.Element) -> Any:
    """Convert an XML element to a Python value (dict / list / str)."""
    children = list(elem)
    if not children:
        return elem.text if elem.text is not None else ""

    # If every child has the same tag name "item", treat as list
    if all(c.tag == "item" for c in children):
        return [_xml_element_to_dict(c) for c in children]

    # Otherwise, collect children into a dict; repeated tags become lists.
    result: dict[str, Any] = {}
    for c in children:
        value = _xml_element_to_dict(c)
        if c.tag in result:
            existing = result[c.tag]
            if isinstance(existing, list):
                existing.append(value)
            else:
                result[c.tag] = [existing, value]
        else:
            result[c.tag] = value
    return result


# --------------------------------------------------------------------------- #
# DocImporter
# --------------------------------------------------------------------------- #
class DocImporter:
    """Import documents from various textual formats into ``list[dict]``."""

    def __init__(self, config: Optional[ImportConfig] = None) -> None:
        self.config = config or ImportConfig()

    # ------------------------------------------------------------------ #
    # Format detection
    # ------------------------------------------------------------------ #
    def detect_format(self, text: str) -> ImportFormat:
        """Heuristically detect the import format of ``text``."""
        if not isinstance(text, str) or not text.strip():
            return ImportFormat.PLAIN_TEXT

        stripped = text.lstrip()

        # XML
        if stripped.startswith("<?xml") or stripped.startswith("<"):
            return ImportFormat.XML

        # JSON vs JSONL
        if stripped.startswith("["):
            return ImportFormat.JSON
        if stripped.startswith("{"):
            # Multiple top-level objects on different lines → JSONL
            lines = [
                ln.strip()
                for ln in text.splitlines()
                if ln.strip()
            ]
            json_object_lines = sum(
                1 for ln in lines if ln.startswith("{") and ln.endswith("}")
            )
            if json_object_lines >= 2 and json_object_lines == len(lines):
                return ImportFormat.JSONL
            return ImportFormat.JSON

        # Markdown headings
        lines = text.splitlines()
        non_empty = [ln for ln in lines if ln.strip()]
        if any(ln.lstrip().startswith("#") for ln in non_empty):
            return ImportFormat.MARKDOWN

        # CSV: comma in first non-empty line and at least 2 non-empty lines
        if non_empty and "," in non_empty[0] and len(non_empty) >= 2:
            return ImportFormat.CSV

        return ImportFormat.PLAIN_TEXT

    # ------------------------------------------------------------------ #
    # Public entry points
    # ------------------------------------------------------------------ #
    def import_string(
        self,
        text: str,
        format: Optional[ImportFormat] = None,
    ) -> ImportResult:
        """Import ``text`` and return an :class:`ImportResult`."""
        if text is None:
            if self.config.strict:
                raise ImportError("text must not be None")
            return ImportResult(
                docs=[],
                stats=ImportStats(
                    docs_imported=0,
                    docs_skipped=0,
                    errors=["text is None"],
                ),
                format=format or self.config.format,
            )

        fmt = format if format is not None else self.config.format
        if fmt is None or fmt == ImportFormat.AUTO:
            fmt = self.detect_format(text)

        stats = ImportStats()
        docs: list[dict] = []

        try:
            if fmt == ImportFormat.JSON:
                docs = self.from_json(text)
            elif fmt == ImportFormat.JSONL:
                docs, jsonl_errors = self._from_jsonl_with_errors(text)
                stats.docs_skipped += len(jsonl_errors)
                stats.errors.extend(jsonl_errors)
                if jsonl_errors and self.config.strict:
                    raise ImportError(
                        f"JSONL parse errors: {jsonl_errors[0]}"
                    )
            elif fmt == ImportFormat.CSV:
                docs = self.from_csv(
                    text,
                    delimiter=self.config.delimiter,
                    has_header=self.config.has_header,
                )
            elif fmt == ImportFormat.TSV:
                docs = self.from_tsv(
                    text, has_header=self.config.has_header
                )
            elif fmt == ImportFormat.XML:
                docs = self.from_xml(text)
            elif fmt == ImportFormat.PLAIN_TEXT:
                docs = self.from_plain_text(text)
            elif fmt == ImportFormat.MARKDOWN:
                docs = self.from_markdown(text)
            else:
                raise ImportError(f"Unsupported format: {fmt!r}")
        except ImportError:
            raise
        except Exception as exc:  # pragma: no cover - defensive
            if self.config.strict:
                raise ImportError(str(exc)) from exc
            stats.errors.append(str(exc))
            docs = []

        stats.docs_imported = len(docs)
        return ImportResult(docs=docs, stats=stats, format=fmt)

    # ------------------------------------------------------------------ #
    # Per-format parsers
    # ------------------------------------------------------------------ #
    def from_json(self, text: str) -> list[dict]:
        """Parse JSON; accept array of objects or single object."""
        try:
            value = json.loads(text)
        except (TypeError, ValueError) as exc:
            if self.config.strict:
                raise ImportError(f"JSON parse failed: {exc}") from exc
            return []
        if value is None:
            return []
        if isinstance(value, list):
            return [v for v in value if isinstance(v, dict)]
        if isinstance(value, dict):
            return [value]
        if self.config.strict:
            raise ImportError(
                f"JSON root must be object or array, got {type(value).__name__}"
            )
        return []

    def _from_jsonl_with_errors(self, text: str) -> tuple[list[dict], list[str]]:
        docs: list[dict] = []
        errors: list[str] = []
        for i, line in enumerate(text.splitlines()):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                value = json.loads(stripped)
            except (TypeError, ValueError) as exc:
                errors.append(f"line {i + 1}: {exc}")
                continue
            if isinstance(value, dict):
                docs.append(value)
            else:
                errors.append(
                    f"line {i + 1}: expected object, got "
                    f"{type(value).__name__}"
                )
        return docs, errors

    def from_jsonl(self, text: str) -> list[dict]:
        """Parse JSONL — newline-delimited JSON objects."""
        docs, errors = self._from_jsonl_with_errors(text)
        if errors and self.config.strict:
            raise ImportError(f"JSONL parse failed: {errors[0]}")
        return docs

    def from_csv(
        self,
        text: str,
        delimiter: str = ",",
        has_header: bool = True,
    ) -> list[dict]:
        """Parse delimited text into a list of dicts."""
        if not text.strip():
            return []
        buf = io.StringIO(text)
        try:
            if has_header:
                reader = csv.DictReader(buf, delimiter=delimiter)
                return [dict(row) for row in reader]
            reader = csv.reader(buf, delimiter=delimiter)
            rows = list(reader)
            if not rows:
                return []
            ncols = max(len(r) for r in rows)
            cols = [f"col_{i}" for i in range(ncols)]
            return [
                {cols[i]: (row[i] if i < len(row) else "") for i in range(ncols)}
                for row in rows
            ]
        except csv.Error as exc:
            if self.config.strict:
                raise ImportError(f"CSV parse failed: {exc}") from exc
            return []

    def from_tsv(self, text: str, has_header: bool = True) -> list[dict]:
        """Parse tab-separated values."""
        return self.from_csv(text, delimiter="\t", has_header=has_header)

    def from_xml(self, text: str) -> list[dict]:
        """Parse XML; expects ``<document>`` children of root."""
        try:
            root = ET.fromstring(text)
        except ET.ParseError as exc:
            if self.config.strict:
                raise ImportError(f"XML parse failed: {exc}") from exc
            return []

        # Documents are children named "document" of root, OR root itself.
        candidates = [c for c in root if c.tag == "document"]
        if not candidates and root.tag == "document":
            candidates = [root]
        if not candidates:
            # Fallback: every direct child becomes a doc
            candidates = list(root)

        docs: list[dict] = []
        for elem in candidates:
            value = _xml_element_to_dict(elem)
            if isinstance(value, dict):
                docs.append(value)
            else:
                docs.append({"content": value})
        return docs

    def from_plain_text(self, text: str) -> list[dict]:
        """Each non-empty paragraph (separated by blank lines) → ``{"content": ...}``.

        Falls back to per-line splitting if the text contains no blank-line
        separators.
        """
        if not text or not text.strip():
            return []
        # Try paragraphs (blank-line separated) first
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        if len(paragraphs) >= 2:
            return [{"content": p} for p in paragraphs]
        # Otherwise split per line
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return [{"content": ln} for ln in lines]

    def from_markdown(self, text: str) -> list[dict]:
        """Parse markdown into a list of ``{"title": ..., "content": ...}`` docs.

        Splits on ``---`` separators or top-level ``#`` headings.
        """
        if not text or not text.strip():
            return []

        # Normalize: split on '---' (horizontal rule) first
        sections: list[str]
        if re.search(r"(?m)^---\s*$", text):
            sections = re.split(r"(?m)^---\s*$", text)
        else:
            # Split on top-level '# ' headings while keeping them in chunks
            parts = re.split(r"(?m)^(?=#\s+)", text)
            sections = parts

        docs: list[dict] = []
        for sec in sections:
            sec = sec.strip()
            if not sec:
                continue
            title = ""
            content_lines: list[str] = []
            lines = sec.splitlines()
            # First heading line becomes title, the rest is content
            first_heading_idx: Optional[int] = None
            for i, ln in enumerate(lines):
                m = re.match(r"^#+\s+(.*)$", ln)
                if m:
                    title = m.group(1).strip()
                    first_heading_idx = i
                    break
            if first_heading_idx is None:
                # No heading — whole section is content
                docs.append({"title": "", "content": sec})
                continue
            content_lines = lines[first_heading_idx + 1:]
            content = "\n".join(content_lines).strip()
            docs.append({"title": title, "content": content})
        return docs

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #
    def validate(
        self,
        doc: dict,
        required_fields: Optional[list[str]] = None,
    ) -> tuple[bool, list[str]]:
        """Validate ``doc`` against ``required_fields``.

        Returns ``(is_valid, errors)``.
        """
        errors: list[str] = []
        if not isinstance(doc, dict):
            return False, [f"not a dict: {type(doc).__name__}"]
        if required_fields:
            for field_name in required_fields:
                if field_name not in doc:
                    errors.append(f"missing required field: {field_name}")
                elif doc[field_name] in (None, ""):
                    errors.append(f"empty required field: {field_name}")
        return (len(errors) == 0), errors

    # ------------------------------------------------------------------ #
    # Batch
    # ------------------------------------------------------------------ #
    def import_batch(
        self,
        texts: list[str],
        format: Optional[ImportFormat] = None,
    ) -> list[ImportResult]:
        """Import several independent text blobs."""
        if not isinstance(texts, list):
            raise ImportError("texts must be a list of strings")
        return [self.import_string(t, format=format) for t in texts]
