# Round 10 — Лог поисковой сессии

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** вирусный multi-agent движок, self-hosted AI стеки, Rust-инструменты

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| MiroFish | @666ghj (BaiFu) | multi-agent simulation / world engine | `projects/mirofish.md` |
| n8n AI Stack (15 мин) | неизвестен | workflow / self-hosted / one-command | `projects/n8n-ai-stack.md` |
| Self-hosted AI Platform | неизвестен | infrastructure / RAG / docker | `projects/self-hosted-ai-platform.md` |
| Rustsn | сообщество | Rust code gen / LLM + compiler loop | `projects/rustsn.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| MiroFish + Lorenzo corpus | — | 2483 карточки → агенты OSS-разработчиков → симуляция реакции сообщества | ⭐⭐⭐⭐⭐ |
| MiroFish-Offline + GraphRAG (R09) | Neo4j + Ollama | Локальная симуляция без облака, граф из Lorenzo | ⭐⭐⭐⭐⭐ |
| n8n Stack + News System (R05) | 5-агентный пайплайн | Автономная news система за 15 мин (не 1.5 месяца) | ⭐⭐⭐⭐ |
| Self-hosted + Lorenzo gateway | gateway.py | Open WebUI + Qdrant + HTTPS поверх gateway → полный UI | ⭐⭐⭐⭐ |
| Rustsn + improve_passage_retrieval | BM25 | BM25 на Rust → Python bindings → 10× быстрее | ⭐⭐⭐ |

## Главная находка раунда

**MiroFish** — самый вирусный AI-проект за все 10 раундов:  
GitHub Global Trending #1, 33 000+ звёзд, $4.1M инвестиций за 24 часа.  
Написан за 10 дней с Claude Code студентом из Пекина.

Уникальная применимость к Lorenzo: **Lorenzo corpus → seed для MiroFish** →  
симуляция того, как OSS-сообщество реагирует на проект Svyazi.  
Это валидация идей без реального запуска.

**n8n AI Stack** + **Self-hosted AI Platform** вместе дают полный production стек:  
один разворачивает workflow-движок, другой — RAG с UI. Оба через Docker.

## Сводная карта R01–R10

| Раунд | Проектов | Ключевая тема | Лучшая находка |
|-------|----------|---------------|----------------|
| R01 | 9 | Memory + Knowledge | AgentFS, Yodoca, knowledge-space |
| R02 | 6 | Voice, parsing, YAML | Coreness Flow, Ирина, Dedoc |
| R03 | 3 | Code review, fine-tuned LLM | DevOps LLM паттерн |
| R04 | 3 | Agent platform, MCP protocol | TRAIL spec, OpenClaw |
| R05 | 3 | Autonomous pipeline, Russian NLP | News System паттерн, Natasha |
| R06 | 4 | Video AI, CLI agents, GitHub automation | Memory MCP v2, DevClaw паттерн |
| R07 | 4 | Multi-agent architecture, agent safety | openLight принцип, 9-агентный паттерн |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI | SocratiCode, Paper2Agent |
| R09 | 4 | GraphRAG, decentralized AI, coding agent | GraphRAG pipeline, HMP, OpenCode |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust | MiroFish, n8n AI Stack |

**Итого: 44 проекта, 24+ авторов**

## Что осталось на R11

- AI для личной продуктивности и GTD (не просто заметки, а агент-планировщик)
- Специализированные агенты для кода (security review, performance profiling)
- Русскоязычные голосовые агенты 2026 (апдейты Ирины из R02)
- AI + IoT / edge computing (агент на устройстве)
