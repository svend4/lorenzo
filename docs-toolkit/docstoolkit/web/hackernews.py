"""Hacker News ingest через Firebase API."""
import json
import urllib.request
from datetime import datetime
from pathlib import Path

from docstoolkit.ingest.base import Document, IngestError, Source
from docstoolkit.web.url import _fetch


HN_API = "https://hacker-news.firebaseio.com/v0"


def _hn_get(endpoint: str) -> dict | list:
    text = _fetch(f"{HN_API}/{endpoint}.json")
    return json.loads(text)


def fetch_hn_item(item_id: int | str) -> Document:
    """Один HN item (story/comment) с дочерними комментариями (1 уровень)."""
    item = _hn_get(f"item/{item_id}")
    if not item:
        raise IngestError(f"HN item {item_id} не найден")

    title = item.get("title", f"HN item {item_id}")
    parts = [
        f"**by {item.get('by', '?')} on {datetime.fromtimestamp(item.get('time', 0)).isoformat(timespec='seconds')}**",
        f"**Score:** {item.get('score', 0)} | **Comments:** {item.get('descendants', 0)}",
    ]
    if item.get("url"):
        parts.append(f"**URL:** {item['url']}")
    parts.append("")

    if item.get("text"):
        parts.append(item["text"])
        parts.append("")

    # Топ-уровень комментариев
    kids = item.get("kids", [])[:5]
    if kids:
        parts.append("## Top comments\n")
        for kid_id in kids:
            try:
                kid = _hn_get(f"item/{kid_id}")
                if kid and kid.get("text"):
                    parts.append(f"### {kid.get('by', '?')}\n")
                    parts.append(kid["text"][:500])
                    parts.append("")
            except Exception:
                continue

    return Document(
        title=title,
        content="\n".join(parts),
        source=Source(
            path=Path(f"hn:{item_id}"),
            format="hackernews",
            size_bytes=0,
            mtime=datetime.now(),
        ),
        metadata={
            "hn_id": int(item_id),
            "type": item.get("type", "?"),
            "score": item.get("score", 0),
            "by": item.get("by", "?"),
            "url": item.get("url", ""),
        },
    )


def fetch_hn_top(n: int = 10) -> list[Document]:
    """Топ-N stories с HN front page."""
    ids = _hn_get("topstories")
    if not isinstance(ids, list):
        raise IngestError("HN: не удалось получить topstories")
    docs = []
    for item_id in ids[:n]:
        try:
            docs.append(fetch_hn_item(item_id))
        except Exception:
            continue
    return docs
