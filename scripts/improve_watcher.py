"""
improve_watcher.py — автономный агент-наблюдатель (Ступень 6).
Следит за изменениями в docs/ и автоматически запускает нужные скрипты.
Запуск: python scripts/improve_watcher.py
        python scripts/improve_watcher.py --once   (однократная проверка)
Зависимости: pip install watchdog   (опционально — без него работает polling)
"""
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

# Правила: паттерн файла → скрипты для запуска
RULES = [
    # Любой .md изменился → обновить индексы
    (lambda p: p.suffix == ".md",           ["improve_index_update.py", "improve_backlinks.py"]),
    # Изменился файл в 01-svyazi/ → обновить summary и stats
    (lambda p: "01-svyazi" in str(p),       ["improve_summaries.py", "improve_stats.py"]),
    # Изменился CONTACTS.md → обновить entities
    (lambda p: p.name == "CONTACTS.md",     ["improve_entities.py"]),
    # Изменился любой README → обновить sitemap
    (lambda p: p.name == "README.md",       ["improve_sitemap.py"]),
    # Изменился скрипт → обновить отчёт
    (lambda p: "scripts" in str(p) and p.suffix == ".py", ["improve_report.py"]),
]

# Скрипты которые запускаем не чаще раза в N секунд
COOLDOWN = 30   # секунд
_last_run: dict[str, float] = {}


def should_run(script: str) -> bool:
    last = _last_run.get(script, 0)
    return (time.time() - last) > COOLDOWN


def run_script(script: str) -> None:
    if not should_run(script):
        return
    path = ROOT / "scripts" / script
    if not path.exists():
        return
    _last_run[script] = time.time()
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] → {script}", flush=True)
    try:
        subprocess.run(
            [sys.executable, str(path)],
            cwd=ROOT, capture_output=True, text=True, timeout=60
        )
    except subprocess.TimeoutExpired:
        print(f"  [{ts}] timeout: {script}", flush=True)
    except Exception as e:
        print(f"  [{ts}] error {script}: {e}", flush=True)


def handle_change(changed_path: Path) -> None:
    triggered: list[str] = []
    for match_fn, scripts in RULES:
        try:
            if match_fn(changed_path):
                triggered.extend(scripts)
        except Exception:
            pass
    for script in dict.fromkeys(triggered):   # dedupe, preserve order
        run_script(script)


def watch_polling(interval: float = 3.0) -> None:
    """Polling-based watcher (без watchdog)."""
    print(f"  polling каждые {interval}s (Ctrl+C для остановки)")
    mtimes: dict[Path, float] = {}

    # Инициализация
    for f in DOCS.rglob("*"):
        if f.is_file():
            try:
                mtimes[f] = f.stat().st_mtime
            except OSError:
                pass

    while True:
        time.sleep(interval)
        changed: list[Path] = []
        current = set(DOCS.rglob("*"))

        for f in current:
            if not f.is_file():
                continue
            try:
                mtime = f.stat().st_mtime
            except OSError:
                continue
            if f not in mtimes or mtimes[f] != mtime:
                mtimes[f] = mtime
                changed.append(f)

        for f in changed:
            ts = datetime.now().strftime("%H:%M:%S")
            print(f"[{ts}] изменён: {f.relative_to(ROOT)}", flush=True)
            handle_change(f)


def watch_watchdog() -> None:
    """Watchdog-based watcher (если установлен)."""
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler

    class Handler(FileSystemEventHandler):
        def on_modified(self, event):
            if not event.is_directory:
                handle_change(Path(event.src_path))
        def on_created(self, event):
            if not event.is_directory:
                handle_change(Path(event.src_path))

    observer = Observer()
    observer.schedule(Handler(), str(DOCS), recursive=True)
    observer.schedule(Handler(), str(ROOT / "scripts"), recursive=False)
    observer.start()
    print(f"  watchdog активен (Ctrl+C для остановки)")
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()


def run_once() -> None:
    """Однократная проверка: запустить базовые скрипты."""
    print("  однократный запуск базовых скриптов...")
    for script in ["improve_index_update.py", "improve_stats.py", "improve_report.py"]:
        run_script(script)
    print("  готово")


def main():
    args = sys.argv[1:]
    print(f"Автономный вотчер Lorenzo / Svyazi 2.0")
    print(f"  docs: {DOCS.relative_to(ROOT)}")

    if "--once" in args:
        run_once()
        return

    try:
        import watchdog  # noqa
        watch_watchdog()
    except ImportError:
        print("  watchdog не установлен → polling mode")
        print("  (для быстрого режима: pip install watchdog)")
        watch_polling()


if __name__ == "__main__":
    main()
