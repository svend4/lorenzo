# Обработка больших массивов — Часть 5: Анализ и NLP

> Что можно узнать о массиве документов без использования LLM.

---

## Что такое «анализ без LLM»

Все инструменты этого раздела работают **локально, без API, бесплатно** — на основе классических алгоритмов NLP: TF-IDF, BM25, TextRank, граф, регулярные выражения.

Они медленнее LLM в «понимании», но:
- Детерминированы (один вход = один выход)
- Масштабируются на миллионы документов
- Не требуют оплаты
- Можно запускать в CI/CD

---

## Группа 1: Извлечение сущностей

### improve_entities.py — индекс проектов и технологий

Строит `docs/ENTITIES.md` — таблицу «сущность → сколько раз упомянута → в каких файлах».

```bash
python scripts/improve_entities.py
```

Результат используется `improve_autofill.py` для автоматической расстановки статусов.

---

### improve_named_entity_index.py — NER без ML

Находит без ML-моделей:
- **Проекты:** CamelCase, имена с заглавной, известные OSS-имена
- **Люди:** @handle, «Андрей», «kksudo»
- **Технологии:** Python, SQLite, MCP, BM25
- **Даты:** 2024, Q1 2026, апрель 2026
- **URL:** github.com/…, habr.com/…

```bash
python scripts/improve_named_entity_index.py
python scripts/improve_named_entity_index.py --type projects --min-mentions 3
```

Вывод: `docs/NAMED_ENTITIES.md` + `docs/named_entities.json`

---

### improve_abbreviations.py — словарь аббревиатур

Находит аббревиатуры (2–5 заглавных букв) и их расшифровки в тексте.

```bash
python scripts/improve_abbreviations.py
# MHTML → "MIME HTML archive format"
# BM25  → "Best Match 25, алгоритм ранжирования"
# RAG   → "Retrieval-Augmented Generation"
```

---

## Группа 2: Граф знаний

### improve_concept_graph.py — граф концептов

Строит граф: какие концепты встречаются вместе в одних документах.

```bash
python scripts/improve_concept_graph.py
python scripts/improve_concept_graph.py --format dot  # Graphviz
python scripts/improve_concept_graph.py --top-concepts 50
```

Вывод: `docs/CONCEPT_GRAPH.md` + `docs/concept_graph.json`

**Применение:** Находит неочевидные связи — например, что «CRDT» и «AgentFS» часто упоминаются вместе, хотя нет прямых ссылок.

---

### improve_network.py — граф документов

Строит граф на уровне **файлов** (не концептов): кто на кого ссылается.

```bash
python scripts/improve_network.py
# Вывод: docs/network.dot (Graphviz), docs/NETWORK.md
```

---

### improve_cross_section.py — граф между секциями

Показывает, какие концепты «переходят» из одной секции в другую.

```bash
python scripts/improve_cross_section.py --top 30 --format dot
```

---

## Группа 3: Тематический анализ

### improve_topic_model.py — TF-IDF кластеризация

Без ML делит документы на тематические кластеры.

```bash
python scripts/improve_topic_model.py --topics 8
```

Пример кластеров:
```
Кластер 1 (87 файлов): agentfs, memory, cardindex, vault, filesystem
Кластер 2 (64 файла):  rag, retrieval, embedding, bm25, search
Кластер 3 (51 файл):   sentinel, security, mcp, allowlist, pii
```

---

### improve_clusters.py — похожие документы

TF-IDF cosine similarity → группы похожих файлов.

```bash
python scripts/improve_clusters.py
```

---

## Группа 4: Качество текста

### improve_textrank.py — автоматические резюме

**TextRank** (аналог PageRank для предложений):
1. Строит граф: предложения = вершины, сходство (Jaccard) = рёбра
2. PageRank = важность предложения
3. Топ-N = резюме

```bash
python scripts/improve_textrank.py                    # SUMMARIES.md
python scripts/improve_textrank.py --apply            # вставить в файлы
python scripts/improve_textrank.py --sentences 5      # 5 предложений
python scripts/improve_textrank.py --query "агент с памятью"
```

---

### improve_contradiction_check.py — противоречия

Ищет противоречивые утверждения между файлами.

```bash
python scripts/improve_contradiction_check.py
python scripts/improve_contradiction_check.py --min-confidence 0.6
```

Пример:
```
⚠️ Противоречие (0.72):
  docs/01-svyazi/03-component-catalog.md: "AgentFS поддерживает concurrent доступ"
  docs/01-svyazi/09-architectural-gaps.md: "AgentFS не поддерживает concurrent multi-agent доступ"
```

---

### improve_paragraph_quality.py — качество абзацев

```bash
python scripts/improve_paragraph_quality.py --verbose
```

Находит:
- **Дубли:** одинаковые абзацы в разных файлах (107 найдено)
- **Вода:** абзацы без конкретики («Это интересный подход»)
- **Обрывы:** незаконченные мысли

---

### improve_passive_voice.py — стиль

Находит пассивный залог, номинализации, канцеляризмы.

```bash
python scripts/improve_passive_voice.py
# "было принято решение" → "решили"
# "осуществляется обработка" → "обрабатывается"
```

---

### improve_vocabulary_richness.py — лексическое разнообразие

TTR (Type-Token Ratio), STTR (стандартизированный), hapax legomena (слова, встреченные 1 раз).

```bash
python scripts/improve_vocabulary_richness.py --section 01-svyazi
```

---

## Группа 5: Временной анализ

### improve_timeline_events.py — хронология

Извлекает даты и события из текстов → `docs/TIMELINE.md`.

```bash
python scripts/improve_timeline_events.py --from 2023 --to 2026
```

---

### improve_version_diff.py — семантический diff

Показывает не diff кода, а **что изменилось по смыслу** между коммитами.

```bash
python scripts/improve_version_diff.py --last 10
```

---

## Итог: что можно узнать без LLM

| Вопрос | Инструмент |
|--------|-----------|
| Какие проекты упоминаются чаще всего? | `improve_entities.py` |
| Какие концепты связаны между собой? | `improve_concept_graph.py` |
| Есть ли противоречия? | `improve_contradiction_check.py` |
| О чём каждый файл в 3 предложениях? | `improve_textrank.py` |
| На какие темы делится весь корпус? | `improve_topic_model.py` |
| Где дублируется информация? | `improve_paragraph_quality.py` |
| Что произошло когда? | `improve_timeline_events.py` |

---

## Следующий шаг

После анализа → **Часть 6: Поиск (BM25, фасеты, пассажи)**
