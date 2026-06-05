# Round 26 — Session Log

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** LLM финансы/BI, CAVM аналитика, Supply Chain AI, LLM как B2B SaaS  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  

## Цели раунда

Продолжение поиска по темам из R25 session-log:
1. **CAVM аналитика** — AI-агенты пишут аналитические отчёты (Code Agent + Variable Memory)
2. **LLM трейдинг** — автономные LLM-трейдеры на бирже (эксперимент с реальными деньгами)
3. **AI в логистике** — прагматичный разбор реального состояния AI в supply chain в России
4. **GenAI монетизация** — продуктовая ошибка pay-as-you-go и альтернативы

## Найденные проекты

### 1. CAVM Framework — AI-агенты пишут аналитические отчёты
- **Файл:** `projects/ai-analytical-reports-cavm.md`
- **Хабр:** https://habr.com/ru/articles/960338/
- **Слой:** orchestration / analytics / knowledge
- **Уникальность:** Code Agent with Variable Memory — пайплайн агентов с общим пространством переменных; каждый шаг = рассуждение + генерация кода + исполнение; VLM-агенты проверяют качество графиков; 12–18 минут вместо 8–14 часов
- **Дата:** октябрь 2025

### 2. Finam Arena — 6 LLM торгуют на бирже
- **Файл:** `projects/finam-arena-llm-trading.md`
- **Хабр:** https://habr.com/ru/companies/finam_broker/articles/1005638/
- **Слой:** orchestration / analytics
- **Уникальность:** Первый публичный RU эксперимент: GPT-5.2, Claude Sonnet 4.5, Gemini 3 Flash, DeepSeek v3.2, Qwen3 Max, Grok 4.1 торговали реальными деньгами на MOEX+NYSE 39 дней; Ensemble +1.67%; LLM = разумный консервативный инвестор, но не чемпион рынка
- **Дата:** март 2026

### 3. AI в логистике — глобальные тренды vs российская реальность
- **Файл:** `projects/ai-logistics-russia-reality.md`
- **Хабр:** https://habr.com/ru/companies/intekey/articles/985430/
- **Слой:** orchestration / analytics / automation
- **Уникальность:** Честный разбор разрыва: Amazon 1M роботов vs российский Excel+1С; прагматичная AI-лестница (4 уровня с ROI); ML прогноз спроса ARIMA→LightGBM; человек на пересечении 3 миров (логистика+DS+системы) = дефицит
- **Дата:** январь 2026

### 4. GenAI продуктовая ошибка: pay-as-you-go убивает рост
- **Файл:** `projects/genai-product-mistake-monetization.md`
- **Хабр:** https://habr.com/ru/articles/1026722/
- **Слой:** orchestration / analytics
- **Уникальность:** Системный разбор конфликта интересов pay-as-you-go; 7 паттернов монетизации GenAI; почему wrapper-стартапы умирают; outcome-based pricing и subscription как альтернатива; специфика российского рынка
- **Дата:** май 2026

## Поиск аналогий в Lorenzo (collab_finder)

Запуск для всех 4 проектов:
```bash
python scripts/improve_collab_finder.py --file docs/06-discovery/round-26/projects/ai-analytical-reports-cavm.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-26/projects/finam-arena-llm-trading.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-26/projects/ai-logistics-russia-reality.md --top 4
python scripts/improve_collab_finder.py --file docs/06-discovery/round-26/projects/genai-product-mistake-monetization.md --top 4
```

Результаты → `docs/COLLAB_SUGGESTIONS.md`

Топ совпадений:
- CAVM → Svyazi, knowledge-space, AgentFS, Rufler
- Finam Arena → Svyazi, agent-memory-mcp, NGT Memory, knowledge-space
- AI Logistics → Svyazi, knowledge-space, AgentFS, NGT Memory
- GenAI Product → Svyazi, agent-memory-mcp, NGT Memory, knowledge-space

## Кумулятивная карта (R01–R26)

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

**Итого:** 108 проектов, 56+ авторов

## Темы для Round 27

1. **LLM для кибербезопасности** — автоматический анализ уязвимостей, pentest-агенты, IDS с LLM-объяснениями (Хабр: темы CTF, SAST с LLM, security automation)
2. **Персонализированные AI-ассистенты** — личный AI на локальных данных (заметки, переписка, calendar), long-term memory, персонализация без cloud
3. **Мультиагентное планирование** — иерархические агентские сети, manager/worker архитектура, backtracking и повторные попытки в сложных задачах
4. **AI в DevEx** — developer experience с AI: автодополнение архитектуры, автогенерация тестов, AI code navigator, поиск по кодовой базе
