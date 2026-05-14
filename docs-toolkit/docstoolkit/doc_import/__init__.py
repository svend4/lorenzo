"""E196 Document importer — imports documents from JSON, JSONL, CSV, TSV, XML, plain text, markdown.

Public API
----------
:class:`ImportFormat`  — enum of supported input formats (incl. AUTO)
:class:`ImportConfig`  — configuration for DocImporter
:class:`ImportStats`   — per-import statistics
:class:`ImportResult`  — result of a single import_string() call
:class:`ImportError`   — raised when import fails (strict mode)
:class:`DocImporter`   — main importer class
"""
from .importer import (
    DocImporter,
    ImportConfig,
    ImportError,
    ImportFormat,
    ImportResult,
    ImportStats,
)

__all__ = [
    "DocImporter",
    "ImportConfig",
    "ImportError",
    "ImportFormat",
    "ImportResult",
    "ImportStats",
]
