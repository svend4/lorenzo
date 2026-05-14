"""Core metadata extractor — stdlib only."""
from __future__ import annotations

import re
from typing import ClassVar

from docstoolkit.metadata_extractor.fields import ExtractedField, FieldType


class MetadataExtractor:
    """Extract typed metadata fields from plain text using regex patterns."""

    # -----------------------------------------------------------------
    # Class-level compiled patterns
    # -----------------------------------------------------------------
    _RE_EMAIL: ClassVar[re.Pattern] = re.compile(
        r"[\w.+-]+@[\w-]+\.[\w.-]+"
    )
    _RE_URL: ClassVar[re.Pattern] = re.compile(
        r"https?://[^\s]+"
    )
    _RE_PHONE: ClassVar[re.Pattern] = re.compile(
        r"\+?[\d][\d\s\-()]{7,15}[\d]"
    )
    # Date patterns — order matters: ISO first, then EU, then US
    _RE_DATE_ISO: ClassVar[re.Pattern] = re.compile(
        r"\d{4}-\d{2}-\d{2}"
    )
    _RE_DATE_EU: ClassVar[re.Pattern] = re.compile(
        r"\d{1,2}\.\d{1,2}\.\d{4}"
    )
    _RE_DATE_US: ClassVar[re.Pattern] = re.compile(
        r"\d{1,2}/\d{1,2}/\d{4}"
    )
    _RE_NUMBER: ClassVar[re.Pattern] = re.compile(
        r"-?\d+\.?\d*"
    )
    _RE_BOOLEAN: ClassVar[re.Pattern] = re.compile(
        r"\b(?:true|false|yes|no|1|0)\b", re.IGNORECASE
    )

    # -----------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------

    def extract(self, text: str) -> list[ExtractedField]:
        """Find all typed matches in *text*; return sorted by start position."""
        results: list[ExtractedField] = []

        for m in self._RE_EMAIL.finditer(text):
            results.append(
                ExtractedField(
                    name="email",
                    value=m.group(),
                    field_type=FieldType.EMAIL,
                    confidence=1.0,
                    source_span=(m.start(), m.end()),
                )
            )

        for m in self._RE_URL.finditer(text):
            results.append(
                ExtractedField(
                    name="url",
                    value=m.group(),
                    field_type=FieldType.URL,
                    confidence=1.0,
                    source_span=(m.start(), m.end()),
                )
            )

        for m in self._RE_PHONE.finditer(text):
            results.append(
                ExtractedField(
                    name="phone",
                    value=m.group(),
                    field_type=FieldType.PHONE,
                    confidence=1.0,
                    source_span=(m.start(), m.end()),
                )
            )

        for pat, label in (
            (self._RE_DATE_ISO, "date_iso"),
            (self._RE_DATE_EU, "date_eu"),
            (self._RE_DATE_US, "date_us"),
        ):
            for m in pat.finditer(text):
                results.append(
                    ExtractedField(
                        name=label,
                        value=m.group(),
                        field_type=FieldType.DATE,
                        confidence=1.0,
                        source_span=(m.start(), m.end()),
                    )
                )

        for m in self._RE_NUMBER.finditer(text):
            results.append(
                ExtractedField(
                    name="number",
                    value=float(m.group()),
                    field_type=FieldType.NUMBER,
                    confidence=1.0,
                    source_span=(m.start(), m.end()),
                )
            )

        for m in self._RE_BOOLEAN.finditer(text):
            raw = m.group().lower()
            bool_val = raw in ("true", "yes", "1")
            results.append(
                ExtractedField(
                    name="boolean",
                    value=bool_val,
                    field_type=FieldType.BOOLEAN,
                    confidence=1.0,
                    source_span=(m.start(), m.end()),
                )
            )

        results.sort(key=lambda f: f.source_span[0])
        return results

    def extract_emails(self, text: str) -> list[ExtractedField]:
        """Return ExtractedField objects for every email address found in *text*."""
        return [
            ExtractedField(
                name="email",
                value=m.group(),
                field_type=FieldType.EMAIL,
                confidence=1.0,
                source_span=(m.start(), m.end()),
            )
            for m in self._RE_EMAIL.finditer(text)
        ]

    def extract_urls(self, text: str) -> list[ExtractedField]:
        """Return ExtractedField objects for every URL found in *text*."""
        return [
            ExtractedField(
                name="url",
                value=m.group(),
                field_type=FieldType.URL,
                confidence=1.0,
                source_span=(m.start(), m.end()),
            )
            for m in self._RE_URL.finditer(text)
        ]

    def extract_dates(self, text: str) -> list[str]:
        """Return matched date strings (ISO, EU, and US formats)."""
        dates: list[str] = []
        for pat in (self._RE_DATE_ISO, self._RE_DATE_EU, self._RE_DATE_US):
            dates.extend(m.group() for m in pat.finditer(text))
        return dates

    def extract_numbers(self, text: str) -> list[float]:
        """Return parsed float values for every number token found in *text*."""
        return [float(m.group()) for m in self._RE_NUMBER.finditer(text)]

    def extract_to_dict(self, text: str) -> dict[str, list]:
        """Extract all fields and group them by FieldType name."""
        result: dict[str, list] = {ft.name: [] for ft in FieldType}
        for ef in self.extract(text):
            result[ef.field_type.name].append(ef.value)
        return result
