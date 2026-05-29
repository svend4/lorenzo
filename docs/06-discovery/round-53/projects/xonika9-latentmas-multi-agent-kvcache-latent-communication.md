---
date: 2026-05-29
tags: [rag, orchestration, security, knowledge, ingestion]
state: normalized
---

# LatentMAS: Мультиагентная система через KV-cache латентное пространство, +14.6pp, -80% токенов

<!-- toc-auto -->
<!-- tags: xonika9-latentmas-multi-agent-kvcache-latent-communication, docs -->


<!-- summary -->
> `xonika9-latentmas-multi-agent-kvcache-latent-communication` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** xonika9  
**Хабр:** https://habr.com/ru/articles/972184/  
**GitHub:** github.com/Gen-Verse/LatentMAS  
**Слой:** orchestration  
**Дата:** декабрь 2025  
**Уникальность:** Мультиагентная система где агенты общаются через KV-cache в латентном пространстве, а не через текстовые сообщения — устраняет bottleneck text serialization/deserialization. +14.6pp accuracy vs TextMAS на AIME/GPQA/GSM8K/MedQA, 70.8-83.7% снижение токенов, 4-4.3× speedup. Не дебаты агентов через текст (larayoda SimCourt) — структурная передача internal states напрямую между слоями трансформера.

## Проблема: текстовая коммуникация агентов — дорогостоящий bottleneck

```
Стандартный TextMAS (Multi-Agent System):
  Агент A → генерирует текстовый ответ (500 токенов)
  Агент B → читает ответ → генерирует свой (500 токенов)
  Агент C → синтезирует оба ответа → финальный ответ

  Проблемы TextMAS:
  1. Tokenization overhead: internal states → text → internal states
     Много информации теряется при сериализации в текст
  2. Дорого: каждый агент = отдельный LLM inference
     N агентов = N × стоимость inference
  3. Медленно: последовательные LLM вызовы + токенизация

LatentMAS решение:
  Агенты НЕ общаются через текст.
  Агент A → передаёт KV-cache (внутренние активации)
  Агент B → использует KV-cache агента A как prefix
  → Без tokenization/detokenization
  → Прямая передача "мыслей" между агентами
  → +14.6pp accuracy, 80% меньше токенов
```

## Архитектура LatentMAS

```python
# xonika9: LatentMAS — Multi-Agent через KV-cache
# habr.com/ru/articles/972184/
# github.com/Gen-Verse/LatentMAS

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class LatentState:
    """
    Внутреннее состояние агента в латентном пространстве.

    Не текст — KV-cache трансформера:
    keys: [n_layers, n_heads, seq_len, head_dim]
    values: [n_layers, n_heads, seq_len, head_dim]

    Содержит: всё что агент "знал" при обработке проблемы
    → Передать другому агенту = передать контекст без потерь
    """
    keys: np.ndarray     # K матрицы всех слоёв
    values: np.ndarray   # V матрицы всех слоёв
    agent_id: str
    token_count: int     # сколько токенов закодировано


@dataclass
class LatentMessage:
    """
    Сообщение между агентами через латентное пространство.

    Вместо строки "Я думаю что X = 42 потому что..." →
    сжатый latent state (KV-cache subset)
    """
    sender: str
    receiver: str
    latent: LatentState
    compression_ratio: float  # насколько сжат state


class LatentMASAgent:
    """
    Агент LatentMAS: думает в латентном пространстве, общается KV-cache.

    Принципиальное отличие от TextMAS:
    TextMAS: think → verbalize → send text → receive text → parse → think
    LatentMAS: think → compress KV → send latent → receive latent → continue thinking

    Сохраняется:
    - Направление мысли (через KV attention patterns)
    - Неопределённость (через распределения вероятностей)
    - Контекст (через seq_len в KV)

    Теряется:
    - Human-readable объяснение (текст не генерируется)
    + Это плюс: нет overhead на генерацию объяснений
    """

    def __init__(self, model, agent_id: str, role: str):
        self.model = model
        self.agent_id = agent_id
        self.role = role  # "specialist_A" | "specialist_B" | "synthesizer"

    def process(self,
                 problem: str,
                 received_latents: list[LatentState]) -> LatentState:
        """
        Обработать проблему с учётом latent states от других агентов.

        received_latents: KV-cache от предыдущих агентов
        → Используется как prefix при forward pass
        → Агент "видит" мысли других без text serialization
        """
        # Объединить полученные latent states как prefix KV
        if received_latents:
            prefix_kv = self._merge_latents(received_latents)
        else:
            prefix_kv = None

        # Forward pass с prefix KV → модель "знает" что думали другие
        output_kv, logits = self.model.forward_with_kv(
            input_text=problem,
            prefix_kv=prefix_kv,  # ← латентный контекст от агентов
            return_kv=True        # ← вернуть KV для передачи дальше
        )

        # Возвращаем наш KV-state (не текст!) следующему агенту
        return LatentState(
            keys=output_kv["keys"],
            values=output_kv["values"],
            agent_id=self.agent_id,
            token_count=output_kv["seq_len"]
        )

    def _merge_latents(self,
                        latents: list[LatentState]) -> dict:
        """
        Объединить KV-cache от нескольких агентов в один prefix.

        Конкатенация по seq_len dimension:
        [agent_A_kv | agent_B_kv] → единый prefix
        → Текущий агент видит всё что думали A и B
        """
        merged_keys = np.concatenate(
            [l.keys for l in latents], axis=2  # axis=2: seq_len
        )
        merged_values = np.concatenate(
            [l.values for l in latents], axis=2
        )
        return {"keys": merged_keys, "values": merged_values}


class LatentMASOrchestrator:
    """
    Оркестратор LatentMAS: координирует агентов без текстовой шины.

    Топология: parallel specialists → synthesizer
    (не sequential chain — параллельно для скорости)

    Шаг 1: K специалистов обрабатывают проблему параллельно
           → каждый возвращает LatentState
    Шаг 2: Synthesizer получает все LatentState как prefix
           → генерирует финальный текстовый ответ
           (только одна текстовая генерация, не K!)
    """

    def __init__(self, n_specialists: int = 3):
        self.specialists = [
            LatentMASAgent(model, f"specialist_{i}", f"perspective_{i}")
            for i in range(n_specialists)
        ]
        self.synthesizer = LatentMASAgent(model, "synthesizer", "synthesis")

    async def solve(self, problem: str) -> str:
        """
        Параллельное мультиагентное решение через латентное пространство.
        """
        import asyncio

        # Шаг 1: Все специалисты параллельно (не последовательно!)
        specialist_latents = await asyncio.gather(*[
            asyncio.to_thread(specialist.process, problem, [])
            for specialist in self.specialists
        ])

        # Шаг 2: Синтезатор с prefix из ВСЕХ specialist KV-states
        synthesis_latent = self.synthesizer.process(
            problem=problem,
            received_latents=list(specialist_latents)
        )

        # Шаг 3: Один текстовый decode для финального ответа
        final_answer = self.model.decode_from_kv(synthesis_latent)
        return final_answer


class LatentCompressor:
    """
    Сжатие KV-cache перед передачей между агентами.

    Полный KV-cache: [n_layers × n_heads × seq_len × head_dim]
    = Гигабайты для длинных последовательностей

    Compression варианты:
    1. Top-K attention: оставить только K наиболее attended токенов
    2. Cross-layer sharing: некоторые слои имеют похожие KV
    3. SVD compression: low-rank approximation KV matrices

    70.8-83.7% token reduction (эквивалент в текстовом пространстве)
    """

    def compress_topk(self,
                       latent: LatentState,
                       retention_ratio: float = 0.3) -> LatentState:
        """
        Top-K retention: оставить 30% наиболее важных позиций.

        Важность = сумма attention scores по всем головам.
        """
        seq_len = latent.keys.shape[2]
        n_keep = int(seq_len * retention_ratio)

        # Вычислить важность каждой позиции
        importance = np.abs(latent.keys).sum(axis=(0, 1, 3))  # sum over layers, heads, dim
        top_indices = np.argsort(importance)[-n_keep:]
        top_indices = np.sort(top_indices)  # сохранить порядок

        compressed = LatentState(
            keys=latent.keys[:, :, top_indices, :],
            values=latent.values[:, :, top_indices, :],
            agent_id=latent.agent_id,
            token_count=n_keep
        )
        return compressed


BENCHMARK_RESULTS = {
    "задачи": {
        "AIME": "математические олимпиадные задачи",
        "GPQA": "graduate-level PhD вопросы",
        "GSM8K": "школьная арифметика с рассуждениями",
        "MedQA": "медицинские вопросы"
    },
    "vs_TextMAS": {
        "accuracy_improvement": "+14.6pp",
        "token_reduction": "70.8-83.7%",
        "speedup": "4-4.3×"
    },
    "vs_single_agent": {
        "accuracy_improvement": "значительный (мультиагентный эффект)",
        "cost_comparable_to": "одиночный LLM inference (за счёт token savings)"
    },
    "github": "github.com/Gen-Verse/LatentMAS"
}
```

## Применение к Lorenzo

```python
# Lorenzo: LatentMAS для поиска и синтеза знаний

class LorenzoLatentSearch:
    """
    xonika9 паттерн для Lorenzo:
    Параллельные специалисты по разным слоям базы знаний.

    Специалист 1: ищет в docs/05-habr-projects/ (KV-state 1)
    Специалист 2: ищет в docs/06-discovery/ (KV-state 2)
    Специалист 3: ищет в docs/01-svyazi/ (KV-state 3)
    Синтезатор: получает 3 KV-states → итоговый ответ

    vs текущий gateway.py:
    Сейчас: один LLM с объединённым контекстом поиска
    LatentMAS: 3 параллельных LLM → синтез в латентном пространстве
    → Лучше при конфликтующей информации из разных разделов
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LatentMAS + Coordination Harness (R46)** | Coordination Harness измеряет fidelity передачи между текстовыми агентами; LatentMAS: fidelity в латентном пространстве — сравнение подходов |
| **LatentMAS + Quantization Deep Dive (R52)** | KV-cache compression (DMC) + LatentMAS latent communication: double compression — меньше памяти при передаче |
| **LatentMAS + Finance RAG 4-head (R49)** | 4-головый ретривер + LatentMAS: каждый retriever head → specialist agent, latent synthesis вместо RRF |
| **LatentMAS + LLM Observability (R45)** | Трейсинг latent communication: какие слои KV наиболее информативны при передаче между агентами |
| **LatentMAS + SENTINEL (R47)** | Latent-space фильтрация опасного контента: SENTINEL работает на KV-уровне до text decoding |

## Контакт

- Статья: https://habr.com/ru/articles/972184/ (декабрь 2025)
- Автор: xonika9 (Хабр)
- GitHub: github.com/Gen-Verse/LatentMAS
- Смежная (CLEV консенсус, R47): docs/06-discovery/round-47/projects/maslennikov-llm-judge-educational-content-clev.md
- Смежная (Coordination Harness, R46): docs/06-discovery/round-46/
- Смежная (Multi-agent case, R21): docs/06-discovery/round-21/
- Смежная (YandexGPT Accel DMC, R53): docs/06-discovery/round-53/projects/roman-gorb-yandex-llm-acceleration-speculative-dmc-kvcache.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
