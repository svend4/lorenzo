"""Базовый HTTP fetcher → markdown.

Использует urllib (stdlib) + html-плагин из ingest/.
"""
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.ingest.html import _HtmlToMd


USER_AGENT = "docstoolkit/0.1 (+https://github.com/svend4/lorenzo)"
TIMEOUT_SEC = 30


def _fetch(url: str, timeout: int = TIMEOUT_SEC) -> str:
    """HTTP GET с User-Agent и таймаутом."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return data.decode(charset, errors="replace")
    except Exception as e:
        raise IngestError(f"HTTP fetch error для {url}: {e}")


def fetch_url(url: str, *, title_hint: str = "") -> Document:
    """Скачивает URL и конвертирует в markdown.

    Создаёт Document с метаданными о источнике.
    """
    if not url.startswith(("http://", "https://")):
        raise IngestError(f"Поддерживаются только http(s):// URL, получено {url}")

    html = _fetch(url)
    parser = _HtmlToMd()
    try:
        parser.feed(html)
    except Exception as e:
        raise IngestError(f"HTML parse error: {e}")

    md = parser.get_markdown()
    if not md:
        raise IngestError(f"Пустой результат для {url}")

    title = parser.title.strip() or title_hint or url

    # Source с фиктивным path (URL как identifier)
    source = Source(
        path=Path(url),
        format="url",
        size_bytes=len(html),
        mtime=datetime.now(),
    )

    return Document(
        title=title,
        content=md,
        source=source,
        metadata={
            "url": url,
            "html_size": len(html),
            "fetched_at": datetime.now().isoformat(timespec='seconds'),
        },
    )
