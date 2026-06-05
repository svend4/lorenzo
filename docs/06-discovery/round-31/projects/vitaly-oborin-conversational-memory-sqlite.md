# Научил ИИ-агента помнить важное и забывать лишнее в SQLite

> [!IMPORTANT]
> Ключевой документ для понимания архитектуры. Рекомендуется прочитать в первую очередь.

<!-- alert-added -->

**Автор:** VitalyOborin (Хабр, март 2025)  
**Хабр:** https://habr.com/ru/articles/1006622/  
**GitHub:** VitalyOborin (автор Yodoca + Wikontic, контакт уже в базе Lorenzo)  
**Слой:** memory / orchestration  
**Дата:** март 2025  
**Уникальность:** Production-grade когнитивная архитектура памяти для локального AI-агента без внешней векторной БД: 4 типа нод (episodic, semantic, procedural, opinion) + 5 типов рёбер включая `supersedes` для эволюции фактов. Кривая забывания Эббингауза + hot/slow path (50ms fire-and-forget). Гибридный поиск FTS5+KNN+граф через RRF.

## Проблема: почему RAG не равно память

```
RAG для долгоживущих агентов:
  → Поиск по документам ≠ поиск в личной памяти
  → Нет эволюции фактов: "Маша была замужем" + "Маша развелась"
    → RAG вернёт ОБА факта как равновалентные
  → Нет временной деградации: факт 3-летней давности = факт вчера
  → Нет типологии: эпизод "встретились" ≠ знание "любит кофе"
  → Нет persona consistency: агент "забывает" кто он между сессиями

Решение VitalyOborin:
  Когнитивная граф-памятная архитектура в SQLite
  → Локально (нет API calls на чтение/запись)
  → Быстро (FTS5 полнотекстовый поиск встроен в SQLite)
  → Типизировано (4 типа нод, 5 типов рёбер)
  → Эволюция фактов (ребро supersedes)
  → Забывание (кривая Эббингауза)
```

## Граф памяти: типы нод и рёбер

```python
from enum import Enum

class NodeType(Enum):
    EPISODIC   = "episodic"    # "Мы встретились в кафе в четверг"
    SEMANTIC   = "semantic"    # "Катя — программист, любит Python"
    PROCEDURAL = "procedural"  # "Когда просит отчёт — форматировать как таблицу"
    OPINION    = "opinion"     # "Считает, что MongoDB лучше PostgreSQL"

class EdgeType(Enum):
    RELATES_TO  = "relates_to"   # общая связь
    SUPERSEDES  = "supersedes"   # новый факт заменяет старый ← ключевое!
    CAUSES      = "causes"       # причинно-следственная
    PART_OF     = "part_of"      # часть целого
    CONTRADICTS = "contradicts"  # противоречие (для детекции конфликтов)

# SQLite схема
MEMORY_SCHEMA = """
CREATE TABLE IF NOT EXISTS memory_nodes (
    id          TEXT PRIMARY KEY,   -- UUID
    node_type   TEXT NOT NULL,
    content     TEXT NOT NULL,      -- сам факт/эпизод
    embedding   BLOB,               -- 256-dim Matryoshka float32
    importance  REAL DEFAULT 1.0,   -- текущая важность (0-1)
    created_at  INTEGER NOT NULL,   -- UNIX timestamp
    accessed_at INTEGER NOT NULL,   -- последний доступ (для forgetting)
    access_count INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS memory_edges (
    id          TEXT PRIMARY KEY,
    source_id   TEXT REFERENCES memory_nodes(id),
    target_id   TEXT REFERENCES memory_nodes(id),
    edge_type   TEXT NOT NULL,
    weight      REAL DEFAULT 1.0,
    created_at  INTEGER NOT NULL
);

-- FTS5 для полнотекстового поиска
CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts
    USING fts5(content, content=memory_nodes, content_rowid=rowid);
"""
```

## Кривая забывания Эббингауза: математика важности

```python
import math
import time

class EbbinghausMemory:
    """
    Важность факта убывает по экспоненте — как в реальной памяти.
    При каждом обращении к факту — reinforce (важность восстанавливается).
    """

    STABILITY_BY_TYPE = {
        NodeType.SEMANTIC:   30.0,   # дни: долгосрочные факты
        NodeType.PROCEDURAL: 60.0,   # инструкции: очень стойкие
        NodeType.OPINION:    20.0,   # мнения меняются чаще
        NodeType.EPISODIC:   7.0,    # эпизоды быстро теряют вес
    }

    def current_importance(self, node: MemoryNode) -> float:
        """
        R(t) = e^(-t/S)
        t = дней с последнего обращения
        S = стабильность (зависит от типа ноды)
        """
        stability = self.STABILITY_BY_TYPE[node.node_type]
        days_since_access = (time.time() - node.accessed_at) / 86400
        retention = math.exp(-days_since_access / stability)
        return retention * node.base_importance

    def reinforce(self, node_id: str, db: sqlite3.Connection):
        """При обращении к ноде — усилить важность (spaced repetition)."""
        now = int(time.time())
        db.execute("""
            UPDATE memory_nodes
            SET accessed_at = ?,
                access_count = access_count + 1,
                importance = MIN(1.0, importance * 1.3)
            WHERE id = ?
        """, (now, node_id))

    def prune_stale(self, db: sqlite3.Connection, threshold: float = 0.05):
        """Периодически удалять ноды с retention < threshold."""
        all_nodes = db.execute(
            "SELECT id, node_type, accessed_at, importance FROM memory_nodes"
        ).fetchall()

        stale = [
            n["id"] for n in all_nodes
            if self.current_importance(n) < threshold
        ]

        if stale:
            db.executemany(
                "DELETE FROM memory_nodes WHERE id = ?",
                [(nid,) for nid in stale]
            )
```

## Hot/Slow Path: запись без блокировки

```python
import asyncio
from collections import deque

class MemoryWriteQueue:
    """
    Hot path: синхронный поиск (< 10ms)
    Slow path: запись асинхронная (fire-and-forget, ~50ms)
    → Агент не ждёт записи в памяти во время разговора
    """

    def __init__(self, db_path: str):
        self._queue = deque()
        self._db = sqlite3.connect(db_path, check_same_thread=False)

    def read_hot(self, query: str, top_k: int = 10) -> list[MemoryNode]:
        """Синхронный гибридный поиск — вызывается во время генерации."""
        return self._hybrid_search(query, top_k)

    def write_async(self, node: MemoryNode):
        """Добавить в очередь записи, не блокировать разговор."""
        self._queue.append(node)

    async def _flush_loop(self):
        """Фоновый воркер: сбрасывает очередь каждые 50ms."""
        while True:
            while self._queue:
                node = self._queue.popleft()
                self._persist(node)
            await asyncio.sleep(0.05)  # 50ms batch window

    def _hybrid_search(self, query: str, top_k: int) -> list[MemoryNode]:
        """
        Три источника → Reciprocal Rank Fusion.
        """
        # 1. FTS5 полнотекстовый поиск (точные совпадения)
        fts_results = self._db.execute("""
            SELECT n.*, fts.rank as fts_score
            FROM memory_fts fts
            JOIN memory_nodes n ON n.rowid = fts.rowid
            WHERE memory_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ?
        """, (query, top_k * 2)).fetchall()

        # 2. KNN по эмбеддингу запроса (256-dim Matryoshka)
        query_embedding = self._embed(query)
        knn_results = self._knn_search(query_embedding, top_k * 2)

        # 3. Граф-обход от топ-нод (семантическое расширение)
        seed_ids = [r["id"] for r in fts_results[:3]]
        graph_results = self._graph_traverse(seed_ids, depth=2)

        # 4. Reciprocal Rank Fusion
        return self._rrf_merge(
            fts_results, knn_results, graph_results,
            weights=[0.4, 0.4, 0.2],
            top_k=top_k
        )
```

## Эволюция фактов: ребро supersedes

```python
class FactEvolution:
    """
    Когда пользователь говорит новое — не удалять старое,
    а создать ребро supersedes. Это сохраняет историю.
    """

    def update_fact(self, old_node_id: str, new_content: str,
                    db: sqlite3.Connection) -> str:
        # Создать новую ноду
        new_node = MemoryNode(
            content=new_content,
            node_type=NodeType.SEMANTIC,
            importance=1.0
        )
        db.execute("INSERT INTO memory_nodes VALUES (?)", (new_node,))

        # Связать supersedes (новый → старый)
        db.execute("""
            INSERT INTO memory_edges (source_id, target_id, edge_type)
            VALUES (?, ?, 'supersedes')
        """, (new_node.id, old_node_id))

        # Снизить важность старой ноды
        db.execute("""
            UPDATE memory_nodes SET importance = importance * 0.3
            WHERE id = ?
        """, (old_node_id,))

        return new_node.id

# Пример: "Маша раньше работала в Сбере" → "Маша теперь в Яндексе"
# График: [Яндекс] --supersedes--> [Сбер]
# При поиске: вернуть [Яндекс] с высокой важностью,
#             [Сбер] — только если запрос про историю
```

## Session consolidation: переход между сессиями

```python
class SessionConsolidator:
    """
    Между сессиями: агент-консолидатор извлекает долгосрочные факты
    из ephemeral истории разговора → записывает в постоянную память.
    """

    async def consolidate(self, session_history: list[Message],
                           memory_store: MemoryWriteQueue):
        # LLM-агент анализирует диалог
        extraction_prompt = f"""
Проанализируй этот разговор и извлеки факты для долгосрочной памяти.
Для каждого факта укажи: тип (semantic/episodic/procedural/opinion), 
содержание, и есть ли противоречие с уже известным.

Разговор:
{self._format_history(session_history)}

Формат ответа: JSON array [{{"type": "...", "content": "...", "supersedes": null|"старый факт"}}]
"""
        extracted_facts = await self.extractor_llm.extract(extraction_prompt)

        for fact in extracted_facts:
            node = MemoryNode(
                content=fact["content"],
                node_type=NodeType[fact["type"].upper()],
                importance=0.8  # новые факты из разговора
            )

            if fact.get("supersedes"):
                # Найти старый факт и обновить
                old_node = memory_store.find_similar(fact["supersedes"])
                if old_node:
                    memory_store.update_fact(old_node.id, fact["content"])
                    continue

            memory_store.write_async(node)
```

## Применение к Lorenzo

VitalyOborin — автор Yodoca + Wikontic (уже в базе контактов Lorenzo). Эта архитектура памяти:

```python
# improve_agent_memory.py (паттерн):

class LorenzoAgentMemory:
    """
    Lorenzo агент с когнитивной памятью.
    Помнит: какие документы часто используются,
    предпочтения пользователя, решённые задачи.
    """

    def __init__(self):
        self.memory = MemoryWriteQueue("data/lorenzo_memory.db")
        self.ebbinghaus = EbbinghausMemory()

    async def answer_with_memory(self, question: str) -> str:
        # 1. Извлечь релевантные воспоминания
        memories = self.memory.read_hot(question, top_k=5)

        # 2. Построить контекст с учётом важности
        memory_context = "\n".join([
            f"[{m.node_type}] {m.content} (важность: {self.ebbinghaus.current_importance(m):.2f})"
            for m in memories
        ])

        # 3. Ответить
        response = await self.llm.ask(
            question=question,
            memory_context=memory_context
        )

        # 4. Записать взаимодействие в память (async)
        self.memory.write_async(MemoryNode(
            content=f"Q: {question} → A: {response[:200]}",
            node_type=NodeType.EPISODIC
        ))

        return response
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Cognitive Memory + Yodoca (R01)** | VitalyOborin объединяет: Yodoca (хранилище) + новая архитектура (граф + забывание) |
| **Cognitive Memory + Durable State (R23)** | Память между сессиями + stateful approval workflows |
| **Cognitive Memory + HITL (R30)** | Агент помнит предыдущие решения HITL → избегает повторных запросов |
| **Cognitive Memory + DBRM (R31)** | Медицинский агент помнит историю пациента между сессиями |
| **Cognitive Memory + LLM Judge (R28)** | Судья оценивает качество консолидации фактов между сессиями |

## Контакт

- Статья: https://habr.com/ru/articles/1006622/ (март 2025)
- VitalyOborin — автор Yodoca + Wikontic (уже в `docs/contacts/`)
- Смежная (Yodoca memory store): docs/05-habr-projects/memory/yodoca.md
- Смежная (RAG vs persistent memory): https://habr.com/ru/articles/981540/
- Смежная (Durable State R23): https://habr.com/ru/articles/1031440/
- Matryoshka Embeddings: arxiv.org/abs/2205.13147
