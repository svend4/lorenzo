"""
improve_benchmark.py — замеряет и записывает время выполнения скриптов.
Хранит историю в docs/benchmark.json, показывает тренды.

Запуск:
    python scripts/improve_benchmark.py                     # запустить все и записать
    python scripts/improve_benchmark.py --group quality     # только одна группа
    python scripts/improve_benchmark.py --report            # только показать историю
    python scripts/improve_benchmark.py --script improve_metrics.py  # один скрипт
"""
import json
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"
BENCH_FILE = DOCS / "benchmark.json"
TODAY = date.today().isoformat()

REPORT_ONLY = "--report" in sys.argv

GROUP_FILTER = None
if "--group" in sys.argv:
    idx = sys.argv.index("--group")
    if idx + 1 < len(sys.argv):
        GROUP_FILTER = sys.argv[idx + 1]

SCRIPT_FILTER = None
if "--script" in sys.argv:
    idx = sys.argv.index("--script")
    if idx + 1 < len(sys.argv):
        SCRIPT_FILTER = sys.argv[idx + 1]


def load_history() -> dict:
    if BENCH_FILE.exists():
        try:
            return json.loads(BENCH_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"runs": [], "scripts": {}}


def save_history(data: dict) -> None:
    BENCH_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _time_script(script: str) -> float | None:
    path = SCRIPTS_DIR / script
    if not path.exists():
        return None
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, str(path)],
        cwd=ROOT, capture_output=True, text=True, timeout=120
    )
    elapsed = time.time() - t0
    if result.returncode != 0:
        return None
    return round(elapsed, 2)


def _get_scripts_to_bench() -> list[str]:
    if SCRIPT_FILTER:
        s = SCRIPT_FILTER if SCRIPT_FILTER.endswith(".py") else SCRIPT_FILTER + ".py"
        return [s]

    # Импортируем группы из run_all
    sys.path.insert(0, str(ROOT / "scripts"))
    try:
        from improve_run_all import GROUPS, GROUP_ORDER, LLM_SCRIPTS, SLOW_SCRIPTS
    except ImportError:
        return []

    if GROUP_FILTER:
        scripts = GROUPS.get(GROUP_FILTER, [])
    else:
        # Быстрые скрипты из всех групп (исключаем slow и LLM)
        scripts = []
        for g in GROUP_ORDER:
            for s in GROUPS.get(g, []):
                if s not in LLM_SCRIPTS and s not in SLOW_SCRIPTS:
                    scripts.append(s)

    return [s for s in scripts if (SCRIPTS_DIR / s).exists()]


def _trend(times: list[float]) -> str:
    if len(times) < 2:
        return "—"
    delta = times[-1] - times[-2]
    if abs(delta) < 0.1:
        return "→ стабильно"
    return f"{'↑ медленнее' if delta > 0 else '↓ быстрее'} на {abs(delta):.1f}с"


def print_report(data: dict) -> None:
    scripts = data.get("scripts", {})
    if not scripts:
        print("  Нет данных — запустите без --report сначала")
        return

    print(f"\n{'Скрипт':<35} {'Последний':<10} {'Среднее':<10} {'Тренд'}")
    print("-" * 75)
    for script, times in sorted(scripts.items(), key=lambda x: -(x[1][-1] if x[1] else 0)):
        if not times:
            continue
        last = times[-1]
        avg = sum(times) / len(times)
        trend = _trend(times)
        icon = "🟢" if last < 5 else ("🟡" if last < 15 else "🔴")
        print(f"{icon} {script:<33} {last:<10.1f} {avg:<10.1f} {trend}")

    runs = data.get("runs", [])
    if runs:
        print(f"\n  Прогонов: {len(runs)}, последний: {runs[-1]['date']}")


def main() -> None:
    print("⏱  improve_benchmark.py — замер времени выполнения скриптов")

    data = load_history()

    if REPORT_ONLY:
        print_report(data)
        return

    scripts = _get_scripts_to_bench()
    if not scripts:
        print("❌ Нет скриптов для замера")
        sys.exit(1)

    print(f"   Скриптов для замера: {len(scripts)}")
    print(f"   Группа: {GROUP_FILTER or 'все быстрые'}\n")

    run_results: dict[str, float] = {}
    for script in scripts:
        print(f"  ▶ {script}...", end=" ", flush=True)
        elapsed = _time_script(script)
        if elapsed is None:
            print("❌ ошибка")
            continue
        run_results[script] = elapsed
        icon = "🟢" if elapsed < 5 else ("🟡" if elapsed < 15 else "🔴")
        print(f"{icon} {elapsed:.1f}с")

        # Записываем в историю
        if script not in data["scripts"]:
            data["scripts"][script] = []
        data["scripts"][script].append(elapsed)
        # Храним последние 20 замеров
        data["scripts"][script] = data["scripts"][script][-20:]

    # Запись прогона
    data["runs"].append({
        "date": TODAY,
        "timestamp": datetime.now().isoformat(),
        "scripts": run_results,
        "total": round(sum(run_results.values()), 1),
    })
    data["runs"] = data["runs"][-50:]  # последние 50 прогонов

    save_history(data)
    print(f"\n  Итого: {sum(run_results.values()):.1f}с для {len(run_results)} скриптов")
    print(f"  История: {BENCH_FILE.relative_to(ROOT)}")

    print("\n  Топ самых медленных:")
    for script, t in sorted(run_results.items(), key=lambda x: -x[1])[:5]:
        trend = _trend(data["scripts"].get(script, [t]))
        print(f"    {t:.1f}с  {script}  {trend}")


if __name__ == "__main__":
    main()
