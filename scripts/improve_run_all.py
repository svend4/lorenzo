"""
improve_run_all.py — мастер-скрипт для запуска всех improve_*.py.
Запускает скрипты в правильном порядке (зависимости учтены).

Флаги:
  --fast          Пропускает медленные скрипты (clusters, similar, html-export)
  --smart         Условный запуск: пропускает если метрика выше порога
  --dry-run       Показывает план без реального запуска
  --group X       Запускает только одну группу
  --changed       Запускает только скрипты, связанные с git-изменёнными файлами
  --only a,b,c    Запускает конкретные скрипты (без группировки)
  --parallel N    Запускает группы параллельно в N потоках (по умолчанию 1)
  --report        После прогона показывает git diff --stat изменённых файлов

Группы (в порядке выполнения):
  structure → index → analysis → extract → quality →
  graph → generate → reports → export

Запуск: python scripts/improve_run_all.py
        python scripts/improve_run_all.py --fast --smart
        python scripts/improve_run_all.py --group generate
        python scripts/improve_run_all.py --changed
        python scripts/improve_run_all.py --only improve_metrics.py,improve_health.py
        python scripts/improve_run_all.py --parallel 4 --report
"""
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).parent.parent

# Группы скриптов с порядком выполнения
GROUPS = {
    "structure": [
        # Базовая структура (запускать первыми)
        "improve_merge_short.py",
        "improve_readmes.py",
        "improve_summaries.py",
        "improve_tags.py",
        "improve_toc.py",
        "improve_autocorrect.py",
    ],
    "index": [
        # Индексы и поиск
        "improve_glossary.py",
        "improve_crossrefs.py",
        "improve_search_index.py",
        "improve_index_update.py",
        "improve_timeline.py",
        "improve_backlinks.py",
    ],
    "analysis": [
        # Аналитика
        "improve_dedup.py",
        "improve_clusters.py",
        "improve_word_freq.py",
        "improve_priorities.py",
        "improve_similar.py",
        "improve_complexity.py",
        "improve_sentiment.py",
        "improve_density.py",
        "improve_heatmap.py",
    ],
    "extract": [
        # Извлечение данных
        "improve_action_items.py",
        "improve_decisions.py",
        "improve_questions.py",
        "improve_kpi.py",
        "improve_entities.py",
        "improve_concepts.py",
        "improve_abbreviations.py",
        "improve_extract_tables.py",
        "improve_extract_code.py",
    ],
    "quality": [
        # Качество и валидация
        "improve_consistency.py",
        "improve_broken_links.py",
        "improve_missing.py",
        "improve_orphans.py",
        "improve_validate.py",
        "improve_metrics.py",
        "improve_alerts.py",
        "improve_spellcheck.py",
        "improve_readability_v2.py",
        "improve_content_gaps.py",
    ],
    "graph": [
        # Граф и визуализация
        "improve_graph.py",
        "improve_mindmap.py",
        "improve_network.py",
        "improve_narrative.py",
    ],
    "reports": [
        # Отчёты (запускать последними)
        "improve_qa.py",
        "improve_contacts.py",
        "improve_changelog.py",
        "improve_reading_order.py",
        "improve_stats.py",
        "improve_health.py",
        "improve_compare.py",
        "improve_sitemap.py",
        "improve_report.py",
    ],
    "generate": [
        # Генерация файлов из шаблонов и данных (после extract/analysis)
        "improve_templates.py",
        "improve_autofill.py",
        "improve_footnotes.py",
        "improve_see_also.py",
        "improve_faq.py",
        "improve_badges.py",
        "improve_word_cloud.py",
    ],
    "reports": [
        # Отчёты (запускать последними)
        "improve_qa.py",
        "improve_contacts.py",
        "improve_changelog.py",
        "improve_reading_order.py",
        "improve_stats.py",
        "improve_health.py",
        "improve_compare.py",
        "improve_sitemap.py",
        "improve_scoring.py",
        "improve_cost.py",
        "improve_schedule.py",
        "improve_digest.py",
        "improve_progress.py",
        "improve_progress_sync.py",
        "improve_contact_priority.py",
        "improve_staleness.py",
        "improve_coverage.py",
        "improve_benchmark.py",
        "improve_report.py",
    ],
    "export": [
        # Экспорт
        "improve_export_csv.py",
        "improve_export_json.py",
        "improve_export_html.py",
        "improve_obsidian.py",
        "improve_rss.py",
        "improve_confluence.py",
        "improve_export_report.py",  # единый сводный отчёт → REPORT.md
    ],
    "cicd": [
        # CI/CD и автоматизация разработки
        "improve_github_issues.py",
        "improve_ci_config.py",
        "improve_pre_commit.py",
        "improve_dependabot.py",
    ],
    "analytics": [
        # Глубокая аналитика
        "improve_citation_index.py",
        "improve_reading_time.py",
        "improve_version_diff.py",
        "improve_topic_model.py",
        "improve_cross_section.py",  # концептуальные мосты между секциями
        "improve_digest_auto.py",    # автодайджест изменений за N дней
    ],
    "textwork": [
        # Работа с текстом: рубрикация, слияние, сравнение
        "improve_outline.py",
        "improve_reclassify.py",
        "improve_merge_by_topic.py",
        "improve_compare_docs.py",
        "improve_subtopic_fill.py",
        "improve_crosslink_all.py",
        "improve_source_map.py",
        "improve_duplicate_across.py",
    ],
    "deeptext": [
        # Глубокая обработка текста: структура, поиск, NLP-анализ
        "improve_auto_toc.py",           # оглавление (TOC) в каждый файл
        "improve_abstract.py",           # структурированный абстракт
        "improve_paragraph_quality.py",  # метрики качества абзацев
        "improve_vocabulary_richness.py",# TTR / STTR / lexical density
        "improve_named_entity_index.py", # именованные сущности → JSON
        "improve_timeline_events.py",    # события на шкале времени
        "improve_contradiction_check.py",# поиск противоречивых утверждений
        "improve_concept_graph.py",      # граф концептов → Mermaid + JSON
        "improve_keyword_index.py",      # инвертированный индекс слов
        "improve_passage_retrieval.py",  # BM25-поиск по абзацам
        "improve_chunk_semantic.py",     # семантические чанки для RAG
        "improve_text_segmenter.py",     # разбивка больших файлов на части
    ],
    "nlpplus": [
        # Расширенный NLP-анализ и поиск
        "improve_textrank.py",           # TextRank резюме без LLM → SUMMARIES.md
        "improve_heading_audit.py",      # аудит иерархии заголовков
        "improve_language_split.py",     # RU/EN состав файлов → LANGUAGE_STATS.md
        "improve_question_extractor.py", # вопросы/гипотезы/TODO → QUESTIONS.md
        "improve_passive_voice.py",      # пассивный залог и канцеляризмы
        "improve_empty_sections.py",     # пустые секции-заглушки
        "improve_faceted_search.py",     # фасетный поиск (запускать с --query)
        "improve_similar_passages.py",   # похожие абзацы TF-IDF cosine
        "improve_knowledge_map.py",      # единый дашборд → KNOWLEDGE_MAP.md
        "improve_reading_list.py",       # список чтения по теме → READING_LIST.md
    ],
    "content": [
        # Применение изменений к контенту (запускать осторожно — меняют файлы)
        "improve_auto_toc.py",           # TOC во все файлы (--apply)
        "improve_abstract.py",           # абстракты во все файлы (--apply)
        "improve_auto_linker.py",        # внутренние ссылки (--apply)
        "improve_gap_filler.py",         # заполнить пустые секции (--apply)
    ],
}

# Скрипты, которые можно пропустить при --fast (медленные)
SLOW_SCRIPTS = {
    "improve_clusters.py",       # TF-IDF на 400 файлах
    "improve_similar.py",        # Jaccard попарно
    "improve_export_html.py",    # 3 MB HTML
    "improve_export_json.py",    # 600 KB JSON
    "improve_search_index.py",   # полный индекс
    "improve_word_cloud.py",     # SVG рендеринг
    "improve_digest.py",         # полный обход git
    "improve_link_preview.py",   # HTTP-запросы к внешним URL
    "improve_topic_model.py",    # TF-IDF на всех файлах
    "improve_epub.py",           # pandoc сборка
    "improve_obsidian.py",       # запись множества файлов
    "improve_confluence.py",     # запись множества файлов
    "improve_benchmark.py",      # запуск всех скриптов
    "improve_reclassify.py",     # перемещение файлов
    "improve_merge_by_topic.py", # слияние файлов
    "improve_duplicate_across.py", # попарное сравнение всех файлов
    "improve_compare_docs.py",   # может делать batch
    "improve_external_compare.py", # HTTP-запросы
    "improve_chunk_semantic.py",   # записывает JSONL для всех файлов
    "improve_keyword_index.py",    # строит большой JSON-индекс
    "improve_text_segmenter.py",   # создаёт подпапки с частями
    "improve_passage_retrieval.py",# строит passages.json
    "improve_similar_passages.py", # попарное TF-IDF сравнение абзацев
    "improve_textrank.py",         # TextRank на всех файлах
    "improve_gap_filler.py",       # BM25-поиск + вставка в файлы
    "improve_auto_linker.py",      # вставка ссылок в тексты
    "improve_reading_list.py",     # BM25-поиск по корпусу
    "improve_cross_section.py",    # TF-IDF по всем секциям
}

# Скрипты требующие ANTHROPIC_API_KEY — никогда не запускаются в run_all
LLM_SCRIPTS = {
    "improve_llm_enrich.py",
    "improve_llm_summary.py",
    "improve_llm_qa.py",
    "improve_llm_contact.py",
}

GROUP_ORDER = ["structure", "index", "analysis", "extract",
               "quality", "graph", "generate", "reports", "export",
               "cicd", "analytics", "textwork", "deeptext", "nlpplus", "content"]

# ---------------------------------------------------------------------------
# Stage 2: условное выполнение по результату предыдущих скриптов
# ---------------------------------------------------------------------------

def _parse_score(text: str) -> float | None:
    """Извлекает числовой балл из текста. Поддерживает форматы:
    - **Средний балл:** 65.7/100
    - ## Общий балл: **75/100**
    - ## Итог: **159/164** (96%)
    """
    patterns = [
        r'Средний балл[:\*\s]+\*{0,2}([\d.]+)/100',
        r'Общий балл[:\*\s]+\*{0,2}([\d.]+)/100',
        r'Итог[:\*\s]+\*\*\d+/\d+\*\*\s*\(([\d.]+)%\)',
        r'([\d.]+)/100',
    ]
    for pat in patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def _read_score(condition_file: str) -> float | None:
    path = ROOT / "docs" / condition_file
    if not path.exists():
        return None
    return _parse_score(path.read_text(encoding="utf-8"))


# Условия для скипа: {script: (condition_file, min_score)}
# Скрипт запускается только если текущий балл НИЖЕ min_score.
SMART_CONDITIONS: dict[str, tuple[str, float]] = {
    "improve_qa.py":         ("METRICS.md", 80.0),
    "improve_validate.py":   ("HEALTH.md",  85.0),
    "improve_health.py":     ("HEALTH.md",  90.0),
    "improve_metrics.py":    ("METRICS.md", 85.0),
    "improve_consistency.py":("HEALTH.md",  90.0),
    "improve_report.py":     ("SCORING.md", 95.0),
}


# Маппинг: расширение/папка docs/ → группа скриптов которую нужно запустить
_CHANGED_SECTION_MAP: dict[str, list[str]] = {
    "05-habr-projects": ["structure", "index", "analysis", "extract", "quality", "generate"],
    "04-ai-collaborations": ["structure", "index", "quality", "generate"],
    "01-svyazi": ["structure", "index", "quality"],
    "02-anthropic-vacancies": ["structure", "index"],
    "03-technology-combinations": ["structure", "index"],
    "contacts": ["reports"],
}


def _get_changed_groups() -> list[str]:
    """Возвращает группы скриптов, связанные с git-изменёнными файлами."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=ROOT, capture_output=True, text=True
    )
    changed_files = result.stdout.strip().splitlines()
    # Также staged изменения
    result2 = subprocess.run(
        ["git", "diff", "--name-only", "--cached"],
        cwd=ROOT, capture_output=True, text=True
    )
    changed_files += result2.stdout.strip().splitlines()

    groups_needed: set[str] = set()
    for f in changed_files:
        parts = Path(f).parts
        if len(parts) >= 2 and parts[0] == "docs":
            section = parts[1]
            for mapped_groups in _CHANGED_SECTION_MAP.get(section, []):
                groups_needed.add(mapped_groups)
        elif len(parts) >= 1 and parts[0] == "scripts":
            # Скрипты изменились — запускаем quality и reports
            groups_needed.update(["quality", "reports"])

    # reports всегда нужен если что-то изменилось
    if groups_needed:
        groups_needed.add("reports")

    # Сохраняем оригинальный порядок из GROUP_ORDER
    return [g for g in GROUP_ORDER if g in groups_needed]


def should_skip_smart(script: str, smart: bool) -> tuple[bool, str]:
    """Возвращает (skip, reason). skip=True — пропустить скрипт."""
    if not smart or script not in SMART_CONDITIONS:
        return False, ""
    condition_file, threshold = SMART_CONDITIONS[script]
    score = _read_score(condition_file)
    if score is None:
        return False, ""  # файл не найден — запускаем
    if score >= threshold:
        return True, f"балл {score:.1f} ≥ {threshold} (из {condition_file})"
    return False, f"балл {score:.1f} < {threshold} — запускаем"


def run_script(script: str, dry_run: bool = False) -> tuple[bool, float]:
    path = ROOT / "scripts" / script
    if not path.exists():
        print(f"  ⚠️  {script} — не найден, пропускаем")
        return False, 0.0

    if dry_run:
        print(f"  [dry-run] {script}")
        return True, 0.0

    t0 = time.time()
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT, capture_output=True, text=True
    )
    elapsed = time.time() - t0

    if result.returncode == 0:
        # Последняя строка вывода
        out = result.stdout.strip().splitlines()
        last = out[-1] if out else ""
        print(f"  ✅ {script} ({elapsed:.1f}s) — {last}")
        return True, elapsed
    else:
        err = result.stderr.strip().splitlines()
        last_err = err[-1] if err else "?"
        print(f"  ❌ {script} ({elapsed:.1f}s) — ОШИБКА: {last_err}")
        return False, elapsed


def main():
    args = sys.argv[1:]
    fast     = "--fast"    in args
    dry_run  = "--dry-run" in args
    smart    = "--smart"   in args
    changed  = "--changed" in args
    report   = "--report"  in args
    parallel = 1
    group_filter = None
    only_scripts: list[str] = []

    if "--parallel" in args:
        idx = args.index("--parallel")
        if idx + 1 < len(args):
            try:
                parallel = max(1, int(args[idx + 1]))
            except ValueError:
                parallel = 4

    if "--group" in args:
        idx = args.index("--group")
        if idx + 1 < len(args):
            group_filter = args[idx + 1]

    if "--only" in args:
        idx = args.index("--only")
        if idx + 1 < len(args):
            raw = args[idx + 1].split(",")
            for name in raw:
                name = name.strip()
                if not name.endswith(".py"):
                    name += ".py"
                only_scripts.append(name)

    print("=" * 60)
    print("Lorenzo — запуск всех скриптов обработки")
    if fast:         print("  Режим: FAST (медленные скрипты пропускаются)")
    if dry_run:      print("  Режим: DRY-RUN (реальный запуск отключён)")
    if smart:        print("  Режим: SMART (условный запуск по метрикам)")
    if changed:      print("  Режим: CHANGED (только скрипты для изменённых файлов)")
    if only_scripts: print(f"  Режим: ONLY — {', '.join(only_scripts)}")
    if parallel > 1: print(f"  Режим: PARALLEL — {parallel} потоков")
    if report:       print("  Режим: REPORT (git diff после прогона)")
    if group_filter: print(f"  Группа: {group_filter}")
    print("=" * 60)

    total_ok   = 0
    total_err  = 0
    total_skip = 0
    total_time = 0.0

    # --only: запускаем список скриптов напрямую, без группировки
    if only_scripts:
        print(f"\n{'─'*40}")
        print(f"Запуск: {len(only_scripts)} скриптов")
        print(f"{'─'*40}")
        for script in only_scripts:
            if script in LLM_SCRIPTS:
                print(f"  🤖 {script} — пропущен (требует ANTHROPIC_API_KEY)")
                total_skip += 1
                continue
            ok, elapsed = run_script(script, dry_run)
            if ok:
                total_ok += 1
            else:
                total_err += 1
            total_time += elapsed

        print("\n" + "=" * 60)
        print(f"Итог: ✅ {total_ok} успешно  ❌ {total_err} ошибок  "
              f"⏩ {total_skip} пропущено  ⏱ {total_time:.0f}с")
        print("=" * 60)
        if total_err > 0:
            sys.exit(1)
        return

    if group_filter:
        groups_to_run = [group_filter]
    elif changed:
        groups_to_run = _get_changed_groups()
        if not groups_to_run:
            print("\nℹ️  Нет изменённых файлов — нечего запускать")
            return
        print(f"  Группы для запуска: {', '.join(groups_to_run)}")
    else:
        groups_to_run = GROUP_ORDER

    def _run_group(group: str) -> tuple[int, int, int, float]:
        """Запускает одну группу. Возвращает (ok, err, skip, time)."""
        scripts = GROUPS.get(group, [])
        if not scripts:
            print(f"\n⚠️  Группа '{group}' не найдена")
            return 0, 0, 0, 0.0

        print(f"\n{'─'*40}")
        print(f"Группа: {group.upper()} ({len(scripts)} скриптов)")
        print(f"{'─'*40}")

        g_ok = g_err = g_skip = 0
        g_time = 0.0
        for script in scripts:
            if script in LLM_SCRIPTS:
                print(f"  🤖 {script} — пропущен (требует ANTHROPIC_API_KEY, запускать отдельно)")
                g_skip += 1
                continue
            if fast and script in SLOW_SCRIPTS:
                print(f"  ⏩ {script} — пропущен (slow)")
                g_skip += 1
                continue
            skip, reason = should_skip_smart(script, smart)
            if skip:
                print(f"  ✔️  {script} — пропущен ({reason})")
                g_skip += 1
                continue
            ok, elapsed = run_script(script, dry_run)
            if ok:
                g_ok += 1
            else:
                g_err += 1
            g_time += elapsed
        return g_ok, g_err, g_skip, g_time

    if parallel > 1 and not dry_run:
        with ThreadPoolExecutor(max_workers=parallel) as ex:
            futures = {ex.submit(_run_group, g): g for g in groups_to_run}
            for fut in as_completed(futures):
                ok, err, skip, t = fut.result()
                total_ok += ok; total_err += err
                total_skip += skip; total_time += t
    else:
        for group in groups_to_run:
            ok, err, skip, t = _run_group(group)
            total_ok += ok; total_err += err
            total_skip += skip; total_time += t

    print("\n" + "=" * 60)
    print(f"Итог: ✅ {total_ok} успешно  ❌ {total_err} ошибок  "
          f"⏩ {total_skip} пропущено  ⏱ {total_time:.0f}с")
    print("=" * 60)

    if report and not dry_run:
        print("\n📋 Изменения (git diff --stat):")
        diff = subprocess.run(["git", "diff", "--stat", "HEAD"],
                              cwd=ROOT, capture_output=True, text=True)
        out = diff.stdout.strip()
        print(out if out else "  нет изменений")

    if total_err > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
