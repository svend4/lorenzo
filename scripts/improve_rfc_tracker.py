"""
improve_rfc_tracker.py — RFC система для Svyazi 2.0.

Управляет RFC-файлами в docs/rfcs/: создание, статусы, реестр, валидация.

RFC (Request for Comments) — формальный документ для архитектурных решений.
Жизненный цикл: Draft → Proposed → Accepted | Rejected | Superseded.

Использование:
  python scripts/improve_rfc_tracker.py                        # список всех RFC
  python scripts/improve_rfc_tracker.py --new "Название" --author "ник"  # создать RFC
  python scripts/improve_rfc_tracker.py --status RFC-0001 Accepted        # изменить статус
  python scripts/improve_rfc_tracker.py --show RFC-0001                   # показать RFC
  python scripts/improve_rfc_tracker.py --update                          # обновить README
  python scripts/improve_rfc_tracker.py --validate                        # проверить структуру
"""
import re
import sys
import argparse
from pathlib import Path
from datetime import datetime

ROOT  = Path(__file__).parent.parent
DOCS  = ROOT / "docs"
RFCS  = DOCS / "rfcs"
TMPL  = RFCS / "template.md"
INDEX = RFCS / "README.md"

VALID_STATUSES = {"Draft", "Proposed", "Accepted", "Rejected", "Superseded"}

STATUS_EMOJI = {
    "Draft":      "📝",
    "Proposed":   "🔍",
    "Accepted":   "✅",
    "Rejected":   "❌",
    "Superseded": "⏭",
}

# ── Парсинг RFC-файла ─────────────────────────────────────────────────────────

def _parse_rfc(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm   = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    meta: dict = {}
    if fm:
        for line in fm.group(1).splitlines():
            m = re.match(r"^(\w+):\s*(.+)", line)
            if m:
                key, val = m.group(1), m.group(2).strip().strip('"\'')
                meta[key] = val
    # Извлечь summary (первый абзац после # заголовка)
    summary_m = re.search(r"## Summary\s*\n+(.+?)(?:\n\n|\Z)", text, re.DOTALL)
    meta["summary"] = summary_m.group(1).strip()[:200] if summary_m else ""
    meta["path"]    = path
    meta["text"]    = text
    meta["filename"] = path.name
    return meta


def _list_rfcs() -> list[dict]:
    if not RFCS.exists():
        return []
    rfcs = []
    for f in sorted(RFCS.glob("RFC-*.md")):
        try:
            rfcs.append(_parse_rfc(f))
        except Exception:
            pass
    return rfcs


# ── Создание RFC ──────────────────────────────────────────────────────────────

def _next_rfc_number() -> int:
    rfcs = _list_rfcs()
    if not rfcs:
        return 1
    nums = []
    for r in rfcs:
        m = re.match(r"RFC-(\d+)", r.get("filename", ""))
        if m:
            nums.append(int(m.group(1)))
    return max(nums, default=0) + 1


def cmd_new(title: str, author: str, tags: str = ""):
    RFCS.mkdir(parents=True, exist_ok=True)
    num    = _next_rfc_number()
    slug   = re.sub(r"[^a-zа-яё0-9]+", "-", title.lower()).strip("-")[:40]
    fname  = f"RFC-{num:04d}-{slug}.md"
    date   = datetime.now().strftime("%Y-%m-%d")
    tags_list = f"[architecture, rfc{', ' + tags if tags else ''}]"

    template = TMPL.read_text(encoding="utf-8") if TMPL.exists() else ""
    content  = (
        template
        .replace("NNNN", f"{num:04d}")
        .replace("RFC Title", title)
        .replace("Draft", "Draft")
        .replace("author-handle", author)
        .replace("YYYY-MM-DD", date)
        .replace("[architecture, rfc]", tags_list)
        .replace("RFC-NNNN: RFC Title", f"RFC-{num:04d}: {title}")
    )

    filepath = RFCS / fname
    filepath.write_text(content, encoding="utf-8")
    print(f"✅ Создан: {filepath.relative_to(ROOT)}")
    print(f"   Номер: RFC-{num:04d}")
    print(f"   Статус: Draft")
    print(f"\nОткройте файл, заполните Summary, Design и Implementation.")
    print(f"Затем: python scripts/improve_rfc_tracker.py --status RFC-{num:04d} Proposed")

    cmd_update()
    return filepath


# ── Изменение статуса ─────────────────────────────────────────────────────────

def cmd_status(rfc_id: str, new_status: str, reason: str = ""):
    if new_status not in VALID_STATUSES:
        print(f"❌ Недопустимый статус: {new_status}")
        print(f"   Допустимые: {', '.join(sorted(VALID_STATUSES))}")
        return

    rfcs = _list_rfcs()
    matched = [r for r in rfcs if rfc_id.upper() in r["filename"].upper()]
    if not matched:
        print(f"❌ RFC не найден: {rfc_id}")
        return
    if len(matched) > 1:
        print(f"❓ Несколько совпадений: {[r['filename'] for r in matched]}")
        return

    rfc  = matched[0]
    path = rfc["path"]
    text = rfc["text"]
    old  = rfc.get("status", "Draft")

    text = re.sub(r"^status:\s*\S+", f"status: {new_status}", text, flags=re.MULTILINE, count=1)
    if reason:
        text += f"\n<!-- status-change: {old} → {new_status} | {datetime.now().strftime('%Y-%m-%d')} | {reason} -->\n"

    path.write_text(text, encoding="utf-8")
    print(f"✅ {rfc['filename']}: {old} → {new_status}")
    if reason:
        print(f"   Причина: {reason}")
    cmd_update()


# ── Показать RFC ──────────────────────────────────────────────────────────────

def cmd_show(rfc_id: str):
    rfcs = _list_rfcs()
    matched = [r for r in rfcs if rfc_id.upper() in r["filename"].upper()]
    if not matched:
        print(f"❌ RFC не найден: {rfc_id}")
        return
    rfc = matched[0]
    print(rfc["text"])


# ── Список RFC ────────────────────────────────────────────────────────────────

def cmd_list():
    rfcs = _list_rfcs()
    if not rfcs:
        print("RFC пока нет. Создайте первый:")
        print('  python scripts/improve_rfc_tracker.py --new "Название" --author "ник"')
        return
    print(f"📋 RFC реестр ({len(rfcs)} документов)\n")
    for rfc in rfcs:
        num    = re.match(r"RFC-(\d+)", rfc["filename"])
        num_s  = num.group(0) if num else rfc["filename"]
        status = rfc.get("status", "Draft")
        emoji  = STATUS_EMOJI.get(status, "❓")
        title  = rfc.get("title", "?")
        author = rfc.get("author", "?")
        date   = rfc.get("date", "")
        print(f"  {emoji} {num_s}: {title}")
        print(f"     Статус: {status} | Автор: {author} | Дата: {date}")
        if rfc.get("summary"):
            print(f"     {rfc['summary'][:100]}")
        print()


# ── Обновить README ───────────────────────────────────────────────────────────

def cmd_update():
    rfcs = _list_rfcs()
    if not INDEX.exists():
        return

    lines = []
    if rfcs:
        lines.append(f"Всего RFC: **{len(rfcs)}**\n")
        for status in ["Accepted", "Proposed", "Draft", "Rejected", "Superseded"]:
            group = [r for r in rfcs if r.get("status", "Draft") == status]
            if not group:
                continue
            emoji = STATUS_EMOJI.get(status, "")
            lines.append(f"\n### {emoji} {status} ({len(group)})\n")
            for r in group:
                num = re.match(r"RFC-\d+", r["filename"])
                num_s = num.group(0) if num else r["filename"]
                title = r.get("title", r["filename"])
                lines.append(f"- [{num_s}: {title}]({r['filename']})")
    else:
        lines.append("_RFC пока не созданы. Запустите `improve_rfc_tracker.py --new \"...\"` для создания первого RFC._")

    body = "\n".join(lines)
    text = INDEX.read_text(encoding="utf-8")
    text = re.sub(
        r"<!-- rfc-index-start -->.*<!-- rfc-index-end -->",
        f"<!-- rfc-index-start -->\n{body}\n<!-- rfc-index-end -->",
        text, flags=re.DOTALL,
    )
    INDEX.write_text(text, encoding="utf-8")


# ── Валидация ─────────────────────────────────────────────────────────────────

def cmd_validate():
    rfcs = _list_rfcs()
    if not rfcs:
        print("Нет RFC для валидации.")
        return

    issues = 0
    for rfc in rfcs:
        errs = []
        if not rfc.get("rfc"):
            errs.append("Нет поля rfc: в frontmatter")
        if not rfc.get("title"):
            errs.append("Нет поля title:")
        if rfc.get("status") not in VALID_STATUSES:
            errs.append(f"Недопустимый статус: {rfc.get('status')}")
        if not rfc.get("author"):
            errs.append("Нет поля author:")
        if not rfc.get("summary"):
            errs.append("Нет секции ## Summary")
        if errs:
            print(f"⚠ {rfc['filename']}:")
            for e in errs:
                print(f"  - {e}")
            issues += len(errs)

    if issues:
        print(f"\nВсего проблем: {issues}")
    else:
        print(f"✅ Все {len(rfcs)} RFC валидны")


# ── Первый RFC (seed) ─────────────────────────────────────────────────────────

def _create_seed_rfc():
    """Создать первый RFC об интеграционных контрактах."""
    RFCS.mkdir(parents=True, exist_ok=True)
    date    = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
rfc: "0001"
title: "Card Envelope как единый контракт данных Svyazi 2.0"
status: Accepted
author: "svend4"
date: {date}
supersedes: ""
superseded_by: ""
tags: [architecture, rfc, card-envelope, core]
---

# RFC-0001: Card Envelope как единый контракт данных Svyazi 2.0

## Summary

Card Envelope — единый формат хранения любого знания в системе Svyazi 2.0.
Все компоненты (AgentFS, Yodoca, MCP, Gateway) обмениваются только через Card Envelope.

## Motivation

Без общего формата каждый компонент создаёт своё представление данных.
AgentFS хранит файлы, Yodoca хранит episodes, CardIndex хранит JSON —
три несовместимых формата для одного понятия «карточка знания».

## Design

```json
{{
  "card_id":      "sha256:...",
  "card_type":    "doc | note | fact | person | project | event | proposal",
  "state":        "raw | normalized | approved | rejected | decayed",
  "sources":      ["url", "file_path"],
  "edges":        [{{"to": "card_id", "rel": "references | contradicts | extends"}}],
  "created_at":   "ISO-8601",
  "updated_at":   "ISO-8601",
  "payload_hash": "sha256:...",
  "payload":      {{
    "title":   "...",
    "summary": "...(300 символов)...",
    "body":    "...(800 слов)...",
    "tags":    ["tag1", "tag2"]
  }}
}}
```

### Инварианты

1. `card_id` — иммутабельный, SHA256 от начального контента
2. `state` — монотонно растёт: raw → normalized → approved (нельзя откатиться без явного decay)
3. `edges` — направленные, типизированные рёбра к другим card_id
4. `payload` — расширяемый, но `title` + `summary` обязательны для normalized

## Alternatives Considered

| Альтернатива | Причина отклонения |
|-------------|-------------------|
| Yodoca-native format | BSL 1.1 лицензия, зависимость от внешнего API |
| JSON-LD / RDF | Избыточная сложность для нашего масштаба |
| Flat файлы без metadata | Нет жизненного цикла и графа |

## Implementation

- [x] `utils_card_envelope.py` — базовая реализация
- [x] `improve_card_index.py` — CardStore
- [x] `gateway.py` — write-back через Card Envelope
- [x] `mcp_server.py` — add_card, update_card_state
- [x] `improve_card_promote.py` — промоушен состояний

## References

- [PROTOTYPE_SPEC §3.1](../PROTOTYPE_SPEC.md)
- [11-integration-contracts](../01-svyazi/11-integration-contracts.md)
"""
    filepath = RFCS / "RFC-0001-card-envelope-contract.md"
    filepath.write_text(content, encoding="utf-8")
    return filepath


# ── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="RFC система для Svyazi 2.0")
    parser.add_argument("--new",      metavar="TITLE",  help="Создать новый RFC")
    parser.add_argument("--author",   default="svend4", help="Автор RFC (для --new)")
    parser.add_argument("--tags",     default="",       help="Теги через запятую (для --new)")
    parser.add_argument("--status",   nargs=2, metavar=("RFC-ID", "STATUS"),
                        help="Изменить статус RFC")
    parser.add_argument("--reason",   default="",       help="Причина смены статуса")
    parser.add_argument("--show",     metavar="RFC-ID", help="Показать RFC")
    parser.add_argument("--update",   action="store_true", help="Обновить README/index")
    parser.add_argument("--validate", action="store_true", help="Валидировать все RFC")
    parser.add_argument("--seed",     action="store_true", help="Создать seed RFC-0001")
    args = parser.parse_args()

    if args.new:
        cmd_new(args.new, args.author, args.tags)
    elif args.status:
        cmd_status(args.status[0], args.status[1], args.reason)
    elif args.show:
        cmd_show(args.show)
    elif args.update:
        cmd_update()
        print("✅ RFC README обновлён")
    elif args.validate:
        cmd_validate()
    elif args.seed:
        p = _create_seed_rfc()
        print(f"✅ Seed RFC создан: {p.relative_to(ROOT)}")
        cmd_update()
    else:
        cmd_list()


if __name__ == "__main__":
    main()
