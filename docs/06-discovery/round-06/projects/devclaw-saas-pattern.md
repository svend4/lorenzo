---
date: 2026-05-15
tags: [orchestration, knowledge, ingestion, architecture, collaboration]
state: normalized
---

# DevClaw SaaS Pattern («SaaS за 5 дней»)

<!-- toc-auto -->
<!-- tags: devclaw-saas-pattern, docs -->


<!-- summary -->
> Задачи ставятся через GitHub Issues (Markdown-спецификация) Claude-агент читает issue → пишет код → создаёт PR
 Задачи ставятся через GitHub Issues (Markdown-спецификация)
 Claude-агент читает issue → пишет код → создаёт PR
 DevClaw (OpenClaw plugin) оркеструет агентов
 Результат: работающий SaaS через 5 дней с нуля
Стек автора
 
Ключевое открытие


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** неизвестен (статья апрель 2026 — уточнить профиль)  
**Хабр:** https://habr.com/ru/articles/1005276/  
**GitHub:** не найден явно  
**Слой:** orchestration / developer-tools / code-generation  
**Дата:** апрель 2026  
**Уникальность:** Паттерн построения полного SaaS-продукта (FastAPI + React + PostgreSQL + Docker) **без написания кода вручную**: Claude-агенты управляют проектом через GitHub Issues как интерфейс задач. DevClaw = плагин OpenClaw (R04) специально для разработки.

## Что делает

- Задачи ставятся через GitHub Issues (Markdown-спецификация)
- Claude-агент читает issue → пишет код → создаёт PR
- DevClaw (OpenClaw plugin) оркеструет агентов
- Результат: работающий SaaS через 5 дней с нуля

## Стек автора

```
GitHub Issues → DevClaw → Claude agents → FastAPI + React + PostgreSQL + Docker
```

## Ключевое открытие

GitHub Issues как **декларативный интерфейс к агентам**: не IDE, не чат,  
а структурированная задача → агент её читает и выполняет.  
Это то же самое, что TRAIL spec (R04) решает на уровне MCP, но для GitHub workflow.

## Почему интересно для Svyazi

Lorenzo уже имеет `improve_github_issues.py`.  
Паттерн «GitHub Issues → агент-исполнитель» = готовая архитектура для  
автоматизации Связи: задача в issue → Lorenzo выполняет через `improve_*.py`.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DevClaw паттерн + Lorenzo runner** | GitHub Issue → `run_improve` → PR с результатом |
| **DevClaw паттерн + OpenClaw (R04)** | OpenClaw как платформа, DevClaw как плагин для Lorenzo |
| **DevClaw паттерн + AI Review (R03)** | Issue → код → автоматическое ревью → merge |
| **DevClaw паттерн + News System (R05)** | Новость → автоматически создаёт issue с карточкой |

## Контакт

- Статья: https://habr.com/ru/articles/1005276/ (апрель 2026)
- ⚠️ Нужно найти GitHub через профиль автора на Хабре

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
