"""
improve_watch.py — следит за изменениями в docs/ и перезапускает нужные скрипты.
Использует polling (без внешних зависимостей).

Запуск:
    python scripts/improve_watch.py            # следит за docs/, запускает --changed
    python scripts/improve_watch.py --group structure  # только одна группа
    python scripts/improve_watch.py --interval 5       # интервал проверки (сек, по умолчанию 3)
    python scripts/improve_watch.py --fast             # пропускать медленные скрипты
    Ctrl+C для остановки.
"""
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRIPTS_DIR = ROOT / "scripts"

INTERVAL = 3
for arg in sys.argv:
    if arg.startswith("--interval="):
        INTERVAL = int(arg.split("=", 1)[1])
if "--interval" in sys.argv:
    idx = sys.argv.index("--interval")
    if idx + 1 < len(sys.argv):
        INTERVAL = int(sys.argv[idx + 1])

GROUP_FILTER = None
if "--group" in sys.argv:
    idx = sys.argv.index("--group")
    if idx + 1 < len(sys.argv):
        GROUP_FILTER = sys.argv[idx + 1]

FAST = "--fast" in sys.argv


def _snapshot(directory: Path) -> dict[Path, float]:
    """Возвращает словарь {путь: mtime} для всех .md файлов в директории."""
    result = {}
    for f in directory.rglob("*.md"):
        try:
            result[f] = f.stat().st_mtime
        except FileNotFoundError:
            pass
    return result


def _changed_files(old: dict, new: dict) -> list[Path]:
    changed = []
    for path, mtime in new.items():
        if path not in old or old[path] != mtime:
            changed.append(path)
    for path in old:
        if path not in new:
            changed.append(path)
    return changed


def _run_scripts(changed: list[Path]) -> None:
    print(f"\n🔄 Изменено {len(changed)} файл(ов):")
    for f in changed[:5]:
        print(f"   - {f.relative_to(ROOT)}")
    if len(changed) > 5:
        print(f"   ...и ещё {len(changed)-5}")

    cmd = [sys.executable, str(SCRIPTS_DIR / "improve_run_all.py")]
    if GROUP_FILTER:
        cmd += ["--group", GROUP_FILTER]
    else:
        cmd.append("--changed")
    if FAST:
        cmd.append("--fast")
    cmd.append("--report")

    print(f"\n▶ {' '.join(cmd[1:])}")
    t0 = time.time()
    result = subprocess.run(cmd, cwd=ROOT)
    elapsed = time.time() - t0
    status = "✅" if result.returncode == 0 else "❌"
    print(f"{status} Готово за {elapsed:.1f}с. Жду изменений...\n")


def main() -> None:
    print("👁  improve_watch.py — слежение за docs/")
    print(f"   Интервал: {INTERVAL}с")
    print(f"   Группа: {GROUP_FILTER or 'auto (--changed)'}")
    print(f"   Fast: {FAST}")
    print("   Ctrl+C для остановки\n")

    snapshot = _snapshot(DOCS)
    print(f"   Файлов в наблюдении: {len(snapshot)}")
    print("   Жду изменений...\n")

    try:
        while True:
            time.sleep(INTERVAL)
            new_snapshot = _snapshot(DOCS)
            changed = _changed_files(snapshot, new_snapshot)
            if changed:
                snapshot = new_snapshot
                _run_scripts(changed)
            else:
                snapshot = new_snapshot
    except KeyboardInterrupt:
        print("\n👋 Остановлено.")


if __name__ == "__main__":
    main()
