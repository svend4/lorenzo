"""Реестр скилов: локальные .claude/skills/ + entry_points плагины."""
from pathlib import Path

from docstoolkit.config import load_config


def discover_skill_dirs() -> list[Path]:
    """Возвращает все директории со скилами (локальная + плагины)."""
    dirs: list[Path] = []
    cfg = load_config()
    local = cfg.root / cfg.paths.get("skills", ".claude/skills")
    if local.exists():
        dirs.append(local)

    # Из entry_points
    try:
        from docstoolkit.plugins import discover
        for ep in discover("docstoolkit.skills"):
            try:
                fn_or_path = ep.load()
                if callable(fn_or_path):
                    p = Path(fn_or_path())
                else:
                    p = Path(fn_or_path)
                if p.exists() and p.is_dir():
                    dirs.append(p)
            except Exception:
                continue
    except Exception:
        pass
    return dirs


def list_skills() -> dict[str, Path]:
    """Возвращает {skill_name: path_to_md} от всех источников."""
    result: dict[str, Path] = {}
    for d in discover_skill_dirs():
        for f in d.glob("*.md"):
            if f.name == "README.md":
                continue
            result[f.stem] = f
    return result


def get_skill_path(name: str) -> Path | None:
    return list_skills().get(name)
