---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# AI-агент с 5-слойной памятью: персонализация через Memory Synthesizer

<!-- toc-auto -->
<!-- tags: five-layer-memory-personalization-pgvector, docs -->


<!-- summary -->
> `five-layer-memory-personalization-pgvector` — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Svetafo  
**Хабр:** https://habr.com/ru/articles/1007940/  
**GitHub:** нет (описание архитектуры)  
**Слой:** memory / orchestration  
**Дата:** март 2026  
**Уникальность:** Пятислойная архитектура памяти (сессионная → эпизодическая → семантическая → база знаний → синтезированные паттерны) с Memory Synthesizer — компонентом нахождения скрытых корреляций через коэффициент Спирмена. Каждый слой управляется отдельно с политиками промоции и декомпозиции. PostgreSQL 16 + pgvector как unified хранилище. Интеграция с n8n для автоматизации триггеров синтеза.

## Проблема: один размер не подходит всем

```
Стандартные LLM ассистенты:
  → Каждая сессия начинается с нуля
  → Или: одна большая "память" без структуры
  → Нет разницы между "вчера сказал" и "фундаментальное предпочтение"

Нужна иерархия:
  Сессионная: "в этом разговоре мы обсуждали X"
  Эпизодическая: "5 марта ты спросил про Y"
  Семантическая: "ты предпочитаешь краткие ответы"
  База знаний: "ты эксперт в области Z"
  Синтезированные паттерны: "обычно тебя интересует A когда ты делаешь B"

Memory Synthesizer:
  → Находит скрытые паттерны через корреляцию Спирмена
  → Автоматически промоутирует важные воспоминания вверх по иерархии
```

## 5-слойная архитектура памяти

```python
# Svetafo: AI-агент с 5-слойной памятью (habr 1007940)

from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
import asyncpg
from pgvector.asyncpg import register_vector

class MemoryLayer(IntEnum):
    SESSION    = 1   # текущий разговор (TTL: сессия)
    EPISODIC   = 2   # конкретные события (TTL: недели)
    SEMANTIC   = 3   # устойчивые предпочтения (TTL: месяцы)
    KNOWLEDGE  = 4   # экспертиза пользователя (TTL: постоянно)
    PATTERNS   = 5   # синтезированные корреляции (TTL: постоянно)

@dataclass
class MemoryNode:
    content: str
    layer: MemoryLayer
    user_id: str
    embedding: list[float]        # pgvector, 1536-dim
    confidence: float = 1.0
    access_count: int = 0
    last_accessed: datetime = field(default_factory=datetime.utcnow)
    metadata: dict = field(default_factory=dict)
    # Для паттернов: Spearman correlation score
    correlation_score: float = 0.0


class FiveLayerMemoryStore:
    """
    PostgreSQL 16 + pgvector как unified хранилище всех 5 слоёв.
    Каждый слой — отдельная политика retention и промоции.
    """

    async def store(self, node: MemoryNode) -> str:
        """Сохранить в нужный слой."""
        async with self.pool.acquire() as conn:
            await register_vector(conn)

            node_id = await conn.fetchval("""
                INSERT INTO memory_nodes
                    (user_id, content, layer, embedding, confidence,
                     correlation_score, metadata)
                VALUES ($1, $2, $3, $4, $5, $6, $7)
                RETURNING id
            """,
                node.user_id, node.content, node.layer.value,
                node.embedding, node.confidence,
                node.correlation_score, node.metadata
            )
        return node_id

    async def retrieve(self, query_embedding: list[float],
                        user_id: str,
                        layers: list[MemoryLayer] = None,
                        top_k: int = 10) -> list[MemoryNode]:
        """
        Гибридный поиск: vector similarity + layer фильтрация.
        Более высокие слои приоритизируются (PATTERNS > KNOWLEDGE > ...).
        """
        layer_filter = layers or list(MemoryLayer)
        layer_values = [l.value for l in layer_filter]

        async with self.pool.acquire() as conn:
            await register_vector(conn)
            rows = await conn.fetch("""
                SELECT *,
                       -- Приоритет: схожесть × (1 + layer/5)
                       (1 - (embedding <=> $1)) * (1.0 + layer / 5.0) AS score
                FROM memory_nodes
                WHERE user_id = $2 AND layer = ANY($3)
                ORDER BY score DESC
                LIMIT $4
            """, query_embedding, user_id, layer_values, top_k)

        return [self._row_to_node(r) for r in rows]

    async def promote(self, node_id: str,
                       target_layer: MemoryLayer):
        """Промоутировать воспоминание на более высокий уровень."""
        async with self.pool.acquire() as conn:
            await conn.execute("""
                UPDATE memory_nodes
                SET layer = $1, promoted_at = NOW()
                WHERE id = $2
            """, target_layer.value, node_id)
```

## Memory Synthesizer: корреляция Спирмена

```python
from scipy import stats
import numpy as np

class MemorySynthesizer:
    """
    Находит скрытые паттерны в эпизодической и семантической памяти.
    Spearman correlation: непараметрическая, устойчива к выбросам.

    Результат: PATTERNS слой (Layer 5) — синтезированные инсайты
    о пользователе, которые он сам не артикулировал.
    """

    CORRELATION_THRESHOLD = 0.65   # порог для создания паттерна
    MIN_OBSERVATIONS = 5           # минимум событий для корреляции

    async def synthesize_patterns(self, user_id: str) -> list[MemoryNode]:
        """
        Найти корреляции в поведении пользователя.
        Запускается по расписанию (n8n триггер: раз в неделю).
        """
        # Загрузить эпизодическую память (конкретные события)
        episodes = await self.store.get_all(user_id, MemoryLayer.EPISODIC)

        if len(episodes) < self.MIN_OBSERVATIONS:
            return []

        patterns = []

        # Попарная корреляция признаков
        feature_vectors = self._extract_features(episodes)
        n_features = feature_vectors.shape[1]

        for i in range(n_features):
            for j in range(i+1, n_features):
                correlation, p_value = stats.spearmanr(
                    feature_vectors[:, i],
                    feature_vectors[:, j]
                )

                # Статистически значимая корреляция
                if abs(correlation) >= self.CORRELATION_THRESHOLD and p_value < 0.05:
                    pattern = await self._create_pattern_description(
                        feature_idx_1=i,
                        feature_idx_2=j,
                        correlation=correlation,
                        user_id=user_id
                    )
                    patterns.append(MemoryNode(
                        content=pattern,
                        layer=MemoryLayer.PATTERNS,
                        user_id=user_id,
                        embedding=await self.embedder.embed(pattern),
                        correlation_score=abs(correlation),
                        confidence=1 - p_value  # p-value → confidence
                    ))

        return patterns

    def _extract_features(self, episodes: list[MemoryNode]) -> np.ndarray:
        """
        Извлечь числовые признаки из эпизодов:
        время суток, тип запроса, длина сессии,
        тематический вектор и т.д.
        """
        features = []
        for ep in episodes:
            features.append([
                ep.last_accessed.hour,           # время суток
                ep.metadata.get("query_length", 0),
                ep.metadata.get("session_duration", 0),
                ep.metadata.get("topic_cluster", 0),
                ep.access_count,
                ep.confidence
            ])
        return np.array(features)

    async def _create_pattern_description(self, feature_idx_1: int,
                                           feature_idx_2: int,
                                           correlation: float,
                                           user_id: str) -> str:
        """LLM формулирует инсайт в человекочитаемый паттерн."""
        feature_names = ["время суток", "длина запроса", "длительность сессии",
                         "тематический кластер", "частота доступа", "достоверность"]

        f1 = feature_names[feature_idx_1]
        f2 = feature_names[feature_idx_2]
        direction = "положительно" if correlation > 0 else "отрицательно"

        prompt = f"""Пользователь {user_id} демонстрирует корреляцию:
{f1} {direction} коррелирует с {f2} (r={correlation:.2f}).

Сформулируй поведенческий паттерн в 1 предложении для персонализации."""

        return await self.llm.generate(prompt)
```

## Политики промоции между слоями

```python
class LayerPromotionPolicy:
    """
    Когда воспоминание "заслуживает" перейти на более высокий слой.
    """

    PROMOTION_RULES = {
        MemoryLayer.SESSION → MemoryLayer.EPISODIC: {
            "condition": "access_count >= 2 OR explicitly_saved",
            "description": "Упомянуто дважды → сохранить как эпизод"
        },
        MemoryLayer.EPISODIC → MemoryLayer.SEMANTIC: {
            "condition": "access_count >= 5 AND age_days >= 7",
            "description": "Повторяется неделю → это предпочтение"
        },
        MemoryLayer.SEMANTIC → MemoryLayer.KNOWLEDGE: {
            "condition": "access_count >= 20 AND confidence >= 0.9",
            "description": "Стабильное предпочтение → экспертиза"
        }
    }

    async def run_promotion_cycle(self, user_id: str):
        """n8n триггерит этот цикл раз в день."""
        for (from_layer, to_layer), rule in self.PROMOTION_RULES.items():
            candidates = await self.store.get_promotion_candidates(
                user_id, from_layer, rule["condition"]
            )
            for node in candidates:
                await self.store.promote(node.id, to_layer)


TECH_STACK = {
    "runtime": "Python 3.12",
    "api": "FastAPI",
    "db": "PostgreSQL 16 + pgvector",
    "telegram": "aiogram 3",
    "automation": "n8n (триггеры синтеза и промоции)",
    "llm": "Claude Haiku (быстро, дёшево) + GPT-4o-mini (сложные задачи)",
    "embeddings": "text-embedding-3-small"
}
```

## Применение к Lorenzo

```python
# Lorenzo может использовать 5-слойную память для Q&A сессий

class LorenzoPersonalizedQA:
    """
    Персонализированный Lorenzo: помнит контекст пользователя
    через 5 слоёв памяти.

    Пример: пользователь неделями работает с memory проектами
    → PATTERNS слой фиксирует: "интересуется персистентной памятью"
    → При новом вопросе: автоматически приоритизировать
      агенты с памятью в результатах поиска
    """

    async def ask(self, user_id: str, question: str) -> str:
        # Загрузить релевантную память пользователя
        q_embedding = await self.embedder.embed(question)
        user_context = await self.memory.retrieve(
            q_embedding, user_id,
            layers=[MemoryLayer.PATTERNS, MemoryLayer.KNOWLEDGE,
                    MemoryLayer.SEMANTIC]
        )

        # Инъекция в промпт
        context_str = "\n".join([m.content for m in user_context])
        answer = await self.llm_qa.ask(
            question,
            extra_context=f"Профиль пользователя:\n{context_str}"
        )

        # Сохранить сессионную память
        await self.memory.store(MemoryNode(
            content=f"Q: {question}\nA: {answer[:200]}",
            layer=MemoryLayer.SESSION,
            user_id=user_id,
            embedding=q_embedding
        ))
        return answer
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **5-Layer Memory + Cognitive Memory (R31)** | SQLite (Cognitive) + pgvector (5-Layer) = гибридное хранилище с Spearman синтезом |
| **5-Layer Memory + Yodoca (R01)** | Yodoca граф + Spearman паттерны = граф с корреляционными рёбрами |
| **5-Layer Memory + Sequential (R38)** | Агенты с 5-слойной памятью в Sequential протоколе: каждый агент помнит историю |
| **5-Layer Memory + LangFuse (R38)** | Memory операции → LangFuse трейсы: наблюдаемость системы памяти |
| **5-Layer Memory + Lorenzo Gateway** | /api/ask + user_id → персонализированные ответы через pgvector |

## Контакт

- Статья: https://habr.com/ru/articles/1007940/ (март 2026)
- Автор: Svetafo (Хабр)
- pgvector: github.com/pgvector/pgvector
- aiogram: github.com/aiogram/aiogram
- Смежная (Yodoca SQLite память): https://habr.com/ru/articles/1006622/
- Смежная (NGT Memory ассоциативный граф): https://habr.com/ru/articles (R01)
- Смежная (personal-context-manager JSON профиль): https://habr.com/ru/articles/892136/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
