"""MHTML (Web Archive) → markdown.

Используется для Claude.ai / ChatGPT экспортов в MHTML-формате.
Извлекает text/html часть и конвертирует через html-плагин.
"""
import email
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.ingest.html import _HtmlToMd


def ingest(path: Path) -> Document:
    with open(path, "rb") as f:
        msg = email.message_from_binary_file(f)

    html = None
    title_hint = ""
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            payload = part.get_payload(decode=True)
            if payload:
                html = payload.decode("utf-8", errors="replace")
                # Subject MHTML может содержать оригинальный URL/title
                title_hint = msg.get("Subject", "")
                break

    if not html:
        raise IngestError("MHTML: не найдено text/html part")

    parser = _HtmlToMd()
    try:
        parser.feed(html)
    except Exception as e:
        raise IngestError(f"MHTML html parse error: {e}")

    md = parser.get_markdown()
    if not md:
        raise IngestError("MHTML: пустой результат после конвертации")

    title = parser.title.strip() or title_hint.strip() or path.stem

    return Document(
        title=title,
        content=md,
        source=Source.from_path(path, "mhtml"),
        metadata={"subject": title_hint, "html_size": len(html)},
    )
