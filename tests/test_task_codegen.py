"""Тесты для improve_task_codegen.py — YAML парсер и валидация."""
from improve_task_codegen import parse_yaml, validate_manifest


def test_parse_yaml_simple():
    text = """
id: hello
version: 1.0
description: test task
"""
    result = parse_yaml(text)
    assert result['id'] == 'hello'
    assert result['version'] == 1.0
    assert result['description'] == 'test task'


def test_parse_yaml_list():
    text = """
trigger_phrases:
  - "first"
  - "second"
"""
    result = parse_yaml(text)
    assert result['trigger_phrases'] == ['first', 'second']


def test_parse_yaml_nested_dict():
    text = """
inputs:
  author:
    type: string
    required: true
"""
    result = parse_yaml(text)
    assert isinstance(result.get('inputs'), dict)
    assert result['inputs']['author']['type'] == 'string'
    assert result['inputs']['author']['required'] is True


def test_validate_manifest_required():
    errs = validate_manifest({'id': 'foo'}, None)
    assert any('version' in e for e in errs)
    assert any('description' in e for e in errs)


def test_validate_manifest_id_format():
    errs = validate_manifest({
        'id': 'BadID',
        'version': 1.0,
        'description': 'test',
    }, None)
    assert any('kebab-case' in e for e in errs)


def test_validate_manifest_mcp_server():
    errs = validate_manifest({
        'id': 'foo',
        'version': 1.0,
        'description': 'test',
        'mcp_server': 'unknown-server',
    }, None)
    assert any('mcp_server' in e for e in errs)


def test_validate_manifest_clean():
    errs = validate_manifest({
        'id': 'my-task',
        'version': 1.0,
        'description': 'test',
        'mcp_server': 'lorenzo-search',
        'trigger_phrases': ['hello'],
    }, None)
    assert errs == []
