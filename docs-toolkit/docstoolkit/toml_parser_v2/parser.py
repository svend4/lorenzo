"""TOML subset parser/serializer — pure stdlib implementation.

Supports a useful subset of TOML 1.0:
  - Comments (# line-end)
  - Basic strings with \\n, \\t, \\\\, \\" escapes
  - Integers (with underscore separators)
  - Floats (incl. exponent form)
  - Booleans (true / false)
  - Arrays (single-line and multi-line)
  - Tables [a] and nested [a.b.c]
  - Inline tables { a = 1, b = 2 }

Datetimes, multi-line strings, and arrays-of-tables are NOT supported.
"""
from __future__ import annotations

from typing import Any, List, Tuple


class ParseError(Exception):
    """Raised when TOML text cannot be parsed."""


class TomlParser:
    """Minimal TOML parser/serializer.

    Instances are stateless — methods can be called on a single shared instance.
    """

    # ------------------------------------------------------------------ parse

    def parse(self, text: str) -> dict:
        """Parse a TOML document into a nested dict."""
        if not isinstance(text, str):
            raise ParseError("input must be a string")

        result: dict = {}
        current_path: List[str] = []  # current table path
        # Pre-join lines that contain unclosed arrays / inline tables
        logical_lines = self._logical_lines(text)

        for lineno, raw in logical_lines:
            line = self._strip_comment(raw).strip()
            if not line:
                continue
            if line.startswith("[") and line.endswith("]"):
                # Table header
                header = line[1:-1].strip()
                if not header:
                    raise ParseError(f"line {lineno}: empty table header")
                if header.startswith("[") or header.endswith("]"):
                    raise ParseError(
                        f"line {lineno}: arrays of tables not supported"
                    )
                current_path = self._split_dotted_key(header)
                self._ensure_table(result, current_path, lineno)
                continue
            if "=" not in line:
                raise ParseError(f"line {lineno}: expected '=' in {line!r}")
            key_part, _, value_part = line.partition("=")
            key_part = key_part.strip()
            value_part = value_part.strip()
            if not key_part:
                raise ParseError(f"line {lineno}: missing key")
            key_path = self._split_dotted_key(key_part)
            full_path = current_path + key_path[:-1]
            container = self._ensure_table(result, full_path, lineno)
            leaf = key_path[-1]
            if leaf in container and not isinstance(container[leaf], dict):
                raise ParseError(f"line {lineno}: duplicate key {leaf!r}")
            try:
                value = self.parse_value(value_part)
            except ParseError as exc:
                raise ParseError(f"line {lineno}: {exc}") from None
            container[leaf] = value
        return result

    def is_valid(self, text: str) -> bool:
        """Return True if `text` parses successfully."""
        try:
            self.parse(text)
            return True
        except ParseError:
            return False

    # ----------------------------------------------------------- parse helpers

    @staticmethod
    def _strip_comment(line: str) -> str:
        """Remove trailing '# comment' but ignore '#' inside strings."""
        out = []
        in_string = False
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and in_string and i + 1 < len(line):
                out.append(ch)
                out.append(line[i + 1])
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
                out.append(ch)
                i += 1
                continue
            if ch == "#" and not in_string:
                break
            out.append(ch)
            i += 1
        return "".join(out)

    @classmethod
    def _logical_lines(cls, text: str) -> List[Tuple[int, str]]:
        """Combine continuation lines (open brackets/braces) into one."""
        lines = text.splitlines()
        result: List[Tuple[int, str]] = []
        buffer = ""
        start_lineno = 0
        depth_sq = 0
        depth_cu = 0
        for idx, raw in enumerate(lines, start=1):
            stripped = cls._strip_comment(raw)
            if buffer:
                buffer += "\n" + raw
            else:
                buffer = raw
                start_lineno = idx
            # update depth using stripped (comment-free) text but track inside strings
            for ch in cls._iter_outside_strings(stripped):
                if ch == "[":
                    depth_sq += 1
                elif ch == "]":
                    depth_sq -= 1
                elif ch == "{":
                    depth_cu += 1
                elif ch == "}":
                    depth_cu -= 1
            if depth_sq <= 0 and depth_cu <= 0:
                result.append((start_lineno, buffer))
                buffer = ""
                depth_sq = 0
                depth_cu = 0
        if buffer:
            # Unbalanced — let the value parser raise a meaningful error
            result.append((start_lineno, buffer))
        return result

    @staticmethod
    def _iter_outside_strings(text: str):
        in_string = False
        i = 0
        while i < len(text):
            ch = text[i]
            if ch == "\\" and in_string and i + 1 < len(text):
                i += 2
                continue
            if ch == '"':
                in_string = not in_string
                i += 1
                continue
            if not in_string:
                yield ch
            i += 1

    @staticmethod
    def _split_dotted_key(key: str) -> List[str]:
        """Split 'a.b.c' into ['a', 'b', 'c'], honoring quoted segments."""
        parts: List[str] = []
        i = 0
        current = []
        while i < len(key):
            ch = key[i]
            if ch == '"':
                # quoted segment
                end = i + 1
                while end < len(key) and key[end] != '"':
                    if key[end] == "\\" and end + 1 < len(key):
                        end += 2
                        continue
                    end += 1
                if end >= len(key):
                    raise ParseError(f"unterminated quoted key in {key!r}")
                current.append(key[i + 1 : end])
                i = end + 1
                continue
            if ch == ".":
                parts.append("".join(current).strip())
                current = []
                i += 1
                continue
            current.append(ch)
            i += 1
        if current:
            parts.append("".join(current).strip())
        parts = [p for p in parts if p != ""]
        if not parts:
            raise ParseError(f"empty key: {key!r}")
        for p in parts:
            if not p:
                raise ParseError(f"empty key segment in {key!r}")
        return parts

    @staticmethod
    def _ensure_table(root: dict, path: List[str], lineno: int) -> dict:
        node = root
        for segment in path:
            if segment not in node:
                node[segment] = {}
            elif not isinstance(node[segment], dict):
                raise ParseError(
                    f"line {lineno}: cannot redefine {segment!r} as a table"
                )
            node = node[segment]
        return node

    # ---------------------------------------------------------- value parsing

    def parse_value(self, text: str) -> Any:
        """Parse a single TOML value from `text`."""
        if not isinstance(text, str):
            raise ParseError("value must be a string")
        s = text.strip()
        if not s:
            raise ParseError("empty value")
        value, rest = self._parse_value(s)
        rest = rest.strip()
        if rest:
            raise ParseError(f"trailing text after value: {rest!r}")
        return value

    def _parse_value(self, s: str) -> Tuple[Any, str]:
        s = s.lstrip()
        if not s:
            raise ParseError("empty value")
        ch = s[0]
        if ch == '"':
            return self._parse_string(s)
        if ch == "[":
            return self._parse_array(s)
        if ch == "{":
            return self._parse_inline_table(s)
        # boolean
        if s.startswith("true") and self._terminator(s, 4):
            return True, s[4:]
        if s.startswith("false") and self._terminator(s, 5):
            return False, s[5:]
        # number — read until terminator
        return self._parse_number(s)

    @staticmethod
    def _terminator(s: str, idx: int) -> bool:
        if idx >= len(s):
            return True
        return s[idx] in " \t,]}\n"

    @staticmethod
    def _parse_string(s: str) -> Tuple[str, str]:
        assert s[0] == '"'
        out = []
        i = 1
        while i < len(s):
            ch = s[i]
            if ch == "\\":
                if i + 1 >= len(s):
                    raise ParseError("dangling escape in string")
                esc = s[i + 1]
                mapping = {
                    "n": "\n",
                    "t": "\t",
                    "r": "\r",
                    "\\": "\\",
                    '"': '"',
                    "/": "/",
                    "b": "\b",
                    "f": "\f",
                    "0": "\0",
                }
                if esc not in mapping:
                    raise ParseError(f"unknown escape: \\{esc}")
                out.append(mapping[esc])
                i += 2
                continue
            if ch == '"':
                return "".join(out), s[i + 1 :]
            out.append(ch)
            i += 1
        raise ParseError("unterminated string")

    def _parse_array(self, s: str) -> Tuple[list, str]:
        assert s[0] == "["
        items: list = []
        i = 1
        n = len(s)
        while i < n:
            # skip whitespace, newlines, commas (allow trailing/leading newlines)
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i >= n:
                raise ParseError("unterminated array")
            if s[i] == "]":
                return items, s[i + 1 :]
            value, rest = self._parse_value(s[i:])
            items.append(value)
            consumed = len(s) - i - len(rest)
            i += consumed
            # skip whitespace/newlines
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i < n and s[i] == ",":
                i += 1
                continue
            # otherwise must be closing bracket
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i < n and s[i] == "]":
                return items, s[i + 1 :]
            if i >= n:
                raise ParseError("unterminated array")
            raise ParseError(f"expected ',' or ']' in array, got {s[i]!r}")
        raise ParseError("unterminated array")

    def _parse_inline_table(self, s: str) -> Tuple[dict, str]:
        assert s[0] == "{"
        result: dict = {}
        i = 1
        n = len(s)
        while i < n:
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i >= n:
                raise ParseError("unterminated inline table")
            if s[i] == "}":
                return result, s[i + 1 :]
            # parse key
            key_end = i
            while key_end < n and s[key_end] not in "= \t":
                key_end += 1
            key_text = s[i:key_end]
            if not key_text:
                raise ParseError("empty key in inline table")
            key_path = self._split_dotted_key(key_text)
            i = key_end
            while i < n and s[i] in " \t":
                i += 1
            if i >= n or s[i] != "=":
                raise ParseError("expected '=' in inline table")
            i += 1
            while i < n and s[i] in " \t":
                i += 1
            value, rest = self._parse_value(s[i:])
            consumed = len(s) - i - len(rest)
            i += consumed
            # place into nested dict
            node = result
            for seg in key_path[:-1]:
                node = node.setdefault(seg, {})
                if not isinstance(node, dict):
                    raise ParseError("invalid nested key in inline table")
            node[key_path[-1]] = value
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i < n and s[i] == ",":
                i += 1
                continue
            while i < n and s[i] in " \t\n\r":
                i += 1
            if i < n and s[i] == "}":
                return result, s[i + 1 :]
            if i >= n:
                raise ParseError("unterminated inline table")
            raise ParseError(
                f"expected ',' or '}}' in inline table, got {s[i]!r}"
            )
        raise ParseError("unterminated inline table")

    @staticmethod
    def _parse_number(s: str) -> Tuple[Any, str]:
        i = 0
        n = len(s)
        # consume token until terminator
        while i < n and s[i] not in " \t,]}\n\r":
            i += 1
        token = s[:i]
        rest = s[i:]
        if not token:
            raise ParseError("empty number")
        cleaned = token.replace("_", "")
        if not cleaned:
            raise ParseError(f"invalid number: {token!r}")
        # detect float
        if any(ch in cleaned for ch in ".eE"):
            try:
                return float(cleaned), rest
            except ValueError:
                raise ParseError(f"invalid float: {token!r}") from None
        # integer
        try:
            return int(cleaned), rest
        except ValueError:
            raise ParseError(f"invalid value: {token!r}") from None

    # ----------------------------------------------------------------- format

    def format_value(self, value: Any) -> str:
        """Format a single value as TOML text."""
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, int):
            return str(value)
        if isinstance(value, float):
            # TOML requires a decimal point for floats
            text = repr(value)
            if "e" not in text and "E" not in text and "." not in text:
                text += ".0"
            return text
        if isinstance(value, str):
            return self._format_string(value)
        if isinstance(value, list):
            return "[" + ", ".join(self.format_value(v) for v in value) + "]"
        if isinstance(value, dict):
            items = ", ".join(
                f"{k} = {self.format_value(v)}" for k, v in value.items()
            )
            return "{" + items + "}"
        if value is None:
            raise ParseError("cannot serialize None to TOML")
        raise ParseError(f"cannot serialize value of type {type(value).__name__}")

    @staticmethod
    def _format_string(value: str) -> str:
        escaped = (
            value.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace("\r", "\\r")
        )
        return '"' + escaped + '"'

    def dump(self, data: dict) -> str:
        """Serialize a nested dict as a TOML document."""
        if not isinstance(data, dict):
            raise ParseError("dump expects a dict at the top level")
        lines: List[str] = []
        # First, scalar (non-dict) top-level keys
        scalar_items = [(k, v) for k, v in data.items() if not isinstance(v, dict)]
        table_items = [(k, v) for k, v in data.items() if isinstance(v, dict)]
        for key, value in scalar_items:
            lines.append(f"{key} = {self.format_value(value)}")
        for key, value in table_items:
            self._dump_table(value, [key], lines)
        return "\n".join(lines) + ("\n" if lines else "")

    def _dump_table(self, table: dict, path: List[str], lines: List[str]) -> None:
        scalar_items = [
            (k, v) for k, v in table.items() if not isinstance(v, dict)
        ]
        nested_items = [(k, v) for k, v in table.items() if isinstance(v, dict)]
        if lines:
            lines.append("")
        lines.append("[" + ".".join(path) + "]")
        for key, value in scalar_items:
            lines.append(f"{key} = {self.format_value(value)}")
        for key, value in nested_items:
            self._dump_table(value, path + [key], lines)

    # ----------------------------------------------------------- dotted access

    @staticmethod
    def get(data: dict, dotted_key: str, default: Any = None) -> Any:
        """Look up a value via dotted key, e.g. 'a.b.c'."""
        if not isinstance(dotted_key, str) or not dotted_key:
            return default
        node: Any = data
        for segment in dotted_key.split("."):
            if isinstance(node, dict) and segment in node:
                node = node[segment]
            else:
                return default
        return node

    @staticmethod
    def set(data: dict, dotted_key: str, value: Any) -> None:
        """Set a value via dotted key, creating intermediate dicts."""
        if not isinstance(data, dict):
            raise ParseError("set requires a dict")
        if not isinstance(dotted_key, str) or not dotted_key:
            raise ParseError("dotted_key must be a non-empty string")
        segments = dotted_key.split(".")
        if any(not s for s in segments):
            raise ParseError("empty segment in dotted_key")
        node = data
        for segment in segments[:-1]:
            existing = node.get(segment)
            if not isinstance(existing, dict):
                existing = {}
                node[segment] = existing
            node = existing
        node[segments[-1]] = value
