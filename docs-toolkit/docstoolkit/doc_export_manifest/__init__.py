"""E368 DocExportManifest — manifest of exported document artifacts.

Public API
----------
:class:`ManifestEntry`      — a single artifact in the manifest
:class:`ExportManifest`     — full manifest for a single export run
:class:`ManifestStats`      — aggregate statistics
:class:`DocExportManifest`  — main interface for manifest management
"""

from .manifest import ManifestEntry, ExportManifest, ManifestStats, DocExportManifest

__all__ = ["ManifestEntry", "ExportManifest", "ManifestStats", "DocExportManifest"]
