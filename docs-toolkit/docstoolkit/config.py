"""Загрузка docstoolkit.toml из текущей директории или родительских."""
from dataclasses import dataclass, field
from pathlib import Path
import tomllib  # Python 3.11+


DEFAULT_CONFIG = {
    "paths": {
        "docs": "docs",
        "templates": "docs/templates",
        "schemas": "docs/templates/_schemas",
        "tasks": "tasks",
        "skills": ".claude/skills",
    },
    "validation": {
        "strict": False,
        "skip_dirs": ["templates", "_schemas", "node_modules", ".git"],
    },
    "language": {
        "primary": "en",
        "fallback": "en",
    },
    "sections": {},
}


@dataclass
class Config:
    root: Path
    paths: dict
    validation: dict
    language: dict
    sections: dict

    @property
    def docs_dir(self) -> Path:
        return self.root / self.paths["docs"]

    @property
    def templates_dir(self) -> Path:
        return self.root / self.paths["templates"]

    @property
    def schemas_dir(self) -> Path:
        return self.root / self.paths["schemas"]


def find_config(start: Path | None = None) -> Path | None:
    """Идёт вверх по дереву ища docstoolkit.toml."""
    cur = (start or Path.cwd()).resolve()
    for parent in [cur, *cur.parents]:
        candidate = parent / "docstoolkit.toml"
        if candidate.exists():
            return candidate
    return None


def deep_merge(base: dict, override: dict) -> dict:
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(start: Path | None = None) -> Config:
    config_path = find_config(start)
    if config_path is None:
        # Используем дефолт + cwd как root
        merged = DEFAULT_CONFIG
        root = (start or Path.cwd()).resolve()
    else:
        with config_path.open("rb") as f:
            user = tomllib.load(f)
        merged = deep_merge(DEFAULT_CONFIG, user)
        root = config_path.parent

    return Config(
        root=root,
        paths=merged["paths"],
        validation=merged["validation"],
        language=merged["language"],
        sections=merged["sections"],
    )
