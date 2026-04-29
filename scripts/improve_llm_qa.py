"""
improve_llm_qa.py — ответы на вопросы по всей базе знаний Lorenzo через Claude API.
Stage 3c: RAG без векторной БД — поиск по search_index.json + LLM-синтез.

Режимы:
  1. Интерактивный: задаёшь вопросы в терминале, получаешь ответы с источниками
  2. Batch: читает вопросы из файла, пишет ответы в docs/QA_ANSWERS.md
  3. Single: ответ на один вопрос через --question "..."

Флаги:
  --save      Сохранять каждый ответ в docs/QA_ANSWERS.md (работает во всех режимах)
  --no-cache  Отключить JSON-кэш (по умолчанию кэш включён, экономит токены)
  --clear-cache  Очистить кэш ответов

Стоимость: ~$0.003-0.01 на вопрос (haiku), зависит от числа найденных источников.
Кэш сохраняет ответы в docs/qa_cache.json — повторные вопросы бесплатны.

Запуск:
    python scripts/improve_llm_qa.py                             # интерактивный режим
    python scripts/improve_llm_qa.py --question "Что такое NGT?" # один вопрос
    python scripts/improve_llm_qa.py --question "..." --save     # + сохранить ответ
    python scripts/improve_llm_qa.py --batch docs/QUESTIONS.md   # batch из файла
    python scripts/improve_llm_qa.py --dry-run --question "..."  # план без API
    python scripts/improve_llm_qa.py --clear-cache               # сбросить кэш
"""
import re
import sys
import json
import time
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "scripts"))

from utils_chunker import chunk_by_paragraphs, estimate_tokens  # noqa: E402

DRY_RUN     = "--dry-run"     in sys.argv
SAVE        = "--save"        in sys.argv
NO_CACHE    = "--no-cache"    in sys.argv
CLEAR_CACHE = "--clear-cache" in sys.argv
TODAY       = date.today().isoformat()
MODEL       = "claude-haiku-4-5-20251001"
INDEX_PATH  = DOCS / "search_index.json"
CACHE_PATH  = DOCS / "qa_cache.json"
TOP_K       = 5     # сколько документов брать для контекста
MAX_CTX     = 6000  # символов контекста на вопрос


# ---------------------------------------------------------------------------
# Поиск релевантных документов (без векторов — keyword BM25-like)
# ---------------------------------------------------------------------------

def load_index() -> list[dict]:
    if not INDEX_PATH.exists():
        return []
    data = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    # Поддерживаем оба формата: список или dict с ключом "docs"/"documents"
    if isinstance(data, list):
        return data
    return data.get("docs", data.get("documents", []))


def tokenize_query(query: str) -> list[str]:
    words = re.findall(r'[а-яёa-z][а-яёa-z\-]{1,}', query.lower())
    stopwords = {"и", "в", "на", "что", "как", "это", "для", "или", "но",
                 "the", "a", "an", "of", "in", "to", "is", "are", "for"}
    return [w for w in words if w not in stopwords]


def _doc_text(doc: dict) -> str:
    """Возвращает лучшее доступное текстовое поле документа.

    search_index.json использует разные ключи в зависимости от версии
    improve_search_index.py: 'content' (новый) или 'preview' (старый).
    356/460 файлов имеют пустой 'content' но заполненный 'preview'.
    """
    return " ".join(filter(None, [
        doc.get("content", ""),
        doc.get("preview", ""),
        doc.get("summary", ""),
    ]))


def score_doc(doc: dict, query_tokens: list[str]) -> float:
    body  = _doc_text(doc).lower()
    title = doc.get("title", "").lower()
    path  = doc.get("path", "").lower()
    tags  = " ".join(doc.get("tags", [])).lower()

    score = 0.0
    for t in query_tokens:
        if t in title:
            score += 5.0 + title.count(t) * 0.5   # сильный буст за заголовок
        if t in path:
            score += 3.0                             # буст за путь (имя файла)
        if t in tags:
            score += 2.0                             # буст за теги
        if t in body:
            score += 1.0 + body.count(t) * 0.05    # базовый по тексту
    return score


def find_relevant(query: str, index: list[dict], top_k: int = TOP_K) -> list[dict]:
    tokens = tokenize_query(query)
    if not tokens:
        return []
    scored = [(score_doc(d, tokens), d) for d in index]
    scored = [(s, d) for s, d in scored if s > 0]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [d for _, d in scored[:top_k]]


def build_context(docs: list[dict], max_chars: int = MAX_CTX) -> str:
    """Собирает контекст из найденных документов."""
    parts = []
    budget = max_chars
    for doc in docs:
        title   = doc.get("title", doc.get("path", "?"))
        path    = doc.get("path", "")
        content = _doc_text(doc)[:800]
        entry   = f"[Источник: {title}]({path})\n{content}"
        if len(entry) > budget:
            entry = entry[:budget]
        parts.append(entry)
        budget -= len(entry)
        if budget <= 0:
            break
    return "\n\n---\n\n".join(parts)


# ---------------------------------------------------------------------------
# Кэш ответов (docs/qa_cache.json) — экономит токены на повторных вопросах
# ---------------------------------------------------------------------------

def _cache_key(question: str) -> str:
    import hashlib
    return hashlib.md5(question.strip().lower().encode()).hexdigest()[:12]


def load_cache() -> dict:
    if NO_CACHE or not CACHE_PATH.exists():
        return {}
    try:
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_cache(cache: dict) -> None:
    if NO_CACHE:
        return
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")


def get_cached(question: str, cache: dict) -> str | None:
    entry = cache.get(_cache_key(question))
    if entry:
        return entry.get("answer")
    return None


def put_cached(question: str, answer: str, cache: dict) -> None:
    cache[_cache_key(question)] = {"question": question, "answer": answer, "date": TODAY}


# ---------------------------------------------------------------------------
# Сохранение ответа в QA_ANSWERS.md
# ---------------------------------------------------------------------------

def append_to_qa_answers(question: str, answer: str, sources: list[dict]) -> None:
    header_needed = not QA_ANSWERS_PATH.exists()
    source_list = "\n".join(
        f"- [{d.get('title', d.get('path', '?'))}]({d.get('path', '')})"
        for d in sources
    )
    entry = f"### {question}\n\n{answer}\n\n**Источники:**\n{source_list}\n\n---\n"
    with open(QA_ANSWERS_PATH, "a", encoding="utf-8") as f:
        if header_needed:
            f.write(QA_ANSWERS_HEADER)
        f.write(entry)


# ---------------------------------------------------------------------------
# LLM-синтез ответа
# ---------------------------------------------------------------------------

QA_PROMPT = """\
Ты помогаешь работать с базой знаний проекта Svyazi 2.0 / Lorenzo.

Вопрос: {question}

Контекст из базы знаний:
{context}

---

Ответь на вопрос на основе контекста. Если контекст не содержит ответа — скажи об этом явно.

Формат ответа:
**Ответ:** [краткий ответ в 1-3 предложениях]

**Детали:** [если нужны — дополнительные факты из контекста]

**Источники:** [перечисли файлы, из которых взял информацию]"""


def ask_llm(question: str, context: str, client) -> str:
    resp = client.messages.create(
        model=MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content":
            QA_PROMPT.format(question=question, context=context)}],
    )
    return resp.content[0].text.strip()


# ---------------------------------------------------------------------------
# Batch режим: читает вопросы из QUESTIONS.md
# ---------------------------------------------------------------------------

def extract_questions_from_md(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    # Ищем строки вида: - Вопрос? или 1. Вопрос? или > Вопрос?
    questions = []
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r'^(?:[-*\d.>]+\s+)?(.+\?)\s*$', line)
        if m and len(m.group(1)) > 10:
            questions.append(m.group(1).strip())
    return questions[:20]  # лимит


QA_ANSWERS_PATH = DOCS / "QA_ANSWERS.md"

QA_ANSWERS_HEADER = f"""\
# Ответы на вопросы (LLM Q&A)

<!-- summary: Автоматические ответы по базе знаний Lorenzo -->
<!-- tags: qa, llm -->

_Обновлено: {TODAY}_
_Модель: claude-haiku-4-5_

---

"""

ANSWER_TEMPLATE = """\
### {question}

{answer}

---
"""


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def single_question(question: str, index: list[dict], client=None,
                    cache: dict | None = None) -> str:
    """Отвечает на один вопрос. Возвращает текст ответа."""
    docs = find_relevant(question, index)
    print(f"\n  Найдено источников: {len(docs)}")
    for d in docs:
        print(f"    - {d.get('title', d.get('path', '?'))}")

    if DRY_RUN:
        context = build_context(docs)
        tokens = estimate_tokens(QA_PROMPT.format(question=question, context=context))
        print(f"  Токенов запроса: ~{tokens:,}  (~${tokens/1e6*0.25:.4f})")
        return ""

    # Проверяем кэш
    if cache is not None:
        cached = get_cached(question, cache)
        if cached:
            print("  (из кэша, API не вызывался)")
            print(f"\n{cached}\n")
            if SAVE:
                append_to_qa_answers(question, cached, docs)
                print("  📝 Сохранено в QA_ANSWERS.md")
            return cached

    context = build_context(docs)
    answer = ask_llm(question, context, client)
    print(f"\n{answer}\n")

    if cache is not None:
        put_cached(question, answer, cache)
        save_cache(cache)

    if SAVE:
        append_to_qa_answers(question, answer, docs)
        print("  📝 Сохранено в QA_ANSWERS.md")

    return answer


QA_PROMPT_WITH_HISTORY = """\
Ты помогаешь работать с базой знаний проекта Svyazi 2.0 / Lorenzo.

История диалога:
{history}

Новый вопрос: {question}

Контекст из базы знаний:
{context}

---

Ответь на вопрос. Можешь опираться на историю диалога если это уместно.
Если контекст не содержит ответа — скажи об этом явно.

Формат:
**Ответ:** [1-3 предложения]

**Детали:** [если нужны дополнительные факты]

**Источники:** [файлы из которых взята информация]"""


def ask_llm_with_history(question: str, context: str, history: list[dict], client) -> str:
    if not history:
        return ask_llm(question, context, client)

    history_text = "\n".join(
        f"Q: {h['q']}\nA: {h['a'][:300]}..." if len(h['a']) > 300 else f"Q: {h['q']}\nA: {h['a']}"
        for h in history[-4:]  # последние 4 обмена
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=700,
        messages=[{"role": "user", "content":
            QA_PROMPT_WITH_HISTORY.format(
                history=history_text, question=question, context=context
            )}],
    )
    return resp.content[0].text.strip()


def interactive_mode(index: list[dict], client, cache: dict) -> None:
    save_hint = " (ответы сохраняются в QA_ANSWERS.md)" if SAVE else " (--save для сохранения)"
    print(f"\nИнтерактивный режим{save_hint}.")
    print("Модель помнит последние 4 вопроса сессии. Введите вопрос (или 'exit'):\n")
    history: list[dict] = []  # [{q, a}, ...]
    while True:
        try:
            q = input("❓ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            break
        if not q or q.lower() in ("exit", "quit", "выход"):
            break

        docs = find_relevant(q, index)
        print(f"\n  Найдено источников: {len(docs)}")
        for d in docs:
            print(f"    - {d.get('title', d.get('path', '?'))}")

        cached = get_cached(q, cache)
        if cached and not history:
            answer = cached
            print("  (из кэша)")
        else:
            context = build_context(docs)
            answer = ask_llm_with_history(q, context, history, client)
            if not history:  # кэшируем только если нет контекста диалога
                put_cached(q, answer, cache)
                save_cache(cache)

        print(f"\n{answer}\n")
        history.append({"q": q, "a": answer})

        if SAVE:
            append_to_qa_answers(q, answer, docs)
            print("  📝 Сохранено в QA_ANSWERS.md")

        time.sleep(0.3)


def batch_mode(batch_path: Path, index: list[dict], client, cache: dict) -> None:
    questions = extract_questions_from_md(batch_path)
    print(f"Вопросов из {batch_path.name}: {len(questions)}\n")

    saved = 0
    for q in questions:
        print(f"  🔄 {q[:60]}...")
        docs = find_relevant(q, index)
        if not docs:
            print("     нет источников — пропускаем")
            continue
        # batch режим всегда сохраняет (--save подразумевается)
        cached = get_cached(q, cache)
        if cached:
            answer = cached
            print("  (из кэша)")
        else:
            context = build_context(docs)
            answer = ask_llm(q, context, client)
            put_cached(q, answer, cache)
            save_cache(cache)
            time.sleep(0.5)

        append_to_qa_answers(q, answer, docs)
        saved += 1
        print(f"  ✅ записано в QA_ANSWERS.md")

    print(f"\n✅ Ответы ({saved}): {QA_ANSWERS_PATH.relative_to(ROOT)}")


def main():
    print("❓ improve_llm_qa.py — Q&A по базе знаний Lorenzo")
    print(f"   Модель: {MODEL}")
    if DRY_RUN:    print("   Режим: dry-run")
    if SAVE:       print("   Режим: --save (ответы → QA_ANSWERS.md)")
    if NO_CACHE:   print("   Режим: --no-cache")
    print()

    # Управление кэшем
    if CLEAR_CACHE:
        if CACHE_PATH.exists():
            CACHE_PATH.unlink()
            print(f"✅ Кэш очищен: {CACHE_PATH.relative_to(ROOT)}")
        else:
            print("ℹ️  Кэш уже пуст")
        return

    cache = load_cache()
    if cache and not NO_CACHE:
        print(f"   Кэш: {len(cache)} ответов в {CACHE_PATH.name}")

    index = load_index()
    if not index:
        print("⚠️  search_index.json не найден. Запустите improve_search_index.py")
        if not DRY_RUN:
            sys.exit(1)

    print(f"   Документов в индексе: {len(index)}\n")

    # Разбор аргументов
    question_arg = None
    if "--question" in sys.argv:
        idx = sys.argv.index("--question")
        if idx + 1 < len(sys.argv):
            question_arg = sys.argv[idx + 1]

    batch_arg = None
    if "--batch" in sys.argv:
        idx = sys.argv.index("--batch")
        if idx + 1 < len(sys.argv):
            batch_arg = ROOT / sys.argv[idx + 1]

    if DRY_RUN:
        q = question_arg or "Что такое NGT Memory?"
        single_question(q, index, client=None, cache=None)
        return

    try:
        import anthropic
    except ImportError:
        print("❌ pip install anthropic")
        sys.exit(1)

    client = anthropic.Anthropic()

    if question_arg:
        single_question(question_arg, index, client, cache)
    elif batch_arg:
        batch_mode(Path(batch_arg), index, client, cache)
    else:
        interactive_mode(index, client, cache)


if __name__ == "__main__":
    main()
