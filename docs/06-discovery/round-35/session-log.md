# Round 35 — Session Log

> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** LLM телеком, персонализация/рекомендации, AI образование v2, agent planning  
**Проектов найдено:** 4  
**Авторов:** 4 новых

## Найденные проекты

| # | Проект | Автор | Слой | Хабр |
|---|--------|-------|------|------|
| 1 | AI Routing Lab: ML для сетевых маршрутов | maxorik (CloudBridge Research) | analytics / orchestration | 970630 |
| 2 | GitHub Repo Embeddings + Recommendations | Puzer (Дмитрий) | analytics / knowledge | 983080 |
| 3 | EduLLM-RU: дообучение для учителей (CRAFT) | daniel_ivanov | analytics | 1026516 |
| 4 | ReAct-агент с LangGraph (GigaChain/Сбер) | trashchenkov | orchestration | 934938 |

## Детали поиска

### Тема 1: LLM для телеком и сети
- **Запрос:** LLM NetOps сетевые маршруты оптимизация ML
- **Выбранная статья:** https://habr.com/ru/articles/970630/ (ноябрь 2025)
- **GitHub:** https://github.com/cloudbridge-research/ai-routing-lab (v0.2.1, MIT)
- **Уникальность:** Random Forest (MAE 3.2мс, R²=0.94) + Q-Learning + UCB Multi-Armed Bandit + Isolation Forest + GPT-4o как AI агент; интеграция с Prometheus; 196 unit-тестов; предсказание деградации за 5-10 мин до события
- **Замечание:** Чистых LLM-for-telecom статей с кодом на Хабре мало; это лучший ML+NetOps проект с реальным GitHub

### Тема 2: Персонализация и рекомендации с LLM
- **Запрос:** LLM рекомендательная система embeddings персонализация
- **Выбранная статья:** https://habr.com/ru/articles/983080/ (январь 2025)
- **GitHub:** https://github.com/Puzer/github-repo-embeddings + demo: puzer.github.io/github_recommender
- **Уникальность:** Hybrid text+behavior: Qwen3-Embedding-0.6B (MRL, 128-dim) из README.md → refine через CF на 4M GitHub Stars; cold-start как среднее векторов starred repos; 100% WASM client-side inference через USearch по 2.5M items; +10% Recall@10 vs одиночного подхода
- **Collab Finder:** нашёл связи с AgentFS, Yodoca, MemNet (knowledge store паттерны)

### Тема 3: AI для образования v2
- **Запрос:** LLM fine-tuning образование учителя студент российский
- **Выбранная статья:** https://habr.com/ru/articles/1026516/ (апрель 2025)
- **GitHub:** https://github.com/csylabs-org/edubench-ru
- **Уникальность:** CRAFT методология (ACL 2025) для синтетических данных: Claude+Gemini Batch API → 30K QA пар; QLoRA+Unsloth Qwen3.5-27B за $400; rank #9/30 (уровень GPT-5.4); 152-ФЗ compliance; EduBench-RU открытый бенчмарк для российских образовательных задач

### Тема 4: Оркестрация и planning LLM агентов
- **Запрос:** ReAct LangGraph агент планирование оркестрация production
- **Выбранная статья:** https://habr.com/ru/companies/sberbank/articles/934938/ (август 2025)
- **GitHub:** https://github.com/ai-forever/gigachain
- **Уникальность:** Эволюция text-parsing ReAct → structured function calling; LangGraph как cyclic state machine; StateSnapshot + MemorySaver для multi-turn памяти; time-travel debugging; полный код с GigaChat-2-Max (российская LLM, не OpenAI)

## Cumulative Table R01–R35

| Раунд | Тема | Проектов |
|-------|------|----------|
| R01 | Memory + Knowledge | 9 |
| R02 | Voice, parsing, YAML | 6 |
| R03 | Code review, fine-tuned LLM | 3 |
| R04 | Agent platform, MCP protocol | 3 |
| R05 | Autonomous pipeline, Russian NLP | 3 |
| R06 | Video AI, CLI agents, GitHub automation | 4 |
| R07 | Multi-agent arch, agent safety, MCP pipeline | 4 |
| R08 | Codebase MCP, scientific ingestion, edu AI | 4 |
| R09 | GraphRAG, decentralized AI, coding agent | 4 |
| R10 | Viral simulation, self-hosted stacks, Rust | 4 |
| R11 | Desktop agents, edge AI, voice embedded | 4 |
| R12 | Data analytics AI, audio gen, vector DBs | 4 |
| R13 | Observability, ADD, self-healing tests, OCR | 4 |
| R14 | Context Engineering, DSPy, AI security, MarkItDown | 4 |
| R15 | Code review AI, Text2SQL, fine-tuning, LLM security | 4 |
| R16 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval | 4 |
| R17 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA | 4 |
| R18 | Agentic RAG, synthetic data, incident AI, RU embeddings | 4 |
| R19 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference | 4 |
| R20 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics | 4 |
| R21 | Multi-agent case, A2A protocol, LLM privacy, RU classification | 4 |
| R22 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod | 4 |
| R23 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection | 4 |
| R24 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек | 4 |
| R25 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование | 4 |
| R26 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт | 4 |
| R27 | LLM кибербезопасность, персональный AI с памятью, 5-фазный оркестратор, RAG тесты | 4 |
| R28 | Volga streaming ML, мультимодальный VLM Сбер, LLM Judge кросс-модельный, Federated edge | 4 |
| R29 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица в LLM | 4 |
| R30 | Coreness Flow composable, VLM vs IDP бенчмарк, синтетика граф-качество, HITL prod | 4 |
| R31 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic | 4 |
| R32 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM | 4 |
| R33 | AI code agents v2, LLM data engineering, суверенный AI, red-teaming | 4 |
| R34 | LLM DevSecOps, Multimodal doc v2, LLM evaluation, Edge AI | 4 |
| R35 | LLM телеком, персонализация, AI образование v2, agent planning | 4 |
| **Итого** | | **144** |

## Темы для Round 36

1. **LLM для финансового compliance и регулирования** — автоматизация отчётности ЦБ, AI для KYC/AML, NLP для регуляторных документов
2. **Continuous fine-tuning и обновление знаний LLM** — online learning, knowledge editing, catastrophic forgetting prevention, ROME/MEMIT методы
3. **AI для supply chain и логистики** — прогнозирование спроса с LLM, оптимизация складов, мультиагентная логистика
4. **LLM для научных исследований** — автоматизация Literature Review, генерация гипотез, AI-assisted peer review

## Новые авторы раунда

| Автор | Проект | Контакт |
|-------|--------|---------|
| maxorik (Максим Ланиес) | AI Routing Lab | github.com/cloudbridge-research |
| Puzer (Дмитрий) | GitHub Repo Embeddings | github.com/Puzer |
| daniel_ivanov | EduLLM-RU | github.com/csylabs-org |
| trashchenkov | GigaChain ReAct Agent | github.com/ai-forever |
