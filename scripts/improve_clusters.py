"""
improve_clusters.py — кластеризует файлы по тематической близости
через TF-IDF вектора и косинусное сходство (без внешних ML-библиотек).
Создаёт docs/CLUSTERS.md.
Запуск: python scripts/improve_clusters.py
"""
import re
import math
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

STOPWORDS_RU = {
    "и", "в", "не", "на", "что", "с", "по", "это", "как", "из",
    "для", "к", "а", "но", "то", "если", "или", "от", "о", "при",
    "за", "уже", "чем", "так", "же", "его", "её", "их", "все",
    "они", "он", "она", "мы", "вы", "я", "но", "бы", "быть",
    "только", "ещё", "также", "этого", "этой", "том", "может",
    "быть", "нет", "да", "такой", "самый", "один", "два", "три",
    "the", "a", "an", "of", "in", "to", "and", "is", "are", "for",
    "that", "this", "with", "be", "by", "as", "at", "or", "not",
}


def tokenize(text: str) -> list[str]:
    """Токенизирует текст, убирая стопслова и короткие слова."""
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{2,}', text.lower())
    return [w for w in words if w not in STOPWORDS_RU]


def build_tfidf(docs: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    """Строит TF-IDF матрицу. docs = {path: [tokens]}"""
    N = len(docs)
    # Подсчёт DF
    df: Counter = Counter()
    for tokens in docs.values():
        df.update(set(tokens))

    # TF-IDF для каждого документа
    tfidf = {}
    for path, tokens in docs.items():
        tf = Counter(tokens)
        total = len(tokens) or 1
        vec = {}
        for word, count in tf.most_common(100):
            tf_val = count / total
            idf_val = math.log((N + 1) / (df[word] + 1)) + 1
            vec[word] = tf_val * idf_val
        tfidf[path] = vec
    return tfidf


def cosine(v1: dict, v2: dict) -> float:
    """Косинусное сходство двух TF-IDF векторов."""
    common = set(v1) & set(v2)
    if not common:
        return 0.0
    dot = sum(v1[w] * v2[w] for w in common)
    norm1 = math.sqrt(sum(x * x for x in v1.values()))
    norm2 = math.sqrt(sum(x * x for x in v2.values()))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


def greedy_cluster(tfidf: dict, threshold: float = 0.15) -> list[list[str]]:
    """Жадная кластеризация: добавляем файл в кластер если сходство >= threshold."""
    paths = list(tfidf.keys())
    assigned = set()
    clusters = []

    for path in paths:
        if path in assigned:
            continue
        cluster = [path]
        assigned.add(path)
        for other in paths:
            if other in assigned:
                continue
            sim = cosine(tfidf[path], tfidf[other])
            if sim >= threshold:
                cluster.append(other)
                assigned.add(other)
        clusters.append(cluster)

    return sorted(clusters, key=lambda c: -len(c))


def top_words(paths: list[str], tfidf: dict, n: int = 6) -> list[str]:
    """Топ слов кластера по среднему TF-IDF."""
    combined: Counter = Counter()
    for p in paths:
        for w, score in tfidf[p].items():
            combined[w] += score
    return [w for w, _ in combined.most_common(n)]


def main():
    print("Кластеризация файлов...")

    # Загружаем документы (только содержательные)
    raw_docs: dict[str, list[str]] = {}
    for f in sorted(DOCS.rglob("*.md")):
        skip = {"README.md", "CLUSTERS.md", "TAGS.md", "GLOSSARY.md",
                "CROSSREFS.md", "PRIORITIES.md", "QA.md", "SEARCH.md"}
        if f.name in skip:
            continue
        text = f.read_text(encoding="utf-8")
        tokens = tokenize(text)
        if len(tokens) >= 30:
            raw_docs[str(f.relative_to(ROOT))] = tokens

    print(f"  документов для кластеризации: {len(raw_docs)}")
    tfidf = build_tfidf(raw_docs)
    clusters = greedy_cluster(tfidf, threshold=0.15)
    print(f"  кластеров найдено: {len(clusters)}")

    lines = [
        "# Кластеры тематически близких файлов\n",
        f"Метод: TF-IDF + косинусное сходство (порог 0.15)  \n"
        f"Документов: {len(raw_docs)}, кластеров: {len(clusters)}\n",
    ]

    for i, cluster in enumerate(clusters[:30], 1):
        words = top_words(cluster, tfidf)
        label = ", ".join(words[:4])
        lines.append(f"\n## Кластер {i} — {label} ({len(cluster)} файлов)\n")
        for path in cluster[:10]:
            short = path.split("/")[-1].replace(".md", "")
            lines.append(f"- `{path}` — _{short}_")
        if len(cluster) > 10:
            lines.append(f"- _...и ещё {len(cluster)-10} файлов_")

    if len(clusters) > 30:
        lines.append(f"\n_...и ещё {len(clusters)-30} малых кластеров (по 1-2 файла)_")

    out = DOCS / "CLUSTERS.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
