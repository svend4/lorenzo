# Визуальное тестирование с AI: скриншоты без ложных срабатываний

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** OTUS (Хабр, 2025) + Avito, T-Bank, Яндекс (смежные статьи)  
**Хабр:** https://habr.com/ru/companies/otus/articles/956492/ (основная)  
**Смежные:** https://habr.com/ru/companies/alfa/articles/850748/, https://habr.com/ru/companies/yandex/articles/890548/  
**GitHub:** не опубликован (разборы паттернов)  
**Слой:** quality / orchestration  
**Дата:** 2025  
**Уникальность:** Первый русскоязычный практический разбор проблемы ложных срабатываний в скриншотном тестировании с применением нейросетей. Ключевое: pixel diff → neural diff → LLM-описание различий. Avito: только 1 из 5 команд использует screenshot-тесты (боятся flakiness). Решение: обучить сеть на "смысловых" различиях вместо пиксельных.

## Проблема ложных срабатываний

```
Традиционный pixel diff:
  Скриншот 1 vs Скриншот 2 → посчитать разные пиксели
  
  Проблема 1: Рендеринг-шум
    Одинаковая страница → разные пиксели из-за anti-aliasing,
    субпиксельного рендеринга шрифтов, анимаций
    → тест падает на каждый запуск

  Проблема 2: Карты и динамический контент
    Карта сдвинулась на 1px → "все границы объектов изменились"
    → 80% пикселей "разные" хотя карта визуально та же

  Проблема 3: Масштаб
    100px кнопка → проверяется 10,000 пикселей
    1 новый элемент → тест падает, хотя это не регрессия
```

## Нейросетевой подход: смысловые различия

```python
# Не "разные пиксели" — а "значимые визуальные изменения"

class NeuralVisualDiff:
    def __init__(self):
        # Encoder: превратить скриншот в embedding визуальных регионов
        self.encoder = load_vision_encoder("clip-vit-b32")

        # Displacement detector: выравнивание перед сравнением
        # Обучен предсказывать (dx, dy) вместо boolean equal/not_equal
        self.displacement_model = DisplacementNet()

        # Classifier: значима ли разница?
        self.diff_classifier = BinaryDiffClassifier()

    def compare(self, screenshot1: Image, screenshot2: Image) -> DiffReport:
        # Шаг 1: выровнять (compensate displacement)
        dx, dy = self.displacement_model.predict(screenshot1, screenshot2)
        aligned_s2 = shift(screenshot2, dx, dy)

        # Шаг 2: embedding-based diff (не пиксельный)
        embedding1 = self.encoder.encode_regions(screenshot1)
        embedding2 = self.encoder.encode_regions(aligned_s2)

        # Шаг 3: классифицировать регионы
        diffs = []
        for region1, region2 in zip(embedding1, embedding2):
            if self.diff_classifier.is_significant(region1, region2):
                diffs.append(DiffRegion(
                    bbox=region1.bbox,
                    description=self.describe_diff(region1, region2),
                    severity=self.assess_severity(region1, region2)
                ))
        return DiffReport(differences=diffs, false_positive_rate=0.02)
```

## LLM для описания различий

```python
# Нейросеть нашла регион с различием → LLM объясняет ЧТО изменилось

class LLMDiffDescriber:
    def describe(self, region_before: Image, region_after: Image) -> str:
        prompt = f"""
        Сравни два скриншота одного UI-элемента.
        Опиши ТОЛЬКО визуально значимые изменения.
        Игнорируй субпиксельные различия.
        
        Формат: "В [компонент] изменился [атрибут]: было [X], стало [Y]"
        Примеры:
          "В кнопке 'Оплатить' изменился цвет: было синий #0066CC, стало зелёный #00AA44"
          "В заголовке добавлен новый текст: 'Акция до 31 мая'"
          "Исчезла иконка корзины в правом верхнем углу"
        """
        return vision_llm.compare(region_before, region_after, prompt)

# Результат: тест-репорт на человеческом языке
# "Обнаружено 2 изменения: кнопка CTA сменила цвет, исчезла иконка"
# вместо "2847 пикселей изменились"
```

## Паттерн из Avito: почему только 20% используют screenshot-тесты

```
Исследование QA в России 2025 (Avito, 800+ специалистов):
  Только 1 из 5 команд использует screenshot-тесты

Причины отказа:
  1. Flakiness (47%): тесты нестабильны, падают без причин
  2. Поддержка (38%): при каждом дизайн-изменении обновлять baseline
  3. CI/CD интеграция (28%): медленные, нет удобного diff в PR
  4. Инструменты (21%): Percy ($$$), Applitools ($$$)

Решение AI-подхода для всех 4 проблем:
  1. Flakiness → neural diff + displacement → false positive rate <2%
  2. Поддержка → LLM автоматически решает: "регрессия или намеренное изменение?"
  3. CI/CD → GitHub Actions + скриншот-комментарий в PR с описанием
  4. Инструменты → open-source стек (Playwright + custom neural diff)
```

## Практический стек 2025

```python
# Playwright + neural diff + LLM описание (всё open-source)

# playwright_visual_test.py
import asyncio
from playwright.async_api import async_playwright

async def visual_regression_test(url: str, baseline_path: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1280, "height": 720})
        await page.goto(url)

        # Скриншот текущего состояния
        current = await page.screenshot()

        # Сравнение с baseline
        diff = neural_diff.compare(
            Image.open(baseline_path),
            Image.open(current)
        )

        if diff.has_significant_changes:
            # LLM описывает что изменилось
            description = llm_describer.describe_all(diff.changed_regions)
            report = {
                "status": "REGRESSION_DETECTED",
                "changes": description,
                "diff_image": diff.visualize()
            }
            # Прикрепить к PR-комментарию
            github.comment_pr(report)
            assert False, f"Visual regression: {description}"
```

## Paттерн T-Bank: отказ от скриншотов → semantic assertions

```python
# Статья T-Bank: "Как отказаться от скриншотов в тестировании" (824132)
# Альтернативный подход: не сравнивать пиксели, а проверять семантику

class SemanticUITest:
    def assert_ui_state(self, page, expected_state: dict):
        """Вместо скриншота — проверка через LLM что видит пользователь"""
        screenshot = page.screenshot()

        actual_state = vision_llm.extract_state(screenshot, {
            "main_heading": "Какой заголовок страницы?",
            "cta_button": "Есть ли кнопка призыва к действию? Какой текст?",
            "error_messages": "Есть ли сообщения об ошибках?",
            "price": "Какая цена отображается?"
        })

        for key, expected in expected_state.items():
            assert actual_state[key] == expected, \
                f"UI regression: {key} = '{actual_state[key]}', expected '{expected}'"

# Преимущество: тест не зависит от пикселей
# "Кнопка 'Купить за 1999₽' должна быть на странице" → всегда стабильно
```

## Применение к Lorenzo

Lorenzo имеет `improve_pre_commit.py` и CI pipeline.  
Visual Testing паттерн = **Documentation Visual QA**:

```python
# improve_visual_qa.py (паттерн):
# Lorenzo генерирует MINDMAP.md (Mermaid), word_cloud.svg, HEATMAP.md
# Visual QA: проверить что сгенерированные визуальные артефакты корректны

def check_visual_artifacts():
    """Проверить визуальные файлы Lorenzo через vision LLM"""
    artifacts = [
        "docs/word_cloud.svg",
        "docs/MINDMAP.md",      # Mermaid → render → screenshot
    ]
    for artifact in artifacts:
        screenshot = render_to_image(artifact)
        issues = vision_llm.check(screenshot, criteria={
            "readable": "Текст разборчив?",
            "complete": "Нет ли обрезанных элементов?",
            "correct": "Структура выглядит логично?"
        })
        if issues:
            report_issue(artifact, issues)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Visual Testing + LLM Tests (R20)** | Mutation тесты для UI: проверить что изменение кода = изменение UI |
| **Visual Testing + AppSec (R22)** | UI screenshot анализ: LLM ищет фишинг-признаки и security UI антипаттерны |
| **Visual Testing + Durable State (R23)** | SessionContext для длинных регрессионных прогонов (reconnect без рестарта) |
| **Visual Testing + CI/CD (R15)** | AI Review code + Visual diff в одном GitHub Actions workflow |
| **Visual Testing + Desmond (R19)** | Cognitive Worker: дизайнер создаёт макет → агент автоматически обновляет baseline |

## Контакт

- Основная (neural diff без ложных срабатываний): https://habr.com/ru/companies/otus/articles/956492/
- Alfa Bank (скриншот-тестирование): https://habr.com/ru/companies/alfa/articles/850748/
- Яндекс (frontend visual testing): https://habr.com/ru/companies/yandex/articles/890548/
- T-Bank (отказ от скриншотов): https://habr.com/ru/companies/tbank/articles/824132/
- Avito (QA в России 2025): https://habr.com/ru/companies/avito/articles/1026786/
- Playwright: github.com/microsoft/playwright (Apache 2.0)
