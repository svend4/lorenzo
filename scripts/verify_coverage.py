"""
verify_coverage.py — проверяет, не было ли потери информации при разбивке.

Запуск:
    python scripts/verify_coverage.py

Что проверяет:
    1. Суммарный объём текста: оригиналы vs docs/
    2. Ключевые термины из оригиналов — есть ли они в docs/
    3. Какие разделы (H2) из Markdown-отчётов попали / не попали в docs/
    4. Пустые или слишком короткие файлы в docs/
"""
import sys
import re
import email
from pathlib import Path
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(Path(__file__).parent))
from extract_mhtml import extract_text_from_mhtml


# ─── 1. Объём текста ──────────────────────────────────────────────────────────

def count_chars_md(path: Path) -> int:
    return len(path.read_text(encoding='utf-8'))

def count_chars_mhtml(path: Path) -> int:
    return len(extract_text_from_mhtml(str(path)))

def count_docs_chars() -> int:
    total = 0
    for f in DOCS.rglob("*.md"):
        total += len(f.read_text(encoding='utf-8'))
    return total


# ─── 2. Ключевые термины ──────────────────────────────────────────────────────

KEY_TERMS = [
    # Из отчётов 1,3
    "CardIndex", "AgentFS", "knowledge-space", "Yodoca", "NGT Memory",
    "LiteParse", "SENTINEL", "LiteLLM", "mclaude", "AI Factory", "Rufler",
    "AutoResearch", "Evidence Envelope", "Memory Write Policy",
    # Из вакансий
    "Forward Deployed", "Research Engineer", "Trust & Safety",
    # Из технологий
    "Sozialrecht", "GDPR", "local-first",
    # Из коллабораций
    "Firecrawl", "Hybrid RAG", "Graph RAG",
    # Из Хабр-проектов
    "MemNet", "Wikontic", "Hebbian",
]

def check_terms_in_docs(terms: list[str]) -> dict[str, bool]:
    docs_text = ""
    for f in DOCS.rglob("*.md"):
        docs_text += f.read_text(encoding='utf-8')

    return {term: (term.lower() in docs_text.lower()) for term in terms}


# ─── 3. Разделы H2 из Markdown-отчётов ──────────────────────────────────────

def check_h2_coverage(md_path: Path) -> tuple[list[str], list[str]]:
    text = md_path.read_text(encoding='utf-8')
    h2s = re.findall(r'^## (.+)$', text, re.MULTILINE)

    docs_text = ""
    for f in DOCS.rglob("*.md"):
        docs_text += f.read_text(encoding='utf-8')

    found = []
    missing = []
    for h2 in h2s:
        # Берём первые 30 символов заголовка для поиска
        snippet = h2[:30]
        if snippet.lower() in docs_text.lower():
            found.append(h2)
        else:
            missing.append(h2)
    return found, missing


# ─── 4. Пустые / короткие файлы ──────────────────────────────────────────────

def check_short_files(min_chars: int = 100) -> list[tuple[Path, int]]:
    short = []
    for f in DOCS.rglob("*.md"):
        size = len(f.read_text(encoding='utf-8'))
        if size < min_chars:
            short.append((f, size))
    return sorted(short, key=lambda x: x[1])


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("ПРОВЕРКА ПОЛНОТЫ РАЗБИВКИ ДОКУМЕНТОВ")
    print("=" * 60)

    # 1. Объём
    print("\n📊 1. Объём текста (символы)")
    md_total = 0
    mhtml_total = 0

    for name in ["deep-research-report (1).md", "deep-research-report (3).md"]:
        p = ROOT / name
        c = count_chars_md(p)
        md_total += c
        print(f"   {name}: {c:,}")

    mhtml_files = [
        "Вакансии в Anthropic по кластерам - Claude",
        "Комбинирование технологий для новых свойств - Claude",
        "Поиск коллабораций AI проектов",
        "Поиск уникальных проектов на Хабре для совместной разработки - Claude",
    ]
    for name in mhtml_files:
        p = ROOT / name
        print(f"   parsing {name[:40]}...", end=" ", flush=True)
        c = count_chars_mhtml(p)
        mhtml_total += c
        print(f"{c:,}")

    total_src = md_total + mhtml_total
    total_docs = count_docs_chars()
    ratio = total_docs / total_src * 100 if total_src else 0

    print(f"\n   Исходники (текст):  {total_src:>12,} симв.")
    print(f"   docs/ (итого):      {total_docs:>12,} симв.")
    print(f"   Покрытие:           {ratio:.1f}%")
    if ratio < 80:
        print("   ⚠️  ВНИМАНИЕ: возможна значительная потеря данных!")
    elif ratio < 95:
        print("   ⚠️  Небольшие потери (дубли, HTML-артефакты — норма)")
    else:
        print("   ✅ Полное покрытие")

    # 2. Ключевые термины
    print("\n🔍 2. Ключевые термины в docs/")
    results = check_terms_in_docs(KEY_TERMS)
    missing_terms = [t for t, found in results.items() if not found]
    found_terms = [t for t, found in results.items() if found]
    print(f"   Найдено: {len(found_terms)}/{len(KEY_TERMS)}")
    if missing_terms:
        print(f"   ❌ Отсутствуют: {', '.join(missing_terms)}")
    else:
        print("   ✅ Все термины найдены")

    # 3. H2-разделы
    print("\n📑 3. Разделы H2 из Markdown-отчётов")
    for name in ["deep-research-report (1).md", "deep-research-report (3).md"]:
        found, missing = check_h2_coverage(ROOT / name)
        print(f"\n   {name}:")
        print(f"   ✅ Найдено в docs/: {len(found)}")
        if missing:
            print(f"   ❌ Не найдено: {len(missing)}")
            for m in missing:
                print(f"      - {m}")

    # 4. Короткие файлы
    print("\n📄 4. Слишком короткие файлы (< 100 символов)")
    short = check_short_files()
    if short:
        for f, size in short[:10]:
            print(f"   ⚠️  {f.relative_to(ROOT)} ({size} симв.)")
        if len(short) > 10:
            print(f"   ... и ещё {len(short)-10}")
    else:
        print("   ✅ Все файлы содержательны")

    # Итог
    print("\n" + "=" * 60)
    total_files = len(list(DOCS.rglob("*.md")))
    print(f"ИТОГО: {total_files} файлов в docs/")
    print(f"Пропущенных терминов: {len(missing_terms)}")
    print(f"Коротких файлов: {len(short)}")
    print("=" * 60)


if __name__ == '__main__':
    main()
