# Migrating to docs-toolkit

Гид для тех, кто уже пользуется LangChain, LlamaIndex или Haystack
и хочет попробовать `docs-toolkit`. Документ описывает 1-в-1 mapping
для базовых сценариев + где `docs-toolkit` идёт другим путём.

---

## 1. Quickstart-сравнение

### LangChain

```python
# LangChain
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI

vectordb = Chroma.from_documents(docs, OpenAIEmbeddings())
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(), retriever=vectordb.as_retriever(k=5)
)
answer = qa.run("Что такое RAG?")
```

### docs-toolkit

```python
# docs-toolkit
from docstoolkit.rag import ask

result = ask("Что такое RAG?", method="hybrid", top_k=5)
print(result.answer)
print(result.citations)
```

**Что изменилось:**
- Нет явного построения vector store — индекс собирается автоматически из
  `docs/` директории по конфигу `docstoolkit.toml`. Persisted в SQLite.
- Нет separate Embeddings класса — выбор провайдера через config
  (`tfidf` по умолчанию, `sentence-transformers` если установлен).
- Возвращается structured `AnswerResult`, а не plain string.

---

## 2. LlamaIndex → docs-toolkit

### LlamaIndex

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

docs = SimpleDirectoryReader("./docs").load_data()
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine(similarity_top_k=5)
response = query_engine.query("Что такое RAG?")
```

### docs-toolkit

```python
from docstoolkit.rag import ask

# .docstoolkit/embeddings.sqlite автоматически собирается из docs/
result = ask("Что такое RAG?", method="semantic", top_k=5)
```

Если нужен явный rebuild индекса:
```bash
docstoolkit index build       # full
docstoolkit index update      # incremental
docstoolkit index stats
```

---

## 3. Концептуальный mapping

| LangChain / LlamaIndex | docs-toolkit |
|---|---|
| `Document` | `docstoolkit.rag.types.Passage` |
| `VectorStore` | SQLite cache в `.docstoolkit/embeddings.sqlite` |
| `Retriever` | `docstoolkit.rag.retriever.Retriever` |
| `LLM` / `ChatModel` | `docstoolkit.rag.answerer.Answerer` (EchoAnswerer / AnthropicAnswerer / …) |
| `Chain` | `docstoolkit.rag.ask()` — единая функция, не классы |
| `Tool` / `AgentExecutor` | `docstoolkit.agent.ReActAgent` + `docstoolkit.task_planner.Planner` |
| `Memory` | `docstoolkit.memory.TieredMemory` (Sprint 74 / I5) |
| `Callbacks` | `result.trace` (Phase III.1) — post-hoc, не runtime hooks |
| `ContextualCompressionRetriever` | `ask(reranker=...)` (Sprint 59 / M2) |
| `MultiQueryRetriever` | `ask(self_rag=True)` (Sprint 70 / I1) — рефлективный re-query loop |
| `Self-querying retriever` | `ask(auto_intent=True)` (Sprint 68 / M4) |
| `ParentDocumentRetriever` | `ask(hierarchical=True)` (Sprint 67 / M3) |

---

## 4. Что у нас есть, чего нет в LangChain/LlamaIndex

| Возможность | docs-toolkit | Где |
|---|---|---|
| Provenance + bootstrap CI per claim | ✓ | `ask(with_provenance=True)` |
| Self-RAG reflective loop | ✓ | `ask(self_rag=True)` |
| Multi-agent debate | ✓ | `ask(with_debate=True)` |
| Graph-of-thoughts | ✓ | `ask(with_got=True)` |
| Negotiation auction broker | ✓ | `ask(with_negotiation=True)` |
| Cognitive-style personality rerank | ✓ | `ask(personality=...)` |
| Document metabolism (stale + propose-rewrite) | ✓ | `metabolism.propose_rewrite()` |
| Per-stage latency trace | ✓ | `result.trace` + `result.to_trace_markdown()` |
| Composition presets | ✓ | `ask_personalized / ask_high_quality / …` |
| Stdlib-only path | ✓ | TFIDFProvider + EchoAnswerer работают без deps |

---

## 5. Что у LangChain/LlamaIndex есть, чего нет у нас

| Возможность | Альтернатива в docs-toolkit |
|---|---|
| Cloud vector stores (Pinecone, Weaviate, Chroma) | SQLite local store. Vector DB подключение — non-goal (см. README §non-goals). |
| Streaming async generation | `docstoolkit.rag.streaming` (SSE via `/api/stream/rag`); внутренний loop пока sync. |
| LangGraph DAG-as-code | `docstoolkit.workflow_engine` + `workflow_v2` — YAML pipelines. |
| LangSmith trace dashboard | `result.trace` + Prometheus экспозиция через `/metrics`. |
| 300+ integrations | Plugin system через PEP 621 entry-points; пиши свой ингредиент за 50 строк. |

---

## 6. Шаги миграции

### Шаг 1: Установка

```bash
cd your-project
pip install -e path/to/docs-toolkit                # vendored
# или, когда выложат на PyPI:
# pip install docs-toolkit
```

### Шаг 2: Конфиг

Создать `docstoolkit.toml` в корне проекта:

```toml
[paths]
docs_dir = "./docs"
cache_dir = ".docstoolkit"

[index]
default_method = "hybrid"
embedding_provider = "tfidf"  # или "sentence-transformers"

[answerer]
default = "echo"              # "anthropic" / "openai" / "ollama"
model = "claude-haiku-4-5-20251001"
```

Или через CLI: `docstoolkit init`.

### Шаг 3: Replace `RetrievalQA.run()` → `ask()`

LangChain:
```python
answer_text = qa.run(question)
```

docs-toolkit:
```python
result = ask(question, top_k=5)
answer_text = result.answer
```

Если нужны citations отдельно — `result.citations` (список dict с `n`, `doc_id`,
`title`, `score`).

### Шаг 4: Подключить advanced-фичи постепенно

Не пытайтесь сразу включить все 17 kwargs. Начните с пресета:

```python
from docstoolkit.rag import ask_high_quality
result = ask_high_quality(question, top_k=5)
```

Затем посмотрите `result.to_trace_markdown()` — увидите, какие стадии
сколько занимают. Включайте дополнительные фичи под конкретные требования.

### Шаг 5: HTTP-доступ

Если у вас был отдельный сервер поверх LangChain:

```bash
docstoolkit serve            # default port 8083
# тестируйте:
curl 'http://localhost:8083/api/ask?q=Что+такое+RAG&top_k=5&trace=1'
```

Endpoints: `/api/ask`, `/api/eval/dashboard`, `/api/saved`, `/api/voice`,
`/api/assets`, `/api/taxonomy`, `/api/diff`, `/api/kg`, `/api/profile`.

OpenAI-compatible `/v1/chat/completions` — см. `docstoolkit/serve.py`.

---

## 7. Когда docs-toolkit вам _не_ подойдёт

- Если ваш стек уже на LangGraph и вы используете её DAG-as-code — не
  переписывайте.
- Если нужен managed vector store с горизонтальным шардингом — это явно
  non-goal docs-toolkit.
- Если корпус — не markdown / не файловая система — нужно писать свой
  ingest plugin (поддерживаем pdf/epub/docx/html/jupyter; YAML, JSON,
  CSV — не из коробки).
- Если хотите LangSmith-style production observability — `result.trace`
  плюс Prometheus `/metrics`; полноценного hosted трейс-store нет.

---

## 8. Помощь

- `examples/composition/` — 8 runnable demo-скриптов
- `COOKBOOK.md` — 10 рецептов по задачам
- `PROFILES.md` — полный feature-индекс
- `ARCHITECTURE.md` — слои и точки расширения
- GitHub Issues — для багов и фич-запросов

---

*Документ актуален для версии 0.3.0 (2026-05-15).*
