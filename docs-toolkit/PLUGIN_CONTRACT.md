# docs-toolkit Plugin Contract

Спецификация, которой должен соответствовать сторонний плагин, чтобы
быть подключаемым к `docs-toolkit`. Документ касается двух уровней:

1. **Discovery** — как пакет регистрируется через `pyproject.toml` entry_points.
2. **Lifecycle** — какие методы плагин обязан/может имплементировать,
   чтобы участвовать в registry + sandbox.

Если вы пишете простой ингредиент (новый retriever, answerer, ingest
adapter, embedding provider) — достаточно уровня (1). Если вам нужны
явные `on_activate` / `on_deactivate` хуки и видимость в реестре —
используйте уровень (2).

---

## 1. Discovery через entry_points

### 1.1. Поддерживаемые группы

| Группа | Что регистрируется | Контракт |
|---|---|---|
| `docstoolkit.skills` | Skill-документ или модуль | См. `.claude/skills/` |
| `docstoolkit.templates` | Template-модуль с JSON Schema | См. `docstoolkit.template_engine` |
| `docstoolkit.ingest` | Ingest-функция `(path) → list[Document]` | См. `docstoolkit.ingest.dispatch` |
| `docstoolkit.embeddings` | Embedding-провайдер | См. `docstoolkit.embeddings.dispatch` |
| `docstoolkit.tasks` | Task-манифест | См. `tasks/*.task.yaml` |
| `docstoolkit.commands` | CLI команда `(args) → int` | См. `docstoolkit.cli` |
| `docstoolkit.retrievers` | Retriever (Phase VII addition) | См. §2.1 ниже |
| `docstoolkit.answerers` | Answerer (Phase VII addition) | См. §2.2 ниже |

### 1.2. Регистрация

```toml
# pyproject.toml вашего пакета
[project]
name = "docstoolkit-myplugin"
version = "0.1.0"

[project.entry-points."docstoolkit.ingest"]
notion = "docstoolkit_myplugin.notion:ingest"

[project.entry-points."docstoolkit.retrievers"]
qdrant = "docstoolkit_myplugin.retrievers.qdrant:QdrantRetriever"
```

После `pip install docstoolkit-myplugin` ваш плагин автоматически
обнаруживается через:

```python
from docstoolkit.plugins import discover, list_plugin_groups

print(list_plugin_groups())
# {'docstoolkit.ingest': ['markdown', 'notion'], ...}

for ep in discover("docstoolkit.retrievers"):
    print(ep.name, ep.value)
```

CLI:

```bash
docstoolkit plugins list
docstoolkit plugins inspect docstoolkit.retrievers qdrant
```

---

## 2. Контракты по группам

### 2.1. Retriever

```python
from typing import Protocol
from docstoolkit.rag.types import Passage


class Retriever(Protocol):
    """Phase VII contract for a retrieval plugin."""

    def search(self, query: str, top_k: int) -> list[Passage]:
        """Return up to top_k Passage objects ranked by relevance."""
        ...
```

**Минимальный пример:**

```python
# docstoolkit_myplugin/retrievers/qdrant.py
from docstoolkit.rag.types import Passage


class QdrantRetriever:
    def __init__(self, host="localhost", port=6333):
        from qdrant_client import QdrantClient
        self.client = QdrantClient(host=host, port=port)

    def search(self, query: str, top_k: int) -> list[Passage]:
        hits = self.client.search(...)
        return [
            Passage(text=h.payload["text"], doc_id=h.payload["doc_id"],
                    title=h.payload.get("title", ""), score=h.score)
            for h in hits
        ]
```

Использование:

```python
from docstoolkit.plugins import load

QdrantRetriever = load("docstoolkit.retrievers", "qdrant")
retriever = QdrantRetriever(host="my-qdrant")
# ...
```

### 2.2. Answerer

```python
class Answerer(Protocol):
    """Phase VII contract for an answer-generation plugin."""

    def answer(self, system: str, user: str,
               model: str = "") -> tuple[str, int, float]:
        """Return (answer_text, tokens_used, cost_usd)."""
        ...
```

### 2.3. Ingest adapter

```python
def ingest(path: str | Path) -> list[Document]:
    """Return list of Document with .text, .metadata, .source_id."""
    ...
```

См. `docstoolkit.ingest.dispatch` — каждый адаптер регистрируется
по имени, например `notion`, `confluence`, `gitlab`.

### 2.4. Embedding provider

```python
class EmbeddingProvider(Protocol):
    def fit(self, texts: list[str]) -> None: ...
    def embed(self, text: str) -> list[float]: ...
    def embed_batch(self, texts: list[str]) -> list[list[float]]: ...
```

См. `docstoolkit.embeddings.tfidf.TFIDFProvider` как референс.

---

## 3. Lifecycle (опциональный)

Если вашему плагину нужны явные `on_activate` / `on_deactivate` хуки,
используйте `Plugin` base class:

```python
from docstoolkit.plugin_system import Plugin, PluginMetadata, PluginStatus


class MyRetrieverPlugin(Plugin):
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="qdrant",
            version="0.1.0",
            tags=["retriever", "vector"],
            description="Qdrant vector-store retriever",
        )

    def on_activate(self) -> None:
        # Открыть connection pool, прогрузить индекс
        self.client = QdrantClient(...)

    def on_deactivate(self) -> None:
        self.client.close()
```

Регистрация в реестре:

```python
from docstoolkit.plugin_system import PluginManager

mgr = PluginManager()
mgr.register(MyRetrieverPlugin())
mgr.load("qdrant")
mgr.activate("qdrant")

print(mgr.active_plugins())  # ["qdrant"]
```

`PluginManager` отслеживает статус (`UNLOADED → LOADED → ACTIVE`),
зависимости между плагинами, и пишет audit-trail в SQLite.

---

## 4. Sandbox (изолированная активация)

Сторонний плагин может выполняться в sandbox с ограниченными
capability:

```python
from docstoolkit.plugin_sandbox import (
    SandboxPolicy, run_in_sandbox,
)

policy = SandboxPolicy(
    allow_filesystem_read=True,
    allow_filesystem_write=False,
    allow_subprocess=False,
    allow_network=False,
    max_memory_mb=512,
)

result = run_in_sandbox(plugin.activate, policy=policy)
```

`SandboxPolicy` — это набор capability-флагов; нарушение бросает
`SandboxViolation`. См. `docstoolkit/plugin_sandbox/sandbox.py` для
деталей реализации.

> **Замечание:** текущий sandbox — process-level (subprocess + resource
> limits). Для full security требуется container (`docker run --rm`),
> что предусмотрено в Phase VIII (Docker patterns).

---

## 5. Версионирование и совместимость

- Используйте **SemVer**. Major-bump публичного API plugin contract'а
  будет анонсирован в [`CHANGELOG.md`](CHANGELOG.md).
- Плагины могут указывать diapason совместимости:

```toml
[project]
dependencies = ["docs-toolkit >=0.3,<0.5"]
```

- Текущая стабильная версия plugin contract: **0.3.0** (2026-05-15).

---

## 6. Публикация

### 6.1. PyPI

Простейший путь — публиковать как обычный Python-пакет:

```bash
python -m build
twine upload dist/*
```

Пользователь устанавливает через `pip install docstoolkit-myplugin`.
Никакой ad-hoc регистрации не нужно — entry_points обнаруживаются
автоматически при `import docstoolkit`.

### 6.2. Marketplace registry (Phase VII.3, planned)

Будущее развитие: `docstoolkit plugins search <keyword>` + `docstoolkit
plugins install <name>` через централизованный реестр. Сейчас — только
PyPI.

---

## 7. Чек-лист публикуемого плагина

- [ ] `pyproject.toml` с `[project.entry-points."docstoolkit.<group>"]`
- [ ] Соответствие протоколу группы (`search()` / `answer()` / `ingest()` / ...)
- [ ] Тесты: minimum smoke-тест с stub-данными
- [ ] Документация: README с usage example
- [ ] Версия в SemVer
- [ ] Совместимость указана в `dependencies`
- [ ] CHANGELOG отслеживает breaking-changes
- [ ] (Опц.) Регистрация в `PluginRegistry` если нужны lifecycle hooks
- [ ] (Опц.) Декларация capability-флагов если требуется sandbox

---

*Документ актуален для версии 0.3.0 (2026-05-15).*
