---
date: 2026-05-29
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 30 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> Coreness Flow — composable AI-агент с plugin discovery и hot-reload Хабр: https://habr.com/ru/articles/1005176/
 Файл:  
 Хабр: https://habr.com/ru/articles/1005176/
 Слой: orchestration / memory / knowledge
 Уникальность: Plug-in = папка с config.json + Python модуль, auto-discovery без регис


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** Composable AI, AI документооборот, Synthetic data v2, Human-in-the-loop  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R29 session-log:
1. **Composable AI архитектуры** — модульные AI-системы, plug-in архитектура, hot-reload
2. **AI для документооборота** — VLM vs IDP бенчмарк, гибридная архитектура
3. **Synthetic data v2** — граф-анализ качества, 8 факторов, model collapse detection
4. **Human-in-the-loop** — трёхуровневая классификация действий, approval workflows

## Найденные проекты

### 1. Coreness Flow — composable AI-агент с plugin discovery и hot-reload
- **Файл:** `projects/coreness-flow-composable-agent.md`
- **Хабр:** https://habr.com/ru/articles/1005176/
- **Слой:** orchestration / memory / knowledge
- **Уникальность:** Plug-in = папка с config.json + Python модуль, auto-discovery без регистрации. Трёхслойная API шина (UI/Backend/Bus). Hot-reload: смена модели/ключа без restart. YAML-сценарии для пайплайнов без кода. Локальный RAG: BGE-M3 ONNX + Qdrant in-memory.
- **Дата:** март 2025

### 2. VLM vs IDP: бенчмарк на российских финансовых документах
- **Файл:** `projects/vlm-vs-idp-document-extraction.md`
- **Хабр:** https://habr.com/ru/companies/contentai/articles/958768/
- **Слой:** ingestion / analytics
- **Уникальность:** 764 синтетических RU финансовых документа (счета, УПД, накладные). Метрики PassThroughRate/FieldF1/CharF1. VLM галлюцинирует числа (-20% CharF1 vs IDP). Гибрид IDP+VLM: лучший результат (PassThrough 96%, FieldF1 0.95). IDP для структурных полей, VLM для контекстного обогащения.
- **Дата:** октябрь 2025

### 3. Сбербанк: граф-анализ качества синтетических данных для LLM
- **Файл:** `projects/sberbank-synthetic-data-graph-quality.md`
- **Хабр:** https://habr.com/ru/companies/sberbank/articles/901222/ + 909934/
- **Слой:** orchestration / analytics
- **Уникальность:** Двухчастная серия: 8 факторов качества синтетики + оригинальный граф-анализ (тексты → knowledge graphs → GCN/GAT/GraphSAGE → t-SNE). "Цифровой отпечаток" генератора в топологии графа. Детекция model collapse через variance графовых эмбеддингов.
- **Дата:** апрель–май 2025

### 4. LLMStart: HITL-фреймворк для production AI-агентов
- **Файл:** `projects/llmstart-hitl-agent-production.md`
- **Хабр:** https://habr.com/ru/companies/llmstart/articles/1015508/
- **Слой:** orchestration
- **Уникальность:** Трёхуровневая классификация действий: mandatory HITL (необратимые) / contextual (зависит от инициатора) / autonomous (только чтение). Последовательный пайплайн: content filter → rate limiter → HITL checkpoint → tool. Confidence thresholds: агент спрашивает при уверенности < 90%. LiteLLM Proxy + LangFuse для калибровки.
- **Дата:** март 2025

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-30/projects/coreness-flow-composable-agent.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-30/projects/vlm-vs-idp-document-extraction.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-30/projects/sberbank-synthetic-data-graph-quality.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-30/projects/llmstart-hitl-agent-production.md --top 4
```

Топ совпадений:
- Coreness Flow → Svyazi, Wikontic, Yodoca, NGT Memory
- VLM vs IDP → Svyazi, NGT Memory, Wikontic
- Synthetic Data → Svyazi, NGT Memory, Wikontic
- HITL → Svyazi, NGT Memory, Wikontic, Yodoca

## Кумулятивная карта (R01–R30)

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
| R30 | Coreness Flow composable, VLM vs IDP, синтетика граф-качество, HITL prod | архитектура, данные |

**Итого:** 124 проекта, 64+ авторов

## Темы для Round 31

1. **LLM в медицине и здравоохранении** — медицинские AI-агенты, анализ клинических данных, диагностика с LLM, compliance HIPAA/ФЗ-323
2. **Conversational AI production** — диалоговые системы в production: управление контекстом разговора, persona consistency, multi-turn memory
3. **AI для DevOps/Platform Engineering** — AI-первый подход к инфраструктуре: автогенерация Terraform/Helm, инфраструктура как разговор, GitOps с AI
4. **Explainable AI (XAI)** — объяснимость LLM-решений: SHAP для трансформеров, chain-of-thought как объяснение, audit trails для регуляторов

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
