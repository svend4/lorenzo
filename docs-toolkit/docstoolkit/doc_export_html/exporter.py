"""E241 Markdown-to-HTML converter (stdlib-only).

Implements a small but practical subset of CommonMark-style markdown,
suitable for documentation rendering inside docs-toolkit.
"""
from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration and result types
# ---------------------------------------------------------------------------


@dataclass
class HtmlConfig:
    """Configuration for :class:`DocExportHtml`."""

    include_toc: bool = False
    wrap_in_html: bool = True  # full <html><body>...</body></html>
    css_class_prefix: str = "md-"
    link_target_blank: bool = False
    escape_html: bool = True  # escape inline HTML in source
    code_language_class: bool = True  # add language-X class to code blocks
    min_heading_for_toc: int = 1
    max_heading_for_toc: int = 3


@dataclass
class HtmlOutput:
    """Result of a single :meth:`DocExportHtml.convert` call."""

    html: str
    toc: Optional[str] = None
    heading_count: int = 0
    link_count: int = 0


# ---------------------------------------------------------------------------
# Main exporter
# ---------------------------------------------------------------------------


_HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_FENCE_RE = re.compile(r"^```\s*([\w+\-.]*)\s*$")
_UL_RE = re.compile(r"^([ \t]*)[-*+]\s+(.*)$")
_OL_RE = re.compile(r"^([ \t]*)(\d+)\.\s+(.*)$")
_BQ_RE = re.compile(r"^>\s?(.*)$")
_TABLE_SEP_RE = re.compile(r"^\s*\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$")


class DocExportHtml:
    """Convert markdown source to HTML using only the Python standard library."""

    def __init__(self, config: Optional[HtmlConfig] = None) -> None:
        self.config = config if config is not None else HtmlConfig()
        # populated during convert() for counters
        self._heading_count = 0
        self._link_count = 0
        self._slug_seen: dict = {}

    # ------------------------------------------------------------------
    # Public top-level conversion
    # ------------------------------------------------------------------

    def convert(self, markdown: str) -> HtmlOutput:
        """Convert ``markdown`` to HTML, returning a :class:`HtmlOutput`."""
        self._heading_count = 0
        self._link_count = 0
        self._slug_seen = {}

        # Build TOC first (on the raw markdown), before code-block extraction
        # so headings inside code fences don't appear in TOC.
        toc_html: Optional[str] = None
        if self.config.include_toc:
            toc_html = self.build_toc(markdown)

        body = self._render_blocks(markdown)

        if self.config.wrap_in_html:
            full = (
                "<!DOCTYPE html>\n"
                "<html>\n<head>\n"
                "<meta charset=\"utf-8\">\n"
                "</head>\n<body>\n"
            )
            if toc_html:
                full += toc_html + "\n"
            full += body
            full += "\n</body>\n</html>"
            out_html = full
        else:
            out_html = body
            if toc_html:
                out_html = toc_html + "\n" + body

        return HtmlOutput(
            html=out_html,
            toc=toc_html,
            heading_count=self._heading_count,
            link_count=self._link_count,
        )

    # ------------------------------------------------------------------
    # Block-level rendering pipeline
    # ------------------------------------------------------------------

    def _render_blocks(self, markdown: str) -> str:
        # Normalise line endings.
        text = markdown.replace("\r\n", "\n").replace("\r", "\n")

        # Extract fenced code blocks first so their content is not
        # interpreted as markdown.
        text, codes = self._extract_code_blocks(text)

        # Split into block groups separated by blank lines.
        lines = text.split("\n")
        blocks: List[List[str]] = []
        current: List[str] = []
        for line in lines:
            if line.strip() == "":
                if current:
                    blocks.append(current)
                    current = []
            else:
                current.append(line)
        if current:
            blocks.append(current)

        rendered: List[str] = []
        for block in blocks:
            rendered.append(self._render_block(block))

        result = "\n".join(b for b in rendered if b)

        # Re-insert code blocks.
        for i, code_html in enumerate(codes):
            placeholder = f"\x00CODEBLOCK{i}\x00"
            result = result.replace(f"<p>{placeholder}</p>", code_html)
            result = result.replace(placeholder, code_html)
        return result

    def _render_block(self, lines: List[str]) -> str:
        # Heading?
        if len(lines) == 1 and _HEADING_RE.match(lines[0]):
            return self._render_heading_line(lines[0])

        # Blockquote?
        if all(_BQ_RE.match(ln) or ln.strip() == "" for ln in lines):
            return self._render_blockquote_block(lines)

        # Table?
        if len(lines) >= 2 and "|" in lines[0] and _TABLE_SEP_RE.match(lines[1]):
            return self._render_table_block(lines)

        # List?
        if _UL_RE.match(lines[0]) or _OL_RE.match(lines[0]):
            return self._render_list_block(lines)

        # Otherwise paragraph.
        joined = " ".join(line.strip() for line in lines)
        return f"<p>{self.convert_inline(joined)}</p>"

    # ------------------------------------------------------------------
    # Code blocks
    # ------------------------------------------------------------------

    def _extract_code_blocks(self, text: str) -> Tuple[str, List[str]]:
        lines = text.split("\n")
        out_lines: List[str] = []
        codes: List[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            m = _FENCE_RE.match(line)
            if m:
                lang = m.group(1) or ""
                buf: List[str] = []
                i += 1
                while i < len(lines) and not _FENCE_RE.match(lines[i]):
                    buf.append(lines[i])
                    i += 1
                # consume closing fence (if present)
                if i < len(lines):
                    i += 1
                code_text = "\n".join(buf)
                escaped = html.escape(code_text)
                if lang and self.config.code_language_class:
                    code_html = (
                        f'<pre><code class="language-{html.escape(lang)}">'
                        f"{escaped}</code></pre>"
                    )
                else:
                    code_html = f"<pre><code>{escaped}</code></pre>"
                placeholder = f"\x00CODEBLOCK{len(codes)}\x00"
                codes.append(code_html)
                out_lines.append(placeholder)
            else:
                out_lines.append(line)
                i += 1
        return "\n".join(out_lines), codes

    def convert_code_blocks(self, text: str) -> str:
        """Public API: convert fenced code blocks in ``text``."""
        replaced, codes = self._extract_code_blocks(text)
        for i, code_html in enumerate(codes):
            placeholder = f"\x00CODEBLOCK{i}\x00"
            replaced = replaced.replace(placeholder, code_html)
        return replaced

    # ------------------------------------------------------------------
    # Headings
    # ------------------------------------------------------------------

    def _render_heading_line(self, line: str) -> str:
        m = _HEADING_RE.match(line)
        if not m:
            return f"<p>{self.convert_inline(line)}</p>"
        level = len(m.group(1))
        raw_text = m.group(2).strip()
        slug = self.to_slug(raw_text)
        inline = self.convert_inline(raw_text)
        self._heading_count += 1
        return f'<h{level} id="{slug}">{inline}</h{level}>'

    def convert_headings(self, text: str) -> str:
        """Convert ATX-style headings in ``text``."""
        out: List[str] = []
        for line in text.replace("\r\n", "\n").split("\n"):
            if _HEADING_RE.match(line):
                out.append(self._render_heading_line(line))
            else:
                out.append(line)
        return "\n".join(out)

    # ------------------------------------------------------------------
    # Paragraphs
    # ------------------------------------------------------------------

    def convert_paragraphs(self, text: str) -> str:
        """Wrap blank-line-separated text blocks as ``<p>`` paragraphs."""
        text = text.replace("\r\n", "\n")
        parts = re.split(r"\n\s*\n", text.strip())
        rendered: List[str] = []
        for part in parts:
            if not part.strip():
                continue
            joined = " ".join(line.strip() for line in part.split("\n"))
            rendered.append(f"<p>{self.convert_inline(joined)}</p>")
        return "\n".join(rendered)

    # ------------------------------------------------------------------
    # Lists
    # ------------------------------------------------------------------

    def _render_list_block(self, lines: List[str]) -> str:
        ordered = bool(_OL_RE.match(lines[0]))
        tag = "ol" if ordered else "ul"
        items: List[str] = []
        for ln in lines:
            m_ul = _UL_RE.match(ln)
            m_ol = _OL_RE.match(ln)
            if m_ol:
                items.append(m_ol.group(3))
            elif m_ul:
                items.append(m_ul.group(2))
            else:
                # continuation appended to previous item
                if items:
                    items[-1] = items[-1] + " " + ln.strip()
        rendered_items = "".join(
            f"<li>{self.convert_inline(item)}</li>" for item in items
        )
        return f"<{tag}>{rendered_items}</{tag}>"

    def convert_lists(self, text: str) -> str:
        """Convert ``-`` / ``1.`` lists in ``text`` to ``<ul>`` / ``<ol>``."""
        text = text.replace("\r\n", "\n")
        lines = text.split("\n")
        out: List[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if _UL_RE.match(line) or _OL_RE.match(line):
                buf: List[str] = []
                while i < len(lines) and (
                    _UL_RE.match(lines[i]) or _OL_RE.match(lines[i])
                ):
                    buf.append(lines[i])
                    i += 1
                out.append(self._render_list_block(buf))
            else:
                out.append(line)
                i += 1
        return "\n".join(out)

    # ------------------------------------------------------------------
    # Blockquotes
    # ------------------------------------------------------------------

    def _render_blockquote_block(self, lines: List[str]) -> str:
        contents: List[str] = []
        for ln in lines:
            if not ln.strip():
                continue
            m = _BQ_RE.match(ln)
            if m:
                contents.append(m.group(1))
            else:
                contents.append(ln)
        joined = " ".join(contents).strip()
        return f"<blockquote>{self.convert_inline(joined)}</blockquote>"

    def convert_blockquotes(self, text: str) -> str:
        """Convert ``> ...`` lines to ``<blockquote>`` elements."""
        text = text.replace("\r\n", "\n")
        lines = text.split("\n")
        out: List[str] = []
        i = 0
        while i < len(lines):
            if _BQ_RE.match(lines[i]):
                buf: List[str] = []
                while i < len(lines) and _BQ_RE.match(lines[i]):
                    buf.append(lines[i])
                    i += 1
                out.append(self._render_blockquote_block(buf))
            else:
                out.append(lines[i])
                i += 1
        return "\n".join(out)

    # ------------------------------------------------------------------
    # Tables
    # ------------------------------------------------------------------

    @staticmethod
    def _split_table_row(row: str) -> List[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [cell.strip() for cell in row.split("|")]

    def _render_table_block(self, lines: List[str]) -> str:
        header = self._split_table_row(lines[0])
        body_rows = [self._split_table_row(ln) for ln in lines[2:] if ln.strip()]
        head_html = (
            "<thead><tr>"
            + "".join(f"<th>{self.convert_inline(c)}</th>" for c in header)
            + "</tr></thead>"
        )
        body_html_parts: List[str] = []
        for row in body_rows:
            body_html_parts.append(
                "<tr>"
                + "".join(f"<td>{self.convert_inline(c)}</td>" for c in row)
                + "</tr>"
            )
        body_html = "<tbody>" + "".join(body_html_parts) + "</tbody>"
        return f"<table>{head_html}{body_html}</table>"

    def convert_tables(self, text: str) -> str:
        """Convert markdown tables to ``<table>`` elements."""
        text = text.replace("\r\n", "\n")
        lines = text.split("\n")
        out: List[str] = []
        i = 0
        while i < len(lines):
            if (
                i + 1 < len(lines)
                and "|" in lines[i]
                and _TABLE_SEP_RE.match(lines[i + 1])
            ):
                buf = [lines[i], lines[i + 1]]
                j = i + 2
                while j < len(lines) and lines[j].strip() and "|" in lines[j]:
                    buf.append(lines[j])
                    j += 1
                out.append(self._render_table_block(buf))
                i = j
            else:
                out.append(lines[i])
                i += 1
        return "\n".join(out)

    # ------------------------------------------------------------------
    # Inline
    # ------------------------------------------------------------------

    def convert_inline(self, text: str) -> str:
        """Convert inline markdown (bold, italic, code, links) in ``text``."""
        # 1. Extract inline code spans first to protect them.
        code_spans: List[str] = []

        def _save_code(match: "re.Match[str]") -> str:
            code_spans.append(match.group(1))
            return f"\x00CODE{len(code_spans) - 1}\x00"

        text = re.sub(r"`([^`]+)`", _save_code, text)

        # 2. Escape HTML if configured.
        if self.config.escape_html:
            text = html.escape(text, quote=False)

        # 3. Links [text](url) — process before bold/italic so URL chars
        #    don't get parsed as emphasis.
        link_spans: List[str] = []

        def _save_link(match: "re.Match[str]") -> str:
            link_text = match.group(1)
            url = match.group(2)
            self._link_count += 1
            # link text may contain emphasis — process recursively-ish:
            inner = self._inline_emphasis(link_text)
            attrs = f'href="{html.escape(url, quote=True)}"'
            if self.config.link_target_blank:
                attrs += ' target="_blank"'
            rendered = f"<a {attrs}>{inner}</a>"
            link_spans.append(rendered)
            return f"\x00LINK{len(link_spans) - 1}\x00"

        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _save_link, text)

        # 4. Emphasis (bold + italic).
        text = self._inline_emphasis(text)

        # 5. Restore links.
        for i, span in enumerate(link_spans):
            text = text.replace(f"\x00LINK{i}\x00", span)

        # 6. Restore code spans (escape their contents).
        for i, span in enumerate(code_spans):
            text = text.replace(
                f"\x00CODE{i}\x00", f"<code>{html.escape(span)}</code>"
            )

        return text

    @staticmethod
    def _inline_emphasis(text: str) -> str:
        # Bold: **x** or __x__
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__([^_]+)__", r"<strong>\1</strong>", text)
        # Italic: *x* or _x_
        text = re.sub(r"(?<!\*)\*([^*\s][^*]*?)\*(?!\*)", r"<em>\1</em>", text)
        text = re.sub(r"(?<!_)_([^_\s][^_]*?)_(?!_)", r"<em>\1</em>", text)
        return text

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def escape(self, text: str) -> str:
        """Escape HTML-special characters in ``text``."""
        return html.escape(text)

    def to_slug(self, text: str) -> str:
        """Convert heading text to a URL-safe slug, ensuring uniqueness."""
        slug = text.strip().lower()
        slug = re.sub(r"[^\w\s\-а-яё]", "", slug, flags=re.UNICODE)
        slug = re.sub(r"[\s_]+", "-", slug)
        slug = slug.strip("-")
        if not slug:
            slug = "section"
        base = slug
        n = self._slug_seen.get(base, 0)
        if n:
            slug = f"{base}-{n}"
        self._slug_seen[base] = n + 1
        return slug

    # ------------------------------------------------------------------
    # TOC
    # ------------------------------------------------------------------

    def build_toc(self, text: str) -> str:
        """Generate a ``<nav>`` table-of-contents from headings in ``text``."""
        text = text.replace("\r\n", "\n")

        # Track which lines are inside fenced code blocks.
        headings: List[Tuple[int, str]] = []
        in_fence = False
        for line in text.split("\n"):
            if _FENCE_RE.match(line):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = _HEADING_RE.match(line)
            if m:
                level = len(m.group(1))
                if (
                    self.config.min_heading_for_toc
                    <= level
                    <= self.config.max_heading_for_toc
                ):
                    headings.append((level, m.group(2).strip()))

        if not headings:
            css_class = f"{self.config.css_class_prefix}toc"
            return f'<nav class="{css_class}"></nav>'

        # Slugs for TOC must match the slugs used in the rendered headings.
        # We reset the seen-state, generate slugs in document order; the
        # actual rendering uses the same algorithm so they will match.
        prev_state = dict(self._slug_seen)
        self._slug_seen = {}
        items_with_slugs = [
            (level, text_, self.to_slug(text_)) for level, text_ in headings
        ]
        self._slug_seen = prev_state

        # Build nested <ul> tree.
        css_class = f"{self.config.css_class_prefix}toc"
        out: List[str] = [f'<nav class="{css_class}">']
        prev_level: Optional[int] = None
        for level, text_, slug in items_with_slugs:
            if prev_level is None:
                # open as many <ul> as needed from base (min level)
                out.append("<ul>")
                for _ in range(level - items_with_slugs[0][0]):
                    out.append("<ul>")
            else:
                if level > prev_level:
                    for _ in range(level - prev_level):
                        out.append("<ul>")
                elif level < prev_level:
                    for _ in range(prev_level - level):
                        out.append("</li></ul>")
                    out.append("</li>")
                else:
                    out.append("</li>")
            out.append(f'<li><a href="#{slug}">{html.escape(text_)}</a>')
            prev_level = level
        # close all remaining lists
        if prev_level is not None:
            base = items_with_slugs[0][0]
            for _ in range(prev_level - base):
                out.append("</li></ul>")
            out.append("</li></ul>")
        out.append("</nav>")
        return "".join(out)
