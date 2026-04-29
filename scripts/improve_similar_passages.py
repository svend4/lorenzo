"""
improve_similar_passages.py — поиск похожих абзацев между файлами (TF-IDF cosine).

Полезно для:
  - Нахождения дублирующегося контента в разных секциях
  - Кандидатов для слияния документов
  - Обнаружения «скопированных» блоков

Алгоритм:
  1. Разбивает все файлы на абзацы (≥ MIN_WORDS слов)
  2. Считает TF-IDF вектор каждого абзаца
  3. Находит пары с cosine similarity ≥ MIN_SIM (только из разных файлов)

Создаёт docs/SIMILAR_PASSAGES.md.
Запуск:
    python scripts/improve_similar_passages.py
    python scripts/improve_similar_passages.py --section 02-anthropic-vacancies
    python scripts/improve_similar_passages.py --min-sim 0.6
    python scripts/improve_similar_passages.py --min-words 30
    python scripts/improve_similar_passages.py --top 30
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

MIN_SIM = 0.5
MIN_WORDS = 20
TOP = 25

if "--min-sim" in sys.argv:
    idx = sys.argv.index("--min-sim")
    if idx + 1 < len(sys.argv):
        MIN_SIM = float(sys.argv[idx + 1])

if "--min-words" in sys.argv:
    idx = sys.argv.index("--min-words")
    if idx + 1 < len(sys.argv):
        MIN_WORDS = int(sys.argv[idx + 1])

if "--top" in sys.argv:
    idx = sys.argv.index("--top")
    if idx + 1 < len(sys.argv):
        TOP = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "SIMILAR_PASSAGES.md", "SEARCH.md", "CONTRADICTIONS.md",
    "PARAGRAPH_QUALITY.md", "VOCABULARY.md", "KEYWORD_INDEX.md",
    "HEADING_AUDIT.md", "PASSIVE_VOICE.md", "QUESTIONS.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "он", "она", "они", "при", "от", "до", "об", "же", "бы", "ли",
    "the", "a", "an", "is", "are", "of", "in", "on", "to", "for",
    "with", "by", "and", "not", "it", "we", "be", "was", "were",
}


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[*_`#|>\[\]()]', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
            if t not in STOPWORDS]


def _extract_passages(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return []
    rel = str(path.relative_to(ROOT))
    paras = re.split(r'\n{2,}', text)
    passages = []
    for para in paras:
        clean = _clean(para)
        tokens = _tokenize(clean)
        if len(tokens) < MIN_WORDS:
            continue
        passages.append({
            "source": rel,
            "text": clean[:300],
            "tokens": tokens,
        })
    return passages


def _tfidf_vectors(passages: list[dict]) -> list[dict]:
    N = len(passages)
    df: Counter = Counter()
    for p in passages:
        for t in set(p["tokens"]):
            df[t] += 1

    idf = {t: math.log((N + 1) / (n + 1)) for t, n in df.items()}

    for p in passages:
        freq = Counter(p["tokens"])
        total = len(p["tokens"])
        vec = {}
        for t, tf in freq.items():
            vec[t] = (tf / total) * idf.get(t, 0)
        p["vec"] = vec

    return passages


def _cosine(a: dict, b: dict) -> float:
    common = set(a) & set(b)
    if not common:
        return 0.0
    dot = sum(a[t] * b[t] for t in common)
    norm_a = math.sqrt(sum(v * v for v in a.values()))
    norm_b = math.sqrt(sum(v * v for v in b.values()))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def find_similar(passages: list[dict]) -> list[dict]:
    """Ищет похожие абзацы через инвертированный индекс (не O(n²))."""
    # Строим инвертированный индекс term → [passage_idx]
    inv: dict[str, list[int]] = defaultdict(list)
    for i, p in enumerate(passages):
        for t in set(p.get("vec", {})):
            inv[t].append(i)

    seen: set[tuple] = set()
    pairs = []

    for t, idxs in inv.items():
        if len(idxs) < 2 or len(idxs) > 100:
            continue
        for ii in range(len(idxs)):
            for jj in range(ii + 1, len(idxs)):
                i, j = idxs[ii], idxs[jj]
                key = (min(i, j), max(i, j))
                if key in seen:
                    continue
                seen.add(key)

                pi, pj = passages[i], passages[j]
                if pi["source"] == pj["source"]:
                    continue

                sim = _cosine(pi.get("vec", {}), pj.get("vec", {}))
                if sim >= MIN_SIM:
                    pairs.append({
                        "sim": round(sim, 3),
                        "source_a": pi["source"],
                        "text_a": pi["text"],
                        "source_b": pj["source"],
                        "text_b": pj["text"],
                    })

    return sorted(pairs, key=lambda x: -x["sim"])


def main() -> None:
    print("🔗 improve_similar_passages.py — похожие абзацы (TF-IDF cosine)")
    print(f"   MIN_SIM={MIN_SIM} | MIN_WORDS={MIN_WORDS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md"))
             if f.name not in SKIP_FILES
             and "-parts" not in str(f)
             and "obsidian" not in str(f)]
    print(f"   Файлов: {len(files)}")

    all_passages = []
    for f in files:
        all_passages.extend(_extract_passages(f))
    print(f"   Абзацев: {len(all_passages)}")

    all_passages = _tfidf_vectors(all_passages)
    print("   Поиск похожих...", end=" ", flush=True)
    pairs = find_similar(all_passages)
    print(f"найдено: {len(pairs)}\n")

    lines = [
        "# Похожие абзацы между документами\n",
        f"_Обновлено: {TODAY}_\n",
        f"Абзацев: **{len(all_passages)}** | Похожих пар: **{len(pairs)}** "
        f"(мин. сходство: {MIN_SIM})\n",
        "> Высокое сходство = кандидаты на слияние или дедупликацию.\n",
    ]

    if pairs:
        lines += ["## Найденные похожие абзацы\n"]
        for i, p in enumerate(pairs[:TOP], 1):
            lines += [
                f"### {i}. Сходство: {p['sim']} ({p['sim']*100:.0f}%)\n",
                f"**A:** `{p['source_a']}`",
                f"> {p['text_a'][:150]}\n",
                f"**B:** `{p['source_b']}`",
                f"> {p['text_b'][:150]}\n",
                "---\n",
            ]
    else:
        lines.append("_Похожих абзацев не найдено при текущем пороге._\n")

    out = DOCS / "SIMILAR_PASSAGES.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  похожих пар: {len(pairs)}")
    if pairs:
        print(f"  топ сходство: {pairs[0]['sim']}")


if __name__ == "__main__":
    main()
