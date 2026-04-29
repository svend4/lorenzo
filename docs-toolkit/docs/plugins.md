# Plugin development

`docs-toolkit` поддерживает 6 типов plugin'ов через PEP 621 entry_points.

## Группы

| Группа | Что регистрирует |
|---|---|
| `docstoolkit.skills` | Callable → Path к директории со скилами |
| `docstoolkit.templates` | Callable → dict {name: {md, schema}} |
| `docstoolkit.ingest` | `ingest(path: Path) → Document` |
| `docstoolkit.embeddings` | Class наследник `EmbeddingProvider` |
| `docstoolkit.tasks` | YAML манифесты задач |
| `docstoolkit.commands` | CLI subcommands |

## Создание плагина

### 1. Структура пакета

```
my-pack/
├── pyproject.toml
└── my_pack/
    ├── __init__.py
    ├── ingest_csv.py
    └── embeddings_openai.py
```

### 2. pyproject.toml

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "docstoolkit-mypack"
version = "0.1.0"
dependencies = ["docs-toolkit>=0.1.0"]

[project.entry-points."docstoolkit.ingest"]
csv = "my_pack.ingest_csv:ingest"

[project.entry-points."docstoolkit.embeddings"]
openai-embed = "my_pack.embeddings_openai:OpenAIEmbedProvider"
```

### 3. Реализация (ingest)

```python
# my_pack/ingest_csv.py
from pathlib import Path
from docstoolkit.ingest.base import Document, IngestError, Source

def ingest(path: Path) -> Document:
    if not path.exists():
        raise IngestError(f"Не найден: {path}")
    text = path.read_text(encoding="utf-8")
    # ... парсинг ...
    return Document(
        title=path.stem,
        content=converted_markdown,
        source=Source.from_path(path, "csv"),
        metadata={"rows": ...},
    )
```

### 4. Реализация (embeddings)

```python
# my_pack/embeddings_openai.py
from docstoolkit.embeddings.base import EmbeddingProvider

class OpenAIEmbedProvider(EmbeddingProvider):
    name = "openai-embed"
    dim = 1536

    def __init__(self, model: str = "text-embedding-3-small"):
        from openai import OpenAI
        self._client = OpenAI()
        self.model = model

    def encode(self, texts):
        resp = self._client.embeddings.create(model=self.model, input=texts)
        return [d.embedding for d in resp.data]

    def similarity(self, query_vec, doc_vecs):
        # cosine similarity
        ...
```

### 5. Установка и использование

```bash
pip install -e ./my-pack
docstoolkit plugins list
# →
# docstoolkit.ingest: ['csv', 'markdown', 'html', ...]
# docstoolkit.embeddings: ['openai-embed', 'tfidf', ...]

docstoolkit ingest my_data.csv -o docs/
docstoolkit search "query" --provider openai-embed
```

## Auto-loading

При `import docstoolkit` автоматически вызывается `autoload_all()` который
подгружает все ingest и embeddings плагины из entry_points. Никакого ручного
импорта не требуется.

## Inspect

```bash
docstoolkit plugins inspect docstoolkit.ingest csv
# →
# {
#   "name": "csv",
#   "group": "docstoolkit.ingest",
#   "value": "my_pack.ingest_csv:ingest",
#   "package": "docstoolkit-mypack",
#   "version": "0.1.0",
#   "callable": true
# }
```

## Полный пример

См. `docs-toolkit/examples/example-plugin-pack/` — рабочий пример с 4 типами
плагинов (ingest, embeddings, skills, templates).
