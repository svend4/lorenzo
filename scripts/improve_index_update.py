"""
improve_index_update.py — инкрементальное обновление search_index.json.
Обновляет только файлы, изменившиеся с момента последней индексации
(по mtime или git diff).
Запуск: python scripts/improve_index_update.py
"""
import re
import json
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
INDEX_FILE = DOCS / "search_index.json"

SKIP = {
    "search_index.json", "export_full.json", "export.csv",
    "sitemap.xml", "network.dot", "index.html",
}


def get_changed_files() -> set[str]:
    """Файлы изменённые в git с последнего коммита."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            cwd=ROOT, capture_output=True, text=True
        )
        changed = {l.strip() for l in result.stdout.splitlines() if l.endswith(".md")}
        # Также незакоммиченные
        result2 = subprocess.run(
            ["git", "diff", "--name-only"],
            cwd=ROOT, capture_output=True, text=True
        )
        changed |= {l.strip() for l in result2.stdout.splitlines() if l.endswith(".md")}
        return changed
    except Exception:
        return set()


def _clean_md(text: str) -> str:
    """Удаляет markdown-разметку и нормализует пробелы."""
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'-\s+\[.+?\]\(#?.+?\)', '', text)   # TOC-ссылки
    text = re.sub(r'\[!(?:WARNING|NOTE|TIP|IMPORTANT|CAUTION)\]', '', text)
    text = re.sub(r'[#*_`\[\]|>^]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _extract_summary_block(text: str) -> str:
    """Извлекает содержимое блока <!-- summary --> ... <!-- (следующий комментарий)."""
    m = re.search(r'<!--\s*summary\s*-->(.*?)(?=<!--|\Z)', text, re.DOTALL)
    if not m:
        return ""
    return _clean_md(m.group(1))


def _extract_body(text: str) -> str:
    """
    Извлекает основной текст файла — тело после boilerplate-секций.

    Стратегия: ищет первый непустой параграф вне блоков summary/abstract/status/TOC.
    Удаляет:
      - Авто-generated блоки (<!-- abstract-auto -->, <!-- autofill-status -->)
      - TOC-ссылки (- [text](#anchor))
      - Alert-цитаты (> [!WARNING/NOTE/TIP])
      - Авто-абстракты (> **Абстракт**)
    Сохраняет:
      - Текст в блоках summary (уже извлечён отдельно)
      - Реальные параграфы и разделы документа
    """
    # Удалить блоки-заглушки целиком
    text = re.sub(r'<!--\s*abstract-auto\s*-->.*?(?=##|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*autofill-status\s*-->.*?(?=##|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*summary\s*-->.*?(?=<!--|\Z)', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--\s*(?:toc-auto|see-also|related-auto|backlinks-auto|backlinks|alert-added|similar-docs)\s*-->', '', text)
    return _clean_md(text)


def _extract_content(text: str, max_chars: int = 2000) -> str:
    """
    Формирует индексируемый контент:
      1. Summary-блок (наиболее релевантный)
      2. Тело документа (stripped boilerplate)
    """
    summary = _extract_summary_block(text)
    body    = _extract_body(text)
    combined = (summary + " " + body).strip()
    return combined[:max_chars]


def build_entry(f: Path) -> dict:
    text = f.read_text(encoding="utf-8")
    rel  = str(f.relative_to(ROOT))

    title = f.stem
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()[:80]
            break

    content = _extract_content(text)
    clean   = _clean_md(text)      # для подсчёта слов (полный текст)

    tags_m = re.search(r'<!--\s*tags:\s*([^-]+?)-->', text)
    tags = [t.strip() for t in tags_m.group(1).split(',')] if tags_m else []

    summary_block = _extract_summary_block(text)
    summary = (summary_block or clean)[:200]

    rel_parts = Path(rel).parts
    section = rel_parts[1] if len(rel_parts) > 2 else "root"

    return {
        "path":    rel,
        "title":   title,
        "section": section,
        "tags":    tags,
        "summary": summary,
        "words":   len(clean.split()),
        "content": content,
        "updated": datetime.now().isoformat()[:19],
    }


def main():
    print("Инкрементальное обновление search_index.json...")

    # Загружаем существующий индекс
    if INDEX_FILE.exists():
        existing = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        if isinstance(existing, list):
            index = {e["path"]: e for e in existing}
        else:
            index = {e["path"]: e for e in existing.get("docs", existing)}
    else:
        index = {}

    changed_paths = get_changed_files()
    print(f"  изменённых файлов: {len(changed_paths)}")

    # Индексируем все md-файлы (обновляем только изменённые)
    updated = 0
    added   = 0
    total   = 0

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        rel = str(f.relative_to(ROOT))
        total += 1

        # Обновляем если: нет в индексе ИЛИ изменился
        if rel not in index:
            index[rel] = build_entry(f)
            added += 1
        elif rel in changed_paths or any(rel.endswith(c) for c in changed_paths):
            index[rel] = build_entry(f)
            updated += 1

    # Удаляем записи об удалённых файлах
    existing_paths = {str(f.relative_to(ROOT)) for f in DOCS.rglob("*.md")}
    removed = [k for k in list(index.keys()) if k not in existing_paths]
    for k in removed:
        del index[k]

    # Сохраняем
    output = sorted(index.values(), key=lambda x: x["path"])
    INDEX_FILE.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    size_kb = INDEX_FILE.stat().st_size // 1024
    print(f"  wrote: {INDEX_FILE.relative_to(ROOT)} ({size_kb} KB)")
    print(f"  всего: {total}, добавлено: {added}, обновлено: {updated}, "
          f"удалено: {len(removed)}")


if __name__ == "__main__":
    main()
