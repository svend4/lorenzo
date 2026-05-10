"""
improve_embedding_index.py — TF-IDF семантический индекс над CardStore.

Строит TF-IDF векторы для всех карточек; поддерживает косинусное сходство
без внешних ML-зависимостей (pure Python + stdlib math).

Индекс сохраняется в cards/tfidf_index.json:
  { "idf": {token: float}, "vectors": {card_id: {token: float}}, "meta": {...} }

Команды:
  --index             построить/перестроить индекс из CardStore
  --query TEXT        найти похожие карточки
  --query TEXT --type project  искать только среди проектов
  --top N             число результатов (по умолч. 10)
  --similar CARD_ID   найти карточки, похожие на данную
  --stats             статистика индекса

Запуск:
    python scripts/improve_embedding_index.py --index
    python scripts/improve_embedding_index.py --query "консолидация памяти агент"
    python scripts/improve_embedding_index.py --query "knowledge graph" --type project --top 5
    python scripts/improve_embedding_index.py --similar sha256:71f9eb7be6254cc6
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

ROOT   = Path(__file__).parent.parent
CARDS  = ROOT / "cards"
INDEX  = CARDS / "tfidf_index.json"
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))
from utils_card_envelope import CardStore, CardEnvelope


# ─────────────────────────────────────────────────────────────────────
# Токенизация
# ─────────────────────────────────────────────────────────────────────

_STOPWORDS_RU = {
    "и", "в", "на", "что", "как", "это", "для", "или", "но", "по", "к", "из",
    "а", "не", "с", "о", "от", "за", "до", "то", "же", "при", "уже", "так",
    "ещё", "бы", "ли", "его", "её", "их", "наш", "ваш", "мой", "свой",
    "всё", "все", "был", "была", "были", "есть", "быть", "если", "чем",
    "где", "когда", "который", "которая", "которые", "через", "этот", "эта",
    "также", "между", "после", "можно", "может", "очень", "более", "такой",
}
_STOPWORDS_EN = {
    "the", "a", "an", "of", "in", "to", "is", "for", "with", "by", "and",
    "or", "but", "on", "at", "from", "are", "was", "were", "be", "been",
    "have", "has", "that", "this", "it", "its", "not", "as", "all",
    "can", "will", "may", "our", "your", "their",
}
STOPWORDS = _STOPWORDS_RU | _STOPWORDS_EN


def tokenize(text: str) -> list[str]:
    """Токенизация: строчные слова ≥3 символов, без стоп-слов."""
    raw = re.findall(r'[а-яёa-z]{3,}', text.lower())
    return [t for t in raw if t not in STOPWORDS]


def card_text(card: CardEnvelope) -> str:
    """Объединяет все текстовые поля карточки в одну строку для индексации."""
    p = card.payload
    parts = [
        p.get("title", ""),
        p.get("summary", ""),
        " ".join(p.get("tags", [])),
        " ".join(p.get("projects", [])),
        card.card_type,
    ]
    # Добавляем имена рёбер
    for e in card.edges[:5]:
        parts.append(e.to.replace("/", " ").replace("-", " ").replace("_", " "))
    return " ".join(parts)


# ─────────────────────────────────────────────────────────────────────
# TF-IDF вычисление
# ─────────────────────────────────────────────────────────────────────

def compute_tf(tokens: list[str]) -> dict[str, float]:
    """TF = count(t) / len(doc)."""
    if not tokens:
        return {}
    counts = Counter(tokens)
    total  = len(tokens)
    return {t: c / total for t, c in counts.items()}


def compute_idf(docs_tokens: list[list[str]], vocab: set[str]) -> dict[str, float]:
    """IDF = log((N+1) / (df+1)) + 1  (сглаженный)."""
    n = len(docs_tokens)
    df: dict[str, int] = Counter()
    for doc in docs_tokens:
        for t in set(doc):
            df[t] += 1
    return {t: math.log((n + 1) / (df.get(t, 0) + 1)) + 1.0 for t in vocab}


def tfidf_vector(tf: dict[str, float], idf: dict[str, float]) -> dict[str, float]:
    """TF-IDF вектор: только ненулевые компоненты."""
    return {t: tf[t] * idf[t] for t in tf if t in idf}


def cosine_sim(v1: dict[str, float], v2: dict[str, float]) -> float:
    """Косинусное сходство двух разреженных векторов."""
    if not v1 or not v2:
        return 0.0
    dot = sum(v1.get(t, 0.0) * v2.get(t, 0.0) for t in v2)
    n1  = math.sqrt(sum(x * x for x in v1.values()))
    n2  = math.sqrt(sum(x * x for x in v2.values()))
    if n1 == 0 or n2 == 0:
        return 0.0
    return dot / (n1 * n2)


# ─────────────────────────────────────────────────────────────────────
# Загрузка / сохранение индекса
# ─────────────────────────────────────────────────────────────────────

def load_index() -> dict | None:
    if not INDEX.exists():
        return None
    try:
        return json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception:
        return None


def save_index(idf: dict, vectors: dict, card_meta: dict) -> None:
    CARDS.mkdir(exist_ok=True)
    data = {
        "meta": {
            "cards":   len(vectors),
            "vocab":   len(idf),
            "version": "1.0",
        },
        "idf":     idf,
        "vectors": vectors,
        "card_meta": card_meta,  # card_id → {title, card_type, state, path}
    }
    INDEX.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")),
                     encoding="utf-8")


# ─────────────────────────────────────────────────────────────────────
# Команды
# ─────────────────────────────────────────────────────────────────────

def cmd_index() -> None:
    if not CARDS.exists() or not any(CARDS.glob("*.json")):
        print("  CardStore пуст. Запустите: python scripts/improve_card_index.py --build")
        return

    store = CardStore(CARDS)
    cards = store.all()
    print(f"  Индексируем {len(cards)} карточек...")

    # Токенизируем все карточки
    all_tokens: list[list[str]] = []
    card_ids: list[str] = []
    for card in cards:
        text   = card_text(card)
        tokens = tokenize(text)
        all_tokens.append(tokens)
        card_ids.append(card.card_id)

    # Словарь
    vocab = set(t for tokens in all_tokens for t in tokens)
    print(f"  Словарь: {len(vocab)} токенов")

    # IDF
    idf = compute_idf(all_tokens, vocab)

    # TF-IDF векторы
    vectors: dict[str, dict[str, float]] = {}
    card_meta: dict[str, dict] = {}
    for card, tokens, cid in zip(cards, all_tokens, card_ids):
        tf  = compute_tf(tokens)
        vec = tfidf_vector(tf, idf)
        # Храним только топ-50 компонент (экономия места)
        top50 = dict(sorted(vec.items(), key=lambda x: -x[1])[:50])
        vectors[cid] = top50
        card_meta[cid] = {
            "title":     card.payload.get("title", "")[:60],
            "card_type": card.card_type,
            "state":     card.state,
            "path":      card.payload.get("path", ""),
        }

    save_index(idf, vectors, card_meta)
    print(f"  Сохранено → {INDEX.relative_to(ROOT)}")
    print(f"  Карточек: {len(vectors)}, словарь: {len(idf)}")


def cmd_query(query: str, top: int = 10, card_type: str = "") -> list[tuple[float, str, dict]]:
    """Поиск по TF-IDF. Возвращает [(score, card_id, meta), ...]."""
    idx = load_index()
    if not idx:
        print("  Индекс не построен. Запустите: --index")
        return []

    idf      = idx["idf"]
    vectors  = idx["vectors"]
    card_meta = idx["card_meta"]

    # Вектор запроса
    q_tokens = tokenize(query)
    if not q_tokens:
        print("  Запрос пустой после токенизации")
        return []
    q_tf  = compute_tf(q_tokens)
    q_vec = tfidf_vector(q_tf, idf)

    results = []
    for cid, vec in vectors.items():
        meta = card_meta.get(cid, {})
        if card_type and meta.get("card_type") != card_type:
            continue
        score = cosine_sim(q_vec, vec)
        if score > 0.0:
            results.append((score, cid, meta))

    results.sort(key=lambda x: -x[0])
    return results[:top]


def cmd_search(query: str, top: int = 10, card_type: str = "") -> None:
    results = cmd_query(query, top=top, card_type=card_type)
    if not results:
        print(f"  Ничего не найдено: «{query}»")
        return

    type_label = f" (тип: {card_type})" if card_type else ""
    print(f"\n  Семантический поиск «{query}»{type_label} — {len(results)} результатов:\n")
    for score, cid, meta in results:
        title = meta.get("title", cid[:16])[:55]
        ctype = meta.get("card_type", "?")
        path  = meta.get("path", "")
        print(f"  [{score:.3f}] {ctype:8}  {title}")
        if path:
            print(f"            {path}")
    print()


def cmd_similar(card_id: str, top: int = 5) -> None:
    idx = load_index()
    if not idx:
        print("  Индекс не построен. Запустите: --index")
        return

    vectors   = idx["vectors"]
    card_meta = idx["card_meta"]

    # Точный или частичный поиск по card_id
    target_cid = None
    if card_id in vectors:
        target_cid = card_id
    else:
        for cid in vectors:
            if card_id.lower() in cid.lower():
                target_cid = cid
                break
        if not target_cid:
            # Поиск по title/path в meta
            for cid, meta in card_meta.items():
                if card_id.lower() in (meta.get("title", "") + meta.get("path", "")).lower():
                    target_cid = cid
                    break

    if not target_cid:
        print(f"  Карточка не найдена: {card_id}")
        return

    target_vec  = vectors[target_cid]
    target_meta = card_meta.get(target_cid, {})
    print(f"\n  Похожие на: {target_meta.get('title', target_cid[:16])[:55]}\n")

    results = []
    for cid, vec in vectors.items():
        if cid == target_cid:
            continue
        score = cosine_sim(target_vec, vec)
        if score > 0.0:
            results.append((score, cid, card_meta.get(cid, {})))

    results.sort(key=lambda x: -x[0])
    for score, cid, meta in results[:top]:
        title = meta.get("title", cid[:16])[:55]
        ctype = meta.get("card_type", "?")
        path  = meta.get("path", "")
        print(f"  [{score:.3f}] {ctype:8}  {title}")
        if path:
            print(f"            {path}")
    print()


def cmd_stats() -> None:
    idx = load_index()
    if not idx:
        print("  Индекс не построен. Запустите: --index")
        return
    m = idx.get("meta", {})
    vectors   = idx["vectors"]
    card_meta = idx["card_meta"]

    # Статистика по типам
    from collections import Counter
    type_counts = Counter(v.get("card_type", "?") for v in card_meta.values())

    print(f"\n  TF-IDF Индекс:")
    print(f"  Карточек:  {m.get('cards', len(vectors))}")
    print(f"  Словарь:   {m.get('vocab', len(idx['idf']))} токенов")
    print(f"  Версия:    {m.get('version', '?')}")
    print(f"\n  По типу:")
    for t, c in type_counts.most_common():
        print(f"    {t:10}  {c}")

    # Топ-10 токенов по IDF (самые редкие = самые информативные)
    idf = idx["idf"]
    top_idf = sorted(idf.items(), key=lambda x: -x[1])[:10]
    print(f"\n  Топ-10 информативных токенов (высокий IDF):")
    for tok, val in top_idf:
        print(f"    {tok:20}  idf={val:.3f}")
    print()


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="TF-IDF семантический индекс над CardStore (без ML-зависимостей)"
    )
    parser.add_argument("--index",   action="store_true",
                        help="Построить/перестроить TF-IDF индекс")
    parser.add_argument("--query",   metavar="ТЕКСТ",
                        help="Семантический поиск по карточкам")
    parser.add_argument("--similar", metavar="CARD_ID",
                        help="Найти карточки, похожие на данную")
    parser.add_argument("--stats",   action="store_true",
                        help="Статистика индекса")
    parser.add_argument("--type",    metavar="ТИП", default="",
                        choices=["", "doc", "project", "person", "note", "fact"],
                        help="Фильтр по типу карточки (для --query)")
    parser.add_argument("--top",     type=int, default=10,
                        help="Число результатов")
    args = parser.parse_args()

    if args.index:
        cmd_index()
    elif args.query:
        cmd_search(args.query, top=args.top, card_type=args.type)
    elif args.similar:
        cmd_similar(args.similar, top=args.top)
    elif args.stats:
        cmd_stats()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
