"""
improve_reclassify.py — раскладывает файлы по подпапкам на основе TF-IDF тематики.

Алгоритм:
  1. TF-IDF по всем файлам секции
  2. k-means кластеризация (без numpy: по ключевым словам)
  3. Именование кластеров по топ-словам
  4. Предложение подпапок + перемещение файлов (с --apply)

Режимы:
  --dry-run   (по умолчанию) — показать план без изменений
  --apply     — реально переместить файлы
  --section   — обрабатывать конкретную секцию (по умолчанию: docs/)
  --topics N  — количество тем (по умолчанию: 8)

Запуск:
    python scripts/improve_reclassify.py --section 02-anthropic-vacancies --dry-run
    python scripts/improve_reclassify.py --section 02-anthropic-vacancies --topics 10 --apply
"""
import math
import re
import shutil
import sys
from collections import Counter, defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

APPLY   = "--apply"   in sys.argv
DRY_RUN = not APPLY

N_TOPICS = 8
if "--topics" in sys.argv:
    idx = sys.argv.index("--topics")
    if idx + 1 < len(sys.argv):
        N_TOPICS = int(sys.argv[idx + 1])

SECTION_FILTER = None
if "--section" in sys.argv:
    idx = sys.argv.index("--section")
    if idx + 1 < len(sys.argv):
        SECTION_FILTER = DOCS / sys.argv[idx + 1]

SKIP_FILES = {
    "README.md", "SEARCH.md", "READABILITY.md", "SPELLCHECK.md",
    "CONTENT_GAPS.md", "LINK_PREVIEW.md", "BROKEN_LINKS.md",
    "COVERAGE.md", "STALENESS.md", "METRICS.md", "HEALTH.md",
    "SCORING.md", "ENTITIES.md", "CONTACTS.md", "TOPIC_MODEL.md",
}

STOPWORDS = {
    "и", "в", "не", "на", "с", "по", "к", "из", "за", "для", "это",
    "как", "но", "или", "что", "был", "были", "его", "её", "их",
    "всё", "при", "от", "до", "об", "же", "бы", "ли", "да", "нет",
    "the", "a", "an", "is", "are", "was", "were", "be", "have", "has",
    "had", "do", "does", "will", "can", "this", "that", "of", "in",
    "on", "at", "to", "for", "with", "by", "from", "as", "or", "and",
    "not", "but", "it", "its", "we", "you", "they", "their", "our",
}

MIN_WORD_LEN = 4
MIN_DOC_WORDS = 30  # пропускаем файлы-заглушки


# ─── TF-IDF ────────────────────────────────────────────────────────────────

def _clean(text: str) -> str:
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'<!--.*?-->', ' ', text, flags=re.DOTALL)
    text = re.sub(r'https?://\S+', ' ', text)
    text = re.sub(r'[#*|>\[\]_~\-]', ' ', text)
    return text.lower()


def _tokenize(text: str) -> list[str]:
    return [
        t for t in re.findall(r'[а-яёa-z]{%d,}' % MIN_WORD_LEN, _clean(text))
        if t not in STOPWORDS
    ]


def _tfidf(docs: dict[str, list[str]]) -> dict[str, dict[str, float]]:
    N = len(docs)
    df: Counter = Counter()
    for tokens in docs.values():
        for w in set(tokens):
            df[w] += 1

    result: dict[str, dict[str, float]] = {}
    for doc_id, tokens in docs.items():
        tf = Counter(tokens)
        total = len(tokens) or 1
        scores: dict[str, float] = {}
        for w, cnt in tf.items():
            if df[w] < 2:
                continue
            scores[w] = (cnt / total) * math.log(N / (1 + df[w]))
        result[doc_id] = scores
    return result


def _top_words(scores: dict[str, float], n: int = 10) -> list[str]:
    return [w for w, _ in sorted(scores.items(), key=lambda x: -x[1])[:n]]


# ─── Кластеризация ─────────────────────────────────────────────────────────

def _kmeans(tfidf: dict[str, dict[str, float]], k: int, iters: int = 5) -> dict[int, list[str]]:
    doc_ids = list(tfidf.keys())
    if len(doc_ids) <= k:
        return {i: [d] for i, d in enumerate(doc_ids)}

    # Инициализация равномерно
    step = max(1, len(doc_ids) // k)
    centroids: list[set[str]] = [
        set(_top_words(tfidf[doc_ids[min(i * step, len(doc_ids) - 1)]], 12))
        for i in range(k)
    ]

    assignment: dict[str, int] = {}
    for _ in range(iters):
        # E-step
        clusters: dict[int, list[str]] = defaultdict(list)
        for doc_id, scores in tfidf.items():
            doc_words = set(_top_words(scores, 12))
            best, best_sim = 0, -1
            for ki, centroid in enumerate(centroids):
                sim = len(doc_words & centroid) / max(1, len(doc_words | centroid))
                if sim > best_sim:
                    best_sim, best = sim, ki
            clusters[best].append(doc_id)
            assignment[doc_id] = best

        # M-step
        for ki, members in clusters.items():
            word_counts: Counter = Counter()
            for doc_id in members:
                for w in _top_words(tfidf[doc_id], 12):
                    word_counts[w] += 1
            centroids[ki] = set(w for w, _ in word_counts.most_common(12))

    return {k: v for k, v in clusters.items() if v}


def _name_cluster(members: list[str], tfidf: dict[str, dict[str, float]]) -> str:
    """Имя кластера — топ-3 слова по суммарному TF-IDF."""
    word_sum: Counter = Counter()
    for doc_id in members:
        for w, s in tfidf[doc_id].items():
            word_sum[w] += s
    top = [w for w, _ in word_sum.most_common(3)]
    return "_".join(top) if top else "misc"


def _safe_folder_name(name: str) -> str:
    name = re.sub(r'[^a-zа-яё0-9_]', '_', name.lower())
    name = re.sub(r'_+', '_', name).strip('_')
    return name[:40]


# ─── Основная логика ───────────────────────────────────────────────────────

def main() -> None:
    print("📂 improve_reclassify.py — тематическая рубрикация файлов")
    print(f"   Тем: {N_TOPICS}  |  Режим: {'APPLY (перемещение файлов!)' if APPLY else 'dry-run'}\n")

    target = SECTION_FILTER or DOCS
    all_files = [
        f for f in sorted(target.rglob("*.md"))
        if f.name not in SKIP_FILES and f.parent == target  # только файлы в корне секции
    ]
    print(f"   Файлов в корне секции: {len(all_files)}")

    # Загружаем и токенизируем
    docs: dict[str, list[str]] = {}
    path_map: dict[str, Path] = {}
    for f in all_files:
        try:
            text = f.read_text(encoding="utf-8")
        except Exception:
            continue
        tokens = _tokenize(text)
        if len(tokens) < MIN_DOC_WORDS:
            continue
        key = str(f.relative_to(ROOT))
        docs[key] = tokens
        path_map[key] = f

    print(f"   Достаточно текста: {len(docs)}/{len(all_files)} файлов\n")

    if len(docs) < 4:
        print("  ⚠️  Слишком мало файлов для кластеризации")
        return

    tfidf = _tfidf(docs)
    k = min(N_TOPICS, len(docs) // 2)
    clusters = _kmeans(tfidf, k)

    # Строим план
    plan: list[dict] = []
    for cluster_id, members in sorted(clusters.items(), key=lambda x: -len(x[1])):
        folder_name = _safe_folder_name(_name_cluster(members, tfidf))
        top_words_list = []
        word_sum: Counter = Counter()
        for doc_id in members:
            for w, s in tfidf[doc_id].items():
                word_sum[w] += s
        top_words_list = [w for w, _ in word_sum.most_common(8)]

        plan.append({
            "cluster_id": cluster_id,
            "folder": folder_name,
            "members": members,
            "top_words": top_words_list,
        })

    # Вывод плана
    total_moves = sum(len(p["members"]) for p in plan)
    print(f"  Кластеров: {len(plan)}  |  Файлов для перемещения: {total_moves}\n")

    for p in plan:
        dest = target / p["folder"]
        print(f"  📁 {p['folder']}/ ({len(p['members'])} файлов)")
        print(f"     Ключевые слова: {', '.join(p['top_words'][:5])}")
        for doc_id in p["members"][:5]:
            print(f"       → {Path(doc_id).name}")
        if len(p["members"]) > 5:
            print(f"       ... и ещё {len(p['members']) - 5}")
        print()

    if DRY_RUN:
        print("  Запустите с --apply для реального перемещения файлов.")
        print("  ВНИМАНИЕ: перемещение обновит все внутренние ссылки только вручную!")
        return

    # Применяем: создаём подпапки и перемещаем файлы
    moved = 0
    for p in plan:
        dest = target / p["folder"]
        dest.mkdir(exist_ok=True)
        # README для подпапки
        readme = dest / "README.md"
        if not readme.exists():
            readme.write_text(
                f"# {p['folder'].replace('_', ' ').title()}\n\n"
                f"_Создана автоматически: {TODAY}_\n\n"
                f"Ключевые темы: {', '.join(p['top_words'][:6])}\n\n"
                f"Файлов: {len(p['members'])}\n",
                encoding="utf-8",
            )
        for doc_id in p["members"]:
            src = path_map.get(doc_id)
            if not src or not src.exists():
                continue
            dst = dest / src.name
            if dst == src:
                continue
            shutil.move(str(src), str(dst))
            moved += 1

    print(f"\n  ✅ Перемещено: {moved} файлов")
    print("  ⚠️  Обновите внутренние ссылки: python scripts/improve_broken_links.py --fix")


if __name__ == "__main__":
    main()
