---
date: 2026-05-28
tags: [rag, orchestration, ingestion, architecture, collaboration]
state: normalized
---

# n8n AI Stack — всё за 15 минут

<!-- toc-auto -->
<!-- tags: n8n-ai-stack, docs -->


<!-- summary -->
> Почему важно для Svyazi Автономная News System (R05) автора заняла 1.5 месяца переписки с n8n.
Автономная News System (R05) автора заняла 1.5 месяца переписки с n8n.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** неизвестен (статья декабрь 2025)  
**Хабр:** https://habr.com/ru/articles/973776/  
**GitHub:** не найден явно (Docker Compose шаблон)  
**Слой:** workflow / orchestration / self-hosted / deploy  
**Дата:** декабрь 2025  
**Уникальность:** Docker Compose шаблон разворачивает **полный AI-стек за 15 минут** вместо нескольких часов: n8n + Redis + Flowise + Qdrant + PostgreSQL + Ollama + Crawl4AI + Grafana + LangFuse + Portainer. Решает проблему "каждый деплой на новый сервер — несколько часов".

## Стек (10 компонентов одной командой)

| Компонент | Роль |
|-----------|------|
| **n8n** | Workflow automation (с очередями через Redis) |
| **Redis** | Очереди + кеш промежуточных результатов |
| **Flowise** | LLM-логика и chains |
| **Qdrant** | Векторная БД (Rust, HNSW) |
| **PostgreSQL** | Данные + бэкапы |
| **Ollama** | Локальные модели + эмбеддинги |
| **Crawl4AI** | Веб-парсинг для RAG |
| **Grafana** | Мониторинг всего стека |
| **LangFuse** | Трейсинг AI-агентов |
| **Portainer** | Управление контейнерами |

## Практический кейс

Telegram-бот, отвечающий на вопросы на основе данных с конкретных сайтов.  
Данные постоянно обновляются через Crawl4AI → Qdrant → n8n-workflow → Telegram.

## Почему важно для Svyazi

Автономная News System (R05) автора заняла 1.5 месяца переписки с n8n.  
Этот шаблон сокращает деплой того же стека до 15 минут.  
Lorenzo + n8n AI Stack = полный Svyazi-стек «под ключ» без DevOps-боли.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **n8n stack + Lorenzo MCP** | Lorenzo-инструменты как n8n-узлы в workflow |
| **n8n stack + News System (R05)** | 5-агентный пайплайн новостей за 15 мин, не 1.5 месяца |
| **n8n stack + Coreness Flow (R02)** | Coreness YAML-события → n8n-триггеры |
| **n8n stack + openLight (R07)** | Инфра-агент через n8n → мониторинг без кастомного кода |

## Контакт

- Статья: https://habr.com/ru/articles/973776/ (декабрь 2025)
- ⚠️ Нужно найти GitHub шаблона через профиль автора


## Использование
```bash
# Запуск
python scripts/improve_n8n_ai_stack.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
