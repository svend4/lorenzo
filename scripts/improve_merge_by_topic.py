"""
improve_merge_by_topic.py — склеивает файлы-фрагменты одной темы в единый документ.

Обнаруживает «цепочки» файлов принадлежащих одной теме по:
  - сходству заголовков (Jaccard по словам)
  - нумерации в имени файла (01-x, 02-x...)
  - общим TF-IDF ключевым словам

Режимы:
  --dry-run   (по умолчанию) — показать план слияния
  --apply     — реально склеить файлы (оригиналы → merged/, удаляет исходники)
  --threshold — порог сходства Jaccard (0.0-1.0, по умолчанию 0.35)
  --min-group — минимальный размер группы для слияния (по умолчанию 2)
  --section   — обрабатывать конкретную секцию

Запуск:
    python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --dry-run
    python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --apply
"""
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY     = "--apply"   in sys.argv
DRY_RUN   = not APPLY

THRESHOLD = 0.35
if "--threshold" in sys.argv:
    idx = sys.argv.index("--threshold")
    if idx + 1 < len(sys.argv):
        THRESHOLD = float(sys.argv[idx + 1])

MIN_GROUP = 2
if "--min-group" in sys.argv:
    idx = sys.argv.index("--min-group")
    if idx + 1 < len(sys.argv):
        MIN_GROUP = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"README.md", "SEARCH.md", "CONTENT_GAPS.md"}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "the", "a", "an", "is", "are",
    "of", "in", "on", "to", "for", "with", "by", "from", "and", "not",
}


# ─── Утилиты ───────────────────────────────────────────────────────────────

def _title_words(path: Path) -> set[str]:
    """Слова из имени файла (без номера и расширения)."""
    name = path.stem.lower()
    name = re.sub(r'^\d+-', '', name)          # убираем ведущий номер
    name = re.sub(r'-md$', '', name)            # убираем суффикс -md
    words = set(re.findall(r'[a-zа-яё]{3,}', name))
    return words - STOPWORDS


def _heading_words(text: str) -> set[str]:
    """Слова из H1/H2 заголовков."""
    headings = re.findall(r'^#{1,2}\s+(.+)$', text, re.MULTILINE)
    words = set()
    for h in headings:
        words |= set(re.findall(r'[a-zа-яёA-ZА-ЯЁ]{3,}', h.lower()))
    return words - STOPWORDS


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def _key_words(text: str, n: int = 15) -> set[str]:
    """Топ-N слов по TF (быстро, без IDF)."""
    clean = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    clean = re.sub(r'https?://\S+', ' ', clean)
    tokens = [
        t for t in re.findall(r'[а-яёa-z]{4,}', clean.lower())
        if t not in STOPWORDS
    ]
    return {w for w, _ in Counter(tokens).most_common(n)}


def _extract_number(path: Path) -> int | None:
    """Извлекает ведущий номер из имени файла."""
    m = re.match(r'^(\d+)', path.stem)
    return int(m.group(1)) if m else None


# ─── Поиск групп ───────────────────────────────────────────────────────────

def _find_groups(files: list[Path], texts: dict[str, str]) -> list[list[Path]]:
    """Находит группы похожих файлов методом Union-Find."""
    n = len(files)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        parent[find(x)] = find(y)

    for i in range(n):
        for j in range(i + 1, n):
            fi, fj = files[i], files[j]
            ti = _title_words(fi)
            tj = _title_words(fj)

            # 1) Jaccard по словам заголовка файла
            title_sim = _jaccard(ti, tj)

            # 2) Последовательные номера (01-foo, 02-foo → одна тема)
            ni, nj = _extract_number(fi), _extract_number(fj)
            seq_bonus = 0.3 if (ni and nj and abs(ni - nj) <= 3 and ti & tj) else 0.0

            # 3) Ключевые слова из текста
            ki = _key_words(texts.get(str(fi.relative_to(ROOT)), ""), 20)
            kj = _key_words(texts.get(str(fj.relative_to(ROOT)), ""), 20)
            kw_sim = _jaccard(ki, kj)

            # Итоговая схожесть
            sim = max(title_sim + seq_bonus, kw_sim * 0.8)
            if sim >= THRESHOLD:
                union(i, j)

    # Собираем группы
    groups: dict[int, list[int]] = defaultdict(list)
    for i in range(n):
        groups[find(i)].append(i)

    return [[files[i] for i in members] for members in groups.values()
            if len(members) >= MIN_GROUP]


# ─── Слияние ───────────────────────────────────────────────────────────────

def _merge_files(group: list[Path], texts: dict[str, str], out_dir: Path) -> Path:
    """Склеивает группу файлов в один документ."""
    # Сортируем по номеру, потом по имени
    group_sorted = sorted(group, key=lambda f: (_extract_number(f) or 999, f.stem))

    # Имя выходного файла — из первого в группе, без номера
    first = group_sorted[0]
    base_name = re.sub(r'^\d+-', '', first.stem)
    base_name = re.sub(r'-md$', '', base_name)
    out_name = f"merged-{base_name}.md"
    out_path = out_dir / out_name

    # Собираем контент
    parts = [
        f"# {base_name.replace('-', ' ').title()}\n\n",
        f"_Слияние {len(group_sorted)} файлов — {TODAY}_\n\n",
        f"> Источники: {', '.join(f.name for f in group_sorted)}\n\n",
    ]

    seen_headings: set[str] = set()
    for f in group_sorted:
        rel = str(f.relative_to(ROOT))
        text = texts.get(rel, "")
        if not text.strip():
            continue

        # Убираем дублирующиеся H1 заголовки
        lines = text.split('\n')
        filtered = []
        for line in lines:
            if re.match(r'^#\s+', line):
                h = line.strip()
                if h in seen_headings:
                    continue
                seen_headings.add(h)
            filtered.append(line)

        parts.append(f"\n<!-- source: {f.name} -->\n")
        parts.append('\n'.join(filtered).strip())
        parts.append('\n\n---\n')

    out_path.write_text(''.join(parts), encoding="utf-8")
    return out_path


# ─── Main ──────────────────────────────────────────────────────────────────

def main() -> None:
    print("🔗 improve_merge_by_topic.py — слияние файлов по теме")
    print(f"   Порог схожести: {THRESHOLD}  |  Мин. группа: {MIN_GROUP}")
    print(f"   Режим: {'APPLY (запись файлов!)' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    all_files = [
        f for f in sorted(target.rglob("*.md"))
        if f.name not in SKIP_FILES
    ]
    print(f"   Файлов: {len(all_files)}")

    # Загружаем тексты
    texts: dict[str, str] = {}
    for f in all_files:
        try:
            texts[str(f.relative_to(ROOT))] = f.read_text(encoding="utf-8")
        except Exception:
            pass

    groups = _find_groups(all_files, texts)
    total_files = sum(len(g) for g in groups)

    print(f"   Найдено групп для слияния: {len(groups)}")
    print(f"   Файлов в группах: {total_files}\n")

    if not groups:
        print("  Нет групп для слияния при текущем пороге схожести.")
        print(f"  Попробуйте уменьшить --threshold (текущий: {THRESHOLD})")
        return

    for i, group in enumerate(sorted(groups, key=lambda g: -len(g)), 1):
        base = re.sub(r'^\d+-', '', group[0].stem)[:40]
        print(f"  Группа {i}: {len(group)} файлов → merged-{base}.md")
        for f in sorted(group, key=lambda x: (_extract_number(x) or 999, x.stem))[:5]:
            print(f"    · {f.name}")
        if len(group) > 5:
            print(f"    ... и ещё {len(group)-5}")
        print()

    if DRY_RUN:
        words_saved = sum(
            len(re.findall(r'\S+', texts.get(str(f.relative_to(ROOT)), "")))
            for g in groups for f in g
        )
        print(f"  Было бы объединено ~{words_saved:,} слов в {len(groups)} файлов")
        print("  Запустите с --apply для реального слияния.")
        return

    # Создаём папку для слитых файлов
    out_dir = target / "merged"
    out_dir.mkdir(exist_ok=True)

    created = 0
    for group in groups:
        try:
            out = _merge_files(group, texts, out_dir)
            print(f"  ✅ {out.name} ({len(group)} файлов)")
            created += 1
        except Exception as e:
            print(f"  ❌ ошибка: {e}")

    print(f"\n  Создано: {created} слитых файлов → {out_dir.relative_to(ROOT)}/")
    print("  Оригиналы сохранены. Удалите вручную после проверки.")


if __name__ == "__main__":
    main()
