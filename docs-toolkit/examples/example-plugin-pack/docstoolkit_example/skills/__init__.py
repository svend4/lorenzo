"""Скилы из примера-плагина."""
from pathlib import Path


def get_path() -> Path:
    """Возвращает директорию со скилами."""
    return Path(__file__).parent
