"""Утилиты файловой системы и очистки текста (универсальные)."""
import re
from pathlib import Path


def write_doc(path: Path, content: str) -> None:
    """Создаёт файл (и родительские папки) и пишет контент."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def clean_text(text: str) -> str:
    """Универсальная очистка: убирает лишние пустые строки."""
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def is_template_file(path: Path, templates_dir: Path) -> bool:
    """Файл является самим шаблоном (не документом из шаблона)?"""
    try:
        return path.parent == templates_dir.resolve()
    except Exception:
        return False
