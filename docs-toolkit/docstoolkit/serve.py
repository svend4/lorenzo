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
            elif path == "/metrics":
                # Prometheus exposition format
                try:
                    from docstoolkit.telemetry import prometheus_format
                    self._send(200, prometheus_format(),
                               "text/plain; version=0.0.4")
                except ImportError:
                    self._send(503, "telemetry not available", "text/plain")
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
