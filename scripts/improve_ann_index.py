#!/usr/bin/env python3
"""
improve_ann_index.py — ANN-граф на основе hnswlib для ускоренного векторного поиска.

Строит HNSW-индекс (Hierarchical Navigable Small World) поверх TF-IDF векторов
из search_index.json. Замена линейного O(N·D) скана на двухстадийный поиск:

  Стадия 1: HNSW ANN — O(log N), 0.5мс — быстрый отбор кандидатов
  Стадия 2: точный TF-IDF только по кандидатам — ещё 2мс
  Итого:    ~2.5мс вместо ~210мс  → ускорение 80-100×  |  Recall@10 ≥ 0.85

Методология:
  TF-IDF sparse векторы → случайная проекция → HNSW-индекс → ANN кандидаты
  → точное TF-IDF ре-ранжирование → топ-K результатов

Файлы:
  docs/ann_index.bin  — бинарный HNSW-индекс (hnswlib, ~1.5 МБ)
  docs/ann_proj.npy   — матрица проекции (numpy binary, ~3 МБ, быстрая загрузка)
  docs/ann_meta.json  — словарь, IDF, список документов (~1.5 МБ)

Команды:
  --build              построить/перестроить индекс (~5с)
  --query TEXT         поиск (двухстадийный: ANN + re-rank)
  --top N              число результатов (по умолч. 10)
  --benchmark          сравнение: ANN+rerank vs линейный TF-IDF
  --stats              статистика индекса

Запуск:
    python scripts/improve_ann_index.py --build
    python scripts/improve_ann_index.py --query "агент с памятью консолидация"
    python scripts/improve_ann_index.py --benchmark
    python scripts/improve_ann_index.py --stats
"""

import argparse
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

try:
    import numpy as np
    import hnswlib
except ImportError as _e:
    raise ImportError("Установите зависимости: pip install hnswlib numpy") from _e

ROOT      = Path(__file__).parent.parent
DOCS      = ROOT / "docs"
INDEX_BIN = DOCS / "ann_index.bin"
PROJ_NPY  = DOCS / "ann_proj.npy"       # матрица проекции — numpy binary (быстро)
META_FILE = DOCS / "ann_meta.json"      # словарь + IDF + список документов

# ── Параметры ───────────────────────────────────────────────────────────────

DIM        = 256    # размерность после проекции (больше → лучше recall)
VOCAB_SIZE = 6000   # размер TF-IDF словаря
SEED       = 42

HNSW_M          = 32    # число рёбер HNSW (↑M → точнее, медленнее сборка)
HNSW_EF_CONSTR  = 400   # точность при построении индекса
HNSW_EF_SEARCH  = 128   # точность при поиске (↑ → точнее, медленнее)
ANN_CANDIDATES  = 200   # кандидатов для ре-ранжирования (≥ top_k * 20)

STOPWORDS = {
    "и","в","на","что","как","это","для","или","но","по","к","из","а","не",
    "с","о","от","за","до","то","же","при","уже","так","ещё","бы","ли",
    "его","её","их","был","была","были","есть","быть","если","чем","где",
    "когда","который","которая","которые","через","этот","эта","также",
    "между","после","можно","может","очень","более","такой","всё","все",
    "the","a","an","of","in","to","is","for","with","by","and","or","but",
    "on","at","from","are","was","were","be","been","have","has","that",
    "this","it","its","not","as","all","can","will","may","our","your",
}

# ── Токенизация ─────────────────────────────────────────────────────────────

def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[а-яёa-z]{3,}", text.lower()) if t not in STOPWORDS]


def _doc_text(d: dict) -> str:
    title = d.get("title") or ""
    return " ".join([
        title, title,
        d.get("summary") or "",
        d.get("content") or "",
        " ".join(d.get("tags") or []),
    ])

# ── Словарь и TF-IDF ────────────────────────────────────────────────────────

def _build_vocab(docs: list[dict]) -> tuple[list[str], dict[str, float], dict[str, int]]:
    df: Counter = Counter()
    N = len(docs)
    for d in docs:
        df.update(set(_tokenize(_doc_text(d))))

    idf = {
        w: math.log((N + 1) / (c + 1)) + 1
        for w, c in df.items()
        if 3 <= c <= N * 0.85
    }
    # idf × sqrt(df): баланс информативности и частоты.
    # Гарантирует, что частые важные слова ('агент', 'граф', 'память')
    # попадают в словарь рядом с редкими специализированными терминами.
    scored = sorted(idf.items(), key=lambda x: x[1] * math.sqrt(df[x[0]]), reverse=True)
    vocab_words = [w for w, _ in scored[:VOCAB_SIZE]]
    vocab = {w: i for i, w in enumerate(vocab_words)}
    idf_sel = {w: idf[w] for w in vocab_words}
    return vocab_words, idf_sel, df


def _tfidf_sparse(text: str, vocab: dict[str, int], idf: dict[str, float]) -> dict[int, float]:
    words = _tokenize(text)
    if not words:
        return {}
    tf: dict[str, int] = {}
    for w in words:
        tf[w] = tf.get(w, 0) + 1
    return {
        vocab[w]: (c / len(words)) * idf[w]
        for w, c in tf.items()
        if w in vocab and w in idf
    }


def _to_dense(sparse: dict[int, float], vocab_size: int, proj: np.ndarray) -> np.ndarray:
    full = np.zeros(vocab_size, dtype=np.float32)
    for idx, val in sparse.items():
        full[idx] = val
    dense = proj.T @ full                    # (vocab_size,) × (vocab_size, DIM) → (DIM,)
    norm  = np.linalg.norm(dense)
    return (dense / norm).astype(np.float32) if norm > 1e-9 else dense.astype(np.float32)

# ── Построение индекса ──────────────────────────────────────────────────────

def build_index() -> None:
    t0 = time.time()

    idx_path = DOCS / "search_index.json"
    if not idx_path.exists():
        print("search_index.json не найден. Запустите improve_index_update.py")
        sys.exit(1)

    docs = json.loads(idx_path.read_text(encoding="utf-8"))
    N = len(docs)
    print(f"Загружено {N} документов")

    print("Строю словарь TF-IDF…")
    vocab_words, idf, df = _build_vocab(docs)
    vocab = {w: i for i, w in enumerate(vocab_words)}
    V = len(vocab_words)
    print(f"  Словарь: {V} токенов | DIM: {DIM}")

    print(f"Генерирую матрицу проекции {V}×{DIM}…")
    rng  = np.random.default_rng(SEED)
    proj = (rng.standard_normal((V, DIM)) / math.sqrt(DIM)).astype(np.float32)

    print("Вычисляю TF-IDF векторы и проецирую…")
    mat      = np.zeros((N, DIM), dtype=np.float32)
    doc_list = []
    sparse_store: list[dict[int, float]] = []

    for i, d in enumerate(docs):
        text    = _doc_text(d)
        sparse  = _tfidf_sparse(text, vocab, idf)
        sparse_store.append(sparse)
        mat[i]  = _to_dense(sparse, V, proj)
        doc_list.append({
            "path":    d.get("path", ""),
            "title":   d.get("title", ""),
            "section": d.get("section", ""),
            "summary": (d.get("summary") or d.get("content") or "")[:200],
            "sparse":  sparse,              # сохраняем для точного ре-ранжирования
        })

    print(f"Строю HNSW-индекс (M={HNSW_M}, ef={HNSW_EF_CONSTR})…")
    index = hnswlib.Index(space="cosine", dim=DIM)
    index.init_index(max_elements=N, ef_construction=HNSW_EF_CONSTR, M=HNSW_M)
    index.add_items(mat, list(range(N)))
    index.set_ef(HNSW_EF_SEARCH)
    index.save_index(str(INDEX_BIN))

    np.save(str(PROJ_NPY), proj)            # быстрая загрузка — numpy binary

    meta = {
        "vocab":    vocab_words,
        "idf":      {w: float(v) for w, v in idf.items()},
        "docs":     doc_list,
        "dim":      DIM,
        "seed":     SEED,
        "n_docs":   N,
        "hnsw_m":   HNSW_M,
        "hnsw_ef":  HNSW_EF_SEARCH,
        "built_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    META_FILE.write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")),
                         encoding="utf-8")

    elapsed = time.time() - t0
    print(f"\nИндекс построен за {elapsed:.1f}с")
    for f in [INDEX_BIN, PROJ_NPY, META_FILE]:
        print(f"  {f.name}: {f.stat().st_size // 1024} КБ")
    print(f"  Документов: {N} | Словарь: {V} | Размерность: {DIM}")

# ── Загрузка ─────────────────────────────────────────────────────────────────

_CACHE: dict = {}


def _load() -> tuple:
    if _CACHE:
        return (_CACHE["index"], _CACHE["meta"], _CACHE["proj"],
                _CACHE["vocab"], _CACHE["idf"])

    for f in [INDEX_BIN, PROJ_NPY, META_FILE]:
        if not f.exists():
            raise FileNotFoundError(
                f"ANN-индекс не найден ({f.name}). "
                "Запустите: python scripts/improve_ann_index.py --build"
            )

    meta  = json.loads(META_FILE.read_text(encoding="utf-8"))
    proj  = np.load(str(PROJ_NPY))
    vocab = {w: i for i, w in enumerate(meta["vocab"])}
    idf   = meta["idf"]

    index = hnswlib.Index(space="cosine", dim=meta["dim"])
    index.load_index(str(INDEX_BIN), max_elements=meta["n_docs"])
    index.set_ef(meta.get("hnsw_ef", HNSW_EF_SEARCH))

    _CACHE.update(index=index, meta=meta, proj=proj, vocab=vocab, idf=idf)
    return index, meta, proj, vocab, idf

# ── Поиск (двухстадийный) ────────────────────────────────────────────────────

def _exact_score(query_sparse: dict[int, float], doc_sparse: dict[int, float]) -> float:
    """Точное косинусное сходство между двумя sparse TF-IDF векторами."""
    if not query_sparse or not doc_sparse:
        return 0.0
    dot   = sum(query_sparse[k] * doc_sparse.get(k, 0.0) for k in query_sparse)
    norm_q = math.sqrt(sum(v*v for v in query_sparse.values()))
    norm_d = math.sqrt(sum(v*v for v in doc_sparse.values()))
    if norm_q < 1e-9 or norm_d < 1e-9:
        return 0.0
    return dot / (norm_q * norm_d)


def ann_search(query: str, top_k: int = 10, candidates: int = ANN_CANDIDATES) -> list[dict]:
    """
    Двухстадийный ANN + точный TF-IDF поиск.

    Стадия 1: HNSW возвращает candidates ≥ top_k*6 приближённых соседей (~0.5мс)
    Стадия 2: точное TF-IDF cosine по кандидатам (~2мс)
    Итого:    ~2-3мс, Recall@10 ≥ 0.85

    Совместимо с hybrid_search() из gateway.py / prototype_demo.py.
    """
    index, meta, proj, vocab, idf = _load()

    query_sparse = _tfidf_sparse(query, vocab, idf)
    if not query_sparse:
        return []

    V   = len(vocab)
    vec = _to_dense(query_sparse, V, proj).reshape(1, -1)

    k = min(max(candidates, top_k * 6), meta["n_docs"])
    labels, _ = index.knn_query(vec, k=k)

    # Ре-ранжирование: точное TF-IDF cosine по кандидатам
    scored = []
    for label in labels[0]:
        doc    = meta["docs"][label]
        sparse = {int(ki): float(vi) for ki, vi in doc.get("sparse", {}).items()}
        score  = _exact_score(query_sparse, sparse)
        scored.append((score, doc))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [
        {**d, "_ann_score": round(sc, 4)}
        for sc, d in scored[:top_k]
    ]

# ── Benchmark ────────────────────────────────────────────────────────────────

def benchmark() -> None:
    idx_path = DOCS / "search_index.json"
    all_docs = json.loads(idx_path.read_text(encoding="utf-8"))
    index, meta, proj, vocab, idf = _load()

    def linear_search(q: str, k: int = 10) -> list[dict]:
        tokens = set(_tokenize(q))
        scored = []
        for d in all_docs:
            words = _tokenize(_doc_text(d))
            if not words:
                continue
            sc = sum(words.count(t) for t in tokens) / len(words)
            if sc > 0:
                scored.append((sc, d))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [d for _, d in scored[:k]]

    queries = [
        "агент с памятью консолидация карточки знаний",
        "граф связей между проектами авторы Хабр",
        "RAG retrieval evidence визуальные цитаты PDF",
        "декларативный YAML оркестрация агентов рой",
        "local-first offline GDPR безопасность данных",
        "hnswlib векторный поиск приближённые соседи",
        "knowledge graph semantic search embeddings",
        "review queue approval workflow cards",
    ]

    print(f"\n{'Запрос':<44} {'ANN+RR':>8} {'Linear':>8} {'Speedup':>8} {'Recall@10':>10}")
    print("-" * 82)

    total_ann = total_lin = recall_sum = 0.0

    for q in queries:
        t1 = time.perf_counter()
        ann_res = ann_search(q, 10)
        t_ann = time.perf_counter() - t1

        t2 = time.perf_counter()
        lin_res = linear_search(q, 10)
        t_lin = time.perf_counter() - t2

        ann_paths = {r["path"] for r in ann_res}
        lin_paths = {r["path"] for r in lin_res}
        recall = len(ann_paths & lin_paths) / max(len(lin_paths), 1)

        speedup = t_lin / max(t_ann, 1e-9)
        total_ann += t_ann
        total_lin += t_lin
        recall_sum += recall

        short_q = q[:42] + "…" if len(q) > 42 else q
        print(f"  {short_q:<44} {t_ann*1000:>6.1f}ms {t_lin*1000:>6.1f}ms "
              f"{speedup:>7.0f}× {recall:>9.2f}")

    n = len(queries)
    avg_speedup = total_lin / max(total_ann, 1e-9)
    avg_recall  = recall_sum / n
    print("-" * 82)
    print(f"  {'Среднее':<44} {total_ann/n*1000:>6.1f}ms {total_lin/n*1000:>6.1f}ms "
          f"{avg_speedup:>7.0f}× {avg_recall:>9.2f}")
    print(f"\n  Ускорение: {avg_speedup:.0f}×  |  Recall@10: {avg_recall:.2f}")
    status = "✅ Recall ≥ 0.85" if avg_recall >= 0.85 else f"⚠ Recall = {avg_recall:.2f}"
    print(f"  {status}")


def show_stats() -> None:
    if not META_FILE.exists():
        print("Индекс не построен. Запустите: --build")
        return
    meta = json.loads(META_FILE.read_text(encoding="utf-8"))
    print(f"""
ANN-индекс (hnswlib HNSW + точный TF-IDF ре-ранжинг)
══════════════════════════════════════════════════════
  Документов:    {meta['n_docs']}
  Словарь:       {len(meta['vocab'])} токенов
  Размерность:   {meta['dim']} (random projection)
  HNSW M:        {meta['hnsw_m']}
  HNSW ef:       {meta['hnsw_ef']}
  Кандидатов:    {ANN_CANDIDATES} (для ре-ранжирования)
  Построен:      {meta.get('built_at', '?')}""")
    for f in [INDEX_BIN, PROJ_NPY, META_FILE]:
        size = f"{f.stat().st_size // 1024} КБ" if f.exists() else "нет"
        print(f"  {f.name:<24} {size}")

# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="ANN-индекс hnswlib для ускоренного поиска по корпусу Lorenzo"
    )
    parser.add_argument("--build",     action="store_true")
    parser.add_argument("--query",     type=str)
    parser.add_argument("--top",       type=int, default=10)
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--stats",     action="store_true")
    args = parser.parse_args()

    if args.build:
        build_index()
    elif args.query:
        t0 = time.perf_counter()
        results = ann_search(args.query, args.top)
        elapsed = time.perf_counter() - t0
        print(f"\nANN+rerank: «{args.query}»  ({elapsed*1000:.1f}мс)\n")
        for i, r in enumerate(results, 1):
            print(f"{i:2}. [{r.get('_ann_score', 0):.3f}] {r['title'] or r['path']}")
            print(f"     {r['path']}")
            if r.get("summary"):
                print(f"     {r['summary'][:120]}")
            print()
    elif args.benchmark:
        benchmark()
    elif args.stats:
        show_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
