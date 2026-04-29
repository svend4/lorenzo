"""Web ingest plugins для docs-toolkit.

Извлекают документы из удалённых источников:
  - URL (общий HTTP fetcher)
  - arxiv.org (через RSS/JSON API)
  - news.ycombinator.com (HN front page + items)
  - habr.com (статьи через простой HTML parse)

Все плагины опциональны — требуют urllib (stdlib, всегда есть).

Использование:
    from docstoolkit.web import fetch_url, fetch_arxiv

    doc = fetch_url("https://example.com/page")
    doc = fetch_arxiv("2401.12345")
"""
from docstoolkit.web.url import fetch_url
from docstoolkit.web.arxiv import fetch_arxiv, search_arxiv
from docstoolkit.web.hackernews import fetch_hn_item, fetch_hn_top
from docstoolkit.web.habr import fetch_habr

__all__ = [
    "fetch_url",
    "fetch_arxiv", "search_arxiv",
    "fetch_hn_item", "fetch_hn_top",
    "fetch_habr",
]
