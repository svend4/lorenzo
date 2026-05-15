# Round 27 — Session Log

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** LLM кибербезопасность, персональный AI с памятью, мультиагентное планирование, AI DevEx  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Темы из R26 session-log:
1. **LLM кибербезопасность** — SAST с LLM, анализ уязвимостей, специализированный fine-tuning
2. **Персональный AI с локальной памятью** — долгосрочная память, персонализация без облака
3. **Мультиагентное планирование** — оркестратор с откатами, иерархия агентов, Skills Library
4. **AI DevEx** — генерация тестов с RAG, PSI-анализ кода, developer productivity

## Найденные проекты

### 1. DerAI — Solar Security: SAST + fine-tuned LLM
- **Файл:** `projects/solar-security-derai-sast.md`
- **Хабр:** https://habr.com/ru/companies/solarsecurity/articles/1031718/
- **Слой:** orchestration / analytics / security
- **Уникальность:** Собственная LLM на 7-летней базе реальных уязвимостей Solar appScreener. Два модуля: DerTriage (классификация, -73% false positives) + DerCodeFix (патчи). Бенчмарк: DerAI > GPT-5.2 > DeepSeek на 12K реальных находок Java/Python. Доменная экспертиза > масштаб модели.
- **Дата:** май 2025

### 2. AI-агент с долгосрочной памятью: личный аналитик здоровья
- **Файл:** `projects/personal-ai-longterm-memory.md`
- **Хабр:** https://habr.com/ru/articles/1007940/
- **Слой:** memory / orchestration / knowledge
- **Уникальность:** Трёхслойная архитектура: оперативная (сессия) + эпизодическая (PostgreSQL+pgvector) + семантическая (MEMORY.md — паттерны за месяцы). Memory Synthesizer пишет поведенческие инсайты в постоянный файл. 14 инструментов, Docker Compose, Telegram-бот, полностью локально.
- **Дата:** март 2026

### 3. Оркестратор: 5-фазная структура воркеров, meta-agent-v3
- **Файл:** `projects/orchestrator-5phase-multiagent.md`
- **Хабр:** https://habr.com/ru/articles/975376/
- **Слой:** orchestration
- **Уникальность:** Воркеры в полной изоляции контекста (только JSON-план, без chat history) + 5-фазный цикл (read→do→validate→report→return). Откат структурно встроен. meta-agent-v3 генерирует нового агента за 2–3 мин из 500-строчного шаблона. 33 агента в production.
- **Дата:** декабрь 2025

### 4. Сбербанк: RAG + LLM автогенерация тестов в JetBrains IDE
- **Файл:** `projects/sberbank-rag-test-generation.md`
- **Хабр:** https://habr.com/ru/companies/sberbank/articles/1011830/
- **Слой:** orchestration / analytics
- **Уникальность:** PSI (Program Structure Interface) обходит Java AST вместо regex — извлекает @Step/@TmsLink аннотации. RAG строит few-shot промпт из реальных тестов проекта. Двойная валидация: LLM self-check + PSI синтаксис. 68% тестов без правок vs 12% zero-shot.
- **Дата:** март 2025

## Поиск аналогий в Lorenzo (collab_finder)

```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-27/projects/solar-security-derai-sast.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-27/projects/personal-ai-longterm-memory.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-27/projects/orchestrator-5phase-multiagent.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-27/projects/sberbank-rag-test-generation.md --top 4
```

Результаты → `docs/COLLAB_SUGGESTIONS.md`

Топ совпадений:
- DerAI → Svyazi, mclaude, Rufler, NGT Memory
- Personal AI → Svyazi, agent-memory-mcp, NGT Memory, knowledge-space
- Orchestrator → Svyazi, Rufler, knowledge-space, mclaude
- RAG TestGen → Rufler, knowledge-space, Svyazi, mclaude

## Кумулятивная карта (R01–R27)

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
| R27 | LLM кибербезопасность, персональный AI, мультиагентный оркестратор, AI DevEx | безопасность, DevEx |

**Итого:** 112 проектов, 58+ авторов

## Темы для Round 28

1. **Streaming/real-time AI** — потоковая обработка с LLM: Kafka + AI, event-driven агенты, real-time аномалии
2. **Multimodal Agent** — агенты работающие с изображениями, аудио и текстом одновременно; vision-language tasks в production
3. **LLM Evaluation frameworks** — автоматическая оценка качества LLM-ответов: LLM-as-judge, benchmark construction, red-teaming
4. **Federated AI / Privacy-preserving** — обучение и инференс без передачи данных: federated learning, homomorphic encryption, PETs
