---
state: normalized
---

# Proposal: Agentfs × Rufler


<!-- summary -->
> Раздел proposal-agentfs-x-rufler-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `proposal-agentfs-x-rufler-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Интеграция knowledge-слоя (Agentfs) и orchestration-слоя (Rufler): Agentfs предоставляет файловую си -->
<!-- tags: proposal, agentfs, rufler, knowledge, orchestration, integration -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\04-ai-collaborations\proposals\proposal-agentfs-x-rufler.md -->

## Что это

Proposal по интеграции knowledge-слоя (Agentfs) и orchestration-слоя (Rufler) в единую систему управления агентными пайплайнами. Agentfs предоставляет файловую систему знаний с рёбрами, Rufler — управляет оркестрацией агентов. Интеграция позволяет Rufler использовать граф Agentfs как рабочую память для навигации и координации.

## Ключевые особенности

- **Файловая система знаний:** Agentfs предоставляет структурированное хранилище знаний с рёбрами (связями между элементами)
- **Оркестрация пайплайнов:** Rufler управляет агентными пайплайнами и принимает решения о маршрутизации и выполнении
- **Граф как рабочая память:** Rufler навигирует по Agentfs-графу в качестве рабочего пространства оркестратора, обеспечивая контекстную осведомлённость

## Статус проекта

| Параметр | Значение |
|----------|----------|
| Язык/стек | — |
| Лицензия | — |
| Ссылка | — |

## Интеграция с Svyazi

Proposal представляет стратегическую интеграцию двух ключевых компонентов архитектуры: knowledge-слоя и orchestration-слоя. Такой подход обогащает базу знаний Svyazi 2.0 моделью распределённого управления агентами с явной репрезентацией контекста и зависимостей.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [proposal-agentfs-x-rufler](docs\04-ai-collaborations\proposals\proposal-agentfs-x-rufler.md)_


## Использование
```bash
# Запуск
python scripts/improve_proposal_agentfs_x_rufler_enriched.py
```
