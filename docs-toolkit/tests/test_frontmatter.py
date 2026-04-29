"""Тесты для docstoolkit.frontmatter"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.frontmatter import extract_frontmatter, parse_yaml


def test_parse_yaml_basic():
    text = 'foo: bar\nnum: 42'
    assert parse_yaml(text) == {'foo': 'bar', 'num': 42}


def test_parse_yaml_quoted_string():
    text = 'ver: "1.0"'
    assert parse_yaml(text)['ver'] == '1.0'


def test_parse_yaml_inline_list():
    text = 'tags: [a, b, c]'
    assert parse_yaml(text)['tags'] == ['a', 'b', 'c']


def test_parse_yaml_bool_null():
    text = 'enabled: true\ndisabled: false\nempty: null'
    result = parse_yaml(text)
    assert result['enabled'] is True
    assert result['disabled'] is False
    assert result['empty'] is None


def test_extract_frontmatter_present():
    text = '---\ntitle: Test\n---\n\n# Body'
    fm, body = extract_frontmatter(text)
    assert fm == {'title': 'Test'}
    assert '# Body' in body


def test_extract_frontmatter_absent():
    text = '# Just a body\n\nNo frontmatter'
    fm, body = extract_frontmatter(text)
    assert fm is None
    assert body == text


def test_parse_yaml_skips_comments():
    text = '# this is a comment\nfoo: bar'
    assert parse_yaml(text) == {'foo': 'bar'}
