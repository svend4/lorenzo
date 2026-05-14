# Round 12 — Лог поисковой сессии

**Дата:** 2026-05-12  
**Статус:** ✅ Завершён  
**Тема:** AI-инструменты для аналитики данных, генерация музыки/аудио, векторные базы данных, IDE AI-агенты

## Найденные проекты

| Проект | Автор | Ниша | Файл |
|--------|-------|------|------|
| HeartMuLa | команда HeartMuLa | audio-gen / music / Apache-2.0 | `projects/heartmula.md` |
| Veai | команда Veai | IDE-agent / JetBrains / MCP | `projects/veai-ide-agent.md` |
| BI Agent Pattern | аноним (Хабр) | analytics / orchestration / architectural | `projects/bi-agent-pattern.md` |
| Vector DB Guide | аноним (Хабр) | vector-db / knowledge / reference | `projects/vector-db-guide.md` |

## Лучшие комбинации раунда

| Новый проект | + Из раундов | Новое свойство | Сила |
|-------------|--------------|----------------|------|
| Veai + Lorenzo MCP | MCP (multiple) | JetBrains IDE → improve_*.py через MCP из IDE | ⭐⭐⭐⭐⭐ |
| BI Pattern + improve_llm_qa | Stage 3 LLM | QA-агент отвечает на вопросы о метриках Lorenzo (HEALTH, KPI) | ⭐⭐⭐⭐⭐ |
| Vector DB Guide → Qdrant | SocratiCode (R08) | SocratiCode уже использует Qdrant — прямой апгрейд Lorenzo corpus | ⭐⭐⭐⭐ |
| HeartMuLa + Ирина (R02) | Voice pipeline R11 | Полный аудио-стек: STT (Ирина) + генерация музыки (HeartMuLa) | ⭐⭐⭐ |
| Vector DB + GraphRAG (R09) | Neo4j pipeline | Neo4j (граф) + pgvectorscale (вектор) = полный GraphRAG стек | ⭐⭐⭐⭐ |

## Главные находки раунда

**Veai** — первый за 12 раундов AI-агент для JetBrains IDE из реестра российского ПО. Поддерживает MCP, что означает прямое подключение к Lorenzo MCP-серверам из IntelliJ IDEA. Архитектура «shared skills» совпадает с `improve_*.py` + openLight (R07).

**BI Agent Pattern** — статья формулирует принцип, который Lorenzo должен реализовать: вместо статичных HEALTH.md, KPI.md, METRICS.md — агент, отвечающий на вопросы. `improve_llm_qa.py` + семантический контекст метрик = шаг к BI-агенту над Lorenzo.

**Vector DB Guide** — практическая карта для будущего масштабирования: ChromaDB при росте > 10K карточек, pgvectorscale при PostgreSQL-стеке. Особо актуально: SocratiCode (R08) уже использует Qdrant — можно унифицировать стек.

**HeartMuLa** — уникальная в R12: генерация, а не обработка. Apache 2.0 = свободная лицензия. Экосистема HeartCodec + HeartCLAP открывает мультимодальный поиск по аудио.

## Сводная карта R01–R12

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
| R11 | 4 | Desktop agents, edge AI, voice embedded | Союз (MCP desktop), RPi+Ирина voice pipeline |
| R12 | 4 | Data analytics AI, audio gen, vector DBs | Veai IDE agent, BI Agent Pattern |

**Итого: 52 проекта, 28+ авторов**

## Что осталось на R13

- **Мониторинг и observability для AI** — LangFuse, Phoenix, Weights & Biases open альтернативы
- **AI для тестирования кода** — automated test generation, mutation testing с LLM
- **Federated learning / privacy ML** — обучение без передачи данных (open source)
- **Document AI / IDP** — intelligent document processing, структурирование неструктурированного (русскоязычные)
