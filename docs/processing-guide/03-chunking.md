# Обработка больших массивов — Часть 3: Разбивка и чанкинг

> Как правильно делить большой текст на смысловые части.

---

## Зачем делить?

Большой файл (50 000+ слов) — проблема для:
- **Поиска**: невозможно найти конкретный факт
- **LLM**: не влезает в контекстное окно
- **RAG**: слишком широкий чанк = шум в ответе
- **Навигации**: человек не читает монолит
- **Версионирования**: любое изменение — diff всего файла

---

## Стратегии разбивки

### Стратегия 1: По заголовкам (H2/H3) — реализовано

```python
# utils_chunker.py — chunk_by_headers()
```

**Как работает:**
- H1 = документ
- H2 = раздел → отдельный файл
- H3 = подраздел → чанк внутри файла

**Плюсы:** Сохраняет авторскую структуру, смысловые границы чёткие.
**Минусы:** Если автор плохо структурировал — секции неравномерные.

**Скрипт:** `part2_split_md.py`, `improve_text_segmenter.py`

```bash
python scripts/improve_text_segmenter.py --dry-run        # план
python scripts/improve_text_segmenter.py --apply --section 02-anthropic-vacancies
```

---

### Стратегия 2: Семантические чанки — реализовано

```python
# improve_chunk_semantic.py
```

**Как работает:**
1. H2/H3 = первичные границы
2. Если секция > 500 слов → дробить по абзацам
3. Если секция < 50 слов → объединить с соседней
4. Каждый чанк: `{file, section, text, word_count, tokens_est}`

**Вывод:** `docs/all_chunks.jsonl` — готово для RAG

```bash
python scripts/improve_chunk_semantic.py
python scripts/improve_chunk_semantic.py --section 05-habr-projects
```

**Пример чанка:**
```json
{
  "file": "docs/04-ai-collaborations/01-executive-summary.md",
  "section": "Executive summary",
  "text": "Если смотреть не на отдельные статьи...",
  "word_count": 312,
  "tokens_est": 520,
  "chunk_id": "04-ai-collaborations/01#executive-summary"
}
```

---

### Стратегия 3: Разбивка по абзацам (BM25-уровень) — реализовано

```python
# improve_passage_retrieval.py
```

**Как работает:** Каждый абзац (≥ 20 слов) — отдельная единица поиска.

**Зачем:** Для точного поиска — не «в каком файле», а «в каком абзаце».

```bash
python scripts/improve_passage_retrieval.py --index
python scripts/improve_passage_retrieval.py --query "ассоциативный граф памяти" --top 5
```

---

### Стратегия 4: Разбивка по теме (TF-IDF рубрикация) — реализовано

```python
# improve_reclassify.py
# improve_topic_model.py
```

**Как работает:** TF-IDF по словам → определяет к какому тематическому кластеру относится файл → перемещает если ошибочно классифицирован.

```bash
python scripts/improve_reclassify.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_topic_model.py --topics 8
```

---

### Стратегия 5: Слияние коротких файлов по теме — реализовано

```python
# improve_merge_by_topic.py
# improve_merge_short.py
```

**Проблема:** После дробления появляются файлы по 50–100 слов — слишком мелко.

**Решение:**
- `merge_short`: объединяет файлы < 100 слов с соседними
- `merge_by_topic`: TF-IDF кластеризация → близкие файлы → один файл

```bash
python scripts/improve_merge_by_topic.py --section 02-anthropic-vacancies --dry-run
python scripts/improve_merge_short.py --min-words 150
```

---

### Стратегия 6: Разбивка по языку — реализовано

```python
# improve_language_split.py
```

**Проблема:** Файлы с MIX RU/EN — сложно индексировать, читать, переводить.

```bash
python scripts/improve_language_split.py                  # статистика
python scripts/improve_language_split.py --split          # разделить
```

---

## Параметры разбивки: что выбрать

| Задача | Стратегия | Размер чанка |
|--------|----------|-------------|
| RAG (LLM-поиск) | Семантический | 200–500 слов |
| Полнотекстовый поиск | По заголовкам | 500–2000 слов |
| Точный поиск фактов | По абзацам | 50–200 слов |
| Навигация человека | По заголовкам H2 | 300–1500 слов |
| Тематическое хранение | По теме (TF-IDF) | любой |

---

## Инструмент выбора стратегии: utils_chunker.py

```python
from scripts.utils_chunker import chunk_by_headers, estimate_tokens

chunks = chunk_by_headers(text, max_words=500, min_words=50)
for chunk in chunks:
    print(f"{chunk['section']}: {chunk['word_count']} слов, ~{estimate_tokens(chunk['text'])} токенов")
```

---

## Следующий шаг

После разбивки → **Часть 4: Структурирование (теги, TOC, шаблоны)**
