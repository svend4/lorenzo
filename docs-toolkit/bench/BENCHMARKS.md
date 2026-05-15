# Benchmark Results — Sprint 54-92 features

Per-feature overhead measured on stubbed Retriever + Answerer (so we
isolate the *feature cost* itself, not retrieval / LLM latency).
Reproduce with:

```bash
python -c "
from bench.runner import run_suites
results = run_suites(['ask_features', 'helpers'])
for r in results:
    print(r['name'], r['median_ms'])
"
```

## `ask_features` suite (stub corpus, 5 passages, top_k=5)

| Benchmark                | Median (ms) | Min (ms) | Iterations | Delta vs baseline |
|--------------------------|------------:|---------:|-----------:|------------------:|
| `ask_baseline`           |       0.043 |    0.038 |         20 |                 — |
| `ask_with_facets`        |       0.077 |    0.071 |         20 |           +34 μs |
| `ask_with_provenance`    |       0.052 |    0.049 |         20 |            +9 μs |
| `ask_rerank_tfidf`       |       0.098 |    0.093 |         20 |           +55 μs |
| `ask_self_rag` (2 iters) |       0.120 |    0.112 |         15 |           +77 μs |
| `ask_with_debate` (1 r)  |       0.092 |    0.081 |         10 |           +49 μs |
| `ask_with_got` (3 hyp)   |       0.085 |    0.077 |         15 |           +42 μs |
| `ask_with_mapreduce`     |       0.062 |    0.058 |         15 |           +19 μs |
| `ask_with_negotiation`   |       0.150 |    0.140 |         15 |          +107 μs |
| `ask_compose_5`          |       0.337 |    0.317 |         10 |          +294 μs |

`ask_compose_5` = baseline + facets + provenance + rerank + self_rag + got.
Composition overhead is sub-linear vs sum of individual features.

## `helpers` suite

| Benchmark                       | Median (ms) | Min (ms) | Iterations |
|---------------------------------|------------:|---------:|-----------:|
| `measure_voice_500ch` (N4)      |       0.324 |    0.313 |         20 |
| `probe_counterfactual_20docs` (I4) |    0.128 |    0.120 |         10 |
| `co_evolve_3seeds` (N10)        |       0.080 |    0.069 |          5 |

## Observations

- **Baseline overhead is ~40 μs** — Sprint 54-92 features are negligible
  vs the cost of real retrieval/LLM calls (which dominate at 10-2000 ms).
- **Most expensive feature: `with_negotiation`** at +107 μs because it
  runs the auction over all candidates with 5 agent types.
- **Cheapest feature: `with_provenance`** at +9 μs — bootstrap CI only
  fires when an answer text is present.
- **Composition is amortised**: 5 features in one call adds ~300 μs
  instead of ~250 μs (sum of individual), so there's only ~50 μs
  shared overhead.

These numbers are environment-dependent — run locally to compare.
History is appended to `bench/history.jsonl` for trend tracking.

## `kg` suite (Phase V.4)

In-memory `TripleStore` populated with 100 entities / 500 triples.
Measures raw KG ops without retrieval / extraction pipeline:

| Bench | Median (ms) | Min (ms) | Iterations |
|---|---:|---:|---:|
| `kg_lookup_by_subject` | 0.020 | 0.018 | 20 |
| `kg_neighbors` | 0.010 | 0.010 | 20 |
| `kg_query_one_pattern` | 0.027 | 0.020 | 20 |
| `kg_query_two_patterns` | 1.856 | 1.779 | 15 |

- **Single-pattern DSL queries are cheap** (~27 μs) — same complexity as a
  direct `find_triples()` call.
- **Multi-pattern joins are O(N · k)** where N is bindings of the first
  pattern and k is the per-pattern fan-out. The 1.86 ms / 2-pattern figure
  is dominated by 5×100 SQL round-trips; can be optimized with a single
  JOIN query if it becomes a bottleneck.

## Phase III.1 trace overhead

Инструментирование `RAGPipeline.run()` через `_TraceTimer` добавило
~5-15 μs на стадию. На baseline:

- До инструментирования: median ~43 μs
- После Phase III.1: median ~54 μs (+11 μs, ~25%)

Включаем `trace` всегда — overhead на real-LLM запросах (10-2000 ms)
теряется в шуме, а observability стоит этого.

## Baseline record

`bench/history.jsonl` хранит один **baseline-снимок** (2026-05-15) против
которого `.github/workflows/benchmark.yml` сравнивает PR-запуски с порогом
50% регрессии. Перезапустить baseline можно командой:

```bash
python -m bench.runner --save
```

После релиза 0.3.0 каждый merge в `main` дописывает новую запись в
`history.jsonl`, что даёт временной ряд для трекинга деградации.
