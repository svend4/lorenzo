"""
improve_run_all.py — мастер-скрипт для запуска всех improve_*.py.
Запускает скрипты в правильном порядке (зависимости учтены).
Поддерживает: --fast (только быстрые), --group <name>, --dry-run, --smart.

  --smart     Условный запуск: пропускает скрипты если метрика уже выше порога.
              Читает docs/METRICS.md, docs/HEALTH.md, docs/SCORING.md.

Запуск: python scripts/improve_run_all.py
        python scripts/improve_run_all.py --fast
        python scripts/improve_run_all.py --group analysis
        python scripts/improve_run_all.py --smart
"""
import re
import subprocess
import sys
import time
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
    "export": [
        # Экспорт
        "improve_export_csv.py",
        "improve_export_json.py",
        "improve_export_html.py",
    ],
}

# Скрипты, которые можно пропустить при --fast (медленные)
SLOW_SCRIPTS = {
    "improve_clusters.py",       # TF-IDF на 400 файлах
    "improve_similar.py",        # Jaccard попарно
    "improve_export_html.py",    # 3 MB HTML
    "improve_export_json.py",    # 600 KB JSON
    "improve_search_index.py",   # полный индекс
}

GROUP_ORDER = ["structure", "index", "analysis", "extract",
               "quality", "graph", "reports", "export"]

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
    group_filter = None
    if "--group" in args:
        idx = args.index("--group")
        if idx + 1 < len(args):
            group_filter = args[idx + 1]

    print("=" * 60)
    print("Lorenzo — запуск всех скриптов обработки")
    if fast:    print("  Режим: FAST (медленные скрипты пропускаются)")
    if dry_run: print("  Режим: DRY-RUN (реальный запуск отключён)")
    if smart:   print("  Режим: SMART (условный запуск по метрикам)")
    if group_filter: print(f"  Группа: {group_filter}")
    print("=" * 60)

    total_ok   = 0
    total_err  = 0
    total_skip = 0
    total_time = 0.0

    groups_to_run = [group_filter] if group_filter else GROUP_ORDER
    for group in groups_to_run:
        scripts = GROUPS.get(group, [])
        if not scripts:
            print(f"\n⚠️  Группа '{group}' не найдена")
            continue

        print(f"\n{'─'*40}")
        print(f"Группа: {group.upper()} ({len(scripts)} скриптов)")
        print(f"{'─'*40}")

        for script in scripts:
            if fast and script in SLOW_SCRIPTS:
                print(f"  ⏩ {script} — пропущен (slow)")
                total_skip += 1
                continue

            skip, reason = should_skip_smart(script, smart)
            if skip:
                print(f"  ✔️  {script} — пропущен ({reason})")
                total_skip += 1
                continue

            ok, elapsed = run_script(script, dry_run)
            if ok:
                total_ok  += 1
            else:
                total_err += 1
            total_time += elapsed

    print("\n" + "=" * 60)
    print(f"Итог: ✅ {total_ok} успешно  ❌ {total_err} ошибок  "
          f"⏩ {total_skip} пропущено  ⏱ {total_time:.0f}с")
    print("=" * 60)

    if total_err > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
