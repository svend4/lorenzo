#!/usr/bin/env python3
"""
Импорт и анализ паттернов из svend4/data70 для Lorenzo/Svyazi 2.0.

Три режима:
  --analyze         показать найденные пересечения с текущим корпусом
  --archetypes      вывести таблицу архетипов для всех карточек docs/
  --dat-demo        демо Dynamic Alpha Tuning на примере запросов
  --import-graph    импортировать infom_import.json как карточки в docs/
  --help

Источник идей: svend4/data70/prepare_for_infom.py
Документация:  docs/DATA70_ANALYSIS.md
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# ── Архетипная таксономия из data70 ──────────────────────────────────────────

ARCHETYPES = {
    "ADCO": ("AI/Digital + Conceptual/Operational",
             ["нейросет", "llm", "gpt", "модел", "агент", "rag", "embedding",
              "программиров", "код", "python", "javascript", "react"]),
    "MSCF": ("Manual + Systematic + Conservative + Formal",
             ["шаблон", "юридич", "договор", "закон", "право", "sgb", "pflege",
              "widerspruch", "antrag", "стандарт", "регламент", "rfc"]),
    "MDCO": ("Mechanical + Dynamic + Creative + Operational",
             ["дрон", "бпла", "uav", "робот", "hardware", "дроно", "мотор",
              "сенсор", "servo", "arduino", "raspberry", "конструкц"]),
    "ASCO": ("Analytical + Systematic + Conservative + Operational",
             ["методолог", "знани", "систематиз", "пирамид", "классификац",
              "анализ", "структур", "архитектур", "индекс", "граф", "онтолог"]),
    "ADEO": ("AI + Dynamic + Exploratory + Operational",
             ["автоматизац", "make.com", "n8n", "workflow", "pipeline",
              "интеграц", "webhook", "api", "скрипт", "batch"]),
    "MDCF": ("Market + Dynamic + Creative + Functional",
             ["бизнес", "стартап", "монетиз", "рынок", "продукт", "saas",
              "клиент", "доход", "финансов", "инвестиц"]),
    "MDEO": ("Mechanical + Dynamic + Exploratory + Operational",
             ["транспорт", "медиа", "дрон", "видео", "журналист",
              "контент", "публикац", "вещани"]),
    "MDEF": ("Medical + Diagnostic + Evaluative + Formal",
             ["медицин", "здоровь", "болезн", "уход", "диагноз", "лечени",
              "пациент", "caremate", "pflegegrad"]),
    "ASEF": ("Analytical + Systematic + Exploratory + Functional",
             []),  # default
}


def classify_archetype(text: str) -> str:
    """Классифицирует текст по архетипу через keyword matching."""
    t = text.lower()
    best_score, best_arch = 0, "ASEF"
    for arch, (_, keywords) in ARCHETYPES.items():
        if not keywords:
            continue
        score = sum(1 for kw in keywords if kw in t)
        if score > best_score:
            best_score, best_arch = score, arch
    return best_arch


# ── Dynamic Alpha Tuning (DAT) — из data70 тема #7 ───────────────────────────

def compute_dynamic_alpha(query: str) -> float:
    """
    Динамически подбирает соотношение BM25/vector для гибридного поиска.

    Короткие точные запросы (коды, имена, ID) → больше BM25 (alpha ниже).
    Длинные концептуальные запросы → больше vector (alpha выше).

    Returns: float в [0.1, 0.9], где выше = больше vector, ниже = больше BM25.
    """
    tokens = query.split()
    q_len = len(tokens)

    # Признаки «точного» запроса
    has_code = bool(re.search(r'[A-Z]{2,}\d|RFC-\d{3,}|#\d{3,}', query))
    has_entity = any(t[0].isupper() for t in tokens if len(t) > 2)
    has_quoted = '"' in query or "«" in query

    if has_code or has_quoted:
        return 0.15  # почти чистый BM25
    if has_entity and q_len <= 3:
        return 0.25  # имя/проект — BM25 доминирует
    if q_len <= 3:
        return 0.40  # короткий запрос
    if q_len <= 6:
        return 0.55  # средний запрос
    if q_len <= 10:
        return 0.70  # длинный концептуальный
    return 0.85      # очень длинный — vector доминирует


def dat_demo():
    """Демонстрация Dynamic Alpha Tuning на примерах."""
    examples = [
        "RFC-0001",
        "AgentFS",
        "агент память",
        "агент с памятью для Svyazi 2.0",
        "как работает консолидация знаний в мультиагентной архитектуре с RAG",
        '"Yodoca"',
        "#RFC",
        "agent memory MCP SQLite консолидация базы знаний",
    ]
    print("Dynamic Alpha Tuning (DAT) демо")
    print("─" * 55)
    print(f"{'Запрос':<45} {'alpha':>6} {'доминирует'}")
    print("─" * 55)
    for q in examples:
        a = compute_dynamic_alpha(q)
        dom = "vector" if a >= 0.6 else "BM25" if a <= 0.4 else "баланс"
        print(f"{q[:44]:<45} {a:>6.2f} {dom}")
    print()
    print("Текущий Lorenzo использует фиксированный alpha=0.6.")
    print("DAT адаптирует баланс под каждый запрос — особенно полезно")
    print("для exact-match (RFC-0001) vs концептуальных запросов.")


# ── Анализ пересечений с Lorenzo ─────────────────────────────────────────────

def analyze_intersections():
    """Ищет пересечения тем data70 с текущим корпусом Lorenzo."""
    # Темы из data70 как search seeds
    data70_themes = {
        "Социальное право": ["sgb", "pflege", "инвалид", "persona", "widerspruch"],
        "ИИ и нейросети": ["llm", "нейросет", "gpt", "модел", "агент", "rag"],
        "Дроны и БПЛА": ["дрон", "бпла", "uav", "skymedia", "wilos"],
        "Управление знаниями": ["пирамид", "бонсай", "инфо-бонсай", "zettelkasten"],
        "Автоматизация": ["make.com", "n8n", "автоматизац", "workflow"],
        "Робототехника": ["робот", "рой", "зоопарк", "caremate"],
        "Юридический ИИ": ["шаблон", "widerspruch", "antrag", "sgb ix"],
    }

    print("Пересечения корпуса Lorenzo с темами data70")
    print("=" * 60)
    total_hits = 0

    for theme, keywords in data70_themes.items():
        hits = []
        for md in DOCS.rglob("*.md"):
            try:
                text = md.read_text(encoding="utf-8", errors="ignore").lower()
                score = sum(1 for kw in keywords if kw in text)
                if score > 0:
                    hits.append((score, md.relative_to(DOCS)))
            except Exception:
                continue

        hits.sort(reverse=True)
        print(f"\n{theme} ({len(hits)} документов):")
        for score, path in hits[:5]:
            print(f"  [{score:2d}] {path}")
        total_hits += len(hits)

    print(f"\nИтого: {total_hits} совпадений по {len(data70_themes)} темам")


# ── Показать архетипы для корпуса ─────────────────────────────────────────────

def show_archetypes(top: int = 30):
    """Классифицирует docs/ по архетипам из data70."""
    arch_groups = defaultdict(list)

    for md in sorted(DOCS.rglob("*.md"))[:500]:
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")[:1500]
            arch = classify_archetype(text)
            arch_groups[arch].append(md.relative_to(DOCS))
        except Exception:
            continue

    print("Распределение документов Lorenzo по архетипам data70")
    print("=" * 60)
    for arch in sorted(arch_groups, key=lambda a: -len(arch_groups[a])):
        label, _ = ARCHETYPES[arch]
        docs = arch_groups[arch]
        print(f"\n{arch} — {label} ({len(docs)} docs)")
        for d in docs[:5]:
            print(f"  {d}")
        if len(docs) > 5:
            print(f"  ... и ещё {len(docs) - 5}")


# ── Импорт infom_import.json как карточки ─────────────────────────────────────

def import_graph(graph_path: Path, dry_run: bool = True):
    """
    Импортирует граф из infom_import.json в docs/cards/data70/.
    Создаёт карточку для каждого нода типа 'project' (depth>=3).
    """
    if not graph_path.exists():
        print(f"Файл не найден: {graph_path}")
        print("Запустите prepare_for_infom.py в data70 или укажите путь вручную.")
        return

    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = [n for n in graph["nodes"]
             if n.get("metadata", {}).get("type") == "project"]

    out_dir = DOCS / "cards" / "data70"
    if not dry_run:
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"{'[dry-run] ' if dry_run else ''}Импорт {len(nodes)} проектов из data70")
    created = 0

    for node in nodes:
        meta = node.get("metadata", {})
        title = node["label"]
        slug = re.sub(r'[^a-zа-яё0-9]+', '-', title.lower()).strip('-')[:50]
        fname = out_dir / f"{slug}.md"

        concepts = ", ".join(meta.get("concepts", []))
        arch = node.get("archetype", "ASEF")
        depth = meta.get("depth", 1)
        chars = meta.get("chars", 0)
        conv_num = meta.get("num", "?")

        content = f"""---
title: "{title}"
state: raw
tags: [data70, import, {arch.lower()}]
archetype: {arch}
depth: {depth}
source: "svend4/data70 conversation #{conv_num}"
summary: "{title[:100]}"
---

# {title}

**Источник:** Архив data70, разговор #{conv_num}
**Архетип:** {arch} ({ARCHETYPES.get(arch, ('?', []))[0]})
**Глубина:** {depth}/5 ({chars:,} символов)
**Ключевые концепции:** {concepts}

> Карточка импортирована из `svend4/data70` через `scripts/improve_data70_import.py`.
> Для получения полного контента обратитесь к исходному архиву.

## Связи

Смотрите: `docs/DATA70_ANALYSIS.md` — полный анализ репозитория data70.
"""
        if not dry_run:
            fname.write_text(content, encoding="utf-8")
        else:
            print(f"  → {fname.relative_to(ROOT)} (depth={depth}, arch={arch})")
        created += 1

    print(f"\n{'Будет создано' if dry_run else 'Создано'}: {created} карточек")
    if dry_run:
        print("Запустите с --import-graph --apply для реального импорта.")


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Интеграция паттернов svend4/data70 с Lorenzo",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--analyze", action="store_true",
                        help="Показать пересечения Lorenzo с темами data70")
    parser.add_argument("--archetypes", action="store_true",
                        help="Показать архетипы документов Lorenzo")
    parser.add_argument("--dat-demo", action="store_true",
                        help="Демо Dynamic Alpha Tuning")
    parser.add_argument("--import-graph", action="store_true",
                        help="Импортировать infom_import.json как карточки")
    parser.add_argument("--graph-path", type=Path,
                        default=Path("/tmp/data70/infom_import.json"),
                        help="Путь к infom_import.json")
    parser.add_argument("--apply", action="store_true",
                        help="Применить изменения (без флага — dry-run)")
    parser.add_argument("--top", type=int, default=30,
                        help="Кол-во документов для --archetypes")
    args = parser.parse_args()

    if not any([args.analyze, args.archetypes,
                getattr(args, "dat_demo", False), args.import_graph]):
        parser.print_help()
        return

    if args.analyze:
        analyze_intersections()

    if args.archetypes:
        show_archetypes(args.top)

    if getattr(args, "dat_demo", False):
        dat_demo()

    if args.import_graph:
        import_graph(args.graph_path, dry_run=not args.apply)


if __name__ == "__main__":
    main()
