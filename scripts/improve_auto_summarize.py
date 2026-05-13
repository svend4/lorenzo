"""
improve_auto_summarize.py — авто-генерация summary и тегов для raw-карточек.

Находит raw-карточки с коротким/отсутствующим summary (< 80 символов)
и инжектирует summary из тела документа, а также теги из keyword-правил.

Это разблокирует переход raw→normalized в improve_card_promote.py.

Использование:
  python scripts/improve_auto_summarize.py --dry-run     # план без изменений
  python scripts/improve_auto_summarize.py --apply       # применить
  python scripts/improve_auto_summarize.py --apply --section 02-anthropic-vacancies
  python scripts/improve_auto_summarize.py --stats       # статистика
"""
import re
import sys
from pathlib import Path
from datetime import datetime

ROOT    = Path(__file__).parent.parent
DOCS    = ROOT / "docs"
SCRIPTS = ROOT / "scripts"

MIN_SUMMARY_LEN  = 80   # порог для promote
TARGET_SUMMARY   = 250  # целевая длина summary

# Те же правила что в improve_tags.py
TOPIC_RULES: dict[str, list[str]] = {
    "memory":        ["yodoca", "ngt memory", "memnet", "agent-memory", "консолидац",
                      "forgetting", "episod", "hebbian", "recall", "память", "memory"],
    "rag":           ["rag", "liteparse", "retrieval", "hybrid rag", "graph rag",
                      "legal rag", "bounding box", "page-level", "evidence", "поиск"],
    "orchestration": ["rufler", "mclaude", "ai factory", "sequential", "handoff",
                      "оркестр", "swarm", "locks", "mailbox", "агент", "agent"],
    "security":      ["sentinel", "litellm", "tool search", "безопасн", "pii",
                      "allowlist", "firewall", "quarantine", "безопасность"],
    "knowledge":     ["knowledge-space", "agentfs", "cardindex", "карточк", "знани",
                      "agentos", "vault", "reference card", "база знаний"],
    "ingestion":     ["svyazi", "import", "нормализац", "extraction", "llm extraction",
                      "dedup", "дедупликац", "парсинг", "parsing"],
    "local-first":   ["local-first", "crdt", "yjs", "automerge", "offline",
                      "whisper", "голос", "voice"],
    "architecture":  ["архитектур", "контракт", "envelope", "интеграц",
                      "зазор", "слой", "layer", "schema", "протокол"],
    "roadmap":       ["дорожная карта", "итерац", "mvp", "фаза", "phase",
                      "roadmap", "прототип", "timeline", "план"],
    "anthropic":     ["anthropic", "вакансии", "hiring", "cluster", "gtm",
                      "research engineer", "trust & safety", "вакансия"],
    "self-improve":  ["autoresearch", "self-improv", "benchmark", "eval",
                      "rollback", "нightly", "петл", "самоулучш", "скрипт"],
    "collaboration": ["коллаборац", "автор", "контакт", "habr", "хабр",
                      "svend4", "andrey", "виталий", "kksudo", "проект"],
}


def _detect_tags(text: str) -> list[str]:
    low = text.lower()
    tags = []
    for topic, keywords in TOPIC_RULES.items():
        if any(kw in low for kw in keywords):
            tags.append(topic)
    return tags[:5]  # не более 5 тегов


def _strip_fm(text: str) -> str:
    return re.sub(r"^---.*?---\s*", "", text, count=1, flags=re.DOTALL)


def _extract_best_summary(text: str) -> str:
    """Извлечь лучший summary из тела документа."""
    body = _strip_fm(text)
    # Убрать HTML-комментарии, code-блоки
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.DOTALL)
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]+`", " ", body)
    # Убрать markdown-разметку
    body = re.sub(r"^#{1,6}\s+(.+)$", r"\1", body, flags=re.MULTILINE)
    body = re.sub(r"\*{1,2}([^*]+)\*{1,2}", r"\1", body)
    body = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
    body = re.sub(r"^\s*[-*+|]\s*", " ", body, flags=re.MULTILINE)
    body = re.sub(r"\n{2,}", "\n", body).strip()

    # Разбить на предложения/абзацы, выбрать лучший
    candidates: list[str] = []
    # Сначала — полные предложения
    for sent in re.split(r"(?<=[.!?])\s+", body):
        sent = sent.strip()
        if 60 <= len(sent) <= 400 and not sent.startswith("#"):
            candidates.append(sent)

    if not candidates:
        # Fallback: параграфы
        for para in re.split(r"\n", body):
            para = para.strip()
            if len(para) >= 60:
                candidates.append(para[:400])

    if not candidates:
        return body[:TARGET_SUMMARY].strip()

    # Ранжировать по длине (ближе к TARGET, но ≥ MIN)
    def score(s: str) -> float:
        length_score = min(len(s), TARGET_SUMMARY) / TARGET_SUMMARY
        # Штраф за очень короткие
        if len(s) < MIN_SUMMARY_LEN:
            length_score *= 0.3
        return length_score

    best = max(candidates, key=score)
    return best[:TARGET_SUMMARY].strip()


def _get_state(text: str) -> str:
    m = re.search(r"^state:\s*(\S+)", text, re.MULTILINE)
    return m.group(1) if m else "raw"


def _get_fm_tags(text: str) -> list[str]:
    m = re.search(r"^tags:\s*\[([^\]]*)\]", text, re.MULTILINE)
    if m:
        return [t.strip().strip("\"'") for t in m.group(1).split(",") if t.strip()]
    return []


def _get_comment_tags(text: str) -> list[str]:
    m = re.search(r"<!--\s*tags:\s*([^-]+)\s*-->", text, re.IGNORECASE)
    if m:
        return [t.strip() for t in m.group(1).split(",") if t.strip()]
    return []


def _get_summary(text: str) -> str:
    m = re.search(r"<!--\s*summary\s*-->\s*>\s*(.+)", text)
    if m:
        return m.group(1).strip()
    # Fallback: первый параграф
    body = _strip_fm(text)
    for para in re.split(r"\n{2,}", body):
        para = para.strip().lstrip("#> ").strip()
        if len(para) > 50:
            return para[:300]
    return ""


def _inject_summary(text: str, summary: str) -> str:
    """Обновить или добавить <!-- summary --> > ... в тексте."""
    summary_line = f"<!-- summary -->\n> {summary}"
    # Если уже есть — заменить
    if re.search(r"<!--\s*summary\s*-->", text):
        text = re.sub(
            r"<!--\s*summary\s*-->\s*>\s*.+",
            f"<!-- summary -->\n> {summary}",
            text,
        )
        return text
    # Вставить после первого H1 или после frontmatter
    lines = text.split("\n")
    insert_at = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = i + 1
            break
    # После первого пустого места от заголовка
    if insert_at > 0:
        while insert_at < len(lines) and not lines[insert_at].strip():
            insert_at += 1
    lines.insert(insert_at, "")
    lines.insert(insert_at + 1, summary_line)
    lines.insert(insert_at + 2, "")
    return "\n".join(lines)


def _inject_fm_tags(text: str, tags: list[str]) -> str:
    """Добавить или обновить frontmatter tags:."""
    tags_str = ", ".join(tags)
    # Если есть frontmatter — добавить/обновить tags
    fm_m = re.match(r"^(---\n)(.*?)(---)", text, re.DOTALL)
    if fm_m:
        fm_body = fm_m.group(2)
        if re.search(r"^tags:", fm_body, re.MULTILINE):
            # Обновить пустые теги
            fm_body = re.sub(
                r"^tags:\s*\[\s*\]",
                f"tags: [{tags_str}]",
                fm_body,
                flags=re.MULTILINE,
            )
        else:
            fm_body += f"tags: [{tags_str}]\n"
        return fm_m.group(1) + fm_body + fm_m.group(3) + text[fm_m.end():]
    # Нет frontmatter — добавить минимальный
    date = datetime.now().strftime("%Y-%m-%d")
    fm = f"---\ndate: {date}\ntags: [{tags_str}]\nstate: raw\n---\n\n"
    return fm + text


def process_file(path: Path, dry_run: bool = True) -> dict:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return {"status": "error"}

    state = _get_state(text)
    if state in ("approved", "normalized", "decayed", "rejected"):
        return {"status": "skip_state"}

    fm_tags  = _get_fm_tags(text)
    cmt_tags = _get_comment_tags(text)
    has_tags = bool(fm_tags or cmt_tags)
    summary  = _get_summary(text)
    needs_summary = len(summary) < MIN_SUMMARY_LEN
    needs_tags    = not has_tags

    if not needs_summary and not needs_tags:
        return {"status": "ok"}

    changes: list[str] = []
    new_text = text

    if needs_summary:
        best = _extract_best_summary(text)
        if len(best) >= MIN_SUMMARY_LEN:
            if not dry_run:
                new_text = _inject_summary(new_text, best)
            changes.append(f"summary={len(best)}ch")

    if needs_tags:
        detected = _detect_tags(text)
        if detected:
            if not dry_run:
                new_text = _inject_fm_tags(new_text, detected)
            changes.append(f"tags={detected[:3]}")

    if not changes:
        return {"status": "insufficient_content"}

    if not dry_run and new_text != text:
        path.write_text(new_text, encoding="utf-8")

    return {
        "status": "changed",
        "path": str(path.relative_to(ROOT)),
        "changes": changes,
    }


def main():
    args = sys.argv[1:]
    dry_run  = "--apply" not in args
    stats_only = "--stats" in args
    section  = ""
    for i, a in enumerate(args):
        if a == "--section" and i + 1 < len(args):
            section = args[i + 1]

    if dry_run and not stats_only:
        print("📋 Auto-Summarize [dry-run] — передайте --apply для применения\n")
    elif not stats_only:
        print("✏️  Auto-Summarize [apply]\n")

    base = DOCS / section if section else DOCS
    paths = [p for p in base.rglob("*.md")
             if "obsidian" not in p.parts
             and not (p.parent == DOCS and p.stem.isupper())]

    results = {"changed": 0, "ok": 0, "skip_state": 0,
               "insufficient_content": 0, "error": 0}
    changed_list: list[dict] = []

    for path in paths:
        r = process_file(path, dry_run=dry_run)
        st = r.get("status", "error")
        results[st] = results.get(st, 0) + 1
        if st == "changed":
            changed_list.append(r)

    print(f"  Файлов проверено: {len(paths)}")
    print(f"  Изменено:         {results['changed']}")
    print(f"  Уже OK:           {results['ok']}")
    print(f"  Пропущено:        {results['skip_state']}")
    print(f"  Мало контента:    {results['insufficient_content']}")

    if changed_list and not stats_only:
        print(f"\n  Примеры изменений:")
        for r in changed_list[:8]:
            print(f"    {r['path']}")
            print(f"      → {', '.join(r['changes'])}")

    if not dry_run:
        print(f"\n✅ Применено: {results['changed']} карточек")
        print(f"   Запустите: python scripts/improve_card_promote.py --apply")
    else:
        print(f"\nℹ️  Запустите с --apply для применения изменений.")


if __name__ == "__main__":
    main()
