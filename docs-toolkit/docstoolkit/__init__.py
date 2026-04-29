"""docs-toolkit — универсальный набор инструментов для markdown-документации."""
__version__ = "0.1.0"

from docstoolkit.config import Config, load_config
from docstoolkit.core import write_doc, clean_text
from docstoolkit.frontmatter import extract_frontmatter, parse_yaml

__all__ = [
    "Config", "load_config",
    "write_doc", "clean_text",
    "extract_frontmatter", "parse_yaml",
]

# Авто-подгрузка плагинов при импорте (тихо, не падает если что-то не так)
try:
    from docstoolkit.plugins import autoload_all
    autoload_all()
except Exception:
    pass
