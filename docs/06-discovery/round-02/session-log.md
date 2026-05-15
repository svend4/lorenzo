---
date: 2026-05-15
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# Round 02 — Лог поисковой сессии

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Запустить поиск комбинаций: Документ создан на основе исследования. Ссылки ведут на связанные материалы.
 
Смотрите также
 Главная
 Метрики
 Здоровье
 Глоссарий
 Сущности


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** 🔄 В процессе  
**Тема:** нейросети, ИИ, программное обеспечение — ниши вне Round 01

---

## Что уже найдено в Round 01 (не повторять)

Авторы: kksudo, spbmolot, VitalyOborin, AnastasiyaW, VitaliySemenov,
Antipozitive, zodigancode, nlaik, Cutcode, Dmitriila, MiXaiLL76,
Sonia_Black, VladSpace, andrey_chuyan, lee-to, tagir_analyzes

Темы: agent memory, knowledge graph, MCP, RAG, multi-agent orchestration,
Wikontic, Legal RAG, AgentFS, Rufler, mclaude

---

## Ниши для Round 02

### Ниша A — Локальные LLM и инфраструктура инференса
> Не агенты, а то на чём они запускаются

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `локальная языковая модель запуск` | ollama-подобные обёртки, свои решения |
| `llm inference оптимизация python` | квантизация, батчинг, кэш |
| `llama cpp python обёртка` | кастомные биндинги |
| `локальный чат своя модель telegram` | боты на локальных моделях |

### Ниша B — Обработка и парсинг документов
> Не RAG целиком, а только слой ingestion/parsing

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `парсинг pdf python нейросеть` | умный парсинг с ML |
| `извлечение данных документы llm` | структурированное извлечение |
| `ocr распознавание текст open source` | локальные OCR с AI |
| `чанкинг текст семантический` | нестандартные стратегии чанкинга |

### Ниша C — Observability и тестирование AI-систем
> Как следить за тем, что агент делает

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `мониторинг llm агент логи` | трейсинг, дашборды |
| `тестирование промпт llm автоматическое` | prompt testing frameworks |
| `оценка качества ответов llm python` | evaluation pipelines |
| `трассировка агент инструменты отладка` | debugging tools |

### Ниша D — Голос и мультимодальность
> Всё что не текст→текст

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `голосовой ассистент open source python` | TTS/STT + LLM |
| `whisper telegram бот локальный` | voice bots |
| `vision llm изображения python` | локальные vision модели |
| `мультимодальный агент видео` | video understanding |

### Ниша E — Инструменты для разработчиков AI
> Не конечные продукты, а dev-tools

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `дообучение файнтюнинг lora python` | fine-tuning утилиты |
| `датасет генерация синтетический llm` | synthetic data tools |
| `промпт менеджер версионирование` | prompt management |
| `векторная база данных локальная` | local vector stores |

### Ниша F — Автоматизация и workflow
> Декларативные пайплайны, не агенты в классическом смысле

| Запрос на Хабре | Что ищем |
|-----------------|----------|
| `автоматизация задач llm workflow` | task automation |
| `планировщик агент python open source` | task planners |
| `n8n аналог python ai` | workflow engines с AI |
| `rpa автоматизация нейросеть` | AI-powered RPA |

---

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| PocketCoder | @Chashchin-Dmitry | F — coding agent | `projects/pocketcoder.md` |
| Ирина | @janvarev | D — голосовой интерфейс | `projects/irene-voice-assistant.md` |
| Dedoc | @ispras (ИСП РАН) | B — парсинг документов | `projects/dedoc.md` |
| Coreness Flow | @Vensus137 | F — YAML workflow | `projects/coreness-flow.md` |
| XAI Agent | @SadSabrina | C — observability/XAI | `projects/xai-agent.md` |
| Doka | неизвестен | A — local agent UI | `projects/doka-local-agent.md` |

## Найденные комбинации с Round 01 (топ)

| Новый проект | + Из Round 01 | Новое свойство |
|-------------|---------------|----------------|
| Ирина | agent-memory-mcp | Голосовой агент с постоянной памятью |
| Dedoc | LiteParse (nlaik) | Двухступенчатый ingestion: структура + evidence |
| Coreness Flow | Rufler | Declarative stack: event-runtime + YAML-DSL |
| PocketCoder | AgentFS | Coding agent с файловой памятью |
| XAI Agent | improve_collab_finder | Объяснимые рекомендации коллабораций |

## Итог раунда

_Заполняется после завершения_

---

## Как добавить проект

1. Скопировать шаблон из `docs/06-discovery/README.md`
2. Создать `projects/<название>.md`
3. Запустить поиск комбинаций:
```bash
python scripts/improve_collab_finder.py \
  --file docs/06-discovery/round-02/projects/<название>.md --top 5
```

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
