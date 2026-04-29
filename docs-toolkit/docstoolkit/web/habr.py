"""Habr.com ingest — статьи через парсинг HTML.

У Habr нет публичного API для получения статьи, поэтому используем HTML.
"""
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.ingest.html import _HtmlToMd
from docstoolkit.web.url import _fetch


def _extract_habr_id(url_or_id: str) -> str:
    """'https://habr.com/ru/articles/123456/' или '123456' → '123456'."""
    if url_or_id.isdigit():
        return url_or_id
    m = re.search(r'/(?:articles|post)/(\d+)/?', url_or_id)
    if m:
        return m.group(1)
    raise IngestError(f"Не удалось извлечь Habr article ID из {url_or_id}")


def fetch_habr(url_or_id: str) -> Document:
    """Скачивает Habr-статью.

    Принимает URL или просто article ID.
    """
    article_id = _extract_habr_id(url_or_id)
    url = f"https://habr.com/ru/articles/{article_id}/"

    html = _fetch(url)

    # Извлечь основной article контент
    article_match = re.search(
        r'<article[^>]*>(.*?)</article>', html, re.DOTALL
    )
    if article_match:
        content_html = article_match.group(1)
    else:
        # Fallback на весь body
        content_html = html

    # Title
    title_match = re.search(r'<title>(.*?)</title>', html, re.DOTALL)
    title = (title_match.group(1) if title_match else f"Habr article {article_id}").strip()
    title = re.sub(r'\s*/\s*Хабр.*$', '', title)
    title = re.sub(r'\s+', ' ', title)

    parser = _HtmlToMd()
    parser.feed(content_html)
    md = parser.get_markdown()

    if not md:
        raise IngestError(f"Habr: пустой контент для {url}")

    return Document(
        title=title,
        content=md,
        source=Source(
            path=Path(f"habr:{article_id}"),
            format="habr",
            size_bytes=len(html),
            mtime=datetime.now(),
        ),
        metadata={
            "habr_id": article_id,
            "url": url,
            "fetched_at": datetime.now().isoformat(timespec='seconds'),
        },
    )
