# Обработка больших массивов — Часть 10: Инновационные подходы

> Что можно сделать сегодня с новыми инструментами — и что ещё не придумано.

---

## Граница между «уже есть» и «ещё нет»

| Уровень | Статус | Пример |
|---------|--------|--------|
| grep, BM25, TF-IDF | ✅ реализовано | `improve_keyword_index.py` |
| Структурирование, TOC, теги | ✅ реализовано | `improve_auto_toc.py` |
| TextRank, граф концептов | ✅ реализовано | `improve_textrank.py` |
| LLM-обогащение (API) | ✅ реализовано | `improve_llm_enrich.py` |
| Векторный поиск | 🟡 план | sentence-transformers + FAISS |
| Мультиагентная обработка | 🟡 концепт | каждый агент = специалист |
| Автономный агент-документатор | 🔴 не реализовано | watcher + LLM + PR |
| Граф знаний с LLM-NER | 🔴 план | spaCy + Claude → Neo4j/Kuzu |
| Инкрементальное обучение | 🔴 концепт | база знаний обновляет модель |

---

## Уровень A: Векторный поиск (следующий шаг)

**Почему BM25 не всегда достаточно:**
```
Запрос: "как агент запоминает контекст разговора"
BM25 найдёт: файлы со словами "агент", "запоминает", "контекст"
Векторный найдёт: файлы о memory, episodic storage, session persistence — даже без этих слов
```

**Реализация:**

```python
# Шаг 1: Индексация (один раз)
from sentence_transformers import SentenceTransformer
import faiss, json, numpy as np

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')  # 200 МБ, CPU

chunks = [json.loads(l) for l in open('docs/all_chunks.jsonl')]
texts = [c['text'] for c in chunks]
embeddings = model.encode(texts, batch_size=32, show_progress_bar=True)

# Сохранить индекс
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings.astype('float32'))
faiss.write_index(index, 'docs/vector_index.faiss')

# Шаг 2: Поиск
query = "как агент запоминает контекст"
query_vec = model.encode([query]).astype('float32')
scores, ids = index.search(query_vec, k=10)

for score, idx in zip(scores[0], ids[0]):
    print(f"[{score:.3f}] {chunks[idx]['file']} — {chunks[idx]['text'][:100]}")
```

**Гибридный поиск (BM25 + вектор):**
```python
# Reciprocal Rank Fusion — объединяет оба ранжирования
def rrf(bm25_results, vector_results, k=60):
    scores = {}
    for rank, (doc, _) in enumerate(bm25_results):
        scores[doc] = scores.get(doc, 0) + 1/(k + rank + 1)
    for rank, (doc, _) in enumerate(vector_results):
        scores[doc] = scores.get(doc, 0) + 1/(k + rank + 1)
    return sorted(scores.items(), key=lambda x: -x[1])
```

**Стоимость:**
- Модель: `paraphrase-multilingual-MiniLM-L12-v2` — бесплатно, CPU, ~200 МБ
- Индексация 1000 чанков: ~30 сек на CPU
- Поиск: < 10 мс

---

## Уровень B: Граф знаний с LLM-NER

**Концепция:** Не просто «кто упоминается», а «кто с кем связан и как».

```python
# Сейчас (regex NER):
entities = extract_by_regex(text)  # ["AgentFS", "kksudo", "SQLite"]

# Будущее (LLM NER):
response = claude.complete(f"""
Извлеки из текста:
1. Сущности: [тип: проект|человек|технология|концепт]
2. Отношения: (субъект) → [тип: использует|создан_автором|конкурент|зависит_от] → (объект)

Текст: {chunk}

Формат: JSON
""")
# → {"entities": [...], "relations": [{"from": "Yodoca", "type": "использует", "to": "SQLite"}]}
```

**Граф-база (без внешних сервисов):**
```python
# Kuzu — встраиваемая граф-БД (как SQLite, но для графов)
import kuzu

db = kuzu.Database('docs/knowledge_graph.kuzu')
conn = kuzu.Connection(db)

conn.execute("CREATE NODE TABLE Project(name STRING, PRIMARY KEY(name))")
conn.execute("CREATE REL TABLE USES(FROM Project TO Project)")

conn.execute("MERGE (p:Project {name: $name})", {"name": "Yodoca"})
conn.execute("MERGE (t:Project {name: $name})", {"name": "SQLite"})
conn.execute("MATCH (a:Project {name:'Yodoca'}),(b:Project {name:'SQLite'}) CREATE (a)-[:USES]->(b)")

# Запрос: что использует AgentFS?
result = conn.execute("MATCH (a:Project {name:'AgentFS'})-[:USES]->(b) RETURN b.name")
```

**Применение:**
- «Покажи все проекты, которые используют SQLite» — за 1 запрос
- «Найди путь между AgentFS и NGT Memory через общие зависимости»
- Визуализация в D3.js / Obsidian Graph

---

## Уровень C: Мультиагентная обработка

**Проблема:** Один LLM-агент обрабатывает документ последовательно. При 1000 файлах — это медленно и дорого.

**Решение:** Специализированные агенты работают параллельно.

```python
# Концепция pipeline с агентами
agents = {
    "extractor":    Agent(role="Извлекай факты и даты"),
    "summarizer":   Agent(role="Создавай краткие резюме"),
    "tagger":       Agent(role="Назначай теги и категории"),
    "linker":       Agent(role="Находи связи с другими документами"),
    "qa_generator": Agent(role="Генерируй вопросы-ответы"),
}

# Параллельная обработка батча файлов
async def process_batch(files: list[Path]):
    tasks = []
    for f in files:
        text = f.read_text()
        for agent in agents.values():
            tasks.append(agent.process(text))
    results = await asyncio.gather(*tasks)
    return merge_results(results)
```

**Claude Agent SDK:**
```python
# С Anthropic SDK — нативная поддержка агентных паттернов
import anthropic

client = anthropic.Anthropic()

def extract_facts(text):
    return client.messages.create(
        model="claude-haiku-4-5",
        system="Ты специалист по извлечению фактов. Только факты, без мнений.",
        messages=[{"role": "user", "content": text}]
    )

def find_contradictions(fact_a, fact_b):
    return client.messages.create(
        model="claude-haiku-4-5",
        system="Ты детектор противоречий. Отвечай YES/NO + объяснение.",
        messages=[{"role": "user", "content": f"Факт 1: {fact_a}\nФакт 2: {fact_b}"}]
    )
```

---

## Уровень D: Автономный агент-документатор

**Идея:** Агент постоянно следит за кодовой базой и сам поддерживает документацию актуальной.

```
git push → webhook → агент читает diff →
    анализирует изменения →
    обновляет docs/ →
    создаёт PR →
    ожидает апрув →
    мержит
```

**Пайплайн:**
```python
# 1. Триггер: изменился файл скрипта
changed_scripts = get_git_diff_files("scripts/")

# 2. Агент читает скрипт + текущую документацию
for script in changed_scripts:
    code = read_file(script)
    current_doc = read_file(f"docs/{script.stem}.md")
    
    # 3. LLM определяет что изменилось по смыслу
    delta = claude.complete(f"""
    Старая документация: {current_doc}
    Новый код: {code}
    
    Что изменилось в поведении? Обнови только изменившиеся секции.
    """)
    
    # 4. Обновляет документ
    write_file(f"docs/{script.stem}.md", apply_delta(current_doc, delta))

# 5. Создаёт PR
create_pr(title="docs: auto-update from code changes [bot]")
```

**Существующая инфраструктура в этом проекте:**
- `improve_watcher.py` — уже следит за файлами
- `mcp_server.py` → `run_improve()` — уже умеет запускать скрипты
- `.github/workflows/docs.yml` — уже запускает на push
- **Недостаёт:** LLM-агент, который читает diff и пишет документацию

---

## Уровень E: Инкрементальное обучение базы знаний

**Концепция:** База знаний не просто хранится — она «учится» при добавлении новых документов.

```python
# Проблема: добавили 100 новых файлов → весь индекс устарел
# Решение: инкрементальное обновление

class IncrementalKnowledgeBase:
    def __init__(self, index_path):
        self.index = load_faiss(index_path)
        self.metadata = load_json("docs/vector_metadata.json")
    
    def add_document(self, file_path):
        text = file_path.read_text()
        new_chunks = semantic_chunk(text)
        new_embeddings = encode(new_chunks)
        
        # Добавить новые чанки в индекс
        self.index.add(new_embeddings)
        self.metadata.extend([{"file": str(file_path), "chunk_id": i} 
                               for i in range(len(new_chunks))])
        
        # Пересчитать BM25 только для изменившихся файлов
        self.bm25.update(file_path, new_chunks)
        
        # Обновить граф концептов
        self.concept_graph.merge(extract_concepts(new_chunks))
    
    def remove_document(self, file_path):
        # Удалить из всех индексов по метаданным
        chunk_ids = [m['id'] for m in self.metadata if m['file'] == str(file_path)]
        self.index.remove_ids(chunk_ids)
```

---

## Уровень F: Темпоральное рассуждение

**Задача:** Не просто «что написано», а «что изменилось, когда и почему».

```python
# improve_temporal_reasoning.py (концепт)

def analyze_evolution(file_path: Path, commits: int = 20):
    """Анализирует эволюцию документа во времени."""
    history = git_log(file_path, n=commits)
    
    snapshots = []
    for commit in history:
        text = git_show(commit.hash, file_path)
        facts = extract_facts_llm(text)
        snapshots.append({"date": commit.date, "facts": facts, "hash": commit.hash})
    
    # Найти: какие факты появились, какие исчезли, какие противоречат
    timeline = diff_facts(snapshots)
    
    return {
        "appeared": timeline["new"],      # факты добавленные после X
        "disappeared": timeline["removed"], # факты убранные после Y
        "changed": timeline["modified"],   # факты изменившиеся
        "stable": timeline["unchanged"],   # факты не менявшиеся
    }
```

**Применение:**
- «Когда AgentFS перестал поддерживать concurrent доступ?»
- «Покажи как изменилась архитектура Svyazi за 6 месяцев»
- Автоматический changelog на основе семантики, а не кода

---

## Уровень G: Голосовой пайплайн (Speech-to-Knowledge)

```
Голосовое сообщение / подкаст
    ↓ Whisper (транскрипция, бесплатно локально)
    ↓ improve_segment_transcript.py (разбивка по темам)
    ↓ improve_llm_enrich.py (структурирование)
    ↓ docs/voice-notes/YYYY-MM-DD-{title}.md
    ↓ improve_search_index.py (добавить в индекс)
```

```python
# whisper_to_knowledge.py (концепт)
import whisper

model = whisper.load_model("base")  # 74 МБ, CPU
result = model.transcribe("meeting-2026-04-29.mp3", language="ru")

# Разбить по временным меткам на темы
segments = segment_by_topic(result['segments'])

for i, seg in enumerate(segments):
    write_doc(f"docs/voice-notes/{date}-topic-{i}.md", seg['text'])
```

---

## Уровень H: Синтез из нескольких репозиториев

**Задача:** Объединить знания из нескольких отдельных репозиториев в единую базу.

```python
# cross_repo_synthesizer.py (концепт)

REPOS = [
    "~/projects/agentfs-research",
    "~/projects/yodoca-notes", 
    "~/projects/lorenzo",
    "~/projects/sentinel-analysis",
]

def synthesize():
    all_chunks = []
    for repo in REPOS:
        chunks = load_chunks(repo + "/docs/all_chunks.jsonl")
        for c in chunks:
            c['source_repo'] = repo
        all_chunks.extend(chunks)
    
    # Единый индекс поверх всех репозиториев
    unified_index = build_bm25(all_chunks)
    unified_vectors = build_faiss(all_chunks)
    
    # Найти связи между репозиториями
    cross_refs = find_cross_repo_concepts(all_chunks)
    
    write_json("~/knowledge-os/unified_index.json", unified_index)
    write_json("~/knowledge-os/cross_refs.json", cross_refs)
```

---

## Уровень I: Не придуманные подходы

### Живой документ (Living Document)

Документ, который сам обновляется при появлении новых данных:

```markdown
<!-- @auto-update: query="AgentFS concurrent access", source="docs/", interval=daily -->
## Статус AgentFS

*Последнее обновление: 2026-04-29 (автоматически)*

AgentFS поддерживает concurrent read, но не concurrent write...
```

Скрипт находит все `<!-- @auto-update -->` директивы, выполняет запрос BM25/LLM и заменяет содержимое секции.

---

### Граф аргументов (Argument Graph)

Не просто «что сказано», а «почему так решили»:

```
Утверждение: "AgentFS не поддерживает concurrent write"
    ↑ Основание: "В коде найден GIL в _write_lock"
    ↑ Контр-аргумент: "В v0.3 добавили MVCC" (источник: commit abc123)
    ↑ Статус: ОТКРЫТЫЙ ВОПРОС (спросить kksudo)
```

Такой граф позволяет отследить «где мы приняли неверное решение на основе устаревших данных».

---

### Нейросеть на собственной базе (Domain-Specific Fine-tuning)

```python
# Использовать базу знаний как датасет для fine-tuning
# Тип: instruction-tuning

training_data = []
for qa in load_json("docs/qa_cache.json"):
    training_data.append({
        "instruction": qa['question'],
        "output": qa['answer'],
        "context": qa['sources'],
    })

# Fine-tune claude-haiku на этих данных →
# модель, которая знает проект лучше базовой
```

---

### Рефлексивный агент (Self-Improving Documentation)

```
Агент читает документ →
    Находит неясность →
    Формулирует вопрос →
    Ищет ответ в других документах →
    Если нашёл → дополняет документ →
    Если не нашёл → добавляет в docs/OPEN_QUESTIONS.md →
    Пересматривает логику своего поиска → улучшает алгоритм
```

Этот паттерн называется **ReAct** (Reasoning + Acting) — агент итеративно уточняет понимание.

---

## Дорожная карта реализации

| Фаза | Что делаем | Инструменты | Стоимость |
|------|-----------|-------------|---------|
| Сейчас | BM25 + TextRank + LLM API | всё в `scripts/` | ~$0.10 |
| Следующий шаг | Векторный поиск | sentence-transformers + FAISS | 0 |
| Через месяц | Граф знаний | Kuzu + claude-haiku | ~$1 |
| Через квартал | Мультиагентный пайплайн | Claude Agent SDK | ~$5/запуск |
| Через год | Автономный агент | MCP + GitHub API + LLM | ~$20/мес |

---

## Вывод

Текущая система (`scripts/improve_*.py`) реализует уровни 1–4 полностью и бесплатно.

Уровни 5–8 (векторный поиск, граф знаний, мультиагент, автономный агент) технически готовы к реализации — инфраструктура (`mcp_server.py`, `improve_watcher.py`, `all_chunks.jsonl`) уже есть. Нужно только:
1. Добавить `sentence-transformers` + FAISS (уровень A)
2. Добавить Kuzu + LLM-NER (уровень B-C)
3. Подключить к существующему `improve_watcher.py` (уровень D)

Остальные уровни (E-I) — это направления исследований, которые можно реализовать поверх существующей базы.

---

← **Часть 9: Автоматизация** | [Содержание](README.md)
