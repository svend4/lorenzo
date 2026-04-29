# API Reference — docs-toolkit

Краткий справочник по public API всех 25 функциональных модулей. Полный обзор — в [`README.md`](README.md), детальный roadmap — в [`../docs/ROADMAP/`](../docs/ROADMAP/).

**Версия:** Unreleased (готовится 0.2.0). 53 спринта реализовано.

---

## Содержание

- [RAG / Retrieval](#rag--retrieval)
- [Agent / Reasoning](#agent--reasoning)
- [Workflow / Orchestration](#workflow--orchestration)
- [Memory / Conversation](#memory--conversation)
- [Eval / A/B / Feedback](#eval--ab--feedback)
- [Governance / Auth / Budget / Prompts](#governance--auth--budget--prompts)
- [Observability / Telemetry](#observability--telemetry)
- [Integration / Federation / Webhooks](#integration--federation--webhooks)
- [Storage / VectorDB / Cache](#storage--vectordb--cache)
- [Utilities](#utilities)

---

## RAG / Retrieval

### `docstoolkit.rag`

```python
from docstoolkit.rag import ask, Retriever
from docstoolkit.rag.types import Passage, RAGQuery, AnswerResult

result: AnswerResult = ask(
    "вопрос",
    top_k=5, method="hybrid", answerer="echo",
    model="claude-haiku-4-5-20251001",
)
# result.answer, result.citations, result.duration_ms, result.tokens_used, result.cost_estimate
```

**Methods:** `keyword`, `bm25`, `semantic` (опц.), `hybrid` (RRF), `adaptive`
**Answerers:** `echo`, `anthropic`, `openai`, `ollama`

### `docstoolkit.rag.streaming`

```python
from docstoolkit.rag.streaming import stream_rag, StreamChunk

for chunk in stream_rag("вопрос?", answerer="anthropic"):
    if chunk.type == "passages_retrieved":
        print(f"Found {chunk.data['count']} passages")
    elif chunk.type == "token":
        print(chunk.data["text"], end="")
    elif chunk.type == "done":
        print(f"\nDone in {chunk.data['duration_ms']}ms")
    elif chunk.type == "error":
        print(f"Error: {chunk.data['msg']}")
```

### `docstoolkit.rag.adaptive`

```python
from docstoolkit.rag.adaptive import adaptive_search, AdaptiveResult

result: AdaptiveResult = adaptive_search(
    "запрос",
    top_k=5, max_hops=3,
    confidence_threshold=0.65,
    method="hybrid",
)
print(result.to_markdown())
# result.hops, result.final_passages, result.final_confidence, result.halted_reason
```

---

## Agent / Reasoning

### `docstoolkit.agent`

```python
from docstoolkit.agent import AgentLoop, Tool, AgentResult

tools = [
    Tool(name="search", fn=my_search, description="Поиск",
         input_schema={"type": "object", "properties": {...}}),
]
agent = AgentLoop(tools=tools, llm="echo", max_iterations=5)
result: AgentResult = agent.run("задача")
# result.answer, result.steps, result.total_tool_calls, result.total_cost
```

### `docstoolkit.agent.planner` (Sprint 50)

```python
from docstoolkit.agent import (
    plan_and_execute, heuristic_planner, execute_plan,
    Plan, Subtask, PlanExecuteResult,
)

# Один-шот:
result: PlanExecuteResult = plan_and_execute(
    "1) найти Yodoca 2) сделать резюме 3) контакт автора",
    agent=my_agent,                # опц.; default echo-executor
    max_replans=1,
)
print(result.to_markdown())

# Раздельно:
plan: Plan = heuristic_planner("задача и подзадача")
result = execute_plan(plan, agent=my_agent,
                      on_subtask=lambda st, sr: print(st.id, sr.ok))
```

---

## Workflow / Orchestration

### `docstoolkit.workflow` (Sprint 47)

```python
from docstoolkit.workflow import Workflow, Step, run, run_async

wf = Workflow(name="rag-pipeline", steps=[
    Step("retrieve", fn=search,
         inputs={"q": "$.question"}),                 # context var
    Step("rerank", fn=rerank,
         inputs={"passages": "$.retrieve.output"}),   # step output
    Step("answer", fn=answer,
         inputs={"q": "$.question", "ps": "$.rerank.output"},
         on_error="retry", max_retries=2),
])

# Sync (sequential):
result = run(wf, {"question": "?"})

# Parallel (level-based):
result = run_async(wf, {"question": "?"}, max_workers=4)
# result.outputs[step_name], result.steps, result.failed, result.report()
```

**on_error:** `fail` (default) | `skip` | `retry`

### `docstoolkit.router` (Sprint 46)

```python
from docstoolkit.router import (
    ModelRouter, ModelChain, ModelHop, RouteResult, BUILTIN_CHAINS,
)

# Built-in:
chain = BUILTIN_CHAINS["balanced"]   # cheap | fast | balanced | high-quality | echo-only

# Custom:
chain = ModelChain(name="my", hops=[
    ModelHop(answerer="anthropic", model="claude-sonnet-4-6", max_retries=1),
    ModelHop(answerer="openai", model="gpt-4o-mini"),
    ModelHop(answerer="echo"),
])

r = ModelRouter(budget_check=lambda scope: True)  # opt budget gate
result: RouteResult = r.invoke(chain, system="...", user="...",
                                budget_scope="user:alice")
# result.answer, result.hop_used, result.errors, result.duration_ms
```

### `docstoolkit.jobs`

```python
from docstoolkit.jobs import Job, Worker, enqueue

enqueue("my_task", payload={"foo": 1})
# Worker poll'ит и обрабатывает
```

---

## Memory / Conversation

### `docstoolkit.conversation` (Sprint 49)

```python
from docstoolkit.conversation import ConversationStore, Session, Message

cs = ConversationStore()  # SQLite в .docstoolkit/conversations.sqlite

sid = cs.create_session(user="alice", title="RAG", skill="rag")
cs.append(sid, role="user", content="что такое RAG?")
cs.append(sid, role="assistant", content="...")

# Tail-fit к token budget:
msgs = cs.history_for_llm(sid, max_tokens=4000,
                          summarize_old=True,
                          system_prompt="You are helpful.")
# returns [{"role": ..., "content": ...}, ...]

# Сжать старые turns:
summary = cs.squash_old(sid, keep_last=4,
                        summarizer=lambda msgs: my_llm_summarize(msgs))
```

### `docstoolkit.cache`

```python
from docstoolkit.cache import Cache, cached

c = Cache(ttl_s=3600)
c.set("key", value)
c.get("key")

@cached(ttl_s=600)
def expensive():
    ...
```

---

## Eval / A/B / Feedback

### `docstoolkit.eval` (Sprint 48)

```python
from docstoolkit.eval import (
    GoldenItem, GoldenSet, run_eval, EvalResult,
    score_answer, score_citations, load_golden_from_yaml,
)

gset = GoldenSet(name="rag-baseline", items=[
    GoldenItem(
        question="что такое Yodoca?",
        expected_answer_contains=["memory", "hot path"],
        expected_doc_ids=["yodoca.md"],
        forbidden_phrases=["галлюцинация"],
        weight=1.0,
    ),
])
result: EvalResult = run_eval(gset, {"method": "hybrid", "answerer": "echo"})
print(result.report())
# result.overall_score, result.avg_answer_score, result.avg_citation_f1
```

### `docstoolkit.experiments` (Sprint 44)

```python
from docstoolkit.experiments import (
    Experiment, ExperimentResult, run_experiment, run_variant,
)

exp = Experiment(
    name="hybrid-vs-keyword",
    variants=[
        {"name": "control", "method": "keyword", "answerer": "echo"},
        {"name": "treatment", "method": "hybrid", "answerer": "echo"},
    ],
    questions=["q1", "q2", "q3"],
)
result: ExperimentResult = run_experiment(exp)
print(result.compare())  # markdown с Verdict (Fastest/Cheapest/Speed delta)
```

### `docstoolkit.feedback` (Sprint 43)

```python
from docstoolkit.feedback import FeedbackStore, Feedback

fs = FeedbackStore()
fs.record(Feedback(
    request="что?", response_text="это.",
    thumbs="up", rating=5, skill="rag",
))

# Wilson confidence interval:
score = fs.quality_score(skill="rag")    # 0-100
agg = fs.aggregate_per_skill()           # {skill: {total, up, down, quality_score}}
recent = fs.list_recent(limit=20, skill="rag", thumbs="up")
```

---

## Governance / Auth / Budget / Prompts

### `docstoolkit.auth` (Sprint 39)

```python
from docstoolkit.auth import User, Scope, check_scope

# Wildcard scopes:
u = User(id="alice", scopes=["rag:*", "feedback:read"])
check_scope(u, "rag:ask")        # True
check_scope(u, "admin:delete")   # False
```

### `docstoolkit.budget` (Sprint 45)

```python
from docstoolkit.budget import (
    BudgetTracker, BudgetRule, BudgetStatus, BudgetExceeded,
)

bt = BudgetTracker()
bt.set_rule(BudgetRule(scope="user:alice", period="day",
                        limit_usd=1.0, warn_at=0.8))

# Перед LLM-вызовом:
status: BudgetStatus = bt.check("user:alice")
if not status.ok:
    raise BudgetExceeded(status.reason)
# Или: bt.enforce("user:alice")  → raises if blocked

# После вызова:
bt.record(scope="user:alice", model="claude-haiku-4-5",
          tokens_in=100, tokens_out=50, cost=0.002)

# Аналитика:
top = bt.top_spenders(period="day", limit=10)
breakdown = bt.per_model_breakdown(period="month")
md = bt.report_markdown(period="day")
```

### `docstoolkit.prompts` (Sprint 51)

```python
from docstoolkit.prompts import Prompt, PromptLibrary, PromptRenderError

lib = PromptLibrary(rng_seed=42)  # deterministic A/B picks
lib.register(Prompt(
    id="rag.system", version=1,
    template="Ты помощник. Контекст:\n{context}\n\nВопрос: {question}",
))

# Render (with strict mode):
text, used = lib.render("rag.system", {"context": "...", "question": "?"})
# raises PromptRenderError on missing/unknown placeholders

# A/B variants:
lib.register(Prompt(id="rag.system", version=2, template="..."))
lib.set_active_variant("rag.system", version=1, weight=0.5,
                        additional=[(2, 0.5)])

# Persistence:
lib.save(Path("prompts.json"))
lib2 = PromptLibrary(path=Path("prompts.json"))
```

### `docstoolkit.skills`

```python
from docstoolkit.skills import Skill, SkillTestSuite

# discovery:
from docstoolkit.skills.testing import test_skill, run_all_tests

results = run_all_tests(skills_dir=".claude/skills")
```

---

## Observability / Telemetry

### `docstoolkit.telemetry` (Sprint 41)

```python
from docstoolkit.telemetry import tracer, meter, prometheus_format
from docstoolkit.telemetry.metrics import Counter, Histogram, Gauge

# Tracing:
with tracer.span("rag.search") as s:
    s.set_attribute("top_k", 5)
    ...

# Metrics:
c = meter.counter("rag_calls_total", "RAG ask invocations")
c.inc()

h = meter.histogram("rag_duration_seconds",
                     buckets=[0.01, 0.1, 1.0, 10.0])
h.observe(0.42)

g = meter.gauge("active_sessions")
g.set(7)

# Expose:
print(prometheus_format())
```

### `docstoolkit.serve`

HTTP endpoints (запуск: `docstoolkit serve --port 8080`):

| Endpoint | Method | Описание |
|----------|--------|----------|
| `/api/ask` | GET | Sync RAG (`?q=...&top_k=5`) |
| `/api/stream/rag` | POST | SSE streaming (Sprint 42) |
| `/api/feedback` | POST | Record feedback |
| `/metrics` | GET | Prometheus exposition |
| `/api/skills` | GET | List skills |
| `/api/health` | GET | Health check |

---

## Integration / Federation / Webhooks

### `docstoolkit.federation` (Sprint 36)

```python
from docstoolkit.federation import Peer, query_peers, merge_results

peers = [Peer(url="http://node-a:8080"), Peer(url="http://node-b:8080")]
results = query_peers(peers, "запрос", top_k=5)
merged = merge_results(results)  # RRF
```

### `docstoolkit.events` (Sprint 37)

```python
from docstoolkit.events import EventBus

bus = EventBus()
bus.subscribe("job.*", lambda evt: print(evt))
bus.publish("job.completed", {"job_id": "x", "status": "ok"})
```

### `docstoolkit.webhooks` (Sprint 52)

```python
from docstoolkit.webhooks import (
    WebhookDispatcher, Subscription, Delivery, DeliveryStatus,
    sign_payload,
)

wh = WebhookDispatcher(max_retries=3)

wh.subscribe(Subscription(
    url="https://hooks.example.com/lorenzo",
    events=["job.*", "feedback.received"],
    secret="hmac-key",
))

deliveries: list[Delivery] = wh.dispatch(
    event="job.completed",
    payload={"job_id": "x"},
)
# delivery.status: pending | sent | failed | dead

# Retry logic (cron job):
wh.retry_failed(max_to_retry=50)

# Stats:
print(wh.stats())
# {subscriptions, active_subscriptions, deliveries_pending/sent/failed/dead}
```

---

## Storage / VectorDB / Cache

### `docstoolkit.embeddings`

```python
from docstoolkit.embeddings import (
    Embedder, TFIDFProvider, SentenceTransformersProvider,
    HybridSearcher, EmbeddingsCache,
)

cache = EmbeddingsCache()       # SQLite persistent

p = TFIDFProvider(cache=cache)
p.fit(documents)
vec = p.encode("query")

# Hybrid search:
hs = HybridSearcher(provider=p, alpha=0.6)
hs.fit(documents)
results = hs.search("query", top_k=5)
```

### `docstoolkit.vectordb` (Sprint 40)

```python
from docstoolkit.vectordb import VectorDB, get_vectordb

# Discovery via entry_points:
db = get_vectordb("memory")  # или "sqlite-vec", "qdrant" (если установлен)
db.upsert(id="d1", vector=[...], metadata={...})
results = db.query(vector=[...], top_k=5)
```

### `docstoolkit.timetravel` (Sprint 41)

```python
from docstoolkit.timetravel import query_at_commit, bisect_corpus

# Запрос как было в commit X:
result = query_at_commit("когда появился RAG?", commit="abc123")

# Найти первый commit где X появилось:
commit = bisect_corpus(predicate=lambda corpus: "X" in corpus.read())
```

### `docstoolkit.cluster`

```python
from docstoolkit.cluster import cluster_embeddings

clusters = cluster_embeddings(vectors, k=5, method="kmeans++")
# returns dict[cluster_id, list[doc_id]]
```

---

## Utilities

### `docstoolkit.config`

```python
from docstoolkit.config import load_config, Config

cfg: Config = load_config()  # читает docstoolkit.toml
print(cfg.root, cfg.docs_dir, cfg.templates_dir)
```

### `docstoolkit.frontmatter`

```python
from docstoolkit.frontmatter import parse_yaml, extract_frontmatter

fm, body = extract_frontmatter(text)
# fm: dict | None, body: str
```

### `docstoolkit.lang`

```python
from docstoolkit.lang import detect_language

lang = detect_language("текст на русском")  # "ru"
lang = detect_language("english text")       # "en"
```

### `docstoolkit.graph`

```python
from docstoolkit.graph import build_graph, to_dot, to_mermaid

g = build_graph(corpus_dir)
dot_str = to_dot(g)
mermaid_str = to_mermaid(g)
```

### `docstoolkit.web`

```python
from docstoolkit.web import fetch_url, extract_main

html = fetch_url("https://example.com")
text = extract_main(html)
```

### `docstoolkit.ingest`

```python
from docstoolkit.ingest import load_markdown, load_pdf, load_multimodal

docs = load_markdown(Path("docs/"))
pdf_text = load_pdf(Path("file.pdf"))
mm_meta = load_multimodal(Path("image.png"))  # Sprint 38
```

---

## CLI команды

| Команда | Описание |
|---------|----------|
| `docstoolkit init` | Создать `docstoolkit.toml` |
| `docstoolkit doc new --type X --slug Y --vars k=v` | Создать документ из шаблона |
| `docstoolkit doc validate [--section X]` | Валидация по JSON Schema |
| `docstoolkit doc list-templates` | Список шаблонов |
| `docstoolkit ingest <path>` | Загрузить документы в индекс |
| `docstoolkit search <query>` | Поиск по индексу |
| `docstoolkit serve [--port 8080]` | Запустить HTTP server |
| `docstoolkit doctor` | Health check |
| `docstoolkit plugins list` | Список плагинов |
| `docstoolkit plugins inspect <name>` | Детали плагина |
| `docstoolkit index build/update/clear/stats` | Управление persistent embeddings cache |
| `docstoolkit skills list` | Список Claude скиллов |
| `docstoolkit skills test [name]` | Запуск golden tests для скиллов |

---

## Тестирование

```bash
pytest tests/                       # 546 тестов
pytest tests/test_rag.py -v         # один модуль
pytest tests/ -k "adaptive"         # по pattern
pytest tests/ --cov=docstoolkit     # с coverage
```

Также:
```bash
python ../scripts/improve_mcp_test.py             # MCP integrity (30/30)
python ../scripts/improve_template_integrity.py   # шаблоны (23/23)
```

---

## Roadmap

35 идей развития × 4 уровня сложности — в [`../docs/ROADMAP/`](../docs/ROADMAP/):

- [00-CURRENT-STATE](../docs/ROADMAP/00-CURRENT-STATE.md) — что есть сейчас, что не умеет
- [01-SIMPLE](../docs/ROADMAP/01-SIMPLE.md) — простые улучшения (1-3 спринта)
- [02-MEDIUM](../docs/ROADMAP/02-MEDIUM.md) — mainstream RAG улучшения
- [03-INNOVATIVE](../docs/ROADMAP/03-INNOVATIVE.md) — frontier research
- [04-NOVEL](../docs/ROADMAP/04-NOVEL.md) — никем не сделанные концепции
- [05-PRIORITIES](../docs/ROADMAP/05-PRIORITIES.md) — 3 пути с конкретными первыми спринтами

---

## Связанные документы

- [`README.md`](README.md) — обзор пакета + quick start
- [`CHANGELOG.md`](CHANGELOG.md) — изменения по версиям
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — как контрибьютить
- [`SECURITY.md`](SECURITY.md) — security policy + best practices
- [`RELEASE.md`](RELEASE.md) — процесс релиза
