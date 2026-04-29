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
  graph → generate → reports → export →
  cicd → analytics → textwork → deeptext
  (enrich и meta — только вручную, требуют/опциональны API)

Запуск: python scripts/improve_run_all.py
        python scripts/improve_run_all.py --fast --smart
        python scripts/improve_run_all.py --group generate
        python scripts/improve_run_all.py --group enrich
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
        "improve_merge_short.py",
        "improve_readmes.py",
        "improve_summaries.py",
        "improve_tags.py",
        "improve_toc.py",
        "improve_autocorrect.py",
    ],
    "index": [
        "improve_glossary.py",
        "improve_crossrefs.py",
        "improve_search_index.py",
        "improve_index_update.py",
        "improve_timeline.py",
        "improve_backlinks.py",
    ],
    "analysis": [
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
        "improve_graph.py",
        "improve_mindmap.py",
        "improve_network.py",
        "improve_narrative.py",
        "improve_word_cloud.py",
        "improve_templates.py",
    ],
    "generate": [
        # Генерация файлов из шаблонов и данных (после extract/analysis)
        "improve_autofill.py",
        "improve_footnotes.py",
        "improve_see_also.py",
        "improve_faq.py",
        "improve_badges.py",
    ],
    "reports": [
        # Отчёты (запускать после generate)
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
        "improve_export_csv.py",
        "improve_export_json.py",
        "improve_export_html.py",
        "improve_obsidian.py",
        "improve_rss.py",
        "improve_confluence.py",
    ],
    "cicd": [
        "improve_github_issues.py",
        "improve_ci_config.py",
        "improve_pre_commit.py",
        "improve_dependabot.py",
    ],
    "analytics": [
        "improve_citation_index.py",
        "improve_reading_time.py",
        "improve_version_diff.py",
        "improve_topic_model.py",
    ],
    "textwork": [
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
        "improve_auto_toc.py",
        "improve_abstract.py",
        "improve_paragraph_quality.py",
        "improve_vocabulary_richness.py",
        "improve_named_entity_index.py",
        "improve_timeline_events.py",
        "improve_contradiction_check.py",
        "improve_concept_graph.py",
        "improve_keyword_index.py",
        "improve_passage_retrieval.py",
        "improve_chunk_semantic.py",
        "improve_text_segmenter.py",
    ],
    # ── Ступень 2-3: автозаполнение + LLM (запускать отдельно) ──────────────
    "enrich": [
        "improve_llm_summary.py",     # каскадная суммаризация разделов
        "improve_llm_enrich.py",      # обогащение проектных файлов (--dry-run сначала)
        "improve_llm_qa.py",          # Q&A по базе знаний
        "improve_llm_gaps.py",        # семантические пробелы
    ],
    # ── Мета: документы о самом репозитории ─────────────────────────────────
    "meta": [
        "improve_tech_radar.py",
        "improve_onboarding.py",
        "improve_dependency_map.py",
        "improve_digest_weekly.py",
        "improve_risk_register.py",
        "improve_changelog_auto.py",
        "improve_index_master.py",
        "improve_component_matrix.py",
        "improve_kpi_snapshot.py",
    ],
}

# Скрипты, которые можно пропустить при --fast (медленные)
SLOW_SCRIPTS = {
    "improve_clusters.py",
    "improve_similar.py",
    "improve_export_html.py",
    "improve_export_json.py",
    "improve_search_index.py",
    "improve_word_cloud.py",
    "improve_digest.py",
    "improve_link_preview.py",
    "improve_topic_model.py",
    "improve_epub.py",
    "improve_obsidian.py",
    "improve_confluence.py",
    "improve_benchmark.py",
    "improve_reclassify.py",
    "improve_merge_by_topic.py",
    "improve_duplicate_across.py",
    "improve_compare_docs.py",
    "improve_external_compare.py",
    "improve_chunk_semantic.py",
    "improve_keyword_index.py",
    "improve_text_segmenter.py",
    "improve_passage_retrieval.py",
}

# LLM-скрипты — никогда не запускаются в автоматическом run_all,
# только через --group enrich или напрямую. Требуют ANTHROPIC_API_KEY.
LLM_SCRIPTS = {
    "improve_llm_enrich.py",
    "improve_llm_summary.py",
    "improve_llm_qa.py",
    "improve_llm_gaps.py",
    "improve_llm_contact.py",
}

GROUP_ORDER = [
    "structure", "index", "analysis", "extract",
    "quality", "graph", "generate", "reports", "export",
    "cicd", "analytics", "textwork", "deeptext",
]
# "enrich" и "meta" намеренно не в GROUP_ORDER — запускаются через --group

# ---------------------------------------------------------------------------
# Stage 2: условное выполнение по результату предыдущих скриптов (--smart)
# ---------------------------------------------------------------------------

def _parse_score(text: str) -> float | None:
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


SMART_CONDITIONS: dict[str, tuple[str, float]] = {
    "improve_qa.py":         ("METRICS.md", 80.0),
    "improve_validate.py":   ("HEALTH.md",  85.0),
    "improve_health.py":     ("HEALTH.md",  90.0),
    "improve_metrics.py":    ("METRICS.md", 85.0),
    "improve_consistency.py":("HEALTH.md",  90.0),
    "improve_report.py":     ("SCORING.md", 95.0),
}

_CHANGED_SECTION_MAP: dict[str, list[str]] = {
    "05-habr-projects":         ["structure", "index", "analysis", "extract", "quality", "generate"],
    "04-ai-collaborations":     ["structure", "index", "quality", "generate"],
    "01-svyazi":                ["structure", "index", "quality"],
    "02-anthropic-vacancies":   ["structure", "index"],
    "03-technology-combinations": ["structure", "index"],
    "contacts":                 ["reports"],
}


def _get_changed_groups() -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "HEAD"],
        cwd=ROOT, capture_output=True, text=True
    )
    changed_files = result.stdout.strip().splitlines()
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
            for mapped_group in _CHANGED_SECTION_MAP.get(section, []):
                groups_needed.add(mapped_group)
        elif len(parts) >= 1 and parts[0] == "scripts":
            groups_needed.update(["quality", "reports"])

    if groups_needed:
        groups_needed.add("reports")
    return [g for g in GROUP_ORDER if g in groups_needed]


def should_skip_smart(script: str, smart: bool) -> tuple[bool, str]:
    if not smart or script not in SMART_CONDITIONS:
        return False, ""
    condition_file, threshold = SMART_CONDITIONS[script]
    score = _read_score(condition_file)
    if score is None:
        return False, ""
    if score >= threshold:
        return True, f"балл {score:.1f} ≥ {threshold} (из {condition_file})"
    return False, f"балл {score:.1f} < {threshold} — запускаем"


# ---------------------------------------------------------------------------
# Запуск одного скрипта
# ---------------------------------------------------------------------------

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
        out = result.stdout.strip().splitlines()
        last = out[-1] if out else ""
        print(f"  ✅ {script} ({elapsed:.1f}s) — {last}")
        return True, elapsed
    else:
        err = result.stderr.strip().splitlines()
        last_err = err[-1] if err else "?"
        print(f"  ❌ {script} ({elapsed:.1f}s) — ОШИБКА: {last_err}")
        return False, elapsed


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

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

    total_ok = total_err = total_skip = 0
    total_time = 0.0

    # --only: запускаем список скриптов напрямую
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
            if ok: total_ok += 1
            else:  total_err += 1
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
                print(f"  🤖 {script} — пропущен (запускать: python scripts/{script})")
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
            if ok: g_ok += 1
            else:  g_err += 1
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
