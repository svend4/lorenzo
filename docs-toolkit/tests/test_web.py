"""Тесты web/ — структурные (без реальных HTTP)."""
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.web import fetch_url, fetch_arxiv
from docstoolkit.web.url import _fetch
from docstoolkit.web.arxiv import _parse_atom_entry
from docstoolkit.web.habr import _extract_habr_id
from docstoolkit.ingest.base import IngestError


def test_fetch_url_invalid_scheme():
    with pytest.raises(IngestError):
        fetch_url("ftp://example.com/file")


def test_fetch_url_with_mock():
    sample_html = ('<html><head><title>Mock Page</title></head>'
                   '<body><h1>Hello</h1><p>World</p></body></html>')
    with patch("docstoolkit.web.url._fetch", return_value=sample_html):
        doc = fetch_url("https://mock.example.com/page")
        assert doc.title == "Mock Page"
        assert doc.source.format == "url"
        assert "Hello" in doc.content
        assert doc.metadata["url"] == "https://mock.example.com/page"


def test_extract_habr_id_from_url():
    assert _extract_habr_id("https://habr.com/ru/articles/123456/") == "123456"
    assert _extract_habr_id("https://habr.com/ru/post/789012/") == "789012"
    assert _extract_habr_id("123456") == "123456"


def test_extract_habr_id_invalid():
    with pytest.raises(IngestError):
        _extract_habr_id("not-a-habr-url")


def test_parse_atom_entry_basic():
    xml = """<entry>
        <id>http://arxiv.org/abs/2401.12345</id>
        <title>Test Paper Title</title>
        <summary>Abstract here</summary>
        <published>2024-01-15T00:00:00Z</published>
        <author><name>John Doe</name></author>
        <author><name>Jane Smith</name></author>
        <category term="cs.AI"/>
        <category term="cs.LG"/>
    </entry>"""
    meta = _parse_atom_entry(xml)
    assert meta["title"] == "Test Paper Title"
    assert meta["summary"] == "Abstract here"
    assert "John Doe" in meta["authors"]
    assert "cs.AI" in meta["categories"]


def test_fetch_arxiv_with_mock():
    sample_xml = """<feed>
    <entry>
        <id>http://arxiv.org/abs/2401.12345v1</id>
        <title>Mock Paper</title>
        <summary>Mock abstract content here.</summary>
        <published>2024-01-15T00:00:00Z</published>
        <author><name>Mock Author</name></author>
        <category term="cs.AI"/>
    </entry>
    </feed>"""
    with patch("docstoolkit.web.arxiv._fetch", return_value=sample_xml):
        doc = fetch_arxiv("2401.12345")
        assert doc.title == "Mock Paper"
        assert doc.source.format == "arxiv"
        assert "Mock abstract" in doc.content
        assert doc.metadata["arxiv_id"] == "2401.12345"
        assert "Mock Author" in doc.metadata["authors"]


def test_fetch_arxiv_strips_prefix():
    sample_xml = """<feed><entry>
        <id>http://arxiv.org/abs/2401.12345v1</id>
        <title>X</title>
        <summary>Y</summary>
        <author><name>A</name></author>
    </entry></feed>"""
    with patch("docstoolkit.web.arxiv._fetch", return_value=sample_xml):
        doc = fetch_arxiv("arxiv:2401.12345")
        assert doc.metadata["arxiv_id"] == "2401.12345"


def test_fetch_arxiv_not_found():
    with patch("docstoolkit.web.arxiv._fetch", return_value="<feed></feed>"):
        with pytest.raises(IngestError):
            fetch_arxiv("nonexistent")
