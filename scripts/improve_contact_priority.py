"""
improve_contact_priority.py — ранжирует авторов по приоритету для контакта.

Формула: score = упоминания × 3 + (4 - статус_шаг) × 5 + слой_буст
  слой_буст: memory=3, knowledge=2, orchestration=2, graph=1, остальные=1

Создаёт docs/CONTACT_PRIORITY.md с топом авторов и рекомендуемым порядком.
Запуск: python scripts/improve_contact_priority.py
"""
import re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TODAY = date.today().isoformat()

LAYER_BOOST = {
    "memory": 3, "knowledge": 3, "filesystem": 2,
    "orchestration": 2, "graph": 1, "ingestion": 1,
    "cardindex": 1, "rag": 2, "search": 2,
}

STATUS_STEPS = {"agreed": 0, "replied": 1, "messaged": 2, "studied": 3, "none": 4}


def _parse_contacts_md() -> list[dict]:
    path = DOCS / "CONTACTS.md"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(
            r'\|\s*\*{0,2}(\w[\w-]*)\*{0,2}\s*\|'
            r'\s*([^|]+)\|'
            r'\s*([^|]+)\|'
            r'\s*(\d+)\s*\|',
            line,
        )
        if m and m.group(1).lower() not in ("автор", "---"):
            rows.append({
                "author":   m.group(1).strip(),
                "project":  m.group(2).strip(),
                "layer":    m.group(3).strip(),
                "mentions": int(m.group(4)),
            })
    return rows


def _get_contact_status(author: str) -> str:
    slug = re.sub(r'[^a-z0-9]', '-', author.lower())
    path = DOCS / "contacts" / f"{slug}.md"
    if not path.exists():
        return "none"
    text = path.read_text(encoding="utf-8")
    for key in ("agreed", "replied", "messaged", "studied"):
        labels = {
            "agreed":   "Договорились о сотрудничестве",
            "replied":  "Получили ответ",
            "messaged": "Написали первое сообщение",
            "studied":  "Изучили профиль",
        }
        if re.search(rf'\[x\].*{re.escape(labels[key])}', text, re.IGNORECASE):
            return key
    return "none"


def _layer_boost(layer: str) -> int:
    layer_lower = layer.lower()
    for key, val in LAYER_BOOST.items():
        if key in layer_lower:
            return val
    return 1


def _compute_score(author: dict, status: str) -> float:
    mentions = author["mentions"]
    status_step = STATUS_STEPS.get(status, 4)
    layer_b = _layer_boost(author["layer"])
    # Больше упоминаний → выше, меньше прогресс → выше приоритет
    return mentions * 3 + (4 - status_step) * 5 + layer_b * 2


def main() -> None:
    print("📊 improve_contact_priority.py — ранжирование контактов")

    authors = _parse_contacts_md()
    if not authors:
        print("⚠️  CONTACTS.md не найден или пустой. Запустите improve_contacts.py")
        return

    scored = []
    for a in authors:
        status = _get_contact_status(a["author"])
        score = _compute_score(a, status)
        scored.append({**a, "status": status, "score": score})

    scored.sort(key=lambda x: -x["score"])

    status_icons = {
        "agreed": "🤝", "replied": "💬", "messaged": "📬",
        "studied": "👁", "none": "⬜",
    }
    status_labels = {
        "agreed": "Договорились", "replied": "Ответили",
        "messaged": "Написали", "studied": "Изучили", "none": "Не начато",
    }

    lines = [
        "# Приоритет контактов\n",
        f"_Обновлено: {TODAY}_\n",
        "## Топ авторов по приоритету\n",
        "| # | Автор | Проект | Слой | Упоминаний | Статус | Балл |",
        "|---|-------|--------|------|-----------|--------|------|",
    ]
    for i, a in enumerate(scored, 1):
        icon = status_icons.get(a["status"], "⬜")
        label = status_labels.get(a["status"], "—")
        lines.append(
            f"| {i} | **{a['author']}** | {a['project']} | {a['layer']} "
            f"| {a['mentions']} | {icon} {label} | {a['score']:.0f} |"
        )

    lines += [
        "",
        "## Рекомендуемые следующие шаги\n",
    ]

    # Топ-3 не написанных
    not_messaged = [a for a in scored if a["status"] in ("none", "studied")][:3]
    if not_messaged:
        lines.append("### Написать первым (ещё не контактировали)\n")
        for a in not_messaged:
            slug = re.sub(r'[^a-z0-9]', '-', a["author"].lower())
            lines.append(
                f"1. **{a['author']}** ({a['project']}, {a['mentions']} упоминаний) "
                f"→ [открыть контакт](contacts/{slug}.md)"
            )

    # Ждём ответа
    waiting = [a for a in scored if a["status"] == "messaged"]
    if waiting:
        lines.append("\n### Ждём ответа (написали, но нет ответа)\n")
        for a in waiting:
            lines.append(f"- **{a['author']}** ({a['project']})")

    lines += [
        "",
        "## Формула расчёта балла\n",
        "```",
        "score = упоминания × 3 + (4 - шаг_статуса) × 5 + буст_слоя × 2",
        "шаг_статуса: none=4, studied=3, messaged=2, replied=1, agreed=0",
        "буст_слоя: memory/knowledge=3, rag/search/filesystem=2, остальные=1",
        "```",
        "",
        "_Чем выше балл — тем важнее написать первым._",
    ]

    out = DOCS / "CONTACT_PRIORITY.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  wrote: {out.relative_to(ROOT)}")
    print(f"  авторов: {len(scored)}")
    print(f"\n  Топ-3:")
    for a in scored[:3]:
        print(f"    {status_icons[a['status']]} {a['author']:15} score={a['score']:.0f}  {a['project']}")


if __name__ == "__main__":
    main()
