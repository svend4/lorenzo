"""
improve_recipe.py — умная система рецептов: последовательности скриптов под конкретную цель.

Рецепт = именованная цепочка скриптов для решения типовой задачи.
Встроенные рецепты охватывают 21 группу; пользователь может добавлять свои.

Команды:
  --list                      список всех рецептов
  --find "улучшить качество"  найти рецепты по описанию цели
  --run <name>                запустить рецепт
  --run <name> --dry-run      показать что будет запущено
  --info <name>               подробная информация о рецепте
  --add <name> --desc "..." --scripts a.py b.py ...  добавить свой рецепт
  --delete <name>             удалить пользовательский рецепт

Запуск:
  python scripts/improve_recipe.py --list
  python scripts/improve_recipe.py --find "найти похожие документы"
  python scripts/improve_recipe.py --run quality-check --dry-run
  python scripts/improve_recipe.py --run full-index
"""
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT    = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
CUSTOM_RECIPES_FILE = SCRIPTS / "recipes.json"

# ─────────────────────────────────────────────────────────────────────
# Встроенные рецепты
# ─────────────────────────────────────────────────────────────────────

BUILTIN_RECIPES: dict[str, dict] = {
    # ── Качество и аудит ───────────────────────────────────────────
    "quality-check": {
        "description": "Полная проверка качества: орфография, ссылки, заголовки, пустые секции",
        "tags": ["quality", "audit", "check", "validation", "проверка"],
        "scripts": [
            ("improve_spellcheck.py",     []),
            ("improve_broken_links.py",   []),
            ("improve_heading_audit.py",  []),
            ("improve_empty_sections.py", []),
            ("improve_validate.py",       []),
            ("improve_consistency.py",    []),
        ],
    },
    "quality-metrics": {
        "description": "Метрики качества: читаемость, словарь, пассивный залог, дубликаты",
        "tags": ["quality", "metrics", "readability", "метрики"],
        "scripts": [
            ("improve_readability_v2.py",       []),
            ("improve_vocabulary_richness.py",   []),
            ("improve_passive_voice.py",         []),
            ("improve_paragraph_quality.py",     []),
            ("improve_dedup.py",                 []),
        ],
    },

    # ── Поиск и индекс ─────────────────────────────────────────────
    "build-search-index": {
        "description": "Построить полный поисковый индекс: passages + search_index",
        "tags": ["search", "index", "bm25", "поиск", "индекс"],
        "scripts": [
            ("improve_passage_retrieval.py", ["--index"]),
            ("improve_index_update.py",      []),
            ("improve_keyword_index.py",     []),
        ],
    },
    "full-index": {
        "description": "Полный индекс + все аналитические карты (медленно, ~5 мин)",
        "tags": ["index", "full", "analytics", "полный"],
        "scripts": [
            ("improve_passage_retrieval.py",    ["--index"]),
            ("improve_index_update.py",         []),
            ("improve_keyword_index.py",        []),
            ("improve_topic_model.py",          []),
            ("improve_concept_graph.py",        []),
            ("improve_similar_passages.py",     []),
            ("improve_knowledge_map.py",        []),
        ],
    },

    # ── Отчёты и дашборды ─────────────────────────────────────────
    "dashboard": {
        "description": "Обновить все дашборды: здоровье, метрики, оценка",
        "tags": ["reports", "dashboard", "health", "дашборд", "отчёт"],
        "scripts": [
            ("improve_health.py",   []),
            ("improve_metrics.py",  []),
            ("improve_scoring.py",  []),
            ("improve_stats.py",    []),
            ("improve_coverage.py", []),
        ],
    },
    "executive-report": {
        "description": "Итоговый отчёт для стейкхолдеров: REPORT.md + DIGEST.md",
        "tags": ["report", "executive", "summary", "отчёт", "итог"],
        "scripts": [
            ("improve_decisions.py",      []),
            ("improve_action_items.py",   []),
            ("improve_kpi.py",            []),
            ("improve_export_report.py",  []),
            ("improve_digest.py",         []),
        ],
    },

    # ── Структура документов ───────────────────────────────────────
    "enrich-docs": {
        "description": "Обогатить документы: TOC, аннотации, теги, see-also",
        "tags": ["enrich", "structure", "toc", "tags", "обогащение"],
        "scripts": [
            ("improve_auto_toc.py",   ["--apply"]),
            ("improve_tags.py",       []),
            ("improve_see_also.py",   []),
            ("improve_glossary.py",   []),
            ("improve_footnotes.py",  []),
        ],
    },
    "add-summaries": {
        "description": "Добавить аннотации + TextRank резюме в документы",
        "tags": ["summaries", "abstract", "textrank", "аннотации"],
        "scripts": [
            ("improve_summaries.py", []),
            ("improve_textrank.py",  []),
            ("improve_abstract.py",  ["--apply"]),
        ],
    },

    # ── Связи и навигация ──────────────────────────────────────────
    "build-links": {
        "description": "Построить все связи: обратные ссылки, перекрёстные ссылки, похожие",
        "tags": ["links", "backlinks", "crossrefs", "related", "ссылки"],
        "scripts": [
            ("improve_backlinks.py",  []),
            ("improve_crossrefs.py",  []),
            ("improve_similar.py",    []),
            ("improve_graph.py",      []),
            ("improve_sitemap.py",    []),
        ],
    },
    "reading-guide": {
        "description": "Гиды для чтения: порядок, список, карта знаний",
        "tags": ["reading", "navigation", "guide", "чтение", "навигация"],
        "scripts": [
            ("improve_reading_order.py", []),
            ("improve_reading_time.py",  []),
            ("improve_outline.py",       []),
            ("improve_knowledge_map.py", []),
        ],
    },

    # ── Анализ контента ────────────────────────────────────────────
    "content-analysis": {
        "description": "Глубокий анализ: сущности, концепты, вопросы, временная шкала",
        "tags": ["analysis", "ner", "concepts", "timeline", "анализ"],
        "scripts": [
            ("improve_named_entity_index.py", []),
            ("improve_concept_graph.py",      []),
            ("improve_question_extractor.py", []),
            ("improve_timeline_events.py",    []),
            ("improve_contradiction_check.py",[]),
        ],
    },
    "topic-clustering": {
        "description": "Тематическая кластеризация: TF-IDF модель + хитмап + плотность",
        "tags": ["topics", "clustering", "heatmap", "тематика", "кластеры"],
        "scripts": [
            ("improve_topic_model.py",  []),
            ("improve_clusters.py",     []),
            ("improve_heatmap.py",      []),
            ("improve_density.py",      []),
            ("improve_word_freq.py",    []),
        ],
    },

    # ── Экспорт ────────────────────────────────────────────────────
    "export-all": {
        "description": "Экспорт во все форматы: HTML, JSON, CSV, RSS, Obsidian",
        "tags": ["export", "html", "json", "rss", "obsidian", "экспорт"],
        "scripts": [
            ("improve_export_html.py",  []),
            ("improve_export_json.py",  []),
            ("improve_export_csv.py",   []),
            ("improve_rss.py",          []),
            ("improve_obsidian.py",     []),
        ],
    },

    # ── Контакты ───────────────────────────────────────────────────
    "contacts-workflow": {
        "description": "Полный цикл работы с контактами: обогащение, приоритет, шаблоны",
        "tags": ["contacts", "authors", "outreach", "контакты", "авторы"],
        "scripts": [
            ("improve_contacts.py",         []),
            ("improve_contact_priority.py", []),
            ("improve_entities.py",         []),
            ("improve_autofill.py",         []),
        ],
    },

    # ── CI/CD ──────────────────────────────────────────────────────
    "setup-cicd": {
        "description": "Настроить CI/CD: GitHub Actions, pre-commit, dependabot",
        "tags": ["cicd", "github", "ci", "automation", "ci/cd"],
        "scripts": [
            ("improve_ci_config.py",     []),
            ("improve_pre_commit.py",    []),
            ("improve_dependabot.py",    []),
            ("improve_github_issues.py", []),
        ],
    },

    # ── Мета ───────────────────────────────────────────────────────
    "meta-docs": {
        "description": "Мета-документы репо: радар технологий, онбординг, реестр рисков",
        "tags": ["meta", "radar", "onboarding", "risks", "мета"],
        "scripts": [
            ("improve_tech_radar.py",       []),
            ("improve_onboarding.py",       []),
            ("improve_risk_register.py",    []),
            ("improve_component_matrix.py", []),
            ("improve_kpi_snapshot.py",     []),
        ],
    },
    "scripts-audit": {
        "description": "Аудит и обогащение самих скриптов (метауровень)",
        "tags": ["scripts", "audit", "meta", "self", "скрипты"],
        "scripts": [
            ("improve_self.py", ["--audit"]),
            ("improve_self.py", ["--catalog"]),
            ("improve_self.py", ["--cross-read"]),
            ("improve_benchmark.py", []),
        ],
    },

    # ── Habr-проекты ───────────────────────────────────────────────
    "habr-deep-dive": {
        "description": "Глубокий анализ Habr-проектов: память, граф знаний, синтез",
        "tags": ["habr", "projects", "memory", "knowledge", "хабр"],
        "scripts": [
            ("improve_subtopic_fill.py", ["--apply", "--section", "05-habr-projects"]),
            ("improve_gap_filler.py",    ["--apply", "--mode", "link"]),
            ("improve_auto_linker.py",   ["--apply", "--types", "projects"]),
        ],
    },

    # ── Полный пайплайн ────────────────────────────────────────────
    "morning-run": {
        "description": "Ежедневный пайплайн: дашборд + дайджест + проверка качества (~3 мин)",
        "tags": ["daily", "pipeline", "morning", "ежедневный", "утро"],
        "scripts": [
            ("improve_health.py",        []),
            ("improve_metrics.py",       []),
            ("improve_digest_auto.py",   []),
            ("improve_version_diff.py",  ["--last", "5"]),
            ("improve_broken_links.py",  []),
            ("improve_content_gaps.py",  []),
        ],
    },
    "weekly-full": {
        "description": "Еженедельный полный прогон: всё от индекса до экспорта (~15 мин)",
        "tags": ["weekly", "full", "pipeline", "еженедельный"],
        "scripts": [
            ("improve_passage_retrieval.py", ["--index"]),
            ("improve_index_update.py",      []),
            ("improve_health.py",            []),
            ("improve_metrics.py",           []),
            ("improve_textrank.py",          []),
            ("improve_topic_model.py",       []),
            ("improve_knowledge_map.py",     []),
            ("improve_export_report.py",     []),
            ("improve_digest_auto.py",       []),
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────
# Загрузка пользовательских рецептов
# ─────────────────────────────────────────────────────────────────────

def _load_custom() -> dict:
    if CUSTOM_RECIPES_FILE.exists():
        try:
            return json.loads(CUSTOM_RECIPES_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_custom(custom: dict) -> None:
    CUSTOM_RECIPES_FILE.write_text(
        json.dumps(custom, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def _all_recipes() -> dict:
    merged = dict(BUILTIN_RECIPES)
    merged.update(_load_custom())
    return merged


# ─────────────────────────────────────────────────────────────────────
# Поиск рецептов по ключевым словам
# ─────────────────────────────────────────────────────────────────────

STOPWORDS = {"и","в","на","что","как","это","для","или","но","по","к","из",
             "the","a","an","of","in","to","is","for","with","by"}

def _score_recipe(goal_tokens: list[str], recipe: dict) -> int:
    tokens_in = set(goal_tokens)
    desc_words = set(re.findall(r'[а-яёa-z]{3,}', recipe["description"].lower()))
    tag_words  = set(" ".join(recipe.get("tags", [])).lower().split())
    hits = len(tokens_in & (desc_words | tag_words))
    return hits


def cmd_find(goal: str) -> None:
    tokens = [t for t in re.findall(r'[а-яёa-z]{3,}', goal.lower())
              if t not in STOPWORDS]
    recipes = _all_recipes()

    scored = []
    for name, r in recipes.items():
        s = _score_recipe(tokens, r)
        if s > 0:
            scored.append((s, name, r))

    scored.sort(key=lambda x: -x[0])

    if not scored:
        print(f"  Нет рецептов по запросу: «{goal}»")
        print("  Попробуйте: --list  или  другие ключевые слова")
        return

    print(f"\n  Рецепты по запросу «{goal}»:\n")
    for score, name, r in scored[:6]:
        custom_mark = " [custom]" if name not in BUILTIN_RECIPES else ""
        n = len(r["scripts"])
        print(f"  {'★' * min(score,5):<6} {name}{custom_mark}")
        print(f"         {r['description']}")
        print(f"         {n} скриптов  |  теги: {', '.join(r.get('tags',[])[:4])}")
        print()
    print(f"  Запуск: python scripts/improve_recipe.py --run <name> [--dry-run]")


# ─────────────────────────────────────────────────────────────────────
# Список рецептов
# ─────────────────────────────────────────────────────────────────────

def cmd_list(group_filter: str = "") -> None:
    recipes = _all_recipes()
    custom  = _load_custom()

    # Сгруппируем по первому тегу
    groups: dict[str, list] = {}
    for name, r in recipes.items():
        tag = r.get("tags", ["other"])[0]
        groups.setdefault(tag, []).append((name, r))

    print(f"\n{'═'*62}")
    print(f"  Lorenzo Recipes  —  {len(recipes)} рецептов ({len(custom)} пользовательских)")
    print(f"{'═'*62}\n")

    for tag, items in sorted(groups.items()):
        if group_filter and group_filter not in tag:
            continue
        print(f"  ▸ {tag.upper()}")
        for name, r in items:
            cmark = " [✎]" if name in custom else ""
            n = len(r["scripts"])
            print(f"    {name:<28} {r['description'][:38]:<38} [{n} скр.]{cmark}")
        print()

    print(f"  python scripts/improve_recipe.py --info <name>")
    print(f"  python scripts/improve_recipe.py --run  <name> [--dry-run]\n")


# ─────────────────────────────────────────────────────────────────────
# Детали рецепта
# ─────────────────────────────────────────────────────────────────────

def cmd_info(name: str) -> None:
    recipes = _all_recipes()
    if name not in recipes:
        print(f"  ❌ Рецепт не найден: {name}")
        print(f"  Доступные: {', '.join(list(recipes)[:8])} ...")
        return

    r = recipes[name]
    custom = name in _load_custom()
    print(f"\n{'─'*60}")
    print(f"  Рецепт: {name}  {'[пользовательский]' if custom else '[встроенный]'}")
    print(f"  {r['description']}")
    print(f"  Теги: {', '.join(r.get('tags', []))}")
    print(f"\n  Скрипты ({len(r['scripts'])}):")
    for i, (script, args) in enumerate(r["scripts"], 1):
        path = SCRIPTS / script
        exists = "✅" if path.exists() else "❌"
        args_str = " ".join(args) if args else ""
        print(f"    {i:2}. {exists} {script}  {args_str}")
    print()
    print(f"  Запуск:    python scripts/improve_recipe.py --run {name}")
    print(f"  Пробный:   python scripts/improve_recipe.py --run {name} --dry-run\n")


# ─────────────────────────────────────────────────────────────────────
# Выполнение рецепта
# ─────────────────────────────────────────────────────────────────────

def cmd_run(name: str, dry_run: bool) -> None:
    recipes = _all_recipes()
    if name not in recipes:
        print(f"  ❌ Рецепт не найден: {name}")
        # Попробовать нечёткий поиск
        close = [n for n in recipes if name in n or n in name]
        if close:
            print(f"  Похожие: {', '.join(close)}")
        return

    r = recipes[name]
    scripts = r["scripts"]

    mode = "[dry-run]" if dry_run else ""
    print(f"\n{'═'*60}")
    print(f"  Рецепт: {name}  {mode}")
    print(f"  {r['description']}")
    print(f"  Скриптов: {len(scripts)}")
    print(f"{'═'*60}\n")

    results: list[tuple[str, bool, float]] = []

    for i, (script, args) in enumerate(scripts, 1):
        path = SCRIPTS / script
        if not path.exists():
            print(f"  {i}/{len(scripts)} ❌ SKIP  {script}  (файл не найден)")
            results.append((script, False, 0.0))
            continue

        cmd = [sys.executable, str(path)] + args
        if dry_run and "--dry-run" not in args:
            cmd.append("--dry-run")

        print(f"  {i}/{len(scripts)} ▶  {script}  {' '.join(args)}", end="", flush=True)
        if dry_run:
            print("  [пропуск в dry-run режиме]")
            results.append((script, True, 0.0))
            continue

        t0 = time.time()
        try:
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120, cwd=str(ROOT)
            )
            elapsed = time.time() - t0
            ok = proc.returncode == 0
            status = "✅" if ok else "⚠"
            print(f"  {status}  ({elapsed:.1f}с)")
            if not ok and proc.stderr:
                for line in proc.stderr.strip().split("\n")[-3:]:
                    print(f"      {line}")
            results.append((script, ok, elapsed))
        except subprocess.TimeoutExpired:
            print("  ⏱ TIMEOUT (120с)")
            results.append((script, False, 120.0))
        except Exception as e:
            print(f"  ❌ {e}")
            results.append((script, False, 0.0))

    # Итог
    total = time.time()
    ok_count = sum(1 for _, ok, _ in results if ok)
    total_sec = sum(t for _, _, t in results)
    print(f"\n{'─'*60}")
    if dry_run:
        print(f"  [dry-run] {len(scripts)} скриптов в рецепте «{name}»")
        print(f"  Запуск без --dry-run применит изменения.\n")
    else:
        print(f"  Итог: {ok_count}/{len(scripts)} успешно  |  {total_sec:.1f}с суммарно\n")


# ─────────────────────────────────────────────────────────────────────
# Добавление / удаление пользовательских рецептов
# ─────────────────────────────────────────────────────────────────────

def cmd_add(name: str, description: str, scripts_list: list[str]) -> None:
    if name in BUILTIN_RECIPES:
        print(f"  ❌ Имя «{name}» зарезервировано встроенным рецептом")
        return

    custom = _load_custom()
    parsed_scripts = []
    for s in scripts_list:
        if s.startswith("--"):
            if parsed_scripts:
                parsed_scripts[-1][1].append(s)
        else:
            parsed_scripts.append([s, []])

    custom[name] = {
        "description": description,
        "tags": [name.split("-")[0]],
        "scripts": [[s, a] for s, a in parsed_scripts],
    }
    _save_custom(custom)
    print(f"  ✅ Рецепт «{name}» добавлен ({len(parsed_scripts)} скриптов)")
    print(f"     Файл: {CUSTOM_RECIPES_FILE.relative_to(ROOT)}")


def cmd_delete(name: str) -> None:
    if name in BUILTIN_RECIPES:
        print(f"  ❌ Нельзя удалить встроенный рецепт «{name}»")
        return
    custom = _load_custom()
    if name not in custom:
        print(f"  ❌ Пользовательский рецепт «{name}» не найден")
        return
    del custom[name]
    _save_custom(custom)
    print(f"  ✅ Рецепт «{name}» удалён")


# ─────────────────────────────────────────────────────────────────────
# main
# ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Умная система рецептов: именованные цепочки скриптов"
    )
    parser.add_argument("--list",    action="store_true",
                        help="Список всех рецептов")
    parser.add_argument("--find",    metavar="ЦЕЛЬ",
                        help="Найти рецепты по описанию цели")
    parser.add_argument("--run",     metavar="ИМЯ",
                        help="Запустить рецепт")
    parser.add_argument("--info",    metavar="ИМЯ",
                        help="Подробная информация о рецепте")
    parser.add_argument("--add",     metavar="ИМЯ",
                        help="Добавить пользовательский рецепт")
    parser.add_argument("--delete",  metavar="ИМЯ",
                        help="Удалить пользовательский рецепт")
    parser.add_argument("--desc",    metavar="ТЕКСТ",
                        help="Описание рецепта (для --add)")
    parser.add_argument("--scripts", nargs="+", metavar="СКРИПТ",
                        help="Список скриптов (для --add)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Показать план без запуска скриптов")
    parser.add_argument("--group",   metavar="ТЕМА",
                        help="Фильтр по первому тегу (для --list)")
    args = parser.parse_args()

    if args.list:
        cmd_list(group_filter=args.group or "")
    elif args.find:
        cmd_find(args.find)
    elif args.run:
        cmd_run(args.run, dry_run=args.dry_run)
    elif args.info:
        cmd_info(args.info)
    elif args.add:
        if not args.desc or not args.scripts:
            print("  ❌ Для --add нужны --desc и --scripts")
            sys.exit(1)
        cmd_add(args.add, args.desc, args.scripts)
    elif args.delete:
        cmd_delete(args.delete)
    else:
        cmd_list()


if __name__ == "__main__":
    main()
