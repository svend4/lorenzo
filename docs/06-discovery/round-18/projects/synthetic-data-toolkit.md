# Synthetic Data Toolkit — подборка OSS-инструментов генерации синтетических данных

**Автор:** команда MWS (Mail.ru / VK Cloud)  
**Хабр:** https://habr.com/ru/companies/mws/articles/932066/  
**GitHub:** https://github.com/datadreamer-dev/DataDreamer (Apache 2.0, U Penn + U Toronto)  
**Слой:** ingestion / knowledge / memory  
**Дата:** 2025  
**Уникальность:** Первый русскоязычный систематический обзор OSS-инструментов для генерации синтетических данных под fine-tuning LLM. Три ключевых инструмента разного уровня: DataDreamer (академический, полный pipeline), Distilabel (production-ready, Argilla), Bespoke Curator (минималистичный, 2025). Прямой путь: готовый корпус → синтетика → fine-tuning по паттерну из R15.

## Три инструмента

### DataDreamer (U Penn + U Toronto, Apache 2.0)

```python
from datadreamer import DataDreamer
from datadreamer.steps import HFGenerateSentenceSimilarity, DataSource

with DataDreamer("./output"):
    # Загрузить датасет
    dataset = DataSource("Dataset", data={"texts": my_texts})
    
    # Генерировать пары вопрос-ответ из текстов
    qa_pairs = dataset.map(
        lambda row: llm.generate(f"Generate Q&A from: {row['texts']}")
    )
    
    # Сохранить + воспроизводимость через кэш
    qa_pairs.save("synthetic_qa")
```

**Особенности:**
- Полный pipeline: датасет → синтетика → fine-tuning → публикация HuggingFace
- Воспроизводимость через кэш (детерминированный pipeline)
- Встроенные watermarking и citation для академических требований

### Distilabel (Argilla, Apache 2.0)

```python
from distilabel.pipeline import Pipeline
from distilabel.steps import LoadDataFromHub
from distilabel.steps.tasks import TextGeneration

pipeline = Pipeline(name="synthetic-qa")

load = LoadDataFromHub(repo_id="my-dataset")
generate = TextGeneration(
    llm=InferenceEndpointsLLM(model_id="meta-llama/Meta-Llama-3.1-8B-Instruct"),
    system_prompt="Generate diverse Q&A pairs..."
)

pipeline.run()
```

**Особенности:**
- Production-grade (Argilla — компания с реальными enterprise-клиентами)
- Поддержка Llama, Mistral, OpenAI, локальные модели через vLLM
- Встроенный Quality Filter: удаляет плохие примеры автоматически

### Bespoke Curator (Apache 2.0, январь 2025)

```python
from bespokelabs import curator

# Минималистичный API — 10 строк до синтетики
prompter = curator.Prompter(
    prompt_func=lambda row: f"Generate instruction for: {row['topic']}",
    model_name="gpt-4o-mini",
    response_format=SyntheticInstruction
)

dataset = prompter(topics_df)
dataset.to_pandas()  # HuggingFace Dataset → pandas
```

**Особенности:**
- Самый простой API (2025, новейший)
- Встроенное кэширование + структурированный вывод через Pydantic
- Оптимизирован для instruction tuning datasets

## Сравнение

| Инструмент | Простота | Функции | Воспроиз-ть | Когда |
|-----------|----------|---------|-------------|-------|
| DataDreamer | сложный | максимум | отличная | академия, полный pipeline |
| Distilabel | средний | production | хорошая | enterprise, масштаб |
| Bespoke Curator | простой | базовые | хорошая | быстрый старт |

## Паттерн: Синтетика для Lorenzo

```
Корпус Lorenzo (2483 карточки)
        ↓
Distilabel / DataDreamer
  → generate_qa(card.body) → {question, answer, context}
  → generate_instructions(card.summary) → {instruction, response}
        ↓
QLoRA fine-tuning (паттерн из R15: Unsloth + Qwen 2.5 7B)
        ↓
Специализированная модель для `improve_llm_qa.py`
  — знает Lorenzo corpus, отвечает без RAG (дешевле)
```

## Применение к Lorenzo

Lorenzo имеет 2483 карточки с `body` (800 слов) и `summary` (300 символов).  
Это **готовый корпус** для синтетики:
- Distilabel генерирует Q&A пары из каждой карточки
- DataDreamer обеспечивает воспроизводимость (важно для исследования)
- Bespoke Curator — быстрый эксперимент за день

Связь с R15 (Fine-tuning): синтетика → Unsloth + QLoRA → специализированная модель.

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Distilabel + Lorenzo corpus** | Автоматическая генерация Q&A из 2483 карточек |
| **DataDreamer + Fine-tuning (R15)** | Воспроизводимый pipeline: корпус → синтетика → модель |
| **Synthetic data + RAG Eval (R16)** | Синтетика → RAGAS бенчмарк → оценка до деплоя |
| **Distilabel + GigaAM (R16)** | Синтетические диалоги для RU speech recognition |
| **DataDreamer + CoT Illusion (R17)** | Генерировать примеры без CoT (паттерн R17) |

## Контакт

- Статья MWS: https://habr.com/ru/companies/mws/articles/932066/
- DataDreamer GitHub: https://github.com/datadreamer-dev/DataDreamer (Apache 2.0)
- Distilabel GitHub: https://github.com/argilla-io/distilabel (Apache 2.0)
- Bespoke Curator: https://github.com/bespokelabsai/curator (Apache 2.0)
- DataDreamer paper: arxiv.org/abs/2402.10379
