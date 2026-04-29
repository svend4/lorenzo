"""Тесты cloud ingest plugins (Notion / Slack / Confluence).

Используют моки + проверяют структурные конвертеры без сетевых вызовов.
"""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.ingest.notion import _extract_page_id as notion_id, _block_to_md, _rich_text
from docstoolkit.ingest.confluence import _storage_to_md, _extract_page_id as conf_id
from docstoolkit.ingest.slack import _ingest_day
from docstoolkit.ingest.base import IngestError


# Notion

def test_notion_extract_page_id_from_uuid():
    assert notion_id("11112222333344445555666677778888") == "11112222-3333-4444-5555-666677778888"


def test_notion_extract_page_id_from_url():
    url = "https://www.notion.so/My-Page-abcdef0123456789abcdef0123456789"
    pid = notion_id(url)
    assert pid.count("-") == 4


def test_notion_block_paragraph():
    block = {
        "type": "paragraph",
        "paragraph": {"rich_text": [
            {"plain_text": "Hello ", "annotations": {}},
            {"plain_text": "world", "annotations": {"bold": True}},
        ]}
    }
    md = _block_to_md(block)
    assert "Hello" in md
    assert "**world**" in md


def test_notion_block_heading():
    block = {"type": "heading_2", "heading_2": {"rich_text": [{"plain_text": "H2"}]}}
    assert _block_to_md(block) == "## H2"


def test_notion_block_code():
    block = {"type": "code", "code": {
        "language": "python",
        "rich_text": [{"plain_text": "print(1)"}]
    }}
    md = _block_to_md(block)
    assert "```python" in md
    assert "print(1)" in md


def test_notion_block_to_do():
    block = {"type": "to_do", "to_do": {
        "checked": True,
        "rich_text": [{"plain_text": "Done item"}]
    }}
    md = _block_to_md(block)
    assert "[x]" in md
    assert "Done item" in md


def test_notion_rich_text_annotations():
    rt = [
        {"plain_text": "x", "annotations": {"italic": True}},
        {"plain_text": "y", "annotations": {"code": True}},
    ]
    out = _rich_text(rt)
    assert "*x*" in out
    assert "`y`" in out


# Confluence

def test_confluence_extract_page_id_from_url():
    url = "https://x.atlassian.net/wiki/spaces/A/pages/67890/Title"
    assert conf_id(url) == "67890"


def test_confluence_extract_page_id_param():
    assert conf_id("?pageId=99999") == "99999"


def test_confluence_extract_page_id_digits():
    assert conf_id("12345") == "12345"


def test_confluence_storage_to_md_headings():
    csf = "<h1>Title</h1><h2>Sub</h2>"
    md = _storage_to_md(csf)
    assert "# Title" in md
    assert "## Sub" in md


def test_confluence_storage_to_md_inline():
    csf = "<p>Hello <strong>bold</strong> and <em>italic</em>.</p>"
    md = _storage_to_md(csf)
    assert "**bold**" in md
    assert "*italic*" in md


def test_confluence_storage_to_md_lists():
    csf = "<ul><li>One</li><li>Two</li></ul>"
    md = _storage_to_md(csf)
    assert "- One" in md
    assert "- Two" in md


def test_confluence_storage_to_md_code():
    csf = '<ac:plain-text-body><![CDATA[print(1)]]></ac:plain-text-body>'
    md = _storage_to_md(csf)
    assert "```" in md
    assert "print(1)" in md


# Slack

def test_slack_ingest_day(tmp_path):
    json_path = tmp_path / "2024-01-15.json"
    messages = [
        {"ts": "1705320000.0", "user": "alice", "text": "Hello"},
        {"ts": "1705320060.0", "user_profile": {"real_name": "Bob"}, "text": "World"},
    ]
    json_path.write_text(json.dumps(messages), encoding="utf-8")

    doc = _ingest_day(json_path)
    assert doc.metadata["messages"] == 2
    assert "Hello" in doc.content
    assert "World" in doc.content
    assert "alice" in doc.content or "Bob" in doc.content


def test_slack_invalid_json_raises(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("not json", encoding="utf-8")
    with pytest.raises(IngestError):
        _ingest_day(bad)


def test_slack_not_list_raises(tmp_path):
    bad = tmp_path / "obj.json"
    bad.write_text('{"foo": "bar"}', encoding="utf-8")
    with pytest.raises(IngestError):
        _ingest_day(bad)
