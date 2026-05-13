# Retrieval Hit Rate Evaluation — Lorenzo / Svyazi 2.0

<!-- toc-auto -->

> [!TIP]
> Этот документ описывает MVP-подход. Начните с него для быстрого прототипа.

<!-- alert-added -->

<!-- summary -->
> Автоматическая оценка качества hybrid_search(). Hit Rate@5 = **0.700** (≥ порог 0.70).

<!-- tags: evaluation, hit-rate, retrieval, hybrid-search -->

---

## Результаты (Hit Rate@5)

| Метрика | Значение | Порог | Статус |
|---------|---------|-------|--------|
| Hit Rate@5 | **0.700** (14/20) | ≥ 0.70 | ✅ PASS |
| Mean MRR      | 0.472 | — | — |
| Avg Latency   | 1.130с | ≤ 5.0с | ✅ |

> **Примечание:** Hit Rate@K = доля запросов, где хотя бы 1 релевантный
> документ попал в топ-K. Стандартный P@K с 1 документом/запрос ≤ 1/K,
> поэтому Hit Rate — правильная метрика для этого набора данных.

---

## Детали (20 запросов)

| # | Запрос | Rank | Hit |
|---|--------|------|-----|
| 1 | Yodoca консолидация SQLite decay forgot memory | 3 | ✅ |
| 2 | AgentFS файловая система агент vault kksudo | 1 | ✅ |
| 3 | NGT Memory ассоциативный граф лингвист ngt структура | 9 | ❌ |
| 4 | agent-memory-mcp типизированная SQLite эпизодическая Vi… | 3 | ✅ |
| 5 | MemNet RAG Challenge Docling pdfplumber FAISS memory | 4 | ✅ |
| 6 | Rufler YAML декларативный агент Claude Code токены swar… | 1 | ✅ |
| 7 | knowledge-space карточки MIT граф 785 AnastasiyaW | 1 | ✅ |
| 8 | LiteParse PDF извлечение Evidence nlaik структура докум… | 2 | ✅ |
| 9 | Wikontic семантический граф VitalyOborin kubernetes нор… | 2 | ✅ |
| 10 | Svyazi 2.0 спецификация прототипа Card Envelope Evidenc… | 2 | ✅ |
| 11 | Card Envelope sha256 card_id payload источник интеграци… | 6 | ❌ |
| 12 | BM25 TF-IDF гибридный поиск Retrieval hybrid search pas… | 6 | ❌ |
| 13 | SENTINEL безопасность PII credentials аудит | 1 | ✅ |
| 14 | Gateway OpenAI FastAPI function calling write-back обог… | 1 | ✅ |
| 15 | авторы Хабр kksudo spbmolot VitalyOborin письма контакт… | 17 | ❌ |
| 16 | Svyazi архитектура CardIndex knowledge три слоя AgentFS | 7 | ❌ |
| 17 | Anthropic вакансии анализ ML research svend4 Nautilus | 8 | ❌ |
| 18 | Review Queue карточки состояние proposal approved decay… | 2 | ✅ |
| 19 | ANN HNSW два этапа hnswlib векторный поиск индекс | 4 | ✅ |
| 20 | Card Envelope sha256 payload Evidence Envelope прототип… | 2 | ✅ |

---

## Методология

- **Метрика:** Hit Rate@5 — доля запросов с ≥1 релевантным документом в топ-5.
- **Поиск:** `hybrid_search()` = 0.6×TF-IDF + 0.4×BM25 с фильтром шумовых документов.
- **Фильтр шума:** исключаются meta-docs (TABLES.md, OUTLINE.md и др.), obsidian-копии, autofilled/.
- **20 запросов:** 9 проектных (само-релевантность) + 11 кросс-секционных.
- **Без ручной разметки:** обновляется автоматически при каждом запуске.

*Сгенерировано: 2026-05-13 07:32*
<!-- see-also -->

---

**Смотрите также:**
- [PROTOTYPE_SPEC](PROTOTYPE_SPEC.md)
- [ENTITIES](ENTITIES.md)
- [DEMO](DEMO.md)
- [DUPLICATES](DUPLICATES.md)



## Использование
```bash
# Запуск
python scripts/improve_precision_eval.py
```
