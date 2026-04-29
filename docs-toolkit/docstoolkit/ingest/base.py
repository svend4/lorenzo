"""Базовые типы для ингестии."""
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


class IngestError(Exception):
    """Ошибка ингестии (плагин не может обработать файл / повреждён / ничего не извлечено)."""


@dataclass
class Source:
    """Происхождение документа."""
    path: Path
    format: str                          # pdf, epub, mhtml, docx, jupyter, html, markdown
    size_bytes: int = 0
    mtime: datetime | None = None

    @classmethod
    def from_path(cls, path: Path, format: str) -> "Source":
        stat = path.stat() if path.exists() else None
        return cls(
            path=path,
            format=format,
            size_bytes=stat.st_size if stat else 0,
            mtime=datetime.fromtimestamp(stat.st_mtime) if stat else None,
        )


@dataclass
class Document:
    """Извлечённый документ."""
    title: str
    content: str                         # markdown
    source: Source
    metadata: dict[str, Any] = field(default_factory=dict)
    sections: list[dict] = field(default_factory=list)  # [{"heading": "...", "level": 2, ...}]

    @property
    def word_count(self) -> int:
        return len(self.content.split())

    @property
    def has_content(self) -> bool:
        return bool(self.content and self.content.strip())

    def to_markdown(self, frontmatter: dict | None = None) -> str:
        """Сериализация в markdown с опциональным frontmatter."""
        parts = []
        if frontmatter:
            parts.append("---")
            for k, v in frontmatter.items():
                parts.append(f"{k}: {_yaml_value(v)}")
            parts.append("---\n")
        if self.title and not self.content.lstrip().startswith("#"):
            parts.append(f"# {self.title}\n")
        parts.append(self.content)
        return "\n".join(parts).strip() + "\n"


def _yaml_value(v):
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(f'"{x}"' if isinstance(x, str) else str(x) for x in v) + "]"
    if isinstance(v, str):
        if any(c in v for c in ': []{}#') or v == "":
            return f'"{v}"'
        return v
    return str(v)
