# Structured Output: три уровня надёжности — Instructor, BAML, Outlines

**Автор:** slivka_83  
**Хабр:** https://habr.com/ru/articles/978534/  
**GitHub:** https://github.com/567-labs/instructor (Instructor), https://github.com/dottxt-ai/outlines (Outlines)  
**Слой:** orchestration / analytics  
**Дата:** декабрь 2025  
**Уникальность:** Системная классификация трёх принципиально разных подходов к надёжному structured output: retry-based (Instructor), soft-parsing (BAML), constrained decoding (Outlines). Каждый уровень решает проблему на разном слое стека. Constrained decoding через logit masking даёт 100% гарантию схемы с первой попытки, но требует доступа к логитам (только self-hosted vLLM/Ollama). Дополнено adversarial-тестированием трёх провайдеров (OpenAI/Gemini/xAI) — ни один не поддерживает полный JSON Schema.

## Проблема: LLM не гарантирует JSON

```
Наивный подход: "Верни JSON с полями name и age"
  → LLM: ```json\n{"name": "Иван", "age": "тридцать два"}```
  → age — строка вместо числа
  → Или: {...} с trailing comma → JSON.parse падает
  → Или: правильный JSON, но не все поля

Production реальность:
  → 0.1-5% запросов дают невалидный JSON
  → При 1000 req/day = 1-50 сбоев/день
  → Нужна надёжность: retry / parsing / constraint

Три уровня решений:
  Уровень 1 (Application): Instructor — retry + валидация
  Уровень 2 (Parsing): BAML — умный парсер, прощает ошибки
  Уровень 3 (Sampling): Outlines — логитная маска, 100% гарантия
```

## Уровень 1: Instructor — retry с Pydantic

```python
# Instructor: retry-based structured output
# github.com/567-labs/instructor

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field, field_validator
from typing import Optional

client = instructor.from_openai(OpenAI())

class UserProfile(BaseModel):
    """
    Pydantic схема = контракт вывода.
    field_validator: кастомная валидация + ошибка возвращается в LLM.
    """
    name: str = Field(description="Полное имя пользователя")
    age: int = Field(ge=0, le=150, description="Возраст в годах")
    email: Optional[str] = Field(None, description="Email (если указан)")
    interests: list[str] = Field(
        default_factory=list,
        description="Список интересов"
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v):
        if v and "@" not in v:
            raise ValueError(f"Невалидный email: {v}")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError("Имя слишком короткое")
        return v.strip()


def extract_profile(text: str, max_retries: int = 3) -> UserProfile:
    """
    Instructor: при ValidationError — ошибка + контекст → LLM → повтор.
    Ошибка валидации Pydantic передаётся обратно в LLM как контекст.
    """
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=UserProfile,
        max_retries=max_retries,  # Instructor обрабатывает retry автоматически
        messages=[{
            "role": "user",
            "content": f"Извлеки профиль пользователя из текста:\n{text}"
        }]
    )

# Что происходит при retry:
# 1. LLM возвращает {"age": "32"} → Pydantic: int ожидался, str получен
# 2. Instructor: "Ошибка: age должен быть int, получили str '32'. Исправь."
# 3. LLM исправляет → {"age": 32} → OK
```

## Уровень 2: BAML — мягкий парсер

```python
# BAML (Boundary AI Markup Language): soft JSON parsing
# Прощает типичные ошибки LLM без retry

class BAMLParser:
    """
    BAML парсит "почти-JSON" вывод LLM:
    - Trailing commas: {"a": 1,} → OK
    - Одинарные кавычки: {'name': 'Иван'} → OK
    - Markdown обёртка: ```json{...}``` → OK
    - Комментарии: {"a": 1 // comment} → OK
    - Неполный JSON (если есть все обязательные поля) → OK
    """

    def parse(self, llm_output: str,
               schema: type[BaseModel]) -> BaseModel | None:
        """
        Попытка парсинга с прогрессивным восстановлением.
        """
        # Шаг 1: Прямой JSON.loads
        cleaned = self._clean_markdown(llm_output)
        try:
            return schema(**json.loads(cleaned))
        except (json.JSONDecodeError, ValueError):
            pass

        # Шаг 2: Исправление типичных ошибок
        fixed = self._fix_common_errors(cleaned)
        try:
            return schema(**json.loads(fixed))
        except (json.JSONDecodeError, ValueError):
            pass

        # Шаг 3: Частичное извлечение через regex
        partial = self._extract_fields_by_regex(llm_output, schema)
        if partial:
            return schema(**partial)

        return None  # не смогли распарсить

    def _fix_common_errors(self, text: str) -> str:
        import re
        text = re.sub(r",\s*}", "}", text)      # trailing comma
        text = re.sub(r",\s*]", "]", text)      # trailing comma в массиве
        text = re.sub(r"'", '"', text)           # одинарные кавычки
        text = re.sub(r"//[^\n]*", "", text)     # комментарии
        return text

    def _clean_markdown(self, text: str) -> str:
        """Убрать ```json ... ``` обёртку."""
        import re
        match = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
        return match.group(1).strip() if match else text.strip()
```

## Уровень 3: Outlines — constrained decoding (100% гарантия)

```python
# Outlines: logit masking для 100% гарантии схемы
# github.com/dottxt-ai/outlines
# Требует: self-hosted vLLM или Ollama (доступ к логитам)

import outlines
from outlines import models, generate

# Загрузить модель локально (нужны логиты)
model = models.transformers("mistralai/Mistral-7B-Instruct-v0.2")

def generate_with_constraint(prompt: str,
                               schema: type[BaseModel]) -> BaseModel:
    """
    Constrained decoding: на каждом шаге генерации токена
    логиты маскируются так, чтобы допустить только токены,
    совместимые с JSON Schema.

    Результат: 100% валидный JSON первой попытки.
    Без retry, без парсинга — физически невозможно получить невалидный JSON.
    """
    generator = generate.json(model, schema)
    result = generator(prompt)
    return result

# Поддерживаемые форматы constraint:
CONSTRAINT_TYPES = {
    "json_schema": "Pydantic модель → JSON Schema → logit mask",
    "regex":       "Строгое регулярное выражение (например UUID, дата)",
    "cfg":         "Context-Free Grammar для произвольных форматов",
    "choice":      "Enum из допустимых значений"
}

# Ограничение: только self-hosted модели
# → vLLM поддерживает guided decoding через /generate API
# → Ollama поддерживает format=json (упрощённый вариант)
# → OpenAI API: НЕТ доступа к логитам → Outlines недоступен
```

## Adversarial-тестирование провайдеров (май 2026)

```python
# Mentalitet (habr 1033478): никто не поддерживает полный JSON Schema
# github.com/feodal01/schema-guided-reasoning-pydantic

PROVIDER_COMPARISON = {
    "тестировались": ["gpt-4o-mini", "gemini-2.0-flash", "grok-3-mini"],
    "через": "единый OpenAI-совместимый API",

    "OpenAI": {
        "требует": "strict: true обязателен",
        "не_поддерживает": ["oneOf", "allOf", "anyOf", "if/then/else"],
        "ошибка": "400 при использовании сложных ключевых слов",
        "особенность": "Pydantic-наследование ломает схему"
    },
    "Gemini": {
        "принимает_но_игнорирует": ["minLength", "maxLength", "pattern", "multipleOf"],
        "вывод": "Высокий acceptance rate, но нет constraint enforcement"
    },
    "xAI_Grok": {
        "поддерживает_большинство": True,
        "не_поддерживает": ["allOf"],
        "лучший_из_трёх": True
    },

    "универсальный_вывод": """
    Client-side валидация через Pydantic ValidationError ОБЯЗАТЕЛЬНА
    даже при использовании Structured Outputs провайдеров.
    Provider-side validation ≠ application-level correctness.
    """,

    "рекомендуемая_стратегия": """
    1. Provider Structured Output (если доступен)
    2. + Pydantic validation (всегда)
    3. + Instructor retry (при ValidationError)
    4. Для self-hosted: + Outlines constrained decoding
    """
}

# Матрица выбора подхода:
DECISION_MATRIX = {
    "cloud_api_надёжность": "Instructor (retry + Pydantic)",
    "cloud_api_скорость":   "BAML (soft parsing, без retry)",
    "self_hosted_гарантия": "Outlines (constrained decoding)",
    "смешанный_парк":       "Instructor + Outlines как fallback"
}
```

## Применение к Lorenzo

```python
# Lorenzo: структурированный вывод для improve_llm_qa.py

from pydantic import BaseModel, Field
import instructor

class LorenzoCitedAnswer(BaseModel):
    """
    Структурированный ответ с источниками.
    Instructor гарантирует наличие всех полей.
    """
    answer: str = Field(description="Ответ на вопрос")
    sources: list[str] = Field(
        description="Список файлов-источников",
        min_length=1  # хотя бы 1 источник обязателен
    )
    confidence: float = Field(ge=0.0, le=1.0)
    related_topics: list[str] = Field(default_factory=list)

class LorenzoStructuredQA:
    """
    improve_llm_qa.py + Instructor = надёжный structured output.
    При ошибке валидации → автоматический retry с контекстом ошибки.
    """
    client = instructor.from_openai(OpenAI())

    def ask(self, question: str, docs: list[str]) -> LorenzoCitedAnswer:
        context = "\n\n".join(docs[:5])
        return self.client.chat.completions.create(
            model="claude-haiku-4-5",
            response_model=LorenzoCitedAnswer,
            max_retries=2,
            messages=[{
                "role": "user",
                "content": f"Вопрос: {question}\n\nКонтекст:\n{context}"
            }]
        )
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Outlines + vLLM (R32)** | vLLM guided decoding + Outlines = production constrained generation |
| **Instructor + MAESTRO (R38)** | CARL DAG шаги → Instructor structured output с retry |
| **Structured Output + CV Guard (R37)** | SGR схема для верификации VLM-ответов о геометрии |
| **Instructor + LangFuse (R38)** | Трейсинг retry-цикла Instructor в LangFuse: сколько попыток тратится |
| **Outlines + Lorenzo Gateway** | /api/ask → Outlines constrained decoding для 100% валидных ответов |

## Контакт

- Статья slivka_83: https://habr.com/ru/articles/978534/ (декабрь 2025)
- Статья Mentalitet: https://habr.com/ru/articles/1033478/ (май 2026, adversarial тест)
- Instructor: https://github.com/567-labs/instructor
- Outlines: https://github.com/dottxt-ai/outlines
- Смежная (structured output паттерны, obulygin): https://habr.com/ru/articles/1025172/
- Смежная (function calling OSS модели, MTS AI): https://habr.com/ru/companies/mts_ai/articles/831220/
