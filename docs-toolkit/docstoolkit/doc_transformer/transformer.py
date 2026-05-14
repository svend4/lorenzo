"""Document transformer — apply named transformations pipeline-style.

Supports a wide range of text transformations: case manipulation, redaction,
replacement, extraction, line-level prefix/suffix, indentation, wrapping, and
more.  Each transform can be applied conditionally (only when a regex matches
the input).

Usage
-----
.. code-block:: python

    from docstoolkit.doc_transformer import (
        DocTransformer, Transform, TransformOp
    )

    t = DocTransformer()
    pipe = [
        Transform(op=TransformOp.STRIP),
        Transform(op=TransformOp.UPPERCASE),
    ]
    result = t.apply_pipeline("  hello  ", pipe)
    assert result.transformed == "HELLO"
    assert result.changed
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TransformOp(str, Enum):
    """Supported transform operations."""

    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    TITLE_CASE = "title_case"
    SENTENCE_CASE = "sentence_case"
    REVERSE = "reverse"
    REDACT = "redact"
    REPLACE = "replace"
    EXTRACT = "extract"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    STRIP = "strip"
    WRAP = "wrap"
    INDENT = "indent"
    DEDENT = "dedent"


@dataclass
class Transform:
    """A single transform spec.

    Parameters
    ----------
    op:
        Which :class:`TransformOp` to apply.
    params:
        Operation-specific parameters (e.g. for REPLACE: ``{"old": "...", "new": "..."}``).
    condition:
        Optional regex pattern; the transform is only applied when
        ``re.search(condition, text)`` matches.
    """

    op: TransformOp
    params: dict = field(default_factory=dict)
    condition: Optional[str] = None


@dataclass
class TransformResult:
    """Result of applying a pipeline of transforms."""

    original: str
    transformed: str
    applied: list = field(default_factory=list)

    @property
    def changed(self) -> bool:
        """True if the transformed text differs from the original."""
        return self.original != self.transformed


class DocTransformer:
    """Apply named transformations to document text."""

    # ------------------------------------------------------------------
    # Individual operations
    # ------------------------------------------------------------------

    def uppercase(self, text: str) -> str:
        return text.upper()

    def lowercase(self, text: str) -> str:
        return text.lower()

    def title_case(self, text: str) -> str:
        return text.title()

    def sentence_case(self, text: str) -> str:
        """Capitalize the first letter of each sentence.

        Sentence boundaries: ``.``, ``!``, ``?``.  Other characters within
        a sentence are preserved as-is (the rest of the sentence is not
        lower-cased — only the first letter is uppercased).
        """
        if not text:
            return text

        # Split keeping the delimiters so we can rebuild the text.
        parts = re.split(r"([.!?]+\s*)", text)
        out = []
        for part in parts:
            if not part:
                out.append(part)
                continue
            # If the part is purely delimiter/whitespace, keep as-is.
            if re.fullmatch(r"[.!?]+\s*", part):
                out.append(part)
                continue
            # Capitalize the first alpha character of the part.
            new_part = []
            done = False
            for ch in part:
                if not done and ch.isalpha():
                    new_part.append(ch.upper())
                    done = True
                else:
                    new_part.append(ch)
            out.append("".join(new_part))
        return "".join(out)

    def reverse(self, text: str) -> str:
        return text[::-1]

    def redact(
        self, text: str, pattern: str, replacement: str = "[REDACTED]"
    ) -> str:
        """Replace all regex matches with ``replacement``."""
        return re.sub(pattern, replacement, text)

    def replace(
        self, text: str, old: str, new: str, regex: bool = False
    ) -> str:
        """Replace ``old`` with ``new``.  If ``regex`` is True, treat ``old``
        as a regex pattern."""
        if regex:
            return re.sub(old, new, text)
        return text.replace(old, new)

    def extract(self, text: str, pattern: str) -> list:
        """Return all regex matches as a list (``re.findall``)."""
        return re.findall(pattern, text)

    def prefix(self, text: str, prefix_str: str) -> str:
        """Prepend ``prefix_str`` to each line."""
        if not text:
            return text
        lines = text.split("\n")
        return "\n".join(prefix_str + line for line in lines)

    def suffix(self, text: str, suffix_str: str) -> str:
        """Append ``suffix_str`` to each line."""
        if not text:
            return text
        lines = text.split("\n")
        return "\n".join(line + suffix_str for line in lines)

    def strip(self, text: str) -> str:
        """Strip whitespace from every line."""
        if not text:
            return text
        lines = text.split("\n")
        return "\n".join(line.strip() for line in lines)

    def wrap(self, text: str, before: str, after: str) -> str:
        """Wrap the whole text with ``before`` and ``after``."""
        return f"{before}{text}{after}"

    def indent(self, text: str, spaces: int = 2) -> str:
        """Indent every line by ``spaces`` spaces."""
        if not text:
            return text
        pad = " " * spaces
        lines = text.split("\n")
        return "\n".join(pad + line for line in lines)

    def dedent(self, text: str) -> str:
        """Remove the common leading whitespace from all lines."""
        return textwrap.dedent(text)

    # ------------------------------------------------------------------
    # Dispatch
    # ------------------------------------------------------------------

    def apply(self, text: str, transform: Transform) -> str:
        """Apply a single transform (ignoring any condition)."""
        op = transform.op
        params = transform.params or {}

        if op == TransformOp.UPPERCASE:
            return self.uppercase(text)
        if op == TransformOp.LOWERCASE:
            return self.lowercase(text)
        if op == TransformOp.TITLE_CASE:
            return self.title_case(text)
        if op == TransformOp.SENTENCE_CASE:
            return self.sentence_case(text)
        if op == TransformOp.REVERSE:
            return self.reverse(text)
        if op == TransformOp.REDACT:
            pattern = params.get("pattern", "")
            replacement = params.get("replacement", "[REDACTED]")
            return self.redact(text, pattern, replacement)
        if op == TransformOp.REPLACE:
            old = params.get("old", "")
            new = params.get("new", "")
            regex = bool(params.get("regex", False))
            return self.replace(text, old, new, regex=regex)
        if op == TransformOp.EXTRACT:
            pattern = params.get("pattern", "")
            matches = self.extract(text, pattern)
            # For pipeline-compatible signature, join with newline.
            return "\n".join(matches)
        if op == TransformOp.PREFIX:
            prefix_str = params.get("prefix", "")
            return self.prefix(text, prefix_str)
        if op == TransformOp.SUFFIX:
            suffix_str = params.get("suffix", "")
            return self.suffix(text, suffix_str)
        if op == TransformOp.STRIP:
            return self.strip(text)
        if op == TransformOp.WRAP:
            before = params.get("before", "")
            after = params.get("after", "")
            return self.wrap(text, before, after)
        if op == TransformOp.INDENT:
            spaces = int(params.get("spaces", 2))
            return self.indent(text, spaces)
        if op == TransformOp.DEDENT:
            return self.dedent(text)

        raise ValueError(f"Unknown transform op: {op!r}")

    # ------------------------------------------------------------------
    # Pipeline / batch
    # ------------------------------------------------------------------

    def apply_pipeline(
        self, text: str, transforms: list
    ) -> TransformResult:
        """Apply a list of transforms in order, returning the full result."""
        original = text
        current = text
        applied: list = []

        for transform in transforms:
            if transform.condition is not None:
                if not re.search(transform.condition, current):
                    continue
            current = self.apply(current, transform)
            applied.append(transform.op)

        return TransformResult(
            original=original, transformed=current, applied=applied
        )

    def apply_batch(
        self, texts: list, transforms: list
    ) -> list:
        """Apply the same pipeline to a list of texts."""
        return [self.apply_pipeline(t, transforms) for t in texts]
