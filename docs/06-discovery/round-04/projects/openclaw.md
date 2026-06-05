# OpenClaw

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Peter Steinberger + community  
**Хабр:** https://habr.com/ru/articles/1020860/ (сравнение плагинов памяти)  
**GitHub:** https://github.com/openclaw/openclaw  
**Слой:** agent-platform / memory / multi-channel  
**Звёзд:** 68 000+ ⭐ (один из крупнейших OSS AI-агентов)  
**Уникальность:** Self-hosted персональный AI-агент с персистентной памятью как Markdown+YAML, работает через Telegram/WhatsApp/Discord/50+ каналов. Память хранится локально под `~/.openclaw`. Экосистема плагинов памяти: пять разных стратегий.

## Что делает

- Агент отвечает на любом канале (Telegram, WhatsApp, Slack, Discord, iMessage...)
- Память: долгосрочная, хранится как plain Markdown + YAML — читаемо, версионируемо
- 5 стратегий памяти на выбор (плагины):
  - **Lossless Claw** — полная история диалогов
  - **OpenViking** — полноценная база контекста
  - **ByteRover** — опыт работы → проектная база знаний
  - **MemPalace** — дословное хранение + архивный поиск
  - **LLM Wiki** — растущая wiki, агент сам её обновляет
- **SwarmClaw** (sub-project): multi-agent swarm runtime, 23+ LLM провайдера

## Почему интересно для Svyazi

OpenClaw — это production-ready платформа для того, что Svyazi строит с нуля. Главная ценность: **пять разных архитектур памяти** — это готовая типология для Lorenzo. Каждый плагин памяти = отдельный подход к хранению знаний агента.

## Возможные комбинации с Round 01

| Комбинация | Новое свойство |
|------------|----------------|
| **OpenClaw + agent-memory-mcp** | OpenClaw как Telegram-фронтенд, agent-memory-mcp как MCP-бэкенд памяти |
| **OpenClaw + knowledge-space** | Свыше 50 каналов доступа к базе знаний Svyazi |
| **OpenClaw LLM Wiki + Yodoca** | Граф-wiki: агент сам строит и обновляет граф из диалогов |
| **SwarmClaw + mclaude** | mclaude как orchestrator, SwarmClaw как swarm runtime |

## Контакт

- GitHub: https://github.com/openclaw
- Docs: https://docs.openclaw.ai/
- Awesome list: https://github.com/SamurAIGPT/awesome-openclaw
