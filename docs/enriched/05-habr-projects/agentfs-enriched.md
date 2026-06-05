---
date: 2026-06-05
tags: [memory, orchestration, security, knowledge, ingestion]
state: normalized
---

# AgentFS


<!-- summary -->
> Раздел agentfs-enriched формируется автоматически из данных репозитория. AgentFS — компонент слоя knowledge/filesystem в экосистеме Svyazi 2.0, разработанный для управления персистентным состоянием агентов.

> [!NOTE]
> Раздел `agentfs-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Параметр | Значение | Упоминаний в репо | 1384 | Слой | knowledge/filesystem | Статус связи | не пис -->
<!-- tags: agentfs, agent, filesystem, obsidian, knowledge, persistent-state, security, compile -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\knowledge\agentfs.md -->

# AgentFS

## Что это

AgentFS — компонент слоя knowledge/filesystem в экосистеме Svyazi 2.0, разработанный для управления персистентным состоянием агентов. Проект находится на стадии alpha и предназначен для интеграции с Obsidian и системами управления знаниями.

## Ключевые особенности

- **Слой архитектуры:** Размещён в слое knowledge/filesystem, обеспечивая файловую абстракцию для работы с состоянием агентов
- **Высокая упоминаемость:** 1384 упоминания в репозитории указывают на широкое использование в кодовой базе
- **Безопасность и ограничения:** Документация содержит описание рисков и ограничений, требующих изучения перед принятием архитектурных решений

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Лицензия | MIT |
| Зрелость | alpha |
| Приоритет | 1 |
| Контакт | @kksudo |
| Последнее обновление | 2026-05-10 |

## Интеграция с Svyazi

AgentFS встроен в знаниевый слой Svyazi 2.0 и взаимодействует с проектами knowledge-space, mclaude, agent-memory-mcp и Wikontic. Компонент критичен для обеспечения персистентного состояния и безопасности в распределённой системе управления агентами.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [agentfs](docs\05-habr-projects\knowledge\agentfs.md)_


## Использование
```bash
# Запуск
python scripts/improve_agentfs_enriched.py
```
