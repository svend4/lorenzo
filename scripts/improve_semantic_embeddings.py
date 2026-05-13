"""
improve_semantic_embeddings.py — Семантические эмбеддинги для корпуса Lorenzo.

Поддерживает два бэкенда:
  1. sentence-transformers (локально, CPU, ~420MB): paraphrase-multilingual-MiniLM-L12-v2
     - Полноценные 384-мерные векторы
     - Понимает синонимы, контекст, RU+EN смешанный текст
     - pip install sentence-transformers

  2. TF-IDF fallback (всегда доступен, pure Python):
     - Использует существующий индекс из improve_embedding_index.py
     - Не требует дополнительных зависимостей

Результат: docs/semantic_index.json — векторы + HNSW-совместимый формат.

Использование:
  python scripts/improve_semantic_embeddings.py --check      # проверить зависимости
  python scripts/improve_semantic_embeddings.py --index      # построить индекс (ST или TF-IDF fallback)
  python scripts/improve_semantic_embeddings.py --query "агент память"  # поиск
  python scripts/improve_semantic_embeddings.py --compare file1.md file2.md  # сравнить два файла
  python scripts/improve_semantic_embeddings.py --backend tfidf  # принудительно TF-IDF

Интеграция с ANN (hnswlib):
  python scripts/improve_ann_index.py  # после --index пересобирает HNSW-граф
"""
import re
import sys
import json
import math
import time
import argparse
from pathlib import Path
from collections import Counter

ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
INDEX = DOCS / "semantic_index.json"

# ── Проверка зависимостей ────────────────────────────────────────────────────

def check_dependencies() -> dict[str, bool]:
    deps = {}
    try:
        import sentence_transformers
        deps["sentence_transformers"] = True
    except ImportError:
        deps["sentence_transformers"] = False
    try:
        import hnswlib
        deps["hnswlib"] = True
    except ImportError:
        deps["hnswlib"] = False
    try:
        import numpy
        deps["numpy"] = True
    except ImportError:
        deps["numpy"] = False
    return deps


def cmd_check():
    deps = check_dependencies()
    print("🔍 Проверка зависимостей:")
    for pkg, ok in deps.items():
        status = "✅" if ok else "❌"
        print(f"  {status} {pkg}")
    if not deps["sentence_transformers"]:
        print("\n  Для полноценных эмбеддингов:")
        print("  pip install sentence-transformers  (~420MB, работает на CPU)")
        print("\n  Текущий режим: TF-IDF fallback (pure Python, всегда работает)")
    else:
        print("\n  ✅ Все зависимости установлены, доступен ST-режим")


# ── TF-IDF fallback ──────────────────────────────────────────────────────────

STOPWORDS = {"и", "в", "на", "что", "как", "это", "для", "или", "но", "из",
             "по", "с", "к", "о", "от", "до", "за", "при", "не", "а", "же",
             "the", "a", "an", "of", "in", "to", "is", "are", "for", "it"}


def tokenize(text: str) -> list[str]:
    words = re.findall(r"[а-яёa-z][а-яёa-z0-9\-]{1,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def build_tfidf_vectors(docs: dict[str, str]) -> tuple[dict, dict]:
    """Строит TF-IDF векторы. Возвращает (idf, vectors)."""
    N = len(docs)
    tokens_map = {name: tokenize(text) for name, text in docs.items()}

    df: Counter = Counter()
    for tokens in tokens_map.values():
        for t in set(tokens):
            df[t] += 1

    vocab = {t for t, n in df.items() if n >= 2}
    idf   = {t: math.log(N / (df[t] + 1e-9) + 1) + 1 for t in vocab}

    vectors: dict[str, dict[str, float]] = {}
    for name, tokens in tokens_map.items():
        filtered = [t for t in tokens if t in vocab]
        if not filtered:
            vectors[name] = {}
            continue
        total = len(filtered)
        tf  = Counter(filtered)
        vec = {t: (c / total) * idf.get(t, 1) for t, c in tf.items()}
        norm = sum(v * v for v in vec.values()) ** 0.5
        if norm:
            vec = {t: v / norm for t, v in vec.items()}
        # Сохраняем топ-100 компонент
        vectors[name] = dict(sorted(vec.items(), key=lambda x: -x[1])[:100])

    return idf, vectors


def cosine_tfidf(va: dict[str, float], vb: dict[str, float]) -> float:
    return sum(va.get(k, 0) * vb.get(k, 0) for k in set(va) | set(vb))


# ── Sentence Transformers бэкенд ─────────────────────────────────────────────

MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"


def load_st_model():
    from sentence_transformers import SentenceTransformer
    print(f"  Загружаю модель {MODEL_NAME}...")
    return SentenceTransformer(MODEL_NAME)


def build_st_vectors(docs: dict[str, str], model) -> dict[str, list[float]]:
    names  = list(docs.keys())
    texts  = [docs[n][:512] for n in names]  # обрезаем для скорости
    print(f"  Кодирую {len(texts)} документов...")
    t0 = time.time()
    embeddings = model.encode(texts, batch_size=32, show_progress_bar=True,
                               convert_to_numpy=True)
    print(f"  Готово за {time.time() - t0:.1f}с")
    return {name: emb.tolist() for name, emb in zip(names, embeddings)}


def cosine_st(va: list[float], vb: list[float]) -> float:
    dot = sum(a * b for a, b in zip(va, vb))
    na  = sum(a * a for a in va) ** 0.5
    nb  = sum(b * b for b in vb) ** 0.5
    return dot / (na * nb) if na and nb else 0.0


# ── Загрузка корпуса ─────────────────────────────────────────────────────────

def load_corpus(section: str = "", limit: int = 0) -> dict[str, str]:
    base = DOCS / section if section else DOCS
    docs: dict[str, str] = {}
    for p in sorted(base.rglob("*.md")):
        if "obsidian" in p.parts:
            continue
        if p.parent == DOCS and p.stem.isupper():
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
            # Очистить от frontmatter и HTML-комментариев
            text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
            text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
            text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
            if len(text.split()) < 20:
                continue
            docs[str(p.relative_to(ROOT))] = text[:2000]
        except Exception:
            continue
        if limit and len(docs) >= limit:
            break
    return docs


# ── Индексирование ───────────────────────────────────────────────────────────

def cmd_index(backend: str = "auto", section: str = "", limit: int = 0):
    deps = check_dependencies()
    use_st = backend == "st" or (backend == "auto" and deps["sentence_transformers"])

    print(f"📐 Semantic Index [{('sentence-transformers' if use_st else 'TF-IDF fallback')}]")
    print(f"  Загрузка корпуса...")
    docs = load_corpus(section, limit)
    print(f"  Загружено: {len(docs)} документов")

    if use_st:
        model   = load_st_model()
        vectors = build_st_vectors(docs, model)
        backend_used = "sentence-transformers"
        dim = len(next(iter(vectors.values()))) if vectors else 384
    else:
        idf, tfidf_vectors = build_tfidf_vectors(docs)
        vectors      = tfidf_vectors
        backend_used = "tfidf"
        dim = 0

    index_data = {
        "meta": {
            "backend": backend_used,
            "model":   MODEL_NAME if use_st else "tfidf",
            "docs":    len(vectors),
            "dim":     dim,
            "built":   __import__("datetime").datetime.now().isoformat(),
        },
        "vectors": vectors,
    }
    if not use_st:
        index_data["idf"] = idf

    INDEX.write_text(json.dumps(index_data, ensure_ascii=False, separators=(",", ":")),
                     encoding="utf-8")
    print(f"  ✅ Сохранено → {INDEX.relative_to(ROOT)}")
    print(f"  Документов: {len(vectors)} | Backend: {backend_used}")
    if not use_st:
        print(f"  Для neural embeddings: pip install sentence-transformers && python {__file__} --index --backend st")


# ── Поиск ────────────────────────────────────────────────────────────────────

def cmd_query(query: str, top: int = 10, backend: str = "auto"):
    if not INDEX.exists():
        print("❌ Индекс не построен. Запустите: --index")
        return

    data    = json.loads(INDEX.read_text(encoding="utf-8"))
    bk      = data["meta"]["backend"]
    vectors = data["vectors"]
    deps    = check_dependencies()

    print(f"🔍 Semantic поиск: «{query}» [{bk}]")

    if bk == "sentence-transformers" and deps["sentence_transformers"]:
        model = load_st_model()
        q_emb = model.encode([query[:512]], convert_to_numpy=True)[0].tolist()
        scored = [(cosine_st(q_emb, v), path) for path, v in vectors.items() if isinstance(v, list)]
    else:
        idf = data.get("idf", {})
        q_tokens = tokenize(query)
        if not q_tokens:
            print("  Запрос пустой после токенизации")
            return
        total   = len(q_tokens)
        q_tf    = Counter(q_tokens)
        q_vec   = {t: (c / total) * idf.get(t, 1) for t, c in q_tf.items()}
        norm    = sum(v * v for v in q_vec.values()) ** 0.5
        if norm:
            q_vec = {t: v / norm for t, v in q_vec.items()}
        scored = [(cosine_tfidf(q_vec, v), path)
                  for path, v in vectors.items() if isinstance(v, dict)]

    scored.sort(reverse=True)
    print(f"\nТоп-{top} результатов:\n")
    for i, (score, path) in enumerate(scored[:top], 1):
        name = "/".join(path.split("/")[-2:])
        print(f"  {i:2}. [{score:.4f}] {name}")


# ── Сравнение двух файлов ────────────────────────────────────────────────────

def cmd_compare(file_a: str, file_b: str):
    if not INDEX.exists():
        print("❌ Индекс не построен. Запустите: --index")
        return

    data    = json.loads(INDEX.read_text(encoding="utf-8"))
    bk      = data["meta"]["backend"]
    vectors = data["vectors"]

    # Нормализовать пути
    def norm_path(p: str) -> str:
        fp = Path(p)
        if not fp.is_absolute():
            fp = ROOT / p
        try:
            return str(fp.relative_to(ROOT))
        except ValueError:
            return p

    pa, pb = norm_path(file_a), norm_path(file_b)

    va = vectors.get(pa) or vectors.get(file_a)
    vb = vectors.get(pb) or vectors.get(file_b)

    if va is None:
        print(f"❌ Файл не в индексе: {pa}")
        return
    if vb is None:
        print(f"❌ Файл не в индексе: {pb}")
        return

    if bk == "sentence-transformers":
        sim = cosine_st(va, vb)
    else:
        sim = cosine_tfidf(va, vb)

    print(f"📐 Semantic similarity [{bk}]:")
    print(f"  A: {pa}")
    print(f"  B: {pb}")
    print(f"  Сходство: {sim:.4f}")
    if sim >= 0.85:
        print(f"  → ⚠ Очень похожи (возможный дубль)")
    elif sim >= 0.5:
        print(f"  → ✅ Тематически близки")
    elif sim >= 0.2:
        print(f"  → 📎 Слабая связь")
    else:
        print(f"  → 🔀 Разные темы")


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Semantic Embeddings для корпуса Lorenzo (ST или TF-IDF)"
    )
    parser.add_argument("--check",    action="store_true",  help="Проверить зависимости")
    parser.add_argument("--index",    action="store_true",  help="Построить семантический индекс")
    parser.add_argument("--query",    metavar="TEXT",        help="Семантический поиск")
    parser.add_argument("--compare",  nargs=2, metavar="FILE", help="Сравнить два файла")
    parser.add_argument("--backend",  default="auto",
                        choices=["auto", "st", "tfidf"],
                        help="Бэкенд: auto | st (sentence-transformers) | tfidf (fallback)")
    parser.add_argument("--section",  default="",           help="Ограничить раздел")
    parser.add_argument("--limit",    type=int, default=0,  help="Максимум документов")
    parser.add_argument("--top",      type=int, default=10, help="Число результатов")
    args = parser.parse_args()

    if args.check:
        cmd_check()
    elif args.index:
        cmd_index(backend=args.backend, section=args.section, limit=args.limit)
    elif args.query:
        cmd_query(args.query, top=args.top, backend=args.backend)
    elif args.compare:
        cmd_compare(*args.compare)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
