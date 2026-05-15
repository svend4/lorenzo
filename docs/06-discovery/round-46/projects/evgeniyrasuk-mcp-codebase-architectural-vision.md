# MCP-сервер для кодовой базы: Tree-sitter + sqlite-vec + архитектурное зрение LLM

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** EvgeniyRasyuk  
**Хабр:** https://habr.com/ru/articles/948002/  
**GitHub:** нет (архитектура описана детально)  
**Слой:** orchestration / knowledge  
**Дата:** сентябрь 2025  
**Уникальность:** Не просто RAG: MCP-сервер с трёхслойным retrieval (Tree-sitter AST → sqlite-vec → local embeddings) даёт LLM "архитектурное зрение" над кодовой базой. 13 специализированных MCP-инструментов: semantic search, dependency tracing, refactoring suggestions. 5.5x быстрее нативного анализа Claude (55.84с → <10с), индексация 100+ файлов/сек, latency <100мс, RAM ~65 МБ. Всё локально без облачных API.

## Проблема: LLM не понимает архитектуру кодовой базы

```
Стандартный подход: дать LLM весь код в контекст
  → Большие проекты (1000+ файлов): не помещается в контекст
  → Нет понимания зависимостей: "что сломается если изменить IUserService?"
  → Нет семантического поиска: нельзя найти "код который делает X"
  → Claude нативный анализ больших repo: ~56 секунд, часто прерывается

Задача:
  → Дать LLM структурированное знание об архитектуре, а не сырой код
  → Ответы на вопросы типа: "что зависит от этого компонента?"
  → Быстрый semantic search по смыслу, не по строкам
  → Работать локально: не слать приватный код в облако

Решение: MCP-сервер как "архитектурная память" кодовой базы
```

## Трёхслойная архитектура retrieval

```python
# EvgeniyRasyuk: MCP-сервер с архитектурным зрением
# habr.com/ru/articles/948002

from pathlib import Path
import sqlite3
import json
from dataclasses import dataclass

@dataclass
class CodeEntity:
    """Единица кода: класс, функция, интерфейс, модуль."""
    entity_type: str     # "class", "function", "interface", "module"
    name: str
    file_path: str
    line_start: int
    line_end: int
    dependencies: list[str]   # что импортирует/вызывает
    dependents: list[str]     # кто импортирует/вызывает это
    embedding: list[float]    # semantic embedding для поиска
    ast_hash: str             # hash AST для incremental update


class CodebaseKnowledgeGraph:
    """
    Слой 1: Tree-sitter AST parsing → граф сущностей кода.
    Слой 2: sqlite-vec → векторный поиск по embedding.
    Слой 3: local embeddings (@xenova/transformers) — без облака.
    """

    def __init__(self, db_path: str = "codebase.db"):
        self.db = sqlite3.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        """SQLite + sqlite-vec extension для векторного поиска."""
        self.db.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS entities_vec
            USING vec0(embedding float[384])
        """)
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY,
                entity_type TEXT,
                name TEXT,
                file_path TEXT,
                line_start INTEGER,
                line_end INTEGER,
                dependencies TEXT,  -- JSON list
                dependents TEXT,    -- JSON list
                ast_hash TEXT
            )
        """)
        self.db.execute("""
            CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)
        """)


class TreeSitterParser:
    """
    Слой 1: Tree-sitter (WebAssembly) для AST parsing.
    Поддерживает: TypeScript, Python, Go, Rust, Java, Kotlin, C++.
    """

    def parse_file(self, file_path: Path) -> list[CodeEntity]:
        """
        Извлечь все сущности из файла через AST.
        Не regex: точный парсинг с пониманием синтаксиса.
        """
        language = self._detect_language(file_path)
        tree = self._parse_with_treesitter(file_path, language)

        entities = []
        for node in self._traverse(tree.root_node):
            if node.type in ("class_declaration", "function_definition",
                             "interface_declaration", "method_definition"):
                entities.append(CodeEntity(
                    entity_type=node.type.replace("_declaration", "").replace("_definition", ""),
                    name=self._extract_name(node),
                    file_path=str(file_path),
                    line_start=node.start_point[0],
                    line_end=node.end_point[0],
                    dependencies=self._extract_imports(node, tree),
                    dependents=[],  # заполняется на втором проходе
                    embedding=[],   # заполняется SemanticAgent
                    ast_hash=self._hash_node(node)
                ))

        return entities

    def _detect_language(self, file_path: Path) -> str:
        suffix_map = {
            ".ts": "typescript", ".tsx": "typescript",
            ".py": "python", ".go": "go",
            ".rs": "rust", ".java": "java",
            ".kt": "kotlin", ".cpp": "cpp"
        }
        return suffix_map.get(file_path.suffix, "unknown")
```

## Multi-agent пайплайн индексации

```python
class CodebaseIndexingPipeline:
    """
    Четыре специализированных агента работают последовательно.
    Каждый агент отвечает за свой слой знания.
    """

    AGENTS = {
        "CollectorAgent": {
            "role": "Сканирование файлов, фильтрация, приоритизация",
            "output": "Список файлов для индексации + изменённые с прошлого раза",
            "speed": "100+ файлов/сек"
        },
        "AnalysisAgent": {
            "role": "Tree-sitter AST parsing → call graphs + inheritance",
            "output": "Граф зависимостей: кто вызывает кого",
            "key_capability": "Точный dependency tracing без regex"
        },
        "SemanticAgent": {
            "role": "Генерация embeddings для всех сущностей",
            "model": "all-MiniLM-L6-v2 (@xenova/transformers, WASM локально)",
            "output": "Векторы в sqlite-vec для семантического поиска"
        },
        "RefactoringAgent": {
            "role": "Анализ дублирования + complexity metrics",
            "output": "Список кандидатов на рефакторинг"
        }
    }

    def index_codebase(self, project_path: Path,
                         incremental: bool = True) -> dict:
        """
        Полная индексация или инкрементальное обновление.
        incremental=True: пересоздать только изменённые сущности.
        """
        # CollectorAgent: найти файлы
        files = self._collect_agent(project_path, incremental)

        # AnalysisAgent: AST + граф зависимостей
        entities = []
        for file in files:
            entities.extend(self._analysis_agent(file))
        dep_graph = self._build_dependency_graph(entities)

        # SemanticAgent: embeddings
        for entity in entities:
            entity.embedding = self._semantic_agent(entity)

        # Сохранить в SQLite + sqlite-vec
        self._persist(entities)

        return {
            "indexed_files": len(files),
            "entities": len(entities),
            "indexing_speed": "100+ файлов/сек"
        }
```

## 13 MCP-инструментов: интерфейс для LLM

```python
# MCP-инструменты: что видит LLM при подключении к серверу

MCP_TOOLS = [
    {
        "name": "semantic_search",
        "description": "Найти сущности кода по смыслу (embedding similarity)",
        "example_query": "authentication middleware",
        "returns": "Топ-N сущностей с score + location"
    },
    {
        "name": "get_dependencies",
        "description": "Что импортирует/вызывает данная сущность",
        "example_query": "UserService",
        "returns": "Дерево зависимостей (прямых и транзитивных)"
    },
    {
        "name": "get_dependents",
        "description": "Кто зависит от данной сущности (impact analysis)",
        "example_query": "IUserService",
        "returns": "Список сущностей + где они используются — что сломается при изменении"
    },
    {
        "name": "find_duplicates",
        "description": "Семантически похожий код (кандидаты на DRY рефакторинг)",
        "example_query": "validation logic",
        "returns": "Пары сущностей с similarity score"
    },
    {
        "name": "get_complexity_hotspots",
        "description": "Файлы/функции с высокой цикломатической сложностью",
        "returns": "Топ-N по complexity + рекомендации"
    },
    {
        "name": "trace_call_path",
        "description": "Путь вызовов от A до B через граф",
        "example_query": "от API endpoint до Database layer",
        "returns": "Цепочка вызовов с кодом каждого шага"
    }
    # + 7 дополнительных инструментов
]

PERFORMANCE_BENCHMARK = {
    "vs_native_claude": {
        "task": "Анализ архитектуры 500-файлового TypeScript проекта",
        "native_claude": "55.84 сек (часто прерывается на context overflow)",
        "mcp_server": "< 10 сек (< 100мс на запрос из pre-built индекса)",
        "speedup": "5.5x"
    },
    "indexing": {
        "speed": "100+ файлов/сек",
        "incremental": "Только изменённые файлы (git diff awareness)"
    },
    "memory": "~65 MB RAM (SQLite + sqlite-vec индекс)",
    "query_latency": "< 100 мс",
    "privacy": "100% локально: Tree-sitter WASM + local embeddings"
}
```

## Сравнение подходов

```python
APPROACH_COMPARISON = {
    "vector_db_neo4j": {
        "pros": "Мощный граф запросов",
        "cons": "Тяжёлый, отдельный сервис, overhead для небольших проектов",
        "когда": "Enterprise проекты с 10K+ сущностей"
    },
    "sqlite_vec": {
        "pros": "Лёгкий (extension для SQLite), zero infra, embedded",
        "cons": "Хуже масштабируется за 100K+ векторов",
        "когда": "Локальные проекты до 50K сущностей — выбор автора"
    },
    "regex_parsing": {
        "pros": "Быстро, без зависимостей",
        "cons": "Ломается на сложных конструкциях (декораторы, дженерики)",
        "когда": "Только для примитивного grep"
    },
    "tree_sitter": {
        "pros": "Точный AST, поддержка 40+ языков, WebAssembly",
        "cons": "Чуть медленнее regex на простых случаях",
        "когда": "Production — выбор автора"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: архитектурное зрение для scripts/ кодовой базы

class LorenzoCodebaseVision:
    """
    EvgeniyRasyuk паттерн для Lorenzo:
    MCP-сервер над scripts/ — дать LLM знание об архитектуре скриптов.
    "Что использует improve_search_index.py?"
    "Какие скрипты зависят от CardStore?"
    "Найди все скрипты работающие с CONTACTS.md"
    """

    def index_scripts(self, scripts_path: str = "scripts/") -> dict:
        """
        Проиндексировать все 159 скриптов improve_*.py.
        Результат: граф зависимостей + semantic search по функциям.
        """
        pipeline = CodebaseIndexingPipeline()
        return pipeline.index_codebase(
            Path(scripts_path),
            incremental=True
        )

    def find_scripts_using(self, module: str) -> list[str]:
        """
        Dependency analysis: какие скрипты импортируют данный модуль?
        Аналог get_dependents для improve_*.py архитектуры.
        """
        return self._query_dependents(module)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Code MCP + LangGraph (R44)** | LangGraph граф с узлами-инструментами MCP: code search → dependency trace → refactor suggest |
| **Code MCP + Kaspersky MCP (R40)** | Два MCP-сервера: code архитектура + security analysis = полный DevSecOps ассистент |
| **Code MCP + LLM Observability (R45)** | Трассировать какие MCP-инструменты LLM вызывает при code review — понять стратегию |
| **Code MCP + LoRA Embeddings (R44)** | LoRA-дообученные embeddings специализированно на кодовой базе → лучший semantic search |
| **Code MCP + Lorenzo Gateway** | /api/ask понимает вопросы об архитектуре scripts/ через MCP + retrieval |

## Контакт

- Статья: https://habr.com/ru/articles/948002/ (сентябрь 2025)
- Автор: EvgeniyRasyuk (Хабр)
- Tree-sitter: tree-sitter.github.io
- sqlite-vec: github.com/asg017/sqlite-vec
- @xenova/transformers: github.com/xenova/transformers.js
- Смежная (Kaspersky MCP security, R40): docs/06-discovery/round-40/
- Смежная (AgentFS файловый MCP, R05): docs/06-discovery/round-05/
- Смежная (LLM DevSecOps, R34): docs/06-discovery/round-34/
