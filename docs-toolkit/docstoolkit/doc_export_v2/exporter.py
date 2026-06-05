"""E235 DocExportV2 — advanced exporter with plugins, templates, and streaming.

Stdlib only: ``json``, ``csv``, ``io``, ``re``.
"""
from __future__ import annotations

import csv
import io
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterator, Optional, Protocol


class ExportFormat(str, Enum):
    """Built-in export formats."""

    JSON = "json"
    JSONL = "jsonl"
    CSV = "csv"
    TSV = "tsv"
    XML = "xml"
    MARKDOWN = "markdown"
    YAML_LIKE = "yaml_like"
    HTML = "html"
    TEXT = "text"


@dataclass
class ExportConfig:
    """Configuration for an export operation."""

    format: ExportFormat = ExportFormat.JSON
    pretty: bool = False
    delimiter: str = ","
    encoding: str = "utf-8"
    template: Optional[str] = None
    fields: Optional[list] = None
    include_metadata: bool = True


@dataclass
class ExportResult:
    """Result of a single export() call."""

    content: str
    format: ExportFormat
    doc_count: int
    byte_size: int
    format_name: str


class FormatPlugin(Protocol):
    """Callable plugin: ``__call__(docs, config) -> str``."""

    def __call__(self, docs: list, config: ExportConfig) -> str:  # pragma: no cover
        ...


# ----------------------------- Helpers -----------------------------


_TEMPLATE_FIELD_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _stringify(value) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return ", ".join(_stringify(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _filter_doc(doc: dict, fields: Optional[list]) -> dict:
    if fields is None:
        return dict(doc)
    return {k: doc.get(k) for k in fields}


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _html_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _render_template(template: str, doc: dict) -> str:
    def replace(match: re.Match) -> str:
        field_name = match.group(1)
        return _stringify(doc.get(field_name, ""))

    return _TEMPLATE_FIELD_RE.sub(replace, template)


# ----------------------------- DocExportV2 -----------------------------


class DocExportV2:
    """Advanced document exporter with plugin and streaming support."""

    BUILTIN_FORMATS = {
        "json",
        "jsonl",
        "csv",
        "tsv",
        "xml",
        "markdown",
        "yaml_like",
        "html",
        "text",
    }

    DEFAULT_MARKDOWN_TEMPLATE = "# ${title}\n\n${content}\n\n---\n\n"

    def __init__(self) -> None:
        self._plugins: dict = {}

    # ------- Plugin management -------

    def register_plugin(self, format_name: str, plugin: Callable) -> bool:
        """Register a custom format plugin. Returns False if name is built-in or already taken."""
        if not isinstance(format_name, str) or not format_name:
            return False
        if format_name in self.BUILTIN_FORMATS:
            return False
        if format_name in self._plugins:
            return False
        if not callable(plugin):
            return False
        self._plugins[format_name] = plugin
        return True

    def unregister_plugin(self, format_name: str) -> bool:
        if format_name in self._plugins:
            del self._plugins[format_name]
            return True
        return False

    @property
    def plugin_count(self) -> int:
        return len(self._plugins)

    def available_formats(self) -> list:
        return sorted(self.BUILTIN_FORMATS) + sorted(self._plugins.keys())

    # ------- Format-specific exporters -------

    def export_to_json(self, docs: list, pretty: bool = False) -> str:
        if pretty:
            return json.dumps(docs, ensure_ascii=False, indent=2, sort_keys=False)
        return json.dumps(docs, ensure_ascii=False)

    def export_to_jsonl(self, docs: list) -> str:
        return "\n".join(json.dumps(d, ensure_ascii=False) for d in docs)

    def export_to_csv(
        self,
        docs: list,
        delimiter: str = ",",
        fields: Optional[list] = None,
    ) -> str:
        if not docs:
            return ""
        if fields is None:
            seen: list = []
            seen_set: set = set()
            for d in docs:
                for k in d.keys():
                    if k not in seen_set:
                        seen.append(k)
                        seen_set.add(k)
            fields = seen
        buf = io.StringIO()
        writer = csv.writer(buf, delimiter=delimiter, lineterminator="\n")
        writer.writerow(fields)
        for d in docs:
            writer.writerow([_stringify(d.get(f, "")) for f in fields])
        return buf.getvalue()

    def export_to_tsv(self, docs: list, fields: Optional[list] = None) -> str:
        return self.export_to_csv(docs, delimiter="\t", fields=fields)

    def export_to_xml(self, docs: list) -> str:
        lines = ['<?xml version="1.0" encoding="utf-8"?>', "<documents>"]
        for doc in docs:
            lines.append("  <document>")
            for k, v in doc.items():
                tag = _xml_escape(str(k))
                value = _xml_escape(_stringify(v))
                lines.append(f"    <{tag}>{value}</{tag}>")
            lines.append("  </document>")
        lines.append("</documents>")
        return "\n".join(lines)

    def export_to_markdown(self, docs: list, template: Optional[str] = None) -> str:
        tmpl = template if template is not None else self.DEFAULT_MARKDOWN_TEMPLATE
        return "".join(_render_template(tmpl, d) for d in docs)

    def export_to_yaml_like(self, docs: list) -> str:
        chunks: list = []
        for doc in docs:
            lines: list = []
            for k, v in doc.items():
                if isinstance(v, (list, tuple)):
                    lines.append(f"{k}:")
                    for item in v:
                        if isinstance(item, str):
                            lines.append(f'  - "{item}"')
                        else:
                            lines.append(f"  - {_stringify(item)}")
                elif isinstance(v, str):
                    escaped = v.replace('"', '\\"')
                    lines.append(f'{k}: "{escaped}"')
                elif v is None:
                    lines.append(f"{k}: null")
                elif isinstance(v, bool):
                    lines.append(f"{k}: {'true' if v else 'false'}")
                else:
                    lines.append(f"{k}: {_stringify(v)}")
            chunks.append("\n".join(lines))
        return "\n\n".join(chunks)

    def export_to_html(self, docs: list, template: Optional[str] = None) -> str:
        parts: list = ["<html><body>"]
        for doc in docs:
            if template is not None:
                parts.append(_render_template(template, doc))
            else:
                title = _html_escape(_stringify(doc.get("title", "")))
                content = _html_escape(_stringify(doc.get("content", "")))
                parts.append(f'<div class="doc"><h1>{title}</h1>{content}</div>')
        parts.append("</body></html>")
        return "".join(parts)

    def export_to_text(self, docs: list) -> str:
        chunks: list = []
        for doc in docs:
            lines: list = []
            for k, v in doc.items():
                lines.append(f"{k}: {_stringify(v)}")
            chunks.append("\n".join(lines))
        return "\n\n".join(chunks)

    def export_to_custom(
        self,
        docs: list,
        format_name: str,
        config: Optional[ExportConfig] = None,
    ) -> str:
        if format_name not in self._plugins:
            raise ValueError(f"Unknown plugin format: {format_name}")
        cfg = config if config is not None else ExportConfig()
        return self._plugins[format_name](docs, cfg)

    # ------- Dispatch -------

    def export(self, docs: list, config: ExportConfig) -> ExportResult:
        """Export with dispatch by config.format. Applies field filtering."""
        filtered = (
            [_filter_doc(d, config.fields) for d in docs]
            if config.fields is not None
            else docs
        )

        fmt = config.format
        if fmt == ExportFormat.JSON:
            content = self.export_to_json(filtered, pretty=config.pretty)
            name = "json"
        elif fmt == ExportFormat.JSONL:
            content = self.export_to_jsonl(filtered)
            name = "jsonl"
        elif fmt == ExportFormat.CSV:
            content = self.export_to_csv(
                filtered, delimiter=config.delimiter, fields=config.fields
            )
            name = "csv"
        elif fmt == ExportFormat.TSV:
            content = self.export_to_tsv(filtered, fields=config.fields)
            name = "tsv"
        elif fmt == ExportFormat.XML:
            content = self.export_to_xml(filtered)
            name = "xml"
        elif fmt == ExportFormat.MARKDOWN:
            content = self.export_to_markdown(filtered, template=config.template)
            name = "markdown"
        elif fmt == ExportFormat.YAML_LIKE:
            content = self.export_to_yaml_like(filtered)
            name = "yaml_like"
        elif fmt == ExportFormat.HTML:
            content = self.export_to_html(filtered, template=config.template)
            name = "html"
        elif fmt == ExportFormat.TEXT:
            content = self.export_to_text(filtered)
            name = "text"
        else:
            raise ValueError(f"Unsupported format: {fmt}")

        byte_size = len(content.encode(config.encoding, errors="replace"))
        return ExportResult(
            content=content,
            format=fmt,
            doc_count=len(filtered),
            byte_size=byte_size,
            format_name=name,
        )

    # ------- Streaming -------

    def export_stream(self, docs: list, config: ExportConfig) -> Iterator[str]:
        """Yield content in chunks. For JSON: ``[``, each doc separated, ``]``.
        For JSONL: one line per doc. Other formats: yield once.
        """
        filtered = (
            [_filter_doc(d, config.fields) for d in docs]
            if config.fields is not None
            else docs
        )

        fmt = config.format
        if fmt == ExportFormat.JSON:
            yield "["
            for i, doc in enumerate(filtered):
                if i > 0:
                    yield ","
                yield json.dumps(doc, ensure_ascii=False)
            yield "]"
        elif fmt == ExportFormat.JSONL:
            for i, doc in enumerate(filtered):
                if i > 0:
                    yield "\n"
                yield json.dumps(doc, ensure_ascii=False)
        else:
            result = self.export(docs, config)
            yield result.content
