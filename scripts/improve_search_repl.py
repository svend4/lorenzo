"""
improve_search_repl.py — интерактивный поисковый терминал (REPL).

Объединяет несколько поисковых движков в одном интерфейсе:
  • BM25-поиск по абзацам (из passages.json или live-индекс)
  • Полнотекстовый поиск по всем docs/
  • Навигация по результатам (:related, :open, :list)

Команды в REPL:
  <запрос>          — BM25-поиск по абзацам
  :full <запрос>    — полнотекстовый поиск
  :list <запрос>    — список файлов по теме (как reading_list)
  :related <файл>   — похожие документы для файла
  :top              — топ-15 самых связанных файлов
  :help             — эта справка
  :exit / Ctrl+C    — выход

Запуск:
    python scripts/improve_search_repl.py
    python scripts/improve_search_repl.py --query "агент память"  # разовый поиск
    python scripts/improve_search_repl.py --index                 # построить индекс заново
"""
import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
PASSAGES_JSON = DOCS / "passages.json"
SEARCH_INDEX  = DOCS / "search_index.json"

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "его", "её", "их", "мы", "вы",
    "при", "от", "до", "об", "the", "a", "an", "is", "of", "in",
    "on", "to", "for", "with", "by", "and", "not", "it", "we",
}

SKIP_FILES = {
    "READING_LIST.md", "SUMMARIES.md", "KNOWLEDGE_MAP.md",
    "SIMILAR_PASSAGES.md", "HEADING_AUDIT.md", "LANGUAGE_STATS.md",
    "PASSIVE_VOICE.md", "EMPTY_SECTIONS.md", "SEARCH_RESULTS.md",
}

TOP = 10  # результатов по умолчанию


# ─────────────────────────────────────────────────────────────────────
# Токенизация
# ─────────────────────────────────────────────────────────────────────

def _tok(text: str) -> list[str]:
    return [t for t in re.findall(r'[а-яёa-z]{3,}', text.lower())
            if t not in STOPWORDS]


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    return re.sub(r'[*_`#|>\[\]()]', ' ', text)


# ─────────────────────────────────────────────────────────────────────
# Построение BM25-индекса (live, если нет passages.json)
# ─────────────────────────────────────────────────────────────────────

def _build_live_index() -> list[dict]:
    """Строит live-индекс абзацев из docs/ (без записи на диск)."""
    print("  Строю live-индекс абзацев...", end="", flush=True)
    passages = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        clean = _clean(text)
        paras = [p.strip() for p in clean.split("\n\n") if len(p.split()) >= 15]
        for para in paras:
            passages.append({
                "file": str(f.relative_to(ROOT)),
                "text": para[:500],
                "tokens": _tok(para),
            })
    print(f" {len(passages)} абзацев из {len(set(p['file'] for p in passages))} файлов")
    return passages


def _load_passages() -> list[dict]:
    if PASSAGES_JSON.exists():
        try:
            raw = json.loads(PASSAGES_JSON.read_text(encoding="utf-8"))
            # Добавляем токены если их нет
            for p in raw:
                if "tokens" not in p:
                    p["tokens"] = _tok(_clean(p.get("text", "")))
            return raw
        except Exception:
            pass
    return _build_live_index()


def _build_bm25(passages: list[dict]) -> dict:
    N = len(passages)
    df: Counter = Counter()
    total_len = 0
    for p in passages:
        total_len += len(p["tokens"])
        for t in set(p["tokens"]):
            df[t] += 1
    avgdl = total_len / max(N, 1)
    idf = {t: math.log((N - n + 0.5) / (n + 0.5) + 1) for t, n in df.items()}
    inv: dict = defaultdict(list)
    for i, p in enumerate(passages):
        freq = Counter(p["tokens"])
        for t, tf in freq.items():
            inv[t].append((i, tf))
    return {"idf": idf, "inv": dict(inv), "avgdl": avgdl,
            "lens": [len(p["tokens"]) for p in passages]}


def _bm25_search(query: str, passages: list[dict], bm25: dict, top: int = TOP) -> list[dict]:
    tokens = _tok(query)
    if not tokens:
        return []
    k1, b = 1.5, 0.75
    avgdl = bm25["avgdl"]
    scores: dict[int, float] = defaultdict(float)
    for t in tokens:
        idf = bm25["idf"].get(t, 0)
        for did, tf in bm25["inv"].get(t, []):
            dl = bm25["lens"][did]
            norm_tf = tf * (k1 + 1) / (tf + k1 * (1 - b + b * dl / avgdl))
            scores[did] += idf * norm_tf

    # Группируем по файлу — берём лучший абзац из каждого
    best_by_file: dict[str, tuple[float, dict]] = {}
    for did, score in sorted(scores.items(), key=lambda x: -x[1]):
        p = passages[did]
        fname = p["file"]
        if fname not in best_by_file or score > best_by_file[fname][0]:
            best_by_file[fname] = (score, p)

    results = sorted(best_by_file.values(), key=lambda x: -x[0])[:top]
    return [{"score": round(s, 2), **p} for s, p in results]


# ─────────────────────────────────────────────────────────────────────
# Полнотекстовый поиск
# ─────────────────────────────────────────────────────────────────────

def _fulltext_search(query: str, top: int = TOP) -> list[dict]:
    tokens = _tok(query)
    if not tokens:
        return []
    results = []
    for f in sorted(DOCS.rglob("*.md")):
        if f.name in SKIP_FILES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        low = text.lower()
        score = sum(low.count(t) for t in tokens)
        if score > 0:
            # Контекст — первое вхождение любого токена
            ctx = ""
            for t in tokens:
                idx = low.find(t)
                if idx >= 0:
                    ctx = text[max(0, idx-30):idx+120].replace("\n", " ").strip()
                    break
            results.append({
                "file": str(f.relative_to(ROOT)),
                "score": score,
                "text": ctx,
            })
    return sorted(results, key=lambda x: -x["score"])[:top]


# ─────────────────────────────────────────────────────────────────────
# Похожие документы для файла (Jaccard на токенах)
# ─────────────────────────────────────────────────────────────────────

def _related(target_file: str, top: int = 5) -> list[dict]:
    target = ROOT / target_file
    if not target.exists():
        # Попробуем найти по имени
        matches = list(DOCS.rglob(f"*{target_file}*"))
        if not matches:
            return []
        target = matches[0]
        target_file = str(target.relative_to(ROOT))

    try:
        toks_a = set(_tok(_clean(target.read_text(encoding="utf-8"))))
    except Exception:
        return []

    results = []
    for f in sorted(DOCS.rglob("*.md")):
        if str(f.relative_to(ROOT)) == target_file or f.name in SKIP_FILES:
            continue
        try:
            toks_b = set(_tok(_clean(f.read_text(encoding="utf-8"))))
        except Exception:
            continue
        if not toks_a or not toks_b:
            continue
        jaccard = len(toks_a & toks_b) / len(toks_a | toks_b)
        if jaccard > 0.05:
            results.append({"file": str(f.relative_to(ROOT)), "score": round(jaccard, 3), "text": ""})

    return sorted(results, key=lambda x: -x["score"])[:top]


# ─────────────────────────────────────────────────────────────────────
# Форматирование вывода
# ─────────────────────────────────────────────────────────────────────

def _fmt_results(results: list[dict], mode: str = "passage") -> str:
    if not results:
        return "  Ничего не найдено.\n"
    lines = []
    for i, r in enumerate(results, 1):
        score_str = f"{r['score']:.2f}" if r.get("score") else ""
        fname = r["file"]
        short = "/".join(fname.split("/")[-2:]) if "/" in fname else fname
        text = r.get("text", "").replace("\n", " ").strip()
        snippet = (text[:100] + "…") if len(text) > 100 else text

        lines.append(f"\n  {i:2}. [{score_str}] {short}")
        if snippet:
            lines.append(f"      {snippet}")
    return "\n".join(lines)


def _print_help() -> None:
    print("""
  Команды:
    <запрос>          BM25-поиск по абзацам (по умолчанию)
    :full <запрос>    Полнотекстовый поиск (считает вхождения слов)
    :list <запрос>    Список файлов по теме с временем чтения
    :related <файл>   Похожие документы (Jaccard на токенах)
    :top              Топ-10 самых цитируемых файлов
    :help             Эта справка
    :exit             Выход (или Ctrl+C / Ctrl+D)

  Примеры:
    > агент память
    > :full Yodoca консолидация
    > :list OSS коллаборации
    > :related docs/05-habr-projects/memory/yodoca.md
    > :top
""")


# ─────────────────────────────────────────────────────────────────────
# Команда :top
# ─────────────────────────────────────────────────────────────────────

def _cmd_top(passages: list[dict]) -> str:
    counts: Counter = Counter(p["file"] for p in passages)
    lines = ["\n  Топ-10 файлов по количеству абзацев:"]
    for fname, n in counts.most_common(10):
        short = "/".join(fname.split("/")[-2:])
        lines.append(f"    {n:4d} абз.  {short}")
    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# REPL
# ─────────────────────────────────────────────────────────────────────

def repl(passages: list[dict], bm25: dict) -> None:
    print("\n" + "═" * 60)
    print("  Lorenzo Search REPL")
    print(f"  Индекс: {len(passages)} абзацев из {len(set(p['file'] for p in passages))} файлов")
    print("  Введите запрос или :help для справки")
    print("═" * 60 + "\n")

    while True:
        try:
            raw = input("  > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n  Выход.")
            break

        if not raw:
            continue

        if raw in (":exit", ":quit", ":q"):
            print("  Выход.")
            break

        if raw == ":help":
            _print_help()
            continue

        if raw == ":top":
            print(_cmd_top(passages))
            continue

        if raw.startswith(":full "):
            query = raw[6:].strip()
            print(f"\n  Полнотекстовый поиск: «{query}»")
            results = _fulltext_search(query)
            print(_fmt_results(results, "full"))
            continue

        if raw.startswith(":related "):
            target = raw[9:].strip()
            print(f"\n  Похожие на: {target}")
            results = _related(target)
            print(_fmt_results(results, "related"))
            continue

        if raw.startswith(":list "):
            query = raw[6:].strip()
            print(f"\n  Список чтения по теме: «{query}»")
            results = _bm25_search(query, passages, bm25, top=15)
            for i, r in enumerate(results, 1):
                fname = r["file"]
                short = "/".join(fname.split("/")[-2:])
                wc = len(r.get("text", "").split())
                rt = max(1, round(wc / 200))
                print(f"  {i:2}. [{rt}мин] {short}")
            continue

        # По умолчанию — BM25
        print(f"\n  BM25-поиск: «{raw}»")
        results = _bm25_search(raw, passages, bm25)
        print(_fmt_results(results))
        print()


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Интерактивный поисковый REPL по документам")
    parser.add_argument("--query", "-q", metavar="ЗАПРОС",
                        help="Разовый поиск без интерактивного режима")
    parser.add_argument("--mode", choices=["bm25", "full", "related", "list"],
                        default="bm25", help="Режим поиска при --query")
    parser.add_argument("--top", type=int, default=TOP,
                        help=f"Количество результатов (по умолчанию {TOP})")
    parser.add_argument("--index", action="store_true",
                        help="Пересобрать live-индекс (игнорировать passages.json)")
    args = parser.parse_args()

    if args.index or not PASSAGES_JSON.exists():
        passages = _build_live_index()
    else:
        passages = _load_passages()

    bm25 = _build_bm25(passages)

    # Разовый поиск (не интерактивный)
    if args.query:
        q = args.query
        if args.mode == "bm25":
            results = _bm25_search(q, passages, bm25, top=args.top)
            print(f"BM25-поиск: «{q}» → {len(results)} результатов")
            print(_fmt_results(results))
        elif args.mode == "full":
            results = _fulltext_search(q, top=args.top)
            print(f"Полнотекстовый поиск: «{q}» → {len(results)} результатов")
            print(_fmt_results(results, "full"))
        elif args.mode == "list":
            results = _bm25_search(q, passages, bm25, top=args.top)
            print(f"Список чтения: «{q}»")
            for i, r in enumerate(results, 1):
                short = "/".join(r["file"].split("/")[-2:])
                print(f"  {i:2}. {short}  [{r['score']:.1f}]")
        elif args.mode == "related":
            results = _related(q, top=args.top)
            print(f"Похожие на: {q}")
            print(_fmt_results(results, "related"))
        return

    repl(passages, bm25)


if __name__ == "__main__":
    main()
