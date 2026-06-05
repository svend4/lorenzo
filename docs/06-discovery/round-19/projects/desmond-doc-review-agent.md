---
date: 2026-06-05
tags: [memory, rag, orchestration, architecture, self-improve]
state: normalized
---

# Desmond — AI-агент проверки документации (Альфа-Банк)

<!-- toc-auto -->
<!-- tags: desmond-doc-review-agent, docs -->


<!-- summary -->
> Автор: команда Alfa Online (Альфа-Банк) Хабр: https://habr.com/ru/companies/alfa/articles/932058/
Хабр: https://habr.com/ru/companies/alfa/articles/932058/  
GitHub: не опубликован (корпоративный проект, полная архитектура описана)  
Слой: orchestration / knowledge / quality  
Дата: 2025  
Уникальность: П


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда Alfa Online (Альфа-Банк)  
**Хабр:** https://habr.com/ru/companies/alfa/articles/932058/  
**GitHub:** не опубликован (корпоративный проект, полная архитектура описана)  
**Слой:** orchestration / knowledge / quality  
**Дата:** 2025  
**Уникальность:** Первый детальный open-architecture кейс **task-oriented AI-агента без диалога** для проверки документации в Confluence. Запускается по webhook из Jira (не по команде пользователя), проверяет ТЗ по единому стандарту, возвращает структурированный отчёт. Паттерн: агент = cognitive worker, не чат-бот.

## Контекст задачи

```
Проблема:
  - Платформенные аналитики вручную проверяют ТЗ продуктовых команд
  - Рутина: проверить полноту, структуру, согласованность разделов
  - Масштаб: сотни документов, разный стиль написания
        ↓
Решение: Desmond
  - Запускается автоматически при изменении статуса задачи в Jira
  - Читает документ из Confluence
  - Проверяет по 20+ критериям
  - Оставляет структурированный комментарий в Jira/Confluence
```

## Архитектура Desmond

```
Jira webhook (изменение статуса задачи)
        ↓
Desmond Agent (task-oriented, без диалога)
  Stage 1: Document fetch
    → Confluence API → полный текст ТЗ (HTML/Markdown)
  Stage 2: Structured analysis
    → LLM: проверить каждый раздел по критериям
    → output: {section: str, status: pass|fail|warn, comment: str}[]
  Stage 3: Report generation
    → структурированный отчёт: что OK, что нужно исправить
  Stage 4: Write back
    → Confluence comment + Jira transition
        ↓
Аналитик видит: чёткий список проблем, не "AI написал что-то"
```

## Ключевые архитектурные решения

### Task-oriented, не чат-бот

```python
# НЕ так (диалог):
response = llm.chat("Проверь этот документ: " + doc_text)
# → нет структуры, каждый раз разный формат

# ТАК (task-oriented):
analysis = llm.complete(
    system=CHECK_CRITERIA_PROMPT,  # 20+ конкретных критериев
    user=doc_text,
    response_format=DocumentAnalysis  # Pydantic-схема
)
# → всегда одинаковая структура, можно мерить качество
```

### Без состояния, реактивный

```
Desmond НЕ хранит историю разговора.
Каждый запуск = полностью независимый анализ.
  Входные данные: документ из Confluence
  Выходные данные: structured report
  Побочные эффекты: комментарий в Jira/Confluence
```

### Критерии проверки

```markdown
## CHECK_CRITERIA_PROMPT включает:
- Наличие всех обязательных разделов (цель, scope, acceptance criteria)
- Полнота описания (нет ли "TBD", "уточнить позже")
- Согласованность: нет ли противоречий между разделами
- Форматирование: таблицы, заголовки, списки
- Наличие примеров для нетривиальных кейсов
- Описание edge cases и error scenarios
```

## Метрики результата

- **−60% времени** платформенных аналитиков на рутинную проверку
- **Единый стандарт** качества: Desmond применяет одни критерии ко всем
- **Быстрая обратная связь**: не нужно ждать аналитика — отчёт за секунды

## Паттерн: Cognitive Worker

```
Традиционный агент = чат-бот с инструментами
  → диалоговый, многоходовый, хранит контекст

Cognitive Worker (Desmond-паттерн):
  → событийный (webhook)
  → stateless
  → структурированный вывод (Pydantic)
  → встраивается в существующий workflow незаметно
  → метрики: precision, recall проверок (измеримо)
```

## Применение к Lorenzo

Lorenzo = LLM-Wiki (R17). Документы в `docs/` — аналог Confluence.  
Desmond-паттерн применим напрямую:

```python
# improve_doc_review.py (не существует, но вот паттерн):
# Триггер: git commit (post-commit hook) → изменился файл в docs/
# Desmond: проверить файл по критериям Lorenzo:
#   - есть ли frontmatter? summary? теги?
#   - нет ли битых ссылок?
#   - нет ли пустых секций?
#   - согласован ли с DECISIONS.md?
# Output: структурированный список issues → REVIEW_REPORT.md
```

Связь с `improve_validate_templates.py` (Lorenzo): Desmond = LLM-слой поверх rule-based валидации.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Desmond + improve_validate** | Rule-based (Lorenzo) + LLM (Desmond) = двухуровневая проверка |
| **Desmond + ADD (R13)** | ADD Chronicle feedback loop — Desmond закрывает петлю |
| **Desmond + Langfuse (R13)** | Каждая проверка Desmond трейсится → качество агента видно |
| **Desmond + Context Engineering (R14)** | AGENTS.md = система критериев для Desmond |
| **Desmond + Agentic RAG (R18)** | Desmond ищет похожие документы → проверяет на дубли |

## Контакт

- Статья: https://habr.com/ru/companies/alfa/articles/932058/ (2025)
- Смежная (AI-агент для проверки ТЗ): https://habr.com/ru/articles/1006372/
- Смежная (CodeWiki Skill — документация к коду): https://habr.com/ru/articles/1002424/
- Смежная (SDD фреймворк): https://habr.com/ru/articles/996526/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
