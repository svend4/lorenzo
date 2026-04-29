"""arxiv.org ingest — статьи и поиск.

API: https://info.arxiv.org/help/api/index.html (Atom XML).
"""
import re
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.web.url import _fetch, USER_AGENT


ARXIV_API = "http://export.arxiv.org/api/query"


def _parse_atom_entry(entry_xml: str) -> dict:
    """Простой парсер одной <entry> из Atom (без зависимостей)."""
    def _get(tag):
        m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', entry_xml, re.DOTALL)
        return m.group(1).strip() if m else ""

    def _get_all(tag):
        return re.findall(rf'<{tag}[^>]*>(.*?)</{tag}>', entry_xml, re.DOTALL)

    return {
        "id": _get("id"),
        "title": re.sub(r'\s+', ' ', _get("title")),
        "summary": re.sub(r'\s+', ' ', _get("summary")),
        "published": _get("published"),
        "authors": [re.sub(r'\s+', ' ', _get_one_name(a)) for a in _get_all("author")],
        "categories": re.findall(r'category[^>]*term="([^"]+)"', entry_xml),
    }


def _get_one_name(author_xml: str) -> str:
    m = re.search(r'<name[^>]*>(.*?)</name>', author_xml, re.DOTALL)
    return m.group(1).strip() if m else ""


def fetch_arxiv(arxiv_id: str) -> Document:
    """Скачивает метаданные и абстракт статьи arxiv по ID (например '2401.12345').

    Не скачивает полный PDF — только метаданные + абстракт.
    Для PDF используйте ingest/pdf.py отдельно.
    """
    arxiv_id = arxiv_id.strip()
    # Убрать префикс arxiv:/arXiv: если есть
    arxiv_id = re.sub(r'^(arxiv|arXiv):', '', arxiv_id)

    url = f"{ARXIV_API}?id_list={urllib.parse.quote(arxiv_id)}"
    xml = _fetch(url)

    entries = re.findall(r'<entry>(.*?)</entry>', xml, re.DOTALL)
    if not entries:
        raise IngestError(f"arxiv: {arxiv_id} не найден")

    meta = _parse_atom_entry(entries[0])
    if not meta["title"]:
        raise IngestError(f"arxiv: пустой title для {arxiv_id}")

    md = [
        f"**arxiv:{arxiv_id}**",
        "",
        f"**Authors:** {', '.join(meta['authors'])}",
        f"**Published:** {meta['published']}",
        f"**Categories:** {', '.join(meta['categories'])}",
        "",
        "## Abstract",
        "",
        meta["summary"],
        "",
        f"## Links",
        "",
        f"- [arxiv:{arxiv_id}]({meta['id']})",
        f"- [PDF](https://arxiv.org/pdf/{arxiv_id})",
    ]

    return Document(
        title=meta["title"],
        content="\n".join(md),
        source=Source(
            path=Path(f"arxiv:{arxiv_id}"),
            format="arxiv",
            size_bytes=len(xml),
            mtime=datetime.now(),
        ),
        metadata={
            "arxiv_id": arxiv_id,
            "authors": meta["authors"],
            "categories": meta["categories"],
            "published": meta["published"],
        },
    )


def search_arxiv(query: str, max_results: int = 10) -> list[Document]:
    """Поиск arxiv по запросу. Возвращает Document для каждой статьи."""
    url = (f"{ARXIV_API}?search_query=all:{urllib.parse.quote(query)}"
           f"&start=0&max_results={max_results}")
    xml = _fetch(url)
    entries = re.findall(r'<entry>(.*?)</entry>', xml, re.DOTALL)

    docs = []
    for entry_xml in entries:
        meta = _parse_atom_entry(entry_xml)
        # Извлечь arxiv_id из id
        m = re.search(r'arxiv\.org/abs/([^v]+)', meta["id"])
        if not m:
            continue
        arxiv_id = m.group(1)
        try:
            docs.append(fetch_arxiv(arxiv_id))
        except IngestError:
            continue
    return docs
