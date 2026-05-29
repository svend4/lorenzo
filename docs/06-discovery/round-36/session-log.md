---
date: 2026-05-29
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# Round 36 — Session Log

<!-- toc-auto -->
<!-- tags: session-log, docs -->


<!-- summary -->
> LLM для медиа и контент-генерации — автоматизация новостных материалов, AI-редакторы, детектирование AI-контента, медиа-мониторинг
2.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Дата:** май 2026  
**Тема:** LLM финансовый compliance, continuous adaptation, логистика AI, LLM для науки  
**Проектов найдено:** 4  
**Авторов:** 4 новых

## Найденные проекты

| # | Проект | Автор | Слой | Хабр |
|---|--------|-------|------|------|
| 1 | Finam FinBench: финансовые бенчмарки LLM | Finam_Broker (Finam AI Lab) | analytics | 989842 |
| 2 | AgentFly/Memento: память вместо файнтюнинга | andre_dataist | memory / orchestration | 940824 |
| 3 | X5Tech TFT: прогнозирование спроса в ритейле | mayo889 (X5 Tech) | analytics | 869750 |
| 4 | Paper2Agent: статьи → MCP инструменты | andre_dataist | orchestration | 945582 |

## Детали поиска

### Тема 1: LLM финансовый compliance и регулирование
- **Запрос:** LLM финансовый бенчмарк compliance оценка
- **Выбранная статья:** https://habr.com/ru/companies/finam_broker/articles/989842/ (январь 2025)
- **GitHub:** https://github.com/FinamAILab/Finam-FinBench_public
- **Уникальность:** Domain-specific финансовые бенчмарки: CFA L1-3, CMT L2, RU финансовые олимпиады; LLM-as-Judge с агрегацией рангов; ключевой вывод: FinGPT специализированная < GPT-4o на CFA; GigaChat лучший на RU специфике
- **Другие кандидаты:** 875286 (T2/Tele2, AML CatBoost ЦБ РФ, нет GitHub), 963262 (cbrapi Python библиотека ЦБ, GitHub: mbk-dev/cbrapi), 1031940 (ASCON NLP ГОСТ, нет GitHub)

### Тема 2: Continuous fine-tuning / knowledge editing
- **Запрос:** LLM continual learning catastrophic forgetting память адаптация
- **Выбранная статья:** https://habr.com/ru/articles/940824/ (август 2025)
- **GitHub:** https://github.com/Agent-on-the-Fly/Memento
- **Уникальность:** M-MDP формализация памяти; soft Q-learning (Haarnoja 2018) для utility оценки кейсов; frozen LLM weights = zero alignment degradation; case-based reasoning + Markovian Decision Process; deployable open-source
- **Collab Finder:** MemNet + NGT Memory (оба работают с memory management)
- **Замечание:** ROME/MEMIT не покрыты на Хабре — только академические статьи

### Тема 3: AI для supply chain и логистики
- **Запрос:** TFT temporal fusion transformer прогноз спрос ритейл
- **Выбранная статья:** https://habr.com/ru/companies/X5Tech/articles/869750/ (декабрь 2024)
- **GitHub:** нет (внутренняя разработка X5)
- **Уникальность:** TFT (Darts + PyTorch Lightning), 4 heads, dual LSTM, 17 квантилей; data-leakage-free метод инжекции future covariates через truncated normal distribution; 7% MAPE на 6 месяцах реальных данных Пятёрочки/Перекрёстка; 11.34% улучшение RTO метрики
- **Collab Finder:** agent-memory-mcp (temporal pattern memory)
- **Другие кандидаты:** 887486 (parseny/Raft, LLM time series temp/crypto, GitHub: parseny/LLM-and-Time-Series)

### Тема 4: LLM для научных исследований
- **Запрос:** Paper2Agent научные статьи MCP инструменты агент
- **Выбранная статья:** https://habr.com/ru/articles/945582/ (сентябрь 2025)
- **GitHub:** https://github.com/jmiao24/Paper2Agent
- **Уникальность:** PDF → MCP server через 4 субагента; 22 геномных инструмента из AlphaGenome за 3 часа; reproducibility success rate как прокси качества публикации; стандартный MCP интерфейс к scientific tools
- **Замечание:** Тот же автор (andre_dataist) что и Memento — вышли с разницей 2 недели

## Cumulative Table R01–R36

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
| R36 | LLM финансовый compliance, continuous adaptation, логистика AI, LLM для науки | 4 |
| **Итого** | | **148** |

## Темы для Round 37

1. **LLM для медиа и контент-генерации** — автоматизация новостных материалов, AI-редакторы, детектирование AI-контента, медиа-мониторинг
2. **Безопасность AI-систем (продолжение)** — prompt injection в production, adversarial attacks на embeddings, защита RAG от атак
3. **LLM для IoT и промышленности** — предсказательное обслуживание с LLM, анализ телеметрии промышленного оборудования
4. **Оценка и calibration LLM** — uncertainty quantification, calibration curves, overconfidence detection, hallucination scoring

## Новые авторы раунда

| Автор | Проект | Контакт |
|-------|--------|---------|
| Finam AI Lab | Finam FinBench | github.com/FinamAILab |
| andre_dataist | AgentFly/Memento + Paper2Agent | habr.com/ru/users/andre_dataist |
| mayo889 (Дмитрий Поляков) | X5Tech TFT | x5.tech |


## Использование
```bash
# Запуск
python scripts/improve_session_log.py
```

## Смотрите также
- [Главная](../../README.md)
- [Метрики](../../METRICS.md)
- [Здоровье](../../HEALTH.md)
- [Глоссарий](../../GLOSSARY.md)
- [Сущности](../../ENTITIES.md)
- [Решения](../../DECISIONS.md)
