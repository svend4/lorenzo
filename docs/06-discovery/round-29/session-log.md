---
date: 2026-05-28
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 29 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> X5 Tech Text2SQL с самопроверкой в production Хабр: https://habr.com/ru/companies/X5Tech/articles/949694/
 Файл:  
 Хабр: https://habr.com/ru/companies/X5Tech/articles/949694/
 Слой: orchestration / analytics
 Уникальность: Production NL2SQL X5 Group: Qwen2.5-72B + M-Schema (DDL с аннотациями типов и примерам


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** Code gen качество, Text2SQL самопроверка, AI мета-мониторинг, Кириллица в LLM  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R28 session-log:
1. **Code generation качество** — comprehension debt, деградация AI-кода, GitClear данные
2. **LLM для баз данных** — NL2SQL второго поколения с самопроверкой, production X5 Tech
3. **Агентные системы мониторинга** — AI наблюдает за AI, 5 классов аномалий, meta-monitoring
4. **Локализация и RU-специфика LLM** — кириллические токены, морфология, стоимость ~2×

## Найденные проекты

### 1. Comprehension Debt — скрытый технический долг AI-кода
- **Файл:** `projects/ai-code-comprehension-debt.md`
- **Хабр:** https://habr.com/ru/articles/1021068/
- **Слой:** orchestration / analytics
- **Уникальность:** GitClear: 211M строк кода 2020–2025: code churn ×2, рефакторинг −60%. Понятие «comprehension debt» — разрыв между размером кодовой базы и пониманием команды. Паттерны деградации AI-кода (copy-paste, context hallucination, test washing). Практика: TDD-принудиловка, `.claude/rules/`, хуки дедупликации.
- **Дата:** апрель 2025

### 2. X5 Tech Text2SQL с самопроверкой в production
- **Файл:** `projects/x5tech-text2sql-self-refinement.md`
- **Хабр:** https://habr.com/ru/companies/X5Tech/articles/949694/
- **Слой:** orchestration / analytics
- **Уникальность:** Production NL2SQL X5 Group: Qwen2.5-72B + M-Schema (DDL с аннотациями типов и примерами) + Self-Refinement Loop (traceback → автоматическая коррекция SQL). Few-shot через vector embeddings похожих запросов. ~76% точность на внутреннем бенчмарке. Тест PET-SQL ансамблей (+3%, 3× дороже).
- **Дата:** сентябрь 2025

### 3. AI мета-мониторинг: LLM анализирует поведение других LLM-агентов
- **Файл:** `projects/ai-meta-monitoring-langfuse.md`
- **Хабр:** https://habr.com/ru/articles/987230/
- **Слой:** orchestration / analytics
- **Уникальность:** Go backend + встроенный LLM классифицирует телеметрию агентов по 5 классам: performance_bottleneck, cost_spike, logical_loop, error_pattern, healthy_operation. Cursor Hooks → Langfuse → LLM-классификатор. Реальный "AI наблюдает за AI". Практические паттерны: read_file_loop, model_escalation, context_overflow, tool_misorder.
- **Дата:** январь 2026

### 4. Кириллица в LLM: русский стоит ~2× дороже английского
- **Файл:** `projects/cyrillic-llm-tokenization-russian.md`
- **Хабр:** https://habr.com/ru/articles/1032610/
- **Слой:** orchestration / analytics
- **Уникальность:** GPT-3.5/4 (`cl100k_base`) — только 435 кириллических токенов из 100К. GPT-4o расширил до 4660. Русская морфология: 2–3+ токенов/слово vs ~1 для английского. Порог приемлемости: < 1.7 токенов/слово. Бенчмарк: YandexGPT лучший (1.3 т/сл), Qwen3 хорош (1.5), cl100k плох (2.8).
- **Дата:** май 2025

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-29/projects/ai-code-comprehension-debt.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-29/projects/x5tech-text2sql-self-refinement.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-29/projects/ai-meta-monitoring-langfuse.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-29/projects/cyrillic-llm-tokenization-russian.md --top 4
```

Результаты → `docs/COLLAB_SUGGESTIONS.md`

Топ совпадений:
- Comprehension Debt → Svyazi, Rufler, mclaude, AgentFS
- Text2SQL → Svyazi, Yodoca
- Meta-Monitor → Svyazi, Wikontic
- Cyrillic → Svyazi, Yodoca

## Кумулятивная карта (R01–R29)

| Раунд | Тема | Ключевые проекты |
|-------|------|-----------------|
| R01 | Memory + Knowledge | AgentFS, MemNet, NGT Memory, Yodoca, knowledge-space, mclaude |
| R02 | Voice, parsing, YAML | голосовые интерфейсы, парсинг, Rufler YAML |
| R03 | Code review, fine-tuned LLM | code review AI, специализированные LLM |
| R04 | Agent platform, MCP protocol | агентные платформы, MCP-протокол |
| R05 | Autonomous pipeline, Russian NLP | автономные пайплайны, RU NLP |
| R06 | Video AI, CLI agents, GitHub automation | видео AI, CLI агенты |
| R07 | Multi-agent arch, agent safety, MCP pipeline | мультиагентные системы |
| R08 | Codebase MCP, scientific ingestion, edu AI | инструменты разработчика |
| R09 | GraphRAG, decentralized AI, coding agent | GraphRAG, децентрализованный AI |
| R10 | Viral simulation, self-hosted stacks, Rust | self-hosted, производительность |
| R11 | Desktop agents, edge AI, voice embedded | edge AI, встроенные системы |
| R12 | Data analytics AI, audio gen, vector DBs | аналитика данных, векторные БД |
| R13 | Observability, ADD, self-healing tests, OCR | наблюдаемость, тесты, OCR |
| R14 | Context Engineering, DSPy, AI security, MarkItDown | контекст, безопасность |
| R15 | Code review AI, Text2SQL, fine-tuning, LLM security | код ревью, SQL, файнтюн |
| R16 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval | мониторинг LLM, ASR |
| R17 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | CoT, граф знаний, DBA |
| R18 | Agentic RAG, synthetic data, incident AI, RU embeddings | RAG, синтетика, FRIDA |
| R19 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | мультимодальный RAG |
| R20 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | тесты, reasoning |
| R21 | Multi-agent case, A2A protocol, LLM privacy, RU classification | A2A, приватность |
| R22 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | legal tech, безопасность |
| R23 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | enterprise AI, безопасность |
| R24 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | производственные системы |
| R25 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | отраслевые решения |
| R26 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт | BI/аналитика, финтех |
| R27 | LLM кибербезопасность, персональный AI, 5-фазный оркестратор, RAG тесты | безопасность, DevEx |
| R28 | Volga streaming ML, мультимодальный VLM, LLM Judge, federated edge | infrastructure, качество |
| R29 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица LLM | качество, RU-специфика |

**Итого:** 120 проектов, 62+ авторов

## Темы для Round 30

1. **Composable AI архитектуры** — модульные AI-системы: plug-in модели, горячая замена компонентов, version management для ML-артефактов
2. **AI для документооборота** — интеллектуальная обработка документов: извлечение данных из PDF/Word, структурирование, классификация, маршрутизация
3. **Simulation и синтетические данные v2** — продвинутая генерация синтетических данных: domain adaptation, quality scoring, distillation датасетов
4. **Агентные workflows с человеком в контуре** — Human-in-the-loop паттерны: когда агент должен остановиться и спросить, approval workflows, confidence thresholds

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
