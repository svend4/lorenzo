---
date: 2026-05-29
tags: [memory, rag, orchestration, knowledge, ingestion]
state: normalized
---

# FRIDA — русскоязычная embedding-модель #1 на ruMTEB

<!-- toc-auto -->
<!-- tags: frida-russian-embeddings, docs -->


<!-- summary -->
> Сравнение с аналогами Модель | Язык | ruMTEB | Лицензия | Размер | FRIDA | RU (+ EN) | #1 67.8 | MIT | 128M |
 
Сравнение с аналогами
 Модель | Язык | ruMTEB | Лицензия | Размер |
 --------|------|--------|---------|--------|
 FRIDA | RU (+ EN) | #1 67.8 | MIT | 128M |
 rubert-tiny2 | RU | 51.4 | Apache 2.0 | 29M |
 multilingual-e5-large | mult


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** команда SberDevices (подразделение Сбербанка)  
**Хабр:** https://habr.com/ru/companies/sberdevices/articles/909924/  
**GitHub:** https://huggingface.co/sergeyzh/rubert-mini-frida (MIT)  
**Слой:** knowledge / ingestion / memory  
**Дата:** декабрь 2024 — май 2025 (#1 на ruMTEB)  
**Уникальность:** Первая open-source русскоязычная embedding-модель, обошедшая все закрытые API (включая OpenAI text-embedding-3-large) на **ruMTEB** — русском аналоге MTEB. Основана на энкодере FRED-T5 (не BERT), поддерживает asymmetric search (query ≠ document). MIT-лицензия, доступна через `sentence-transformers`.

## Архитектура

```
FRED-T5 (encoder-only часть)
  ↓
Fine-tuning на русскоязычных парах:
  - STS (семантическая близость)
  - NLI (entailment / contradiction)
  - QA пары (query → relevant document)
  - Information Retrieval
  ↓
FRIDA: 128M параметров, 768-dim embeddings
  + asymmetric режим:
    query_prefix = "Запрос: "
    document_prefix = "Документ: "
```

## Производительность (ruMTEB, май 2025)

```
ruMTEB лидерборд:
  1. FRIDA (SberDevices, MIT)          — 67.8 avg
  2. e5-mistral-7b-instruct            — 65.2 avg
  3. text-embedding-3-large (OpenAI)   — 64.1 avg
  4. multilingual-e5-large             — 62.3 avg
  5. rubert-tiny2                      — 51.4 avg

Задачи в ruMTEB:
  - STS (semantic similarity)
  - Classification
  - Clustering
  - Retrieval (поиск релевантных документов)
  - Reranking
  - PairClassification
```

**FRIDA #1** по средней оценке, особенно на Retrieval (+4.3 vs text-embedding-3-large).

## Использование

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sergeyzh/rubert-mini-frida")

# Asymmetric search (рекомендуется)
query = "Запрос: Как работает агент с памятью?"
documents = [
    "Документ: AgentFS хранит факты в файловой системе...",
    "Документ: NGT Memory использует граф ближайших соседей..."
]

query_emb = model.encode(query)
doc_embs = model.encode(documents)
scores = query_emb @ doc_embs.T  # cosine similarity
```

## Сравнение с аналогами

| Модель | Язык | ruMTEB | Лицензия | Размер |
|--------|------|--------|---------|--------|
| **FRIDA** | RU (+ EN) | **#1 67.8** | MIT | 128M |
| rubert-tiny2 | RU | 51.4 | Apache 2.0 | 29M |
| multilingual-e5-large | multi | 62.3 | MIT | 560M |
| text-embedding-3-large | multi | 64.1 | проприетарная | ? (API) |
| GigaChat embeddings | RU | ~63 | проприетарная | API |

FRIDA — единственная MIT-модель в топ-3, работает полностью локально.

## Семейство FRIDA

| Модель | Размер | Скорость | Точность | Когда |
|--------|--------|----------|----------|-------|
| rubert-mini-frida | 128M | быстрая | высокая | production |
| FRIDA-large | 420M | медленная | выше | если важна точность |

## Применение к Lorenzo

Lorenzo сейчас использует TF-IDF (pure Python) для семантического поиска.  
FRIDA = прямая замена на **нейронные embeddings**:

```python
# Сейчас: TF-IDF в improve_embedding_index.py
tfidf_matrix = TfidfVectorizer().fit_transform(docs)

# С FRIDA: нейронный поиск (install: pip install sentence-transformers)
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("sergeyzh/rubert-mini-frida")
embeddings = model.encode(["Запрос: " + d for d in docs])
```

**Ожидаемый эффект:** recall@10 для RU-запросов +15-25% (по ruMTEB retrieval задаче).

Для `improve_llm_qa.py` и `mcp_server.py` — лучший первый шаг нежели полный GraphRAG.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **FRIDA + Lorenzo search** | TF-IDF → FRIDA: нейронный поиск по 2483 карточкам |
| **FRIDA + GigaAM (R16)** | Voice query (GigaAM) → FRIDA embedding → ответ |
| **FRIDA + Sberbank KG (R17)** | Векторный поиск в hybrid KG — оба от SberDevices |
| **FRIDA + Agentic RAG (R18)** | Agentic RAG с нейронными embeddings для RU-корпуса |
| **FRIDA + RAG Eval (R16)** | RAGAS оценивает FRIDA recall vs TF-IDF в CI |
| **FRIDA + Synthetic Data (R18)** | Синтетика для дообучения FRIDA под Lorenzo-специфику |

## Контакт

- Статья: https://habr.com/ru/companies/sberdevices/articles/909924/ (декабрь 2024)
- HuggingFace: https://huggingface.co/sergeyzh/rubert-mini-frida (MIT)
- ruMTEB лидерборд: huggingface.co/spaces/mteb/leaderboard (Russian)
- FRED-T5 (базовая модель): github.com/sberbank-ai/FRED-T5
- Смежная (ruBERT сравнение): https://habr.com/ru/articles/778484/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
