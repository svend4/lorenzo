"""Confluence ingest — REST API + Confluence Storage Format.

Опционально: atlassian-python-api для Cloud / Server.
"""
import re
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path_or_id: str | Path) -> Document:
    """Принимает:
      - Путь к экспортированному XML (Confluence Storage Format)
      - URL https://your-instance.atlassian.net/wiki/spaces/.../pages/12345
      - Page ID (digits only)
    """
    s = str(path_or_id)
    p = Path(s)
    if p.exists() and p.suffix in (".xml", ".html"):
        return _ingest_storage_format(p)

    try:
        from atlassian import Confluence
        import os
    except ImportError:
        raise ImportError("Для Confluence API: pip install atlassian-python-api")

    base_url = os.environ.get("CONFLUENCE_URL")
    token = os.environ.get("CONFLUENCE_TOKEN")
    user = os.environ.get("CONFLUENCE_USER")
    if not (base_url and token):
        raise IngestError("CONFLUENCE_URL + CONFLUENCE_TOKEN env vars нужны")

    page_id = _extract_page_id(s)
    if not page_id:
        raise IngestError(f"Не удалось извлечь page_id из {s}")

    conf = Confluence(url=base_url, username=user, password=token, cloud=True)
    page = conf.get_page_by_id(page_id, expand="body.storage")
    if not page:
        raise IngestError(f"Confluence page {page_id} не найдена")

    storage = page.get("body", {}).get("storage", {}).get("value", "")
    md = _storage_to_md(storage)

    return Document(
        title=page.get("title", page_id),
        content=md,
        source=Source(
            path=Path(f"confluence:{page_id}"),
            format="confluence",
            size_bytes=len(md),
            mtime=datetime.now(),
        ),
        metadata={
            "confluence_id": page_id,
            "url": page.get("_links", {}).get("webui", ""),
            "version": page.get("version", {}).get("number", 0),
        },
    )


def _ingest_storage_format(path: Path) -> Document:
    """Конверт Confluence Storage Format (XML-like) → markdown."""
    text = path.read_text(encoding="utf-8")
    md = _storage_to_md(text)
    if not md:
        raise IngestError(f"{path}: пустой результат")

    title_m = re.search(r'<title>(.*?)</title>', text)
    title = title_m.group(1).strip() if title_m else path.stem

    return Document(
        title=title,
        content=md,
        source=Source.from_path(path, "confluence"),
        metadata={"original_size": len(text)},
    )


def _extract_page_id(s: str) -> str:
    if s.isdigit():
        return s
    m = re.search(r'/pages/(\d+)', s)
    if m:
        return m.group(1)
    m = re.search(r'pageId=(\d+)', s)
    if m:
        return m.group(1)
    return ""


def _storage_to_md(storage: str) -> str:
    """Минимальный конверт CSF → markdown.

    Поддержка: h1-h6, p, ul/ol, code, strong/em, a, hr.
    """
    text = storage
    # Заголовки
    for level in range(1, 7):
        text = re.sub(rf'<h{level}[^>]*>(.*?)</h{level}>',
                       lambda m, lvl=level: f"\n{'#' * lvl} {m.group(1).strip()}\n",
                       text, flags=re.DOTALL | re.IGNORECASE)
    # Параграфы
    text = re.sub(r'<p[^>]*>(.*?)</p>',
                   lambda m: f"\n{m.group(1).strip()}\n",
                   text, flags=re.DOTALL | re.IGNORECASE)
    # Списки
    text = re.sub(r'<li[^>]*>(.*?)</li>',
                   lambda m: f"- {m.group(1).strip()}\n",
                   text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'</?(ul|ol)[^>]*>', '', text, flags=re.IGNORECASE)
    # Inline
    text = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', text,
                   flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', text,
                   flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text,
                   flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', r'[\2](\1)', text,
                   flags=re.DOTALL | re.IGNORECASE)
    # Code blocks (ac:structured-macro для confluence)
    text = re.sub(r'<ac:plain-text-body><!\[CDATA\[(.+?)\]\]></ac:plain-text-body>',
                   lambda m: f"\n```\n{m.group(1)}\n```\n",
                   text, flags=re.DOTALL)
    # HR
    text = re.sub(r'<hr\s*/?>', '\n---\n', text, flags=re.IGNORECASE)
    # Strip всё остальное
    text = re.sub(r'<[^>]+>', '', text)
    # HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    text = text.replace("&quot;", '"').replace("&nbsp;", " ")
    # Cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()
