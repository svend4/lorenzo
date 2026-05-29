---
date: 2026-05-29
tags: [rag, orchestration, knowledge, ingestion, architecture]
state: normalized
---

# PhysicalAgent: VLA-агент для роботов без обучения на траекториях

<!-- toc-auto -->
<!-- tags: physicalagent-vla-robotics-multimodal, docs -->


<!-- summary -->
> Автор: Artem_Lykov (MTS blog) Хабр: https://habr.com/ru/companies/ru_mts/articles/979682/
Хабр: https://habr.com/ru/companies/ru_mts/articles/979682/  
GitHub: нет; ArXiv: https://arxiv.org/pdf/2509.13903  
Слой: orchestration / analytics  
Дата: декабрь 2025  
Уникальность: 4-агентный VLA-пайплайн (Perceiv


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Artem_Lykov (MTS blog)  
**Хабр:** https://habr.com/ru/companies/ru_mts/articles/979682/  
**GitHub:** нет; ArXiv: https://arxiv.org/pdf/2509.13903  
**Слой:** orchestration / analytics  
**Дата:** декабрь 2025  
**Уникальность:** 4-агентный VLA-пайплайн (Perceive→Plan→Reason→Act) для управления роботами без сбора дорогостоящих датасетов траекторий. Ключевой паттерн: видео-агент синтезирует гипотетическое видео выполнения задачи → мониторинг-агент верифицирует физическую реалистичность через мультимодальный LLM → motion-агент извлекает команды суставов → исполнение на реальном роботе с итерацией при отказе. Результат: 80% успех к 3-4 итерации без task-specific обучения.

## Проблема: датасеты траекторий дороги и не обобщаются

```
Традиционный robot learning подход:
  → Collect 50K+ human demonstrations
  → Train task-specific policy
  → $100K+ стоимость разметки
  → Работает только для одной задачи

Vision-Language-Action (VLA) подход:
  → Fine-tune RT-2/OpenVLA на демонстрациях
  → Требует: качественные видеозаписи + joint annotations
  → Не обобщается на новые объекты/обстановки
  → NVIDIA GR00T: большая модель, но всё равно нужны демо

PhysicalAgent: нулевой сбор данных
  → LLM понимает задачу из текстового описания
  → Video generation agent синтезирует "что должно произойти"
  → Физическая верификация через VLM
  → Итеративное уточнение при отказе реального робота
```

## 4-агентный пайплайн

```python
# PhysicalAgent: VLA без task-specific training
# arxiv.org/pdf/2509.13903

from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class RobotTask:
    """Задача для робота — только текст, без демонстраций."""
    description: str           # "Возьми красный куб и положи в корзину"
    robot_type: str            # "UR5 manipulator" / "Humanoid" / "Simulation"
    current_state: dict        # текущее состояние из сенсоров


class PhysicalAgentPipeline:
    """
    4-агентный пайплайн: текст → видео → команды → робот.

    Ключевое: VLM как физический валидатор.
    Если видео не реалистично (телекинез, нарушение гравитации) →
    перегенерировать.
    """

    # Агент 1: Perceive — понимание задачи и состояния
    def perceive(self, task: RobotTask) -> dict:
        """
        Мультимодальный LLM анализирует:
        - Текстовое описание задачи
        - Текущее состояние (изображение рабочей зоны)
        - Параметры робота (DOF, рабочая зона, constraints)

        Выход: структурированный план действий
        """
        state_image = self.camera.capture()
        plan = self.vlm.analyze(
            text=task.description,
            image=state_image,
            robot_spec=task.robot_type
        )
        return {
            "subtasks": plan["steps"],          # ["найти красный куб", "захват", ...]
            "objects_detected": plan["objects"], # bounding boxes объектов
            "constraints": plan["constraints"]  # "не ронять", "медленно"
        }

    # Агент 2: Plan — генерация видео желаемой траектории
    def plan(self, perception: dict, task: RobotTask) -> str:
        """
        Video generation: синтез гипотетического видео выполнения.
        Модели: Sora-style / CogVideoX / Wan2.1

        Промпт: "Робот UR5 берёт красный куб захватом сверху
        и перемещает в синюю корзину справа. Плавное движение,
        без столкновений."
        """
        video_prompt = self._build_video_prompt(perception, task)
        hypothetical_video = self.video_gen.generate(
            prompt=video_prompt,
            duration_seconds=5,
            fps=30
        )
        return hypothetical_video  # path к видеофайлу

    # Агент 3: Reason — физическая верификация VLM
    def reason(self, video_path: str,
                task: RobotTask,
                max_attempts: int = 5) -> str:
        """
        VLM-мониторинг: видео физически реалистично?

        Проверяет:
        - Нарушение гравитации (объекты летают)
        - Телекинез (рука не касается объекта)
        - Нарушение joint limits
        - Столкновения с препятствиями

        Если нереалистично → перегенерировать с уточнённым промптом.
        """
        for attempt in range(max_attempts):
            validation = self.vlm.validate_physics(
                video=video_path,
                task=task.description,
                robot_type=task.robot_type,
                questions=[
                    "Рука реально касается объекта?",
                    "Движение физически возможно для данного манипулятора?",
                    "Нет ли телекинеза или нарушения гравитации?"
                ]
            )

            if validation["is_physically_plausible"]:
                return video_path  # видео верифицировано

            # Уточнить промпт по обратной связи
            video_path = self.plan_with_feedback(
                feedback=validation["issues"],
                task=task
            )

        return video_path  # лучшее из попыток

    # Агент 4: Act — извлечение команд и исполнение
    def act(self, verified_video: str,
             robot: "RobotInterface",
             max_retries: int = 4) -> dict:
        """
        Motion extraction: видео → joint angles per frame.
        Execution: команды → реальный робот → проверка успеха.
        Retry loop: если упал → perception → новый план.
        """
        joint_commands = self.motion_extractor.extract(verified_video)

        for attempt in range(max_retries):
            success = robot.execute(joint_commands)

            if success:
                return {"success": True, "attempts": attempt + 1}

            # Perception → новое видео → новые команды
            current_state = robot.get_state()
            new_video = self.plan(
                self.perceive(RobotTask(
                    description=f"Продолжи задачу. Текущее состояние: {current_state}",
                    robot_type=robot.type,
                    current_state=current_state
                )),
                task=None
            )
            joint_commands = self.motion_extractor.extract(new_video)

        return {"success": False, "attempts": max_retries}
```

## Поддерживаемые VLM и результаты

```python
SYSTEM_PROFILE = {
    "arxiv": "https://arxiv.org/pdf/2509.13903",
    "автор": "Artem Lykov et al. (публикация MTS blog)",

    "поддерживаемые_vlm": [
        "GPT-4o",          # физическая верификация
        "Claude 3.5",      # физическая верификация
        "Qwen-VL",         # открытая альтернатива
        "Gemini Pro Flash" # быстрая верификация
    ],

    "поддерживаемые_роботы": [
        "Манипуляторы (UR5, Franka)",
        "Гуманоидные роботы",
        "Симуляторы (IsaacGym, MuJoCo)"
    ],

    "результаты": {
        "success_rate_iteration_1": "~40-50%",
        "success_rate_iteration_3_4": "~80%",
        "task_specific_training_data": "0 (zero-shot)",
        "физическая_валидация": "ключевой фактор успеха"
    },

    "сравнение": {
        "RT-2": "Требует 130K траекторий; PhysicalAgent: 0",
        "OpenVLA": "Fine-tuning нужен; PhysicalAgent: zero-shot",
        "GR00T": "NVIDIA proprietary + датасеты; PhysicalAgent: API only"
    },

    "стек": {
        "video_generation": "Sora / CogVideoX / Wan2.1",
        "vlm_validation": "GPT-4o / Claude 3.5 / Qwen-VL",
        "motion_extraction": "Pose estimation из видеокадров",
        "robot_interface": "ROS / IsaacGym API"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: PhysicalAgent паттерн — видео-планирование для агентов

class LorenzoHypotheticalPlanner:
    """
    PhysicalAgent паттерн для Lorenzo:
    Перед выполнением сложного multi-step действия —
    LLM строит "гипотетический сценарий" и валидирует его.

    Аналог video generation: текстовый "черновик" действия
    → VLM-style валидация через LLM → исполнение.
    """

    def plan_with_validation(self, task: str) -> dict:
        # Шаг 1: Сгенерировать черновой план
        draft_plan = self.llm.generate(f"Опиши шаг за шагом как выполнить: {task}")

        # Шаг 2: Валидация плана (аналог физической верификации)
        validation = self.llm.validate(
            f"Проверь план: {draft_plan}\n"
            f"Есть ли противоречия, недостающие шаги, риски?"
        )

        # Шаг 3: Уточнение если нужно
        if not validation["is_valid"]:
            draft_plan = self.llm.refine(draft_plan, validation["issues"])

        return {"plan": draft_plan, "validated": True}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **PhysicalAgent + MAESTRO (R38)** | CARL DAG для пошаговой верификации каждого этапа VLA-пайплайна |
| **PhysicalAgent + Sequential (R38)** | Ансамбль VLM-агентов верифицирует физическую реалистичность без координатора |
| **PhysicalAgent + LangFuse (R38)** | Трейсинг каждой попытки Perceive→Plan→Reason→Act: где именно отказы |
| **PhysicalAgent + Graph RAG (R38)** | База знаний физических ограничений роботов → VectorCypher поиск при валидации |
| **PhysicalAgent + Stryker Testing (R39)** | Mutation testing видео-планов: проверка устойчивости VLA к вариациям сцены |

## Контакт

- Статья: https://habr.com/ru/companies/ru_mts/articles/979682/ (декабрь 2025)
- ArXiv: https://arxiv.org/pdf/2509.13903
- Смежная (VLA обзор RT-2/OpenVLA/GR00T): https://habr.com/ru/articles/829018/
- Смежная (OCR VLM для документов, М.Видео): https://habr.com/ru/companies/mvideo/articles/897266/
- Смежная (LLM для чертежей бенчмарк): https://habr.com/ru/companies/tehnologika/articles/851394/

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
