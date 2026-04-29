"""
improve_textrank.py — извлекательное резюме через TextRank (без LLM).

Алгоритм TextRank:
  1. Разбивает текст на предложения
  2. Строит граф сходства (Jaccard на токенах)
  3. Запускает PageRank на графе
  4. Топ-N предложений = резюме

Создаёт docs/SUMMARIES.md + опционально вставляет блок в файлы.
Запуск:
    python scripts/improve_textrank.py               # только отчёт
    python scripts/improve_textrank.py --apply       # вставить в файлы
    python scripts/improve_textrank.py --section 05-habr-projects
    python scripts/improve_textrank.py --sentences 3 # размер резюме
    python scripts/improve_textrank.py --query "агент память"  # резюме под запрос
"""
import re
import sys
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY = "--apply" in sys.argv
SENTENCES = 3
SUMMARY_MARKER = "<!-- textrank-summary -->"

if "--sentences" in sys.argv:
    idx = sys.argv.index("--sentences")
    if idx + 1 < len(sys.argv):
        SENTENCES = int(sys.argv[idx + 1])

QUERY = None
if "--query" in sys.argv:
    idx = sys.argv.index("--query")
    if idx + 1 < len(sys.argv):
        QUERY = sys.argv[idx + 1]

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

MIN_WORDS = 150
DAMPING = 0.85
MAX_ITER = 30

SKIP_FILES = {
    "SUMMARIES.md", "SEARCH.md", "OUTLINE.md", "CONTRADICTIONS.md",
    "PARAGRAPH_QUALITY.md", "VOCABULARY.md", "KEYWORD_INDEX.md",
    "CONCEPT_GRAPH.md", "NAMED_ENTITIES.md", "TIMELINE.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "этот", "его", "её", "их",
    "мы", "вы", "он", "она", "они", "при", "от", "до", "об",
    "the", "a", "an", "is", "are", "of", "in", "on", "to", "for",
    "with", "by", "and", "not", "it", "we", "be", "was", "were",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'^#{1,6}\s+.+$', ' ', text, flags=re.MULTILINE)
    text = re.sub(r'[*_`|>\[\]()]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r'[а-яёa-z]{3,}', text.lower()) if t not in STOPWORDS}


def _split_sentences(text: str) -> list[str]:
    clean = _clean(text)
    sents = re.split(r'(?<=[.!?])\s+', clean)
    return [s.strip() for s in sents if len(s.split()) >= 8]


def _jaccard(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _query_boost(sent_tokens: set, query_tokens: set) -> float:
    if not query_tokens:
        return 0.0
    return len(sent_tokens & query_tokens) / len(query_tokens)


def textrank(sentences: list[str], n: int = 3, query: str | None = None) -> list[str]:
    if len(sentences) <= n:
        return sentences

    token_sets = [_tokenize(s) for s in sentences]
    q_tokens = _tokenize(query) if query else set()

    # Матрица сходства
    N = len(sentences)
    scores = [1.0] * N
    graph: dict[int, list[tuple[int, float]]] = defaultdict(list)

    for i in range(N):
        for j in range(i + 1, N):
            sim = _jaccard(token_sets[i], token_sets[j])
            if sim > 0.05:
                graph[i].append((j, sim))
                graph[j].append((i, sim))

    # PageRank итерации
    for _ in range(MAX_ITER):
        new_scores = [0.0] * N
        for i in range(N):
            incoming = sum(
                w * scores[j] / max(sum(ww for _, ww in graph[j]), 1e-9)
                for j, w in graph[i]
            )
            new_scores[i] = (1 - DAMPING) + DAMPING * incoming
        scores = new_scores

    # Бонус за релевантность запросу
    if q_tokens:
        for i in range(N):
            scores[i] += _query_boost(token_sets[i], q_tokens) * 2.0

    # Топ-N с сохранением порядка
    ranked = sorted(range(N), key=lambda i: -scores[i])[:n]
    top_indices = sorted(ranked)
    return [sentences[i] for i in top_indices]


def summarize_file(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    if len(text.split()) < MIN_WORDS:
        return None

    title_m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    title = title_m.group(1).strip() if title_m else path.stem

    sents = _split_sentences(text)
    if len(sents) < 3:
        return None

    summary_sents = textrank(sents, SENTENCES, QUERY)
    summary = " ".join(summary_sents)

    return {
        "file": str(path.relative_to(ROOT)),
        "title": title,
        "summary": summary,
        "sentences": summary_sents,
        "total_sents": len(sents),
    }


def _insert_summary(path: Path, summary_sents: list[str]) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return False

    block_lines = [
        SUMMARY_MARKER,
        "> **Резюме** (TextRank)",
        ">",
    ]
    for s in summary_sents:
        block_lines.append(f"> {s}")
    block_lines.append(">")
    block = "\n".join(block_lines)

    if SUMMARY_MARKER in text:
        new_text = re.sub(
            rf'{re.escape(SUMMARY_MARKER)}.*?(?=\n[^>]|\Z)',
            block,
            text, flags=re.DOTALL
        )
        if new_text == text:
            return False
    else:
        m = re.search(r'^#\s+.+$', text, re.MULTILINE)
        if m:
            pos = m.end()
            new_text = text[:pos] + "\n\n" + block + "\n" + text[pos:]
        else:
            new_text = block + "\n\n" + text

    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    print("📝 improve_textrank.py — извлекательное резюме (TextRank)")
    print(f"   Предложений в резюме: {SENTENCES} | Damping: {DAMPING}")
    if QUERY:
        print(f"   Запрос: «{QUERY}»")
    print(f"   Режим: {'APPLY' if APPLY else 'report only'}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}\n")

    results = []
    applied = 0
    for f in files:
        res = summarize_file(f)
        if res:
            results.append(res)
            if APPLY:
                if _insert_summary(f, res["sentences"]):
                    applied += 1

    print(f"   Резюмировано: {len(results)} файлов\n")

    lines = [
        "# Резюме документов (TextRank)\n",
        f"_Обновлено: {TODAY}_\n",
        f"Файлов: **{len(results)}** | Предложений: **{SENTENCES}** на документ\n",
    ]
    if QUERY:
        lines.append(f"> Фокус запроса: «{QUERY}»\n")

    for res in results[:50]:
        lines += [
            f"## `{res['file']}`\n",
            f"_{res['title']}_\n",
            f"> {res['summary']}\n",
        ]

    out = DOCS / "SUMMARIES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    if APPLY:
        print(f"  вставлено в файлы: {applied}")
    else:
        print("  Запустите с --apply для вставки резюме в файлы.")


if __name__ == "__main__":
    main()
