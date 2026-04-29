# Обработка больших массивов — Часть 6: Поиск

> Как найти нужное в 1000+ документах: от простого grep до BM25 и фасетов.

---

## Уровни поиска (от простого к сложному)

```
Уровень 1: grep / find                  — быстро, грубо
Уровень 2: Поисковый индекс             — полнотекстовый, с preview
Уровень 3: BM25 (Okapi)                 — релевантность, не просто вхождение
Уровень 4: Поиск по абзацам (passage)  — точность на уровне абзаца
Уровень 5: Фасетный поиск              — поиск с фильтрами
Уровень 6: Список чтения по теме       — персонализированный маршрут
Уровень 7: Семантический (векторный)   — нужен embedding-модель
Уровень 8: LLM Q&A                     — вопрос → ответ с цитатами
```

---

## Уровень 2: Поисковый индекс — improve_search_index.py

**Строит:** `docs/search_index.json` — 1053 документа, 4.5 МБ

Каждая запись:
```json
{
  "file": "docs/05-habr-projects/memory/yodoca.md",
  "title": "Yodoca: консолидация и забывание",
  "content": "Yodoca — Научил ИИ-агента помнить важное...",
  "preview": "SQLite + FTS5, hot path < 50 мс...",
  "tags": ["memory", "sqlite", "collaboration"],
  "words": 847
}
```

```bash
python scripts/improve_search_index.py
python scripts/improve_index_update.py   # инкрементальное обновление
```

---

## Уровень 3: BM25 — improve_keyword_index.py

**BM25 (Best Match 25)** — стандарт информационного поиска. Лучше TF-IDF:
- Учитывает насыщенность документа (term saturation)
- Учитывает длину документа (document length normalization)
- Параметры: k1=1.5, b=0.75

```bash
python scripts/improve_keyword_index.py                    # построить индекс
python scripts/improve_keyword_index.py --query "агент память"  # поиск
```

**Инвертированный индекс + биграммы:**
```
"агент" → [{file: yodoca.md, score: 4.2}, {file: agentfs.md, score: 3.8}]
"агент память" → [{file: ngt-memory.md, score: 6.1}, ...]
```

---

## Уровень 4: Поиск по абзацам — improve_passage_retrieval.py

**Зачем:** Файл о Yodoca — 800 слов. BM25 найдёт файл. Но нужен **конкретный абзац** про «hot path».

```bash
python scripts/improve_passage_retrieval.py --index                    # построить
python scripts/improve_passage_retrieval.py --query "горячий путь SQLite" --top 5
```

**Результат:**
```
1. [0.847] docs/05-habr-projects/memory/yodoca.md §"hot path"
   "разделение на hot path (запись эпизодов в SQLite + FTS5 за <50 мс, без LLM) и
    slow path (асинхронные эмбеддинги)..."

2. [0.631] docs/04-ai-collaborations/04-приоритетные-ансамбли.md §"Память"
   "Yodoca обеспечивает горячий путь без LLM..."
```

**Применение в RAG:** Этот же `passages.json` можно подавать в LLM как контекст.

---

## Уровень 5: Фасетный поиск — improve_faceted_search.py

**Фасеты** — фильтры поверх полнотекстового поиска:

```bash
# Поиск по тексту в конкретной секции
python scripts/improve_faceted_search.py --query "граф памяти" --section 05-habr-projects

# Поиск файлов с конкретной сущностью
python scripts/improve_faceted_search.py --entity "AgentFS" --top 10

# Только файлы с проектами, изменённые после даты
python scripts/improve_faceted_search.py --type projects --after 2026-01-01

# Комбинация фасетов
python scripts/improve_faceted_search.py \
  --query "безопасность" \
  --entity "SENTINEL" \
  --section 04-ai-collaborations \
  --min-words 300
```

**Аналог:** Google Advanced Search, Elasticsearch с фильтрами.

---

## Уровень 6: Персонализированный список чтения — improve_reading_list.py

**Не просто поиск — маршрут изучения темы:**

```bash
python scripts/improve_reading_list.py --query "агент с памятью"
python scripts/improve_reading_list.py --query "RAG retrieval" --top 20
python scripts/improve_reading_list.py --query "Yodoca" --section 05-habr-projects
python scripts/improve_reading_list.py --format json  # machine-readable
```

**Алгоритм:**
1. BM25 по запросу → базовый score
2. Умножает на важность файла (из PRIORITIES.md)
3. Умножает на связность (количество входящих ссылок)
4. Оценивает время чтения (200 сл/мин RU, 250 EN)
5. Группирует по секциям для логического порядка

**Результат:**
```markdown
## Список чтения: "агент с памятью" (15 документов, ~45 мин)

### docs/05-habr-projects/memory/ (3 документа, ~12 мин)
1. yodoca.md — 847 слов, ~4 мин ⭐
2. ngt-memory.md — 1203 слова, ~6 мин
3. memnet.md — 412 слов, ~2 мин

### docs/04-ai-collaborations/ (4 документа, ~18 мин)
...
```

---

## Уровень 7: Похожие пассажи — improve_similar_passages.py

**Находит дублирующийся контент** между файлами — не точные копии, а **смыслово похожие** абзацы (TF-IDF cosine).

```bash
python scripts/improve_similar_passages.py
python scripts/improve_similar_passages.py --min-sim 0.7  # только очень похожие
```

**Применение:**
- Обнаружить, что одна идея описана в 5 разных местах
- Кандидаты для слияния в один канонический документ

---

## Уровень 8: Семантический поиск (не реализован, план)

**Векторный поиск** — embeddings + cosine similarity:

```python
# Нужно: sentence-transformers или API
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Индексация
embeddings = model.encode([chunk['text'] for chunk in chunks])
# → сохранить в FAISS / ChromaDB / SQLite-vec

# Поиск
query_vec = model.encode("как устроена долгосрочная память агента")
scores = cosine_similarity(query_vec, embeddings)
```

**Преимущество над BM25:** Находит семантически близкие тексты даже без общих слов.

**Почему не реализовано:** Требует ML-модель (200+ МБ) или платный API. BM25 даёт 80% качества при 0% стоимости.

---

## Сравнение методов поиска

| Метод | Точность | Скорость | Стоимость | Реализован |
|-------|---------|---------|----------|-----------|
| grep | низкая | мгновенно | 0 | ✅ |
| Полнотекстовый индекс | средняя | быстро | 0 | ✅ |
| BM25 | высокая | быстро | 0 | ✅ |
| Поиск по абзацам | очень высокая | быстро | 0 | ✅ |
| Фасетный | высокая + фильтры | быстро | 0 | ✅ |
| Семантический (векторный) | очень высокая | средне | модель | ❌ план |
| LLM Q&A | максимальная | медленно | $API | ✅ (ждёт ключа) |

---

## Следующий шаг

После поиска → **Часть 7: LLM-обогащение**
