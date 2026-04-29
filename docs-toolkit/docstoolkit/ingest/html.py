"""HTML (.html, .htm) → markdown."""
import re
from html.parser import HTMLParser
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


class _HtmlToMd(HTMLParser):
    """Минимальный HTML→Markdown без зависимостей.
    Поддерживает: h1-h6, p, ul/ol/li, code, pre, a, strong/b, em/i, br, hr."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.title: str = ""
        self.in_title = False
        self.in_script = False
        self.in_style = False
        self.in_code = 0
        self.in_pre = 0
        self.list_stack: list[tuple[str, int]] = []  # [(type, counter)]
        self.skip_chars = False
        self.href: str = ""
        self.in_anchor = False
        self.anchor_text: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            self.in_script = True
        elif tag == "style":
            self.in_style = True
        elif tag == "title":
            self.in_title = True
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.parts.append("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self.parts.append("\n\n")
        elif tag == "br":
            self.parts.append("  \n")
        elif tag == "hr":
            self.parts.append("\n\n---\n\n")
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "code":
            if not self.in_pre:
                self.parts.append("`")
                self.in_code += 1
        elif tag == "pre":
            self.parts.append("\n\n```\n")
            self.in_pre += 1
        elif tag == "ul":
            self.list_stack.append(("ul", 0))
        elif tag == "ol":
            self.list_stack.append(("ol", 0))
        elif tag == "li":
            if self.list_stack:
                kind, n = self.list_stack[-1]
                indent = "  " * (len(self.list_stack) - 1)
                if kind == "ol":
                    self.list_stack[-1] = (kind, n + 1)
                    self.parts.append(f"\n{indent}{n + 1}. ")
                else:
                    self.parts.append(f"\n{indent}- ")
        elif tag == "a":
            href = dict(attrs).get("href", "")
            self.href = href
            self.in_anchor = True
            self.anchor_text = []

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        elif tag == "style":
            self.in_style = False
        elif tag == "title":
            self.in_title = False
        elif tag in ("strong", "b"):
            self.parts.append("**")
        elif tag in ("em", "i"):
            self.parts.append("*")
        elif tag == "code" and self.in_code:
            self.parts.append("`")
            self.in_code -= 1
        elif tag == "pre":
            self.parts.append("\n```\n")
            self.in_pre -= 1
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
        elif tag == "a" and self.in_anchor:
            text = "".join(self.anchor_text).strip()
            self.in_anchor = False
            if self.href and text:
                self.parts.append(f"[{text}]({self.href})")
            else:
                self.parts.append(text)
            self.href = ""
            self.anchor_text = []

    def handle_data(self, data):
        if self.in_script or self.in_style:
            return
        if self.in_title:
            self.title += data
            return
        if self.in_anchor:
            self.anchor_text.append(data)
        else:
            self.parts.append(data)

    def get_markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r'\n{4,}', '\n\n\n', text)
        text = re.sub(r' +', ' ', text)
        return text.strip()


def ingest(path: Path) -> Document:
    text = path.read_text(encoding="utf-8", errors="replace")
    parser = _HtmlToMd()
    try:
        parser.feed(text)
    except Exception as e:
        raise IngestError(f"HTML parse error: {e}")
    md = parser.get_markdown()
    if not md:
        raise IngestError("HTML: пустой результат после конвертации")
    title = parser.title.strip() or path.stem

    return Document(
        title=title,
        content=md,
        source=Source.from_path(path, "html"),
        metadata={"original_size": len(text)},
    )
