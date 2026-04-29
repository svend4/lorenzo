---
title: "Local-first и P2P стек"
tags:
  - technology-combinations
date: 2026-04-29
---

# Local-first и P2P стек

<!-- toc -->
## Содержание

- [Упоминается в](#упоминается-в)
- [Упоминается в](#упоминается-в)
- [Связанные документы](#связанные-документы)
- [Связанные документы](#связанные-документы)

---


<!-- abstract-auto -->
> **Абстракт** (авто)
>
> 🎯 **Проблема:** Local-first и P2P стек - Сложные архитектурные → Claude Opus Проекты: Svyazi, CardIndex, Yjs --- локальная Qwen3:8B - Средние → облачная DeepSeek - Сложные архитектурные → Claude O
> 🔧 **Подход:** Local-first и P2P стек - Сложные архитектурные → Claude Opus Проекты: Svyazi, CardIndex, Yjs --- локальная Qwen3:8B - Средние → облачная DeepSeek - Сложные архитектурные → Claude O
> ✅ **Результат:** 2.2 Fault-tolerant агентский граф Router даёт fallback из коробки.
> 🏷️ **Ключевые слова:** `knowledge`, `technology`, `combinations`, `svyazi`, `articles`, `first`, `cardindex`, `graph`
>


<!-- summary -->
> - Сложные архитектурные → Claude Opus
**Проекты:** Svyazi, [[01-executive-summary|CardIndex]], Yjs

---
<!-- tags: rag, knowledge, ingestion, local-first, architecture, collaboration -->




локальная Qwen3:8B
- Средние → облачная [[memnet|DeepSeek]]
- Сложные архитектурные → Claude Opus
- Роутер перед каждым агентом, не после
Экономия: 80% запросов идут на дешёвые модели, Opus только для Planner-агента.
2.2 Fault-tolerant агентский граф Router даёт fallback из коробки. Если Opus недоступен → Sonnet → GPT-5.4 → локальная модель. Мультиагентная система перестаёт ломаться при отказе одного провайдера.
---
#### Комбинация 3: CRDT local-first × Svyazi CardIndex
Родители:
- CRDT / RON / Yjs (habr.com/ru/articles/534510/, habr.com/ru/articles/946722/) — conflict-free replicated data types, p2p синхронизация
- Svyazi [[01-executive-summary|CardIndex]] — YAML-структура профилей с хешами для дедупликации
Дети:
3.1 P2P-граф сообщества без центрального сервера Сейчас Svyazi — single-user система. С CRDT:
- Каждый участник ведёт локальный [[01-executive-summary|CardIndex]]
- Изменения синхронизируются p2p через Yjs
- Конфликты (два человека обновили профиль одного участника) мержатся автоматически
- Никакого центрального сервера — privacy by design
Для legal-community Max'а: каждый юрист в сообществе ведёт свой локальный граф дел и участников, но всё синхронизируется peer-to-peer. Данные не покидают машины участников.
3.2 Offline-first discovery Discovery-файл Svyazi (накопление неизвестного) синхронизируется через CRDT между устройствами:
- Ноутбук нашёл новую сущность → добавил в discovery
- Телефон оффлайн 2 дня
- При подключении автоматически получает обновления
- Модерация тоже распределённая
---
#### Комбинация 4: Парсинг с LLM × Graph-RAG × Правильная агентская архитектура
Родители:
- Парсинг с LLM (habr.com/ru/articles/892954/) — Structured Outputs, Pydantic, автоматическое извлечение структуры
- Graph-RAG (habr.com/ru/articles/871700/) — Microsoft Research, графы знаний вместо плоского RAG
- Durable state агенты (habr.com/ru/articles/1028290/)
Дети:
4.1 Self-building legal knowledge graph Агент читает новые решения Sozialgericht:
- Парсер LLM: извлекает сущности (судья, § закона, истец, ответчик, решение)
- Graph builder: строит

<!-- similar-docs -->

---

**Похожие документы:**
- [[01-agent-routing]] (сходство 0.12)
- [[05-benchmarks]] (сходство 0.11)
- [[02-knowledge-graphs]] (сходство 0.11)


<!-- see-also -->

---

**Смотрите также:**
- [[01-agent-routing]]
- [[05-benchmarks]]
- [[02-knowledge-graphs]]
- [[WORD_FREQ]]

<!-- backlinks-auto -->
## Упоминается в

- [[01-agent-routing|Агентные системы и роутинг]]
- [[05-benchmarks|Бенчмарки и производительность]]
- [[02-knowledge-graphs|Графы знаний и Legal AI]]
- [[README|Комбинирование технологий для новых свойств]]
## Упоминается в

- [[README|Комбинирование технологий для новых свойств]]

<!-- related-auto -->
## Связанные документы

- [[02-knowledge-graphs|Графы знаний и Legal AI]] _33%_
- [[05-benchmarks|Бенчмарки и производительность]] _29%_
- [[README|Комбинирование технологий для новых свойств]] _21%_
## Связанные документы

- [[05-benchmarks|Бенчмарки и производительность]] _33%_
- [[02-knowledge-graphs|Графы знаний и Legal AI]] _29%_
- [[README|Комбинирование технологий для новых свойств]] _25%_
- [[PRIORITIES|Приоритеты файлов]] _25%_
- [[01-agent-routing|Агентные системы и роутинг]] _21%_
- [[GLOSSARY|Глоссарий проектов]] _17%_
- [[HEATMAP|Тепловая карта тем]] _17%_
- [[SITEMAP|Карта репозитория Lorenzo]] _17%_
