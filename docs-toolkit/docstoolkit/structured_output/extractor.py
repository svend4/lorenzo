"""Extraction utilities for structured output parsing."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field


@dataclass
class ExtractionResult:
    """Result of an extraction attempt."""

    data: dict
    missing_fields: list[str] = field(default_factory=list)
    parse_errors: list[str] = field(default_factory=list)
    raw_text: str = ""

    def is_complete(self) -> bool:
        """Return True if no required fields are missing."""
        return len(self.missing_fields) == 0

    def is_valid(self) -> bool:
        """Return True if no parse errors occurred."""
        return len(self.parse_errors) == 0


class StructuredExtractor:
    """Extract structured data from various text formats."""

    def extract_json(self, text: str) -> dict | None:
        """Find and parse the first valid JSON object {...} in text.

        Handles JSON embedded in prose, code fences, or other surrounding text.
        Only matches top-level JSON objects, not objects nested inside arrays.
        """
        # Walk through the text tracking array depth so we only try to parse
        # { ... } blocks that are at the "top level" of the surrounding text
        # (i.e., not inside a [ ... ] array construct).
        i = 0
        n = len(text)
        array_depth = 0
        in_string = False
        escape_next = False

        while i < n:
            ch = text[i]

            if escape_next:
                escape_next = False
                i += 1
                continue

            if ch == "\\" and in_string:
                escape_next = True
                i += 1
                continue

            if ch == '"':
                in_string = not in_string
                i += 1
                continue

            if in_string:
                i += 1
                continue

            if ch == "[":
                array_depth += 1
                i += 1
                continue

            if ch == "]":
                if array_depth > 0:
                    array_depth -= 1
                i += 1
                continue

            if ch == "{" and array_depth == 0:
                # Try to extract a complete JSON object starting here
                start = i
                depth = 0
                j = start
                inner_string = False
                inner_escape = False
                end = -1

                while j < n:
                    c = text[j]

                    if inner_escape:
                        inner_escape = False
                        j += 1
                        continue

                    if c == "\\" and inner_string:
                        inner_escape = True
                        j += 1
                        continue

                    if c == '"':
                        inner_string = not inner_string
                        j += 1
                        continue

                    if inner_string:
                        j += 1
                        continue

                    if c == "{":
                        depth += 1
                    elif c == "}":
                        depth -= 1
                        if depth == 0:
                            end = j
                            break

                    j += 1

                if end != -1:
                    candidate = text[start : end + 1]
                    try:
                        result = json.loads(candidate)
                        if isinstance(result, dict):
                            return result
                    except (json.JSONDecodeError, ValueError):
                        pass
                # Move past this brace
                i += 1
                continue

            i += 1

        return None

    def extract_markdown_table(self, text: str) -> list[dict]:
        """Parse a Markdown table into a list of dicts.

        The header row becomes the dict keys.
        Returns an empty list if no valid table is found.
        """
        lines = text.splitlines()
        table_lines: list[str] = []
        in_table = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("|") and stripped.endswith("|"):
                table_lines.append(stripped)
                in_table = True
            elif in_table:
                # Stop at the first non-table line after a table started
                if stripped:
                    break

        if len(table_lines) < 2:
            return []

        # Parse header
        header_line = table_lines[0]
        headers = [h.strip() for h in header_line.strip("|").split("|")]
        headers = [h for h in headers if h]  # remove empty

        if not headers:
            return []

        # Check that second line is a separator (contains dashes)
        separator_line = table_lines[1]
        separator_cells = [c.strip() for c in separator_line.strip("|").split("|")]
        is_separator = all(
            re.match(r"^:?-+:?$", cell) for cell in separator_cells if cell.strip()
        )

        if not is_separator:
            return []

        # Parse data rows
        rows = []
        for line in table_lines[2:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            # Align cells to headers
            row: dict[str, str] = {}
            for i, header in enumerate(headers):
                row[header] = cells[i] if i < len(cells) else ""
            rows.append(row)

        return rows

    def extract_key_value(self, text: str, sep: str = ":") -> dict:
        """Parse 'key: value' lines from text into a dict.

        Lines not containing the separator are skipped.
        """
        result: dict[str, str] = {}
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            idx = line.find(sep)
            if idx == -1:
                continue
            key = line[:idx].strip()
            value = line[idx + len(sep) :].strip()
            if key:
                result[key] = value
        return result

    def extract_code_block(self, text: str, lang: str = "") -> str | None:
        """Extract content of first matching fenced code block.

        If lang is provided, only match fences with that language identifier.
        If lang is empty, match any fenced code block.
        Returns None if no matching block is found.
        """
        # Build pattern for opening fence
        if lang:
            # Match ```lang or ```lang with trailing whitespace
            open_pattern = re.compile(
                r"^```[ \t]*" + re.escape(lang) + r"[ \t]*$", re.MULTILINE
            )
        else:
            # Match ``` optionally followed by a language identifier
            open_pattern = re.compile(r"^```[ \t]*\w*[ \t]*$", re.MULTILINE)

        close_pattern = re.compile(r"^```[ \t]*$", re.MULTILINE)

        open_match = open_pattern.search(text)
        if open_match is None:
            return None

        # Find the closing fence after the opening
        search_start = open_match.end()
        close_match = close_pattern.search(text, search_start)
        if close_match is None:
            return None

        content = text[search_start : close_match.start()]
        # Strip leading newline if present
        if content.startswith("\n"):
            content = content[1:]
        # Strip trailing newline if present
        if content.endswith("\n"):
            content = content[:-1]

        return content
