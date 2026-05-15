---
date: 2026-05-15
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# ЕГЭ AI-репетитор: 6-сценарный оркестратор для математики без LangChain

<!-- toc-auto -->
<!-- tags: vladotpad-ege-ai-tutor-math-scenario-orchestrator, docs -->


<!-- summary -->
> `vladotpad-ege-ai-tutor-math-scenario-orchestrator` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** vladotpad (Владислав Калиниченко, Innopolis University, Research Scientist)  
**Хабр:** https://habr.com/ru/articles/989136/  
**GitHub:** нет (production кейс, venture)  
**Слой:** orchestration  
**Дата:** январь 2025  
**Уникальность:** Единственный задокументированный на Хабре AI-репетитор для ЕГЭ по математике с детальной архитектурой: 3 итерации (RAG→агент→fine-tune), 6-сценарный педагогический оркестратор с режимом «сократическая частичная помощь», math OCR → LaTeX для символьной математики. Отказ от LangChain в production в пользу bare OpenAI API (конкретный разбор причин). Результат: 86 баллов ЕГЭ (топ-уровень) на демо-варианте 2025.

## Проблема: AI не умеет "учить" математику

```
Стандартный ChatGPT для ЕГЭ:
  Вопрос: "Реши задачу 19: ..."
  → ChatGPT: выдаёт готовое решение
  → Ученик: списал, ничему не научился
  → На реальном ЕГЭ: завалил

Репетитор для ЕГЭ должен:
  1. НЕ давать готовый ответ сразу (Сократ: вопросы, не ответы)
  2. Проверять решение ученика (верификация шагов)
  3. Объяснять теорию когда нужно (не когда не просят)
  4. Понимать математические обозначения из фото задач
  5. Знать специфику ЕГЭ: типы задач, критерии оценки

Три эволюции deeplitlm:
  v1 (RAG-based): vector DB 4K пар задача→решение, few-shot
  → Не умеет вести диалог, нет сценарного контроля

  v2 (agent-based): 6-сценарный оркестратор, bare OpenAI API
  → Хорошо умеет учить, но не специализирован на ЕГЭ

  v3 (fine-tuned): LLM обучена на реформулированных решениях
  → Максимальное качество объяснений по шагам
```

## Архитектура: 6-сценарный педагогический оркестратор

```python
# vladotpad (Innopolis University): deeplitlm ЕГЭ-репетитор
# habr.com/ru/articles/989136/

from dataclasses import dataclass
from typing import Literal
from enum import Enum

class PedagogicalScenario(Enum):
    """
    6 сценариев взаимодействия с учеником.

    Ключевое отличие от ChatGPT: не один режим "ответить",
    а шесть режимов с разными педагогическими целями.
    """
    SOLVE_FOR_ME = "solve"          # Сценарий 1: Решить задачу полностью
    VERIFY_SOLUTION = "verify"      # Сценарий 2: Проверить решение ученика
    PARTIAL_HINT = "hint"           # Сценарий 3: Сократическая частичная помощь
    THEORY_QA = "theory"            # Сценарий 4: Теоретический вопрос
    EXAM_RULES = "rules"            # Сценарий 5: Правила ЕГЭ/критерии
    COLLABORATIVE_STEP = "collab"   # Сценарий 6: Совместное пошаговое решение


@dataclass
class StudentMessage:
    """Входящее сообщение от ученика."""
    text: str
    image_path: str | None = None  # фото задачи из учебника
    session_history: list[dict] = None  # предыдущий диалог

@dataclass
class TutorResponse:
    """Ответ репетитора."""
    text: str
    scenario_used: PedagogicalScenario
    step_number: int | None = None  # для COLLABORATIVE_STEP
    latex_rendered: str | None = None  # математические формулы


class MathOCRPipeline:
    """
    Конвертация фото задач в LaTeX для LLM.

    Проблема: ЕГЭ-задачи часто содержат сложные математические
    символы (интегралы, дроби, корни, тригонометрия).
    LLM плохо понимает скриншоты с формулами.

    Решение: Math OCR → LaTeX строка → LLM понимает структуру

    Инструменты: pix2tex, Mathpix, LaTeX-OCR
    """

    def extract_math(self, image_path: str) -> str:
        """
        Изображение задачи → LaTeX строка.
        Например: фото "∫(x² + 3x)dx" → "\\int (x^2 + 3x)\\,dx"
        """
        from PIL import Image
        img = Image.open(image_path)

        # pix2tex: специализированный Math OCR
        from pix2tex.cli import LatexOCR
        model = LatexOCR()
        latex_str = model(img)

        return latex_str  # "\\int_0^1 x^2\\,dx = \\frac{1}{3}"


class EGETutorOrchestrator:
    """
    Педагогический оркестратор для ЕГЭ по математике.

    deeplitlm v2: bare OpenAI API (не LangChain!)

    Почему отказались от LangChain:
    1. Friction при кастомной логике роутинга сценариев
    2. Abstraction leak: нельзя точно контролировать промпты
    3. Версионирование: API LangChain менялся, ломал production
    4. Debugging: сложно трейсить что именно пошло не так
    → Итог: bare openai.ChatCompletion + ручной state management
    """

    def __init__(self, task_db: "EGETaskDatabase"):
        self.task_db = task_db
        self.ocr = MathOCRPipeline()

    def route_scenario(self, message: StudentMessage) -> PedagogicalScenario:
        """
        Определить педагогический сценарий по запросу ученика.

        Ключевые паттерны:
        "реши задачу" → SOLVE_FOR_ME
        "проверь моё решение" → VERIFY_SOLUTION
        "подскажи только первый шаг" → PARTIAL_HINT (Сократ!)
        "что такое производная?" → THEORY_QA
        "сколько баллов за задание 19?" → EXAM_RULES
        "давай вместе решим" → COLLABORATIVE_STEP
        """
        text = message.text.lower()

        if any(kw in text for kw in ["реши", "найди", "вычисли"]) and \
           "сам" not in text and "мой" not in text:
            return PedagogicalScenario.SOLVE_FOR_ME

        elif any(kw in text for kw in ["проверь", "правильно ли", "верно ли"]):
            return PedagogicalScenario.VERIFY_SOLUTION

        elif any(kw in text for kw in ["подскажи", "намекни", "первый шаг"]):
            return PedagogicalScenario.PARTIAL_HINT  # Сократ

        elif any(kw in text for kw in ["что такое", "объясни", "почему"]):
            return PedagogicalScenario.THEORY_QA

        elif any(kw in text for kw in ["балл", "критерий", "правило егэ"]):
            return PedagogicalScenario.EXAM_RULES

        else:
            return PedagogicalScenario.COLLABORATIVE_STEP  # дефолт

    async def respond(self, message: StudentMessage) -> TutorResponse:
        """
        Ответить на сообщение ученика через нужный сценарий.
        """
        # OCR если есть изображение
        task_text = message.text
        if message.image_path:
            latex = self.ocr.extract_math(message.image_path)
            task_text = f"{message.text}\n[Задача из изображения: ${latex}$]"

        # Роутинг сценария
        scenario = self.route_scenario(message)

        # Получить похожие задачи из БД (RAG компонент deeplitlm v1)
        similar_tasks = self.task_db.find_similar(task_text, top_k=3)

        # Вызов LLM с нужным системным промптом
        system_prompt = self._get_scenario_prompt(scenario, similar_tasks)

        response_text = await self._call_openai(
            system=system_prompt,
            history=message.session_history or [],
            user=task_text
        )

        return TutorResponse(
            text=response_text,
            scenario_used=scenario
        )

    def _get_scenario_prompt(self,
                              scenario: PedagogicalScenario,
                              similar_tasks: list) -> str:
        """Системный промпт для каждого педагогического сценария."""

        few_shots = "\n".join([
            f"Задача: {t['task']}\nРешение: {t['solution']}"
            for t in similar_tasks
        ])

        base = f"""Ты репетитор по математике ЕГЭ. Вот похожие задачи для контекста:
{few_shots}
"""

        if scenario == PedagogicalScenario.PARTIAL_HINT:
            return base + """
ВАЖНО: НЕ давай полное решение. Задай наводящий вопрос или укажи ТОЛЬКО на следующий шаг.
Метод Сократа: ученик должен дойти до ответа сам.
Пример: "Попробуй сначала найти область допустимых значений. Что можно сказать о знаменателе?"
"""
        elif scenario == PedagogicalScenario.VERIFY_SOLUTION:
            return base + """
Проверь решение ученика пошагово. Укажи на первую ошибку (если есть).
Не давай правильное решение — спроси что ученик думает о шаге где ошибка.
"""
        elif scenario == PedagogicalScenario.COLLABORATIVE_STEP:
            return base + """
Решаем вместе пошагово. Предложи первый шаг, спроси ученика что он думает.
Жди ответа перед следующим шагом.
"""
        else:
            return base + "Ответь полно и понятно на вопрос ученика."


class EGETaskDatabase:
    """
    Vector DB с 4000+ парами задача→решение.

    Организация: по номеру задания ЕГЭ (1-19) + подтема.
    Few-shot retrieval: находим похожие задачи → LLM понимает контекст.

    deeplitlm v1 архитектура (сохранена в v2/v3 как RAG компонент).
    """

    N_TASKS = 4000  # задача+решение пар
    EMBEDDING_DIM = 1536  # text-embedding-3-small

    def find_similar(self, query: str, top_k: int = 3) -> list[dict]:
        """BM25 + cosine similarity по тематике задачи."""
        pass  # pgvector или FAISS


RESULTS = {
    "бенчмарк": "Демо-вариант ЕГЭ по математике 2025",
    "результат": "86 вторичных баллов (топ-уровень)",
    "база_знаний": "4000+ задача→решение пар (grouped by тип задания)",
    "причина_отказа_от_LangChain": [
        "Friction при кастомной логике роутинга",
        "Abstraction leak: нет контроля над промптами",
        "API нестабильность между версиями",
        "Сложный дебаггинг"
    ],
    "итерации": {
        "v1_RAG": "In-context few-shot, нет педагогического контроля",
        "v2_agent": "6-сценарный оркестратор, bare OpenAI API",
        "v3_finetuned": "LLM дообучена на реформулированных решениях"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: педагогический оркестратор для /api/ask

class LorenzoQueryOrchestrator:
    """
    vladotpad паттерн для Lorenzo:
    Роутинг запросов по педагогическим сценариям.

    Сценарий "дай пример": → поиск конкретного проекта с кодом
    Сценарий "объясни концепт": → теоретический ответ без примеров
    Сценарий "сравни подходы": → сравнение 2-3 проектов
    Сценарий "с чего начать": → сократический вопрос про контекст

    Аналог PARTIAL_HINT для Lorenzo:
    "Как сделать RAG?" → "Какой тип данных ищешь? Структурированный или нет?"
    (не давать готовый ответ, вести к правильному выбору архитектуры)
    """
    pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **ЕГЭ Tutor + Behavioral Profiles (R50)** | Профиль "ученик-новичок" vs "ученик-продвинутый" → разные сценарии по умолчанию |
| **ЕГЭ Tutor + Agent Evaluation (R48)** | Golden Set для педагогических сценариев: эталонные трассы "правильного обучения" vs "просто ответа" |
| **ЕГЭ Tutor + LangGraph (R44)** | LangGraph: scenario_router_node → partial_hint_node/verify_node/collab_node с checkpoint |
| **ЕГЭ Tutor + LLM Observability (R45)** | Трейсинг: какие сценарии ученики выбирают чаще, где репетитор "срывается" в SOLVE_FOR_ME |
| **ЕГЭ Tutor + Knowledge Graph (R47)** | Темпоральный граф прогресса студента: как понимание тем меняется со временем |

## Контакт

- Статья: https://habr.com/ru/articles/989136/ (январь 2025)
- Автор: vladotpad (Владислав Калиниченко, Innopolis University, Research Scientist)
- Math OCR: pix2tex (github.com/lukas-blecher/LaTeX-OCR) / Mathpix API
- ЕГЭ формат: fipi.ru (Федеральный институт педагогических измерений)
- Смежная (EdTech AI, R24): docs/06-discovery/round-24/
- Смежная (AI образование v2, R35): docs/06-discovery/round-35/
- Смежная (LLM Judge образование/CLEV, R47): docs/06-discovery/round-47/projects/maslennikov-llm-judge-educational-content-clev.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
