---
date: 2026-05-15
tags: [memory, rag, orchestration, ingestion, local-first]
state: normalized
---

# Мультимодальные LLM: зачем бизнесу модели которые видят, слышат и понимают

<!-- toc-auto -->
<!-- tags: multimodal-llm-vision-audio-text, docs -->


<!-- summary -->
> Автор: Александр Капитанов (руководитель ML-команд Сбер AI), интервью Highload++, июнь 2025  
Хабр: https://habr.com/ru/companies/oleg-bunin/articles/914848/  
GitHub: не применимо (production архитектура Сбер)  
Слой: orchestration / ingestion / ana


> [!NOTE]
> Документ создан на основе исследования. Ссылки ведут на связанные материалы.

<!-- alert-added -->

**Автор:** Александр Капитанов (руководитель ML-команд Сбер AI), интервью Highload++, июнь 2025  
**Хабр:** https://habr.com/ru/companies/oleg-bunin/articles/914848/  
**GitHub:** не применимо (production архитектура Сбер)  
**Слой:** orchestration / ingestion / analytics  
**Дата:** июнь 2025  
**Уникальность:** Глубокое production-интервью: три модальности (текст + изображения/видео + аудио/речь) в единой системе. Реальные кейсы Сбер: документооборот (OCR+текст), реклама (изображение+текст), медицина (PACS+аудио консультации+клинические записи). AGE-VLM alternating attention для снижения галлюцинаций. Практическое масштабирование на GPU.

## Три модальности: не три модели, а одна система

```
Наивный подход (pipeline):
  Изображение → OCR → текст → LLM → ответ
  Аудио → ASR → текст → LLM → ответ
  
  Проблемы:
  ❌ Потеря контекста при транскрипции
  ❌ OCR ошибки накапливаются
  ❌ Три вызова → 3× задержка и стоимость

Мультимодальный подход (Сбер):
  [Изображение + Аудио + Текст] → Единая мультимодальная модель → Ответ
  
  Преимущества:
  ✅ Модель "видит" документ, а не текст из OCR
  ✅ Интонация из аудио влияет на интерпретацию
  ✅ Один вызов — меньше задержки
```

## Архитектура: как соединить модальности

```python
# Cross-attention fusion: стандарт для image+text

class VisionLanguageModel:
    """
    Текст → Token embeddings (как обычно)
    Изображение → Visual encoder (ViT/CLIP) → patch embeddings
    Слияние: cross-attention между текстовыми и visual токенами
    """

    def __init__(self):
        self.text_encoder = LanguageModel()          # LLM backbone
        self.vision_encoder = ViTEncoder()            # Vision Transformer
        self.audio_encoder = WhisperEncoder()         # аудио токенизация
        self.fusion = CrossAttentionFusion()          # слияние

    def forward(self, text: str, image: Image = None,
                audio: Audio = None) -> str:
        # Текстовые токены
        text_embeds = self.text_encoder.embed(text)

        # Визуальные токены (если есть изображение)
        if image is not None:
            visual_embeds = self.vision_encoder(image)
            # → N патчей 16×16 → каждый = один "токен"
            text_embeds = self.fusion.cross_attend(
                query=text_embeds,
                key_value=visual_embeds
            )

        # Аудио токены (если есть звук)
        if audio is not None:
            audio_embeds = self.audio_encoder(audio)
            # Whisper-style: mel-spectrogram → embeddings
            # Не транскрипт — сырые акустические признаки
            text_embeds = self.fusion.cross_attend(
                query=text_embeds,
                key_value=audio_embeds
            )

        return self.text_encoder.generate(text_embeds)
```

## AGE-VLM: alternating attention против галлюцинаций

```python
# Проблема: стандартный cross-attention → модель игнорирует изображение
# при длинном тексте (text tokens доминируют)

# AGE-VLM (Alternating Group Experts):
# Слои чередуются: нечётные → только text, чётные → text+visual

class AGEVisionLanguageModel:
    def __init__(self, n_layers: int = 32):
        self.layers = []
        for i in range(n_layers):
            if i % 2 == 0:
                # Чётные слои: full multimodal attention
                self.layers.append(MultimodalAttentionLayer())
            else:
                # Нечётные: только text self-attention
                self.layers.append(TextOnlyAttentionLayer())

    # Эффект:
    # → Модель не может "забыть" изображение к концу forward pass
    # → Визуальные признаки "освежаются" каждые 2 слоя
    # → Галлюцинации снижаются на 23% (внутренний бенчмарк Сбер)
```

## Production кейсы Сбер

```python
# Кейс 1: Документооборот (текст + сканы)

class DocumentAnalysisPipeline:
    """
    Вместо: scan → OCR (ошибки) → text → LLM
    Теперь:  scan image + text query → VLM
    """
    def analyze_contract(self, scan: Image, question: str) -> str:
        # Модель видит документ как изображение
        # → понимает таблицы, рукописные подписи, печати
        # → OCR ошибки не накапливаются
        return self.vlm.generate(
            text=f"Ответь на вопрос по договору: {question}",
            image=scan
        )
        # Точность: +18% vs OCR+LLM пайплайн на рукописных документах


# Кейс 2: Медицина (PACS + аудио + текст)

class MedicalAssistant:
    """
    Входные данные врача:
      - DICOM снимок (PACS)
      - Аудиозапись консультации
      - Текстовые заметки из ЭМК
    """
    def generate_summary(self, scan: Image, audio: Audio,
                         notes: str) -> MedicalSummary:
        prompt = """
        На основе снимка, аудиозаписи консультации и заметок из ЭМК:
        1. Опиши патологии на снимке
        2. Сопоставь с жалобами пациента из аудио
        3. Выдели противоречия между жалобами и снимком
        """
        return self.vlm.generate(
            text=prompt + notes,
            image=scan,
            audio=audio
        )
        # Ключевое: интонация пациента ("боль сильная" vs "терпимая")
        # влияет на итоговую интерпретацию вместе со снимком


# Кейс 3: Реклама (изображение + текст = контекстный таргетинг)

class AdContextAnalyzer:
    def classify_ad_context(self, banner: Image, page_text: str) -> AdContext:
        # Понимает не просто категорию изображения,
        # а совместный смысл изображения + контекста страницы
        return self.vlm.classify(
            text=f"Контекст страницы: {page_text[:500]}",
            image=banner,
            labels=AD_SAFETY_CATEGORIES
        )
```

## Практика масштабирования

```
GPU выбор (2025):
  Consumer (RTX 4090, 24 GB):
    → 7B VLM: работает (fp16 + квантизация 4bit)
    → 13B VLM: с трудом (batch=1, медленно)
    → Для прода: нет

  A100 40GB:
    → До 34B VLM без квантизации
    → Batch inference: эффективно
    → Для прода: да (мультиарендность)

  H100 80GB:
    → 70B+ VLM
    → Flash Attention 2: -40% памяти, +30% скорость
    → Для прода крупных задач

Оптимизации:
  → Flash Attention 2: обязательно для VLM
  → Lazy tokenization изображений: токенизируй только нужные патчи
  → KV-cache: особенно важен при длинных документах
  → Quantization (AWQ/GPTQ): 4bit с минимальной потерей качества
```

## Применение к Lorenzo

Lorenzo + VLM паттерн → **Мультимодальный анализ артефактов**:

```python
# improve_visual_analysis.py (паттерн):
# Lorenzo работает с текстом. VLM позволяет работать и с изображениями.

class LorenzoVLMAnalyzer:
    """Анализ изображений в docs/ (диаграммы, скриншоты, графики)"""

    def analyze_diagram(self, image_path: str,
                        context: str) -> str:
        """
        Lorenzo находит .png/.svg в docs/ → VLM описывает
        Пример: архитектурная диаграмма Svyazi 2.0
        → "Диаграмма показывает: CardStore → MCP → Gateway,
           отсутствует связь между CardStore и GraphRAG"
        """
        return self.vlm.generate(
            text=f"Опиши архитектуру на диаграмме. Контекст: {context}",
            image=load_image(image_path)
        )

    def check_screenshot_quality(self, screenshot: Image) -> QualityReport:
        """Аналог VisualCheckerAgent из CAVM (R26)"""
        return self.vlm.check(
            image=screenshot,
            criteria=["читаемость", "полнота", "артефакты"]
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Multimodal + CAVM (R26)** | VLM-агент как Visual Checker: проверяет графики в аналитическом отчёте |
| **Multimodal + Visual Testing (R25)** | VLM понимает смысл изменений UI, не только пиксели |
| **Multimodal + RAG TestGen (R27)** | Скриншот теста → VLM → описание → RAG → новый тест |
| **Multimodal + AIOps (R24)** | Скриншот графика метрик → VLM → "вижу аномалию в 14:32" |
| **Multimodal + Personal AI (R27)** | Фото еды → VLM → калории → в episodic memory |

## Контакт

- Статья: https://habr.com/ru/companies/oleg-bunin/articles/914848/ (июнь 2025)
- Смежная (Яндекс VLM Алиса): https://habr.com/ru/companies/yandex/articles/904584/
- Смежная (CAVM Visual Checker R26): https://habr.com/ru/articles/960338/
- AGE-VLM paper: arxiv.org/abs/2412.18083
- LLaVA (open-source VLM): github.com/haotian-liu/LLaVA

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
