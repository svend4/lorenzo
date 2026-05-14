"""Frontmatter parser — parse and manipulate YAML-like frontmatter in markdown (stdlib only)."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterator

# ---------------------------------------------------------------------------
# Regex to detect the opening --- and closing --- of a frontmatter block.
# The frontmatter must start at the very beginning of the document.
# ---------------------------------------------------------------------------
_FM_RE = re.compile(r'\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)', re.DOTALL)


# ---------------------------------------------------------------------------
# FrontmatterData
# ---------------------------------------------------------------------------

@dataclass
class FrontmatterData:
    """Result of parsing a markdown document's frontmatter."""

    data: dict = field(default_factory=dict)
    content: str = ""
    has_frontmatter: bool = False
    raw_frontmatter: str = ""

    def get(self, key: str, default: Any = None) -> Any:
        """Dict-like access with a default."""
        return self.data.get(key, default)

    def keys(self) -> Iterator[str]:
        """Return keys of the parsed data dict."""
        return self.data.keys()


# ---------------------------------------------------------------------------
# Internal YAML-subset helpers
# ---------------------------------------------------------------------------

def _coerce(s: str) -> Any:
    """Convert a scalar YAML string token to a Python value."""
    stripped = s.strip()
    # Quoted strings
    if (stripped.startswith('"') and stripped.endswith('"')) or \
       (stripped.startswith("'") and stripped.endswith("'")):
        return stripped[1:-1]
    # Null
    if stripped in ('null', '~', ''):
        return None
    # Booleans (case-insensitive as per YAML)
    if stripped.lower() == 'true':
        return True
    if stripped.lower() == 'false':
        return False
    # Integer
    if re.fullmatch(r'-?\d+', stripped):
        return int(stripped)
    # Float
    if re.fullmatch(r'-?\d+\.\d+', stripped):
        return float(stripped)
    return stripped


def _parse_yaml_subset(text: str) -> dict:
    """
    Parse a flat YAML-subset string into a Python dict.

    Supports:
    - Scalar values: strings, quoted strings, int, float, bool, null/~
    - Block lists (``key:\\n  - item``)
    - Inline lists (``key: [a, b, c]``) for completeness
    """
    result: dict = {}
    current_key: str | None = None
    current_list: list | None = None

    for raw_line in text.splitlines():
        line = raw_line.rstrip()

        # Blank or comment line
        if not line or line.lstrip().startswith('#'):
            continue

        # List item continuation
        stripped = line.lstrip()
        if stripped.startswith('- ') and current_list is not None:
            item_str = stripped[2:].strip()
            current_list.append(_coerce(item_str))
            continue
        # Bare "-" as a list item (empty string item)
        if stripped == '-' and current_list is not None:
            current_list.append(None)
            continue

        # Key: value line
        m = re.match(r'^([A-Za-z_][\w\-]*)\s*:\s*(.*)$', line)
        if not m:
            # not a recognised line — skip
            current_list = None
            continue

        key = m.group(1)
        value = m.group(2).strip()
        current_key = key
        current_list = None

        if value == '':
            # Might be the start of a block list
            current_list = []
            result[key] = current_list
        elif value == '[]':
            result[key] = []
        elif value.startswith('[') and value.endswith(']'):
            inner = value[1:-1].strip()
            if not inner:
                result[key] = []
            else:
                items = [s.strip() for s in inner.split(',')]
                result[key] = [_coerce(x) for x in items]
        else:
            result[key] = _coerce(value)

    return result


def _dump_yaml_subset(data: dict) -> str:
    """Serialize a flat dict to YAML-subset string."""
    lines: list[str] = []
    for key, value in data.items():
        if value is None:
            lines.append(f"{key}: null")
        elif isinstance(value, bool):
            lines.append(f"{key}: {'true' if value else 'false'}")
        elif isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                if item is None:
                    lines.append(f"  - null")
                elif isinstance(item, bool):
                    lines.append(f"  - {'true' if item else 'false'}")
                else:
                    lines.append(f"  - {item}")
        else:
            lines.append(f"{key}: {value}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# FrontmatterParser
# ---------------------------------------------------------------------------

class FrontmatterParser:
    """Parse and manipulate YAML-like frontmatter blocks in markdown documents."""

    # ------------------------------------------------------------------
    # Core parse / dump
    # ------------------------------------------------------------------

    def parse(self, text: str) -> FrontmatterData:
        """Extract frontmatter and body from *text*.

        Returns a :class:`FrontmatterData` instance. When no frontmatter is
        found, ``has_frontmatter`` is ``False`` and ``content`` is the full
        input text.
        """
        m = _FM_RE.match(text)
        if not m:
            return FrontmatterData(
                data={},
                content=text,
                has_frontmatter=False,
                raw_frontmatter="",
            )
        raw = m.group(1)
        try:
            data = _parse_yaml_subset(raw)
        except Exception:
            data = {}
        content = text[m.end():]
        return FrontmatterData(
            data=data,
            content=content,
            has_frontmatter=True,
            raw_frontmatter=raw,
        )

    def dump(self, data: dict, content: str = "") -> str:
        """Serialize *data* and *content* to a markdown string with frontmatter.

        The result has the form::

            ---
            key: value
            ---
            <content>
        """
        fm_str = _dump_yaml_subset(data)
        if content:
            return f"---\n{fm_str}\n---\n{content}"
        return f"---\n{fm_str}\n---\n"

    # ------------------------------------------------------------------
    # Higher-level helpers
    # ------------------------------------------------------------------

    def update(self, text: str, updates: dict) -> str:
        """Parse *text*, merge *updates* into the frontmatter, and dump.

        Keys present in *updates* overwrite existing values; new keys are
        appended. When *text* has no frontmatter a fresh frontmatter block is
        prepended.
        """
        fm = self.parse(text)
        merged = {**fm.data, **updates}
        return self.dump(merged, fm.content)

    def remove(self, text: str) -> str:
        """Strip frontmatter from *text* and return the body only."""
        return self.parse(text).content

    def has_frontmatter(self, text: str) -> bool:
        """Return ``True`` if *text* starts with a valid frontmatter block."""
        return bool(_FM_RE.match(text))

    def extract_field(self, text: str, key: str, default: Any = None) -> Any:
        """Convenience method: parse *text* and return the value of *key*."""
        return self.parse(text).get(key, default)
