# Дистилляция агентских трейсов: обучение DevOps-LLM без разметки

**Автор:** makarsuperstar (Александр Макаренко)  
**Хабр:** https://habr.com/ru/articles/1033434/  
**GitHub:** нет  
**Слой:** analytics / orchestration  
**Дата:** май 2026  
**Уникальность:** Пайплайн дистилляции агентских трейсов для DevOps-LLM без ручной разметки: учительская модель (Gemma4:31b) переформатирует instruction/response пары в структурированный JSON-формат агента через few-shot из 5 эталонных трейсов. 8-метричный взвешенный валидатор (порог 84.8/100) фильтрует ~24% примеров. Ключевое открытие: domain mismatch (Magicoder: 38% on-topic vs GitHub трейсы: 95%) — acceptance rate не предсказывает on-topic качество.

## Проблема: нет данных для обучения специализированного агента

```
Хочу DevOps-агента: мониторинг, алерты, git, CI/CD.
Проблема: нет датасета агентских трейсов для этой задачи.

Варианты:
  1. Ручная разметка → дорого, медленно
  2. Синтетика от сильной модели (GPT-5) → дорого, API зависимость
  3. Дистилляция: учитель переформатирует существующие данные

Дистилляция через few-shot:
  → 5 эталонных трейсов в контексте учителя
  → Учитель переформатирует любой instruction/response в agent-JSON
  → 8-метричный валидатор фильтрует мусор
  → Ученик обучается на чистых трейсах
```

## Пайплайн дистилляции: teacher → student

```python
# makarsuperstar: дистилляция агентских трейсов (habr 1033434)

import json
import ollama
from dataclasses import dataclass
from typing import Optional

@dataclass
class AgentTrace:
    """
    Структурированный формат агентского трейса.
    Ученик обучается именно этому формату.
    """
    system: str          # системный промпт агента
    messages: list[dict] # история: user/assistant/tool_call
    thought: str         # внутреннее рассуждение агента
    code: str            # сгенерированный код/команда
    tool_calls: list     # вызовы инструментов
    final_answer: str    # итоговый ответ
    verification: str    # проверка ответа перед выдачей


class TeacherDistiller:
    """
    Учитель: Gemma4:31b через Ollama (победил DeepSeek-Coder-v2 и Qwen3.6:27b).
    Среднее качество: 92.0 vs 72.7 у ближайшего конкурента.
    """

    # 5 эталонных трейсов в few-shot — критично для качества
    EXEMPLAR_TRACES: list[AgentTrace] = []  # заполняются вручную

    def distill(self, raw_instruction: str,
                raw_response: str) -> Optional[AgentTrace]:
        """
        Переформатировать сырую пару instruction/response
        в структурированный AgentTrace.
        """
        few_shot_examples = "\n\n".join([
            f"ПРИМЕР {i+1}:\n{json.dumps(t.__dict__, ensure_ascii=False)}"
            for i, t in enumerate(self.EXEMPLAR_TRACES)
        ])

        prompt = f"""Переформатируй instruction/response в структуру агентского трейса.

ЭТАЛОННЫЕ ПРИМЕРЫ:
{few_shot_examples}

ВХОДНЫЕ ДАННЫЕ:
Instruction: {raw_instruction}
Response: {raw_response}

Верни JSON в точно том же формате что в примерах."""

        response = ollama.generate(
            model="gemma4:31b",
            prompt=prompt,
            options={
                "num_ctx": 16384,      # ОБЯЗАТЕЛЬНО: few-shot = 5-7K токенов
                "repeat_penalty": 1.15  # снижает повторения в длинных трейсах
            }
        )

        try:
            trace_dict = json.loads(response["response"])
            return AgentTrace(**trace_dict)
        except (json.JSONDecodeError, TypeError):
            return None
```

## 8-метричный взвешенный валидатор

```python
class TraceValidator:
    """
    Порог: 84.8/100. Фильтрует ~24% примеров.
    Каждая метрика взвешена по важности для качества агента.
    """

    METRICS = {
        # Критические (вес 1.0): без них трейс бесполезен
        "json_parses":                  1.0,  # JSON валиден
        "has_messages":                 1.0,  # есть история сообщений
        "assistant_has_thought_and_code": 1.0, # есть рассуждение и код
        "final_answer_present":         1.0,  # есть итоговый ответ

        # Важные (вес 0.7-0.8)
        "tool_call_present":            0.8,  # вызов инструмента присутствует
        "verification_before_final":    0.7,  # агент проверяет перед ответом

        # Желательные (вес 0.3-0.5)
        "system_present":               0.5,  # есть системный промпт
        "step_count_in_range":          0.3,  # 3-15 шагов (не слишком мало/много)
    }

    THRESHOLD = 84.8  # эмпирически подобран на 10% выборке

    def score(self, trace: AgentTrace) -> float:
        """
        Взвешенная оценка трейса. Возвращает 0-100.
        """
        total_weight = sum(self.METRICS.values())
        weighted_score = 0.0

        checks = {
            "json_parses": trace is not None,
            "has_messages": bool(trace.messages),
            "assistant_has_thought_and_code": bool(trace.thought and trace.code),
            "final_answer_present": bool(trace.final_answer),
            "tool_call_present": bool(trace.tool_calls),
            "verification_before_final": bool(trace.verification),
            "system_present": bool(trace.system),
            "step_count_in_range": 3 <= len(trace.messages) <= 15
        }

        for metric, weight in self.METRICS.items():
            if checks.get(metric, False):
                weighted_score += weight

        return (weighted_score / total_weight) * 100

    def is_valid(self, trace: AgentTrace) -> bool:
        return self.score(trace) >= self.THRESHOLD
```

## Ключевое открытие: domain mismatch

```python
DOMAIN_MISMATCH_EXPERIMENT = {
    "проблема": "Acceptance rate ≠ on-topic quality",

    "Magicoder_датасет": {
        "тип": "алгоритмические задачи (LeetCode-style)",
        "acceptance_rate": "74%",    # валидатор пропускает
        "on_topic_rate":   "38%",    # реально по теме DevOps
        "вывод": "Высокий acceptance при полном domain mismatch"
    },

    "GitHub_трейсы": {
        "тип": "реальные git/CI/CD операции",
        "acceptance_rate": "74%",    # тот же acceptance rate!
        "on_topic_rate":   "95%",    # почти все по теме
        "вывод": "Тот же acceptance rate, но 2.5× лучше on-topic"
    },

    "урок": """
    Валидатор проверяет СТРУКТУРУ трейса, не СОДЕРЖАНИЕ.
    Алгоритмическая задача может иметь идеальную структуру
    agent-трейса, но быть совершенно не о DevOps.

    → Выбор источника данных важнее качества валидатора
    → Domain proximity источника = ключевой гиперпараметр
    """,

    "практический_совет": "Для domain-specific LLM: приоритизировать тематические датасеты, измерять on-topic отдельно от acceptance rate"
}

FINAL_RESULTS = {
    "модель": "oni:base-clean.v2",
    "ученик": "Qwen3:14b",
    "учитель": "Gemma4:31b (avg_score=92.0 vs DeepSeek-Coder-v2=72.7)",
    "датасет": "3899 валидных трейсов из ~5000 сырых",
    "фильтрация": "~24% отброшено валидатором (порог 84.8/100)",
    "качество": "10/10 на боевых тестах (0 галлюцинаций)",
    "источник": "GitHub трейсы (95% on-topic) > Magicoder (38% on-topic)"
}
```

## Полный пайплайн: от сырых данных до обученной модели

```python
class AgentDistillationPipeline:
    """
    End-to-end: сырые данные → обученный агент.
    """

    def run(self, raw_dataset: list[dict],
             output_model: str = "devops-agent-v1") -> dict:

        print(f"Шаг 1: Distillation ({len(raw_dataset)} примеров)")
        distiller = TeacherDistiller()
        validator = TraceValidator()

        valid_traces = []
        stats = {"total": len(raw_dataset), "valid": 0, "filtered": 0}

        for item in raw_dataset:
            trace = distiller.distill(item["instruction"], item["response"])
            if trace and validator.is_valid(trace):
                valid_traces.append(trace)
                stats["valid"] += 1
            else:
                stats["filtered"] += 1

        print(f"  Принято: {stats['valid']}, отфильтровано: {stats['filtered']}")
        print(f"  Acceptance rate: {stats['valid']/stats['total']*100:.1f}%")

        print(f"Шаг 2: Fine-tuning Qwen3:14b на {len(valid_traces)} трейсах")
        # ollama create / mlx-lm / unsloth → обучение ученика
        self.trainer.finetune(
            base_model="qwen3:14b",
            traces=valid_traces,
            output_name=output_model
        )

        return stats
```

## Применение к Lorenzo

```python
# Lorenzo: дистилляция для специализированного knowledge-агента

class LorenzoTraceDistillation:
    """
    Создать Lorenzo-специфичный агент через дистилляцию:
    1. Собрать трейсы: Q&A сессии через improve_llm_qa.py
    2. Учитель переформатирует в agent-JSON
    3. Валидатор фильтрует (8 метрик)
    4. Ученик (малая модель) обучается на трейсах
    → Локальный Lorenzo-агент без API зависимости
    """

    LORENZO_METRICS = {
        # Специфичные для Lorenzo метрики валидации
        "uses_bm25_tool":     1.0,  # агент вызывает поиск
        "has_source_citation": 0.9, # ссылается на источники
        "answer_in_russian":   0.8, # отвечает на русском
        "has_verification":    0.7, # проверяет ответ
    }
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Distillation + LLAMATOR (R33)** | LLAMATOR генерирует атакующие трейсы → дистилляция защитного агента |
| **Distillation + EduLLM (R35)** | Дистилляция образовательных трейсов: учитель демонстрирует педагогику |
| **Distillation + Cognitive Memory (R31)** | Трейсы с памятью: дистилляция memory-aware агентских паттернов |
| **Distillation + ReAct LangGraph (R35)** | LangGraph трейсы → дистилляция компактного ReAct агента |
| **Distillation + Lorenzo Gateway** | Локальный дистиллированный Lorenzo-агент вместо API calls |

## Контакт

- Статья: https://habr.com/ru/articles/1033434/ (май 2026)
- Автор: makarsuperstar (Хабр)
- Ollama: ollama.ai
- Смежная (синтетика граф-анализ, Сбер): https://habr.com/ru/companies/sberbank/articles/909934/
- Смежная (OSS инструменты синтетики, MWS): https://habr.com/ru/companies/mws/articles/932066/
- Смежная (DPO alignment без разметки): https://habr.com/ru/articles/1002298/
