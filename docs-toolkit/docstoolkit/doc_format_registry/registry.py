"""E314 DocFormatRegistry — core registry implementation."""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class FormatSpec:
    """A registered document format."""

    format_id: str
    mime_type: str
    extensions: list[str] = field(default_factory=list)
    max_size_bytes: Optional[int] = None
    description: str = ""
    schema: dict = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Result of validating a document against a format."""

    valid: bool
    format_id: str
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class FormatStats:
    """Aggregate statistics over all registered formats."""

    total_formats: int
    total_mime_types: int
    total_extensions: int


class DocFormatRegistry:
    """Thread-safe registry for document formats and MIME types."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._formats: dict[str, FormatSpec] = {}
        self._ext_index: dict[str, str] = {}
        self._mime_index: dict[str, str] = {}

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register(self, spec: FormatSpec) -> None:
        """Register or replace a format; update extension and MIME indexes."""
        with self._lock:
            # Remove old index entries if replacing an existing format
            old = self._formats.get(spec.format_id)
            if old is not None:
                for ext in old.extensions:
                    if self._ext_index.get(ext) == spec.format_id:
                        del self._ext_index[ext]
                if self._mime_index.get(old.mime_type) == spec.format_id:
                    del self._mime_index[old.mime_type]

            self._formats[spec.format_id] = spec

            for ext in spec.extensions:
                self._ext_index[ext] = spec.format_id

            self._mime_index[spec.mime_type] = spec.format_id

    def unregister(self, format_id: str) -> bool:
        """Remove a format from all indexes. Returns True if it existed."""
        with self._lock:
            spec = self._formats.pop(format_id, None)
            if spec is None:
                return False

            for ext in spec.extensions:
                if self._ext_index.get(ext) == format_id:
                    del self._ext_index[ext]

            if self._mime_index.get(spec.mime_type) == format_id:
                del self._mime_index[spec.mime_type]

            return True

    # ------------------------------------------------------------------
    # Lookups
    # ------------------------------------------------------------------

    def get_format(self, format_id: str) -> Optional[FormatSpec]:
        """Return the FormatSpec for *format_id*, or None."""
        with self._lock:
            return self._formats.get(format_id)

    def by_extension(self, ext: str) -> Optional[FormatSpec]:
        """Lookup a format by file extension (e.g. '.md')."""
        with self._lock:
            fid = self._ext_index.get(ext)
            if fid is None:
                return None
            return self._formats.get(fid)

    def by_mime_type(self, mime_type: str) -> Optional[FormatSpec]:
        """Lookup a format by MIME type."""
        with self._lock:
            fid = self._mime_index.get(mime_type)
            if fid is None:
                return None
            return self._formats.get(fid)

    def list_formats(self) -> list[FormatSpec]:
        """Return all registered formats sorted by format_id."""
        with self._lock:
            return [self._formats[k] for k in sorted(self._formats)]

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(
        self,
        format_id: str,
        content: str,
        size_bytes: Optional[int] = None,
    ) -> ValidationResult:
        """Validate *content* against the registered format *format_id*.

        Checks performed (in order):
        1. Format existence.
        2. Size limit (if both *size_bytes* and ``max_size_bytes`` are set).
        3. Required fields — each entry in ``schema["required_fields"]`` must
           appear as the start of some line in *content*.
        4. Forbidden patterns — each entry in ``schema["forbidden_patterns"]``
           must not appear as a substring of *content* (adds warnings, not errors).
        """
        with self._lock:
            spec = self._formats.get(format_id)

        if spec is None:
            return ValidationResult(
                valid=False,
                format_id=format_id,
                errors=["Unknown format"],
            )

        errors: list[str] = []
        warnings: list[str] = []

        # Size check
        if size_bytes is not None and spec.max_size_bytes is not None:
            if size_bytes > spec.max_size_bytes:
                errors.append("Exceeds max size")

        # Required fields
        required_fields: list[str] = spec.schema.get("required_fields", [])
        if required_fields:
            lines = content.splitlines()
            for req in required_fields:
                if not any(line.startswith(req) for line in lines):
                    errors.append(f"Missing required field: {req}")

        # Forbidden patterns
        forbidden_patterns: list[str] = spec.schema.get("forbidden_patterns", [])
        for pattern in forbidden_patterns:
            if pattern in content:
                warnings.append(f"Forbidden pattern found: {pattern}")

        return ValidationResult(
            valid=len(errors) == 0,
            format_id=format_id,
            errors=errors,
            warnings=warnings,
        )

    # ------------------------------------------------------------------
    # Detection
    # ------------------------------------------------------------------

    def detect_format(self, filename: str) -> Optional[FormatSpec]:
        """Detect a format from a filename by extracting its extension."""
        dot = filename.rfind(".")
        if dot == -1:
            return None
        ext = filename[dot:]  # includes the dot, e.g. ".md"
        return self.by_extension(ext)

    # ------------------------------------------------------------------
    # Statistics
    # ------------------------------------------------------------------

    def stats(self) -> FormatStats:
        """Return aggregate statistics over all registered formats."""
        with self._lock:
            total_formats = len(self._formats)
            unique_mimes = len({spec.mime_type for spec in self._formats.values()})
            unique_exts = len(
                {ext for spec in self._formats.values() for ext in spec.extensions}
            )
        return FormatStats(
            total_formats=total_formats,
            total_mime_types=unique_mimes,
            total_extensions=unique_exts,
        )
