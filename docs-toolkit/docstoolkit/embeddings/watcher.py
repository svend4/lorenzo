"""Watcher: отслеживание изменений в docs_dir через polling.

Использование:
    from docstoolkit.embeddings.watcher import watch_once, watch_loop
    from docstoolkit.embeddings.incremental import IncrementalIndex

    idx = IncrementalIndex(root)

    # Один скан:
    result = watch_once(docs_dir, idx)
    print(result.changed, result.added, result.deleted)

    # Непрерывный мониторинг:
    def on_change(r: WatchResult):
        print("Изменилось:", r.changed + r.added)

    watch_loop(docs_dir, idx, callback=on_change, interval_sec=30)
"""
import time
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.embeddings.incremental import IncrementalIndex


@dataclass
class WatchResult:
    """Результат одного скана: изменённые, добавленные и удалённые файлы."""
    changed: list[Path] = field(default_factory=list)   # существуют, но mtime/size изменились
    added: list[Path] = field(default_factory=list)      # новые файлы (не были в манифесте)
    deleted: list[Path] = field(default_factory=list)    # удалённые (были в манифесте)

    @property
    def has_changes(self) -> bool:
        return bool(self.changed or self.added or self.deleted)

    @property
    def total(self) -> int:
        return len(self.changed) + len(self.added) + len(self.deleted)


def watch_once(docs_dir: Path, index: IncrementalIndex) -> WatchResult:
    """Одиночный скан: определить что изменилось по сравнению с манифестом.

    Не обновляет манифест — только читает. Caller решает, вызывать ли mark_indexed.
    """
    docs_dir = Path(docs_dir)
    result = WatchResult()

    # Текущие файлы на диске
    current_paths: set[str] = set()
    for path in sorted(docs_dir.rglob("*.md")):
        if not path.is_file():
            continue
        try:
            stat = path.stat()
        except OSError:
            continue
        current_paths.add(str(path))

        row = index.conn.execute(
            "SELECT mtime, size FROM manifest WHERE path = ?",
            (str(path),)
        ).fetchone()

        if row is None:
            result.added.append(path)
        elif row["mtime"] != stat.st_mtime or row["size"] != stat.st_size:
            result.changed.append(path)

    # Файлы в манифесте, которые относятся к docs_dir, но исчезли
    rows = index.conn.execute("SELECT path FROM manifest").fetchall()
    for row in rows:
        p = Path(row["path"])
        try:
            p.relative_to(docs_dir)
        except ValueError:
            continue
        if str(p) not in current_paths:
            result.deleted.append(p)

    return result


def watch_loop(
    docs_dir: Path,
    index: IncrementalIndex,
    callback,
    interval_sec: float = 30,
) -> None:
    """Цикл polling: вызывает callback(WatchResult) когда есть изменения.

    Блокирующий. Для фонового использования запустить в отдельном потоке.
    callback(result: WatchResult) — вызывается только при наличии изменений.
    """
    docs_dir = Path(docs_dir)
    while True:
        result = watch_once(docs_dir, index)
        if result.has_changes:
            callback(result)
        time.sleep(interval_sec)
