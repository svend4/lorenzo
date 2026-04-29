"""
improve_external_compare.py — сравнивает документы базы с внешними источниками.

Для заданной темы или файла:
  1. Скачивает внешний URL (HTML → plain text)
  2. Сравнивает с вашим документом (ключевые слова, уникальное, общее)
  3. Показывает что есть у них, чего нет у вас — и наоборот

Также поддерживает --auto: сканирует docs/ на URL-ссылки и сравнивает
документ с тем, на что он ссылается.

Запуск:
    python scripts/improve_external_compare.py --file docs/05-habr-projects/memory/yodoca.md --url https://habr.com/...
    python scripts/improve_external_compare.py --query "AgentFS" --url https://github.com/kksudo/agentfs
    python scripts/improve_external_compare.py --auto --section 05-habr-projects
    python scripts/improve_external_compare.py --auto --limit 5
"""
import re
import sys
import urllib.request
import urllib.error
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

TIMEOUT = 10
AUTO = "--auto" in sys.argv

FILE_ARG = None
if "--file" in sys.argv:
    idx = sys.argv.index("--file")
    if idx + 1 < len(sys.argv):
        FILE_ARG = ROOT / sys.argv[idx + 1]

URL_ARG = None
if "--url" in sys.argv:
    idx = sys.argv.index("--url")
    if idx + 1 < len(sys.argv):
        URL_ARG = sys.argv[idx + 1]

QUERY = None
if "--query" in sys.argv:
    idx = sys.argv.index("--query")
    if idx + 1 < len(sys.argv):
        QUERY = sys.argv[idx + 1]

LIMIT = 10
if "--limit" in sys.argv:
    idx = sys.argv.index("--limit")
    if idx + 1 < len(sys.argv):
        LIMIT = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "and", "not",
    "it", "its", "we", "you", "they", "their", "our", "be", "been",
}


def _fetch_url(url: str) -> str:
    """Скачивает URL и возвращает plain text (убирает HTML-теги)."""
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Lorenzo-compare/1.0 (research tool)"},
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            html = resp.read(200_000).decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        return f"Error: {e}"

    # Убираем script/style
    html = re.sub(r'<script[^>]*>.*?</script>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'<style[^>]*>.*?</style>', ' ', html, flags=re.DOTALL | re.IGNORECASE)
    # Убираем теги
    text = re.sub(r'<[^>]+>', ' ', html)
    # Убираем лишние пробелы
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()[:50_000]


def _tokens(text: str, n: int = 50) -> set[str]:
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', text.lower())
        if t not in STOPWORDS
    ]
    return {w for w, _ in Counter(tokens).most_common(n)}


def _top_freq(text: str, n: int = 30) -> list[tuple[str, int]]:
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', text.lower())
        if t not in STOPWORDS
    ]
    return Counter(tokens).most_common(n)


def _extract_urls_from_doc(text: str) -> list[str]:
    """Извлекает внешние URL из документа."""
    urls = re.findall(r'https?://[^\s\)\]">]{10,}', text)
    return [u.rstrip('.,;)') for u in urls if 'github.com' in u or 'habr.com' in u]


def _find_best_doc(query: str) -> Path | None:
    """Находит файл в базе, наиболее релевантный запросу."""
    query_low = query.lower()
    best_score, best_file = 0, None
    for f in DOCS.rglob("*.md"):
        score = 0
        if query_low in f.stem.lower():
            score += 10
        try:
            text = f.read_text(encoding="utf-8")
            if query_low in text.lower():
                score += text.lower().count(query_low)
        except Exception:
            pass
        if score > best_score:
            best_score, best_file = score, f
    return best_file


def compare_with_url(doc_path: Path, url: str) -> dict:
    """Сравнивает документ с внешним URL."""
    try:
        doc_text = doc_path.read_text(encoding="utf-8")
    except Exception as e:
        return {"error": str(e)}

    print(f"     Скачиваем {url[:60]}...", end=" ", flush=True)
    ext_text = _fetch_url(url)
    print("готово" if not ext_text.startswith("Error") and not ext_text.startswith("HTTP") else "ошибка")

    if ext_text.startswith("Error") or ext_text.startswith("HTTP"):
        return {"error": ext_text, "url": url}

    doc_words = _tokens(doc_text, 60)
    ext_words = _tokens(ext_text, 60)

    common = doc_words & ext_words
    only_doc = doc_words - ext_words
    only_ext = ext_words - doc_words
    jaccard = len(common) / max(1, len(doc_words | ext_words))

    # Уникальные частотные слова внешнего источника (чего нет у нас)
    ext_freq = Counter(
        t for t in re.findall(r'[а-яёa-z]{4,}', ext_text.lower())
        if t not in STOPWORDS
    )
    missing_topics = [w for w, _ in ext_freq.most_common(30) if w in only_ext][:10]

    return {
        "doc_path": doc_path,
        "url": url,
        "jaccard": round(jaccard, 3),
        "common": sorted(common)[:15],
        "only_doc": sorted(only_doc)[:10],
        "only_ext": sorted(only_ext)[:10],
        "missing_topics": missing_topics,
        "ext_len": len(ext_text.split()),
        "doc_len": len(doc_text.split()),
    }


def format_result(r: dict) -> list[str]:
    if "error" in r:
        return [f"❌ Ошибка: {r['error']} ({r.get('url', '')})\n"]

    rel = r["doc_path"].relative_to(ROOT)
    pct = int(r["jaccard"] * 100)
    lines = [
        f"### `{rel}` vs `{r['url'][:60]}`\n",
        f"**Схожесть:** {pct}% | **Слов в базе:** {r['doc_len']} | **Слов у источника:** {r['ext_len']}\n",
    ]
    if r["common"]:
        lines.append(f"**Общие темы:** {', '.join(f'`{w}`' for w in r['common'][:10])}\n")
    if r["missing_topics"]:
        lines.append(f"**В источнике, но не в базе:** {', '.join(f'`{w}`' for w in r['missing_topics'])}\n")
        lines.append("> ⚠️ Рассмотрите дополнение документа этими темами\n")
    if r["only_doc"]:
        lines.append(f"**Только в вашем документе:** {', '.join(f'`{w}`' for w in r['only_doc'][:8])}\n")
    return lines


def main() -> None:
    print("🌐 improve_external_compare.py — сравнение с внешними источниками\n")

    all_results = []

    if AUTO:
        target = SECTION_FILTER or DOCS
        files = sorted(target.rglob("*.md"))
        print(f"   Режим: auto-сканирование {len(files)} файлов\n")

        done = 0
        for f in files:
            if done >= LIMIT:
                break
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            urls = _extract_urls_from_doc(text)
            if not urls:
                continue
            for url in urls[:2]:
                print(f"  📄 {f.relative_to(ROOT)}")
                result = compare_with_url(f, url)
                all_results.append(result)
                done += 1
                if done >= LIMIT:
                    break

    elif FILE_ARG and URL_ARG:
        if not FILE_ARG.exists():
            print(f"❌ Файл не найден: {FILE_ARG}")
            return
        result = compare_with_url(FILE_ARG, URL_ARG)
        all_results.append(result)

    elif QUERY and URL_ARG:
        doc = _find_best_doc(QUERY)
        if not doc:
            print(f"❌ Документ по запросу '{QUERY}' не найден в базе")
            return
        print(f"  Найден документ: {doc.relative_to(ROOT)}")
        result = compare_with_url(doc, URL_ARG)
        all_results.append(result)

    else:
        print("Использование:")
        print("  --file docs/... --url https://...")
        print("  --query 'AgentFS' --url https://github.com/...")
        print("  --auto --section 05-habr-projects --limit 10")
        return

    # Формируем отчёт
    lines = [
        "# Сравнение с внешними источниками\n",
        f"_Обновлено: {TODAY}_\n",
        f"Сравнений: **{len(all_results)}**\n",
    ]
    for r in all_results:
        lines.extend(format_result(r))
        lines.append("---\n")

    out = DOCS / "EXTERNAL_COMPARE.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\n  wrote: {out.relative_to(ROOT)}")
    print(f"  сравнений: {len(all_results)}")


if __name__ == "__main__":
    main()
