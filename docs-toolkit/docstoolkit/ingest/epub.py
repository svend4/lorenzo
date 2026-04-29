"""EPUB (.epub) → markdown.

Опционально: использует ebooklib если установлен.
"""
from pathlib import Path

try:
    import ebooklib
    from ebooklib import epub
except ImportError:
    raise ImportError("Для ингестии EPUB установите: pip install ebooklib")

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.ingest.html import _HtmlToMd


def ingest(path: Path) -> Document:
    try:
        book = epub.read_epub(str(path))
    except Exception as e:
        raise IngestError(f"EPUB parse error: {e}")

    title = book.title or path.stem
    authors = []
    for k, v in book.metadata.get("http://purl.org/dc/elements/1.1/", {}).items():
        if k == "creator":
            authors = [item[0] for item in v]
            break

    parts: list[str] = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            html = item.get_content().decode("utf-8", errors="replace")
            parser = _HtmlToMd()
            try:
                parser.feed(html)
                md = parser.get_markdown()
                if md:
                    parts.append(md)
            except Exception:
                continue

    if not parts:
        raise IngestError("EPUB: не извлечено контента")

    content = "\n\n---\n\n".join(parts)

    return Document(
        title=title,
        content=content,
        source=Source.from_path(path, "epub"),
        metadata={
            "authors": authors,
            "chapters": len(parts),
        },
    )
