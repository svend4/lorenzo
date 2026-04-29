"""
improve_cross_section.py — граф концептов между секциями.

Показывает какие ключевые понятия встречаются сразу в нескольких секциях
и насколько сильна их связь:
  1. TF-IDF веса ключевых слов по каждой секции
  2. Matrise пересечений (косинусное сходство секций)
  3. Mermaid-граф секций с весами рёбер
  4. Топ-концепты с их «coverage» по секциям

Запуск:
    python scripts/improve_cross_section.py
    python scripts/improve_cross_section.py --top 30     # топ-30 концептов
    python scripts/improve_cross_section.py --min-secs 2 # встречается в ≥2 секциях
    python scripts/improve_cross_section.py --format dot # + Graphviz DOT
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

TOP_CONCEPTS = 40
MIN_SECTIONS = 2
EXPORT_DOT = "--format" in sys.argv and sys.argv[sys.argv.index("--format") + 1] == "dot"

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP_CONCEPTS = int(sys.argv[idx + 1])

if "--min-secs" in sys.argv:
    idx = sys.argv.index("--min-secs")
    if idx + 1 < len(sys.argv):
        MIN_SECTIONS = int(sys.argv[idx + 1])

SKIP_FILES = {
    "KNOWLEDGE_MAP.md", "SEARCH.md", "SUMMARIES.md", "READING_LIST.md",
    "KEYWORD_INDEX.md", "CONTRADICTIONS.md", "SIMILAR_PASSAGES.md",
    "HEADING_AUDIT.md", "PARAGRAPH_QUALITY.md", "PASSIVE_VOICE.md",
    "EMPTY_SECTIONS.md", "QUESTIONS.md", "LANGUAGE_STATS.md",
    "VOCABULARY.md", "NAMED_ENTITIES.md", "CONCEPT_GRAPH.md",
    "CROSS_SECTION.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "так", "все", "они", "же", "том", "был",
    "the", "a", "an", "is", "of", "in", "on", "to", "for", "with",
    "by", "and", "not", "it", "we", "are", "this", "that", "be",
    "docs", "summary", "callout", "tags", "true", "false",
}

SECTION_LABELS = {
    "01-svyazi":               "Svyazi 2.0",
    "02-anthropic-vacancies":  "Anthropic",
    "03-technology-combinations": "Технологии",
    "04-ai-collaborations":    "AI-ансамбли",
    "05-habr-projects":        "Хабр-проекты",
    "contacts":                "Контакты",
    "templates":               "Шаблоны",
}


def _tokenize(text: str) -> list[str]:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return [t for t in re.findall(r'[а-яёa-z]{4,}', text.lower())
            if t not in STOPWORDS]


def _build_section_vectors(docs_dir: Path) -> dict[str, Counter]:
    """TF-суммы токенов по секциям (взвешенные по файлам внутри секции)."""
    sec_tokens: dict[str, list[str]] = defaultdict(list)

    for subdir in sorted(docs_dir.iterdir()):
        if not subdir.is_dir() or subdir.name.startswith("."):
            continue
        sec = subdir.name
        for f in subdir.rglob("*.md"):
            if f.name in SKIP_FILES or "-parts" in str(f):
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except Exception:
                continue
            sec_tokens[sec].extend(_tokenize(text))

    return {sec: Counter(tokens) for sec, tokens in sec_tokens.items()}


def _tfidf(sec_vectors: dict[str, Counter]) -> dict[str, dict[str, float]]:
    """TF-IDF: TF нормированный по секции × IDF по числу секций."""
    N = len(sec_vectors)
    df: Counter = Counter()
    for tokens in sec_vectors.values():
        for t in tokens:
            df[t] += 1

    tfidf: dict[str, dict[str, float]] = {}
    for sec, tokens in sec_vectors.items():
        total = sum(tokens.values()) or 1
        tfidf[sec] = {}
        for t, cnt in tokens.items():
            tf = cnt / total
            idf = math.log((N + 1) / (df[t] + 1)) + 1
            tfidf[sec][t] = round(tf * idf * 1000, 4)

    return tfidf


def _cosine(a: dict[str, float], b: dict[str, float]) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    num = sum(a[t] * b[t] for t in common)
    denom = math.sqrt(sum(v**2 for v in a.values())) * math.sqrt(sum(v**2 for v in b.values()))
    return round(num / denom, 3) if denom else 0.0


def _cross_concepts(tfidf: dict[str, dict[str, float]],
                    top: int, min_secs: int) -> list[dict]:
    """Концепты, присутствующие в ≥ min_secs секциях, отсортированные по охвату."""
    all_terms: set[str] = set()
    for vec in tfidf.values():
        all_terms |= set(vec)

    results = []
    sections = list(tfidf)
    for term in all_terms:
        scores = {sec: tfidf[sec].get(term, 0.0) for sec in sections}
        present = [sec for sec, s in scores.items() if s > 0]
        if len(present) < min_secs:
            continue
        avg = sum(scores[s] for s in present) / len(present)
        results.append({
            "term": term,
            "sections": present,
            "n_secs": len(present),
            "avg_score": round(avg, 4),
            "scores": {s: round(scores[s], 4) for s in sections},
        })

    results.sort(key=lambda x: (-x["n_secs"], -x["avg_score"]))
    return results[:top]


def _mermaid_graph(sections: list[str], sim_matrix: dict,
                   threshold: float = 0.05) -> list[str]:
    lines = ["```mermaid", "graph LR"]
    # Nodes
    for sec in sections:
        label = SECTION_LABELS.get(sec, sec)
        safe = sec.replace("-", "_")
        lines.append(f'    {safe}["{label}"]')
    # Edges
    seen: set[frozenset] = set()
    for i, a in enumerate(sections):
        for b in sections[i+1:]:
            key = frozenset([a, b])
            if key in seen:
                continue
            seen.add(key)
            sim = sim_matrix.get((a, b), 0.0)
            if sim < threshold:
                continue
            weight = round(sim * 100)
            a_safe = a.replace("-", "_")
            b_safe = b.replace("-", "_")
            lines.append(f"    {a_safe} -- {weight}% --> {b_safe}")
    lines.append("```")
    return lines


def _dot_graph(sections: list[str], sim_matrix: dict,
               threshold: float = 0.05) -> str:
    lines = ["digraph cross_section {", '  rankdir=LR;',
             '  node [shape=box, style=filled, fillcolor=lightblue];']
    for sec in sections:
        label = SECTION_LABELS.get(sec, sec)
        safe = sec.replace("-", "_")
        lines.append(f'  {safe} [label="{label}"];')
    seen: set[frozenset] = set()
    for a in sections:
        for b in sections:
            if a == b:
                continue
            key = frozenset([a, b])
            if key in seen:
                continue
            seen.add(key)
            sim = sim_matrix.get((a, b), 0.0)
            if sim < threshold:
                continue
            a_safe = a.replace("-", "_")
            b_safe = b.replace("-", "_")
            lines.append(f'  {a_safe} -> {b_safe} [label="{sim:.2f}", '
                         f'penwidth={max(1, int(sim * 10))}];')
    lines.append("}")
    return "\n".join(lines)


def main() -> None:
    print("🔗 improve_cross_section.py — концептуальные мосты между секциями")
    print(f"   TOP={TOP_CONCEPTS}, MIN_SECTIONS={MIN_SECTIONS}\n")

    print("   Строю TF-IDF векторы секций...", end=" ", flush=True)
    sec_vectors = _build_section_vectors(DOCS)
    sections = [s for s in sorted(sec_vectors)
                if s not in {"templates", "badges"}
                and sum(sec_vectors[s].values()) > 100]
    print(f"{len(sections)} секций")

    tfidf = _tfidf({s: sec_vectors[s] for s in sections})

    # Матрица сходства
    sim_matrix: dict[tuple, float] = {}
    for i, a in enumerate(sections):
        for b in sections[i+1:]:
            sim = _cosine(tfidf[a], tfidf[b])
            sim_matrix[(a, b)] = sim
            sim_matrix[(b, a)] = sim

    # Кросс-концепты
    concepts = _cross_concepts(tfidf, TOP_CONCEPTS, MIN_SECTIONS)
    print(f"   Концептов (≥{MIN_SECTIONS} секции): {len(concepts)}")

    # Вывод
    lines = [
        "# Кросс-секционный анализ\n",
        f"_Обновлено: {TODAY}_\n",
        "---\n",
        "## Матрица сходства секций\n",
        "_(косинусное сходство TF-IDF векторов)_\n",
    ]

    # Таблица сходства
    header = "| Секция | " + " | ".join(SECTION_LABELS.get(s, s) for s in sections) + " |"
    sep = "|--------|" + "|".join(["------"] * len(sections)) + "|"
    lines += [header, sep]
    for a in sections:
        row_vals = []
        for b in sections:
            if a == b:
                row_vals.append("**—**")
            else:
                v = sim_matrix.get((a, b), 0.0)
                bar = "█" * int(v * 10) + "░" * (10 - int(v * 10))
                row_vals.append(f"{v:.2f} {bar[:5]}")
        lines.append(f"| `{SECTION_LABELS.get(a, a)}` | " + " | ".join(row_vals) + " |")

    # Mermaid граф
    lines += [
        "\n## Граф связей\n",
        "_(толщина / процент = косинусное сходство × 100)_\n",
    ]
    lines += _mermaid_graph(sections, sim_matrix)

    # Кросс-концепты таблица
    lines += [
        f"\n## Топ-{TOP_CONCEPTS} кросс-секционных концептов\n",
        f"_Присутствуют в ≥ {MIN_SECTIONS} секциях_\n",
        "| Концепт | Секций | Авг. TF-IDF | Присутствует в |",
        "|---------|--------|-------------|----------------|",
    ]
    for c in concepts:
        secs_str = ", ".join(f"`{SECTION_LABELS.get(s, s)}`" for s in c["sections"])
        lines.append(
            f"| `{c['term']}` | {c['n_secs']} | {c['avg_score']:.4f} | {secs_str} |"
        )

    # По каждому концепту — детальная строка сравнения
    lines += [
        "\n## Детальная карта концептов\n",
        "_Для каждого концепта — TF-IDF вес в каждой секции_\n",
    ]
    sec_short = [SECTION_LABELS.get(s, s)[:10] for s in sections]
    header2 = "| Концепт | " + " | ".join(sec_short) + " |"
    sep2 = "|---------|" + "|".join(["------"] * len(sections)) + "|"
    lines += [header2, sep2]
    for c in concepts[:20]:
        vals = []
        for s in sections:
            v = c["scores"].get(s, 0.0)
            if v > 0:
                vals.append(f"**{v:.3f}**")
            else:
                vals.append("—")
        lines.append(f"| `{c['term']}` | " + " | ".join(vals) + " |")

    out = DOCS / "CROSS_SECTION.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")

    if EXPORT_DOT:
        dot_out = DOCS / "cross_section.dot"
        dot_out.write_text(_dot_graph(sections, sim_matrix), encoding="utf-8")
        print(f"  wrote: {dot_out.relative_to(ROOT)}")

    # Итог в консоль
    print(f"\n  Топ-5 кросс-секционных концептов:")
    for c in concepts[:5]:
        secs = ", ".join(SECTION_LABELS.get(s, s) for s in c["sections"])
        print(f"    «{c['term']}» → {c['n_secs']} секции: {secs}")

    print(f"\n  Топ-3 связанных пары секций:")
    sorted_pairs = sorted(sim_matrix.items(), key=lambda x: -x[1])
    seen_p: set[frozenset] = set()
    count = 0
    for (a, b), sim in sorted_pairs:
        key = frozenset([a, b])
        if key in seen_p:
            continue
        seen_p.add(key)
        print(f"    {SECTION_LABELS.get(a, a)} ↔ {SECTION_LABELS.get(b, b)}: {sim:.3f}")
        count += 1
        if count >= 3:
            break


if __name__ == "__main__":
    main()
