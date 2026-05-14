# Coreness Flow

**Автор:** @Vensus137  
**Хабр (Flow):** https://habr.com/ru/articles/1005176/  
**Хабр (Platform):** https://habr.com/ru/articles/986354/  
**GitHub:** https://github.com/Vensus137/Coreness-Flow  
**Слой:** orchestration / workflow-engine  
**Дата:** 2025-2026 (активный проект, две статьи)  
**Уникальность:** Event-driven YAML-агент без облака. Реагирует на события (сообщение, webhook, cron), выполняет цепочки действий из конфига. Меняешь поведение агента — меняешь YAML, не код. Self-hosted платформа «от одного бота к сотням».

## Что делает

- Агент описывается YAML-сценариями (не кодом)
- Event triggers: webhook, cron, message, custom
- Агентский роутинг через системные сценарии поверх общего механизма
- Self-hosted, Windows-first, но портируемый
- Платформа Coreness: управление множеством агентов из одного места

## Почему интересно для Svyazi

Это прямой конкурент/партнёр для Rufler (zodigancode) — оба декларативные YAML-оркестраторы. Coreness более production-ready и event-driven, Rufler более DSL-ориентированный. Вместе — полный declarative stack.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **Coreness Flow + Rufler** | Coreness как runtime (запускает события), Rufler как DSL (описывает логику) — разделение ответственностей |
| **Coreness Flow + mclaude** | mclaude как LLM-мозг, Coreness как event-шина — агент реагирует на внешние события |
| **Coreness Flow + agent-memory-mcp** | Каждое событие пишет в MCP-память → агент обучается на истории событий |
| **Coreness Platform + knowledge-space** | Множество агентов, каждый отвечает за свою секцию базы знаний |

## Контакт

- GitHub: https://github.com/Vensus137
- Habr: https://habr.com/ru/users/Vensus137/ (судя по статьям)
