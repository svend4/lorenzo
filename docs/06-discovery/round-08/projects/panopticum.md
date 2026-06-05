---
state: normalized
---

# Panopticum (единый интерфейс для баз данных)

<!-- toc-auto -->
<!-- tags: panopticum, docs -->


<!-- summary -->
> Хабр: https://habr.com/ru/articles/996620/ GitHub: не найден явно (Docker Hub: sharque/panopticum)
Хабр: https://habr.com/ru/articles/996620/  
GitHub: не найден явно (Docker Hub: sharque/panopticum)  
Слой: developer-tools / databases / unified-interface  
Дата: март 2026  
Уникальность: Единый веб-интерфейс для PostgreSQL, Mong


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @sharque  
**Хабр:** https://habr.com/ru/articles/996620/  
**GitHub:** не найден явно (Docker Hub: sharque/panopticum)  
**Слой:** developer-tools / databases / unified-interface  
**Дата:** март 2026  
**Уникальность:** Единый веб-интерфейс для PostgreSQL, MongoDB, Redis и других баз данных — вместо набора разрозненных инструментов. Запускается через Docker, работает локально. Решает проблему «зоопарка консолей» при работе с несколькими СУБД.

## Что умеет

- Единый UI для PostgreSQL, MongoDB, Redis и других
- Docker-деплой — запускается одной командой
- Работает полностью локально (нет облачных зависимостей)
- Переключение между БД в одном интерфейсе

## Контекст (из поиска по MCP + БД)

В 2025–2026 году каждый вендор СУБД выпустил свой MCP-сервер:
- OLAP: ClickHouse, Snowflake, Firebolt
- SQL: Postgres (несколько unofficial), YugabyteDB, Oracle
- NoSQL: MongoDB, Neo4j, Redis
- Cloud: Amazon, Microsoft, Google multi-system MCP

Panopticum решает ту же проблему на UI-уровне: не нужен отдельный клиент для каждой СУБД.

## Почему важно для Svyazi

Lorenzo использует SQLite (audit.db) и JSON-индексы.  
При масштабировании на PostgreSQL (как в News System, R05) — нужен единый интерфейс.  
Panopticum + MCP-серверы СУБД = полный стек: агент через MCP → данные, человек через Panopticum → те же данные.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Panopticum + Lorenzo MCP servers** | Человек видит данные Lorenzo через единый UI |
| **Panopticum + TRAIL spec (R04)** | Panopticum как admin-слой над MCP-пайплайном БД |
| **Panopticum + News System (R05)** | PostgreSQL news DB + Redis cache в одном интерфейсе |
| **Panopticum + openLight (R07)** | Мониторинг инфраструктуры + просмотр всех БД агента |

## Контакт

- Docker Hub: sharque/panopticum
- Статья: https://habr.com/ru/articles/996620/ (март 2026)
- ⚠️ Нужно найти GitHub @sharque


## Использование
```bash
# Запуск
python scripts/improve_panopticum.py
```

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
