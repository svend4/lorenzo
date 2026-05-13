# Round 51 — Session Log

**Дата:** май 2026  
**Статус:** ✅ Завершён  
**Проектов найдено:** 4  
**Итого по всем раундам:** 208 проектов, 90+ авторов

## Темы поиска

1. **LLM для видеоанализа в реальном времени** — streaming video understanding, event detection, CLIP+VLM гибриды
2. **Верификация кода формальными методами + LLM** — Design by Contract, proof assistants, contract-driven code generation
3. **Адаптивные обучающие системы v2** — AI-репетиторы, педагогические оркестраторы, сценарный routing
4. **LLM для биоинформатики и геномики** — de novo drug discovery, молекулярная генерация, GNN + RL

## Найденные проекты

| # | Автор | Проект | Слой | Файл |
|---|-------|--------|------|------|
| 1 | eCaesar | Video RAG: CLIP-Only поиск без LLM-декодера | knowledge/ingestion | `projects/ecaesar-mts-video-rag-clip-vlm-search.md` |
| 2 | Miller83 | Design by Contract + LLM: формальные контракты для криптографии | orchestration | `projects/miller83-design-by-contract-llm-crypto-hardware.md` |
| 3 | vladotpad | ЕГЭ AI-репетитор: 6-сценарный оркестратор | orchestration | `projects/vladotpad-ege-ai-tutor-math-scenario-orchestrator.md` |
| 4 | AlexanderTelepov | FREED++: GNN+RL для de novo генерации молекул | analytics/knowledge | `projects/alexandertelepov-freed-plus-plus-drug-discovery-rl-gnn.md` |

## Ключевые находки раунда

- **eCaesar (MTS AI):** CLIP-Only RAG для видеонаблюдения — ключевое решение: отбросить language decoder VLM при индексации, 10–100× speedup. CLIP ViT-B/32 + FAISS, 80% Recall vs 35–70% text-only. GPT-4V только как опциональный reranker топ-K. [habr.com/ru/companies/mts_ai/articles/804555/](https://habr.com/ru/companies/mts_ai/articles/804555/)

- **Miller83:** Design by Contract + LLM для PKI на STM32/RK3328 — 10-строчные YAML-контракты (PRE/POST/INV) → LLM генерирует имплементацию + contract-validation тесты. 2 критических уязвимости пойманы до продакшена (PKCS#1 v1.5 вместо PSS, AES-CBC вместо GCM). 62 контракт-теста, 12/12 NIST 800-90B аудит. [habr.com/ru/articles/1025244/](https://habr.com/ru/articles/1025244/)

- **vladotpad (Innopolis):** ЕГЭ AI-репетитор — 3 итерации (RAG→агент→fine-tune), 6-сценарный педагогический оркестратор включая «сократическую частичную помощь», math OCR→LaTeX, отказ от LangChain в пользу bare OpenAI API (конкретный разбор причин). 86 баллов ЕГЭ. [habr.com/ru/articles/989136/](https://habr.com/ru/articles/989136/)

- **AlexanderTelepov (AIRI):** FREED++ — нашёл и исправил критический баг в NeurIPS 2021 FREED (critic получал probability distributions вместо attachment point embeddings). GNN + actor-critic RL для de novo генерации молекул. 8.5× speedup, 22× снижение памяти, тестирование на 6 белках-мишенях. [habr.com/ru/companies/airi/articles/842534/](https://habr.com/ru/companies/airi/articles/842534/)

## Темы для Round 52

1. **LLM квантование и прунинг для edge deployment** — GPTQ/AWQ, quantization-aware training, LoRA + квантование, model compression для production
2. **Conversational AI с handoff и эскалацией** — multi-turn dialog agents, human escalation protocols, customer support с LLM
3. **LLM для финансового аудита и бухгалтерии** — автоматизация проводок, reconciliation, invoice processing, LLM для GL
4. **Федеративное обучение LLM** — federated fine-tuning, differential privacy, privacy-preserving FL на распределённых данных

## Накопленная таблица раундов (R01–R51)

| Раунд | Проектов | Ключевая тема |
|-------|----------|---------------|
| R01 | 9 | Memory + Knowledge |
| R02 | 6 | Voice, parsing, YAML |
| R03 | 3 | Code review, fine-tuned LLM |
| R04 | 3 | Agent platform, MCP protocol |
| R05 | 3 | Autonomous pipeline, Russian NLP |
| R06 | 4 | Video AI, CLI agents, GitHub automation |
| R07 | 4 | Multi-agent arch, agent safety, MCP pipeline |
| R08 | 4 | Codebase MCP, scientific ingestion, edu AI |
| R09 | 4 | GraphRAG, decentralized AI, coding agent |
| R10 | 4 | Viral simulation, self-hosted stacks, Rust |
| R11 | 4 | Desktop agents, edge AI, voice embedded |
| R12 | 4 | Data analytics AI, audio gen, vector DBs |
| R13 | 4 | Observability, ADD, self-healing tests, OCR |
| R14 | 4 | Context Engineering, DSPy, AI security, MarkItDown |
| R15 | 4 | Code review AI, Text2SQL, fine-tuning, LLM security |
| R16 | 4 | No-LangChain, monitoring LLM, GigaAM-v3 ASR, RAG eval |
| R17 | 4 | CoT research, LLM-Wiki, Knowledge Graph, LLM DBA |
| R18 | 4 | Agentic RAG, synthetic data, incident AI, RU embeddings |
| R19 | 4 | Multimodal RAG (Docling), doc review AI, vector DB, LLM inference |
| R20 | 4 | LLM unit tests, DeepSeek V3.2, Reasoning models, LLM economics |
| R21 | 4 | Multi-agent case, A2A protocol, LLM privacy, RU classification |
| R22 | 4 | Legal NLP, LLM AppSec, self-hosted AI, Graph RAG prod |
| R23 | 4 | HR AI, Durable State агентов, RPA+AI Enterprise, Prompt Injection |
| R24 | 4 | DevOps LLM fine-tuning, AIOps Sberbank, EdTech AI, Private LLM стек |
| R25 | 4 | Юридический RAG, нормоконтроль LLM, AI-наука, визуальное тестирование |
| R26 | 4 | CAVM аналитика, Finam LLM трейдинг, AI логистика, GenAI продукт |
| R27 | 4 | LLM кибербезопасность, персональный AI с памятью, 5-фазный оркестратор, RAG тесты |
| R28 | 4 | Volga streaming ML, мультимодальный VLM Сбер, LLM Judge кросс-модельный, Federated edge |
| R29 | 4 | Comprehension debt, Text2SQL X5, AI мета-мониторинг, Кириллица в LLM |
| R30 | 4 | Coreness Flow composable, VLM vs IDP бенчмарк, синтетика граф-качество, HITL prod |
| R31 | 4 | DBRM медицина, Cognitive Memory SQLite, LLM+Terraform DevOps, XAI mechanistic |
| R32 | 4 | Enterprise RAG (МТС), vLLM inference opt, FinPDF pipeline, Авито VLM |
| R33 | 4 | AI code agents v2, LLM data engineering, суверенный AI, red-teaming |
| R34 | 4 | LLM DevSecOps, Multimodal doc v2, LLM evaluation, Edge AI |
| R35 | 4 | LLM телеком, персонализация, AI образование v2, agent planning |
| R36 | 4 | LLM финансовый compliance, continuous adaptation, логистика AI, LLM для науки |
| R37 | 4 | LLM медиа, AI безопасность v2, LLM IoT/промышленность, LLM calibration |
| R38 | 4 | LLM медицина v2, multiagent coordination, LLM observability, RAG v3 |
| R39 | 4 | LLM юридическая авт. v2, synthetic data, персонализация v2, AI testing v2 |
| R40 | 4 | LLM строительство, structured output v2, образование v3, кибербезопасность v2 |
| R41 | 4 | Агро ML pipeline, SWE-MERA бенчмарк, Robovoice поддержка, Privacy LLM |
| R42 | 4 | AML LLM советник, PhysicalAgent VLA, SherlockOps SRE, T-Bank RU LLM |
| R43 | 4 | feeds.fun медиа, RAG чанкинг, LOCK-R reasoning, Kaspersky MLAD ICS |
| R44 | 4 | AI EMR ассистент, LoRA эмбеддинги, Yandex LLM eval, LangGraph агенты |
| R45 | 4 | MWS Vision Bench, MOEX DistilBERT, Avito Mistral RU, LLM Observability |
| R46 | 4 | Coordination Harness, Telecom Classifier, Code MCP, AQLM.rs браузер |
| R47 | 4 | LLM Judge образование, SENTINEL безопасность, MTS code review, Temporal KG |
| R48 | 4 | LLM медицина v3, Multimodal RAG v2, ML промышленность v2, Agent evaluation v2 |
| R49 | 4 | Finance RAG 4-head, GBNF constrained decoding, Self-hosted 4×4090, SAP Text2SQL |
| R50 | 4 | LLM персонализация v3, Qwen3Guard модерация, SR-Scientist, RAG embedder fine-tuning |
| R51 | 4 | Video RAG CLIP, Design by Contract, ЕГЭ репетитор, FREED++ drug discovery |
| **Итого** | **208** | |
