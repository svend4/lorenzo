"""Markdown renderer — convert structured data into markdown text.

Pure stdlib. Provides primitives for common markdown constructs as well as a
``render_document`` helper that walks a list of typed blocks.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

@dataclass
class RenderConfig:
    """Configuration for :class:`MarkdownRenderer`.

    Attributes:
        heading_style: ``"atx"`` (``# H1``) or ``"setext"`` (underline).
        list_marker: One of ``-``, ``*``, ``+``.
        numbered_marker: Suffix for numbered list items (typically ``.``).
        table_alignment: Mapping ``column_name -> "left"|"right"|"center"``.
        bold_marker: Marker pair for bold spans.
        italic_marker: Marker pair for italic spans.
        code_fence: Fence sequence for code blocks.
    """

    heading_style: str = "atx"
    list_marker: str = "-"
    numbered_marker: str = "."
    table_alignment: dict[str, str] = field(default_factory=dict)
    bold_marker: str = "**"
    italic_marker: str = "*"
    code_fence: str = "```"


# ---------------------------------------------------------------------------
# Renderer
# ---------------------------------------------------------------------------

class MarkdownRenderer:
    """Render markdown primitives from structured data."""

    def __init__(self, config: RenderConfig | None = None) -> None:
        self.config = config if config is not None else RenderConfig()

    # ----- inline ----------------------------------------------------------

    def bold(self, text: str) -> str:
        m = self.config.bold_marker
        return f"{m}{text}{m}"

    def italic(self, text: str) -> str:
        m = self.config.italic_marker
        return f"{m}{text}{m}"

    def code(self, text: str) -> str:
        # Pick a backtick run that doesn't collide with the content.
        if "`" not in text:
            return f"`{text}`"
        # Find the longest backtick run inside text and use one more.
        max_run = 0
        current = 0
        for ch in text:
            if ch == "`":
                current += 1
                if current > max_run:
                    max_run = current
            else:
                current = 0
        fence = "`" * (max_run + 1)
        # Add padding spaces so adjacent backticks don't merge.
        return f"{fence} {text} {fence}"

    def link(self, text: str, url: str, title: str = "") -> str:
        if title:
            return f'[{text}]({url} "{title}")'
        return f"[{text}]({url})"

    def image(self, alt: str, url: str, title: str = "") -> str:
        if title:
            return f'![{alt}]({url} "{title}")'
        return f"![{alt}]({url})"

    # ----- block ----------------------------------------------------------

    def heading(self, text: str, level: int = 1) -> str:
        if level < 1 or level > 6:
            raise ValueError(f"heading level must be in 1..6, got {level}")
        style = self.config.heading_style
        if style == "setext" and level in (1, 2):
            underline_char = "=" if level == 1 else "-"
            underline = underline_char * max(len(text), 3)
            return f"{text}\n{underline}\n"
        # default: ATX (setext also falls back to ATX for levels 3-6)
        return f"{'#' * level} {text}\n"

    def paragraph(self, text: str) -> str:
        return f"{text}\n"

    def code_block(self, text: str, language: str = "") -> str:
        fence = self.config.code_fence
        body = text
        if body and not body.endswith("\n"):
            body += "\n"
        return f"{fence}{language}\n{body}{fence}\n"

    def blockquote(self, text: str) -> str:
        if text == "":
            return ">\n"
        lines = text.split("\n")
        prefixed = []
        for line in lines:
            if line == "":
                prefixed.append(">")
            else:
                prefixed.append(f"> {line}")
        return "\n".join(prefixed) + "\n"

    def horizontal_rule(self) -> str:
        return "---\n"

    # ----- lists ----------------------------------------------------------

    def list(self, items: list[str], ordered: bool = False) -> str:  # noqa: A003
        if not items:
            return ""
        out: list[str] = []
        if ordered:
            for i, item in enumerate(items, 1):
                out.append(f"{i}{self.config.numbered_marker} {item}")
        else:
            marker = self.config.list_marker
            for item in items:
                out.append(f"{marker} {item}")
        return "\n".join(out) + "\n"

    def nested_list(self, items: list, indent_level: int = 0) -> str:
        """Render a (possibly nested) list.

        ``items`` is a list whose elements are either strings (leaf items) or
        nested ``list`` instances. A nested list belongs to the previous string
        leaf and is indented by two extra spaces per level.
        """
        if not items:
            return ""
        marker = self.config.list_marker
        indent = "  " * indent_level
        out: list[str] = []
        for item in items:
            if isinstance(item, list):
                nested = self.nested_list(item, indent_level + 1)
                if nested:
                    # Strip trailing newline so caller can manage line joins.
                    out.append(nested.rstrip("\n"))
            else:
                out.append(f"{indent}{marker} {item}")
        return "\n".join(out) + "\n"

    # ----- tables ---------------------------------------------------------

    def table(self, headers: list[str], rows: list[list[str]]) -> str:
        if not headers:
            return ""
        # Normalize rows length to headers length.
        norm_rows: list[list[str]] = []
        for row in rows:
            r = list(row)
            if len(r) < len(headers):
                r = r + [""] * (len(headers) - len(r))
            elif len(r) > len(headers):
                r = r[: len(headers)]
            norm_rows.append([str(c) for c in r])
        # Column widths.
        widths = [len(str(h)) for h in headers]
        for row in norm_rows:
            for i, cell in enumerate(row):
                if len(cell) > widths[i]:
                    widths[i] = len(cell)
        # Minimum width 3 to host alignment markers ``---`` / ``:--`` etc.
        widths = [max(w, 3) for w in widths]

        def fmt_cell(cell: str, w: int, align: str) -> str:
            if align == "right":
                return cell.rjust(w)
            if align == "center":
                # Center within width.
                total_pad = w - len(cell)
                left = total_pad // 2
                right = total_pad - left
                return " " * left + cell + " " * right
            return cell.ljust(w)

        # Build header row.
        aligns: list[str] = []
        for h in headers:
            aligns.append(self.config.table_alignment.get(h, "left"))

        header_line = (
            "| "
            + " | ".join(fmt_cell(str(h), widths[i], aligns[i]) for i, h in enumerate(headers))
            + " |"
        )

        # Separator with alignment markers.
        sep_parts: list[str] = []
        for w, align in zip(widths, aligns):
            if align == "center":
                seg = ":" + "-" * (w - 2) + ":"
            elif align == "right":
                seg = "-" * (w - 1) + ":"
            elif align == "left" and any(a != "left" for a in aligns):
                # If any alignment in the table is non-default, write the
                # explicit left marker so the table is unambiguous.
                seg = ":" + "-" * (w - 1)
            else:
                seg = "-" * w
            sep_parts.append(seg)
        separator = "|" + "|".join(f"{p}" for p in sep_parts) + "|"
        # Pad separator segments with surrounding spaces only if no alignment
        # is set anywhere in the table (purely cosmetic for the simple case).
        if not self.config.table_alignment:
            separator = (
                "|" + "|".join("-" * (w + 2) for w in widths) + "|"
            )

        lines = [header_line, separator]
        for row in norm_rows:
            line = (
                "| "
                + " | ".join(fmt_cell(cell, widths[i], aligns[i]) for i, cell in enumerate(row))
                + " |"
            )
            lines.append(line)
        return "\n".join(lines) + "\n"

    # ----- task / definition lists ---------------------------------------

    def task_list(self, items: list[tuple[str, bool]]) -> str:
        if not items:
            return ""
        marker = self.config.list_marker
        out: list[str] = []
        for text, checked in items:
            box = "[x]" if checked else "[ ]"
            out.append(f"{marker} {box} {text}")
        return "\n".join(out) + "\n"

    def definition_list(self, items: list[tuple[str, str]]) -> str:
        if not items:
            return ""
        out: list[str] = []
        for term, definition in items:
            out.append(f"{term}\n: {definition}")
        return "\n\n".join(out) + "\n"

    # ----- document ------------------------------------------------------

    def render_document(self, blocks: list[dict[str, Any]]) -> str:
        """Walk a list of typed blocks and produce a single markdown string.

        Each block is a dict with a ``type`` key. Recognised types:

        - ``heading``: ``{"type": "heading", "level": 1, "text": "..."}``
        - ``paragraph``: ``{"type": "paragraph", "text": "..."}``
        - ``code_block``: ``{"type": "code_block", "text": "...", "language": "py"}``
        - ``list``: ``{"type": "list", "items": [...], "ordered": False}``
        - ``nested_list``: ``{"type": "nested_list", "items": [...]}``
        - ``table``: ``{"type": "table", "headers": [...], "rows": [[...], ...]}``
        - ``blockquote``: ``{"type": "blockquote", "text": "..."}``
        - ``horizontal_rule``: ``{"type": "horizontal_rule"}``
        - ``task_list``: ``{"type": "task_list", "items": [(t, b), ...]}``
        - ``definition_list``: ``{"type": "definition_list", "items": [(k, v), ...]}``
        """
        parts: list[str] = []
        for block in blocks:
            btype = block.get("type")
            if btype == "heading":
                parts.append(self.heading(block["text"], block.get("level", 1)))
            elif btype == "paragraph":
                parts.append(self.paragraph(block["text"]))
            elif btype == "code_block":
                parts.append(
                    self.code_block(block["text"], block.get("language", ""))
                )
            elif btype == "list":
                parts.append(self.list(block["items"], block.get("ordered", False)))
            elif btype == "nested_list":
                parts.append(self.nested_list(block["items"]))
            elif btype == "table":
                parts.append(self.table(block["headers"], block.get("rows", [])))
            elif btype == "blockquote":
                parts.append(self.blockquote(block["text"]))
            elif btype == "horizontal_rule":
                parts.append(self.horizontal_rule())
            elif btype == "task_list":
                parts.append(self.task_list(block["items"]))
            elif btype == "definition_list":
                parts.append(self.definition_list(block["items"]))
            else:
                raise ValueError(f"unknown block type: {btype!r}")
        return "\n".join(parts)
