"""E195 Document exporter — exports documents to JSON, JSONL, CSV, TSV, XML, plain text, markdown.

Public API
----------
:class:`ExportFormat`  — enum of supported output formats
:class:`ExportConfig`  — configuration for DocExporter
:class:`ExportResult`  — result of a single export() call
:class:`ExportError`   — raised when export fails
:class:`DocExporter`   — main exporter class
"""
from .exporter import (
    DocExporter,
    ExportConfig,
    ExportError,
    ExportFormat,
    ExportResult,
)

__all__ = [
    "DocExporter",
    "ExportConfig",
    "ExportError",
    "ExportFormat",
    "ExportResult",
]
