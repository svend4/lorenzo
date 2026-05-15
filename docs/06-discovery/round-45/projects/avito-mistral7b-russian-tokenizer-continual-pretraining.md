# Авито: адаптация Mistral-7B к русскому языку — новый токенизатор + continual pretraining

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Anastasiya_Rysmyatova (Авито, команда LLM)  
**Хабр:** https://habr.com/ru/companies/avito/articles/852958/  
**GitHub:** нет (внутренняя система Авито)  
**Слой:** analytics  
**Дата:** октябрь 2024  
**Уникальность:** Полный end-to-end pipeline русификации Mistral-7B-v0.1: замена токенизатора с нуля (chars/token 2.1→3.3, +57% токен-эффективность для русского) + continual pretraining на 1.1 TB дедуплицированных русских текстов (72× A100, 15 дней/эпоха) + SFT для e-commerce задач Авито (модерация, поиск, описания, извлечение параметров). Единственная русскоязычная статья с детальным описанием инициализации embedding-слоя при замене токенизатора.

## Проблема: Mistral-7B плохо говорит по-русски

```
Mistral-7B-v0.1 проблемы с русским языком:
  → Токенизатор обучен на английском
  → Русское слово → много токенов (chars/token = 2.1 vs 4.0 для EN)
  → "Привет" → ["▁П", "ри", "вет"] вместо одного токена
  → Инференс в 1.5-2x медленнее для русского текста
  → Русские знания "размыты" по редким токенам

Следствия для бизнеса (Авито):
  → Модерация объявлений: хуже понимает RU нарушения
  → Поиск: хуже матчинг RU запросов с RU объявлениями
  → Генерация описаний: "угловатый" русский стиль
  → Стоимость: больше токенов = дороже API + медленнее

Решение: полная русификация базовой модели
  → Новый токенизатор (оптимизирован для русского)
  → Continual pretraining на русском корпусе
  → SFT на Авито-специфичных задачах
```

## Замена токенизатора: ключевая техническая деталь

```python
# Авито: адаптация Mistral-7B к русскому языку
# habr.com/ru/companies/avito/articles/852958

from transformers import AutoTokenizer, AutoModelForCausalLM
from sentencepiece import SentencePieceTrainer
import torch

class RussianTokenizerReplacement:
    """
    Замена токенизатора Mistral-7B: главный архитектурный вызов.

    Проблема: новый токенизатор → новые токен-ID → сломанные embedding-веса.
    Решение Авито: инициализация embedding новых токенов через
    усреднение embeddings их подтокенов в старом токенизаторе.
    """

    def train_russian_tokenizer(self,
                                 corpus_path: str,
                                 vocab_size: int = 32000) -> None:
        """
        Обучить новый SentencePiece токенизатор на русском корпусе.
        Цель: chars/token 2.1 (Mistral) → 3.3 (русский оптимум).
        """
        SentencePieceTrainer.train(
            input=corpus_path,
            model_prefix="ru_tokenizer",
            vocab_size=vocab_size,
            character_coverage=0.9999,   # для кириллицы — почти 100%
            model_type="bpe",
            pad_id=0, bos_id=1, eos_id=2, unk_id=3,
            byte_fallback=True           # для редких Unicode символов
        )

    def initialize_new_embeddings(self,
                                   old_model,
                                   old_tokenizer,
                                   new_tokenizer) -> torch.nn.Module:
        """
        Ключевая инновация: инициализация embeddings для новых токенов.

        Алгоритм:
        1. Для каждого нового токена (из нового токенизатора):
           а. Токенизировать его текст СТАРЫМ токенизатором
           б. Получить embeddings подтокенов из старой модели
           в. Усреднить → начальный embedding нового токена

        Почему это важно:
        → Случайная инициализация → долгое обучение (embeddings с нуля)
        → Усреднение → семантически близкие начальные веса
        → В ~100GB обучения можно заморозить embeddings (стабильность)
        """
        old_embeddings = old_model.get_input_embeddings()
        new_vocab_size = len(new_tokenizer)
        embedding_dim = old_embeddings.weight.shape[1]

        new_embedding = torch.nn.Embedding(new_vocab_size, embedding_dim)

        for new_token_id in range(new_vocab_size):
            new_token_text = new_tokenizer.convert_ids_to_tokens([new_token_id])[0]

            # Токенизировать новый токен старым токенизатором
            old_token_ids = old_tokenizer.encode(
                new_token_text.replace("▁", " "),  # убрать SentencePiece пробел
                add_special_tokens=False
            )

            if old_token_ids:
                # Усреднить embeddings подтокенов
                old_embeds = old_embeddings.weight[old_token_ids]
                new_embedding.weight.data[new_token_id] = old_embeds.mean(dim=0)
            else:
                # Fallback: случайная инициализация для неизвестных токенов
                torch.nn.init.normal_(
                    new_embedding.weight.data[new_token_id:new_token_id+1]
                )

        return new_embedding


TOKENIZER_COMPARISON = {
    "метрика": "chars/token (больше = лучше для данного языка)",
    "baseline_mistral_ru": 2.1,   # Mistral на русском тексте
    "avito_new_ru": 3.3,          # новый токенизатор
    "improvement": "+57% токен-эффективность",
    "следствие": "~1.5x быстрее инференс для русского текста",
    "baseline_en": 4.0            # английский в Mistral-7B (референс)
}
```

## Continual Pretraining: 1.1 TB русского корпуса

```python
class ContinualPretrainingPipeline:
    """
    Continual pretraining Mistral-7B на русском корпусе.
    Ключевые решения: заморозка, шедулинг, mix с английским.
    """

    CORPUS_COMPOSITION = {
        "total_size": "1.1 TB дедуплицированных русских текстов",
        "sources": [
            "Открытые русскоязычные корпуса (CommonCrawl RU, Wikipedia RU)",
            "Публичные веб-данные (новости, форумы, блоги)",
            "Авито-специфичные данные (объявления, описания)"
        ],
        "deduplication": "MinHash LSH + точная дедупликация URL"
    }

    TRAINING_STAGES = [
        {
            "stage": 1,
            "description": "Embeddings заморожены — только обучаем трансформер",
            "data_volume": "~100 GB",
            "reason": (
                "Стабилизировать обучение. Новые embeddings нестабильны "
                "в первые шаги — заморозка даёт трансформеру привыкнуть."
            )
        },
        {
            "stage": 2,
            "description": "Все параметры разморожены — полное обучение",
            "data_volume": "1.0 TB",
            "reason": "Финальная адаптация embeddings к новому токенизатору"
        }
    ]

    TRAINING_CONFIG = {
        "hardware": "72 × NVIDIA A100 80GB",
        "training_time": "~15 дней на эпоху",
        "framework": "Megatron-LM + DeepSpeed",
        "precision": "bf16",
        "context_length": 4096,
        "batch_size": "глобальный 2048",
        "lr": 1e-4,
        "warmup": "1000 шагов",
        "en_ru_mix": "10% английских данных для сохранения EN знаний"
    }

    STABILITY_TRICKS = {
        "loss_spike_handling": (
            "При loss spike → откат к последнему чекпоинту. "
            "За 15 дней обучения 3-4 спайка — ожидаемо."
        ),
        "gpu_failure": (
            "Из 72 GPU за эпоху выходит 1-2 GPU. "
            "Elastic training: перераспределение без остановки."
        ),
        "gradient_clipping": "max_norm=1.0 — обязательно для стабильности"
    }
```

## SFT для задач Авито

```python
class AvitoSFTPipeline:
    """
    Supervised Fine-Tuning на задачах Авито.
    Базовая модель после CPT → специализация под e-commerce.
    """

    AVITO_TASKS = {
        "moderation": {
            "description": "Обнаружение нарушений в объявлениях",
            "input": "Текст объявления + категория",
            "output": "Класс нарушения (мошенничество/запрещённый товар/спам/OK)",
            "metric": "F1 на тест-сете нарушений"
        },

        "moderation_review": {
            "description": "Объяснение решения о нарушении пользователю",
            "input": "Текст объявления + тип нарушения",
            "output": "Понятное объяснение + инструкция по исправлению"
        },

        "search_relevance": {
            "description": "Матчинг поискового запроса с объявлением",
            "input": "Запрос пользователя + заголовок объявления",
            "output": "Скор релевантности 0-1",
            "metric": "NDCG@10"
        },

        "parameter_extraction": {
            "description": "Извлечение структурированных данных из описания",
            "input": "Текст объявления (например, квартиры)",
            "output": "JSON: {площадь, этаж, комнаты, год_постройки, ...}",
            "metric": "F1 на JSON-полях"
        }
    }

    def prepare_sft_data(self, task: str,
                          raw_examples: list[dict]) -> list[dict]:
        """
        Подготовка SFT данных в формат Mistral instruction tuning.
        [INST] запрос [/INST] ответ
        """
        formatted = []
        for ex in raw_examples:
            instruction = self._build_instruction(task, ex)
            response = ex["expected_output"]
            formatted.append({
                "text": f"[INST] {instruction} [/INST] {response}"
            })
        return formatted


BENCHMARK_RESULTS = {
    "оценка": "Внутренний тест-сет Авито для каждой задачи",
    "baseline": "Mistral-7B-v0.1 без адаптации",

    "улучшения": {
        "moderation_F1": "+15-20 pp vs baseline (специализированная терминология)",
        "search_NDCG": "+8-12 pp (лучше понимает RU запросы и объявления)",
        "tokenizer_speed": "1.5x быстрее инференс для русского текста",
        "chars_per_token": "2.1 → 3.3 (+57% эффективность)"
    },

    "MMLU_RU": "Улучшение на русскоязычном MMLU после CPT"
}
```

## Ключевые инженерные уроки

```python
ENGINEERING_LESSONS = {
    "embedding_инициализация": (
        "Не инициализируй embeddings случайно при замене токенизатора. "
        "Усреднение старых embeddings → 2-3x быстрее сходимость."
    ),

    "заморозка_в_начале": (
        "Первые ~100GB: заморозь embeddings. "
        "Трансформер адаптируется → потом размораживай."
    ),

    "смешивание_языков": (
        "10% английского в corpus предотвращает catastrophic forgetting. "
        "Без EN-данных модель 'забывает' английский за 2-3 эпохи."
    ),

    "lora_недостаточно": (
        "LoRA не решает проблему токенизатора. "
        "Если базовый токенизатор плохой → нужен полный CPT."
    ),

    "дедупликация_критична": (
        "Без дедупликации модель переобучается на популярных текстах. "
        "MinHash LSH для 1TB+ — единственный практичный вариант."
    )
}
```

## Применение к Lorenzo

```python
# Lorenzo: Avito-паттерн для улучшения базовых моделей в пайплайне

class LorenzoModelAdaptationPipeline:
    """
    Авито паттерн для Lorenzo:
    Если базовая embedding-модель (multilingual-e5) плохо работает на docs/ →
    применить CPT-паттерн на корпусе Svyazi.
    Более легко: LoRA (R44 PGK-паттерн); тяжелее: полный CPT (Авито-паттерн).
    """

    def decide_adaptation_depth(self,
                                  baseline_recall: float) -> str:
        """
        Выбор глубины адаптации по baseline метрике.
        Recall@5 < 60%: полный CPT + новый токенизатор
        Recall@5 60-70%: LoRA fine-tuning (PGK паттерн)
        Recall@5 > 70%: prompt engineering достаточно
        """
        if baseline_recall < 0.60:
            return "full_cpt"       # Авито паттерн
        elif baseline_recall < 0.70:
            return "lora"           # PGK паттерн (R44)
        else:
            return "prompt_only"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Avito CPT + LoRA Embeddings (R44)** | CPT создаёт русскую базу → LoRA адаптирует к домену = двухуровневая адаптация |
| **Avito CPT + T-Bank T-Lite (R42)** | Сравнение подходов: replay-based (T-Bank) vs полная замена токенизатора (Авито) |
| **Avito CPT + MWS Vision Bench (R45)** | Русифицированный VLM → тест на русских бизнес-документах |
| **Avito CPT + Synthetic Data (R39)** | Синтетические RU диалоги для SFT вместо реальных пользовательских данных |
| **Avito CPT + Privacy Gateway (R41)** | CPT на локальных данных → On-Device инференс без отправки в облако |

## Контакт

- Статья: https://habr.com/ru/companies/avito/articles/852958/ (октябрь 2024)
- Автор: Anastasiya_Rysmyatova (Авито, LLM-команда)
- Base model: Mistral-7B-v0.1 (mistral.ai)
- Смежная (T-Bank T-Lite/T-Pro RU LLM, R42): docs/06-discovery/round-42/projects/tbank-tlite-tpro-russian-llm-training.md
- Смежная (Кириллица в LLM, R29): docs/06-discovery/round-29/
- Смежная (LoRA fine-tuning эмбеддингов PGK, R44): docs/06-discovery/round-44/projects/pgk-lora-embedding-finetuning-legal-hardneg.md
