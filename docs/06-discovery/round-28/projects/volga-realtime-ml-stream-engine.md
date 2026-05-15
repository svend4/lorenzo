# Volga: движок real-time обработки данных для AI/ML — аналог Spark/Flink на Rust

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** dirty_valera (Хабр, апрель 2025)  
**Хабр:** https://habr.com/ru/articles/1021290/  
**GitHub:** github.com/volga-project/volga (Apache 2.0)  
**Слой:** orchestration / analytics / ingestion  
**Дата:** апрель 2025  
**Уникальность:** Rust-движок распределённой потоковой обработки, специально спроектированный для ML feature computation в real-time. Apache Arrow (columnar in-memory) + DataFusion (SQL query planning). Три режима: streaming, batch, request. Point-in-time correct window aggregations — критично для consistent online/offline ML пайплайнов. StateDB через SlateDB. Альтернатива Spark/Flink с ML-first API.

## Проблема: Spark/Flink не созданы для ML пайплайнов

```
Apache Spark (batch):
  → Хорош для ETL, плох для real-time features
  → Нет point-in-time correctness из коробки
  → JVM overhead: memory и latency

Apache Flink (streaming):
  → Сложная операционная модель
  → Нет нативного ML API
  → Stateful операции: сложно правильно

Проблема feature store:
  Online  (production): фичи за последние N минут → нужно быстро
  Offline (training):   фичи за прошлый период → нужно корректно
  
  Point-in-time correctness:
  Если обучали на данных t=10:00, то фичи должны быть рассчитаны
  только по данным доступным в t=10:00 (никакого "утечки будущего")
  
  Spark/Flink: нужно самому реализовывать → ошибки → плохие модели
  Volga: встроено из коробки
```

## Архитектура Volga

```rust
// Три режима выполнения в одном API

// Режим 1: STREAMING — непрерывная обработка событий
let pipeline = Pipeline::new()
    .source(KafkaSource::new("user_events"))
    .map(|event| extract_features(event))
    .window(TumblingWindow::minutes(5))
    .aggregate(|w| FeatureVector {
        clicks_5m: w.count(),
        revenue_5m: w.sum("amount"),
        unique_users_5m: w.approx_distinct("user_id"),
    })
    .sink(FeatureStoreSink::new("user_features_online"));

// Режим 2: BATCH — обработка исторических данных
let batch_job = BatchJob::new()
    .source(ParquetSource::new("s3://data/events/"))
    .point_in_time_join(            // ← Ключевое: PIT-корректность
        right: ParquetSource::new("s3://data/labels/"),
        timestamp_col: "event_time"
    )
    .aggregate(same_feature_logic)  // Тот же код что в streaming!
    .sink(ParquetSink::new("s3://features/training/"));

// Режим 3: REQUEST — on-demand для inference
let feature_server = RequestServer::new()
    .serve(|user_id: UserId| -> FeatureVector {
        feature_store.get_latest(user_id)
    });

// Единый код для трёх режимов → нет training/serving skew
```

## Apache Arrow: почему Rust + columnar

```python
# Arrow в памяти: колоночное хранение для ML

# Обычный подход (row-based):
events = [
    {"user_id": 1, "amount": 100, "ts": 1000},
    {"user_id": 2, "amount": 200, "ts": 1001},
    # ...
]
# Чтобы посчитать sum(amount): обойти все строки → cache miss

# Arrow подход (columnar):
amounts = [100, 200, 300, ...]  # все amount в одном блоке памяти
user_ids = [1, 2, 3, ...]

# sum(amount): SIMD-операция над непрерывным массивом → быстро
# → 10-100× ускорение для агрегаций над миллионами событий

# DataFusion: SQL поверх Arrow
import datafusion
ctx = datafusion.SessionContext()
ctx.register_record_batches("events", arrow_batches)
result = ctx.sql("""
    SELECT user_id,
           COUNT(*) as clicks_5m,
           SUM(amount) as revenue_5m
    FROM events
    WHERE ts > now() - INTERVAL '5 minutes'
    GROUP BY user_id
""").collect()
# → Apache Arrow RecordBatch → прямо в numpy/pandas без copy
```

## Point-in-time Correct Window Aggregations

```python
# Критично для ML: не использовать данные "из будущего"

class PointInTimeFeatureStore:
    """
    Пример проблемы:
    - Событие: пользователь сделал покупку в t=10:00
    - Фича: "количество кликов за последний час"
    - Правильно: клики с 9:00 до 10:00
    - Неправильно: клики с 9:00 до 11:00 (утечка будущего!)
    
    Volga гарантирует корректность автоматически
    """

    def get_feature_at_timestamp(self,
                                  entity_id: str,
                                  feature_name: str,
                                  as_of: datetime) -> float:
        """
        Возвращает значение фичи как оно было известно в момент as_of
        Используется для: backfill обучающих данных без data leakage
        """
        return self.time_travel_query(
            entity=entity_id,
            feature=feature_name,
            timestamp=as_of  # строго < as_of
        )

# При обучении модели:
training_data = []
for event in labeled_events:
    features = feature_store.get_feature_at_timestamp(
        entity_id=event.user_id,
        feature_name="clicks_1h",
        as_of=event.timestamp  # только данные ДО этого события
    )
    training_data.append((features, event.label))

# → Нет утечки будущего → честная оценка модели → нет деградации в проде
```

## ML-специфичные агрегации

```python
# Volga добавляет агрегации которых нет в Spark/Flink

VOLGA_ML_AGGREGATIONS = {
    # Стандартные
    "count": "COUNT(*)",
    "sum": "SUM(col)",
    "mean": "AVG(col)",

    # ML-специфичные
    "top_k": """
        TOP(category_col, k=3)
        → ['electronics', 'clothing', 'books']
        Используется: top категории которые смотрел пользователь
    """,

    "categorical_distribution": """
        CATDIST(category_col)
        → {'electronics': 0.6, 'clothing': 0.3, 'books': 0.1}
        Используется: распределение действий для рекомендаций
    """,

    "time_weighted_avg": """
        TWAVE(value_col, decay=0.9)
        → Exponential decay: последние события важнее
        Используется: скользящее среднее с учётом давности
    """,

    "approx_distinct": """
        HLL(user_id_col)  # HyperLogLog
        → ~unique count, ±2% ошибка
        Используется: уникальные пользователи без GROUP BY
    """
}
```

## SlateDB: state management

```
Volga stateful операции → SlateDB (LSM-tree поверх S3/MinIO)

vs. Flink RocksDB (локальный state):
  ✅ State в объектном хранилище = нет привязки к серверу
  ✅ Instant restore после краша (читать из S3, не replay logs)
  ✅ Дешевле (S3 vs NVMe)
  ❌ Latency выше для мелких операций (сеть vs локальный диск)
  Компромисс: подходит для batch/near-realtime, не подходит для <1ms

Для Lorenzo: SlateDB = идеальный backend для долгосрочного state агентов
```

## Применение к Lorenzo

Volga паттерн → **Streaming индексация новых документов**:

```python
# improve_streaming_index.py (паттерн):
# Volga-style: события изменения файлов → real-time индекс

class LorenzoStreamProcessor:
    """
    Аналог Volga: file change events → feature extraction → index update
    """

    def __init__(self):
        self.window = TumblingWindow(minutes=5)

    def process_file_changes(self, events: Stream[FileChange]) -> None:
        events \
            .filter(lambda e: e.path.endswith(".md")) \
            .map(lambda e: self.extract_features(e)) \
            .window(self.window) \
            .aggregate(lambda w: IndexUpdate(
                new_docs=w.count(),
                modified_sections=w.collect("section"),
                top_topics=w.top_k("topic", k=5)
            )) \
            .sink(self.update_search_index)

    # Point-in-time: search_index.json знает состояние на момент запроса
    # → нет race condition между write и read
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Volga + AIOps (R24)** | Streaming метрики → Volga агрегирует фичи → AIOps IncidentPredictor |
| **Volga + AI Logistics (R26)** | Real-time фичи склада → ML прогноз спроса без batch ETL |
| **Volga + CAVM (R26)** | CAVM получает свежие фичи из Volga вместо snapshot-данных |
| **Volga + LLM Router (R20)** | Volga агрегирует нагрузку → роутинг к дешёвой/дорогой модели |
| **Volga + Sberbank RAG Test (R27)** | Streaming coverage metrics → авто-триггер генерации тестов |

## Контакт

- Статья: https://habr.com/ru/articles/1021290/ (апрель 2025)
- GitHub: github.com/volga-project/volga (Apache 2.0)
- Смежная (AIOps Sberbank R24): https://habr.com/ru/companies/sberbank/articles/1015336/
- Apache Arrow: arrow.apache.org
- Apache DataFusion: github.com/apache/datafusion
- SlateDB: github.com/slatedb/slatedb
