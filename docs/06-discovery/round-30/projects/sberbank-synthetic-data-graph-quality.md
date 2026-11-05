---
date: 2026-06-05
tags: [memory, rag, knowledge, architecture, anthropic]
state: normalized
---

# Генерация синтетических данных для LLM: граф-анализ качества вместо BLEU/ROUGE

<!-- toc-auto -->
<!-- tags: sberbank-synthetic-data-graph-quality, docs -->


<!-- summary -->
> Генерация синтетических данных для LLM: граф-анализ качества вместо BLEU/ROUGE — раздел документации проекта Lorenzo.
 
 
 
>   — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** SberTeam (Сбербанк, Хабр, апрель–май 2025)  
**Хабр:** https://habr.com/ru/companies/sberbank/articles/901222/ (ч.1), https://habr.com/ru/companies/sberbank/articles/909934/ (ч.2)  
**GitHub:** не опубликован (внутренние исследования Сбер)  
**Слой:** orchestration / analytics  
**Дата:** апрель–май 2025  
**Уникальность:** Две части: (1) 8 факторов качества синтетики для LLM + риски деградации при переиспользовании; (2) оригинальный метод оценки через граф-анализ — тексты → knowledge graphs → GCN/GAT/GraphSAGE → t-SNE визуализация. Гипотеза: каждый генератор оставляет "цифровой отпечаток" в топологии графа → детектировать синтетику и фильтровать дубли.

## Проблема: как измерить качество синтетических данных?

```
Классические метрики (BLEU/ROUGE):
  → Измеряют n-gram перекрытие
  → Не улавливают семантическое качество
  → Не обнаруживают "model collapse" (деградацию)
  → Не детектируют дубли и шаблонность

Реальные проблемы синтетики для LLM:
  ❌ Model Collapse: модель обучилась на синтетике → генерирует
     ещё более "синтетическую" синтетику → качество падает
  ❌ Distribution Shift: синтетика ≠ реальные данные пользователей
  ❌ Hidden Duplicates: тексты выглядят разными, но несут одну информацию
  ❌ Generator Fingerprint: GANs/VAEs/LLM оставляют паттерны
     → модель учится угадывать генератор, не задачу

Решение Сбер: граф-анализ структуры знаний
```

## Восемь факторов качества синтетики (Часть 1)

```python
SYNTHETIC_DATA_QUALITY_FACTORS = {
    "1_lexical_diversity": {
        "описание": "Разнообразие словарного запаса",
        "метрика": "TTR (Type-Token Ratio) > 0.6",
        "риск": "Модель выучивает шаблонные фразы, не смысл"
    },
    "2_syntactic_variation": {
        "описание": "Разнообразие синтаксических конструкций",
        "метрика": "Entropy синтаксических деревьев",
        "риск": "Одинаковая структура предложений → предсказуемость"
    },
    "3_semantic_coherence": {
        "описание": "Логическая связность внутри текста",
        "метрика": "Cosine similarity последовательных предложений (≥ 0.4)",
        "риск": "Бессвязные тексты → модель учится hallucinate"
    },
    "4_thematic_consistency": {
        "описание": "Текст об одной теме, без тематических скачков",
        "метрика": "LDA topic probability variance < 0.15",
        "риск": "Смешение тем → путаница в fine-tuning"
    },
    "5_controlled_noise": {
        "описание": "Реалистичные опечатки, разговорность (как в реальных данных)",
        "метрика": "Noise ratio 2-5% токенов",
        "риск": "Слишком чистая синтетика → gap с production данными"
    },
    "6_stylistic_diversification": {
        "описание": "Разные стили (формальный, разговорный, технический)",
        "метрика": "Silhouette score по стилевым кластерам > 0.3",
        "риск": "Один стиль → модель ломается на разговорном вводе"
    },
    "7_factual_grounding": {
        "описание": "Факты в синтетике соответствуют реальности",
        "метрика": "Entity linking recall ≥ 0.80",
        "риск": "Hallucinated facts в обучающих данных → hallucinated model"
    },
    "8_coverage_balance": {
        "описание": "Равномерное покрытие всех поддоменов задачи",
        "метрика": "KL-divergence между синтетикой и целевым распределением",
        "риск": "Переобученность на популярных случаях"
    }
}
```

## Граф-анализ качества (Часть 2): "цифровой отпечаток" генератора

```python
# Ключевая идея: тексты → knowledge graphs → GNN эмбеддинги → кластеры

class SyntheticDataGraphAnalyzer:
    """
    Вместо: сравнивать тексты напрямую (BLEU)
    Подход: сравнивать СТРУКТУРЫ ЗНАНИЙ через графы
    """

    def text_to_knowledge_graph(self, text: str) -> nx.DiGraph:
        """
        Шаг 1: Извлечь entities и relations из текста
        """
        # NER: извлечь сущности
        entities = self.ner.extract(text)
        # RE: извлечь отношения между сущностями
        relations = self.re_extractor.extract(text, entities)

        G = nx.DiGraph()
        for entity in entities:
            G.add_node(entity.text, type=entity.type, embedding=entity.embedding)
        for relation in relations:
            G.add_edge(relation.head, relation.tail,
                       type=relation.type, weight=relation.confidence)
        return G

    def extract_graph_embedding(self, G: nx.DiGraph) -> np.ndarray:
        """
        Шаг 2: GNN извлекает эмбеддинг графа (не текста!)
        """
        # Конвертировать в формат для GNN
        data = nx_to_torch_geometric(G)

        # GraphSAGE: хорош для inductive learning на новых графах
        embedding = self.graphsage(data.x, data.edge_index)
        # → Вектор 256-dim, описывающий СТРУКТУРУ знаний, не слова

        return embedding.mean(dim=0).detach().numpy()  # graph-level pooling

    def detect_generator_fingerprint(self,
                                      texts: list[str],
                                      source: str) -> FingerprintReport:
        """
        Шаг 3: t-SNE визуализация показывает кластеры по генератору
        """
        embeddings = [self.extract_graph_embedding(
            self.text_to_knowledge_graph(t)
        ) for t in texts]

        # t-SNE: уменьшить размерность до 2D
        coords_2d = TSNE(n_components=2, random_state=42).fit_transform(
            np.array(embeddings)
        )

        # Если тексты из одного генератора → кластеризуются вместе
        # "Цифровой отпечаток" = характерная область в пространстве
        return FingerprintReport(
            source=source,
            cluster_coords=coords_2d,
            silhouette_score=silhouette_score(coords_2d, [source] * len(texts))
        )
```

## Применение: фильтрация синтетики и детекция model collapse

```python
class SyntheticDataPipeline:
    """
    Production pipeline: генерация + оценка + фильтрация
    """

    def generate_and_filter(self,
                             n_samples: int,
                             target_distribution: np.ndarray) -> Dataset:
        # Шаг 1: Генерировать много синтетики
        raw_samples = self.generator.generate(n_samples * 2)  # 2× запас

        # Шаг 2: Граф-оценка каждого сэмпла
        scored_samples = []
        for sample in raw_samples:
            graph = self.analyzer.text_to_knowledge_graph(sample.text)
            embedding = self.analyzer.extract_graph_embedding(graph)

            quality_scores = {
                "lexical_diversity": self.measure_ttr(sample.text),
                "semantic_coherence": self.measure_coherence(sample.text),
                "graph_novelty": self.measure_novelty(embedding, scored_samples),
                "factual_grounding": self.measure_entity_linking(sample.text)
            }
            sample.quality_score = np.mean(list(quality_scores.values()))
            scored_samples.append(sample)

        # Шаг 3: Фильтрация (убрать низкое качество и дубли)
        filtered = [s for s in scored_samples if s.quality_score > 0.75]

        # Шаг 4: Проверка distribution shift
        dataset_embedding = np.mean([
            self.analyzer.extract_graph_embedding(
                self.analyzer.text_to_knowledge_graph(s.text)
            ) for s in filtered
        ], axis=0)

        kl_div = kl_divergence(dataset_embedding, target_distribution)
        if kl_div > 0.3:
            print(f"WARNING: Distribution shift detected (KL={kl_div:.3f})")

        return Dataset(filtered[:n_samples])

    def detect_model_collapse(self, generation_history: list[Dataset]) -> bool:
        """
        Model collapse: граф-эмбеддинги генераций сходятся к одной точке
        (разнообразие тем/структур падает)
        """
        embeddings_per_gen = [
            np.mean([self.analyzer.extract_graph_embedding(
                self.analyzer.text_to_knowledge_graph(s.text)
            ) for s in dataset], axis=0)
            for dataset in generation_history
        ]

        # Если дисперсия эмбеддингов падает → collapse
        variance = np.var(embeddings_per_gen, axis=0).mean()
        return variance < 0.01  # порог
```

## Применение к Lorenzo

Lorenzo мог бы генерировать синтетические Q&A пары для fine-tuning:

```python
# improve_synthetic_qa.py (паттерн):

class LorenzoSyntheticQAGenerator:
    """
    Генерирует синтетические Q&A для обучения поиска по базе знаний
    + Граф-оценка качества (Сбер паттерн)
    """

    def generate_qa_pairs(self, doc: str, n: int = 10) -> list[QAPair]:
        raw_qa = self.llm.generate_qa(doc, n=n * 2)  # 2× запас

        # Оценка качества
        scored = []
        for qa in raw_qa:
            score = {
                "relevance": self.measure_answer_relevance(qa, doc),
                "specificity": self.measure_question_specificity(qa.question),
                "graph_novelty": self.measure_graph_novelty(qa)
            }
            qa.score = np.mean(list(score.values()))
            scored.append(qa)

        # Вернуть топ-N
        return sorted(scored, key=lambda x: x.score, reverse=True)[:n]
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Synthetic Data + Fine-tuning (R24)** | Граф-оценка качества синтетики ПЕРЕД дистилляцией → меньше catastrophic forgetting |
| **Synthetic Data + RAG eval (R16)** | Синтетические Q&A → автобенчмарк для RAG пайплайна |
| **Synthetic Data + LLM Judge (R28)** | LLM Judge оценивает синтетику (factual grounding) |
| **Synthetic Data + Graph RAG (R22)** | Knowledge graphs синтетики → обогащение GraphRAG |
| **Synthetic Data + AI Science (R25)** | Синтетика для научных данных: digital twins → обучение |

## Контакт

- Статья (ч.1): https://habr.com/ru/companies/sberbank/articles/901222/ (апрель 2025)
- Статья (ч.2): https://habr.com/ru/companies/sberbank/articles/909934/ (май 2025)
- Смежная (dataset distillation pipeline R24): https://habr.com/ru/articles/1033434/
- Смежная (open-source синтетика обзор): https://habr.com/ru/companies/mws/articles/932066/
- GraphSAGE: github.com/williamleif/GraphSAGE
- Synthetic Data Vault: github.com/sdv-dev/SDV (MIT)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
