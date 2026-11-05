---
date: 2026-06-05
tags: [orchestration, knowledge, ingestion, architecture, collaboration]
state: normalized
---

# knowledge-space[^knowledge-space]


<!-- summary -->
> Раздел knowledge-space-enriched формируется автоматически из данных репозитория.

> [!NOTE]
> Раздел `knowledge-space-enriched` формируется автоматически из данных репозитория.

<!-- alert-added -->

<!-- summary: Ключевой принцип: карточки написаны «для агентов, не людей» — каждая содержит максимум структурирова -->
<!-- tags: knowledge-space, agent, reference, cards, wiki-links, domains, research, inbox -->
<!-- enriched: 2026-05-29 by improve_llm_enrich.py -->
<!-- source: docs\05-habr-projects\knowledge\knowledge-space.md -->

# knowledge-space

## Что это
Проект создания пространства знаний с картами информации, оптимизированными для обработки агентами, а не людьми. Каждая карточка содержит максимум структурированной информации в минимуме текста, с явным указанием подводных камней (gotchas) и связями через wiki-links на связанные концепты.

## Ключевые особенности
- **Agent-first подход:** Карточки структурированы специально для чтения и обработки AI-агентами, что отличает их от традиционной документации
- **Система wiki-links:** Реализована навигация между связанными концептами и доменами через гибкую систему перекрестных ссылок
- **Минималистичный формат:** Максимум информации при минимуме текстового описания — оптимизация для быстрого парсинга

## Статус проекта
| Параметр | Значение |
|----------|----------|
| Лицензия | MIT |
| Зрелость | beta |
| Приоритет | 2 |
| Слой | knowledge/orchestration |
| Контакт | [@AnastasiyaW](../../contacts/anastasiyaw.md) |

## Интеграция с Svyazi
Проект образует ядро слоя knowledge в архитектуре Svyazi 2.0, обеспечивая структурированное хранилище карточек-знаний для работы распределённых агентов. Система wiki-links и доменов поддерживает навигацию по базе и интеграцию с другими компонентами через AgentFS и координацией на слое orchestration.
---
_Обогащено автоматически: 2026-05-29_
_Источник: [knowledge-space](docs\05-habr-projects\knowledge\knowledge-space.md)_


## Использование
```bash
# Запуск
python scripts/improve_knowledge_space_enriched.py
```
