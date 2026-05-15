---
date: 2026-05-15
tags: [memory, rag, orchestration, security, knowledge]
state: normalized
---

# Round 32 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> МТС RAG: гибридный поиск для корпоративного AI-помощника Хабр: https://habr.com/ru/companies/ru_mts/articles/970476/
 Файл:  
 Хабр: https://habr.com/ru/companies/ru_mts/articles/970476/
 Слой: ingestion / orchestration / knowledge
 Уникальность: Точная формула ранжирования:   + буст-факторы (заголовок ×1.2,


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** Enterprise RAG, LLM inference optimization, финансовая аналитика, мультимодальный production  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R31 session-log:
1. **AI для корпоративного поиска** — Enterprise RAG: поиск по внутренним знаниям компании, гибридные индексы (BM25 + плотный поиск), access control в RAG, freshness проблема
2. **LLM inference optimization** — KV cache compression, speculative decoding, batching стратегии, quantization для production; как сделать inference дешевле без потери качества
3. **AI для финансовой аналитики** — анализ финансовой отчётности через LLM, risk scoring, document extraction из годовых отчётов, NLP для МСФО/РСБУ
4. **Multi-modal production pipelines** — vision+text+audio в production: routing модальностей, preprocessing pipelines, мультимодальный RAG, latency optimization

## Найденные проекты

### 1. МТС RAG: гибридный поиск для корпоративного AI-помощника
- **Файл:** `projects/mts-enterprise-rag-hybrid-search.md`
- **Хабр:** https://habr.com/ru/companies/ru_mts/articles/970476/
- **Слой:** ingestion / orchestration / knowledge
- **Уникальность:** Точная формула ранжирования: `0.7×vector + 0.3×BM25` + буст-факторы (заголовок ×1.2, свежесть ×1.1, решения ×1.5). Полностью on-premise (BGE-m3 + Cotype Pro 2). Zero-downtime инкрементальная индексация через content-hash. Делегирование ACL источникам (Confluence/Jira).
- **Дата:** декабрь 2025

### 2. vLLM Production Stack: KV-cache, FP8, Speculative Decoding
- **Файл:** `projects/vllm-production-stack-inference-optimization.md`
- **Хабр:** https://habr.com/ru/articles/1016062/
- **Слой:** orchestration / ingestion
- **Уникальность:** Единственная RU статья 2025 с реальными Kubernetes YAML + GuideLLM бенчмарками BF16 vs FP8 (~3x снижение KV-cache памяти). Покрывает весь стек: prefix caching → tensor parallelism → FP8 quantization → speculative decoding → LMCache cross-request reuse.
- **Дата:** март 2025

### 3. Amvera: PDF pipeline для анализа финансовых отчётов
- **Файл:** `projects/llm-financial-pdf-analytics-pipeline.md`
- **Хабр:** https://habr.com/ru/companies/amvera/articles/949966/
- **Слой:** ingestion / analytics
- **Уникальность:** End-to-end pipeline: requests+BS4 discovery → PyMuPDF extraction → LLaMA 8B с двумя режимами промптинга (структурированные метрики EBITDA/выручка + регуляторные риски) → asyncio + Telegram рассылка. GitHub с рабочим кодом.
- **Дата:** сентябрь 2025

### 4. Авито: мультимодальный VLM pipeline для обогащения поиска
- **Файл:** `projects/avito-multimodal-vlm-search-enrichment.md`
- **Хабр:** https://habr.com/ru/companies/avito/articles/1024136/
- **Слой:** ingestion / orchestration / analytics
- **Уникальность:** Production VLM (Qwen2.5-VL-7B "A-Vision") генерирует русские описания объявлений по фото: 1500 объявлений/мин, 21 нода, 3 ДЦ. Категорийные LoRA (0.1-1% параметров), vLLM continuous batching + PagedAttention, Cyrillic tokenizer rebuild (-50% генерации). Queue-based pipeline (Worker → QaaS → LLM Worker).
- **Дата:** апрель 2026

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-32/projects/mts-enterprise-rag-hybrid-search.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-32/projects/vllm-production-stack-inference-optimization.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-32/projects/llm-financial-pdf-analytics-pipeline.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-32/projects/avito-multimodal-vlm-search-enrichment.md --top 4
```

Результаты: все 4 — новые ниши без совпадений в текущей базе проектов Lorenzo.  
Вывод: R32 охватывает production-инфраструктурный слой (inference, multimodal, corporate RAG), слабо представленный в R01-R31.

## Кумулятивная карта (R01–R32)

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
| R31 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic | медицина, память, IaC |
| R32 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM | production infra |

**Итого: 132 проекта, 68+ авторов**

## Темы для Round 33

1. **AI code agents нового поколения** — мультифайловый рефакторинг, автоматическая генерация тестов, PR automation, параллельные агенты для одной задачи, MCP-first разработка
2. **LLM для инженерии данных** — генерация dbt/SQL/Spark пайплайнов через LLM, data quality checks с AI, ETL через агентов, автоматическая документация датасетов
3. **Суверенный AI (on-premise)** — self-hosted LLM стеки без зависимости от OpenAI/Anthropic, частный inference в контуре компании, российские LLM в production, Ollama/vLLM+локальные модели
4. **LLM alignment и red-teaming** — red-teaming LLM в российском контексте, jailbreaking устойчивость, конституциональный AI, evaluation безопасности, audit trails для регуляторов

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
- [Решения](../../DECISIONS.md)
