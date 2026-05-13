"""Tests for scripts/extract_mhtml.py."""

import importlib
import sys
from pathlib import Path

import pytest
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

mod = importlib.import_module("extract_mhtml")


def tag(html: str):
    """Return the first element of parsed HTML."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.contents[0]


# ── _el_to_md ─────────────────────────────────────────────────────────────────

def test_el_to_md_h1():
    result = mod._el_to_md(tag("<h1>Title</h1>"))
    assert result == "# Title"


def test_el_to_md_h2():
    result = mod._el_to_md(tag("<h2>Subtitle</h2>"))
    assert result == "## Subtitle"


def test_el_to_md_h3():
    result = mod._el_to_md(tag("<h3>Section</h3>"))
    assert result == "### Section"


def test_el_to_md_paragraph():
    result = mod._el_to_md(tag("<p>Hello world.</p>"))
    assert "Hello world." in result


def test_el_to_md_strong():
    result = mod._el_to_md(tag("<strong>Bold</strong>"))
    assert result == "**Bold**"


def test_el_to_md_bold_tag():
    result = mod._el_to_md(tag("<b>Bold</b>"))
    assert result == "**Bold**"


def test_el_to_md_em():
    result = mod._el_to_md(tag("<em>Italic</em>"))
    assert result == "*Italic*"


def test_el_to_md_inline_code():
    result = mod._el_to_md(tag("<code>var x = 1;</code>"))
    assert result == "`var x = 1;`"


def test_el_to_md_pre_code():
    result = mod._el_to_md(tag("<pre><code>def foo():\n    pass</code></pre>"))
    assert "```" in result
    assert "def foo():" in result


def test_el_to_md_pre_code_language():
    result = mod._el_to_md(tag('<pre><code class="language-python">x = 1</code></pre>'))
    assert "```python" in result


def test_el_to_md_ul():
    result = mod._el_to_md(tag("<ul><li>Item 1</li><li>Item 2</li></ul>"))
    assert "- Item 1" in result
    assert "- Item 2" in result


def test_el_to_md_ol():
    result = mod._el_to_md(tag("<ol><li>First</li><li>Second</li></ol>"))
    assert "1." in result
    assert "2." in result


def test_el_to_md_table():
    html = "<table><tr><th>A</th><th>B</th></tr><tr><td>1</td><td>2</td></tr></table>"
    result = mod._el_to_md(tag(html))
    assert "| A | B |" in result
    assert "---" in result


def test_el_to_md_blockquote():
    result = mod._el_to_md(tag("<blockquote>Quoted text</blockquote>"))
    assert result.startswith("> ")
    assert "Quoted text" in result


def test_el_to_md_hr():
    result = mod._el_to_md(tag("<hr/>"))
    assert result == "---"


def test_el_to_md_link_http():
    result = mod._el_to_md(tag('<a href="https://example.com">Example</a>'))
    assert "[Example](https://example.com)" == result


def test_el_to_md_link_relative():
    result = mod._el_to_md(tag('<a href="/page">Local</a>'))
    assert result == "Local"


def test_el_to_md_span_passthrough():
    result = mod._el_to_md(tag("<span>Span text</span>"))
    assert "Span text" in result


def test_el_to_md_div_passthrough():
    result = mod._el_to_md(tag("<div>Div content</div>"))
    assert "Div content" in result


def test_el_to_md_string_input():
    result = mod._el_to_md("  plain text  ")
    assert result == "plain text"


def test_el_to_md_empty_strong():
    result = mod._el_to_md(tag("<strong></strong>"))
    assert result == ""


# ── _extract_claude_response ──────────────────────────────────────────────────

def test_extract_claude_response_returns_string():
    soup = BeautifulSoup("<div><p>Hello</p><p>World</p></div>", "html.parser")
    div = soup.find("div")
    result = mod._extract_claude_response(div)
    assert isinstance(result, str)


def test_extract_claude_response_joins_paragraphs():
    soup = BeautifulSoup("<div><p>First paragraph.</p><p>Second paragraph.</p></div>", "html.parser")
    div = soup.find("div")
    result = mod._extract_claude_response(div)
    assert "First paragraph." in result
    assert "Second paragraph." in result


def test_extract_claude_response_empty_div():
    soup = BeautifulSoup("<div></div>", "html.parser")
    div = soup.find("div")
    result = mod._extract_claude_response(div)
    assert isinstance(result, str)
    assert result == ""


def test_extract_claude_response_with_heading():
    soup = BeautifulSoup("<div><h2>Section</h2><p>Content.</p></div>", "html.parser")
    div = soup.find("div")
    result = mod._extract_claude_response(div)
    assert "Section" in result
    assert "Content." in result
