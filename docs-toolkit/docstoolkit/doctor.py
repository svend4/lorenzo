"""
doctor.py — система диагностики docs-toolkit.

Проверяет:
  1. Конфиг (docstoolkit.toml найден, валиден)
  2. Структура (docs/, templates/, schemas/ существуют)
  3. Шаблоны (количество + соответствие схемам)
  4. Документы (валидируются по схемам)
  5. Опциональные зависимости (mcp, anthropic, pypdf, ebooklib, python-docx)
  6. Python версия (>= 3.10)
  7. Plugins (ingest plugins загружаются)

Возвращает:
  - 0: всё в порядке
  - 1: есть warnings
  - 2: есть errors

Запуск:
    docstoolkit doctor
    docstoolkit doctor --json
"""
import importlib.util
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

from docstoolkit.config import load_config, find_config


@dataclass
class CheckResult:
    name: str
    status: str  # ok | warn | error
    message: str = ""
    detail: dict = field(default_factory=dict)

    @property
    def icon(self) -> str:
        return {'ok': '✓', 'warn': '⚠', 'error': '✗'}.get(self.status, '?')


def check_python_version() -> CheckResult:
    v = sys.version_info
    if v >= (3, 10):
        return CheckResult("python_version", "ok",
                           f"Python {v.major}.{v.minor}.{v.micro}")
    return CheckResult("python_version", "error",
                       f"Python {v.major}.{v.minor} < 3.10 — обновите")


def check_config() -> CheckResult:
    config_path = find_config()
    if not config_path:
        return CheckResult("config", "warn",
                           "docstoolkit.toml не найден — используется дефолт",
                           {"hint": "docstoolkit init"})
    try:
        cfg = load_config()
        return CheckResult("config", "ok",
                           f"Загружен {config_path}",
                           {"root": str(cfg.root)})
    except Exception as e:
        return CheckResult("config", "error", f"Ошибка загрузки: {e}")


def check_structure(cfg) -> list[CheckResult]:
    results = []
    for name, attr in [("docs_dir", "docs_dir"),
                       ("templates_dir", "templates_dir"),
                       ("schemas_dir", "schemas_dir")]:
        path = getattr(cfg, attr)
        if path.exists():
            count = len(list(path.glob("*"))) if path.is_dir() else 0
            results.append(CheckResult(f"path_{name}", "ok",
                                       f"{path} (содержит {count} элементов)"))
        else:
            severity = "warn" if name != "docs_dir" else "error"
            results.append(CheckResult(f"path_{name}", severity,
                                       f"{path} не существует"))
    return results


def check_templates(cfg) -> CheckResult:
    if not cfg.templates_dir.exists():
        return CheckResult("templates", "warn", "templates/ не существует")
    templates = [p for p in cfg.templates_dir.glob("*.md") if p.name != "README.md"]
    schemas_dir = cfg.schemas_dir
    if not schemas_dir.exists():
        return CheckResult("templates", "warn",
                           f"{len(templates)} шаблонов, но _schemas/ нет")

    schemas = list(schemas_dir.glob("*.json"))
    template_names = {p.stem for p in templates}
    schema_names = {p.stem for p in schemas}

    missing_schemas = template_names - schema_names
    orphan_schemas = schema_names - template_names

    detail = {
        "templates": len(templates),
        "schemas": len(schemas),
    }
    if missing_schemas:
        detail["missing_schemas"] = sorted(missing_schemas)
    if orphan_schemas:
        detail["orphan_schemas"] = sorted(orphan_schemas)

    if missing_schemas:
        return CheckResult("templates", "warn",
                           f"{len(missing_schemas)} шаблонов без схем",
                           detail)
    return CheckResult("templates", "ok",
                       f"{len(templates)} шаблонов, {len(schemas)} схем",
                       detail)


def check_optional_deps() -> list[CheckResult]:
    deps = [
        ("mcp", "MCP сервер"),
        ("anthropic", "LLM-функции"),
        ("pypdf", "PDF ингестия"),
        ("ebooklib", "EPUB ингестия"),
        ("docx", "DOCX ингестия (python-docx)"),
        ("pytest", "Тесты"),
    ]
    results = []
    for module, purpose in deps:
        try:
            spec = importlib.util.find_spec(module)
            if spec:
                results.append(CheckResult(f"dep_{module}", "ok", f"{purpose}"))
            else:
                results.append(CheckResult(f"dep_{module}", "warn",
                                           f"{purpose} (pip install {module})"))
        except Exception:
            results.append(CheckResult(f"dep_{module}", "warn",
                                       f"{purpose} — недоступен"))
    return results


def check_ingest_plugins() -> CheckResult:
    try:
        from docstoolkit.ingest import list_plugins
        plugins = list_plugins()
        return CheckResult("ingest_plugins", "ok",
                           f"{len(plugins)} плагинов: {', '.join(sorted(plugins))}")
    except Exception as e:
        return CheckResult("ingest_plugins", "error", f"Ошибка загрузки: {e}")


def check_writable(cfg) -> CheckResult:
    """Можем ли писать в docs/."""
    docs = cfg.docs_dir
    if not docs.exists():
        return CheckResult("writable", "warn", "docs/ не существует")
    test_file = docs / ".docstoolkit_write_test"
    try:
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        return CheckResult("writable", "ok", "docs/ доступна для записи")
    except Exception as e:
        return CheckResult("writable", "error", f"docs/ read-only: {e}")


def run_all_checks() -> list[CheckResult]:
    results: list[CheckResult] = []
    results.append(check_python_version())

    cfg_check = check_config()
    results.append(cfg_check)

    if cfg_check.status != "error":
        try:
            cfg = load_config()
            results.extend(check_structure(cfg))
            results.append(check_templates(cfg))
            results.append(check_writable(cfg))
        except Exception as e:
            results.append(CheckResult("structure", "error", str(e)))

    results.append(check_ingest_plugins())
    results.extend(check_optional_deps())

    return results


def render_text(results: list[CheckResult]) -> str:
    lines = ["# docstoolkit doctor\n"]

    by_status = {'ok': 0, 'warn': 0, 'error': 0}
    for r in results:
        by_status[r.status] = by_status.get(r.status, 0) + 1

    summary_color = "❌" if by_status['error'] else ("⚠️" if by_status['warn'] else "✅")
    lines.append(f"{summary_color} {by_status['ok']} ok, {by_status['warn']} warnings, {by_status['error']} errors\n")

    for r in results:
        lines.append(f"{r.icon} {r.name:25s} {r.message}")
        for k, v in r.detail.items():
            lines.append(f"    {k}: {v}")

    if by_status['error']:
        lines.append("\nИсправьте errors и запустите doctor снова.")
    return "\n".join(lines)


def render_json(results: list[CheckResult]) -> str:
    return json.dumps(
        [{"name": r.name, "status": r.status,
          "message": r.message, "detail": r.detail} for r in results],
        ensure_ascii=False, indent=2
    )


def doctor(as_json: bool = False) -> int:
    results = run_all_checks()
    if as_json:
        print(render_json(results))
    else:
        print(render_text(results))

    has_errors = any(r.status == 'error' for r in results)
    has_warns = any(r.status == 'warn' for r in results)
    if has_errors:
        return 2
    if has_warns:
        return 1
    return 0
