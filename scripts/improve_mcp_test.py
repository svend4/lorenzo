"""
improve_mcp_test.py — smoke-тесты для всех MCP-серверов.

Проверяет:
  1. Что каждый сервер импортируется без ошибок
  2. Что dispatch() возвращает строку для известных инструментов
  3. Что dispatch() обрабатывает unknown tool gracefully

Не запускает stdio_server (требует MCP-клиента).

Запуск:
    python scripts/improve_mcp_test.py
"""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"


SERVERS = [
    ("mcp_search_server", [
        ("search_docs", {"query": "test"}),
        ("find_similar", {"file_path": "docs/HEALTH.md"}),
    ]),
    ("mcp_contacts_server", [
        ("list_contacts", {}),
        ("get_contact", {"author": "nonexistent"}),
    ]),
    ("mcp_runner_server", [
        ("list_scripts", {"group": "structure"}),
    ]),
    ("mcp_graph_server", [
        ("get_health", {}),
    ]),
    ("mcp_templates_server", [
        ("list_templates", {}),
        ("list_tasks", {}),
    ]),
    ("mcp_export_server", [
        ("list_formats", {}),
    ]),
    ("mcp_watch_server", [
        ("recent_changes", {"hours": 24}),
        ("pending_actions", {}),
    ]),
    ("mcp_skills_server", [
        ("list_skills", {"category": "meta"}),
        ("match_skill", {"query": "найди про"}),
        ("compose_skills", {"skills": ["search", "summarize"]}),
        ("get_skill", {"name": "skill-router"}),
    ]),
]


def _import(module_name: str):
    """Импорт без запуска __main__."""
    path = SCRIPTS / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    sys.path.insert(0, str(SCRIPTS))
    try:
        spec.loader.exec_module(mod)
    except SystemExit:
        # Сервер вызвал sys.exit() — обычно из-за отсутствия mcp пакета
        pass
    return mod


def main():
    sys.path.insert(0, str(SCRIPTS))
    failed = 0
    passed = 0
    for module_name, tests in SERVERS:
        try:
            mod = _import(module_name)
        except Exception as e:
            print(f"❌ import {module_name}: {e}")
            failed += 1
            continue

        if not hasattr(mod, 'dispatch'):
            print(f"⚠️  {module_name}: нет функции dispatch")
            continue

        for tool, args in tests:
            try:
                result = mod.dispatch(tool, args)
                if not isinstance(result, str):
                    print(f"❌ {module_name}.{tool}: вернул не string ({type(result).__name__})")
                    failed += 1
                    continue
                print(f"✓ {module_name}.{tool} → {len(result)} chars")
                passed += 1
            except Exception as e:
                print(f"❌ {module_name}.{tool}: {e}")
                failed += 1

        # Тест unknown tool
        try:
            result = mod.dispatch("__nonexistent__", {})
            if "Неизвестный" in result or "unknown" in result.lower():
                passed += 1
            else:
                print(f"⚠️  {module_name}: dispatch не обработал unknown tool gracefully")
        except Exception as e:
            print(f"❌ {module_name}.dispatch(unknown): {e}")
            failed += 1

    print(f"\n{'=' * 50}")
    print(f"Passed: {passed}, Failed: {failed}")
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
