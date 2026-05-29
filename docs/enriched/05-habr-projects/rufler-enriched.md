---
date: 2026-05-29
tags: [memory, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# Rufler


<!-- summary -->
> Раздел rufler-enriched формируется автоматически из данных репозитория. Rufler — это компонент оркестрации на уровне agent-swarm, предназначенный для декларативного управления сложными рабочими процессами.

> [!NOTE]
> Раздел `rufler-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: tags: [rufler, yaml, orchestration, agent-swarm, claude-code, declarative, mcp, token-accounting] До -->
<!-- tags: rufler, yaml, declarative, orchestration, agent-swarm, claude-code, mcp, depends_on, pause, resume -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\knowledge\rufler.md -->

# Rufler

Rufler — это компонент оркестрации на уровне agent-swarm, предназначенный для декларативного управления сложными рабочими процессами. Проект решает задачу координации распределённых агентов через YAML-конфигурации и обеспечивает взаимодействие с MCP-интерфейсами.

## Ключевые особенности

- **Декларативная оркестрация:** управление workflows через YAML-конфигурации с поддержкой зависимостей (depends_on), паузы и возобновления процессов
- **Интеграция с Claude Code и MCP:** встроенная поддержка агентских протоколов для расширения функциональности
- **Token-accounting:** мониторинг и учёт потребления токенов в рамках выполняемых операций
- **Agent-swarm архитектура:** поддержка координации множества агентов для параллельного выполнения задач

## Статус проекта

| Параметр | Значение |
|----------|---------|
| Язык/стек | YAML, Claude Code, MCP |
| Лицензия | MIT |
| Зрелость | Beta |
| Приоритет | 2 |
| Контакт | [@zodigancode](../../contacts/zodigancode.md) |

## Интеграция с Svyazi

Rufler является частью слоя оркестрации в архитектуре Svyazi 2.0, обеспечивая управление агентскими процессами на уровне выше базовых компонентов. Проект интегрируется с другими компонентами экосистемы, включая agent-memory-mcp и knowledge-space, для построения сложных многоагентных систем.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [rufler](docs\05-habr-projects\knowledge\rufler.md)_


## Использование
```bash
# Запуск
python scripts/improve_rufler_enriched.py
```
