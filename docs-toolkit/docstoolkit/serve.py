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
  <a href="/search">🔍 Search</a>
  <a href="/faceted">🗂 Faceted</a>
  <a href="/rag">🤖 RAG</a>
  <a href="/graph">🌐 Graph</a>
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
                # HTML form + result rendering
                q = params.get("q", [""])[0]
                if "json" in params:
                    self._send_json(self._search(q))
                else:
                    self._send(200, self._render_search_ui(q))
            elif path == "/rag":
                q = params.get("q", [""])[0]
                method = params.get("method", ["hybrid"])[0]
                if "json" in params:
                    self._send_json(self._rag_ask(q, method))
                else:
                    self._send(200, self._render_rag_ui(q, method))
            elif path == "/graph":
                self._send(200, self._render_graph_ui())
            elif path == "/api/health":
                self._send_json(self._health())
            elif path == "/api/registry":
                self._send_json(self._registry())
            elif path == "/api/graph":
                self._send_json(self._graph_data(
                    int(params.get("max_nodes", ["50"])[0]),
                    int(params.get("min_edge", ["3"])[0]),
                ))
            elif path.startswith("/api/stream/jobs/"):
                job_id = path[len("/api/stream/jobs/"):]
                self._stream_job_progress(job_id)
            elif path == "/api/stream/build":
                # Streaming embeddings build
                self._stream_build_index(params.get("provider", ["tfidf"])[0])
            elif path == "/api/stream/heartbeat":
                self._stream_heartbeat(int(params.get("count", ["5"])[0]))
            elif path == "/api/stream/rag":
                self._stream_rag_sse(
                    params.get("q", [""])[0],
                    params.get("method", ["hybrid"])[0],
                    params.get("answerer", ["echo"])[0],
                    int(params.get("top_k", ["5"])[0]),
                )
            elif path == "/faceted":
                q = params.get("q", [""])[0]
                section = params.get("section", [""])[0]
                lang = params.get("lang", [""])[0]
                tags = params.get("tags", [""])[0]
                self._send(200, self._render_faceted_ui(q, section, lang, tags))
            elif path == "/api/faceted":
                q = params.get("q", [""])[0]
                section = params.get("section", [""])[0]
                lang = params.get("lang", [""])[0]
                tags = params.get("tags", [""])[0]
                docs = self._load_search_index()
                results = _faceted_search(docs, q, section=section, lang=lang, tags=tags)
                self._send_json({"query": q, "section": section, "lang": lang,
                                 "tags": tags, "results": results,
                                 "total": len(results)})
            elif path == "/metrics":
                # Prometheus exposition format
                try:
                    from docstoolkit.telemetry import prometheus_format
                    self._send(200, prometheus_format(),
                               "text/plain; version=0.0.4")
                except ImportError:
                    self._send(503, "telemetry not available", "text/plain")
            # ---------------- Sprint 54-92 feature endpoints ----------------
            elif path == "/api/ask":
                # Full-featured RAG via rag.ask(); accepts any subset of
                # kwargs (with_facets, with_provenance, self_rag, etc.) as
                # query strings. Boolean params accept "1"/"true"/"on".
                self._send_json(_api_ask(params))
            elif path == "/api/eval/dashboard":
                # HTML dashboard from continuous online eval data
                self._send(200, _api_eval_dashboard(params),
                           "text/html; charset=utf-8")
            elif path == "/api/saved":
                # List saved queries
                self._send_json(_api_saved_list(params))
            elif path == "/api/voice":
                # N4 epistemic profile of a text snippet
                self._send_json(_api_voice(params))
            elif path == "/api/assets":
                # M8 multi-modal asset search
                self._send_json(_api_assets(params))
            elif path == "/api/taxonomy":
                # N7 self-organising taxonomy over retrieved docs
                self._send_json(_api_taxonomy(params))
            elif path == "/api/diff":
                # S5 bulk diff between two commits
                self._send_json(_api_diff(params))
            elif path == "/api/kg":
                # M1 KG stats / direct entity-based retrieval
                self._send_json(_api_kg(params))
            elif path == "/api/profile":
                # S6 user profile load/save
                self._send_json(_api_profile(params))
            else:
                self._send(404, _wrap_html("404", "<h1>404 Not Found</h1>"))
        except Exception as e:
            self._send(500, _wrap_html("Error", f"<h1>500</h1><pre>{_escape(str(e))}</pre>"))

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

    # ----- New UI endpoints -----

    def _render_search_ui(self, q: str) -> str:
        result = self._search(q) if q else {"results": []}
        results_html = ""
        if q:
            if not result.get("results"):
                results_html = f"<p>Ничего не найдено по «{_escape(q)}»</p>"
            else:
                rows = []
                for r in result["results"]:
                    snippet = _escape(r.get("preview", "")[:300])
                    title = _escape(r.get("title", r.get("path", "?")))
                    path = r.get("path", "")
                    score = r.get("score", 0)
                    rows.append(
                        f'<div style="margin-bottom:1.5em;padding:0.5em;'
                        f'border-left:3px solid #0366d6">'
                        f'<a href="/docs/{_escape(path[5:] if path.startswith("docs/") else path)}">'
                        f'<strong>{title}</strong></a> '
                        f'<span style="color:#586069">score {score:.3f}</span>'
                        f'<div style="color:#586069;font-size:0.9em">{path}</div>'
                        f'<p>{snippet}…</p></div>')
                results_html = f"<p>Найдено: {len(result['results'])}</p>" + "".join(rows)

        body = f"""
<h1>🔍 Поиск</h1>
<form action="/search" method="get">
  <input name="q" placeholder="Запрос..." value="{_escape(q)}" autofocus
         style="width:60%">
  <button>Найти</button>
  <a href="/search?q={urllib.parse.quote(q)}&json=1" style="margin-left:1em">JSON</a>
</form>
<hr>
{results_html}
"""
        return _wrap_html("Search", body)

    def _render_rag_ui(self, q: str, method: str = "hybrid") -> str:
        result_html = ""
        if q:
            try:
                result = self._rag_ask(q, method)
                citations = result.get("citations", [])
                cites_html = ""
                if citations:
                    rows = []
                    for c in citations:
                        rows.append(f'<li>[{c["n"]}] '
                                    f'<a href="/docs/{_escape(c["doc_id"][5:] if c["doc_id"].startswith("docs/") else c["doc_id"])}">'
                                    f'<strong>{_escape(c.get("title", c["doc_id"]))}</strong></a> '
                                    f'<span style="color:#586069">score {c["score"]:.3f}</span></li>')
                    cites_html = f"<h3>Источники</h3><ol>{''.join(rows)}</ol>"
                answer_html = _md_to_html(result.get("answer", ""))
                result_html = (
                    f'<div style="background:#f6f8fa;padding:1em;border-radius:6px">'
                    f'<h3>Ответ</h3>{answer_html}{cites_html}'
                    f'<p style="color:#586069;font-size:0.85em">'
                    f'Время: {result.get("duration_ms", 0)}ms · '
                    f'Метод: {result.get("method", "?")} · '
                    f'Токенов: {result.get("tokens_used", 0)} · '
                    f'Cost: ${result.get("cost_estimate", 0):.6f}'
                    f'</p></div>'
                )
            except Exception as e:
                result_html = f'<p style="color:red">Ошибка: {_escape(str(e))}</p>'

        method_options = "".join(
            f'<option value="{m}"{" selected" if m == method else ""}>{m}</option>'
            for m in ["hybrid", "keyword", "semantic"]
        )
        body = f"""
<h1>🤖 RAG: вопрос-ответ</h1>
<form action="/rag" method="get">
  <input name="q" placeholder="Вопрос..." value="{_escape(q)}" autofocus
         style="width:55%">
  <select name="method">{method_options}</select>
  <button>Спросить</button>
</form>
<p style="color:#586069;font-size:0.85em">
Используется echo answerer (mock). Для реальных ответов установите
provider через config.</p>
<hr>
{result_html}
"""
        return _wrap_html("RAG", body)

    def _render_graph_ui(self) -> str:
        body = """
<h1>🌐 Knowledge graph</h1>
<p>Топ концептов и их связей. Загружается из <code>/api/graph</code>.</p>

<div style="margin:1em 0">
  Max nodes:
  <select id="max-nodes">
    <option value="30">30</option>
    <option value="50" selected>50</option>
    <option value="100">100</option>
    <option value="200">200</option>
  </select>
  Min edge weight:
  <select id="min-edge">
    <option value="2">2</option>
    <option value="3" selected>3</option>
    <option value="5">5</option>
    <option value="10">10</option>
  </select>
  <button onclick="loadGraph()">Обновить</button>
</div>

<div id="graph" style="width:100%;height:600px;border:1px solid #e1e4e8"></div>
<div id="info" style="margin-top:1em;padding:0.5em;background:#f6f8fa"></div>

<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<script>
const KIND_COLORS = {
  person: '#e1ecf4',
  project: '#d4f0d4',
  concept: '#f3e6d4',
  date: '#f0d4d4',
};

let network = null;

async function loadGraph() {
  const maxN = document.getElementById('max-nodes').value;
  const minE = document.getElementById('min-edge').value;
  document.getElementById('info').textContent = 'Загрузка...';
  const r = await fetch(`/api/graph?max_nodes=${maxN}&min_edge=${minE}`);
  const data = await r.json();
  document.getElementById('info').textContent =
    `Узлов: ${data.nodes.length}, связей: ${data.edges.length}`;

  const nodes = new vis.DataSet(data.nodes.map(n => ({
    id: n.name,
    label: `${n.name} (${n.count})`,
    color: KIND_COLORS[n.kind] || '#eeeeee',
    shape: 'box',
    title: `${n.kind}: ${n.count} mentions, ${n.docs} docs`,
  })));
  const edges = new vis.DataSet(data.edges.map(e => ({
    from: e[0], to: e[1], value: e[2],
    title: `weight ${e[2]}`,
  })));

  network = new vis.Network(
    document.getElementById('graph'),
    { nodes, edges },
    {
      physics: { enabled: true, stabilization: { iterations: 100 } },
      edges: { smooth: false },
      interaction: { hover: true },
    }
  );

  network.on('click', params => {
    if (params.nodes.length > 0) {
      const id = params.nodes[0];
      const node = data.nodes.find(n => n.name === id);
      document.getElementById('info').innerHTML =
        `<strong>${node.name}</strong> (${node.kind}): ${node.count} mentions, ${node.docs} docs`;
    }
  });
}

loadGraph();
</script>
"""
        return _wrap_html("Graph", body)

    def _rag_ask(self, q: str, method: str = "hybrid") -> dict:
        if not q:
            return {"answer": "", "citations": []}
        try:
            from docstoolkit.rag import ask
            result = ask(q, top_k=5, method=method, answerer="echo")
            return {
                "answer": result.answer,
                "citations": result.citations,
                "method": result.method,
                "duration_ms": result.duration_ms,
                "tokens_used": result.tokens_used,
                "cost_estimate": result.cost_estimate,
            }
        except Exception as e:
            return {"error": str(e), "answer": "", "citations": []}

    # ----- SSE (Server-Sent Events) -----

    def _send_sse_headers(self):
        """Подготовка SSE-ответа: длинный поток events."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def _sse_event(self, event: str, data) -> bytes:
        """Форматирует одно SSE-событие."""
        if not isinstance(data, str):
            data = json.dumps(data, ensure_ascii=False)
        return f"event: {event}\ndata: {data}\n\n".encode("utf-8")

    def _stream_heartbeat(self, count: int = 5):
        """Простой demo: heartbeat каждую секунду."""
        import time as _time
        self._send_sse_headers()
        try:
            for i in range(count):
                self.wfile.write(self._sse_event("tick", {
                    "n": i + 1, "ts": datetime.now().isoformat(timespec='seconds')
                }))
                self.wfile.flush()
                _time.sleep(1.0)
            self.wfile.write(self._sse_event("done", {"total": count}))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _stream_job_progress(self, job_id: str):
        """SSE-стрим прогресса job'а из jobs.sqlite."""
        import time as _time
        try:
            from docstoolkit.jobs import get_status
        except ImportError:
            self._send_sse_headers()
            self.wfile.write(self._sse_event("error", {"msg": "jobs not available"}))
            return

        self._send_sse_headers()
        try:
            last_progress = -1
            for _ in range(60):  # макс 60 итераций по 0.5с = 30 сек
                job = get_status(job_id)
                if not job:
                    self.wfile.write(self._sse_event("error", {"msg": "not found"}))
                    self.wfile.flush()
                    return
                if job.progress != last_progress or job.status != "running":
                    self.wfile.write(self._sse_event("progress", {
                        "id": job.id, "status": job.status,
                        "progress": job.progress,
                        "message": job.progress_message,
                    }))
                    self.wfile.flush()
                    last_progress = job.progress
                if job.status in ("completed", "failed", "cancelled"):
                    self.wfile.write(self._sse_event("done", {
                        "id": job.id, "status": job.status,
                        "duration_ms": job.duration_ms,
                        "result": job.result,
                        "error": job.error,
                    }))
                    self.wfile.flush()
                    return
                _time.sleep(0.5)
            self.wfile.write(self._sse_event("timeout", {"id": job_id}))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _stream_rag_sse(self, q: str, method: str, answerer: str, top_k: int):
        """SSE-стрим RAG с token-by-token output."""
        try:
            from docstoolkit.rag.streaming import stream_rag
        except ImportError:
            self._send_sse_headers()
            self.wfile.write(self._sse_event("error", {"msg": "rag not available"}))
            return

        self._send_sse_headers()
        try:
            for chunk in stream_rag(q, top_k=top_k, method=method, answerer=answerer):
                self.wfile.write(self._sse_event(chunk.type, chunk.data))
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:
            try:
                self.wfile.write(self._sse_event("error", {"msg": str(e)[:200]}))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _stream_build_index(self, provider: str = "tfidf"):
        """SSE-стрим build embeddings cache с progress events."""
        try:
            from docstoolkit.embeddings.cache import EmbeddingCache
            from docstoolkit.embeddings import get_provider
        except ImportError:
            self._send_sse_headers()
            self.wfile.write(self._sse_event("error", {"msg": "embeddings not available"}))
            return

        self._send_sse_headers()
        try:
            self.wfile.write(self._sse_event("start", {"provider": provider}))
            self.wfile.flush()

            docs = self._load_search_index()
            if not docs:
                self.wfile.write(self._sse_event("error", {"msg": "no search_index.json"}))
                return

            cache_path = self.cfg.root / ".docstoolkit" / "cache" / "embeddings.sqlite"
            cache = EmbeddingCache(cache_path)
            cache.invalidate(provider)

            if provider == "tfidf":
                from docstoolkit.embeddings.tfidf import TFIDFProvider
                prov = TFIDFProvider(cache=cache)
                prov.fit([d.get("content", "") + " " + d.get("title", "")
                          for d in docs], force=True)
                self.wfile.write(self._sse_event("idf", {"tokens": len(prov._idf)}))
                self.wfile.flush()
            else:
                prov = get_provider(provider)

            n = len(docs)
            saved = 0
            for i, d in enumerate(docs):
                text = d.get("content", "") + " " + d.get("title", "")
                if not text.strip():
                    continue
                doc_id = d.get("path", "")
                if not doc_id:
                    continue
                vec = prov.encode([text])[0]
                cache.save_vector(provider, doc_id, text, vec,
                                  dim=len(vec) if isinstance(vec, list) else 0)
                saved += 1
                if i % 50 == 0:
                    self.wfile.write(self._sse_event("progress", {
                        "saved": saved, "total": n,
                        "percent": int(100 * i / n) if n else 100,
                    }))
                    self.wfile.flush()

            cache.close()
            self.wfile.write(self._sse_event("done", {
                "provider": provider, "vectors": saved, "total": n,
            }))
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception as e:
            try:
                self.wfile.write(self._sse_event("error", {"msg": str(e)[:200]}))
                self.wfile.flush()
            except (BrokenPipeError, ConnectionResetError):
                pass

    def _graph_data(self, max_nodes: int = 50, min_edge: int = 3) -> dict:
        try:
            from docstoolkit.graph import build_from_docs_index
        except ImportError:
            return {"nodes": [], "edges": []}
        g = build_from_docs_index()
        top_names = {name for name, _ in g.top_concepts(max_nodes)}
        nodes = [
            {"name": name, "kind": data["kind"],
             "count": data["count"], "docs": len(data["docs"])}
            for name, data in g.nodes.items() if name in top_names
        ]
        edges = [
            [a, b, w]
            for (a, b), w in g.edges.items()
            if a in top_names and b in top_names and w >= min_edge
        ]
        return {"nodes": nodes, "edges": edges,
                "stats": g.stats()}


    def _render_faceted_ui(self, q: str, section: str = "",
                           lang: str = "", tags: str = "") -> str:
        """Рендер HTML-страницы фасетного поиска."""
        docs = self._load_search_index()

        # Собрать уникальные секции из paths
        sections: list[str] = sorted({
            d.get("path", "").split("/")[0]
            for d in docs
            if d.get("path", "") and "/" in d.get("path", "")
        })

        # Собрать топ-20 тегов из frontmatter
        tag_counter: dict[str, int] = {}
        for d in docs:
            for t in d.get("tags", []):
                if isinstance(t, str) and t:
                    tag_counter[t] = tag_counter.get(t, 0) + 1
        top_tags = sorted(tag_counter, key=lambda x: -tag_counter[x])[:20]

        # Результаты
        results = _faceted_search(docs, q, section=section, lang=lang, tags=tags) if (q or section or lang or tags) else []

        # Build section options
        section_opts = '<option value="">All sections</option>'
        for s in sections:
            sel = ' selected' if s == section else ''
            section_opts += f'<option value="{_escape(s)}"{sel}>{_escape(s)}</option>'

        # Build lang options
        lang_opts = ""
        for lv in ["", "RU", "EN", "MIX"]:
            lbl = lv if lv else "All languages"
            sel = ' selected' if lv == lang else ''
            lang_opts += f'<option value="{_escape(lv)}"{sel}>{_escape(lbl)}</option>'

        # Build tags checkboxes
        selected_tags = {t.strip() for t in tags.split(",") if t.strip()}
        tags_html = ""
        for t in top_tags:
            checked = ' checked' if t in selected_tags else ''
            tags_html += (f'<label style="margin-right:0.75em">'
                         f'<input type="checkbox" name="tags_cb" value="{_escape(t)}"{checked}> '
                         f'<span class="tag">{_escape(t)}</span></label>')

        # Results table
        results_html = ""
        if results:
            rows = "".join(
                f'<tr>'
                f'<td><a href="/docs/{_escape(r["path"][5:] if r["path"].startswith("docs/") else r["path"])}">'
                f'{_escape(r["title"] or r["path"])}</a></td>'
                f'<td><code>{_escape(r.get("section", ""))}</code></td>'
                f'<td>{r.get("score", 0):.3f}</td>'
                f'<td>{r.get("word_count", 0)}</td>'
                f'<td>{"".join(f"<span class=tag>{_escape(t)}</span>" for t in r.get("tags", []))}</td>'
                f'</tr>'
                for r in results
            )
            results_html = (
                f'<p>Найдено: {len(results)}</p>'
                f'<table><tr><th>Title</th><th>Section</th><th>Score</th>'
                f'<th>Words</th><th>Tags</th></tr>{rows}</table>'
            )
        elif q or section or lang or tags:
            results_html = "<p>Ничего не найдено.</p>"

        body = f"""
<h1>🗂 Faceted Search</h1>
<form action="/faceted" method="get" id="faceted-form">
  <div style="margin-bottom:0.75em">
    <input name="q" placeholder="Text query..." value="{_escape(q)}"
           style="width:50%" autofocus>
    <select name="section" style="margin-left:0.5em">{section_opts}</select>
    <select name="lang" style="margin-left:0.5em">{lang_opts}</select>
    <button style="margin-left:0.5em">Search</button>
    <a href="/api/faceted?q={urllib.parse.quote(q)}&amp;section={urllib.parse.quote(section)}&amp;lang={urllib.parse.quote(lang)}&amp;tags={urllib.parse.quote(tags)}"
       style="margin-left:1em">JSON</a>
  </div>
  <div style="margin-bottom:1em">
    <strong>Tags:</strong>&nbsp;{tags_html if tags_html else "<em>no tags in index</em>"}
  </div>
  <input type="hidden" name="tags" id="tags-hidden" value="{_escape(tags)}">
</form>
<script>
// Sync checkboxes to hidden tags input
document.getElementById('faceted-form').addEventListener('submit', function() {{
  var checked = Array.from(document.querySelectorAll('[name=tags_cb]:checked')).map(e => e.value);
  document.getElementById('tags-hidden').value = checked.join(',');
}});
</script>
<hr>
{results_html}
"""
        return _wrap_html("Faceted Search", body)


def _faceted_search(
    docs: list[dict],
    q: str,
    section: str = "",
    lang: str = "",
    tags: str = "",
) -> list[dict]:
    """Фасетный поиск: фильтрация + TF-IDF ранжирование по запросу.

    Args:
        docs: список записей из search_index.json
        q: текстовый запрос
        section: фильтр по первой части пути (e.g. "docs")
        lang: фильтр по языку (RU / EN / MIX / "")
        tags: строка тегов через запятую

    Returns:
        Список dict с полями: title, path, section, score, word_count, tags
    """
    # Normalize tag filter
    tag_set = {t.strip().lower() for t in tags.split(",") if t.strip()}

    # Step 1: filter
    filtered: list[dict] = []
    for d in docs:
        path = d.get("path", "")
        # section filter: match first path component
        if section:
            parts = path.split("/")
            doc_section = parts[0] if parts else ""
            if doc_section != section:
                continue
        # language filter
        if lang:
            doc_lang = (d.get("lang") or d.get("language") or "").upper()
            if doc_lang != lang.upper():
                continue
        # tags filter
        if tag_set:
            doc_tags = {t.lower() for t in d.get("tags", []) if isinstance(t, str)}
            if not tag_set.intersection(doc_tags):
                continue
        filtered.append(d)

    # Step 2: score by query (simple TF-IDF approximation: term frequency in content)
    q_lower = q.lower().strip()
    q_terms = q_lower.split() if q_lower else []

    def _score(d: dict) -> float:
        if not q_terms:
            return 0.0
        text = " ".join([
            d.get("title", "") * 3,  # title weight ×3 (repeat)
            d.get("content", ""),
            d.get("preview", ""),
        ]).lower()
        total = len(text.split()) or 1
        tf = sum(text.count(t) for t in q_terms)
        return tf / total

    # Step 3: build result records
    scored: list[dict] = []
    for d in filtered:
        score = _score(d)
        if q_terms and score == 0.0:
            continue
        path = d.get("path", "")
        parts = path.split("/")
        doc_section = parts[0] if len(parts) > 1 else ""
        scored.append({
            "title": d.get("title", ""),
            "path": path,
            "section": doc_section,
            "score": score,
            "word_count": d.get("word_count") or len((d.get("content") or "").split()),
            "tags": [t for t in d.get("tags", []) if isinstance(t, str)],
        })

    # Sort: by score desc, then title
    scored.sort(key=lambda x: (-x["score"], x["title"]))
    return scored[:50]


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


# ---------------------------------------------------------------------------
# Sprint 54-92 endpoint implementations
# ---------------------------------------------------------------------------


def _qbool(params: dict, key: str, default: bool = False) -> bool:
    raw = params.get(key, [""])[0].lower()
    if not raw:
        return default
    return raw in ("1", "true", "yes", "on")


def _qint(params: dict, key: str, default: int) -> int:
    try:
        return int(params.get(key, [str(default)])[0])
    except (ValueError, TypeError):
        return default


def _qstr(params: dict, key: str, default: str = "") -> str:
    return params.get(key, [default])[0]


def _api_ask(params: dict) -> dict:
    """Full-featured RAG via rag.ask() — every kwarg exposed as query string."""
    from docstoolkit.rag import ask

    q = _qstr(params, "q")
    if not q:
        return {"error": "missing q parameter"}

    kwargs = {
        "top_k":            _qint(params, "top_k", 5),
        "method":           _qstr(params, "method", "hybrid"),
        "answerer":         _qstr(params, "answerer", "echo"),
        "user_id":          _qstr(params, "user_id"),
        "with_facets":      _qbool(params, "with_facets"),
        "with_provenance":  _qbool(params, "with_provenance"),
        "self_rag":         _qbool(params, "self_rag"),
        "auto_intent":      _qbool(params, "auto_intent"),
        "hierarchical":     _qbool(params, "hierarchical"),
        "with_debate":      _qbool(params, "with_debate"),
        "with_mapreduce":   _qbool(params, "with_mapreduce"),
        "with_got":         _qbool(params, "with_got"),
        "with_negotiation": _qbool(params, "with_negotiation"),
        "at_commit":        _qstr(params, "at_commit"),
    }
    # Filters via simple "field:value,field2:value2" form
    raw_filters = _qstr(params, "filters")
    if raw_filters:
        flt: dict[str, str] = {}
        for part in raw_filters.split(","):
            if ":" in part:
                k, v = part.split(":", 1)
                flt[k.strip()] = v.strip()
        kwargs["filters"] = flt

    try:
        r = ask(q, **kwargs)
    except Exception as e:
        return {"error": str(e)}

    out = {
        "query": q,
        "answer": r.answer,
        "duration_ms": r.duration_ms,
        "passages": [
            {"doc_id": p.doc_id, "title": p.title, "score": p.score}
            for p in r.retrieved_passages
        ],
        "citations": r.citations,
    }
    if r.facets:
        out["facets"] = [a.to_dict() for a in r.facets]
    if r.provenance is not None:
        try:
            out["provenance"] = {
                "overall_confidence": r.provenance.overall_confidence,
                "n_claims": len(r.provenance.claims),
            }
        except Exception:
            pass
    if r.got_result is not None:
        try:
            out["got"] = {
                "final_answer": r.got_result.final_answer,
                "confirmed": r.got_result.confirmed_count,
                "refuted": r.got_result.refuted_count,
            }
        except Exception:
            pass
    if r.at_commit:
        out["at_commit"] = r.at_commit
    # Phase III.3 — opt-in composition trace via ?trace=1
    if _qbool(params, "trace") and r.trace:
        out["trace"] = [
            {"stage": ev.stage,
             "t_ms": round(ev.t_ms, 4),
             "payload": ev.payload}
            for ev in r.trace
        ]
    return out


def _api_eval_dashboard(params: dict) -> str:
    from docstoolkit.online_eval import OnlineEvalStore, render_dashboard
    days = _qint(params, "days", 7)
    store = OnlineEvalStore()
    try:
        return render_dashboard(store, window_days=days)
    finally:
        store.close()


def _api_saved_list(params: dict) -> dict:
    from docstoolkit.rag.saved import list_queries
    owner = _qstr(params, "owner")
    qs = list_queries(owner=owner)
    return {
        "owner": owner,
        "queries": [
            {"id": q.id, "query": q.query, "owner": q.owner,
             "schedule": q.schedule, "top_k": q.top_k}
            for q in qs
        ],
        "total": len(qs),
    }


def _api_voice(params: dict) -> dict:
    from docstoolkit.rag.advanced import measure_voice
    text = _qstr(params, "text")
    if not text:
        return {"error": "missing text parameter"}
    return {"text_length": len(text), "voice": measure_voice(text)}


def _api_assets(params: dict) -> dict:
    from docstoolkit.rag.advanced import search_assets
    q = _qstr(params, "q")
    asset_type = _qstr(params, "type")
    tag = _qstr(params, "tag")
    assets = search_assets(q, asset_type=asset_type, tag=tag)
    return {"query": q, "type": asset_type, "tag": tag,
            "assets": assets, "total": len(assets)}


def _api_taxonomy(params: dict) -> dict:
    from docstoolkit.rag.advanced import build_taxonomy_ask
    q = _qstr(params, "q")
    if not q:
        return {"error": "missing q parameter"}
    levels = _qint(params, "levels", 3)
    top_k = _qint(params, "top_k", 25)
    return build_taxonomy_ask(q, top_k=top_k, levels=levels)


def _api_diff(params: dict) -> dict:
    """Bulk diff between two git commits within the active docs_dir."""
    from pathlib import Path as _P
    from docstoolkit.rag.bulk_diff import diff_commits, diff_since_days

    days = params.get("days", [""])[0]
    a = _qstr(params, "from")
    b = _qstr(params, "to", "HEAD")
    docs_dir = getattr(DocsHandler.cfg, "docs_dir", _P("docs"))
    try:
        if days:
            res = diff_since_days(docs_dir, int(days))
        elif a and b:
            res = diff_commits(docs_dir, a, b)
        else:
            return {"error": "specify from+to or days parameter"}
    except Exception as e:
        return {"error": str(e)}
    return {
        "added": res.added,
        "removed": res.removed,
        "modified": res.modified,
        "total_changes": res.total_changes,
    }


def _api_kg(params: dict) -> dict:
    """KG stats and entity-based search."""
    from docstoolkit.knowledge_graph import KGRetriever

    kgr = KGRetriever()
    q = _qstr(params, "q")
    if q:
        hits = kgr.search(q, top_k=_qint(params, "top_k", 5))
        return {
            "query": q,
            "stats": kgr.stats(),
            "passages": [
                {"doc_id": p.doc_id, "title": p.title, "score": p.score}
                for p in hits
            ],
        }
    return {"stats": kgr.stats()}


def _api_profile(params: dict) -> dict:
    """Load or list user profiles."""
    from docstoolkit.conversation.profile import ProfileStore

    store = ProfileStore()
    try:
        user_id = _qstr(params, "user_id")
        if user_id:
            p = store.load(user_id)
            if p is None:
                return {"user_id": user_id, "exists": False}
            return {
                "user_id": p.user_id,
                "exists": True,
                "interests": p.interests,
                "preferred_sections": p.preferred_sections,
                "preferred_retriever": p.preferred_retriever,
                "read_docs_count": len(p.read_docs),
            }
        return {"users": store.list_users()}
    finally:
        store.close()
