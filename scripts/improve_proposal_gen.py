"""
improve_proposal_gen.py — Автогенерация proposal-карточек интеграции проектов.

Сравнивает все пары проектов из docs/05-habr-projects/ и docs/CONTACTS.md,
вычисляет тематическое сходство и архитектурную комплементарность,
генерирует proposal-карточки для топ-N пар.

Логика:
  1. Загружает проектные файлы из 05-habr-projects/ (9 богатых файлов)
  2. Для каждой пары вычисляет: TF-IDF сходство + слой-комплементарность
  3. Пары с высокой комплементарностью (разные слои, высокое сходство) → proposals
  4. Создаёт Card Envelope с card_type=proposal, state=raw

Архитектурные слои (для комплементарности):
  memory:       yodoca, ngt-memory, agent-memory-mcp, memnet
  knowledge:    agentfs, knowledge-space, mclaude, wikontic
  ingestion:    research-docs-liteparse, rufler
  orchestration: mclaude, rufler

Использование:
  python scripts/improve_proposal_gen.py --dry-run      # показать топ-10 пар
  python scripts/improve_proposal_gen.py --apply        # создать карточки
  python scripts/improve_proposal_gen.py --top 20       # топ-20 пар
  python scripts/improve_proposal_gen.py --min-sim 0.1  # порог сходства
  python scripts/improve_proposal_gen.py --stats        # существующие proposals
"""
import re
import sys
import json
import math
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from collections import Counter
from itertools import combinations

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
HABR    = DOCS / "05-habr-projects"
COLLABS = DOCS / "04-ai-collaborations"

# Слои архитектуры Svyazi 2.0
LAYER_MAP = {
    "yodoca":                  "memory",
    "ngt-memory":              "memory",
    "agent-memory-mcp":        "memory",
    "memnet":                  "memory",
    "agentfs":                 "knowledge",
    "knowledge-space":         "knowledge",
    "wikontic":                "knowledge",
    "mclaude":                 "orchestration",
    "rufler":                  "orchestration",
    "research-docs-liteparse": "ingestion",
}

# Авторы проектов
AUTHOR_MAP = {
    "yodoca":                  "VitalyOborin",
    "ngt-memory":              "spbmolot",
    "agent-memory-mcp":        "VitaliySemenov",
    "memnet":                  "Antipozitive",
    "agentfs":                 "kksudo",
    "knowledge-space":         "AnastasiyaW",
    "mclaude":                 "AnastasiyaW",
    "wikontic":                "VitalyOborin",
    "rufler":                  "zodigancode",
    "research-docs-liteparse": "nlaik",
}

# Шаблоны гипотез по комбинациям слоёв
HYPOTHESIS_TEMPLATES = {
    ("memory", "knowledge"): (
        "{a} обеспечивает персистентную память эпизодов, "
        "{b} хранит структурированный граф знаний. "
        "Интеграция: episodes из {a} как узлы графа в {b} — "
        "контекстно-зависимый retrieval с временно́й семантикой."
    ),
    ("memory", "orchestration"): (
        "{a} типизирует memory-примитивы (episode/fact/proposal), "
        "{b} оркестрирует агентов через декларативные пайплайны. "
        "Интеграция: {b} читает релевантный контекст из {a} "
        "перед каждым шагом пайплайна — stateful orchestration."
    ),
    ("memory", "ingestion"): (
        "{a} хранит знания с decay и consolidation, "
        "{b} извлекает структурированные данные из документов. "
        "Интеграция: extracted evidence из {b} → episodes в {a} — "
        "автоматическое накопление верифицированных фактов."
    ),
    ("knowledge", "orchestration"): (
        "{a} предоставляет файловую систему знаний с рёбрами, "
        "{b} управляет агентными пайплайнами. "
        "Интеграция: {b} навигирует по {a} как по рабочему пространству — "
        "граф как рабочая память оркестратора."
    ),
    ("knowledge", "ingestion"): (
        "{a} хранит знания в виде графа документов, "
        "{b} парсит и извлекает структуру из сырых источников. "
        "Интеграция: {b} → Card Envelope → {a} — "
        "автоматическое обогащение графа из внешних источников."
    ),
    ("orchestration", "ingestion"): (
        "{a} декларативно описывает агентные workflow, "
        "{b} автоматизирует ingestion документов. "
        "Интеграция: {a} как планировщик batch-обогащения через {b} — "
        "scheduled knowledge harvesting."
    ),
    ("memory", "memory"): (
        "{a} и {b} — разные подходы к агентной памяти. "
        "Интеграция: {a} как hot-cache быстрых ассоциаций, "
        "{b} как cold-store долгосрочных фактов — двухуровневая память."
    ),
    ("knowledge", "knowledge"): (
        "{a} и {b} — разные модели представления знаний. "
        "Интеграция: {a} как файловый бэкенд, {b} как семантический слой — "
        "knowledge graph с файловой персистентностью."
    ),
}


# ── TF-IDF утилиты ───────────────────────────────────────────────────────────

STOPWORDS = {"и", "в", "на", "что", "как", "это", "для", "или", "но", "из",
             "по", "с", "к", "о", "от", "до", "за", "при", "не", "а", "же",
             "the", "a", "an", "of", "in", "to", "is", "are", "for", "it",
             "that", "with", "as", "by", "be", "at", "this", "from", "or"}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[а-яёa-z][а-яёa-z0-9\-]{2,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def build_tfidf(docs: dict[str, str]) -> dict[str, dict[str, float]]:
    N = len(docs)
    tf_docs = {name: Counter(tokenize(text)) for name, text in docs.items()}
    df: Counter = Counter()
    for tf in tf_docs.values():
        for term in tf:
            df[term] += 1
    idf = {t: math.log(N / (n + 1)) + 1 for t, n in df.items()}
    vectors: dict[str, dict[str, float]] = {}
    for name, tf in tf_docs.items():
        total = sum(tf.values()) or 1
        vec = {t: (c / total) * idf.get(t, 1) for t, c in tf.items()}
        norm = sum(v * v for v in vec.values()) ** 0.5
        vectors[name] = {t: v / norm for t, v in vec.items()} if norm else {}
    return vectors


def cosine(va: dict[str, float], vb: dict[str, float]) -> float:
    return sum(va.get(k, 0) * vb.get(k, 0) for k in set(va) | set(vb))


# ── Загрузка проектов ────────────────────────────────────────────────────────

def load_projects() -> dict[str, dict]:
    projects: dict[str, dict] = {}
    for md_file in HABR.rglob("*.md"):
        if md_file.name in ("README.md", "QA.md"):
            continue
        stem = md_file.stem.lower()
        text = md_file.read_text(encoding="utf-8", errors="ignore")
        # Определить слой
        layer = "unknown"
        for key, lyr in LAYER_MAP.items():
            if key in stem:
                layer = lyr
                break
        projects[stem] = {
            "path":   md_file,
            "text":   text,
            "layer":  layer,
            "author": AUTHOR_MAP.get(stem, "?"),
            "name":   stem,
        }
    return projects


# ── Генерация гипотез ────────────────────────────────────────────────────────

def _make_hypothesis(pa: dict, pb: dict, similarity: float) -> str:
    la, lb = pa["layer"], pb["layer"]
    key = (la, lb) if (la, lb) in HYPOTHESIS_TEMPLATES else (lb, la)
    template = HYPOTHESIS_TEMPLATES.get(
        key,
        "{a} и {b} — взаимодополняющие компоненты Knowledge OS. "
        "Интеграция открывает синергию через общий Card Envelope контракт."
    )
    return template.format(a=pa["name"].title(), b=pb["name"].title())


def _complementarity_bonus(la: str, lb: str) -> float:
    """Разные слои дают бонус к рейтингу пары."""
    if la == lb:
        return 0.0
    pairs = {frozenset(["memory", "knowledge"]): 0.3,
             frozenset(["memory", "ingestion"]): 0.25,
             frozenset(["knowledge", "ingestion"]): 0.25,
             frozenset(["orchestration", "memory"]): 0.2,
             frozenset(["orchestration", "knowledge"]): 0.2,
             frozenset(["orchestration", "ingestion"]): 0.15}
    return pairs.get(frozenset([la, lb]), 0.1)


# ── Создание карточки ─────────────────────────────────────────────────────────

def _write_proposal(pa: dict, pb: dict, hypothesis: str,
                    similarity: float, score: float) -> Path:
    date     = datetime.now().strftime("%Y-%m-%d")
    na, nb   = pa["name"], pb["name"]
    card_id  = hashlib.sha256(f"proposal:{na}:{nb}".encode()).hexdigest()[:12]
    slug     = f"proposal-{re.sub(r'[^a-z0-9]+', '-', na)}-x-{re.sub(r'[^a-z0-9]+', '-', nb)}"[:70]
    tags_str = f"proposal, {na}, {nb}, {pa['layer']}, {pb['layer']}, integration"

    content = f"""## Гипотеза интеграции

{hypothesis}

## Проекты

| Параметр | {na.title()} | {nb.title()} |
|----------|{'—' * len(na)}|{'—' * len(nb)}|
| Слой | {pa['layer']} | {pb['layer']} |
| Автор | {pa['author']} | {pb['author']} |
| Файл | `{pa['path'].relative_to(ROOT)}` | `{pb['path'].relative_to(ROOT)}` |

## Метрики совместимости

| Метрика | Значение |
|---------|---------|
| Тематическое сходство (TF-IDF cosine) | {similarity:.3f} |
| Комплементарность слоёв | {"✅ высокая" if pa['layer'] != pb['layer'] else "⚠ одинаковый слой"} |
| Итоговый рейтинг | {score:.3f} |

## Архитектурный контракт

Точка интеграции: **Card Envelope** (`card_type="{na}"`, edges к `{nb}`).

```json
{{
  "card_type": "integration_proposal",
  "state": "raw",
  "projects": ["{na}", "{nb}"],
  "contract": "Card Envelope §3.1",
  "layer_a": "{pa['layer']}",
  "layer_b": "{pb['layer']}"
}}
```

## Следующие шаги

- [ ] Изучить API {na.title()} и {nb.title()}
- [ ] Определить точку интеграции (Card Envelope / MCP)
- [ ] Связаться с {pa['author']} и {pb['author']}
- [ ] Создать proof-of-concept (≤ 1 неделя)
- [ ] Написать RFC в docs/rfcs/

## Статус ревью

- [ ] Одобрено
- [ ] Отклонено
- [ ] Отложено
"""

    md = f"""---
title: "Proposal: {na.title()} × {nb.title()}"
date: {date}
card_id: {card_id}
card_type: proposal
state: raw
tags: [{tags_str}]
projects: [{na}, {nb}]
similarity: {similarity:.3f}
score: {score:.3f}
source: proposal-gen
---

# Proposal: {na.title()} × {nb.title()}

<!-- summary -->
> Интеграция {pa['layer']}-слоя ({na.title()}) и {pb['layer']}-слоя ({nb.title()}): {hypothesis[:120]}

<!-- tags: {tags_str} -->

{content}

---
_Сгенерировано improve_proposal_gen.py: {date}_
"""
    target = COLLABS / "proposals"
    target.mkdir(parents=True, exist_ok=True)
    filepath = target / f"{slug}.md"
    filepath.write_text(md, encoding="utf-8")
    return filepath


def _proposal_exists(na: str, nb: str) -> bool:
    target = COLLABS / "proposals"
    if not target.exists():
        return False
    slug_part = f"{re.sub(r'[^a-z0-9]+', '-', na)}-x-{re.sub(r'[^a-z0-9]+', '-', nb)}"
    for f in target.glob("*.md"):
        if slug_part in f.name or f"{re.sub(r'[^a-z0-9]+', '-', nb)}-x-{re.sub(r'[^a-z0-9]+', '-', na)}" in f.name:
            return True
    return False


# ── Главная логика ───────────────────────────────────────────────────────────

def run(dry_run: bool, top: int, min_sim: float, stats_only: bool):
    if stats_only:
        target = COLLABS / "proposals"
        existing = list(target.glob("*.md")) if target.exists() else []
        print(f"📊 Proposal Generator статистика:")
        print(f"  Существующих proposals: {len(existing)}")
        print(f"  Проектных файлов: {sum(1 for _ in HABR.rglob('*.md') if _.name not in ('README.md', 'QA.md'))}")
        return

    projects = load_projects()
    if not projects:
        print(f"❌ Проектные файлы не найдены в {HABR}")
        return

    print(f"📋 Proposal Generator {'[dry-run]' if dry_run else '[apply]'}")
    print(f"   Проектов загружено: {len(projects)}")

    # TF-IDF векторы
    texts   = {name: p["text"] for name, p in projects.items()}
    vectors = build_tfidf(texts)

    # Все пары
    pairs: list[tuple] = []
    names = list(projects.keys())
    for na, nb in combinations(names, 2):
        sim   = cosine(vectors.get(na, {}), vectors.get(nb, {}))
        bonus = _complementarity_bonus(projects[na]["layer"], projects[nb]["layer"])
        score = sim + bonus
        if sim >= min_sim:
            pairs.append((score, sim, na, nb))

    pairs.sort(reverse=True)
    top_pairs = pairs[:top]

    print(f"   Пар найдено: {len(pairs)} | Показываем топ-{top}\n")

    created = 0
    skipped = 0

    for score, sim, na, nb in top_pairs:
        pa, pb = projects[na], projects[nb]
        hypothesis = _make_hypothesis(pa, pb, sim)
        print(f"  [{score:.3f}] {na.title()} × {nb.title()}")
        print(f"    Слои: {pa['layer']} + {pb['layer']} | sim={sim:.3f}")
        print(f"    {hypothesis[:100]}...")

        if _proposal_exists(na, nb):
            print(f"    ⏭ Уже существует, пропуск")
            skipped += 1
            continue

        if not dry_run:
            path = _write_proposal(pa, pb, hypothesis, sim, score)
            print(f"    ✅ {path.relative_to(ROOT)}")
            created += 1
        print()

    if not dry_run and created:
        import subprocess
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "improve_index_update.py")],
            cwd=ROOT, capture_output=True, timeout=60,
        )
        print(f"\n✅ Создано proposals: {created} | Пропущено (уже есть): {skipped}")
        _write_proposals_index()
    elif dry_run:
        print(f"\nℹ️  Запустите с --apply чтобы создать {len(top_pairs) - skipped} proposals")


def _write_proposals_index():
    target = COLLABS / "proposals"
    cards  = sorted(target.glob("*.md"))
    lines  = ["# Proposals — Гипотезы интеграции\n",
               f"_Обновлено: {datetime.now().strftime('%Y-%m-%d')}_\n",
               f"Всего proposals: {len(cards)}\n"]
    for c in cards:
        text  = c.read_text(encoding="utf-8", errors="ignore")
        title = re.search(r"^#\s+(.+)", text, re.MULTILINE)
        lines.append(f"- [{title.group(1) if title else c.stem}]({c.name})")
    (target / "README.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Proposal Generator: автогенерация гипотез интеграции")
    parser.add_argument("--dry-run",  action="store_true", default=True)
    parser.add_argument("--apply",    action="store_true")
    parser.add_argument("--top",      type=int,   default=10, help="Топ N пар (по умолч. 10)")
    parser.add_argument("--min-sim",  type=float, default=0.05, help="Минимальное сходство (по умолч. 0.05)")
    parser.add_argument("--stats",    action="store_true")
    args = parser.parse_args()
    run(dry_run=not args.apply, top=args.top, min_sim=args.min_sim, stats_only=args.stats)


if __name__ == "__main__":
    main()
