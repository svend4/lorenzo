"""
serve.py — встроенный HTTP-сервер для docs-toolkit (только stdlib).

Запускает простой dashboard:
  - /                  — главная страница со сводкой
  - /docs              — список документов
  - /docs/<path>       — рендер одного файла
  - /search?q=...      — JSON поиск
  - /templates         — список шаблонов
  - /api/health        — JSON health check
  - /api/registry      — JSON всех артефактов

Запуск:
    docstoolkit serve --port 8000
"""
import http.server
import json
import re
import socketserver
import urllib.parse
from datetime import datetime
from pathlib import Path

from docstoolkit.config import load_config
from docstoolkit.frontmatter import extract_frontmatter


CSS = """
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
       max-width: 1200px; margin: 2em auto; padding: 0 1em; line-height: 1.5;
       color: #24292e; }
h1, h2, h3 { color: #0366d6; }
a { color: #0366d6; text-decoration: none; }
a:hover { text-decoration: underline; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; }
th, td { border: 1px solid #e1e4e8; padding: 8px 12px; text-align: left; }
th { background: #f6f8fa; }
tr:nth-child(even) { background: #f9f9f9; }
code { background: #f6f8fa; padding: 2px 6px; border-radius: 3px;
       font-family: "SF Mono", Consolas, monospace; font-size: 0.9em; }
pre { background: #f6f8fa; padding: 12px; border-radius: 6px; overflow: auto; }
nav { background: #f6f8fa; padding: 8px 16px; border-radius: 6px; margin-bottom: 1em; }
nav a { margin-right: 1em; }
.score { font-size: 2em; font-weight: bold; }
.score.green { color: #28a745; }
.score.yellow { color: #ffc107; }
.score.red { color: #dc3545; }
form input { padding: 6px 10px; font-size: 1em; width: 60%; }
form button { padding: 6px 14px; font-size: 1em; background: #0366d6;
              color: white; border: none; border-radius: 4px; cursor: pointer; }
.tag { background: #e1ecf4; color: #0366d6; padding: 2px 8px; border-radius: 3px;
       font-size: 0.85em; margin-right: 4px; }
"""

NAV = """
<nav>
  <a href="/">🏠 Home</a>
  <a href="/docs">📚 Docs</a>
  <a href="/templates">📝 Templates</a>
  <a href="/api/registry">🗂 Registry (JSON)</a>
  <a href="/api/health">💚 Health (JSON)</a>
</nav>
"""


def _wrap_html(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title} — docs-toolkit</title>
<style>{CSS}</style>
</head>
<body>
{NAV}
{body}
</body>
</html>"""


class DocsHandler(http.server.BaseHTTPRequestHandler):
    cfg = None  # настраивается в serve()

    def log_message(self, format, *args):
        pass  # Тихий режим

    def _send(self, status: int, body: str, content_type: str = "text/html; charset=utf-8"):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(encoded)

    def _send_json(self, data, status: int = 200):
        body = json.dumps(data, ensure_ascii=False, indent=2)
        self._send(status, body, "application/json; charset=utf-8")

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path.rstrip("/") or "/"
        params = urllib.parse.parse_qs(url.query)

        try:
            if path == "/":
                self._send(200, self._render_home())
            elif path == "/docs":
                self._send(200, self._render_docs_list())
            elif path.startswith("/docs/"):
                rel = path[len("/docs/"):]
                self._send(200, self._render_doc(rel))
            elif path == "/templates":
                self._send(200, self._render_templates())
            elif path == "/search":
                q = params.get("q", [""])[0]
                self._send_json(self._search(q))
            elif path == "/api/health":
                self._send_json(self._health())
            elif path == "/api/registry":
                self._send_json(self._registry())
            else:
                self._send(404, _wrap_html("404", "<h1>404 Not Found</h1>"))
        except Exception as e:
            self._send(500, _wrap_html("Error", f"<h1>500</h1><pre>{e}</pre>"))

    # ----- Renderers -----

    def _render_home(self) -> str:
        h = self._health()
        score = h.get("health_score") or 0
        color = "green" if score >= 75 else "yellow" if score >= 50 else "red"
        body = f"""
<h1>📊 docs-toolkit dashboard</h1>
<p><strong>Корень:</strong> <code>{self.cfg.root}</code></p>

<div class="score {color}">{score}/100</div>
<p>Health score (из <a href="/docs/HEALTH.md">HEALTH.md</a>)</p>

<h2>Поиск</h2>
<form action="/search" method="get">
  <input name="q" placeholder="Запрос..." autofocus>
  <button>Найти</button>
</form>
<p><small>Возвращает JSON. UI: TODO.</small></p>

<h2>Сводка</h2>
<table>
  <tr><th>Слой</th><th>Кол-во</th></tr>
  <tr><td>Документов в docs/</td><td>{h.get('docs_count', '?')}</td></tr>
  <tr><td>Шаблонов</td><td>{h.get('templates_count', '?')}</td></tr>
  <tr><td>Слов всего</td><td>{h.get('total_words', '?'):,}</td></tr>
</table>

<p><em>Обновлено: {datetime.now().isoformat(timespec='seconds')}</em></p>
"""
        return _wrap_html("Home", body)

    def _render_docs_list(self) -> str:
        docs = self.cfg.docs_dir
        if not docs.exists():
            return _wrap_html("Docs", f"<p>docs/ не найден: {docs}</p>")
        files = sorted(docs.rglob("*.md"))[:300]
        rows = []
        for f in files:
            rel = f.relative_to(docs)
            rows.append(f'<tr><td><a href="/docs/{rel}">{rel}</a></td>'
                        f'<td>{f.stat().st_size:,} B</td></tr>')
        body = f"<h1>📚 Документы ({len(files)})</h1>\n<table>" \
               f"<tr><th>Путь</th><th>Размер</th></tr>{''.join(rows)}</table>"
        return _wrap_html("Docs", body)

    def _render_doc(self, rel: str) -> str:
        path = (self.cfg.docs_dir / rel).resolve()
        # Защита от path traversal
        try:
            path.relative_to(self.cfg.docs_dir.resolve())
        except ValueError:
            return _wrap_html("Forbidden", "<h1>403</h1>")
        if not path.exists():
            return _wrap_html("Not found", f"<h1>404</h1><p>{rel}</p>")
        text = path.read_text(encoding="utf-8")
        fm, body = extract_frontmatter(text)

        fm_html = ""
        if fm:
            rows = "".join(f'<tr><td><code>{k}</code></td><td>{_escape(str(v))}</td></tr>'
                           for k, v in fm.items())
            fm_html = f'<details><summary>Frontmatter</summary><table>{rows}</table></details>'

        # Минимальный markdown→html (для preview)
        html_body = _md_to_html(body)
        return _wrap_html(rel, f"<h1>{rel}</h1>{fm_html}<hr>{html_body}")

    def _render_templates(self) -> str:
        td = self.cfg.templates_dir
        sd = self.cfg.schemas_dir
        if not td.exists():
            return _wrap_html("Templates", "<p>Нет templates/</p>")
        rows = []
        for path in sorted(td.glob("*.md")):
            if path.name == "README.md":
                continue
            schema = sd / f"{path.stem}.json"
            desc = ""
            req_fields = ""
            if schema.exists():
                try:
                    s = json.loads(schema.read_text(encoding="utf-8"))
                    desc = s.get("description", "")[:120]
                    req_fields = ", ".join(s.get("required", []))
                except Exception:
                    pass
            rows.append(f'<tr><td><a href="/docs/templates/{path.name}"><code>{path.stem}</code></a></td>'
                        f'<td>{_escape(desc)}</td><td>{_escape(req_fields)}</td></tr>')
        body = f"<h1>📝 Шаблоны ({len(rows)})</h1><table>" \
               "<tr><th>Шаблон</th><th>Описание</th><th>Required fields</th></tr>" \
               f"{''.join(rows)}</table>"
        return _wrap_html("Templates", body)

    def _search(self, q: str) -> dict:
        if not q:
            return {"query": "", "results": []}
        index = self._load_search_index()
        if not index:
            return {"query": q, "error": "search_index.json not found", "results": []}
        ql = q.lower()
        scored = []
        for d in index:
            score = 0
            if ql in d.get("title", "").lower():
                score += 5
            if ql in d.get("path", "").lower():
                score += 3
            if ql in d.get("content", "").lower() or ql in d.get("preview", "").lower():
                score += 1
            if score > 0:
                scored.append({"score": score, "title": d.get("title", ""),
                               "path": d.get("path", ""),
                               "preview": d.get("preview", "")[:200]})
        scored.sort(key=lambda x: -x["score"])
        return {"query": q, "results": scored[:20]}

    def _load_search_index(self) -> list[dict]:
        path = self.cfg.docs_dir / "search_index.json"
        if not path.exists():
            return []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else data.get("docs", [])
        except Exception:
            return []

    def _health(self) -> dict:
        docs = self.cfg.docs_dir
        result = {
            "ts": datetime.now().isoformat(timespec='seconds'),
            "root": str(self.cfg.root),
            "docs_count": 0,
            "templates_count": 0,
            "total_words": 0,
            "health_score": None,
        }
        if docs.exists():
            files = list(docs.rglob("*.md"))
            result["docs_count"] = len(files)
            for f in files[:500]:  # Sampled
                try:
                    result["total_words"] += len(f.read_text(encoding="utf-8").split())
                except Exception:
                    pass
        td = self.cfg.templates_dir
        if td.exists():
            result["templates_count"] = sum(1 for f in td.glob("*.md") if f.name != "README.md")

        # Прочитать HEALTH.md если есть
        health_md = docs / "HEALTH.md"
        if health_md.exists():
            text = health_md.read_text(encoding="utf-8")
            m = re.search(r'(\d+)/100', text)
            if m:
                result["health_score"] = int(m.group(1))
        return result

    def _registry(self) -> dict:
        return {
            "ts": datetime.now().isoformat(timespec='seconds'),
            "config": {
                "root": str(self.cfg.root),
                "docs_dir": str(self.cfg.docs_dir),
                "templates_dir": str(self.cfg.templates_dir),
            },
            "health": self._health(),
        }


def _md_to_html(md: str) -> str:
    """Минимальный markdown → html для preview."""
    html_lines = []
    in_code = False
    for line in md.splitlines():
        if line.startswith("```"):
            html_lines.append("</pre>" if in_code else "<pre>")
            in_code = not in_code
            continue
        if in_code:
            html_lines.append(_escape(line))
            continue
        # Headings
        m = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if m:
            level = len(m.group(1))
            html_lines.append(f"<h{level}>{_escape(m.group(2))}</h{level}>")
            continue
        # List
        if line.startswith("- "):
            html_lines.append(f"<li>{_inline(line[2:])}</li>")
            continue
        if not line.strip():
            html_lines.append("<br>")
            continue
        html_lines.append(f"<p>{_inline(line)}</p>")
    return "\n".join(html_lines)


def _inline(text: str) -> str:
    text = _escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'`(.+?)`', r'<code>\1</code>', text)
    text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
    return text


def _escape(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;").replace("'", "&#x27;"))


def serve(port: int = 8000, bind: str = "127.0.0.1"):
    cfg = load_config()
    DocsHandler.cfg = cfg

    print(f"📊 docs-toolkit serve")
    print(f"   Корень: {cfg.root}")
    print(f"   docs/:  {cfg.docs_dir}")
    print(f"   URL:    http://{bind}:{port}/")
    print(f"   Ctrl+C для остановки\n")

    with socketserver.TCPServer((bind, port), DocsHandler) as httpd:
        httpd.allow_reuse_address = True
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Остановлено")
