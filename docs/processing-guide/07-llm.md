# Обработка больших массивов — Часть 7: LLM-обогащение

> Что может сделать языковая модель с документами, чего не может классический алгоритм.

---

## Граница классики и LLM

| Задача | Классика | LLM |
|--------|---------|-----|
| Найти все упоминания «AgentFS» | ✅ grep/BM25 | ✅ |
| Понять что AgentFS *делает* | ❌ | ✅ |
| Найти противоречия | 🟡 (ключевые слова) | ✅ (смысловые) |
| Написать резюме | 🟡 (TextRank) | ✅ (связный текст) |
| Предложить вопрос автору | ❌ | ✅ |
| Заполнить пробелы в документации | ❌ | ✅ |
| Перевести на другой язык | ❌ | ✅ |

---

## Архитектура: 5 LLM-скриптов

```
improve_llm_enrich.py    ← обогатить файл: добавить секции, углубить анализ
improve_llm_qa.py        ← Q&A по базе: вопрос → ответ с источниками
improve_llm_summary.py   ← каскадная суммаризация → DIGEST.md
improve_llm_gaps.py      ← найти пробелы: чего не хватает в документации
improve_llm_contact.py   ← персонализированные письма авторам
```

Все скрипты используют **claude-haiku-4-5** (дешёвый, быстрый) и **prompt caching**.

---

## improve_llm_enrich.py — обогащение файлов

**Что делает:** Читает файл, анализирует и дополняет недостающие секции.

```bash
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...

python scripts/improve_llm_enrich.py --dry-run       # план + стоимость
python scripts/improve_llm_enrich.py --section 05-habr-projects  # ~$0.003
python scripts/improve_llm_enrich.py --file docs/05-habr-projects/memory/yodoca.md
python scripts/improve_llm_enrich.py --force          # перезаписать уже обогащённые
```

**Добавляет:**
- `## Технические детали` — если не было конкретики
- `## Место в архитектуре Svyazi` — как компонент встраивается
- `## Вопросы для автора` — что стоит уточнить
- `## Альтернативы` — похожие проекты и чем отличается

**Стоимость:**
```
21 файл × ~3000 токенов ≈ $0.011 всего
```

**Prompt caching:** Системный промпт кешируется → повторные запросы дешевле на 90%.

---

## improve_llm_qa.py — Q&A по базе знаний

**Что делает:** Вопрос на русском → поиск BM25 по `search_index.json` → ответ Claude с цитатами.

```bash
python scripts/improve_llm_qa.py --question "Что такое NGT Memory?"
python scripts/improve_llm_qa.py --question "Какая лицензия у Yodoca?"
python scripts/improve_llm_qa.py  # интерактивный режим
```

**Пример:**
```
Вопрос: Чем Yodoca отличается от NGT Memory?

Ответ: Yodoca (Apache 2.0) фокусируется на консолидации эпизодической
памяти через SQLite + FTS5, с явным механизмом "забывания" неважных событий.
NGT Memory (BSL 1.1) использует хеббовский ассоциативный граф: связи между
концептами усиливаются при совместных упоминаниях.

Источники:
- docs/05-habr-projects/memory/yodoca.md (score: 0.87)
- docs/05-habr-projects/memory/ngt-memory.md (score: 0.81)
```

**Кеш:** Повторные вопросы берутся из `docs/qa_cache.json` — бесплатно.

---

## improve_llm_summary.py — каскадная суммаризация

**Проблема:** Документ из 50 000 слов не влезает в контекст.

**Решение — Map-Reduce:**
1. **Map:** Каждая секция → краткое резюме (параллельно)
2. **Reduce:** Все резюме → итоговый дайджест

```bash
python scripts/improve_llm_summary.py --file docs/02-anthropic-vacancies/00-intro.md
python scripts/improve_llm_summary.py --section 01-svyazi
```

**utils_chunker.py** автоматически делит большие документы перед отправкой в API.

---

## improve_llm_gaps.py — пробелы в документации

**Что делает:** Анализирует всю базу знаний и находит:
- Темы, которые упоминаются, но не раскрыты
- Вопросы, которые остались без ответа
- Связи между проектами, которые не задокументированы

```bash
python scripts/improve_llm_gaps.py
# → docs/LLM_GAPS.md
```

---

## improve_llm_contact.py — персонализированные письма

**Что делает:** Читает `docs/contacts/<author>.md` + проектный файл → генерирует персонализированное первое сообщение.

```bash
python scripts/improve_llm_contact.py --author kksudo
python scripts/improve_llm_contact.py --all  # все 14 авторов
```

**Правила:**
- Конкретная ссылка на проект (URL из документа)
- Один конкретный технический вопрос
- Объяснение Svyazi в 1 предложении
- Максимум 5–7 предложений

---

## Стратегии работы с большими документами

### Стратегия 1: Sliding Window

```python
# utils_chunker.py
chunks = chunk_by_headers(text, max_words=2000)
for chunk in chunks:
    result = llm.complete(prompt + chunk['text'])
    results.append(result)
final = llm.complete(reduce_prompt + '\n'.join(results))
```

### Стратегия 2: Иерархическая суммаризация

```
Уровень 3: Абзац → 1 предложение
Уровень 2: Секция → 3 предложения  
Уровень 1: Документ → 1 абзац
Уровень 0: Раздел → 1 страница
```

### Стратегия 3: RAG (Retrieval-Augmented Generation)

```python
# Не передавать весь документ — только релевантные пассажи
query = "как работает hot path в Yodoca"
passages = bm25_search(query, passages_index, top_k=5)
context = '\n---\n'.join([p['text'] for p in passages])
answer = llm.complete(f"На основе контекста:\n{context}\n\nВопрос: {query}")
```

**Этот подход реализован в `improve_llm_qa.py`.**

---

## Оценка стоимости

| Операция | Модель | Стоимость |
|---------|-------|----------|
| Обогатить 1 файл (3K токенов) | claude-haiku-4-5 | ~$0.0005 |
| Обогатить 21 файл | claude-haiku-4-5 | ~$0.011 |
| Q&A 100 вопросов (с кешем) | claude-haiku-4-5 | ~$0.05 |
| Суммаризация 1 большого файла | claude-haiku-4-5 | ~$0.002 |
| 14 персонализированных писем | claude-haiku-4-5 | ~$0.003 |
| **Весь проект целиком** | claude-haiku-4-5 | **~$0.10** |

---

## Следующий шаг

После LLM-обогащения → **Часть 8: Экспорт и интеграции**
