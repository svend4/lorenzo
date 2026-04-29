"""Plugin discovery через Python entry_points.

Третьи стороны могут добавлять расширения, регистрируя entry_points в pyproject:

    [project.entry-points."docstoolkit.skills"]
    my-skill = "my_pkg.skills:my_skill_module"

    [project.entry-points."docstoolkit.templates"]
    my-template = "my_pkg.templates:my_template_module"

    [project.entry-points."docstoolkit.ingest"]
    notion = "my_pkg.ingest.notion:ingest"

    [project.entry-points."docstoolkit.embeddings"]
    openai = "my_pkg.embeddings.openai:OpenAIProvider"

Использование:
    from docstoolkit.plugins import discover, list_plugin_groups

    plugins = discover("docstoolkit.ingest")
    for ep in plugins:
        plugin_fn = ep.load()
        # ...

CLI:
    docstoolkit plugins list
    docstoolkit plugins inspect <group> <name>
"""
import sys
from typing import Any


SUPPORTED_GROUPS = [
    "docstoolkit.skills",
    "docstoolkit.templates",
    "docstoolkit.ingest",
    "docstoolkit.embeddings",
    "docstoolkit.tasks",
    "docstoolkit.commands",
]


def _entry_points(group: str):
    """Кросс-версионный entry_points (3.10+ и 3.12+)."""
    try:
        from importlib.metadata import entry_points
    except ImportError:
        return []
    if sys.version_info >= (3, 10):
        return list(entry_points(group=group))
    eps = entry_points()
    if hasattr(eps, "select"):
        return list(eps.select(group=group))
    return list(eps.get(group, []))


def discover(group: str) -> list:
    """Возвращает все entry_points для группы."""
    if group not in SUPPORTED_GROUPS:
        raise ValueError(f"Неизвестная группа {group}. "
                         f"Доступные: {SUPPORTED_GROUPS}")
    return _entry_points(group)


def load(group: str, name: str) -> Any:
    """Загружает один плагин по имени."""
    for ep in discover(group):
        if ep.name == name:
            return ep.load()
    raise KeyError(f"Плагин {group}/{name} не найден")


def list_plugin_groups() -> dict[str, list[str]]:
    """Возвращает {group: [plugin_names]}."""
    result = {}
    for group in SUPPORTED_GROUPS:
        try:
            eps = discover(group)
            result[group] = [ep.name for ep in eps]
        except Exception:
            result[group] = []
    return result


def inspect_plugin(group: str, name: str) -> dict:
    """Подробная информация о плагине."""
    for ep in discover(group):
        if ep.name == name:
            info = {
                "name": ep.name,
                "group": group,
                "value": ep.value,
                "module": ep.module if hasattr(ep, "module") else "?",
            }
            if hasattr(ep, "dist") and ep.dist:
                info["package"] = ep.dist.name
                info["version"] = ep.dist.version
            try:
                obj = ep.load()
                info["docstring"] = (obj.__doc__ or "").strip()[:300]
                info["callable"] = callable(obj)
            except Exception as e:
                info["load_error"] = str(e)
            return info
    return {"error": f"plugin {group}/{name} not found"}


# ---------------------------------------------------------------------------
# Auto-discovery в core: при импорте подгружаем зарегистрированные плагины
# ---------------------------------------------------------------------------

def autoload_ingest_plugins():
    """При запуске docs-toolkit подключает все ingest-плагины из entry_points."""
    try:
        from docstoolkit.ingest.dispatch import register
    except ImportError:
        return 0
    count = 0
    for ep in discover("docstoolkit.ingest"):
        try:
            fn = ep.load()
            register(ep.name, fn)
            count += 1
        except Exception as e:
            sys.stderr.write(f"⚠️ Ingest plugin {ep.name} ошибка: {e}\n")
    return count


def autoload_embedding_providers():
    """Подключает embedding-провайдеры из entry_points."""
    try:
        from docstoolkit.embeddings.dispatch import register
    except ImportError:
        return 0
    count = 0
    for ep in discover("docstoolkit.embeddings"):
        try:
            cls = ep.load()
            register(ep.name, cls)
            count += 1
        except Exception as e:
            sys.stderr.write(f"⚠️ Embedding plugin {ep.name} ошибка: {e}\n")
    return count


def autoload_all() -> dict:
    """Подключает все плагины из entry_points. Возвращает счётчик."""
    return {
        "ingest": autoload_ingest_plugins(),
        "embeddings": autoload_embedding_providers(),
    }
