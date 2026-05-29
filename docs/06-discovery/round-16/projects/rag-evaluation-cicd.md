---
date: 2026-05-29
tags: [memory, rag, orchestration, security, ingestion]
state: normalized
---

# RAG Evaluation CI/CD — модульное тестирование RAG-пайплайнов

<!-- toc-auto -->
<!-- tags: rag-evaluation-cicd, docs -->


<!-- summary -->
> RAG Evaluation CI/CD — модульное тестирование RAG-пайплайнов — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** независимый исследователь (Хабр)  
**Хабр:** https://habr.com/ru/articles/865420/  
**GitHub:** RAGAS: github.com/explodinggradients/ragas (Apache 2.0); DeepEval: github.com/confident-ai/deepeval (Apache 2.0)  
**Слой:** quality / testing / orchestration  
**Дата:** 2025  
**Уникальность:** Единственная на Хабре статья, связывающая RAGAS-метрики с **CI/CD пайплайном**: RAG тест = обычный unit-тест, запускаемый на каждый PR. Превращает оценку качества RAG из разовой проверки в непрерывную систему контроля.

## Метрики RAGAS

| Метрика | Что измеряет | Идеал |
|---------|-------------|-------|
| **Faithfulness** | Соответствие ответа найденному контексту | 1.0 |
| **Answer Relevance** | Отвечает ли на конкретный вопрос | 1.0 |
| **Context Precision** | Релевантность найденных чанков | 1.0 |
| **Context Recall** | Покрытие всего нужного контекста | 1.0 |
| **Answer Correctness** | Фактическая точность (если есть ground truth) | 1.0 |

## Модульный подход (из статьи)

```python
# RAG-тест как unit-тест:
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy

def test_rag_pipeline_quality():
    result = evaluate(
        dataset=test_questions,
        metrics=[faithfulness, answer_relevancy],
    )
    assert result['faithfulness'] > 0.8,   "RAG hallucinations!"
    assert result['answer_relevancy'] > 0.7, "Irrelevant answers!"
```

## CI/CD интеграция

```yaml
# .github/workflows/rag-eval.yml
- name: Run RAG evaluation
  run: python -m pytest tests/test_rag_quality.py
  # Блокирует merge если качество RAG упало
```

## DeepEval — альтернатива RAGAS

| Аспект | RAGAS | DeepEval |
|--------|-------|---------|
| Метрик | 5 RAG-специфичных | 14+ (RAG + агенты + безопасность) |
| CI/CD | через pytest | нативная интеграция |
| Агенты | нет | да (tool use, reasoning) |
| Лицензия | Apache 2.0 | Apache 2.0 |

DeepEval умеет оценивать не только RAG, но и **агентные цепочки** (tool use correctness, hallucination в reasoning).

## Применение к Lorenzo

Lorenzo использует BM25 + TF-IDF поиск в `improve_semantic_search.py`.  
Сейчас: нет автоматической проверки качества поиска.  
С RAG Evaluation: **тест-набор вопросов → RAGAS оценивает → CI блокирует если ухудшилось**.

```bash
# Lorenzo test suite:
python -m pytest tests/test_search_quality.py  # RAGAS над BM25+TF-IDF
python -m pytest tests/test_llm_qa_quality.py  # DeepEval над improve_llm_qa.py
```

Комбинация с `improve_benchmark.py`: история качества поиска по времени.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **RAG Eval + improve_semantic_search** | Непрерывный мониторинг качества BM25+TF-IDF поиска Lorenzo |
| **RAG Eval + AI Review (R15)** | AI Review проверяет код → RAG Eval проверяет качество RAG в CI |
| **RAG Eval + Observability (R13)** | Langfuse трейсит + RAGAS оценивает = полная картина качества |
| **RAG Eval + DSPy (R14)** | DSPy оптимизирует промпты → RAGAS проверяет что качество выросло |

## Контакт

- Статья: https://habr.com/ru/articles/865420/
- RAGAS GitHub: https://github.com/explodinggradients/ragas (Apache 2.0)
- DeepEval GitHub: https://github.com/confident-ai/deepeval (Apache 2.0)
- pip install ragas deepeval

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
