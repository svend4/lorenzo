# Personalization & Production Guide — docs-toolkit

Документация фичей Пути A — Quick Value (Sprint 54-60 / S6, S4, M2, M5, S7).
Все 5 фич доступны через single entry point `docstoolkit.rag.ask()`.

## Sprint 54 / S6 — Per-User Preferences

`UserProfile` хранит per-user defaults: `preferred_retriever`, `preferred_sections`,
`interests`, `read_docs`. Профиль персистится в SQLite (`.docstoolkit/profiles.sqlite`).

### CLI / Python API

```python
from docstoolkit.conversation.profile import (
    ProfileStore, UserProfile, apply_profile,
)
from docstoolkit.rag import ask

store = ProfileStore()
store.save(UserProfile(
    user_id="alice",
    preferred_retriever="bm25",
    preferred_sections=["05-habr-projects"],
    interests=["memory", "agents"],
))

# Alice's query — автоматически использует bm25 + section boost + interest injection
result = ask("Что такое RAG?", user_id="alice")
```

Приоритет: явный `method=...` в `ask()` всегда побеждает `preferred_retriever`.
Если профиль отсутствует — поведение не меняется (no-op).

### apply_profile middleware

Используется внутри `ask()`, но доступна как public API для agent.run /
custom pipelines:

```python
from docstoolkit.conversation.profile import apply_profile

kwargs = {"top_k": 5}
apply_profile("alice", kwargs)  # mutates in place + returns
# kwargs == {"top_k": 5, "method": "bm25", "_profile": <UserProfile>}
```

## Sprint 56 / S4 — Citation Graph + PageRank Boost

`PageRankBoostedRetriever` оборачивает любой retriever и поднимает в выдаче
документы с высоким PageRank по графу внутренних markdown-ссылок.

```python
from pathlib import Path
from docstoolkit.citations import PageRankBoostedRetriever
from docstoolkit.rag.retriever import Retriever

base = Retriever(method="hybrid")
boosted = PageRankBoostedRetriever(
    base=base,
    corpus_dir=Path("docs"),
    alpha=0.3,   # boost intensity
    cap=0.4,     # ceiling: no doc can multiply >1.4x
)
results = boosted.search("RAG", top_k=5)
```

PageRank вычисляется lazy при первом `search()`; кешируется в инстансе.
Для готового lookup-словаря:

```python
from docstoolkit.citations import build_pr_lookup
pr_scores = build_pr_lookup(Path("docs"))  # {doc_id: score}
```

## Sprint 56 / M5 — Continuous Online Eval

Sampler + SQLite store + drift detection + HTML dashboard:

```python
from docstoolkit.online_eval import (
    OnlineEvalSampler, OnlineEvalStore, OnlineEvalRunner,
    render_dashboard,
)
from docstoolkit.rag import ask

store   = OnlineEvalStore()
runner  = OnlineEvalRunner(
    store=store,
    golden_dataset_path=Path("docs/eval/golden.yaml"),
    sampler=OnlineEvalSampler(sample_rate=0.05),
)

# Production query — 5% сэмплируется и сравнивается с golden dataset
result = ask("вопрос", eval_runner=runner)

# Weekly drift check
for d in runner.compute_drift(window_days=7):
    if d.significant:
        print(f"DRIFT {d.metric}: {d.delta:+.3f}")

# HTML dashboard
Path("dashboard.html").write_text(render_dashboard(store), encoding="utf-8")
```

`eval_runner` — best-effort: исключения не валят пользовательский запрос.

## Sprint 59 / M2 — Cross-Encoder Reranking

Pipeline по умолчанию забирает `top_k * 3` кандидатов из retriever, режет
до `top_k` после реранкинга:

```python
from docstoolkit.rag import ask
from docstoolkit.rerank.reranker import get_reranker

# stdlib-only — TF-IDF cosine reranker
result = ask("query", reranker=get_reranker("tfidf"))

# BGE cross-encoder (опционально, fallback на TF-IDF если зависимостей нет)
result = ask("query", reranker=get_reranker("bge"))

# LLM-judge реранкинг
result = ask("query", reranker=get_reranker("llm", answerer_name="anthropic"))
```

| Реранкер | Зависимости | Качество | Скорость |
|----------|-------------|----------|----------|
| `noop`   | none        | baseline | мгновенно |
| `tfidf`  | stdlib      | +5-10% P@5 | <1ms |
| `bge`    | sentence-transformers | +15-25% P@5 | 50-200ms/passage |
| `llm`    | anthropic API | best | seconds + cost |

## Sprint 60 / S7 — Read-Receipt Tracking

При `user_id` любой `ask()` автоматически добавляет извлечённые
`doc_id` в `profile.read_docs`. `PersonalizedRetriever` затем
штрафует уже прочитанные документы (-0.1 score), создавая
"recency loop" — пользователь видит новое чаще.

```python
result1 = ask("query", user_id="alice")
# Alice прочитала doc1, doc2, doc3

result2 = ask("query", user_id="alice")
# Те же документы теперь со штрафом -0.1; новые поднимаются выше
```

Логирование чтения — best-effort, не блокирует ответ при сбое БД.

## Композиция всех фич

Все 5 sprint-фич сочетаются ортогонально:

```python
result = ask(
    "Что такое RAG?",
    user_id="alice",                     # S6 + S7
    reranker=get_reranker("bge"),        # M2
    eval_runner=runner,                  # M5
)
# 1. apply_profile → method="bm25" (Alice's preference)
# 2. PersonalizedRetriever → section boost + read penalty
# 3. retrieve top_k*3 candidates
# 4. BGE reranker → top_k
# 5. answer
# 6. sample for online eval
# 7. mark all retrieved docs as read for Alice
```

PageRank-boost применяется когда вы оборачиваете базовый Retriever:

```python
from docstoolkit.citations import PageRankBoostedRetriever
# (потребует custom pipeline; будет интегрировано в ask() в Sprint 61)
```

## Что дальше — Путь B / C

См. [`docs/ROADMAP/02-MEDIUM.md`](../docs/ROADMAP/02-MEDIUM.md),
[`03-INNOVATIVE.md`](../docs/ROADMAP/03-INNOVATIVE.md),
[`04-NOVEL.md`](../docs/ROADMAP/04-NOVEL.md).

Ближайшие задачи Пути B:
- **I3** Provenance + confidence intervals (5 спринтов)
- **M1** Knowledge graph multi-hop (4 спринта)
- **I1** Self-RAG с reflection (5 спринтов)
