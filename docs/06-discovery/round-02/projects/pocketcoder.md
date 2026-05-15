# PocketCoder

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Дмитрий Чащин / @Chashchin-Dmitry  
**Хабр:** https://habr.com/ru/articles/991022/  
**GitHub:** https://github.com/Chashchin-Dmitry/pocketcoder  
**Слой:** orchestration / coding-agent  
**Дата статьи:** февраль 2026  
**Уникальность:** Coding agent, заточенный под *любые* локальные модели — не привязан к конкретной. Реализует Agent Loop (думает → действует → смотрит на результат → решает что дальше) поверх любого Ollama/LM Studio endpoint.

## Что делает

- Agent Loop для задач кодирования: планирование → запись кода → запуск → анализ вывода → итерация
- Работает с любой локальной моделью через OpenAI-совместимый API
- Open source, MIT

## Почему интересно для Svyazi

Svyazi нужен coding layer — агент, который может писать и запускать скрипты обработки документов по запросу. PocketCoder — готовый Agent Loop под это.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **PocketCoder + AgentFS** | Coding agent с персистентной файловой памятью — помнит контекст задачи между сессиями |
| **PocketCoder + agent-memory-mcp** | Coding agent с MCP-памятью — каждый запуск обогащает базу знаний |
| **PocketCoder + Rufler** | YAML-описание задачи → PocketCoder её реализует → Rufler orchestrates результат |

## Контакт

- GitHub: https://github.com/Chashchin-Dmitry
- Комментарии к статье: https://habr.com/ru/articles/991022/
