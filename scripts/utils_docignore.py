"""
utils_docignore.py — загрузка .docignore и проверка пути на исключение.

Аналог .gitignore для скриптов improve_*.py которые модифицируют контент.

Использование:
    from utils_docignore import is_ignored, load_patterns

    if is_ignored(path):
        continue  # скрипт не должен трогать этот файл

Поддерживаемые паттерны:
    - Точные пути: docs/REPORT.md
    - Glob: docs/badges/*.svg
    - Рекурсивный glob: **/README.md
    - Папки (заканчивается на /): docs/templates/_schemas/
    - Комментарии: # ...
    - Пустые строки игнорируются
"""
import fnmatch
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCIGNORE = ROOT / ".docignore"


@lru_cache(maxsize=1)
def load_patterns() -> list[str]:
    """Возвращает список паттернов из .docignore (с кэшем)."""
    if not DOCIGNORE.exists():
        return []
    patterns: list[str] = []
    for raw in DOCIGNORE.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        patterns.append(line)
    return patterns


def is_ignored(path: str | Path, root: Path | None = None) -> bool:
    """Проверяет, попадает ли путь под .docignore.

    Args:
        path: проверяемый путь (абсолютный или относительный)
        root: корень репо (по умолчанию ROOT)
    """
    root = root or ROOT
    p = Path(path)
    try:
        if p.is_absolute():
            rel = p.relative_to(root)
        else:
            rel = p
    except ValueError:
        return False

    rel_str = str(rel).replace("\\", "/")
    patterns = load_patterns()

    for pat in patterns:
        # Папка (с trailing /)
        if pat.endswith("/"):
            prefix = pat.rstrip("/")
            if rel_str == prefix or rel_str.startswith(prefix + "/"):
                return True
        # Рекурсивный glob с **
        elif "**" in pat:
            # **/README.md → match если путь заканчивается на README.md
            tail = pat.replace("**/", "")
            if fnmatch.fnmatch(rel.name, tail):
                return True
            if fnmatch.fnmatch(rel_str, pat.replace("**/", "*/")):
                return True
        # Обычный glob
        elif "*" in pat or "?" in pat:
            if fnmatch.fnmatch(rel_str, pat):
                return True
        # Точный путь
        else:
            if rel_str == pat:
                return True
    return False


def filter_paths(paths) -> list[Path]:
    """Фильтрует список путей, оставляя только не-игнорируемые."""
    return [Path(p) for p in paths if not is_ignored(p)]


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python utils_docignore.py <path1> [<path2> ...]")
        print(f"Загружено паттернов: {len(load_patterns())}")
        for p in load_patterns():
            print(f"  {p}")
        sys.exit(0)
    for p in sys.argv[1:]:
        result = "IGNORED" if is_ignored(p) else "ok"
        print(f"  [{result}] {p}")
