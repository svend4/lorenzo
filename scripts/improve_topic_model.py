"""
improve_topic_model.py — тематическое моделирование без ML-зависимостей.

Реализует упрощённый TF-IDF + кластеризацию по ключевым словам.
Без sklearn/gensim: только стандартная библиотека Python.

Алгоритм:
  1. TF-IDF для всех слов во всех файлах
  2. Топ-N ключевых слов по TF-IDF для каждого файла
  3. Кластеризация файлов по пересечению ключевых слов
  4. Именование кластеров по самым частым словам

Создаёт docs/TOPIC_MODEL.md.
Запуск:
    python scripts/improve_topic_model.py
    python scripts/improve_topic_model.py --topics 8
    python scripts/improve_topic_model.py --section 05-habr-projects
    python scripts/improve_topic_model.py --top-words 10
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

N_TOPICS = 6
if "--topics" in sys.argv:
    idx = sys.argv.index("--topics")
    if idx + 1 < len(sys.argv):
        N_TOPICS = int(sys.argv[idx + 1])

TOP_WORDS = 8
if "--top-words" in sys.argv:
    idx = sys.argv.index("--top-words")
    if idx + 1 < len(sys.argv):
        TOP_WORDS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {"TOPIC_MODEL.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
              "CONTENT_GAPS.md", "CITATION_INDEX.md", "READING_TIME.md"}

# Стоп-слова (RU + EN)
STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "были", "его", "её", "их",
    "всё", "при", "от", "до", "об", "же", "бы", "ли", "да", "нет",
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "can",
    "could", "should", "may", "might", "this", "that", "these", "those",
    "it", "its", "of", "in", "on", "at", "to", "for", "with", "by",
    "from", "as", "or", "and", "not", "but", "if", "then", "so",
}

MIN_WORD_LEN = 4
MIN_WORD_FREQ = 2


def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[#*|>\[\]_~\-]', ' ', text)
    return text.lower()


def _tokenize(text: str) -> list[str]:
    clean = _clean(text)
    tokens = re.findall(r'[а-яёa-z]{%d,}' % MIN_WORD_LEN, clean)
    return [t for t in tokens if t not in STOPWORDS]


def _compute_tfidf(docs: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    """Вычисляет TF-IDF. Возвращает {doc_id: {word: score}}."""
    N = len(docs)

    # DF: сколько документов содержат слово
    df: Counter = Counter()
    for tokens in docs.values():
        for word in set(tokens):
            df[word] += 1

    tfidf: dict[str, dict[str, float]] = {}
    for doc_id, tokens in docs.items():
        tf = Counter(tokens)
        total = len(tokens) or 1
        scores: dict[str, float] = {}
        for word, count in tf.items():
            if df[word] < MIN_WORD_FREQ:
                continue
            tf_score = count / total
            idf_score = math.log(N / (1 + df[word]))
            scores[word] = tf_score * idf_score
        tfidf[doc_id] = scores

    return tfidf


def _top_words(scores: dict[str, float], n: int) -> list[str]:
    return [w for w, _ in sorted(scores.items(), key=lambda x: -x[1])[:n]]


def _cluster_files(tfidf: dict[str, dict[str, float]], n_clusters: int) -> dict[int, list[str]]:
    """Простая кластеризация: k-means по ключевым словам (без numpy)."""
    # Выбираем начальные центроиды из файлов с максимальным разнообразием
    doc_ids = list(tfidf.keys())
    if not doc_ids:
        return {}

    # Инициализация: берём равномерно по списку
    step = max(1, len(doc_ids) // n_clusters)
    centroids: list[set[str]] = []
    for i in range(n_clusters):
        idx = min(i * step, len(doc_ids) - 1)
        centroids.append(set(_top_words(tfidf[doc_ids[idx]], TOP_WORDS)))

    # E-step: назначение кластеров (3 итерации достаточно)
    for _ in range(3):
        clusters: dict[int, list[str]] = defaultdict(list)
        for doc_id, scores in tfidf.items():
            doc_words = set(_top_words(scores, TOP_WORDS))
            best_cluster = 0
            best_overlap = -1
            for k, centroid in enumerate(centroids):
                overlap = len(doc_words & centroid)
                if overlap > best_overlap:
                    best_overlap = overlap
                    best_cluster = k
            clusters[best_cluster].append(doc_id)

        # M-step: обновляем центроиды
        for k, doc_list in clusters.items():
            word_counts: Counter = Counter()
            for doc_id in doc_list:
                for w in _top_words(tfidf[doc_id], TOP_WORDS):
                    word_counts[w] += 1
            centroids[k] = set(w for w, _ in word_counts.most_common(TOP_WORDS))

    # Удаляем пустые кластеры
    return {k: v for k, v in clusters.items() if v}


def _name_cluster(doc_ids: list[str], tfidf: dict[str, dict[str, float]]) -> str:
    word_counts: Counter = Counter()
    for doc_id in doc_ids:
        for w in _top_words(tfidf[doc_id], TOP_WORDS // 2):
            word_counts[w] += 1
    top = [w for w, _ in word_counts.most_common(3)]
    return ', '.join(top) if top else "разное"


def main() -> None:
    print("🧩 improve_topic_model.py — тематическое моделирование (TF-IDF)")
    print(f"   Тем: {N_TOPICS}, топ слов: {TOP_WORDS}\n")

    target = SECTION_FILTER or DOCS
    files = [f for f in sorted(target.rglob("*.md")) if f.name not in SKIP_FILES]
    print(f"   Файлов: {len(files)}")

    # Токенизация
    docs: dict[str, list[str]] = {}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        tokens = _tokenize(text)
        if len(tokens) >= 20:
            docs[str(f.relative_to(ROOT))] = tokens

    print(f"   Документов с достаточным текстом: {len(docs)}\n")

    if len(docs) < N_TOPICS:
        print("  ⚠️  Недостаточно документов для кластеризации")
        n_actual = max(1, len(docs))
    else:
        n_actual = N_TOPICS

    tfidf = _compute_tfidf(docs)
    clusters = _cluster_files(tfidf, n_actual)

    lines = [
        "# Тематическое моделирование (TF-IDF)\n",
        f"_Обновлено: {TODAY}_\n",
        f"Документов: **{len(docs)}** | Тем: **{len(clusters)}**\n",
        "> Кластеризация на основе TF-IDF без ML-зависимостей.\n",
    ]

    for k, doc_list in sorted(clusters.items(), key=lambda x: -len(x[1])):
        cluster_name = _name_cluster(doc_list, tfidf)
        lines += [
            f"\n## Тема {k+1}: {cluster_name} ({len(doc_list)} документов)\n",
        ]

        # Топ слова кластера
        word_counts: Counter = Counter()
        for doc_id in doc_list:
            for w, score in tfidf[doc_id].items():
                word_counts[w] += score
        top_cluster_words = [w for w, _ in word_counts.most_common(12)]
        lines.append(f"**Ключевые слова:** {', '.join(f'`{w}`' for w in top_cluster_words)}\n")

        lines.append("**Документы:**")
        for doc_id in sorted(doc_list)[:15]:
            top_w = _top_words(tfidf[doc_id], 4)
            lines.append(f"- `{doc_id}` — {', '.join(top_w)}")
        if len(doc_list) > 15:
            lines.append(f"- ... и ещё {len(doc_list)-15} документов")

    # Матрица сходства топ-5 документов из каждой темы (краткая)
    lines += ["\n## Топ уникальных слов по темам\n",
              "| Тема | Слово 1 | Слово 2 | Слово 3 | Слово 4 | Слово 5 |",
              "|------|---------|---------|---------|---------|---------|"]
    for k, doc_list in sorted(clusters.items(), key=lambda x: -len(x[1])):
        cluster_name = _name_cluster(doc_list, tfidf)
        word_counts = Counter()
        for doc_id in doc_list:
            for w, score in tfidf[doc_id].items():
                word_counts[w] += score
        top5 = [w for w, _ in word_counts.most_common(5)]
        while len(top5) < 5:
            top5.append("—")
        lines.append(f"| {cluster_name[:20]} | {' | '.join(top5)} |")

    out = DOCS / "TOPIC_MODEL.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  тем: {len(clusters)}, документов: {len(docs)}")


if __name__ == "__main__":
    main()
