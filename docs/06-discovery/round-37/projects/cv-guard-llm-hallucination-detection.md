# CV как судья для LLM: трёхуровневая детекция галлюцинаций

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Bahama_Papa  
**Хабр:** https://habr.com/ru/articles/1007788/  
**GitHub:** нет (production система PhotoMentor)  
**Слой:** analytics  
**Дата:** март 2025  
**Уникальность:** Трёхуровневая система детекции галлюцинаций для мультимодального LLM (Gemini Vision): YOLO bounding boxes + детерминированные CV проверки (гистограммы, Canny/Hough) как Guard V1; паттерн-матчинг текстовых утверждений к измеренной пиксельной геометрии как Guard V2. ~70% детекция пространственных галлюцинаций при <100ms overhead на реальном продукте ($6-10/месяц).

## Проблема: мультимодальные LLM видят то, чего нет

```
PhotoMentor = AI-ментор для фотографов
  → Пользователь загружает фото
  → Gemini Vision анализирует: "горизонт завален на 5°", "пересветы в небе"
  → Проблема: 15-20% утверждений о геометрии/физике — ЛОЖЬ

Типичные галлюцинации Gemini Vision на фото:
  "Горизонт ровный" → на самом деле завален на 12°
  "Небо правильно экспонировано" → гистограмма показывает clipping
  "Объект сфокусирован" → blur map показывает расфокус

Причина: мультимодальные LLM рассуждают на токенах, не пикселях
  → Не "измеряют" горизонт — угадывают по паттернам
  → Не "читают" гистограмму — описывают типичную картинку
  → Детерминированный CV может измерить точно
```

## Трёхуровневый pipeline

```python
# PhotoMentor: hallucination guard для Gemini Vision

class HallucinationGuard:
    """
    Слой 1: Генерация ответа LLM
    Слой 2: Guard V1 (детерминированный CV)
    Слой 3: Guard V2 (text-geometry matching)

    ~100ms overhead vs 2-3s inference Gemini Vision
    """

    async def analyze_photo(self, image_path: str) -> dict:
        # Шаг 1: Параллельно запустить LLM + CV анализ
        llm_response, cv_measurements = await asyncio.gather(
            self.gemini.analyze(image_path),
            self.cv_analyzer.measure(image_path)
        )

        # Шаг 2: Guard V1 — проверить CV измерения
        v1_flags = self.guard_v1.check(cv_measurements)

        # Шаг 3: Guard V2 — сопоставить текст LLM с CV данными
        v2_flags = self.guard_v2.match(
            llm_claims=self.extract_claims(llm_response),
            cv_measurements=cv_measurements
        )

        # Финальный ответ: скорректированный или с предупреждением
        if v1_flags or v2_flags:
            return self.correct_response(llm_response, v1_flags, v2_flags)
        return llm_response
```

## Guard V1: детерминированный CV

```python
import cv2
import numpy as np
from ultralytics import YOLO

class CVGuardV1:
    """
    Объективные измерения: LLM не может оспорить физику.
    """

    def __init__(self):
        self.yolo = YOLO("yolov8n.pt")  # детекция объектов

    def measure_horizon(self, image: np.ndarray) -> dict:
        """
        Измерение горизонта через Canny + Hough Transform.
        Если LLM говорит "горизонт ровный", а Hough показывает >2° — флаг.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        lines = cv2.HoughLinesP(
            edges, rho=1, theta=np.pi/180,
            threshold=100, minLineLength=100, maxLineGap=10
        )

        if lines is None:
            return {"horizon_detected": False}

        # Найти самую длинную горизонтальную линию
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if abs(angle) < 30:  # горизонтальная линия
                angles.append(angle)

        if not angles:
            return {"horizon_detected": False}

        avg_angle = np.mean(angles)
        return {
            "horizon_detected": True,
            "tilt_degrees": float(avg_angle),
            "is_level": abs(avg_angle) < 1.5  # допуск 1.5°
        }

    def measure_exposure(self, image: np.ndarray) -> dict:
        """
        Анализ гистограммы для детекции пересветов/недодержки.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
        hist_normalized = hist.flatten() / hist.sum()

        # Пересвет: >5% пикселей в диапазоне 250-255
        overexposed_pct = hist_normalized[250:].sum()
        # Недодержка: >5% пикселей в диапазоне 0-5
        underexposed_pct = hist_normalized[:6].sum()

        return {
            "overexposed": overexposed_pct > 0.05,
            "underexposed": underexposed_pct > 0.05,
            "overexposed_pct": float(overexposed_pct * 100),
            "underexposed_pct": float(underexposed_pct * 100)
        }

    def measure_sharpness(self, image: np.ndarray,
                           bbox: tuple = None) -> dict:
        """
        Резкость через Laplacian variance.
        bbox: зона проверки (например, лицо от YOLO)
        """
        if bbox:
            x1, y1, x2, y2 = bbox
            roi = image[y1:y2, x1:x2]
        else:
            roi = image

        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

        return {
            "sharpness_score": float(laplacian_var),
            "is_sharp": laplacian_var > 100,  # эмпирический порог
        }
```

## Guard V2: паттерн-матчинг текста к геометрии

```python
import re

class CVGuardV2:
    """
    Сопоставление текстовых утверждений LLM с CV измерениями.
    LLM говорит "горизонт ровный" → проверить cv_measurements.horizon.is_level
    """

    # Словарь: паттерн в тексте LLM → какое CV измерение проверить
    CLAIM_PATTERNS = {
        r"горизонт (ровный|правильный|выровнен)": "horizon.is_level",
        r"горизонт (завал|наклон|перекошен)": "NOT horizon.is_level",
        r"(пересвет|переэкспонирован|выбитые света)": "exposure.overexposed",
        r"(недодержка|темный|недоэкспонирован)": "exposure.underexposed",
        r"(резкий|в фокусе|четкий)": "sharpness.is_sharp",
        r"(нерезкий|не в фокусе|размытый)": "NOT sharpness.is_sharp",
    }

    def match(self, llm_claims: str,
               cv_measurements: dict) -> list[dict]:
        """
        Найти противоречия между текстом LLM и CV данными.
        """
        contradictions = []

        for pattern, cv_path in self.CLAIM_PATTERNS.items():
            if re.search(pattern, llm_claims, re.IGNORECASE):
                # LLM сделала это утверждение — проверить по CV
                negated = cv_path.startswith("NOT ")
                actual_path = cv_path.lstrip("NOT ")

                cv_value = self._get_nested(cv_measurements, actual_path)
                expected = not negated if cv_value else negated

                if not expected:
                    contradictions.append({
                        "claim": pattern,
                        "llm_said": "present" if not negated else "absent",
                        "cv_measured": str(cv_value),
                        "severity": "high"
                    })

        return contradictions

    def correct_response(self, original: str,
                          contradictions: list[dict],
                          cv_data: dict) -> dict:
        """
        Скорректировать ответ LLM на основе CV данных.
        """
        corrections = []
        for c in contradictions:
            corrections.append(
                f"⚠️ Уточнение: CV анализ показывает '{c['cv_measured']}' "
                f"(LLM утверждала обратное)"
            )

        return {
            "llm_response": original,
            "corrections": corrections,
            "cv_measurements": cv_data,
            "hallucinations_detected": len(contradictions)
        }
```

## Результаты на PhotoMentor

```python
PHOTOMENTOR_RESULTS = {
    "продукт": "PhotoMentor — AI-ментор для фотографов",
    "проблема": "15-20% Gemini Vision ответов содержат пространственные галлюцинации",
    "тестовый_датасет": "500 фото с верифицированными ground truth измерениями",

    "guard_v1_performance": {
        "описание": "Детерминированный CV (Canny + гистограмма + Laplacian)",
        "catch_rate": "~45% галлюцинаций",
        "false_positive_rate": "~3%",
        "latency_ms": 40
    },

    "guard_v2_performance": {
        "описание": "Text-geometry matching",
        "catch_rate": "~25% дополнительных галлюцинаций",
        "false_positive_rate": "~5%",
        "latency_ms": 15
    },

    "combined": {
        "total_catch_rate": "~70% пространственных галлюцинаций",
        "false_positive_rate": "~7%",
        "total_latency_ms": "<100",
        "monthly_cost": "$6-10 (CV inference на CPU)"
    },

    "ключевой_вывод": (
        "Детерминированный CV = best complement к мультимодальному LLM "
        "для физически верифицируемых утверждений. "
        "LLM хороши в семантике, CV хорош в геометрии."
    )
}
```

## Обобщение: грounded fact-checking паттерн

```python
class GroundedFactChecker:
    """
    Обобщённый паттерн Bahama_Papa для любого домена:
    Там где есть детерминированная верификация → не доверяй LLM.

    Примеры применения:
    - Медицина: LLM описывает рентген → сравнить с radiodensity измерениями
    - Финансы: LLM анализирует график → сравнить с численными данными
    - Производство: LLM описывает чертёж → сравнить с CAD параметрами
    """

    FACT_CHECKER_REGISTRY = {
        "photography": CVGuardV1,        # геометрия, гистограмма, резкость
        "medical_imaging": DicomChecker, # HU значения, размеры
        "financial_charts": ChartParser, # цены, объёмы, индикаторы
        "engineering": CADValidator      # размеры, допуски, материалы
    }

    def verify_llm_claim(self, domain: str,
                          llm_response: str,
                          source_data: any) -> dict:
        checker = self.FACT_CHECKER_REGISTRY[domain]
        measurements = checker.measure(source_data)
        claims = self.extract_verifiable_claims(llm_response, domain)
        return self.match_claims_to_measurements(claims, measurements)
```

## Применение к Lorenzo

```python
# Lorenzo анализирует документы.
# CV Guard паттерн: верификация фактических утверждений LLM

class LorenzoFactVerifier:
    """
    improve_llm_qa.py иногда галлюцинирует о числах/датах в документах.
    Guard паттерн: сравнить ответ LLM с детерминированным извлечением.
    """

    def verify_answer(self, question: str, llm_answer: str,
                       source_docs: list[str]) -> dict:
        # Детерминированно извлечь числа, даты, имена из источников
        facts = self.deterministic_extractor.extract(source_docs)

        # Сравнить с тем что сказала LLM
        llm_claims = self.claim_extractor.extract(llm_answer)
        contradictions = self.match(llm_claims, facts)

        return {
            "answer": llm_answer,
            "verified": len(contradictions) == 0,
            "contradictions": contradictions
        }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **CV Guard + LLAMATOR (R33)** | LLAMATOR генерирует visual jailbreaks → CV Guard как defence |
| **CV Guard + VLM vs IDP (R30)** | CV Guard для верификации VLM извлечения из документов |
| **CV Guard + DBRM (R31)** | Guard layer в медицинском AI: CV верифицирует LLM описания снимков |
| **CV Guard + LLM Judge (R28)** | Кросс-модельный judge + CV Ground truth = robust hallucination scoring |
| **CV Guard + Avito VLM (R32)** | Верификация VLM описаний товаров: детерминированный CV vs LLM |

## Контакт

- Статья: https://habr.com/ru/articles/1007788/ (март 2025)
- PhotoMentor: AI-ментор для фотографов
- YOLO v8: github.com/ultralytics/ultralytics
- Смежная (почему LLM врут с умным видом): https://habr.com/ru/articles/944978/
- Смежная (EICS метрика, white-box uncertainty): https://habr.com/ru/articles/1033580/
- OpenCV: opencv.org
