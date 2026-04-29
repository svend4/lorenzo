"""Шаблоны из примера-плагина."""
from pathlib import Path


def get_paths() -> dict:
    """Возвращает {template_name: {md_path, schema_path}}."""
    base = Path(__file__).parent
    return {
        "api-spec": {
            "md": base / "api-spec.md",
            "schema": base / "api-spec.json",
        }
    }
