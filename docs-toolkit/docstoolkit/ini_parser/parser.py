"""INI-format config parser/serializer — pure stdlib implementation.

Features:
  - Sections: ``[section_name]``
  - Key-value pairs: ``key = value`` or ``key: value``
  - Comments: ``;`` or ``#`` to end of line
  - Empty lines allowed
  - Preserves insertion order of sections and keys
  - Typed accessors: get_int / get_float / get_bool / get_list
  - Text-level mutations: set / remove_key / remove_section
  - Merge of two IniFile objects (b overrides a)
  - Optional ``[DEFAULT]`` section: keys are visible from every section
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# --------------------------------------------------------------------- errors

class ParseError(Exception):
    """Raised when INI text cannot be parsed."""


# ------------------------------------------------------------------ datatypes

@dataclass
class IniSection:
    """A single ``[section]`` of an INI file."""

    name: str
    entries: Dict[str, str] = field(default_factory=dict)
    comments: List[str] = field(default_factory=list)


@dataclass
class IniFile:
    """Parsed INI document."""

    sections: Dict[str, IniSection] = field(default_factory=dict)
    header_comments: List[str] = field(default_factory=list)

    @property
    def section_names(self) -> List[str]:
        return list(self.sections.keys())

    def get_section(self, name: str) -> Optional[IniSection]:
        return self.sections.get(name)


# ------------------------------------------------------------------ constants

_DEFAULT_SECTION = "DEFAULT"
_TRUE_VALUES = frozenset({"true", "1", "yes", "on"})
_FALSE_VALUES = frozenset({"false", "0", "no", "off"})
_SECTION_RE = re.compile(r"^\[(?P<name>[^\]]*)\]\s*$")


# --------------------------------------------------------------------- parser

class IniParser:
    """INI parser/serializer.

    Stateless — a single instance can be re-used freely.
    """

    # ------------------------------------------------------------------ parse

    def parse(self, text: str) -> IniFile:
        """Parse an INI document into an :class:`IniFile`."""
        if not isinstance(text, str):
            raise ParseError("input must be a string")

        ini = IniFile()
        pending_comments: List[str] = []
        current: Optional[IniSection] = None
        seen_first_section = False

        for lineno, raw in enumerate(text.splitlines(), start=1):
            line = raw.rstrip()
            stripped = line.strip()

            # blank line --------------------------------------------------
            if not stripped:
                if not seen_first_section and pending_comments:
                    # Keep pending_comments as header comments until first section
                    pass
                continue

            # comment -----------------------------------------------------
            if stripped[0] in ";#":
                # capture text after the comment marker (including marker)
                pending_comments.append(stripped)
                continue

            # section header ---------------------------------------------
            m = _SECTION_RE.match(stripped)
            if m is not None:
                name = m.group("name").strip()
                if not name:
                    raise ParseError(
                        f"line {lineno}: empty section name"
                    )
                if not seen_first_section:
                    ini.header_comments = list(pending_comments)
                    pending_comments = []
                    seen_first_section = True
                if name in ini.sections:
                    # re-open existing section
                    current = ini.sections[name]
                    pending_comments = []
                    continue
                section = IniSection(
                    name=name,
                    comments=list(pending_comments),
                )
                ini.sections[name] = section
                current = section
                pending_comments = []
                continue

            # key=value or key:value -------------------------------------
            sep_idx = _find_separator(stripped)
            if sep_idx < 0:
                raise ParseError(
                    f"line {lineno}: expected '=' or ':' in {stripped!r}"
                )
            key = stripped[:sep_idx].strip()
            value = stripped[sep_idx + 1:].strip()
            if not key:
                raise ParseError(f"line {lineno}: missing key")

            if current is None:
                # value without a section — create an implicit one
                # but treat it as an error to be strict.
                raise ParseError(
                    f"line {lineno}: key {key!r} outside of any section"
                )
            current.entries[key] = value
            # comments accumulated above a key are discarded by design;
            # the contract only stores comments preceding sections.
            pending_comments = []

        if not seen_first_section:
            # whole file was only comments / blank lines
            ini.header_comments = list(pending_comments)
        return ini

    # ------------------------------------------------------------------- dump

    def dump(self, ini: IniFile) -> str:
        """Serialize an :class:`IniFile` back to text."""
        parts: List[str] = []

        for comment in ini.header_comments:
            parts.append(comment)
        if ini.header_comments and ini.sections:
            parts.append("")

        first = True
        for name, section in ini.sections.items():
            if not first:
                parts.append("")
            first = False
            for comment in section.comments:
                parts.append(comment)
            parts.append(f"[{name}]")
            for key, value in section.entries.items():
                parts.append(f"{key} = {value}")

        text = "\n".join(parts)
        if text and not text.endswith("\n"):
            text += "\n"
        return text

    # ------------------------------------------------------------- validation

    def is_valid(self, text: str) -> bool:
        try:
            self.parse(text)
        except ParseError:
            return False
        return True

    # ---------------------------------------------------------------- getters

    def get(
        self,
        text: str,
        section: str,
        key: str,
        default: Optional[str] = None,
    ) -> Optional[str]:
        """Return the string value of ``section/key`` or ``default``."""
        ini = self.parse(text)
        sec = ini.get_section(section)
        if sec is not None and key in sec.entries:
            return sec.entries[key]
        # fall back to DEFAULT
        default_sec = ini.get_section(_DEFAULT_SECTION)
        if default_sec is not None and key in default_sec.entries:
            return default_sec.entries[key]
        return default

    def get_int(
        self,
        text: str,
        section: str,
        key: str,
        default: int = 0,
    ) -> int:
        value = self.get(text, section, key)
        if value is None:
            return default
        try:
            return int(value.strip(), 0) if _looks_like_int(value) else int(
                value.strip()
            )
        except ValueError:
            try:
                return int(float(value.strip()))
            except ValueError:
                return default

    def get_float(
        self,
        text: str,
        section: str,
        key: str,
        default: float = 0.0,
    ) -> float:
        value = self.get(text, section, key)
        if value is None:
            return default
        try:
            return float(value.strip())
        except ValueError:
            return default

    def get_bool(
        self,
        text: str,
        section: str,
        key: str,
        default: bool = False,
    ) -> bool:
        value = self.get(text, section, key)
        if value is None:
            return default
        norm = value.strip().lower()
        if norm in _TRUE_VALUES:
            return True
        if norm in _FALSE_VALUES:
            return False
        return default

    def get_list(
        self,
        text: str,
        section: str,
        key: str,
        separator: str = ",",
    ) -> List[str]:
        value = self.get(text, section, key)
        if value is None or value == "":
            return []
        return [item.strip() for item in value.split(separator)]

    # --------------------------------------------------------------- mutators

    def set(
        self,
        text: str,
        section: str,
        key: str,
        value: str,
    ) -> str:
        """Return ``text`` with ``section/key`` set to ``value``.

        Adds the section and/or key if missing.  Preserves the original
        document structure when possible.
        """
        ini = self.parse(text)
        sec = ini.get_section(section)
        if sec is None:
            sec = IniSection(name=section)
            ini.sections[section] = sec
        sec.entries[key] = value
        return self.dump(ini)

    def remove_key(self, text: str, section: str, key: str) -> str:
        ini = self.parse(text)
        sec = ini.get_section(section)
        if sec is not None and key in sec.entries:
            del sec.entries[key]
        return self.dump(ini)

    def remove_section(self, text: str, section: str) -> str:
        ini = self.parse(text)
        if section in ini.sections:
            del ini.sections[section]
        return self.dump(ini)

    # ------------------------------------------------------------------ merge

    def merge(self, ini_a: IniFile, ini_b: IniFile) -> IniFile:
        """Return a new :class:`IniFile` where ``ini_b`` overrides ``ini_a``.

        Sections present only in ``ini_a`` are kept verbatim.  Sections
        present in ``ini_b`` either extend or override the matching section
        in ``ini_a`` on a per-key basis.  ``header_comments`` from ``ini_a``
        are preserved; ``ini_b`` header comments are appended if non-empty.
        """
        merged = IniFile()
        merged.header_comments = list(ini_a.header_comments)
        for comment in ini_b.header_comments:
            if comment not in merged.header_comments:
                merged.header_comments.append(comment)

        for name, section in ini_a.sections.items():
            merged.sections[name] = IniSection(
                name=name,
                entries=dict(section.entries),
                comments=list(section.comments),
            )

        for name, section in ini_b.sections.items():
            if name in merged.sections:
                existing = merged.sections[name]
                for key, value in section.entries.items():
                    existing.entries[key] = value
                # extend comments without duplicates
                for comment in section.comments:
                    if comment not in existing.comments:
                        existing.comments.append(comment)
            else:
                merged.sections[name] = IniSection(
                    name=name,
                    entries=dict(section.entries),
                    comments=list(section.comments),
                )

        return merged


# --------------------------------------------------------------------- helpers

def _find_separator(line: str) -> int:
    """Return the index of the first separator (``=`` or ``:``) in ``line``.

    The earliest occurring separator wins.  Returns ``-1`` if none exists.
    """
    eq = line.find("=")
    co = line.find(":")
    if eq < 0:
        return co
    if co < 0:
        return eq
    return min(eq, co)


def _looks_like_int(value: str) -> bool:
    s = value.strip()
    if not s:
        return False
    if s[0] in "+-":
        s = s[1:]
    if s.startswith(("0x", "0X", "0o", "0O", "0b", "0B")):
        return True
    return s.isdigit()
