"""Тесты docstoolkit.serve — рендеринг и handler."""
import json
import socketserver
import sys
import threading
import urllib.request
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from docstoolkit.serve import _md_to_html, _escape, _inline, DocsHandler
from docstoolkit.config import Config


def test_escape_html():
    assert _escape("<script>") == "&lt;script&gt;"
    assert _escape("a & b") == "a &amp; b"
    assert _escape('a"b') == "a&quot;b"
    assert _escape("a'b") == "a&#x27;b"


def test_inline_markdown():
    assert "<strong>bold</strong>" in _inline("**bold**")
    assert "<code>code</code>" in _inline("`code`")
    assert '<a href="url">text</a>' in _inline("[text](url)")


def test_inline_escape_first():
    """XSS в инлайне должны экранироваться до markdown-обработки."""
    out = _inline("<script>**alert**</script>")
    assert "<script>" not in out


def test_md_to_html_headings():
    out = _md_to_html("# H1\n## H2\n### H3")
    assert "<h1>H1</h1>" in out
    assert "<h2>H2</h2>" in out
    assert "<h3>H3</h3>" in out


def test_md_to_html_lists():
    out = _md_to_html("- one\n- two")
    assert "<li>one</li>" in out
    assert "<li>two</li>" in out


def test_md_to_html_code_block():
    out = _md_to_html("```\nx = 1\n```")
    assert "<pre>" in out
    assert "</pre>" in out


def test_handler_path_traversal_blocked(tmp_path):
    """Запросы с .. не должны выходить за пределы docs/."""
    cfg = Config(
        root=tmp_path,
        paths={"docs": "docs", "templates": "docs/templates",
               "schemas": "docs/templates/_schemas",
               "tasks": "tasks", "skills": ".claude/skills"},
        validation={}, language={}, sections={},
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "ok.md").write_text("# ok")
    secret = tmp_path / "secret.txt"
    secret.write_text("password")

    DocsHandler.cfg = cfg

    httpd = socketserver.TCPServer(("127.0.0.1", 0), DocsHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    try:
        # Path traversal должен возвращать 200 с "403"-страницей
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}/docs/../secret.txt")
        body = r.read().decode("utf-8")
        assert "403" in body or "404" in body
        assert "password" not in body
    finally:
        httpd.shutdown()


def test_handler_health_endpoint(tmp_path):
    cfg = Config(
        root=tmp_path,
        paths={"docs": "docs", "templates": "docs/templates",
               "schemas": "docs/templates/_schemas",
               "tasks": "tasks", "skills": ".claude/skills"},
        validation={}, language={}, sections={},
    )
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "a.md").write_text("# a")
    (docs / "b.md").write_text("# b")

    DocsHandler.cfg = cfg
    httpd = socketserver.TCPServer(("127.0.0.1", 0), DocsHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()

    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{port}/api/health")
        data = json.loads(r.read().decode("utf-8"))
        assert data["docs_count"] == 2
        assert "ts" in data
    finally:
        httpd.shutdown()


def test_handler_404(tmp_path):
    cfg = Config(
        root=tmp_path,
        paths={"docs": "docs", "templates": "docs/templates",
               "schemas": "docs/templates/_schemas",
               "tasks": "tasks", "skills": ".claude/skills"},
        validation={}, language={}, sections={},
    )
    (tmp_path / "docs").mkdir()
    DocsHandler.cfg = cfg
    httpd = socketserver.TCPServer(("127.0.0.1", 0), DocsHandler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/nonexistent")
        except urllib.error.HTTPError as e:
            assert e.code == 404
    finally:
        httpd.shutdown()
