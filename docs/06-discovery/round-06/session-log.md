# Round 06 — Лог поисковой сессии

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** изображения/видео AI, CLI-агенты, специализированные MCP, GitHub-автоматизация

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| Ботинок | неизвестен | CLI agent / SSH / low-VRAM | `projects/botinok.md` |
| Memory MCP v0.8.0 | @ipiton | memory backbone / engineering artifacts | `projects/memory-mcp-v2.md` |
| Wunjo CE | @wladradchenko | video generation / multimodal / OSS | `projects/wunjo-ce.md` |
| DevClaw SaaS Pattern | неизвестен | GitHub Issues → agents / code-gen | `projects/devclaw-saas-pattern.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Memory MCP v2 | improve_passage_retrieval | Тип запроса → источник ранжирования | ⭐⭐⭐⭐⭐ |
| DevClaw паттерн | Lorenzo runner + GitHub Issues | Issue → improve_*.py → PR автоматически | ⭐⭐⭐⭐⭐ |
| Ботинок | Lorenzo runner (SSH) | Минимальный агент для CI/VPS без GUI | ⭐⭐⭐⭐ |
| Wunjo CE | Lorenzo карточки | Видео-превью для проектных описаний | ⭐⭐⭐ |

## Главная находка раунда

**Memory MCP v0.8.0** — проект из Round 01 (@ipiton/agent-memory-mcp) вырос в инженерную memory backbone.  
Статья вышла 2 дня назад. Это сигнал зрелости: из «semantic search tool» → «production memory layer».  
Классификация артефактов (runbook, postmortem, ADR) прямо применима к Lorenzo-карточкам.

**DevClaw SaaS Pattern** — архитектурный паттерн, который закрывает петлю Lorenzo:  
GitHub Issues → Claude агент → `improve_*.py` → PR. Это то, что `improve_workflow_v2.py` должен делать.

## Сводная карта R01–R06

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |

**Итого: 28 проектов, 18+ авторов**

## Что осталось на R07

- AI для научных публикаций (arXiv, цитирование, summarization)
- Decentralized / federated AI (без единого сервера)
- Русскоязычные образовательные AI (персональные тьюторы)
- Специализированные MCP-серверы (БД, файловые системы, бизнес-инструменты)
