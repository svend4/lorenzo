---
date: 2026-05-28
tags: [orchestration, security, architecture, roadmap, collaboration]
state: normalized
---

# LLM Immune System — защита AI за 3 мс (open-source)

<!-- toc-auto -->
<!-- tags: llm-immune-system, docs -->


<!-- summary -->
> Автор: независимый разработчик (Хабр) Хабр: https://habr.com/ru/articles/996896/
Хабр: https://habr.com/ru/articles/996896/  
GitHub: уточнить (статья описывает open-source реализацию)  
Слой: quality / security / orchestration  
Дата: 2026  
Уникальность: Токен-бай-токен фильтрация LLM-отв


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый разработчик (Хабр)  
**Хабр:** https://habr.com/ru/articles/996896/  
**GitHub:** уточнить (статья описывает open-source реализацию)  
**Слой:** quality / security / orchestration  
**Дата:** 2026  
**Уникальность:** Токен-бай-токен фильтрация LLM-ответов в реальном времени с задержкой **3 мс** — единственная найденная за 15 раундов система иммунной защиты для AI-агентов. Работает как middleware: перехватывает поток токенов ещё до отображения пользователю или передачи следующему агенту.

## Принцип работы

```
LLM генерирует токены (streaming)
        ↓
Immune System (middleware, 3ms per token)
  ├── Классификатор намерений (каждый токен / скользящее окно)
  ├── Детектор prompt injection
  ├── Проверка на запрещённые паттерны
  └── Детектор data leakage (API-ключи, PII)
        ↓
Безопасный поток токенов → пользователь / следующий агент
```

### Метрики

| Показатель | Значение |
|-----------|---------|
| Latency добавляемая | 3 мс на токен |
| Работает с | любым streaming LLM API |
| Ложные срабатывания | настраиваемый порог |
| Режим | мягкий (предупреждение) / жёсткий (блокировка) |

## Что детектирует

1. **Prompt injection** — когда внешние данные содержат инструкции для LLM
2. **Data leakage** — API-ключи, токены, персональные данные в ответе
3. **Jailbreak паттерны** — попытки обойти system prompt
4. **Запрещённый контент** — настраиваемые правила (регуляторные требования)
5. **Аномальные паттерны** — отклонение от нормального распределения ответов

## Связь с предыдущими находками

| Проект | Проблема | Immune System решает |
|--------|---------|---------------------|
| Clawdbot Audit (R14) | Prompt injection без защиты | Детектирует на уровне токена |
| Clawdbot Audit (R14) | Data leakage в ответах | Блокирует до отправки |
| openLight (R07) | Whitelist инструментов | Immune System = runtime защита |
| ADD Chronicles (R13) | Агент учится → может учиться плохому | Фильтр на всех итерациях |

## Архитектура как middleware

```python
# Паттерн применения:
async for token in llm.stream(prompt):
    safe_token = immune_system.check(token)  # 3ms
    if safe_token:
        yield safe_token
    else:
        yield immune_system.handle_violation(token)
```

Этот паттерн применим к любому streaming-агенту без изменения LLM-логики.

## Применение к Lorenzo

Lorenzo вызывает LLM в `improve_llm_enrich.py`, `improve_llm_qa.py`, `improve_llm_contact.py`.  
Immune System добавляется как **тонкий слой вокруг всех LLM-вызовов**:
- Защита от prompt injection при обработке внешних документов (MarkItDown → corpus)
- Детекция случайной записи API-ключей в docs/
- Аномалия в ответах → alert в Langfuse (R13)

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Immune System + Security Audit (R14)** | Audit выявляет уязвимости → Immune System закрывает их в runtime |
| **Immune System + Observability (R13)** | Каждое срабатывание Immune System трейсится в Langfuse |
| **Immune System + openLight (R07)** | openLight (tool whitelist) + Immune System (output filter) = двойная защита |
| **Immune System + ADD (R13)** | ADD feedback loop защищён от poisoning через иммунную систему |

## Контакт

- Статья: https://habr.com/ru/articles/996896/
- ⚠️ GitHub: уточнить через профиль автора на Хабре

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
