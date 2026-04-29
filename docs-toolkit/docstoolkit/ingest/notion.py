"""Notion ingest — через REST API.

Опционально: использует notion-client если установлен.
Иначе можно работать с экспортированным ZIP (.md файлы внутри).
"""
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source


def ingest(path_or_id: str | Path) -> Document:
    """path_or_id может быть:
      - Notion page ID (32-hex или dashed UUID)
      - URL https://www.notion.so/...
      - Path к экспортированному .md из Notion ZIP
    """
    p = Path(str(path_or_id))
    if p.exists() and p.suffix == ".md":
        return _ingest_exported(p)

    # Иначе — API
    try:
        from notion_client import Client as NotionClient
        import os
    except ImportError:
        raise ImportError("Для Notion API: pip install notion-client")

    token = os.environ.get("NOTION_TOKEN")
    if not token:
        raise IngestError("NOTION_TOKEN env var требуется для API")

    page_id = _extract_page_id(str(path_or_id))
    if not page_id:
        raise IngestError(f"Не удалось извлечь page_id из {path_or_id}")

    notion = NotionClient(auth=token)
    page = notion.pages.retrieve(page_id=page_id)
    blocks = notion.blocks.children.list(block_id=page_id, page_size=200)

    title = _extract_title(page)
    md_parts = [_block_to_md(b) for b in blocks.get("results", [])]
    md = "\n\n".join(p for p in md_parts if p)

    if not md:
        raise IngestError(f"Notion {page_id}: пустая страница")

    return Document(
        title=title or page_id,
        content=md,
        source=Source(
            path=Path(f"notion:{page_id}"),
            format="notion",
            size_bytes=len(md),
            mtime=datetime.now(),
        ),
        metadata={
            "notion_id": page_id,
            "url": page.get("url", ""),
            "block_count": len(blocks.get("results", [])),
        },
    )


def _ingest_exported(path: Path) -> Document:
    """Notion экспортирует страницы как .md в ZIP — берём как обычный markdown."""
    from docstoolkit.ingest.markdown import ingest as _md_ingest
    doc = _md_ingest(path)
    doc.source.format = "notion-export"
    return doc


def _extract_page_id(s: str) -> str:
    """Извлекает page_id из URL или возвращает как есть если уже UUID."""
    import re
    # Notion URL: https://www.notion.so/Title-32hexchars
    m = re.search(r'([0-9a-f]{32})', s.replace("-", ""))
    if m:
        h = m.group(1)
        return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"
    return s


def _extract_title(page: dict) -> str:
    """Title из properties.Name.title[0].plain_text."""
    props = page.get("properties", {})
    for key in ("Name", "Title", "title"):
        if key in props:
            t = props[key].get("title", [])
            if t and isinstance(t, list):
                return t[0].get("plain_text", "") or ""
    return ""


def _block_to_md(block: dict) -> str:
    """Конверт одного Notion block в markdown. Минимальная поддержка."""
    btype = block.get("type", "")
    data = block.get(btype, {})

    if btype == "paragraph":
        return _rich_text(data.get("rich_text", []))
    if btype.startswith("heading_"):
        level = int(btype.split("_")[1])
        return f"{'#' * level} {_rich_text(data.get('rich_text', []))}"
    if btype == "bulleted_list_item":
        return f"- {_rich_text(data.get('rich_text', []))}"
    if btype == "numbered_list_item":
        return f"1. {_rich_text(data.get('rich_text', []))}"
    if btype == "to_do":
        checked = "[x]" if data.get("checked") else "[ ]"
        return f"- {checked} {_rich_text(data.get('rich_text', []))}"
    if btype == "code":
        lang = data.get("language", "")
        text = _rich_text(data.get("rich_text", []))
        return f"```{lang}\n{text}\n```"
    if btype == "quote":
        return f"> {_rich_text(data.get('rich_text', []))}"
    if btype == "divider":
        return "---"
    return _rich_text(data.get("rich_text", []))


def _rich_text(rt: list) -> str:
    parts = []
    for t in rt:
        text = t.get("plain_text", "")
        ann = t.get("annotations", {})
        if ann.get("bold"):
            text = f"**{text}**"
        if ann.get("italic"):
            text = f"*{text}*"
        if ann.get("code"):
            text = f"`{text}`"
        parts.append(text)
    return "".join(parts)
