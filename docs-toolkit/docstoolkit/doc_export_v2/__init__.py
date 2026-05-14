"""E235 Document exporter v2 — advanced export with custom formats, templates, batch processing, and streaming.

Public API
----------
:class:`ExportFormat`  — enum of supported output formats
:class:`ExportConfig`  — configuration for DocExportV2
:class:`ExportResult`  — result of a single export() call
:class:`DocExportV2`   — main exporter class with plugin support and streaming
"""
from .exporter import (
    DocExportV2,
    ExportConfig,
    ExportFormat,
    ExportResult,
    FormatPlugin,
)

__all__ = [
    "DocExportV2",
    "ExportConfig",
    "ExportFormat",
    "ExportResult",
    "FormatPlugin",
]
