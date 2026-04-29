"""Регистр плагинов и диспетчеризация по расширению."""
from pathlib import Path
from typing import Callable

from docstoolkit.ingest.base import Document, IngestError, Source


_REGISTRY: dict[str, Callable[[Path], Document]] = {}


def register(extension: str, fn: Callable[[Path], Document]) -> None:
    """Регистрация плагина для расширения (без точки)."""
    _REGISTRY[extension.lower().lstrip(".")] = fn


def get_plugin(extension: str) -> Callable[[Path], Document] | None:
    return _REGISTRY.get(extension.lower().lstrip("."))


def list_plugins() -> dict[str, Callable]:
    return dict(_REGISTRY)


def ingest_file(path: str | Path) -> Document:
    """Главная точка входа: ингестия одного файла."""
    p = Path(path)
    if not p.exists():
        raise IngestError(f"Файл не найден: {p}")
    ext = p.suffix.lower().lstrip(".")
    plugin = get_plugin(ext)
    if not plugin:
        raise IngestError(f"Нет плагина для .{ext}. Доступные: {sorted(_REGISTRY)}")
    return plugin(p)


def ingest_dir(path: str | Path, *, recursive: bool = True) -> list[Document]:
    """Ингестия всех поддерживаемых файлов в директории."""
    p = Path(path)
    if not p.is_dir():
        raise IngestError(f"Не директория: {p}")
    pattern = "**/*" if recursive else "*"
    docs: list[Document] = []
    for f in p.glob(pattern):
        if not f.is_file():
            continue
        ext = f.suffix.lower().lstrip(".")
        if ext not in _REGISTRY:
            continue
        try:
            docs.append(ingest_file(f))
        except IngestError as e:
            print(f"⚠️ skip {f}: {e}")
    return docs


# Авто-регистрация всех плагинов при импорте dispatch
def _autoload():
    from docstoolkit.ingest import (
        markdown as _md,
        html as _html,
        mhtml as _mhtml,
        jupyter as _jp,
    )
    # plugins регистрируются через декоратор @register или вручную в каждом
    register("md", _md.ingest)
    register("markdown", _md.ingest)
    register("html", _html.ingest)
    register("htm", _html.ingest)
    register("mhtml", _mhtml.ingest)
    register("ipynb", _jp.ingest)
    # Опциональные (нужны зависимости)
    try:
        from docstoolkit.ingest import pdf as _pdf
        register("pdf", _pdf.ingest)
    except ImportError:
        pass
    try:
        from docstoolkit.ingest import epub as _epub
        register("epub", _epub.ingest)
    except ImportError:
        pass
    try:
        from docstoolkit.ingest import docx as _docx
        register("docx", _docx.ingest)
    except ImportError:
        pass


_autoload()
