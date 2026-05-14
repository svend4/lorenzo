# YooMoney: LLM-скрининг резюме — -70% ручного труда HR

**Автор:** команда YooMoney (Хабр, январь 2026)  
**Хабр:** https://habr.com/ru/companies/yoomoney/articles/986874/  
**GitHub:** не опубликован (внутренний инструмент, архитектура описана)  
**Слой:** orchestration / analytics / knowledge  
**Дата:** январь 2026  
**Уникальность:** Первый публичный российский кейс автоматизации полного цикла найма с LLM: от получения резюме в CRM до ранжированного списка кандидатов. Ключевое: Gemma-3 (локально, данные не покидают контур), -70% ручного труда HRBP, интеграция в существующую CRM-R без замены процессов.

## Задача и контекст

```
Боль HR: до 80% рабочего времени HRBP = первичный анализ резюме
  → сотни откликов → ручная оценка hard/soft скиллов → ранжирование

Требования:
  1. Данные кандидатов не покидают YooMoney (privacy compliance)
  2. Интеграция в CRM-R (существующая система)
  3. Структурированный вывод для HRBP
  4. Работа без GPU-кластера (on-premise сервер)
```

## Архитектура системы

```
Новое резюме → CRM-R
      ↓
LLM Screening Service (Gemma-3, локально)
      ↓
  Этап 1: Извлечение структуры
    → имя, навыки, опыт, образование, проекты
    → JSON структура (без галлюцинаций — только факты из текста)
      ↓
  Этап 2: Сопоставление с вакансией
    → запрос вакансии из CRM-R (JD: требования + nice-to-have)
    → оценка каждого требования: ✅ соответствует / ❌ не соответствует / ❓ неясно
      ↓
  Этап 3: Итоговый скор + объяснение
    → relevance_score (0–100)
    → strengths: ["5 лет Python", "опыт распределённых систем"]
    → gaps: ["нет опыта Kubernetes", "soft skills не описаны"]
    → recommendation: "PRIORITY / REVIEW / SKIP"
      ↓
CRM-R: ранжированный список → HRBP
```

## Промпт для скрининга

```python
SCREENING_PROMPT = """
Ты — опытный технический рекрутер. Оцени резюме кандидата
относительно требований вакансии.

## Вакансия:
{job_description}

## Резюме:
{resume_text}

## Задача:
1. Извлеки ключевые навыки кандидата (только то, что есть в тексте)
2. Сопоставь с каждым требованием вакансии
3. Вычисли общий скор соответствия

Отвечай строго в JSON:
{{
  "skills_found": ["Python", "PostgreSQL", ...],
  "requirements_match": [
    {{"req": "5+ лет Python", "match": true, "evidence": "6 лет в Tinkoff"}},
    {{"req": "Kubernetes", "match": false, "evidence": null}},
  ],
  "relevance_score": 78,
  "recommendation": "PRIORITY",
  "strengths": ["..."],
  "gaps": ["..."]
}}
"""
```

## Ключевые результаты

```
До внедрения:
  HRBP время на скрининг: до 80% рабочего дня
  Среднее время на 1 резюме: ~8 минут
  Субъективность: высокая (устал → пропущен кандидат)

После внедрения:
  Ручной труд HR: -70%
  Время скрининга LLM: ~15 секунд на резюме
  Согласованность: стабильная (одинаковые критерии для всех)
  Privacy: 100% — Gemma-3 работает on-premise, данные не выходят
```

## Выбор модели: почему Gemma-3

```
Варианты рассматривались:
  Claude / GPT-4o:   лучшее качество, но данные → облако (не соответствует политике)
  LLaMA 3.1:8b:     хорошо EN, слабее RU резюме
  Qwen2.5:7b:       хорошо RU, но нестабильный JSON output
  Gemma-3 ✅:        Google, хорошее RU + EN, стабильный JSON через grammar sampling

Деплой: 1 GPU-сервер on-premise, Ollama + grammar_sampling для JSON
```

## Интеграция с CRM-R

```python
# Webhook из CRM-R при новом резюме:
@app.post("/screen-resume")
async def screen_resume(resume_id: str, vacancy_id: str):
    resume_text = crm.get_resume(resume_id)
    job_desc = crm.get_vacancy(vacancy_id)

    result = llm_screen(resume_text, job_desc)  # Gemma-3 local

    # Обновить CRM-R:
    crm.update_candidate(
        resume_id,
        score=result["relevance_score"],
        recommendation=result["recommendation"],
        strengths=result["strengths"],
        gaps=result["gaps"]
    )
    # Теперь HRBP видит ранжированный список автоматически
```

## Bias Awareness

```
Проблема bias в HR-AI (упомянута в статье):
  → LLM может воспроизводить паттерны прошлых найма (если обучена на них)
  → Галлюцинации: "кандидат умеет X" — если X не в резюме

Меры YooMoney:
  → Только факты из резюме (prompt: "только то, что есть в тексте")
  → evidence обязательное поле (цитата из резюме или null)
  → HRBP не видит только скор — видит объяснение и evidence
  → Финальное решение всегда за человеком
```

## Применение к Lorenzo

Lorenzo имеет `improve_llm_enrich.py` для обогащения документов.  
HR-скрининг паттерн = **Document Relevance Analysis** для любых документов:

```python
# improve_doc_relevance.py (паттерн из YooMoney):
def score_doc_relevance(doc_path: str, query_criteria: dict) -> RelevanceReport:
    """Оценить документ относительно набора критериев"""
    text = read_doc(doc_path)

    result = llm_client.score_against_criteria(
        text=text,
        criteria=query_criteria,  # как JD в HR
        require_evidence=True,     # цитаты из текста (anti-hallucination)
        output_format="json"
    )
    # Применение: поиск проектов для коллаборации по критериям Svyazi
    # "Найти файлы, соответствующие 'memory + Russian NLP + open-source'"
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **HR Screening + LLM Router (R20)** | Haiku для bulk-скрининга, Sonnet только для финалистов |
| **HR Screening + Jay Guard (R21)** | Анонимизировать ФИО/паспорт → LLM → деанонимизировать (ФЗ-152) |
| **HR Screening + Docling (R19)** | PDF резюме → Docling таблицы опыта → LLM оценка |
| **HR Screening + Contract Analysis (R22)** | Трудовой договор → тот же Risk Analysis паттерн |
| **HR Screening + Desmond (R19)** | Webhook → LLM скрининг → structured report в Jira/Confluence |

## Контакт

- Статья: https://habr.com/ru/companies/yoomoney/articles/986874/ (январь 2026)
- Смежная (HR Tech Россия 2026): https://habr.com/ru/articles/1005150/
- Смежная (AI-инструменты для HR топ-10): https://habr.com/ru/companies/bothub/articles/971014/
- Gemma-3: github.com/google-deepmind/gemma (Apache 2.0)
- Ollama grammar sampling: ollama.com/docs/api#structured-outputs
