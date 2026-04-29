"""PDF (.pdf) → markdown.

Опционально: использует pypdf если установлен.
Если нет — выбрасывает ImportError при загрузке плагина.
"""
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    try:
        from PyPDF2 import PdfReader  # старая версия
    except ImportError:
        raise ImportError("Для ингестии PDF установите: pip install pypdf")

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path: Path) -> Document:
    try:
        reader = PdfReader(str(path))
    except Exception as e:
        raise IngestError(f"PDF parse error: {e}")

    parts: list[str] = []
    title = ""

    if reader.metadata and reader.metadata.title:
        title = str(reader.metadata.title)

    for i, page in enumerate(reader.pages, 1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        text = text.strip()
        if text:
            parts.append(f"## Страница {i}\n\n{text}")

    if not parts:
        raise IngestError("PDF: не извлечён текст (возможно скан без OCR)")

    content = "\n\n".join(parts)
    if not title:
        # Первая значимая строка
        for line in content.splitlines():
            line = line.strip()
            if line and not line.startswith("##"):
                title = line[:200]
                break

    return Document(
        title=title or path.stem,
        content=content,
        source=Source.from_path(path, "pdf"),
        metadata={
            "page_count": len(reader.pages),
            "pdf_metadata": dict(reader.metadata or {}),
        },
    )
