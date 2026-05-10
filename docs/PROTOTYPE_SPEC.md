# Svyazi 2.0 — Спецификация прототипа

<!-- summary -->
> > **Версия:** 1.0 · **Дата:** 2026-05-10 · **Статус:** Draft
**Проекты:** Svyazi, CardIndex, AgentFS, knowledge-space, mclaude, AI Factory, LiteParse, Legal RAG

---

<!-- toc -->
## Содержание

- [1. Цель прототипа](#1-цель-прототипа)
- [2. Компоненты MVP (три слоя)](#2-компоненты-mvp-три-слоя)
- [3. Интеграционные контракты](#3-интеграционные-контракты)
  - [3.1 Card Envelope](#31-card-envelope)
  - [3.2 Evidence Envelope](#32-evidence-envelope)
  - [3.3 Memory Write Policy](#33-memory-write-policy)
  - [3.4 Skill & Tool Policy](#34-skill-tool-policy)
  - [3.5 Review Record](#35-review-record)
- [4. Архитектура прототипа](#4-архитектура-прототипа)
- [5. Итерации MVP](#5-итерации-mvp)
  - [Итерация 0 — Вертикальный срез (2 недели)](#итерация-0-вертикальный-срез-2-недели)
  - [Итерация 1 — Retrieval Loop (2 недели)](#итерация-1-retrieval-loop-2-недели)
  - [Итерация 2 — Consolidation (2 недели)](#итерация-2-consolidation-2-недели)
  - [Итерация 3 — Collaboration Finder (финальная)](#итерация-3-collaboration-finder-финальная)
- [6. Технический стек](#6-технический-стек)
- [7. Риски и митигация](#7-риски-и-митигация)
- [8. Успешные метрики](#8-успешные-метрики)
- [9. Следующие шаги](#9-следующие-шаги)

---

<!-- tags: memory, rag, orchestration, security, knowledge, ingestion, local-first, architecture, roadmap, self-improvement, collaboration -->




> **Версия:** 1.0 · **Дата:** 2026-05-10 · **Статус:** Draft

---

## 1. Цель прототипа

Доказать одну центральную способность системы: **Knowledge OS находит и объясняет кандидатные коллаборации по свободным описаниям, документам и ключевым словам.**

Прототип не претендует на полноту. Он минимален настолько, чтобы:

1. Продемонстрировать ценность трёхслойной архитектуры на реальных данных
2. Получить обратную связь от авторов Хабр-проектов до крупных инвестиций
3. Сформировать общий интеграционный контракт, на который все компоненты могут опереться

---

## 2. Компоненты MVP (три слоя)

| Слой | Компонент | Роль в прототипе | Лицензия |
|------|-----------|------------------|----------|
| **Ingestion** | Svyazi / CardIndex | Нормализация документов → Card Envelope | MIT |
| **Memory** | Yodoca | Консолидация + forgetting + ассоциативные связи | Apache 2.0 |
| **Knowledge** | AgentFS | Файловая система-граф (Obsidian vault style) | MIT |
| **Orchestration** | mclaude / AI Factory | Маршрутизация агентов, Tool Search | — |
| **Retrieval** | Hybrid RAG + LiteParse | Поиск по документам + извлечение структуры | — |

**Почему именно эти три:** они покрывают жизненный цикл знания — поступление → хранение → навигация — и уже частично задокументированы авторами с Хабра.

---

## 3. Интеграционные контракты

> Без общего языка данных компоненты создадут три несовместимых «карточки» и четыре формата памяти.

### 3.1 Card Envelope

Базовая единица хранения. Любой документ, заметка или факт сначала становится карточкой.

```json
{
  "card_id":      "sha256:...",
  "card_type":    "doc | note | fact | person | project",
  "state":        "raw | normalized | inferred | approved | rejected | decayed",
  "sources":      ["url", "file_path"],
  "edges":        [{"to": "card_id", "rel": "references | contradicts | extends"}],
  "created_at":   "ISO-8601",
  "updated_at":   "ISO-8601",
  "payload_hash": "sha256:...",
  "payload":      { ... }
}
```

**Откуда:** CardIndex-мышление Svyazi + immutable-event практики AgentFS + Memory OS bi-temporal records.

### 3.2 Evidence Envelope

Любой retrieval-ответ возвращает не только текст, но и доказательную цепочку.

```json
{
  "source_id":        "card_id или url",
  "page_or_span":     "3 | §4.2 | 00:01:23-00:02:10",
  "bbox_or_offset":   [x, y, w, h] ,
  "retrieval_method": "bm25 | semantic | graph | hybrid",
  "confidence":       0.87,
  "supporting_nodes": ["card_id", ...]
}
```

**Откуда:** LiteParse page+box, Legal RAG source attribution, Hybrid/Graph RAG evidence chains.

### 3.3 Memory Write Policy

Записать «что-то в память» — никогда не одна операция.

| `write_type` | Когда | Требует ревью |
|-------------|-------|---------------|
| `episode`   | Сырое наблюдение, не проверено | нет |
| `fact`      | Подтверждённое знание | нет (если confidence > 0.9) |
| `proposal`  | Гипотеза агента | да |
| `decay_event` | Снижение значимости | нет |

**Откуда:** Yodoca consolidation+forgetting, NGT Memory иерархическая консолидация, agent-memory-mcp typed primitives.

### 3.4 Skill & Tool Policy

```
tool_class:    read | annotate | plan | mutate | publish | external_send
approval_mode: auto | review | blocked
path_scope:    local | project | global
network_scope: offline | internal | internet
```

**Откуда:** Tool Search (экономия контекста) + SENTINEL (аудит угроз) + AI Factory governance.

### 3.5 Review Record

```json
{
  "reviewer_role":  "human | agent | auto",
  "decision":       "approved | rejected | deferred",
  "reason":         "...",
  "evidence_refs":  ["card_id", ...],
  "follow_up":      "optional_task_id"
}
```

---

## 4. Архитектура прототипа

```
┌─────────────────────────────────────────────────────────┐
│                     Пользователь / LLM                  │
└───────────────────────────┬─────────────────────────────┘
                            │  запрос (свободный текст)
                            ▼
┌─────────────────────────────────────────────────────────┐
│              Orchestration Layer (mclaude)               │
│  Tool Search → Router → Agent Pool → Review Queue        │
└──────┬─────────────────────┬──────────────────────┬──────┘
       │                     │                      │
       ▼                     ▼                      ▼
┌─────────────┐    ┌─────────────────┐    ┌────────────────┐
│  Retrieval  │    │  Memory Layer   │    │ Knowledge Graph │
│  Hybrid RAG │    │     Yodoca      │    │    AgentFS      │
│  LiteParse  │    │  episode→fact   │    │  vault + edges  │
└──────┬──────┘    └────────┬────────┘    └────────┬───────┘
       │                    │                       │
       └────────────────────┴───────────────────────┘
                            │  Card Envelope
                            ▼
                   ┌─────────────────┐
                   │ Ingestion Layer  │
                   │  Svyazi/CardIndex│
                   │  LiteParse       │
                   └─────────────────┘
```

---

## 5. Итерации MVP

### Итерация 0 — Вертикальный срез (2 недели)

**Цель:** доказать, что три компонента вообще говорят на одном языке.

- [ ] CardIndex принимает документ → возвращает Card Envelope (JSON)
- [ ] AgentFS сохраняет карточку как файл с YAML frontmatter + edge-ссылки
- [ ] Yodoca получает карточку → создаёт memory episode
- [ ] MCP-инструмент `search_knowledge(query)` обходит AgentFS vault + Yodoca

**Критерий готовности:** один документ проходит путь от загрузки до поиска по нему за < 5 секунд.

### Итерация 1 — Retrieval Loop (2 недели)

**Цель:** BM25 + семантический поиск по всем карточкам.

- [ ] Hybrid RAG: BM25 (passages.json) + embedding (faiss / hnswlib)
- [ ] Evidence Envelope прикрепляется к каждому результату
- [ ] Review Queue: proposal-факты ждут одобрения человека
- [ ] Базовый UI: поиск + просмотр карточки + подтверждение/отклонение

**Критерий:** Precision@5 > 0.7 на 20 тестовых запросах из `docs/`.

### Итерация 2 — Consolidation (2 недели)

**Цель:** Yodoca consolidation + decay работают в фоне.

- [ ] Cron/scheduler запускает consolidation раз в сутки
- [ ] Дублирующиеся карточки мерджатся (similarity > 0.9)
- [ ] Старые episodes без подтверждения получают decay_event
- [ ] SENTINEL-check: каждый tool call логируется, аномалии флагируются

**Критерий:** после 7 дней работы накопленный шум (orphan cards) < 15%.

### Итерация 3 — Collaboration Finder (финальная)

**Цель:** система предлагает OSS-коллаборации из базы знаний.

- [ ] Агент анализирует новый документ → находит топ-5 похожих проектов
- [ ] Для каждого проекта: контакт автора + шаблон первого сообщения
- [ ] Экспорт в Obsidian vault (improve_obsidian.py) + RSS-фид (improve_rss.py)
- [ ] End-to-end тест: загружаем новую Хабр-статью → получаем рекомендацию за < 10с

---

## 6. Технический стек

| Компонент | Технология | Обоснование |
|-----------|-----------|-------------|
| Language | Python 3.11+ | все компоненты на Python, без сборки |
| Vector store | hnswlib (local) | MIT, без сервера, < 10 MB |
| BM25 | pure-python (passages.json) | уже работает в `improve_search_repl.py` |
| Graph store | markdown + YAML frontmatter | AgentFS-native, git-friendly |
| Memory | Yodoca API | консолидация без сервера |
| MCP transport | stdio | Claude Desktop compatible |
| Orchestration | mclaude (local) | минимальная зависимость |
| Review UI | Streamlit (опционально) | быстрый прототип |

**Принципы:** local-first, offline-capable, GDPR-safe, без облачных зависимостей по умолчанию.

---

## 7. Риски и митигация

| Риск | Вероятность | Митигация |
|------|-------------|-----------|
| Контракты несовместимы между проектами | высокая | Фиксируем Card Envelope в итерации 0, не двигаемся дальше без согласования |
| Yodoca API нестабильный (BSL 1.1) | средняя | Собственный адаптер с тонким интерфейсом |
| AgentFS vault разрастается до > 10K файлов | низкая | Sharding по дате + namespace |
| Авторы не отвечают на контакт | средняя | Параллельный поиск альтернатив (MemNet, agent-memory-mcp) |
| BM25 не справляется с кириллицей | низкая | Уже проверено: `improve_search_repl.py` обрабатывает 19K абзацев |

---

## 8. Успешные метрики

| Метрика | Порог MVP | Источник |
|---------|-----------|---------|
| Retrieval Precision@5 | ≥ 0.70 | ручная оценка 20 запросов |
| Latency (search→result) | ≤ 5с | локальный запуск |
| Card накопление (7 дней) | ≥ 500 карточек | автоматически |
| Orphan rate | ≤ 15% | Yodoca consolidation |
| Collaboration suggestions качество | ≥ 3/5 оценка | экспертная оценка |

---

## 9. Следующие шаги

```
1. Связаться с авторами:
   - kksudo (AgentFS)           → docs/contacts/kksudo.md
   - VitalyOborin (Yodoca)      → docs/contacts/vitalyoborin.md
   - AnastasiyaW (knowledge-space) → docs/contacts/anastasiyaw.md

2. Запустить итерацию 0:
   python scripts/improve_recipe.py --run habr-deep-dive

3. Построить поисковый индекс:
   python scripts/improve_passage_retrieval.py --index
   python scripts/improve_search_repl.py

4. Обновить план в PROGRESS.md:
   python scripts/improve_progress_sync.py
```

---

*Документ синтезирован из: `docs/01-svyazi/07-mvp-planning.md`, `docs/01-svyazi/11-integration-contracts.md`, `docs/01-svyazi/09-architectural-gaps.md`, `docs/01-svyazi/12-roadmap.md`*
