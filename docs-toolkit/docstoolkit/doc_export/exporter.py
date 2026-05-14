"""DocExporter — export documents to various textual formats.

Stdlib-only implementation supporting JSON, JSONL, CSV, TSV, XML, plain text
and markdown. Documents are passed in as ``list[dict]``; no specific schema is
required, but ``title`` and ``content`` keys are honoured by the markdown and
plain-text exporters when present.
"""
from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable, Optional
from xml.sax.saxutils import escape as xml_escape


class ExportFormat(Enum):
    """Supported export formats."""

    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    TSV = "tsv"
    XML = "xml"
    PLAIN_TEXT = "plain_text"
    MARKDOWN = "markdown"


class ExportError(Exception):
    """Raised when a document export fails."""


@dataclass
class ExportConfig:
    """Configuration for :class:`DocExporter`."""

    format: ExportFormat = ExportFormat.JSON
    include_metadata: bool = True
    pretty: bool = False
    delimiter: str = ","
    encoding: str = "utf-8"


@dataclass
class ExportResult:
    """Result of an export operation."""

    format: ExportFormat
    content: str
    doc_count: int
    byte_size: int


def _ensure_docs(docs: Any) -> list[dict]:
    if docs is None:
        raise ExportError("docs must not be None")
    if not isinstance(docs, list):
        raise ExportError("docs must be a list of dicts")
    for i, d in enumerate(docs):
        if not isinstance(d, dict):
            raise ExportError(f"docs[{i}] is not a dict")
    return docs


def _all_keys(docs: list[dict]) -> list[str]:
    """Return union of keys preserving first-seen order across docs."""
    seen: dict[str, None] = {}
    for d in docs:
        for k in d.keys():
            if k not in seen:
                seen[k] = None
    return list(seen.keys())


def _stringify_cell(value: Any) -> str:
    """Convert a value to a string suitable for CSV/TSV/plain-text output."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, dict, tuple)):
        try:
            return json.dumps(value, ensure_ascii=False)
        except (TypeError, ValueError):
            return str(value)
    return str(value)


def _xml_render_value(key: str, value: Any) -> str:
    """Render a single value as XML element(s). Lists become repeated tags."""
    if value is None:
        return f"<{key}></{key}>"
    if isinstance(value, dict):
        inner = "".join(_xml_render_value(k, v) for k, v in value.items())
        return f"<{key}>{inner}</{key}>"
    if isinstance(value, list):
        # Render each item as a child element. Use singular-ish "item" tag.
        items = "".join(_xml_render_value("item", v) for v in value)
        return f"<{key}>{items}</{key}>"
    text = xml_escape(str(value))
    return f"<{key}>{text}</{key}>"


class DocExporter:
    """Export a list of dict-documents to a variety of textual formats."""

    def __init__(self, config: Optional[ExportConfig] = None) -> None:
        self.config = config or ExportConfig()

    # ------------------------------------------------------------------ #
    # Discovery
    # ------------------------------------------------------------------ #
    def available_formats(self) -> list[ExportFormat]:
        """Return the list of supported :class:`ExportFormat` values."""
        return list(ExportFormat)

    # ------------------------------------------------------------------ #
    # Main entry points
    # ------------------------------------------------------------------ #
    def export(
        self,
        docs: list[dict],
        config: Optional[ExportConfig] = None,
    ) -> ExportResult:
        """Export ``docs`` and return a populated :class:`ExportResult`."""
        cfg = config or self.config
        docs = _ensure_docs(docs)

        content = self._dispatch(docs, cfg)
        byte_size = len(content.encode(cfg.encoding))
        return ExportResult(
            format=cfg.format,
            content=content,
            doc_count=len(docs),
            byte_size=byte_size,
        )

    def export_to_string(
        self,
        docs: list[dict],
        format: Optional[ExportFormat] = None,
    ) -> str:
        """Export ``docs`` and return the raw string body."""
        cfg = self.config
        if format is not None:
            cfg = ExportConfig(
                format=format,
                include_metadata=cfg.include_metadata,
                pretty=cfg.pretty,
                delimiter=cfg.delimiter,
                encoding=cfg.encoding,
            )
        docs = _ensure_docs(docs)
        return self._dispatch(docs, cfg)

    def _dispatch(self, docs: list[dict], cfg: ExportConfig) -> str:
        fmt = cfg.format
        if fmt == ExportFormat.JSON:
            return self.export_to_json(docs, pretty=cfg.pretty)
        if fmt == ExportFormat.JSONL:
            return self.export_to_jsonl(docs)
        if fmt == ExportFormat.CSV:
            return self.export_to_csv(docs, delimiter=cfg.delimiter)
        if fmt == ExportFormat.TSV:
            return self.export_to_tsv(docs)
        if fmt == ExportFormat.XML:
            return self.export_to_xml(docs)
        if fmt == ExportFormat.PLAIN_TEXT:
            return self.export_to_plain_text(docs)
        if fmt == ExportFormat.MARKDOWN:
            return self.export_to_markdown(docs)
        raise ExportError(f"Unsupported format: {fmt!r}")

    # ------------------------------------------------------------------ #
    # Per-format implementations
    # ------------------------------------------------------------------ #
    def export_to_json(self, docs: list[dict], pretty: bool = False) -> str:
        docs = _ensure_docs(docs)
        try:
            if pretty:
                return json.dumps(docs, ensure_ascii=False, indent=2)
            return json.dumps(docs, ensure_ascii=False)
        except (TypeError, ValueError) as exc:
            raise ExportError(f"JSON serialization failed: {exc}") from exc

    def export_to_jsonl(self, docs: list[dict]) -> str:
        docs = _ensure_docs(docs)
        try:
            return "\n".join(json.dumps(d, ensure_ascii=False) for d in docs)
        except (TypeError, ValueError) as exc:
            raise ExportError(f"JSONL serialization failed: {exc}") from exc

    def export_to_csv(self, docs: list[dict], delimiter: str = ",") -> str:
        docs = _ensure_docs(docs)
        if not docs:
            return ""
        columns = _all_keys(docs)
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=delimiter, lineterminator="\n")
        writer.writerow(columns)
        for d in docs:
            writer.writerow([_stringify_cell(d.get(col)) for col in columns])
        return buf.getvalue()

    def export_to_tsv(self, docs: list[dict]) -> str:
        return self.export_to_csv(docs, delimiter="\t")

    def export_to_xml(self, docs: list[dict]) -> str:
        docs = _ensure_docs(docs)
        parts: list[str] = ['<?xml version="1.0" encoding="UTF-8"?>', "<documents>"]
        for d in docs:
            inner = "".join(_xml_render_value(k, v) for k, v in d.items())
            parts.append(f"<document>{inner}</document>")
        parts.append("</documents>")
        return "".join(parts)

    def export_to_plain_text(self, docs: list[dict]) -> str:
        docs = _ensure_docs(docs)
        lines: list[str] = []
        for d in docs:
            if "content" in d and d["content"] is not None:
                text = _stringify_cell(d["content"])
            else:
                # one-line summary: "key: value | key: value"
                text = " | ".join(
                    f"{k}: {_stringify_cell(v)}" for k, v in d.items()
                )
            lines.append(text)
        return "\n\n".join(lines)

    def export_to_markdown(self, docs: list[dict]) -> str:
        docs = _ensure_docs(docs)
        chunks: list[str] = []
        for d in docs:
            title = d.get("title", "Untitled")
            content = d.get("content", "")
            chunks.append(
                f"# {_stringify_cell(title)}\n\n"
                f"{_stringify_cell(content)}\n\n"
                "---\n"
            )
        return "\n".join(chunks)

    # ------------------------------------------------------------------ #
    # Batch
    # ------------------------------------------------------------------ #
    def export_batch(
        self,
        docs_list: list[list[dict]],
        format: ExportFormat,
    ) -> list[ExportResult]:
        """Export several independent document batches."""
        if not isinstance(docs_list, list):
            raise ExportError("docs_list must be a list of lists of dicts")
        results: list[ExportResult] = []
        for i, batch in enumerate(docs_list):
            if not isinstance(batch, list):
                raise ExportError(f"docs_list[{i}] is not a list")
            cfg = ExportConfig(
                format=format,
                include_metadata=self.config.include_metadata,
                pretty=self.config.pretty,
                delimiter=self.config.delimiter,
                encoding=self.config.encoding,
            )
            results.append(self.export(batch, cfg))
        return results
