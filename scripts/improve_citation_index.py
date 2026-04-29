"""
improve_citation_index.py — индекс внешних URL по частоте цитирования.

Для каждого внешнего URL показывает:
  - сколько файлов его цитируют
  - в каких секциях
  - насколько «авторитетен» домен в контексте проекта

Создаёт docs/CITATION_INDEX.md.
Запуск: python scripts/improve_citation_index.py
        python scripts/improve_citation_index.py --min-citations 2
        python scripts/improve_citation_index.py --domain github.com
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date
from urllib.parse import urlparse

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

MIN_CITATIONS = 1
if "--min-citations" in sys.argv:
    idx = sys.argv.index("--min-citations")
    if idx + 1 < len(sys.argv):
        MIN_CITATIONS = int(sys.argv[idx + 1])

DOMAIN_FILTER = None
if "--domain" in sys.argv:
    idx = sys.argv.index("--domain")
    if idx + 1 < len(sys.argv):
        DOMAIN_FILTER = sys.argv[idx + 1]

SKIP_FILES = {"CITATION_INDEX.md", "LINK_PREVIEW.md", "SEARCH.md", "BROKEN_LINKS.md"}

URL_RE = re.compile(r'https?://[^\s\)\]">]{5,}')

# Авторитетные домены для Knowledge OS / ML-сообщества
AUTHORITY_DOMAINS = {
    "github.com": 5, "arxiv.org": 5, "huggingface.co": 4,
    "habr.com": 4, "anthropic.com": 4,
    "medium.com": 3, "blog.": 2, "docs.": 3, "wiki.": 2,
    "youtube.com": 2, "youtu.be": 2,
    "stackoverflow.com": 3, "pypi.org": 3,
}


def _domain(url: str) -> str:
    try:
        return urlparse(url).netloc.lstrip("www.")
    except Exception:
        return ""


def _authority_score(url: str) -> int:
    dom = _domain(url)
    for pattern, score in AUTHORITY_DOMAINS.items():
        if pattern in dom:
            return score
    return 1


def _extract_urls(text: str) -> list[str]:
    # Убираем code-блоки
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'`[^`]+`', ' ', clean)
    return URL_RE.findall(clean)


def _normalize_url(url: str) -> str:
    # Убираем trailing punctuation
    return url.rstrip('.,;:)')


def main() -> None:
    print("📖 improve_citation_index.py — индекс цитирования URL")
    print(f"   Мин. цитирований: {MIN_CITATIONS}")

    # url -> set of files
    url_files: dict[str, set[str]] = defaultdict(set)
    # url -> count
    url_count: Counter = Counter()
    # domain -> set of urls
    domain_urls: dict[str, set[str]] = defaultdict(set)

    all_files = [f for f in sorted(DOCS.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(all_files)}\n")

    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        rel = str(f.relative_to(ROOT))
        urls = set(_normalize_url(u) for u in _extract_urls(text))
        for url in urls:
            if DOMAIN_FILTER and DOMAIN_FILTER not in url:
                continue
            url_files[url].add(rel)
            url_count[url] += 1
            domain_urls[_domain(url)].add(url)

    # Фильтрация по минимуму
    filtered = {url: files for url, files in url_files.items()
                if len(files) >= MIN_CITATIONS}

    # Топ доменов
    domain_counts = Counter({d: len(urls) for d, urls in domain_urls.items()})

    # Сортировка: score = count * authority
    def _score(url: str) -> float:
        return len(url_files[url]) * _authority_score(url)

    ranked = sorted(filtered.items(), key=lambda x: -_score(x[0]))

    lines = [
        "# Индекс цитирования URL\n",
        f"_Обновлено: {TODAY}_\n",
        f"Уникальных URL: **{len(url_count)}** | "
        f"Отфильтровано (≥{MIN_CITATIONS}): **{len(filtered)}**\n",
    ]

    # Топ доменов
    lines += [
        "## Топ доменов\n",
        "| Домен | URL | Авторитетность |",
        "|-------|-----|----------------|",
    ]
    for domain, count in domain_counts.most_common(20):
        auth = _authority_score(f"https://{domain}/")
        lines.append(f"| `{domain}` | {count} | {'⭐' * auth} |")

    # Топ цитируемых URL
    lines += [
        "\n## Наиболее цитируемые URL\n",
        "| URL | Файлов | Авторитетность | Домен |",
        "|-----|--------|----------------|-------|",
    ]
    for url, files in ranked[:50]:
        auth = _authority_score(url)
        dom = _domain(url)
        display_url = url[:70] + ('...' if len(url) > 70 else '')
        lines.append(f"| `{display_url}` | {len(files)} | {'⭐' * auth} | `{dom}` |")

    if DOMAIN_FILTER:
        lines += [f"\n_Фильтр по домену: `{DOMAIN_FILTER}`_\n"]

    # Детали для топ-10
    lines += ["\n## Детали топ-10\n"]
    for url, files in ranked[:10]:
        lines.append(f"### `{url[:80]}`\n")
        lines.append(f"Цитируется в {len(files)} файлах, авторитетность: {_authority_score(url)}\n")
        for f in sorted(files)[:5]:
            lines.append(f"- `{f}`")
        if len(files) > 5:
            lines.append(f"- ... и ещё {len(files)-5}")
        lines.append("")

    out = DOCS / "CITATION_INDEX.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  уникальных URL: {len(url_count)}, отфильтровано: {len(filtered)}")
    top3 = [_domain(u) for u, _ in ranked[:3]]
    if top3:
        print(f"  топ домены: {', '.join(top3)}")


if __name__ == "__main__":
    main()
