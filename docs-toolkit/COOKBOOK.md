# docs-toolkit Cookbook

10 рецептов по типовым задачам. Каждый — самодостаточный, скопировал и запустил.
Все примеры используют stdlib-only функциональность; внешние модели/индексы
— опциональные подключаемые ингредиенты.

Если только начинаете знакомство — смотрите [`README.md`](README.md) и
[`examples/composition/`](examples/composition/).

---

## 1. «Хочу RAG над моими markdown-файлами» — quickstart

**Задача:** одна функция, синхронно, без сети, без `pip install` лишнего.

```python
from docstoolkit.rag import ask

# Echo answerer — никаких LLM, ответ строится из retrieved пассажей.
# Над реальными docs/ автоматически собирается hybrid индекс.
result = ask("Что такое RAG?", method="hybrid", top_k=5)
print(result.answer)
for c in result.citations:
    print(f"  [{c['n']}] {c['title']} ({c['doc_id']}) — score {c['score']:.2f}")
```

**Подключить Anthropic / OpenAI:**

```bash
pip install -e ".[anthropic]"     # или ".[openai]"
export ANTHROPIC_API_KEY=...
```

```python
result = ask("Что такое RAG?", answerer="anthropic",
             model="claude-haiku-4-5-20251001", top_k=5)
```

---

## 2. «Хочу проверить, что ответ опирается на источники» — provenance + CI

**Задача:** для каждого утверждения в ответе показать с какой вероятностью
оно поддерживается корпусом + bootstrap-доверительный интервал.

```python
from docstoolkit.rag import ask_high_quality
from docstoolkit.rerank.reranker import TFIDFReranker

result = ask_high_quality(
    "Каковы три основных компонента RAG?",
    reranker=TFIDFReranker(),   # M2 cross-encoder rerank
    top_k=5,
)

print(result.answer)
print(f"\nProvenance overall confidence: "
      f"{result.provenance.overall_confidence:.2f}")
for claim in result.provenance.claims:
    ci_low, ci_high = claim.confidence_ci
    print(f"  • {claim.text}")
    print(f"    confidence {claim.confidence:.2f} (CI {ci_low:.2f}–{ci_high:.2f})")
    for src in claim.sources:
        print(f"    ← {src.doc_id} (sim {src.similarity:.2f})")
```

Преимущество: каждый claim либо привязан к пассажу с CI, либо помечен
`unsupported`. Используйте `result.provenance.high_confidence_claims(0.7)`
для фильтрации.

---

## 3. «Хочу видеть, сколько времени съела каждая фича» — trace

**Задача:** debug latency при сложной композиции.

```python
from docstoolkit.rag import ask_full_stack

result = ask_full_stack(
    "Сложный вопрос с глубоким рассуждением",
    top_k=3,
)

# Markdown-таблица всех стадий
print(result.to_trace_markdown())

# Программный доступ
for ev in result.trace:
    print(f"{ev.stage:25} {ev.t_ms:6.2f} ms  {ev.payload}")
```

`TraceEvent(stage, t_ms, payload)` собирается на каждой стадии:
`retrieve / filter / rerank / personality_rerank / negotiation_auction /
assemble / answer / mapreduce_answer / debate / facets / provenance /
got / self_rag_iter / memory_recall`.

---

## 4. «Хочу A/B-тест разных retrievers» — bandit

**Задача:** автоматически выбирать вариант retrievera, который чаще даёт
успешный результат, без статичной конфигурации.

```python
from docstoolkit.bandit import BanditExperiment
from docstoolkit.rag.bandit_ask import ask_with_bandit, evaluate_record

exp = BanditExperiment("rag-AB", arms=["bm25", "hybrid", "semantic"])
variants = {
    "bm25":     {"method": "bm25"},
    "hybrid":   {"method": "hybrid"},
    "semantic": {"method": "semantic"},
}

for question in production_queries:
    result, picked = ask_with_bandit(question, exp, variants)
    # Решите как мерить успех: длина ответа, click-through, манивал и т.д.
    success = len(result.answer) > 100 and len(result.citations) >= 2
    evaluate_record(exp, picked, result, success_threshold=0.5)

# После сотни-другой запросов:
print(f"Bandit converged on: {exp.choose()}")
```

Bandit использует UCB1; не требует ML-зависимостей.

---

## 5. «Хочу найти устаревшие документы» — document metabolism

**Задача:** найти документы, которые давно не обновлялись, и предложить
их перезапись на основе свежих источников из корпуса.

```python
from docstoolkit.metabolism import propose_rewrite, rank_stale_documents

docs = [
    ("docs/old/architecture", content_old, "2024-01-15T00:00:00Z"),
    ("docs/old/intro",        content_intro, "2024-03-01T00:00:00Z"),
    ("docs/fresh/recent",     content_fresh, "2026-05-01T00:00:00Z"),
]

stale = rank_stale_documents(docs, threshold_days=180.0)
for doc_id, age in stale:
    print(f"  стало: {doc_id} ({age.days_since_update:.0f} дней)")

# Для самого старого — сгенерировать proposal
target_id, age = stale[0]
target_content = next(c for d, c, _ in docs if d == target_id)
proposal = propose_rewrite(
    target_id, target_content,
    sources=[("docs/fresh/recent", "Recent thoughts about same topic.")],
    last_modified_iso="2024-01-15T00:00:00Z",
    min_relevance=0.1,
)
print(f"Состояние: {proposal.target_state.value}")
print(f"Фрагменты для абсорбции: {len(proposal.fragments)}")
```

См. ещё `examples/composition/06_path_C.py`.

---

## 6. «Хочу сделать запрос „как было год назад“» — time-travel

**Задача:** ответить на запрос _как если бы корпус был в состоянии
определённого git commit_.

```python
from docstoolkit.rag import ask

result = ask(
    "Какова была архитектура полгода назад?",
    at_commit="abc123def",  # git SHA
    top_k=5,
)

print(result.answer)
print(f"Corpus snapshot: {result.at_commit}")
```

Под капотом: `docstoolkit.temporal.query_at_time` делает `git show <SHA>:<file>`
для каждого retrieved doc — никаких внешних индексов истории.

---

## 7. «Хочу персонализировать RAG под пользователя» — user profiles

```python
from docstoolkit.conversation.profile import (
    ProfileStore, UserProfile,
)
from docstoolkit.rag import ask_personalized

store = ProfileStore()  # .docstoolkit/profiles.sqlite
store.save(UserProfile(
    user_id="alice",
    preferred_retriever="bm25",
    preferred_sections=["05-habr-projects/memory"],
    interests=["agent memory", "MCP"],
))
store.close()

result = ask_personalized(
    "Каковы лучшие практики работы с памятью?",
    user_id="alice",
    top_k=5,
)

# Автоматически:
#  - retriever переключён на BM25 (profile.preferred_retriever)
#  - boost для passages из memory section
#  - retrieved doc_ids записаны в profile.read_docs (S7 read-receipts)
#  - на следующих запросах эти же docs получают -0.1 score penalty
```

---

## 8. «Хочу обнаружить пробелы в корпусе» — counterfactual probing

**Задача:** какие вопросы _нельзя ответить_ без конкретного документа?
Полезно при пересмотре корпуса.

```python
from docstoolkit.rag.advanced import probe_counterfactual

corpus = {
    "a": "Python and RAG together solve grounding problems.",
    "b": "Docker enables reproducible deployment.",
    "c": "Python is widely used for scripting.",
}

# «Что произойдёт, если убрать документ 'a'?»
result = probe_counterfactual("How does Python solve grounding?",
                              corpus, "a")
print(f"affected: {result['affected']}, severity: {result['severity']}")
# affected=True → ответ существенно изменится → документ 'a' критичен
```

Используется внутри `examples/composition/07_standalone.py`.

---

## 9. «Хочу собрать федеративную golden-метрику без раскрытия данных» — N5

**Задача:** несколько нод оценивают свои корпусы локально, отдают только
агрегированные числа с дифференциальной приватностью.

```python
from docstoolkit.rag.advanced import federated_aggregate

# На каждой ноде локально:
local_metrics = [
    {"precision": 0.83, "recall": 0.71, "f1": 0.77},  # node A
    {"precision": 0.79, "recall": 0.68, "f1": 0.73},  # node B
    {"precision": 0.81, "recall": 0.74, "f1": 0.77},  # node C
]

# Centralised aggregator получает только шумовые средние:
aggregated = federated_aggregate(
    local_metrics,
    epsilon=1.0,        # privacy budget
    mechanism="laplace",
)
print(aggregated)
# {"precision": 0.80 ± 0.04, "recall": 0.71 ± 0.04, "f1": 0.76 ± 0.04}
```

Текущая реализация — stub-уровень; полный stack см. в Фазе VI roadmap
([`DEVELOPMENT_STATUS.md`](DEVELOPMENT_STATUS.md)).

---

## 10. «Хочу всё одновременно» — full-stack composition

**Задача:** stress-тест и understanding: что происходит, когда включены
ВСЕ 14 совместимых фич.

```python
from docstoolkit.rag import ask_full_stack
from docstoolkit.memory import TieredMemory
from docstoolkit.personality import CognitiveProfile
from docstoolkit.rerank.reranker import TFIDFReranker

memory = TieredMemory()
personality = CognitiveProfile(
    skepticism=0.7, synthesis=0.5, verification=0.6,
    pragmatism=0.4, exploration=0.5,
)

result = ask_full_stack(
    "Как ансамбль агентов с памятью улучшает grounding?",
    user_id="alice",
    memory=memory,
    personality=personality,
    reranker=TFIDFReranker(),
    top_k=3,
)

print(result.answer)
print(f"Trace ({len(result.trace)} stages, {result.duration_ms} ms total):")
print(result.to_trace_markdown())
```

Запустите `examples/composition/08_full_stack.py` локально, чтобы увидеть
вывод. Каждый раздел `trace` показывает, какая фича сколько потратила.

---

## Полезные ссылки

| Документ | Что внутри |
|---|---|
| [`README.md`](README.md) | Установка, quick-start, карта модулей |
| [`PROFILES.md`](PROFILES.md) | Полный feature-индекс 17 kwargs + 6 пресетов |
| [`API.md`](API.md) | Сигнатуры всех публичных API |
| [`DEVELOPMENT_STATUS.md`](DEVELOPMENT_STATUS.md) | Текущий статус + дорожная карта на 9 фаз |
| [`bench/BENCHMARKS.md`](bench/BENCHMARKS.md) | Реальные накладные расходы каждой фичи |
| [`examples/composition/`](examples/composition/) | 8 runnable demo-скриптов |
| [`CHANGELOG.md`](CHANGELOG.md) | История версий |
