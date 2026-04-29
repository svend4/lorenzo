"""
improve_complexity.py — оценка читаемости документов.
Метрики: длина предложений, плотность терминов, глубина вложенности заголовков.
Создаёт docs/COMPLEXITY.md.
Запуск: python scripts/improve_complexity.py
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

TECH_TERMS = [
    "mcp", "rag", "llm", "api", "sdk", "crdt", "tfidf", "cosine",
    "svyazi", "cardindex", "agentfs", "sentinel", "rufler", "yodoca",
    "envelope", "allowlist", "quarantine", "embedding", "vector",
    "jaccard", "faiss", "mermaid", "yaml", "json", "oauth", "jwt",
]

SKIP = {"COMPLEXITY.md", "WORD_FREQ.md", "COMPARE.md", "DENSITY.md"}


def strip_md(text: str) -> str:
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'[#*_`>|]', ' ', text)
    return text


def avg_sentence_len(text: str) -> float:
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if len(s.split()) >= 3]
    if not sentences:
        return 0
    return sum(len(s.split()) for s in sentences) / len(sentences)


def term_density(text: str) -> float:
    words = text.lower().split()
    if not words:
        return 0
    hits = sum(1 for w in words if w in TECH_TERMS)
    return hits / len(words) * 100


def heading_depth(text: str) -> int:
    depths = [len(m.group(1)) for m in re.finditer(r'^(#{1,6})\s', text, re.MULTILINE)]
    return max(depths) if depths else 0


def complexity_score(avg_sent: float, term_dens: float, depth: int, words: int) -> int:
    score = 0
    if avg_sent > 25: score += 2
    elif avg_sent > 15: score += 1
    if term_dens > 3: score += 2
    elif term_dens > 1: score += 1
    if depth >= 4: score += 1
    if words > 3000: score += 2
    elif words > 1000: score += 1
    return min(score, 5)


LEVEL = {0: "🟢 Простой", 1: "🟢 Простой", 2: "🟡 Средний",
          3: "🟡 Средний", 4: "🔴 Сложный", 5: "🔴 Сложный"}


def main():
    print("Оценка читаемости...")
    rows = []

    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP:
            continue
        raw = f.read_text(encoding="utf-8")
        if len(raw) < 200:
            continue
        clean = strip_md(raw)
        words = len(clean.split())
        avg_sent = avg_sentence_len(clean)
        term_d   = term_density(clean)
        depth    = heading_depth(raw)
        score    = complexity_score(avg_sent, term_d, depth, words)
        rows.append({
            "file":     str(f.relative_to(ROOT)),
            "words":    words,
            "avg_sent": round(avg_sent, 1),
            "term_d":   round(term_d, 2),
            "depth":    depth,
            "score":    score,
        })

    rows.sort(key=lambda x: -x["score"])

    dist = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in rows:
        dist[r["score"]] += 1

    lines = [
        "# Оценка читаемости документов\n",
        f"**Файлов проанализировано:** {len(rows)}\n",
        "## Распределение сложности\n",
        "| Уровень | Файлов |",
        "|---------|--------|",
        f"| 🟢 Простой (0-1) | {dist[0]+dist[1]} |",
        f"| 🟡 Средний (2-3)  | {dist[2]+dist[3]} |",
        f"| 🔴 Сложный (4-5)  | {dist[4]+dist[5]} |",

        "\n## Самые сложные документы\n",
        "| Документ | Слов | Ср.длина пред. | Термин.плотность | Ур.заголовков | Балл |",
        "|----------|------|---------------|-----------------|--------------|------|",
    ]

    for r in rows[:25]:
        short = r["file"].split("/")[-1].replace(".md", "")[:35]
        lines.append(
            f"| `{short}` | {r['words']} | {r['avg_sent']} | "
            f"{r['term_d']}% | H{r['depth']} | {LEVEL[r['score']]} |"
        )

    lines += ["\n## Самые простые документы\n",
              "| Документ | Слов | Балл |",
              "|----------|------|------|"]
    for r in sorted(rows, key=lambda x: x["score"])[:15]:
        short = r["file"].split("/")[-1].replace(".md", "")[:40]
        lines.append(f"| `{short}` | {r['words']} | {LEVEL[r['score']]} |")

    lines += [
        "\n## Методология\n",
        "- **Средняя длина предложения** > 25 слов → +2 балла",
        "- **Терминологическая плотность** > 3% → +2 балла",
        "- **Глубина заголовков** H4+ → +1 балл",
        "- **Объём** > 3000 слов → +2 балла",
    ]

    out = DOCS / "COMPLEXITY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    simple = dist[0] + dist[1]
    medium = dist[2] + dist[3]
    hard   = dist[4] + dist[5]
    print(f"  простых: {simple}, средних: {medium}, сложных: {hard}")


if __name__ == "__main__":
    main()
