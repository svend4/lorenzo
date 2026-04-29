"""Часть 1: импорты и утилиты записи файлов."""
import os
import re
import sys
import email
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

def write_doc(path: Path, content: str):
    """Создаёт файл (и папки) и пишет контент."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  wrote: {path.relative_to(ROOT)}")

def clean(text: str) -> str:
    """Убирает cite-теги и лишние пробелы."""
    text = re.sub(r'citeturn\w+', '', text)
    text = re.sub(r'\n{4,}', '\n\n\n', text)
    return text.strip()
