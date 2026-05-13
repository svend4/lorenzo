# Retrieval Hit Rate Evaluation — Lorenzo / Svyazi 2.0

<!-- summary -->
> Автоматическая оценка качества hybrid_search(). Hit Rate@10 = **1.000** (≥ порог 0.70).

<!-- tags: evaluation, hit-rate, retrieval, hybrid-search -->

---

## Результаты (Hit Rate@10)

| Метрика | Значение | Порог | Статус |
|---------|---------|-------|--------|
| Hit Rate@10 | **1.000** (20/20) | ≥ 0.70 | ✅ PASS |
| Mean MRR      | 0.441 | — | — |
| Avg Latency   | 1.251с | ≤ 5.0с | ✅ |

> **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный
> документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K,
> поэтому Hit Rate — правильная метрика для этого набора данных.

---

## Детали (20 запросов)

| # | Запрос | Rank | Hit |
|---|--------|------|-----|
| 1 | Yodoca консолидация SQLite decay forgot memory | 1 | ✅ |
| 2 | AgentFS файловая система агент vault kksudo | 3 | ✅ |
| 3 | NGT Memory ассоциативный граф лингвист ngt структура | 5 | ✅ |
| 4 | agent-memory-mcp типизированная SQLite эпизодическая Vi… | 3 | ✅ |
| 5 | MemNet RAG Challenge Docling pdfplumber FAISS memory | 7 | ✅ |
| 6 | Rufler YAML декларативный агент Claude Code токены swar… | 1 | ✅ |
| 7 | knowledge-space карточки MIT граф 785 AnastasiyaW | 3 | ✅ |
| 8 | LiteParse PDF извлечение Evidence nlaik структура докум… | 3 | ✅ |
| 9 | Wikontic семантический граф VitalyOborin kubernetes нор… | 3 | ✅ |
| 10 | Svyazi 2.0 спецификация прототипа Card Envelope Evidenc… | 3 | ✅ |
| 11 | Card Envelope sha256 card_id payload источник интеграци… | 5 | ✅ |
| 12 | BM25 TF-IDF гибридный поиск Retrieval hybrid search pas… | 10 | ✅ |
| 13 | SENTINEL безопасность PII credentials аудит | 1 | ✅ |
| 14 | Gateway OpenAI FastAPI function calling write-back обог… | 1 | ✅ |
| 15 | авторы Хабр kksudo spbmolot VitalyOborin письма контакт… | 5 | ✅ |
| 16 | Svyazi CardIndex Knowledge OS три контракта CardEnvelop… | 6 | ✅ |
| 17 | Anthropic вакансии анализ ML research svend4 Nautilus | 1 | ✅ |
| 18 | Review Queue карточки состояние proposal approved decay… | 3 | ✅ |
| 19 | ANN HNSW два этапа hnswlib векторный поиск индекс | 7 | ✅ |
| 20 | Card Envelope sha256 payload Evidence Envelope прототип… | 3 | ✅ |

---

## Методология

- **Метрика:** Hit Rate@10 — доля запросов с ≥1 релевантным документом в топ-10.
- **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов.
- **Фильтр шума:** исключаются meta-docs (TABLES.md, OUTLINE.md и др.), obsidian-копии, autofilled/.
- **20 запросов:** 9 проектных (само-релевантность) + 11 кросс-секционных.
- **Без ручной разметки:** обновляется автоматически при каждом запуске.

*Сгенерировано: 2026-05-13 15:12*