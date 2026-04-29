"""Ингестия документов из разных форматов в markdown.

Базовый протокол:
  - Каждый плагин экспортирует функцию `ingest(path: Path) -> Document`
  - Document — dataclass с полями: title, content, metadata, source

Регистр плагинов: REGISTRY автоматически выбирает по расширению.
Поддержать новый формат: добавить файл и зарегистрировать в _registry.py.
"""
from docstoolkit.ingest.base import Document, Source, IngestError
from docstoolkit.ingest.dispatch import ingest_file, ingest_dir, get_plugin, list_plugins

__all__ = [
    "Document", "Source", "IngestError",
    "ingest_file", "ingest_dir", "get_plugin", "list_plugins",
]
