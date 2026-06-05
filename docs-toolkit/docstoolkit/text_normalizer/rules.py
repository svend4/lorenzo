"""NormRule dataclass and built-in rule sets for text normalization."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class NormRule:
    """A single normalization rule backed by a compiled regex substitution.

    The *replacement* may be either a plain string (passed to ``re.sub``
    directly) or a callable that accepts a :class:`re.Match` object and
    returns a replacement string.  The latter is useful for case-folding and
    other transformations that cannot be expressed as a static string.
    """

    name: str
    pattern: str
    replacement: str | Callable[[re.Match], str]
    flags: int = 0
    description: str = ""

    def apply(self, text: str) -> str:
        """Return *text* with the rule applied via ``re.sub``."""
        return re.sub(self.pattern, self.replacement, text, flags=self.flags)


# ---------------------------------------------------------------------------
# Built-in rule sets
# ---------------------------------------------------------------------------

def whitespace_rules() -> list[NormRule]:
    """Return rules that clean up whitespace.

    Rules are applied in this order:

    1. Normalize Windows/Mac line endings to ``\\n``.
    2. Collapse three or more consecutive blank lines to two newlines.
    3. Collapse multiple horizontal whitespace characters on one line to a
       single space.
    4. Strip leading/trailing spaces from every line.
    5. Strip leading/trailing newlines from the whole text.
    """
    return [
        NormRule(
            name="normalize_line_endings",
            pattern=r"\r\n|\r",
            replacement="\n",
            description="Convert Windows (CRLF) and old Mac (CR) line endings to LF",
        ),
        NormRule(
            name="collapse_blank_lines",
            pattern=r"\n{3,}",
            replacement="\n\n",
            description="Collapse three or more consecutive newlines to two",
        ),
        NormRule(
            name="collapse_spaces",
            pattern=r"[^\S\n]+",
            replacement=" ",
            description="Collapse multiple horizontal whitespace characters to a single space",
        ),
        NormRule(
            name="strip_line_whitespace",
            pattern=r"^ | $",
            replacement="",
            flags=re.MULTILINE,
            description="Strip leading and trailing spaces from every line",
        ),
        NormRule(
            name="strip_text_edges",
            pattern=r"^\n+|\n+$",
            replacement="",
            description="Strip leading and trailing newlines from the whole text",
        ),
    ]


def punctuation_rules() -> list[NormRule]:
    """Return rules that normalize punctuation.

    1. Em-dash (—, U+2014) and en-dash (–, U+2013) → ASCII hyphen-minus.
    2. Curly/typographic double quotes → straight ``"``.
    3. Curly/typographic single quotes and backtick → straight ``'``.
    4. Unicode ellipsis (…) → three ASCII dots.
    5. Strip a trailing period from a word that is followed by whitespace or
       end-of-string (avoids stripping genuine sentence-ending periods in most
       cases handled by other rules).
    """
    return [
        NormRule(
            name="em_dash_to_hyphen",
            pattern=r"[–—]",
            replacement="-",
            description="Replace en-dash and em-dash with ASCII hyphen",
        ),
        NormRule(
            name="normalize_double_quotes",
            pattern='[“”«»„]',
            replacement='"',
            description="Replace typographic double-quote variants with straight double quote",
        ),
        NormRule(
            name="normalize_single_quotes",
            pattern="[‘’`]",
            replacement="'",
            description="Replace typographic single-quote / backtick variants with apostrophe",
        ),
        NormRule(
            name="ellipsis_to_dots",
            pattern=r"…",
            replacement="...",
            description="Replace Unicode ellipsis character with three ASCII dots",
        ),
        NormRule(
            name="strip_trailing_word_dot",
            pattern=r"(\w)\.(?=\s|$)",
            replacement=r"\1",
            flags=re.MULTILINE,
            description="Remove trailing period from a word followed by whitespace or end-of-line",
        ),
    ]


def case_rules() -> list[NormRule]:
    """Return rules that normalize letter case to lower-case.

    Uses a callable replacement so that every run of uppercase letters
    (ASCII and Cyrillic) is folded to lower-case via :meth:`str.lower`.
    """
    return [
        NormRule(
            name="lowercase_all",
            pattern=r"[A-ZА-ЯЁ]+",
            replacement=lambda m: m.group(0).lower(),
            flags=re.UNICODE,
            description="Convert all uppercase letters to lowercase",
        ),
    ]


def number_rules() -> list[NormRule]:
    """Return rules that replace numeric literals with ``[NUM]``.

    Floats are matched *before* integers so that ``3.14`` becomes a single
    ``[NUM]`` token rather than ``[NUM].[NUM]``.  Only "standalone" numbers
    delimited by word boundaries are replaced, so sub-strings inside
    identifiers (e.g. ``model3``) are left intact.
    """
    return [
        NormRule(
            name="replace_float",
            pattern=r"\b\d+\.\d+\b",
            replacement="[NUM]",
            description="Replace standalone floating-point literals with [NUM]",
        ),
        NormRule(
            name="replace_integer",
            pattern=r"\b\d+\b",
            replacement="[NUM]",
            description="Replace standalone integer literals with [NUM]",
        ),
    ]
