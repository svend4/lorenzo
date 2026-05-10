"""
improve_collab_finder.py — Collaboration Finder для Svyazi 2.0.

Реализует PROTOTYPE_SPEC.md Итерация 3: агент анализирует документ или
запрос и возвращает топ-5 OSS-проектов-кандидатов для коллаборации,
с контактами авторов и шаблонами первого сообщения.

Алгоритм (гибридный):
  1. Семантический ранг — TF-IDF косинус по cards/tfidf_index.json
  2. BM25-ранг  — токенный поиск по CardStore
  3. Граф-бонус  — дополнительный вес за рёбра между карточками
  4. Объединение: score = 0.6*semantic + 0.4*bm25 + 0.1*graph

Контакт: ищем docs/contacts/<author>.md по имени проекта.
Шаблон:  генерируем первое сообщение на основе данных карточки.

Команды:
  --query "текст"        найти коллаборации по свободному запросу
  --file docs/some.md    найти коллаборации по документу
  --top N                число кандидатов (по умолч. 5)
  --type project|all     фильтровать только проекты (по умолч. project)
  --dry-run              показать кандидатов без записи файла
  --out PATH             куда писать отчёт (по умолч. docs/COLLAB_SUGGESTIONS.md)

Запуск:
    python scripts/improve_collab_finder.py --query "агент с памятью и консолидацией"
    python scripts/improve_collab_finder.py --file docs/PROTOTYPE_SPEC.md --top 7
    python scripts/improve_collab_finder.py --query "graff RAG knowledge" --dry-run
"""
import argparse
import json
import math
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
CARDS   = ROOT / "cards"
INDEX   = CARDS / "tfidf_index.json"
OUT_MD  = DOCS / "COLLAB_SUGGESTIONS.md"
SCRIPTS = ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS))
from utils_card_envelope import CardStore, CardEnvelope

# Импорт TF-IDF утилит из embedding_index
try:
    import importlib.util as _ilu
    _spec = _ilu.spec_from_file_location("emb", SCRIPTS / "improve_embedding_index.py")
    _emb  = _ilu.module_from_spec(_spec)
    _spec.loader.exec_module(_emb)          # type: ignore
    _tokenize    = _emb.tokenize
    _compute_tf  = _emb.compute_tf
    _tfidf_vec   = _emb.tfidf_vector
    _cosine_sim  = _emb.cosine_sim
    _HAVE_EMB    = True
except Exception:
    _HAVE_EMB = False

# ─────────────────────────────────────────────────────────────────────
# Загрузка данных
# ─────────────────────────────────────────────────────────────────────

def _load_index() -> dict | None:
    if not INDEX.exists():
        return None
    try:
        return json.loads(INDEX.read_text(encoding="utf-8"))
    except Exception:
        return None


def _load_contacts() -> dict[str, Path]:
    """Сопоставляет ключевые слова (имя проекта/автора) → Path контактного файла."""
    mapping: dict[str, Path] = {}
    contacts_dir = DOCS / "contacts"
    if not contacts_dir.exists():
        return mapping
    for f in contacts_dir.glob("*.md"):
        if f.name == "README.md":
            continue
        stem = f.stem.lower()
        mapping[stem] = f
        # Читаем frontmatter для projects
        try:
            text = f.read_text(encoding="utf-8")
            m = re.search(r'^projects:\s*\[([^\]]+)\]', text, re.MULTILINE)
            if m:
                for proj in re.findall(r'"([^"]+)"', m.group(1)):
                    mapping[proj.lower()] = f
            # author_handle
            m2 = re.search(r'^author:\s*"([^"]+)"', text, re.MULTILINE)
            if m2:
                mapping[m2.group(1).lower()] = f
        except Exception:
            pass
    return mapping


_GENERIC_PROJECTS = {
    "svyazi", "cardindex", "mclaude", "ai factory", "hybrid rag",
    "graph rag", "legal rag", "knowledge os",
}


def _find_contact(card: CardEnvelope, contacts: dict[str, Path]) -> Path | None:
    """Ищет контактный файл по названию основного проекта карточки.

    Только path-stem и первый сегмент заголовка — никаких payload.projects
    (они включают все упомянутые проекты и дают ложные совпадения).
    """
    title = card.payload.get("title", "").lower()
    path  = card.payload.get("path", "")

    # Убираем Markdown-сноски [^...]
    title_clean = re.sub(r'\[\^[^\]]*\]', '', title)

    # Первый сегмент до основных разделителей
    first_seg = re.split(r'[:—–+]', title_clean)[0].strip()

    candidates: list[str] = []

    # Path stem (hyphen-stripped): "agent-memory-mcp" → "agentmemory mcp"... → "agentmemorymcp"
    stem_raw = Path(path).stem.lower()
    # Вариант с дефисом и без
    candidates.append(stem_raw)
    candidates.append(re.sub(r'[^а-яёa-z0-9]', '', stem_raw))

    # Первый сегмент заголовка
    candidates.append(first_seg)
    candidates.append(re.sub(r'[^а-яёa-z0-9]', '', first_seg))

    # Убираем пустые и дубли
    seen: set[str] = set()
    keys: list[str] = []
    for k in candidates:
        k = k.strip()
        if k and k not in seen:
            seen.add(k)
            keys.append(k)

    # Точные совпадения
    for key in keys:
        if key in contacts:
            return contacts[key]

    # Частичное совпадение — только для ключей ≥ 7 символов (reduce false positives)
    for key in keys:
        if len(key) < 7:
            continue
        for ckey, cpath in contacts.items():
            if len(ckey) < 4:
                continue
            if key in ckey or ckey in key:
                return cpath

    return None


def _read_contact_brief(path: Path) -> dict:
    """Извлекает ключевые поля из контактного md-файла."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return {}

    author = re.search(r'^author:\s*"([^"]+)"', text, re.MULTILINE)
    handle = re.search(r'^author_handle:\s*"([^"]+)"', text, re.MULTILINE)
    platform = re.search(r'^platform:\s*(\S+)', text, re.MULTILINE)
    status   = re.search(r'^status:\s*(\S+)', text, re.MULTILINE)
    projects = re.findall(r'"([^"]+)"', re.search(r'^projects:\s*\[([^\]]+)\]',
                          text, re.MULTILINE).group(1)
                          if re.search(r'^projects:', text, re.MULTILINE) else "")
    return {
        "author":   author.group(1) if author else path.stem,
        "handle":   handle.group(1) if handle else "",
        "platform": platform.group(1) if platform else "GitHub",
        "status":   status.group(1) if status else "unknown",
        "projects": projects,
        "path":     str(path.relative_to(ROOT)),
    }


# ─────────────────────────────────────────────────────────────────────
# Ранжирование: гибридный BM25 + TF-IDF
# ─────────────────────────────────────────────────────────────────────

_STOPWORDS = {
    "и","в","на","что","как","это","для","или","но","по","к","из","а","не","с",
    "the","a","an","of","in","to","is","for","with","by","and","or","but","on",
}


def _bm25_score(query_tokens: list[str], card: CardEnvelope,
                k1: float = 1.5, b: float = 0.75, avg_len: float = 50.0) -> float:
    text = json.dumps(card.payload, ensure_ascii=False).lower()
    tokens = re.findall(r'[а-яёa-z]{3,}', text)
    tf_map = Counter(tokens)
    dl = len(tokens)
    score = 0.0
    for qt in query_tokens:
        tf = tf_map.get(qt, 0)
        if tf == 0:
            continue
        idf = math.log(2.0)  # упрощённый IDF без корпуса
        tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avg_len))
        score += idf * tf_norm
    return score


def _semantic_score(query_vec: dict, card_id: str, idx: dict) -> float:
    if not _HAVE_EMB or not idx:
        return 0.0
    vec = idx["vectors"].get(card_id, {})
    return _cosine_sim(query_vec, vec)


def _graph_bonus(card: CardEnvelope, candidate_ids: set[str]) -> float:
    """Бонус за рёбра к другим кандидатам (граф-коннективность)."""
    bonus = 0.0
    for edge in card.edges:
        for cid in candidate_ids:
            if edge.to in cid or cid in edge.to:
                bonus += 0.05
    return min(bonus, 0.3)


def _title_key(card: CardEnvelope) -> str:
    """Нормализованный ключ заголовка для дедупликации.

    Нормализует так, чтобы «Yodoca[^yodoca]: консолидация», «Yodoca»,
    «NGT[^ngt] Memory: граф» → «ngtmemory» и
    «MemNet / memory-is-all-you-need» → «memnet» совпадали с
    «MemNet: исследовательская память» → «memnet».
    """
    t = card.payload.get("title", "").lower()
    # 1. Удаляем Markdown-сноски [^...]
    t = re.sub(r'\[\^[^\]]*\]', '', t)
    # 2. Берём первый сегмент до жёстких разделителей (включая "/")
    first = re.split(r'[:—–()/]', t)[0].strip()
    # 3. Убираем не-алфавитные символы и пробелы
    key = re.sub(r'[^а-яёa-z0-9\s]', ' ', first).strip()
    key = re.sub(r'\s+', '', key)[:40]
    return key or re.sub(r'[^а-яёa-z0-9]', '', t)[:40]


def find_candidates(query_text: str, top: int = 5,
                    card_type: str = "project") -> list[dict]:
    """Гибридный поиск: возвращает список dict с данными кандидатов.

    Дедупликация: из нескольких карточек с одинаковым заголовком оставляем
    только одну (приоритет — не obsidian/, не из дублирующих папок).
    """
    if not CARDS.exists():
        return []

    store = CardStore(CARDS)
    all_cards = store.all()

    # Фильтр по типу
    if card_type and card_type != "all":
        pool = [c for c in all_cards if c.card_type == card_type]
    else:
        pool = all_cards

    if not pool:
        return []

    # Дедупликация по нормализованному заголовку
    # Предпочитаем основной docs/ над obsidian/ и другими зеркалами
    _MIRROR_PREFIXES = ("docs/obsidian/", "obsidian/")

    def _is_mirror(card: CardEnvelope) -> bool:
        p = card.payload.get("path", "")
        return any(p.startswith(pfx) for pfx in _MIRROR_PREFIXES)

    # Предпочтительные источники: богатый контент из 05-habr-projects/
    # над заглушками svyazi-2-0/components/ (те же 0 рёбер, но мало текста)
    _STUB_PREFIXES = ("docs/svyazi-2-0/", "svyazi-2-0/")

    def _card_weight(c: CardEnvelope) -> tuple[int, int, int]:
        """Вес для дедупликации: (не-зеркало, рёбра, слов в тексте)."""
        not_mirror = 0 if _is_mirror(c) else 1
        edges = len(c.edges)
        # Штрафуем заглушки: у них мало слов и они из svyazi-2-0/
        wc = c.payload.get("wc", 0)
        path = c.payload.get("path", "")
        if any(path.startswith(p) for p in _STUB_PREFIXES):
            wc = wc // 4  # понижаем приоритет относительно богатых файлов
        return (not_mirror, edges, wc)

    deduped: dict[str, CardEnvelope] = {}
    for card in pool:
        key = _title_key(card)
        if not key:
            key = card.card_id
        existing = deduped.get(key)
        if existing is None:
            deduped[key] = card
        elif _card_weight(card) > _card_weight(existing):
            deduped[key] = card

    pool = list(deduped.values())

    # Токены запроса
    q_tokens = [t for t in re.findall(r'[а-яёa-z]{3,}', query_text.lower())
                if t not in _STOPWORDS]
    if not q_tokens:
        return []

    # TF-IDF вектор запроса
    idx = _load_index() if _HAVE_EMB else None
    q_vec: dict = {}
    if idx and _HAVE_EMB:
        q_tf  = _compute_tf(q_tokens)
        q_vec = _tfidf_vec(q_tf, idx["idf"])

    # Avg doc length для BM25
    avg_len = max(
        sum(len(re.findall(r'\S+', json.dumps(c.payload))) for c in pool) / len(pool),
        1.0,
    )

    # Оценка каждого кандидата
    scored = []
    for card in pool:
        s_sem = _semantic_score(q_vec, card.card_id, idx) if idx else 0.0
        s_bm  = _bm25_score(q_tokens, card, avg_len=avg_len)
        scored.append((s_sem, s_bm, card))

    # Нормализация BM25 к [0, 1]
    max_bm = max((s for _, s, _ in scored), default=1.0) or 1.0
    scored = [(s_sem, s_bm / max_bm, c) for s_sem, s_bm, c in scored]

    # Собираем топ-2N для граф-бонуса
    pre_top = sorted(scored, key=lambda x: -(0.6 * x[0] + 0.4 * x[1]))[:top * 2]
    top_ids = {c.card_id for _, _, c in pre_top}

    final_scored = []
    for s_sem, s_bm, card in pre_top:
        g = _graph_bonus(card, top_ids)
        score = 0.6 * s_sem + 0.4 * s_bm + g
        final_scored.append((score, card))

    final_scored.sort(key=lambda x: -x[0])
    # Порог минимальной релевантности — исключаем нулевые попадания
    min_score = 0.01
    return [
        {"score": score, "card": card}
        for score, card in final_scored[:top]
        if score >= min_score
    ]


# ─────────────────────────────────────────────────────────────────────
# Генерация шаблона сообщения
# ─────────────────────────────────────────────────────────────────────

def _generate_message(card: CardEnvelope, contact: dict, query: str) -> str:
    """Генерирует шаблон первого сообщения автору проекта."""
    title   = card.payload.get("title", "ваш проект")[:50]
    author  = contact.get("author", "Автор")
    handle  = contact.get("handle", "")
    proj_list = ", ".join(contact.get("projects", [title.split(":")[0].strip()])[:3])
    platform  = contact.get("platform", "GitHub")

    # Извлекаем ключевые особенности проекта из summary
    summary = card.payload.get("summary", "")[:150]

    # Тема коллаборации из запроса
    q_short = query[:60].rstrip()

    lines = [
        f"**Кому:** {author} ({handle or platform})",
        f"**Тема:** Коллаборация по теме «{q_short}»",
        "",
        f"Привет, {author}!",
        "",
        f"Изучил{'а' if 'a' in author.lower() else ''} ваш проект **{proj_list}**"
        f" и вижу сильную синергию с задачами, над которыми работаю.",
    ]

    if summary:
        lines += [
            "",
            f"Особенно ценна идея: _{summary}_",
        ]

    lines += [
        "",
        "Работаю над Knowledge OS для локальных коллаборационных сетей"
        " (Svyazi 2.0 — CardIndex + Retrieval + Memory).",
        "Хотел бы обсудить возможность интеграции или обмена опытом.",
        "",
        "**Конкретные вопросы:**",
        f"- Как {proj_list} решает [_конкретный аспект из запроса_]?",
        "- Есть ли API / адаптер для внешних систем?",
        "- Открыты к совместным PR или техническому обмену?",
        "",
        "Репо: github.com/svend4/lorenzo | Документация: docs/PROTOTYPE_SPEC.md",
        "",
        "С уважением,",
        "Lorenzo / svend4",
    ]

    return "\n".join(lines)


# ─────────────────────────────────────────────────────────────────────
# Вывод и запись
# ─────────────────────────────────────────────────────────────────────

def _format_report(query: str, source_file: str,
                   candidates: list[dict], contacts: dict[str, Path]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "# Рекомендации по коллаборации (Collaboration Finder)",
        "",
        f"<!-- summary -->",
        f"> Автоматический поиск партнёрских проектов для: «{query[:80]}»",
        f"> **Дата:** {now}  **Кандидатов:** {len(candidates)}",
        "",
        "---",
        "",
        f"<!-- tags: collaboration, projects, recommendations, svyazi -->",
        "",
    ]

    if source_file:
        lines += [f"**Источник:** `{source_file}`", ""]

    lines += [
        f"**Запрос:** {query}",
        "",
        "---",
        "",
    ]

    for i, item in enumerate(candidates, 1):
        card  = item["card"]
        score = item["score"]
        title = card.payload.get("title", card.card_id[:20])
        path  = card.payload.get("path", "")
        tags  = ", ".join(card.payload.get("tags", [])[:5])
        projs = ", ".join(card.payload.get("projects", [])[:4])
        summary = card.payload.get("summary", "")[:200]
        edges_count = len(card.edges)

        lines += [
            f"## {i}. {title}",
            "",
            f"**Релевантность:** `{score:.3f}`  "
            f"**Тип:** `{card.card_type}`  "
            f"**Состояние:** `{card.state}`  "
            f"**Связей:** {edges_count}",
            "",
        ]

        if path:
            lines.append(f"**Документ:** [`{path}`]({path})")
            lines.append("")

        if tags:
            lines.append(f"**Теги:** {tags}")
        if projs:
            lines.append(f"**Упомянутые проекты:** {projs}")
        if tags or projs:
            lines.append("")

        if summary:
            lines += [f"> {summary}", ""]

        # Рёбра
        if card.edges:
            lines.append(f"**Связан с:**")
            for e in card.edges[:4]:
                lines.append(f"  - [{e.to}]({e.to}) _{e.rel}_")
            lines.append("")

        # Контакт автора
        contact_path = _find_contact(card, contacts)
        if contact_path:
            contact_info = _read_contact_brief(contact_path)
            author   = contact_info.get("author", "?")
            handle   = contact_info.get("handle", "")
            platform = contact_info.get("platform", "GitHub")
            status   = contact_info.get("status", "unknown")
            contact_doc = contact_info.get("path", "")

            status_icon = {"not_started": "⬜", "studied": "📖",
                           "messaged": "📨", "responded": "✅"}.get(status, "❓")
            lines += [
                f"**Автор:** {author} {handle}  |  {platform}  |  {status_icon} `{status}`",
            ]
            if contact_doc:
                lines.append(f"**Контакт:** [`{contact_doc}`]({contact_doc})")
            lines.append("")

            # Шаблон сообщения
            msg = _generate_message(card, contact_info, query)
            lines += [
                "<details>",
                f"<summary>📧 Шаблон первого сообщения → {author}</summary>",
                "",
                "```",
                msg,
                "```",
                "",
                "</details>",
                "",
            ]
        else:
            lines += ["**Автор:** контакт не найден в docs/contacts/", ""]

        lines += ["---", ""]

    # Следующие шаги
    lines += [
        "## Следующие шаги",
        "",
        "1. Изучить топ-3 кандидата и выбрать приоритет",
        "2. Обновить статус контакта:",
        "   ```",
        "   python scripts/improve_contact_status.py --author <имя> --studied",
        "   ```",
        "3. Отправить сообщение по шаблону выше",
        "4. Обновить после ответа:",
        "   ```",
        "   python scripts/improve_contact_status.py --author <имя> --messaged",
        "   ```",
        "5. Повторить поиск с уточнённым запросом:",
        f"   ```",
        f"   python scripts/improve_collab_finder.py --query \"{query[:50]}\"",
        f"   ```",
        "",
        f"_Сгенерировано: {now}  |  Алгоритм: TF-IDF + BM25 + граф_",
    ]

    return "\n".join(lines) + "\n"


def cmd_find(query: str, source_file: str = "", top: int = 5,
             card_type: str = "project", dry_run: bool = False,
             out: Path = OUT_MD) -> None:

    print(f"\n  Collaboration Finder")
    print(f"  Запрос: «{query[:60]}»")
    print(f"  Режим:  {'dry-run' if dry_run else 'полный'}  |  Топ: {top}  |  Тип: {card_type}\n")

    if not CARDS.exists() or not any(CARDS.glob("*.json")):
        print("  ❌ CardStore пуст. Запустите: python scripts/improve_card_index.py --build")
        return

    if not INDEX.exists():
        print("  ⚠ TF-IDF индекс не найден — используется только BM25.")
        print("    Рекомендуется: python scripts/improve_embedding_index.py --index")

    candidates = find_candidates(query, top=top, card_type=card_type)

    if not candidates:
        print(f"  Ничего не найдено по запросу «{query}»")
        print("  Попробуйте: --type all  или  другой запрос")
        return

    contacts = _load_contacts()

    print(f"  Найдено {len(candidates)} кандидатов:\n")
    for i, item in enumerate(candidates, 1):
        card  = item["card"]
        score = item["score"]
        title = card.payload.get("title", card.card_id[:20])[:55]
        cp    = _find_contact(card, contacts)
        author = _read_contact_brief(cp).get("author", "—") if cp else "—"
        print(f"  {i}. [{score:.3f}]  {card.card_type:8}  {title}")
        print(f"       Автор: {author}  |  Связей: {len(card.edges)}")
    print()

    if dry_run:
        print("  [dry-run] Файл не записан. Уберите --dry-run для создания отчёта.")
        return

    report = _format_report(query, source_file, candidates, contacts)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"  Записано → {out.relative_to(ROOT)}")
    print(f"  ({len(report.splitlines())} строк, {len(report)} символов)")


# ─────────────────────────────────────────────────────────────────────
# Извлечение запроса из файла
# ─────────────────────────────────────────────────────────────────────

def _extract_file_query(text: str, max_tokens: int = 120) -> str:
    """Извлекает тематические токены из Markdown-файла для поиска.

    Приоритет: H1-заголовок → теги → сводка/summary → первые параграфы.
    Пропускает HTML-комментарии, блоки frontmatter, alert-блоки.
    """
    parts: list[str] = []

    # Frontmatter YAML (между ---)
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', text, re.DOTALL)
    fm_text = ""
    if fm_match:
        fm_text = fm_match.group(1)
        # Извлекаем title/tags/summary из frontmatter
        for field in ("title", "summary", "tags", "description"):
            m = re.search(rf'^{field}:\s*(.+)$', fm_text, re.MULTILINE | re.IGNORECASE)
            if m:
                val = m.group(1).strip().strip('"').strip("'")
                parts.append(val)

    # H1 заголовок
    h1 = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    if h1:
        parts.insert(0, h1.group(1).strip())

    # Теги из <!-- tags: ... -->
    tags_match = re.search(r'<!--\s*tags:\s*([^>]+)-->', text)
    if tags_match:
        parts.append(tags_match.group(1).strip())

    # Строки summary-блоков (> ...)
    summary_lines = re.findall(r'^>\s+(.+)$', text, re.MULTILINE)
    for sl in summary_lines[:3]:
        # Пропускаем meta-строки (Версия:, Дата:, [!TIP] и т.п.)
        if re.search(r'Версия:|Дата:|Статус:|\[!', sl):
            continue
        parts.append(sl.strip())

    # Обычные параграфы (не заголовки, не цитаты, не комментарии, не код)
    body_lines = []
    in_code = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if not stripped:
            continue
        if stripped.startswith(("#", ">", "<!--", "|", "-", "*", "+")):
            continue
        if re.match(r'^\d+\.', stripped):
            continue
        body_lines.append(stripped)
        if len(body_lines) >= 20:
            break

    if body_lines:
        parts.append(" ".join(body_lines))

    combined = " ".join(parts)
    # Оставляем только значимые слова (токенизация)
    tokens = re.findall(r'[а-яёa-z]{4,}', combined.lower())
    # Убираем очевидный мусор (однобуквенные и технические термины)
    tokens = [t for t in tokens if t not in _STOPWORDS]
    # Ограничиваем длину и убираем дубли (сохраняя порядок)
    seen: set[str] = set()
    result: list[str] = []
    for t in tokens:
        if t not in seen:
            seen.add(t)
            result.append(t)
        if len(result) >= max_tokens:
            break

    return " ".join(result) if result else combined[:500]


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Collaboration Finder — ищет партнёрские OSS-проекты (Svyazi 2.0 Iter.3)"
    )
    parser.add_argument("--query",   metavar="ТЕКСТ",
                        help="Свободный текст запроса")
    parser.add_argument("--file",    metavar="ПУТЬ",
                        help="Путь к .md файлу — запрос из его содержимого")
    parser.add_argument("--top",     type=int, default=5,
                        help="Число кандидатов (по умолч. 5)")
    parser.add_argument("--type",    metavar="ТИП", default="project",
                        choices=["project", "all", "doc", "person"],
                        help="Тип карточек для поиска (по умолч. project)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Вывести кандидатов без записи файла")
    parser.add_argument("--out",     metavar="ПУТЬ",
                        help=f"Путь для отчёта (по умолч. {OUT_MD.relative_to(ROOT)})")
    args = parser.parse_args()

    # Определяем запрос
    query = ""
    source_file = ""
    if args.query:
        query = args.query
    elif args.file:
        fp = Path(args.file)
        if not fp.is_absolute():
            fp = ROOT / args.file
        if not fp.exists():
            print(f"  ❌ Файл не найден: {args.file}")
            sys.exit(1)
        text = fp.read_text(encoding="utf-8")
        source_file = str(fp.relative_to(ROOT)) if fp.is_relative_to(ROOT) else args.file
        # Извлекаем заголовок и тематическое содержимое (без мета-разметки)
        query = _extract_file_query(text)
        print(f"  Файл: {source_file} ({len(text.split())} слов → запрос: {len(query.split())} токенов)")
    else:
        parser.print_help()
        sys.exit(0)

    out = Path(args.out) if args.out else OUT_MD

    cmd_find(
        query=query,
        source_file=source_file,
        top=args.top,
        card_type=args.type,
        dry_run=args.dry_run,
        out=out,
    )


if __name__ == "__main__":
    main()
