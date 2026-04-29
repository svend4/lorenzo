"""
improve_link_preview.py — проверяет внешние ссылки в docs/ и кэширует их статус.

Для каждой уникальной URL:
  - HEAD-запрос (timeout 8с) → HTTP-статус
  - Если 200: извлекает <title> из HTML
  - Кэш в docs/link_cache.json (повторные проверки пропускаются если < CACHE_DAYS)

Создаёт docs/LINK_PREVIEW.md.
Запуск:
    python scripts/improve_link_preview.py
    python scripts/improve_link_preview.py --refresh   # игнорировать кэш
    python scripts/improve_link_preview.py --timeout 5
    python scripts/improve_link_preview.py --section 05-habr-projects
"""
import json
import re
import sys
import urllib.request
import urllib.error
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()
CACHE_FILE = DOCS / "link_cache.json"
CACHE_DAYS = 7

REFRESH = "--refresh" in sys.argv
TIMEOUT = 8
if "--timeout" in sys.argv:
    idx = sys.argv.index("--timeout")
    if idx + 1 < len(sys.argv):
        TIMEOUT = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"LINK_PREVIEW.md", "SEARCH.md"}

URL_RE = re.compile(r'https?://[^\s\)\]">]+')


def load_cache() -> dict:
    if CACHE_FILE.exists() and not REFRESH:
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def save_cache(cache: dict) -> None:
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def _is_fresh(entry: dict) -> bool:
    checked = entry.get("checked")
    if not checked:
        return False
    try:
        dt = datetime.fromisoformat(checked)
        return datetime.now() - dt < timedelta(days=CACHE_DAYS)
    except Exception:
        return False


def _fetch_title(url: str) -> str:
    """Пытается извлечь <title> из HTML (первые 8 КБ)."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Lorenzo-link-checker/1.0"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "html" not in ct:
                return ""
            chunk = resp.read(8192).decode("utf-8", errors="ignore")
            m = re.search(r'<title[^>]*>([^<]{1,120})</title>', chunk, re.IGNORECASE)
            return m.group(1).strip() if m else ""
    except Exception:
        return ""


def check_url(url: str, cache: dict) -> dict:
    """Проверяет URL; возвращает запись {status, title, checked}."""
    if url in cache and _is_fresh(cache[url]):
        return cache[url]

    entry: dict = {"checked": datetime.now().isoformat()}
    try:
        req = urllib.request.Request(
            url,
            method="HEAD",
            headers={"User-Agent": "Lorenzo-link-checker/1.0"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            entry["status"] = resp.status
    except urllib.error.HTTPError as e:
        entry["status"] = e.code
    except Exception:
        entry["status"] = 0  # недоступен

    if entry["status"] == 200:
        entry["title"] = _fetch_title(url)
    else:
        entry["title"] = ""

    cache[url] = entry
    return entry


def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text)


def main() -> None:
    print("🔗 improve_link_preview.py — проверка внешних ссылок")
    print(f"   Таймаут: {TIMEOUT}с, кэш: {CACHE_DAYS} дней")

    cache = load_cache()
    cached_count = sum(1 for e in cache.values() if _is_fresh(e))
    print(f"   Кэшировано: {cached_count} ссылок\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]

    # Собираем все URL
    url_sources: dict[str, list[str]] = defaultdict(list)
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for url in set(extract_urls(text)):
            url_sources[url].append(str(f.relative_to(ROOT)))

    total_urls = len(url_sources)
    print(f"   Уникальных URL: {total_urls}")

    # Проверяем
    results = []
    checked_new = 0
    for i, (url, sources) in enumerate(sorted(url_sources.items()), 1):
        in_cache = url in cache and _is_fresh(cache[url])
        if not in_cache:
            print(f"  [{i}/{total_urls}] {url[:70]}...", end="\r", flush=True)
            checked_new += 1

        entry = check_url(url, cache)
        results.append({
            "url": url,
            "status": entry.get("status", 0),
            "title": entry.get("title", ""),
            "sources": sources,
        })

    save_cache(cache)
    if checked_new:
        print(f"\n   Проверено новых: {checked_new}")

    # Разбивка по статусу
    ok = [r for r in results if r["status"] == 200]
    broken = [r for r in results if r["status"] not in (200, 301, 302) or r["status"] == 0]
    redirects = [r for r in results if r["status"] in (301, 302)]

    lines = [
        "# Статус внешних ссылок\n",
        f"_Обновлено: {TODAY}_\n",
        f"Всего URL: **{total_urls}** | ✅ Работают: **{len(ok)}** "
        f"| 🔄 Редиректы: **{len(redirects)}** | ❌ Недоступны: **{len(broken)}**\n",
    ]

    if broken:
        lines += [
            f"## ❌ Недоступные ссылки ({len(broken)})\n",
            "| URL | Статус | Файлы |",
            "|-----|--------|-------|",
        ]
        for r in sorted(broken, key=lambda x: x["status"]):
            status_str = str(r["status"]) if r["status"] else "timeout"
            files_str = ", ".join(f"`{s}`" for s in r["sources"][:2])
            if len(r["sources"]) > 2:
                files_str += f" +{len(r['sources'])-2}"
            lines.append(f"| `{r['url'][:80]}` | {status_str} | {files_str} |")

    if redirects:
        lines += [
            f"\n## 🔄 Редиректы ({len(redirects)})\n",
            "| URL | Статус |",
            "|-----|--------|",
        ]
        for r in redirects[:20]:
            lines.append(f"| `{r['url'][:80]}` | {r['status']} |")

    lines += [
        f"\n## ✅ Работающие ссылки ({len(ok)})\n",
        "| URL | Заголовок страницы |",
        "|-----|--------------------|",
    ]
    for r in ok[:50]:
        title = r["title"][:60] if r["title"] else "—"
        lines.append(f"| `{r['url'][:70]}` | {title} |")

    out = DOCS / "LINK_PREVIEW.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  ✅ {len(ok)} | 🔄 {len(redirects)} | ❌ {len(broken)}")


if __name__ == "__main__":
    main()
