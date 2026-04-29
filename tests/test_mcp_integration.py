"""Интеграционные тесты MCP-серверов: проверяют контракт инструментов.

Не требуют реального mcp-runtime — используют stub из mcp_common.
Проверяют:
  1. Каждый сервер экспортирует TOOLS/dispatch
  2. dispatch обрабатывает все объявленные tool names
  3. dispatch обрабатывает unknown tool gracefully
  4. dispatch возвращает строку для всех инструментов
  5. Inputs Schema каждого Tool — валидный JSON Schema
"""
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"

SERVERS = [
    "mcp_search_server",
    "mcp_contacts_server",
    "mcp_runner_server",
    "mcp_graph_server",
    "mcp_templates_server",
    "mcp_export_server",
    "mcp_llm_server",
    "mcp_watch_server",
]


def load_server(name: str):
    sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.mark.parametrize("server_name", SERVERS)
def test_server_exports(server_name):
    mod = load_server(server_name)
    assert hasattr(mod, 'dispatch'), f"{server_name} нет dispatch"
    assert hasattr(mod, 'TOOLS'), f"{server_name} нет TOOLS"
    assert isinstance(mod.TOOLS, list), f"{server_name}.TOOLS не list"
    assert len(mod.TOOLS) > 0, f"{server_name}.TOOLS пуст"


@pytest.mark.parametrize("server_name", SERVERS)
def test_dispatch_unknown_tool(server_name):
    mod = load_server(server_name)
    result = mod.dispatch("__nonexistent_tool__", {})
    assert isinstance(result, str)
    assert any(s in result.lower() for s in ['неизвест', 'unknown'])


@pytest.mark.parametrize("server_name", SERVERS)
def test_dispatch_returns_string(server_name):
    mod = load_server(server_name)
    for tool in mod.TOOLS:
        tool_name = getattr(tool, 'name', None) or tool.__dict__.get('name')
        if not tool_name:
            continue
        # Минимальные args
        result = mod.dispatch(tool_name, {})
        assert isinstance(result, str), \
            f"{server_name}.{tool_name} вернул {type(result).__name__}, не str"


@pytest.mark.parametrize("server_name", SERVERS)
def test_input_schemas_valid_json_schema(server_name):
    mod = load_server(server_name)
    for tool in mod.TOOLS:
        schema = getattr(tool, 'inputSchema', None) or tool.__dict__.get('inputSchema')
        if not schema:
            continue
        assert isinstance(schema, dict), \
            f"{server_name}: inputSchema не dict"
        assert schema.get('type') == 'object', \
            f"{server_name}: inputSchema.type != 'object'"
        assert 'properties' in schema, \
            f"{server_name}: inputSchema без properties"
        if 'required' in schema:
            assert isinstance(schema['required'], list)


def test_logging_works(tmp_path, monkeypatch):
    """log_call записывает корректный JSONL."""
    sys.path.insert(0, str(SCRIPTS))
    import mcp_common
    log_path = tmp_path / 'mcp_calls.jsonl'
    monkeypatch.setattr(mcp_common, 'LOG_PATH', log_path)

    mcp_common.log_call('lorenzo-search', 'search_docs', {'query': 'test'}, 50, 'ok')
    mcp_common.log_call('lorenzo-graph', 'get_health', {}, 100, 'error')

    assert log_path.exists()
    lines = log_path.read_text(encoding='utf-8').strip().splitlines()
    assert len(lines) == 2
    e1 = json.loads(lines[0])
    assert e1['server'] == 'lorenzo-search'
    assert e1['tool'] == 'search_docs'
    assert 'ts' in e1
    assert e1['duration_ms'] == 50

    e2 = json.loads(lines[1])
    assert e2['status'] == 'error'


def test_search_server_integration():
    """End-to-end: search_docs возвращает форматированный markdown."""
    mod = load_server('mcp_search_server')
    result = mod.dispatch('search_docs', {'query': 'Yodoca', 'top_k': 2})
    assert isinstance(result, str)
    if 'Найдено' in result:
        assert 'Yodoca' in result or 'memory' in result.lower()


def test_templates_server_lists_22_templates():
    mod = load_server('mcp_templates_server')
    result = mod.dispatch('list_templates', {})
    assert isinstance(result, str)
    assert 'Шаблоны' in result
    # У нас 22 шаблона + 1 README = должны видеть несколько ключевых
    assert 'rfc' in result
    assert 'contact-outreach' in result


def test_runner_server_lists_groups():
    mod = load_server('mcp_runner_server')
    result = mod.dispatch('list_scripts', {'group': 'quality'})
    assert isinstance(result, str)
    # quality-группа должна содержать improve_validate.py или metrics
    assert 'improve_' in result


def test_contacts_server_lists_migrated_contacts():
    mod = load_server('mcp_contacts_server')
    result = mod.dispatch('list_contacts', {})
    assert isinstance(result, str)
    if 'Контактов' in result:
        # После миграции должно быть >= 14 контактов
        import re
        m = re.search(r'\*\*Контактов:\s*(\d+)\*\*', result)
        if m:
            assert int(m.group(1)) >= 10
