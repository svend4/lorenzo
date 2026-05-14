# Round 31 — Session Log

**Дата:** май 2026  
**Тема:** LLM медицина, Conversational AI production, AI DevOps, Explainable AI  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R30 session-log:
1. **LLM в медицине и здравоохранении** — медицинские AI-агенты, анализ клинических данных, диагностика с LLM, compliance HIPAA/ФЗ-323
2. **Conversational AI production** — диалоговые системы в production: управление контекстом разговора, persona consistency, multi-turn memory
3. **AI для DevOps/Platform Engineering** — AI-первый подход к инфраструктуре: автогенерация Terraform/Helm, инфраструктура как разговор, GitOps с AI
4. **Explainable AI (XAI)** — объяснимость LLM-решений: SHAP для трансформеров, chain-of-thought как объяснение, audit trails для регуляторов

## Найденные проекты

### 1. Raft: Построение AI агентов в медицине (DBRM)
- **Файл:** `projects/raft-medical-ai-agents-dbrm.md`
- **Хабр:** https://habr.com/ru/companies/raft/articles/960388/
- **Слой:** orchestration / analytics
- **Уникальность:** Dynamic Behavior Reward Model: вместо RAG — иерархические метрики (safety/usefulness/completeness/relevance) через LLM-судей, откалиброванных на врачах. Пул специализированных судей по категориям. Cohen's Kappa мониторинг. Bootstrap ground truth (500 врачебных аннотаций → synthetic scaling). Явное соответствие ФЗ-323 и 152-ФЗ.
- **Дата:** октябрь 2025

### 2. VitalyOborin: Когнитивная память агента в SQLite (гроккинг + забывание)
- **Файл:** `projects/vitaly-oborin-conversational-memory-sqlite.md`
- **Хабр:** https://habr.com/ru/articles/1006622/
- **Слой:** memory / orchestration
- **Уникальность:** 4 типа нод (episodic/semantic/procedural/opinion) + 5 типов рёбер включая `supersedes` для эволюции фактов. Кривая забывания Эббингауза. Hot/slow path (~50ms). Гибридный поиск FTS5+KNN(256-dim Matryoshka)+граф через RRF. Session consolidation agent. **Автор уже в базе контактов Lorenzo** (создатель Yodoca + Wikontic).
- **Дата:** март 2025

### 3. sshaplygin: LLM-generated Terraform для Yandex Cloud
- **Файл:** `projects/llm-terraform-yandex-cloud-devops.md`
- **Хабр:** https://habr.com/ru/articles/1020612/
- **Слой:** orchestration / ingestion
- **Уникальность:** Claude Code генерирует Terraform + Go Cloud Function для Yandex Cloud. Event-driven автодеплой: `docker push` → Container Registry Trigger → Go Cloud Function → Yandex API → новая ревизия. Реальный Terraform HCL + Go handler код. Рефлексия об ограничениях AI-assisted IaC.
- **Дата:** апрель 2026

### 4. fanat503: Mechanistic Interpretability — поймать трансформер на читерстве
- **Файл:** `projects/mechanistic-interpretability-transformer-grokking.md`
- **Хабр:** https://habr.com/ru/articles/1008656/
- **Слой:** analytics
- **Уникальность:** Ручная хирургия матриц внимания Q×K^T по 4 слоям/4 головам: найдена отсутствующая Carry-over Head (доказательство читерства через Name Mover Head). Гроккинг: weight_decay=1.0 → compactные circuits → читаемые паттерны. GitHub с воспроизводимым кодом. Единственная статья 2024-2026 на Хабре с forensic-аудитом нейросети.
- **Дата:** март 2025

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-31/projects/raft-medical-ai-agents-dbrm.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-31/projects/vitaly-oborin-conversational-memory-sqlite.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-31/projects/llm-terraform-yandex-cloud-devops.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-31/projects/mechanistic-interpretability-transformer-grokking.md --top 4
```

Топ совпадений:
- DBRM medical → Svyazi, Rufler, mclaude, AgentFS
- Cognitive Memory (VitalyOborin) → NGT Memory, Wikontic, knowledge-space, research-docs
- Terraform+LLM DevOps → (нет совпадений — новая ниша)
- XAI Mechanistic → (нет совпадений — новая ниша)

## Кумулятивная карта (R01–R31)

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
| R31 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic | медицина, память, IaC, интерпретируемость |

**Итого: 128 проектов, 66+ авторов**

## Темы для Round 32

1. **AI для корпоративного поиска** — Enterprise RAG: поиск по внутренним знаниям компании, гибридные индексы (BM25 + плотный поиск), access control в RAG, freshness проблема
2. **LLM inference optimization** — KV cache compression, speculative decoding, batching стратегии, quantization для production; как сделать inference дешевле без потери качества
3. **AI для финансовой аналитики** — анализ финансовой отчётности через LLM, risk scoring, document extraction из годовых отчётов, NLP для МСФО/РСБУ
4. **Multi-modal production pipelines** — vision+text+audio в production: routing модальностей, preprocessing pipelines, мультимодальный RAG, latency optimization
