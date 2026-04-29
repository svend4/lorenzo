"""Тесты ингестии."""
import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.ingest import ingest_file, list_plugins, IngestError


def test_list_plugins_includes_basics():
    plugins = list_plugins()
    assert "md" in plugins
    assert "html" in plugins
    assert "ipynb" in plugins
    assert "mhtml" in plugins


def test_ingest_markdown_basic(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# Hello\n\n## Section A\n\nSome text\n\n## Section B\n\nMore", encoding="utf-8")
    doc = ingest_file(f)
    assert doc.title == "Hello"
    assert doc.source.format == "markdown"
    assert len(doc.sections) >= 2
    assert "Hello" in doc.content


def test_ingest_html_basic(tmp_path):
    f = tmp_path / "test.html"
    f.write_text(
        '<html><head><title>Page Title</title></head><body>'
        '<h1>Heading</h1><p>Paragraph with <strong>bold</strong>.</p>'
        '<ul><li>One</li><li>Two</li></ul></body></html>',
        encoding="utf-8"
    )
    doc = ingest_file(f)
    assert doc.title == "Page Title"
    assert doc.source.format == "html"
    assert "# Heading" in doc.content
    assert "**bold**" in doc.content
    assert "- One" in doc.content


def test_ingest_jupyter(tmp_path):
    nb = {
        "cells": [
            {"cell_type": "markdown", "source": ["# NB Title\n", "Description"]},
            {"cell_type": "code", "source": ["x = 1"], "outputs": []},
        ],
        "metadata": {"kernelspec": {"language": "python"}},
    }
    f = tmp_path / "test.ipynb"
    f.write_text(json.dumps(nb), encoding="utf-8")
    doc = ingest_file(f)
    assert doc.title == "NB Title"
    assert doc.metadata["code_cells"] == 1
    assert "```python" in doc.content


def test_ingest_unknown_extension_raises(tmp_path):
    f = tmp_path / "test.xyz"
    f.write_text("data")
    with pytest.raises(IngestError):
        ingest_file(f)


def test_ingest_missing_file_raises(tmp_path):
    with pytest.raises(IngestError):
        ingest_file(tmp_path / "nonexistent.md")


def test_document_to_markdown_with_frontmatter(tmp_path):
    f = tmp_path / "test.md"
    f.write_text("# T\n\ncontent", encoding="utf-8")
    doc = ingest_file(f)
    md = doc.to_markdown(frontmatter={"title": "T", "tag": "x"})
    assert md.startswith("---\n")
    assert 'title: "T"' in md or 'title: T' in md


def test_html_strips_script_and_style(tmp_path):
    f = tmp_path / "test.html"
    f.write_text(
        '<html><head><script>alert("x")</script><style>body{color:red}</style></head>'
        '<body><h1>Real Content</h1></body></html>',
        encoding="utf-8"
    )
    doc = ingest_file(f)
    assert "alert" not in doc.content
    assert "color:red" not in doc.content
    assert "Real Content" in doc.content
