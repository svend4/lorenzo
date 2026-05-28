---
date: 2026-05-28
tags: [memory, orchestration, ingestion, architecture, collaboration]
state: normalized
---

# Self-Aware MCP Server
<!-- tags: self-aware-mcp, docs -->


<!-- summary -->
> Автор: @vuguzum (Хабр + GitHub) Хабр: https://habr.com/ru/articles/1007122/ GitHub: https://github.com/vuguzum/self-aware-mcp-server
Хабр: https://habr.com/ru/articles/1007122/  
GitHub: https://github.com/vuguzum/self-aware-mcp-server  
Слой: MCP / contextual-grounding  
Дата: март 2026  
Уникальность: MCP-сервер, который даёт агенту ответы на «W


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** @vuguzum (Хабр + GitHub)  
**Хабр:** https://habr.com/ru/articles/1007122/  
**GitHub:** https://github.com/vuguzum/self-aware-mcp-server  
**Слой:** MCP / contextual-grounding  
**Дата:** март 2026  
**Уникальность:** MCP-сервер, который даёт агенту ответы на «What, Where, When, How Much»: местоположение, текущее время, ОС, точные вычисления. Маленький (4 инструмента), но решает фундаментальную проблему: агент работает не в вакууме, а в контексте реального мира. Написан в агент-режиме (GLM-5).

## Что делает

Четыре инструмента:
- `get_current_location` — контекст местоположения («Москва» или «Home office, Bali»)
- `get_current_time` — точное время с таймзоной
- `get_os_info` — ОС, версия, железо
- `calculate` — точные вычисления (без галлюцинаций LLM на арифметике)

## Почему интересно для Svyazi

Lorenzo сейчас работает без временного и пространственного контекста. `get_current_time` + Lorenzo = датирование документов, дайджесты «за сегодня», агенд «что изменилось с прошлого запуска». Три строки контекста меняют качество взаимодействия с агентом.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **Self-Aware MCP + Lorenzo MCP-серверы** | Добавить в `.mcp.json` как 7-й сервер: все инструменты Lorenzo получают временной контекст |
| **Self-Aware MCP + improve_digest_auto** | Дайджест с точным временем: «изменения за последние 24 часа с 14:00 12 мая» |
| **Self-Aware MCP + update_contact_status** | Заметки к контактам автоматически датируются точным временем |
| **Self-Aware MCP + agent-memory-mcp** | Воспоминания привязываются к времени и месту |

## Быстрое подключение к Lorenzo

```bash
claude mcp add self-aware python \
  /path/to/self-aware-mcp-server/server.py \
  --scope project
```

## Контакт

- GitHub: https://github.com/vuguzum
- Habr: https://habr.com/ru/users/vuguzum/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
