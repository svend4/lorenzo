"""Markdown (.md) — pass-through с извлечением заголовка."""
import re
from pathlib import Path

from docstoolkit.ingest.base import Document, Source


def ingest(path: Path) -> Document:
    text = path.read_text(encoding="utf-8")
    title = _extract_title(text) or path.stem

    sections = []
    for m in re.finditer(r'^(#{1,6})\s+(.+?)\s*$', text, re.MULTILINE):
        sections.append({"heading": m.group(2), "level": len(m.group(1))})

    return Document(
        title=title,
        content=text,
        source=Source.from_path(path, "markdown"),
        metadata={"section_count": len(sections)},
        sections=sections,
    )


def _extract_title(text: str) -> str | None:
    m = re.search(r'^#\s+(.+?)\s*$', text, re.MULTILINE)
    return m.group(1) if m else None
