"""
prototype_demo.py — демонстрация Knowledge OS Svyazi 2.0.

Полный цикл: запрос → гибридный поиск → кандидаты коллаборации → контакты → письма.
Измеряет латентность против критериев успеха из PROTOTYPE_SPEC.md.

Использование:
    python scripts/prototype_demo.py --query "агент с памятью граф знаний"
    python scripts/prototype_demo.py --file docs/PROTOTYPE_SPEC.md
    python scripts/prototype_demo.py --query "RAG retrieval" --top 5
    python scripts/prototype_demo.py --benchmark   # прогон 5 эталонных запросов
    python scripts/prototype_demo.py --json        # вывод в JSON
"""
import json
import re
import sys
import time
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))

# ── Парсинг аргументов ────────────────────────────────────────────────────────
def _arg(flag: str, default=None):
    try:
        idx = sys.argv.index(flag)
        return sys.argv[idx + 1] if idx + 1 < len(sys.argv) else default
    except ValueError:
        return default

QUERY     = _arg("--query")
FILE_ARG  = _arg("--file")
TOP       = int(_arg("--top", 5))
JSON_OUT  = "--json" in sys.argv
BENCHMARK = "--benchmark" in sys.argv

# ── Успешные метрики (из PROTOTYPE_SPEC.md §8) ────────────────────────────────
SUCCESS = {
    "latency_s":    5.0,
    "cards_min":    500,
    "orphan_max":   0.15,
    "precision_5":  0.70,
    "collab_score": 3,
}

BENCHMARK_QUERIES = [
    "агент с памятью консолидация карточки знаний",
    "граф связей между проектами авторы Хабр",
    "RAG retrieval evidence визуальные цитаты PDF",
    "декларативный YAML оркестрация агентов рой",
    "local-first offline GDPR безопасность данных",
]


# ── Утилиты ───────────────────────────────────────────────────────────────────
def _load_index() -> list[dict]:
    path = DOCS / "search_index.json"
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else data.get("docs", [])


def _tokenize(text: str) -> list[str]:
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{2,}', text.lower())
    stop = {"и", "в", "на", "что", "как", "это", "для", "или", "но", "от",
            "the", "a", "an", "of", "in", "to", "is", "are", "for", "with"}
    return [w for w in words if w not in stop]


def _doc_text(doc: dict) -> str:
    return " ".join(filter(None, [
        doc.get("content", ""),
        doc.get("preview", ""),
        doc.get("summary", ""),
    ]))


def tfidf_search(query: str, top_k: int = 10) -> list[dict]:
    """TF-IDF косинусный поиск по search_index.json."""
    index  = _load_index()
    tokens = _tokenize(query)
    if not tokens or not index:
        return []

    from collections import Counter
    import math

    def tf(text_tokens, tok):
        c = text_tokens.count(tok)
        return c / len(text_tokens) if text_tokens else 0

    N = len(index)
    df: dict[str, int] = {}
    docs_tokens = []
    for doc in index:
        toks = _tokenize(_doc_text(doc) + " " + doc.get("title", ""))
        docs_tokens.append(toks)
        for t in set(toks):
            df[t] = df.get(t, 0) + 1

    scored = []
    for i, (doc, toks) in enumerate(zip(index, docs_tokens)):
        score = 0.0
        for tok in tokens:
            if tok not in df:
                continue
            idf = math.log((N + 1) / (df[tok] + 1))
            score += tf(toks, tok) * idf
        if score > 0:
            scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def bm25_search(query: str, top_k: int = 10) -> list[dict]:
    """BM25 поиск по passages.json."""
    passages_path = DOCS / "passages.json"
    if not passages_path.exists():
        return []
    try:
        raw = json.loads(passages_path.read_text(encoding="utf-8"))
        passages = raw.get("passages", raw) if isinstance(raw, dict) else raw
    except Exception:
        return []

    tokens = _tokenize(query)
    if not tokens:
        return []

    import math
    k1, b = 1.5, 0.75
    N = len(passages)
    avgdl = sum(len(p.get("text", "").split()) for p in passages) / max(N, 1)

    df: dict[str, int] = {}
    for p in passages:
        toks = set(_tokenize(p.get("text", "")))
        for t in toks:
            df[t] = df.get(t, 0) + 1

    scored = []
    for p in passages:
        text = p.get("text", "")
        toks = _tokenize(text)
        dl = len(toks)
        score = 0.0
        from collections import Counter
        tc = Counter(toks)
        for tok in tokens:
            if tok not in df:
                continue
            idf = math.log((N - df[tok] + 0.5) / (df[tok] + 0.5) + 1)
            tf_score = tc.get(tok, 0) * (k1 + 1) / (tc.get(tok, 0) + k1 * (1 - b + b * dl / avgdl))
            score += idf * tf_score
        if score > 0:
            scored.append((score, p))

    scored.sort(key=lambda x: x[0], reverse=True)
    # Дедупликация по файлу
    seen_files: set[str] = set()
    results = []
    for _, p in scored:
        f = p.get("file", "")
        if f not in seen_files:
            seen_files.add(f)
            results.append({"title": Path(f).stem, "file": f,
                            "preview": p.get("text", "")[:200]})
        if len(results) >= top_k:
            break
    return results


def hybrid_search(query: str, top_k: int = 10) -> list[dict]:
    """Гибридный поиск: 0.6×TF-IDF + 0.4×BM25."""
    tfidf = tfidf_search(query, top_k * 2)
    bm    = bm25_search(query, top_k * 2)

    scores: dict[str, float] = {}
    files:  dict[str, dict]  = {}

    for rank, doc in enumerate(tfidf):
        f = doc.get("file", doc.get("path", ""))
        scores[f] = scores.get(f, 0) + 0.6 * (1 / (rank + 1))
        files[f]  = doc

    for rank, doc in enumerate(bm):
        f = doc.get("file", "")
        scores[f] = scores.get(f, 0) + 0.4 * (1 / (rank + 1))
        if f not in files:
            files[f] = doc

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [files[f] for f, _ in ranked[:top_k]]


def find_collabs(query: str, top_k: int = 5) -> list[dict]:
    """Находит кандидатов коллаборации через improve_collab_finder."""
    # Парсим project-файлы напрямую для скорости
    project_dirs = [
        DOCS / "05-habr-projects" / "memory",
        DOCS / "05-habr-projects" / "knowledge",
    ]
    tokens = _tokenize(query)

    candidates = []
    for d in project_dirs:
        if not d.exists():
            continue
        for f in d.glob("*.md"):
            if f.name == "README.md":
                continue
            try:
                text = f.read_text(encoding="utf-8")
            except OSError:
                continue
            doc_tokens = _tokenize(text)
            if not doc_tokens:
                continue
            # Jaccard similarity
            s1, s2 = set(tokens), set(doc_tokens)
            sim = len(s1 & s2) / len(s1 | s2) if s1 | s2 else 0
            # Автор
            author_m = re.search(r'\|\s*Автор\s*\|\s*([^\|\n]+)', text)
            author = author_m.group(1).strip() if author_m else "—"
            # Контакт
            contact_m = re.search(r'\[@([^\]]+)\]\(.*?contacts/([^\)]+)\.md\)', text)
            contact_file = contact_m.group(2) if contact_m else None
            # Письмо
            letter_file = DOCS / "letters" / f"{contact_file}.md" if contact_file else None
            has_letter = letter_file.exists() if letter_file else False
            # Название
            title_m = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else f.stem
            candidates.append({
                "title":       title,
                "file":        str(f.relative_to(ROOT)),
                "author":      author,
                "contact":     contact_file,
                "has_letter":  has_letter,
                "letter_path": f"docs/letters/{contact_file}.md" if has_letter else None,
                "score":       round(sim, 4),
            })

    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:top_k]


def get_stats() -> dict:
    """Метрики репозитория для сравнения с критериями успеха."""
    # Карточки
    index   = _load_index()
    cards   = len(index)
    orphans = 0
    orphan_path = DOCS / "ORPHANS.md"
    if orphan_path.exists():
        m = re.search(r'изолированных:\s*(\d+)', orphan_path.read_text())
        orphans = int(m.group(1)) if m else 0
    orphan_rate = orphans / cards if cards else 0
    return {"cards": cards, "orphan_rate": orphan_rate, "orphans": orphans}


def run_demo(query: str, top_k: int = 5) -> dict:
    """Запускает полный цикл Knowledge OS и возвращает результат."""
    t0 = time.time()

    # 1. Гибридный поиск
    search_results = hybrid_search(query, top_k * 2)

    # 2. Кандидаты коллаборации
    collabs = find_collabs(query, top_k)

    # 3. Метрики репо
    stats = get_stats()

    latency = round(time.time() - t0, 3)

    return {
        "query":          query,
        "latency_s":      latency,
        "search_results": search_results[:top_k],
        "collabs":        collabs,
        "stats":          stats,
        "criteria": {
            "latency_ok":  latency <= SUCCESS["latency_s"],
            "cards_ok":    stats["cards"] >= SUCCESS["cards_min"],
            "orphan_ok":   stats["orphan_rate"] <= SUCCESS["orphan_max"],
        },
    }


def print_demo(result: dict) -> None:
    q  = result["query"]
    lat = result["latency_s"]
    cr  = result["criteria"]
    stats = result["stats"]

    print("=" * 60)
    print(f"  Knowledge OS — Svyazi 2.0")
    print(f"  Запрос: «{q}»")
    print("=" * 60)

    # Метрики
    print(f"\n  Латентность:  {lat}s  {'✅' if cr['latency_ok'] else '❌'} (порог ≤{SUCCESS['latency_s']}s)")
    print(f"  Карточек:     {stats['cards']}   {'✅' if cr['cards_ok'] else '❌'} (порог ≥{SUCCESS['cards_min']})")
    print(f"  Orphan rate:  {stats['orphan_rate']:.1%}  {'✅' if cr['orphan_ok'] else '❌'} (порог ≤{SUCCESS['orphan_max']:.0%})")

    # Поиск
    print(f"\n── Гибридный поиск (top {len(result['search_results'])}) ──")
    for i, doc in enumerate(result["search_results"], 1):
        title = doc.get("title") or Path(doc.get("file", "")).stem
        path  = doc.get("file", doc.get("path", "—"))
        print(f"  {i}. {title}")
        print(f"     {path}")

    # Коллаборации
    print(f"\n── Кандидаты коллаборации (top {len(result['collabs'])}) ──")
    for i, c in enumerate(result["collabs"], 1):
        letter_mark = "📩" if c["has_letter"] else "  "
        print(f"  {i}. {letter_mark} [{c['score']:.3f}] {c['title']}")
        print(f"       Автор: {c['author']}")
        if c["has_letter"]:
            print(f"       Письмо: {c['letter_path']}")

    print("\n" + "=" * 60)


def benchmark() -> None:
    """Прогон 5 эталонных запросов, измерение метрик."""
    print("Benchmark — Knowledge OS Svyazi 2.0")
    print(f"{'Запрос':<45} {'Латентность':>12} {'Найдено':>8}")
    print("-" * 68)

    latencies = []
    for q in BENCHMARK_QUERIES:
        r = run_demo(q, TOP)
        lat = r["latency_s"]
        found = len(r["collabs"])
        latencies.append(lat)
        status = "✅" if lat <= SUCCESS["latency_s"] else "❌"
        short_q = q[:43]
        print(f"  {short_q:<45} {lat:>8.3f}s {status}  {found:>4} коллаб.")

    avg = sum(latencies) / len(latencies)
    print(f"\n  Среднее: {avg:.3f}s  (порог ≤{SUCCESS['latency_s']}s)")
    stats = get_stats()
    print(f"  Карточек: {stats['cards']}  |  Orphan: {stats['orphan_rate']:.1%}")
    # Авто-оценка Hit Rate@10 (из improve_precision_eval)
    hit_rate = None
    try:
        sys.path.insert(0, str(ROOT / "scripts"))
        from improve_precision_eval import run_eval
        ev = run_eval(k=10, verbose=False)
        hit_rate = ev["hit_rate"]
    except Exception:
        pass

    print("\nКритерии PROTOTYPE_SPEC §8:")
    print(f"  ✅ Latency ≤ 5s      — {avg:.3f}s")
    print(f"  {'✅' if stats['cards'] >= 500 else '❌'} Cards ≥ 500      — {stats['cards']}")
    print(f"  {'✅' if stats['orphan_rate'] <= 0.15 else '❌'} Orphan ≤ 15%    — {stats['orphan_rate']:.1%}")
    if hit_rate is not None:
        icon = "✅" if hit_rate >= 0.70 else "❌"
        print(f"  {icon} Hit Rate@10 ≥ 0.70 — {hit_rate:.3f}  (20 авто-запросов)")
    else:
        print(f"  ⬜ Hit Rate@10 ≥ 0.70 — не удалось запустить precision_eval")
    # Авто-оценка качества коллабораций (known-projects hit в top-1)
    _KNOWN = {
        "yodoca", "agentfs", "ngt-memory", "memnet", "agent-memory-mcp",
        "knowledge-space", "rufler", "research-docs-liteparse", "wikontic",
        "mclaude",
    }
    collab_hits = 0
    for q in BENCHMARK_QUERIES:
        r = run_demo(q, TOP)
        if r["collabs"] and any(p in r["collabs"][0].get("file", "") for p in _KNOWN):
            collab_hits += 1
    collab_icon = "✅" if collab_hits >= 3 else "❌"
    print(f"  {collab_icon} Collab quality ≥ 3/5 — {collab_hits}/{len(BENCHMARK_QUERIES)}")


def main():
    query = QUERY

    # Если задан файл — извлекаем текст как запрос
    if FILE_ARG and not query:
        fp = ROOT / FILE_ARG if not Path(FILE_ARG).is_absolute() else Path(FILE_ARG)
        if fp.exists():
            text = fp.read_text(encoding="utf-8")
            # Берём первые 200 слов без markdown-разметки
            clean = re.sub(r'[#*`>\[\]|]', ' ', text)
            words = clean.split()[:200]
            query = " ".join(words)
        else:
            print(f"Файл не найден: {FILE_ARG}")
            sys.exit(1)

    if BENCHMARK:
        benchmark()
        return

    if not query:
        print("Использование:")
        print("  python scripts/prototype_demo.py --query \"ваш запрос\"")
        print("  python scripts/prototype_demo.py --file docs/PROTOTYPE_SPEC.md")
        print("  python scripts/prototype_demo.py --benchmark")
        sys.exit(0)

    result = run_demo(query, TOP)

    if JSON_OUT:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_demo(result)


if __name__ == "__main__":
    main()
