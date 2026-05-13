"""
improve_progress_sync.py — синхронизирует PROGRESS.md с реальным состоянием файлов.
Stage 2: оркестратор, читает файловую систему, обновляет прогресс детерминированно.

Что проверяет:
  Контакты:  сколько файлов в docs/contacts/, сколько с [x] отметками
  Обогащение: сколько файлов в docs/enriched/
  Архитектура: наличие ключевых документов
  Скрипты: сколько improve_*.py существует
  Дайджест: есть ли docs/DIGEST.md и сколько секций

Что обновляет в PROGRESS.md:
  - Блок ## Ключевые этапы — перерисовывает прогресс-бар и ✅/⬜
  - Блок ## Состояние компонентов — детальная таблица по факту
  - Блок ## Следующий шаг — первая незакрытая задача

Запуск:
    python scripts/improve_progress_sync.py
    python scripts/improve_progress_sync.py --dry-run  # только показать, не писать
"""
import re
import sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRIPTS = ROOT / "scripts"
DRY_RUN = "--dry-run" in sys.argv
TODAY = date.today().isoformat()
PROGRESS_PATH = DOCS / "PROGRESS.md"


# ---------------------------------------------------------------------------
# Сбор фактического состояния
# ---------------------------------------------------------------------------

def count_contacts() -> dict:
    """Сколько контактных файлов есть и с каким статусом."""
    contact_dir = DOCS / "contacts"
    if not contact_dir.exists():
        return {"total": 0, "studied": 0, "messaged": 0, "replied": 0, "agreed": 0}

    total = studied = messaged = replied = agreed = 0
    for f in contact_dir.glob("*.md"):
        if f.name == "README.md":
            continue
        text = f.read_text(encoding="utf-8")
        total += 1
        if re.search(r'\[x\].*Изучили профиль', text, re.IGNORECASE):
            studied += 1
        if re.search(r'\[x\].*Написали первое', text, re.IGNORECASE):
            messaged += 1
        if re.search(r'\[x\].*Получили ответ', text, re.IGNORECASE):
            replied += 1
        if re.search(r'\[x\].*Договорились', text, re.IGNORECASE):
            agreed += 1

    return {"total": total, "studied": studied,
            "messaged": messaged, "replied": replied, "agreed": agreed}


def count_enriched() -> dict:
    """Сколько файлов обогащено через LLM."""
    enriched_dir = DOCS / "enriched"
    if not enriched_dir.exists():
        return {"total": 0, "sections": []}
    files = list(enriched_dir.rglob("*-enriched.md"))
    sections = list({f.parent.name for f in files})
    return {"total": len(files), "sections": sections}


def count_scripts() -> dict:
    """Статус скриптов обработки."""
    all_scripts  = list(SCRIPTS.glob("improve_*.py"))
    llm_scripts  = [s for s in all_scripts if "llm" in s.name]
    util_scripts = list(SCRIPTS.glob("utils_*.py"))
    mcp_exists   = (SCRIPTS / "mcp_server.py").exists()
    return {
        "total":   len(all_scripts),
        "llm":     len(llm_scripts),
        "utils":   len(util_scripts),
        "mcp":     mcp_exists,
    }


def check_architecture_docs() -> dict:
    """Наличие ключевых архитектурных документов."""
    key_files = {
        "executive_summary": DOCS / "01-svyazi" / "01-executive-summary.md",
        "component_catalog": DOCS / "01-svyazi" / "03-component-catalog.md",
        "ensembles":         DOCS / "01-svyazi" / "04-ensembles-overview.md",
        "integration":       DOCS / "01-svyazi" / "11-integration-contracts.md",
        "roadmap":           DOCS / "01-svyazi" / "12-roadmap.md",
        "contacts_md":       DOCS / "CONTACTS.md",
        "decisions":         DOCS / "DECISIONS.md",
        "scoring":           DOCS / "SCORING.md",
    }
    return {k: v.exists() for k, v in key_files.items()}


def check_quality_scores() -> dict:
    """Текущие баллы качества из уже сгенерированных файлов."""
    result = {}

    health = DOCS / "HEALTH.md"
    if health.exists():
        m = re.search(r'Общий балл.*\*\*([\d.]+)/100\*\*', health.read_text(encoding="utf-8"))
        result["health"] = float(m.group(1)) if m else None

    metrics = DOCS / "METRICS.md"
    if metrics.exists():
        m = re.search(r'Средний балл.*\*\*([\d.]+)/100', metrics.read_text(encoding="utf-8"))
        result["metrics"] = float(m.group(1)) if m else None

    scoring = DOCS / "SCORING.md"
    if scoring.exists():
        m = re.search(r'Итог.*\((\d+)%\)', scoring.read_text(encoding="utf-8"))
        result["scoring"] = float(m.group(1)) if m else None

    return result


def check_digest() -> dict:
    """Состояние DIGEST.md."""
    digest = DOCS / "DIGEST.md"
    if not digest.exists():
        return {"exists": False, "sections": 0}
    text = digest.read_text(encoding="utf-8")
    sections = len(re.findall(r'^## ', text, re.MULTILINE))
    return {"exists": True, "sections": sections}


def check_skills() -> dict:
    skills_dir = ROOT / ".claude" / "skills"
    if not skills_dir.exists():
        return {"total": 0, "names": []}
    names = [f.stem for f in skills_dir.glob("*.md")]
    return {"total": len(names), "names": names}


def check_prototype() -> dict:
    """Проверяет готовность прототипа Knowledge OS."""
    demo    = SCRIPTS / "prototype_demo.py"
    gateway = SCRIPTS / "gateway.py"
    prec    = DOCS / "PRECISION_EVAL.md"
    hit_rate = None
    if prec.exists():
        m = re.search(r'Hit Rate@\d+\s*\|\s*\*\*([\d.]+)\*\*', prec.read_text(encoding="utf-8"))
        if m:
            hit_rate = float(m.group(1))
    return {
        "demo_exists":    demo.exists(),
        "gateway_exists": gateway.exists(),
        "hit_rate":       hit_rate,
        "ready": demo.exists() and gateway.exists() and hit_rate is not None and hit_rate >= 0.70,
    }


def check_testing() -> dict:
    """Проверяет наличие тестового покрытия."""
    tests_dir = ROOT / "tests"
    prec      = DOCS / "PRECISION_EVAL.md"
    n_tests   = len(list(tests_dir.glob("test_*.py"))) if tests_dir.exists() else 0
    hit_pass  = False
    if prec.exists():
        hit_pass = "✅ PASS" in prec.read_text(encoding="utf-8")
    return {
        "n_test_files": n_tests,
        "hit_rate_pass": hit_pass,
        "ready": n_tests >= 5 and hit_pass,
    }


def check_published() -> dict:
    """Проверяет наличие git-тега v* (признак публикации MVP)."""
    import subprocess
    try:
        result = subprocess.run(
            ["git", "tag", "--list", "v*"],
            capture_output=True, text=True, cwd=str(ROOT), timeout=10,
        )
        tags = [t.strip() for t in result.stdout.splitlines() if t.strip()]
    except Exception:
        tags = []
    return {
        "tags": tags,
        "ready": len(tags) > 0,
    }


# ---------------------------------------------------------------------------
# Вычисление статуса milestone
# ---------------------------------------------------------------------------

def compute_milestones(contacts: dict, enriched: dict, arch: dict,
                       scripts: dict, digest: dict,
                       prototype: dict | None = None,
                       testing: dict | None = None,
                       published: dict | None = None) -> list[dict]:
    """Возвращает список milestone с реальным статусом."""
    return [
        {
            "title": "Определена архитектура Svyazi 2.0",
            "done":  arch["executive_summary"] and arch["component_catalog"],
            "detail": "docs/01-svyazi/01-executive-summary.md + 03-component-catalog.md",
        },
        {
            "title": "Составлен каталог 20+ компонентов",
            "done":  arch["component_catalog"],
            "detail": "docs/01-svyazi/03-component-catalog.md",
        },
        {
            "title": "Выявлены 5 ансамблей",
            "done":  arch["ensembles"],
            "detail": "docs/01-svyazi/04-ensembles-overview.md",
        },
        {
            "title": "Описаны интеграционные контракты",
            "done":  arch["integration"],
            "detail": "docs/01-svyazi/11-integration-contracts.md",
        },
        {
            "title": "Составлены контакты авторов",
            "done":  contacts["total"] >= 10,
            "detail": f"docs/contacts/: {contacts['total']} файлов",
        },
        {
            "title": "Написаны авторам ключевых компонентов",
            "done":  contacts["messaged"] >= 3,
            "detail": f"Написали: {contacts['messaged']}/{contacts['total']}",
        },
        {
            "title": "Получены ответы от авторов",
            "done":  contacts["replied"] >= 2,
            "detail": f"Ответили: {contacts['replied']}/{contacts['total']}",
        },
        {
            "title": "LLM-обогащение проектных файлов",
            "done":  enriched["total"] >= 10,
            "detail": f"docs/enriched/: {enriched['total']} файлов",
        },
        {
            "title": "Создан рабочий прототип Knowledge OS",
            "done":  (prototype or {}).get("ready", False),
            "detail": (
                f"gateway.py + prototype_demo.py, Hit Rate@10={prototype['hit_rate']:.3f} ✅"
                if prototype and prototype.get("ready")
                else "scripts/gateway.py + prototype_demo.py + Hit Rate@10 ≥ 0.70"
            ),
        },
        {
            "title": "Пройдено тестирование ансамбля",
            "done":  (testing or {}).get("ready", False),
            "detail": (
                f"{testing['n_test_files']} тестовых файлов, Hit Rate@10 PASS ✅"
                if testing and testing.get("ready")
                else "tests/ ≥ 5 файлов + Hit Rate@10 PASS"
            ),
        },
        {
            "title": "Опубликован MVP на GitHub",
            "done":  (published or {}).get("ready", False),
            "detail": (
                f"git tag {', '.join((published or {}).get('tags', []))} ✅"
                if published and published.get("ready")
                else "Создать git tag v* для публикации MVP"
            ),
        },
    ]


def progress_bar(done: int, total: int, width: int = 20) -> str:
    filled = round(done / total * width) if total > 0 else 0
    bar = "█" * filled + "░" * (width - filled)
    pct = round(done / total * 100) if total > 0 else 0
    return f"`{bar} {pct}%` {done}/{total}"


# ---------------------------------------------------------------------------
# Построение нового PROGRESS.md
# ---------------------------------------------------------------------------

def build_progress_md(
    milestones: list[dict],
    contacts: dict,
    enriched: dict,
    scripts: dict,
    scores: dict,
    digest: dict,
    skills: dict,
) -> str:
    done_count = sum(1 for m in milestones if m["done"])
    total_count = len(milestones)

    lines = [
        "# Прогресс MVP",
        "",
        f"_Обновлено: {TODAY} (improve_progress_sync.py)_",
        "",
        "## Ключевые этапы (Milestones)",
        "",
        progress_bar(done_count, total_count),
        "",
    ]

    for m in milestones:
        mark = "✅" if m["done"] else "⬜"
        lines.append(f"{mark} {m['title']}")

    # Следующий незакрытый
    next_m = next((m for m in milestones if not m["done"]), None)

    lines += [
        "",
        "## Состояние компонентов",
        "",
        "| Компонент | Статус | Детали |",
        "|-----------|--------|--------|",
    ]

    # Контакты
    c = contacts
    if c["total"] == 0:
        c_status = "❌ не создано"
    elif c["messaged"] == 0:
        c_status = f"⚠️ {c['total']} файлов, не отправлено"
    elif c["replied"] == 0:
        c_status = f"📬 написали {c['messaged']}, ждём ответов"
    else:
        c_status = f"✅ {c['replied']} ответов"
    lines.append(f"| Контакты авторов | {c_status} | {c['total']} файлов в docs/contacts/ |")

    # Обогащение
    if enriched["total"] == 0:
        e_status = "⬜ не запущено"
    elif enriched["total"] < 10:
        e_status = f"🔄 {enriched['total']} файлов"
    else:
        e_status = f"✅ {enriched['total']} файлов"
    lines.append(f"| LLM-обогащение | {e_status} | pip install anthropic && python scripts/improve_llm_enrich.py |")

    # Скрипты
    lines.append(f"| Скрипты обработки | ✅ {scripts['total']} скриптов | "
                 f"{scripts['llm']} LLM-скриптов, MCP={'✅' if scripts['mcp'] else '❌'} |")

    # Дайджест
    if digest["exists"] and digest["sections"] > 0:
        d_status = f"✅ {digest['sections']} секций"
    elif digest["exists"]:
        d_status = "⚠️ пустой"
    else:
        d_status = "⬜ не создан"
    lines.append(f"| DIGEST.md | {d_status} | python scripts/improve_llm_summary.py |")

    # Скиллы
    if skills["total"] > 0:
        sk_status = f"✅ {skills['total']} скиллов"
    else:
        sk_status = "❌ нет"
    lines.append(f"| Claude Skills | {sk_status} | {', '.join(skills['names'])} |")

    lines += [
        "",
        "## Метрики качества",
        "",
        "| Метрика | Балл | Статус |",
        "|---------|------|--------|",
    ]

    def score_status(v, good=80, ok=60):
        if v is None: return "—", "❓"
        icon = "🟢" if v >= good else ("🟡" if v >= ok else "🔴")
        return f"{v:.1f}/100", icon

    h_val, h_icon = score_status(scores.get("health"), 85, 70)
    m_val, m_icon = score_status(scores.get("metrics"), 75, 60)
    s_val, s_icon = score_status(scores.get("scoring"), 95, 80)
    lines.append(f"| Здоровье репо (HEALTH) | {h_val} | {h_icon} |")
    lines.append(f"| Качество доков (METRICS) | {m_val} | {m_icon} |")
    lines.append(f"| Go/No-Go (SCORING) | {s_val} | {s_icon} |")

    # Следующий шаг
    lines += ["", "## Следующий шаг", ""]
    if next_m:
        lines.append(f"➡️ **{next_m['title']}**")
        lines.append("")
        lines.append(f"_{next_m['detail']}_")
        lines.append("")

        # Конкретные действия для первых незакрытых
        if "Написаны авторам" in next_m["title"]:
            lines += [
                "Контактные файлы готовы. Откройте и отправьте:",
                "",
                "```bash",
                "# Приоритет 1: kksudo (AgentFS, 13 упоминаний)",
                "cat docs/contacts/kksudo.md",
                "",
                "# Приоритет 2: spbmolot (NGT Memory, 12 упоминаний)",
                "cat docs/contacts/spbmolot.md",
                "",
                "# Приоритет 3: AnastasiyaW (knowledge-space, 11 упоминаний)",
                "cat docs/contacts/anastasiyaw.md",
                "```",
            ]
        elif "Написали" in (next_m.get("detail") or "") and "LLM" in next_m["title"]:
            lines += [
                "```bash",
                "pip install anthropic",
                "python scripts/improve_llm_enrich.py --section 05-habr-projects",
                "```",
            ]

    lines += [
        "",
        "## Связанные документы",
        "",
        "- [Контакты авторов](CONTACTS.md)",
        "- [Go/No-Go Scoring](SCORING.md)",
        "- [Health Dashboard](HEALTH.md)",
        "- [MVP Planning](01-svyazi/07-mvp-planning.md)",
        "",
        "<!-- auto-end -->",
        "",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    print("📊 improve_progress_sync.py — синхронизация PROGRESS.md")
    if DRY_RUN:
        print("   Режим: dry-run\n")

    print("Собираем состояние...")
    contacts  = count_contacts()
    enriched  = count_enriched()
    scripts   = count_scripts()
    arch      = check_architecture_docs()
    scores    = check_quality_scores()
    digest    = check_digest()
    skills    = check_skills()
    prototype  = check_prototype()
    testing    = check_testing()
    published  = check_published()

    print(f"  Контакты:   {contacts['total']} файлов "
          f"(написали: {contacts['messaged']}, ответили: {contacts['replied']})")
    print(f"  Обогащено:  {enriched['total']} файлов")
    print(f"  Скрипты:    {scripts['total']} (LLM: {scripts['llm']})")
    print(f"  Баллы:      health={scores.get('health')}, "
          f"metrics={scores.get('metrics')}, scoring={scores.get('scoring')}")
    print(f"  Опубликован: тегов={len(published['tags'])}")
    print()

    milestones = compute_milestones(contacts, enriched, arch, scripts, digest,
                                    prototype=prototype, testing=testing,
                                    published=published)
    done = sum(1 for m in milestones if m["done"])
    print(f"Milestones: {done}/{len(milestones)}")
    for m in milestones:
        print(f"  {'✅' if m['done'] else '⬜'} {m['title']}")
    print()

    new_content = build_progress_md(
        milestones, contacts, enriched, scripts, scores, digest, skills
    )

    if DRY_RUN:
        print("--- PROGRESS.md (preview) ---")
        print(new_content[:1500])
        print("...")
        return

    # Сохраняем ручные секции после маркера <!-- auto-end -->
    manual_suffix = ""
    if PROGRESS_PATH.exists():
        existing = PROGRESS_PATH.read_text(encoding="utf-8")
        marker = "<!-- auto-end -->"
        if marker in existing:
            manual_suffix = existing.split(marker, 1)[1]

    final_content = new_content
    if manual_suffix.strip():
        final_content = new_content.rstrip() + "\n" + manual_suffix

    PROGRESS_PATH.write_text(final_content, encoding="utf-8")
    print(f"✅ {PROGRESS_PATH.relative_to(ROOT)} обновлён")
    print(f"   Следующий шаг: {next((m['title'] for m in milestones if not m['done']), 'Всё готово!')}")


if __name__ == "__main__":
    main()
