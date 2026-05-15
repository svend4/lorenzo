---
date: 2026-05-15
tags: [memory, rag, knowledge, ingestion, architecture]
state: normalized
---

# DerAI: Fine-tuned LLM для SAST — Solar Security против GPT-5 на реальных уязвимостях

<!-- toc-auto -->
<!-- tags: solar-security-derai-sast, docs -->


<!-- summary -->
> Автор: команда Solar Security (Хабр, май 2025) Хабр: https://habr.com/ru/companies/solarsecurity/articles/1031718/
Хабр: https://habr.com/ru/companies/solarsecurity/articles/1031718/  
GitHub: не опубликован (проприетарная система)  
Слой: orchestration / analytics / security  
Дата: май 2025  
Уникальность: Solar


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** команда Solar Security (Хабр, май 2025)  
**Хабр:** https://habr.com/ru/companies/solarsecurity/articles/1031718/  
**GitHub:** не опубликован (проприетарная система)  
**Слой:** orchestration / analytics / security  
**Дата:** май 2025  
**Уникальность:** Solar Security обучили собственную LLM DerAI на 7-летней базе реальных уязвимостей из SAST-продукта Solar appScreener. Два модуля: DerTriage (классификация) + DerCodeFix (генерация патчей). Сравнение с GPT-5.2, DeepSeek 3.2, GigaChat на 12 000 реальных находок — DerAI выиграла за счёт доменной экспертизы, а не масштаба модели.

## Архитектура DerAI

```
Solar appScreener (SAST):
  ↓ 12 000+ уязвимостей (Java, Python)
  ↓ 7 лет размеченных данных

DerAI система (два модуля):
  ┌─────────────────────┐
  │   DerTriage         │  Классификация: false positive или real?
  │   (фильтрация)      │  Input: SAST finding + code context
  │                     │  Output: confirmed/dismissed + reasoning
  └──────────┬──────────┘
             ↓ только confirmed уязвимости
  ┌──────────┴──────────┐
  │   DerCodeFix        │  Генерация патча для реальной уязвимости
  │   (исправление)     │  Input: vulnerable code + CWE + severity
  │                     │  Output: fixed code + explanation
  └─────────────────────┘
```

## Почему fine-tuning победил GPT-5.2

```python
# Бенчмарк Solar Security (20 реальных проектов, ~12K находок)

BENCHMARK_RESULTS = {
    "DerAI (fine-tuned Solar)": {
        "precision": 0.91,
        "recall": 0.87,
        "f1": 0.89,
        "false_positive_reduction": "73%",
        "advantage": "знает специфику appScreener: как именно находки формируются"
    },
    "GPT-5.2 (zero-shot)": {
        "precision": 0.78,
        "recall": 0.81,
        "f1": 0.79,
        "false_positive_reduction": "51%",
        "weakness": "не знает контекст SAST-инструмента, галлюцинирует паттерны"
    },
    "DeepSeek-v3.2 (zero-shot)": {
        "precision": 0.74,
        "recall": 0.76,
        "f1": 0.75,
        "false_positive_reduction": "44%"
    },
    "GigaChat (few-shot)": {
        "precision": 0.71,
        "recall": 0.68,
        "f1": 0.69,
        "false_positive_reduction": "38%"
    }
}

# Вывод: специализированная маленькая модель > GPT-5 в узкой задаче
# Ключ: 7 лет размеченных данных = несравнимый тренировочный набор
```

## DerTriage: классификация уязвимостей

```python
# Упрощённый промпт DerTriage

TRIAGE_PROMPT = """
Ты — эксперт по анализу результатов SAST-сканирования.

Находка от Solar appScreener:
  CWE: {cwe_id} ({cwe_name})
  Уязвимый код:
  ```{language}
  {vulnerable_code}
  ```
  Контекст: {code_context}
  Правило срабатывания: {rule_description}

Задача: определить является ли это реальной уязвимостью или false positive.

Критерии для false positive:
  - Данные приходят только из доверенного источника
  - Уязвимость недостижима через публичный интерфейс
  - Санитизация выполняется в вызывающем коде
  - Тестовый или mock-код

Формат ответа:
{{
  "verdict": "real" | "false_positive",
  "confidence": 0.0-1.0,
  "reasoning": "...",
  "evidence": ["...", "..."]
}}
"""

class DerTriage:
    def classify(self, finding: SASTFinding) -> TriageResult:
        response = self.llm.generate(
            TRIAGE_PROMPT.format(
                cwe_id=finding.cwe,
                cwe_name=finding.cwe_name,
                language=finding.language,
                vulnerable_code=finding.code_snippet,
                code_context=finding.context,
                rule_description=finding.rule
            )
        )
        return TriageResult(**parse_json(response))
```

## DerCodeFix: генерация патча

```python
# Паттерн генерации исправления

CODEFIX_PROMPT = """
Уязвимость подтверждена: {cwe_id} — {cwe_name}
Severity: {severity}

Уязвимый код:
```{language}
{vulnerable_code}
```

Правила исправления для {cwe_id}:
{remediation_rules}  # из базы знаний Solar

Сгенерируй минимальное исправление:
1. Не меняй логику, только устрани уязвимость
2. Добавь комментарий почему именно так
3. Если нужны импорты — укажи

Формат:
{{
  "fixed_code": "...",
  "explanation": "...",
  "imports_needed": [...],
  "breaking_changes": false
}}
"""

class DerCodeFix:
    def generate_patch(self, finding: SASTFinding, triage: TriageResult) -> Patch:
        if triage.verdict != "real":
            return None

        rules = self.remediation_db.get_rules(finding.cwe)
        response = self.llm.generate(
            CODEFIX_PROMPT.format(
                cwe_id=finding.cwe,
                cwe_name=finding.cwe_name,
                severity=finding.severity,
                language=finding.language,
                vulnerable_code=finding.code_snippet,
                remediation_rules=rules
            )
        )
        return Patch(**parse_json(response))
```

## Pipeline в SAST-процессе

```
1. Solar appScreener → 12,000 находок за CI-прогон

2. DerTriage (batch):
   → 8,760 dismissed (false positives, -73%)
   → 3,240 confirmed (реальные уязвимости)

3. DerCodeFix (на confirmed):
   → Автоматические патчи для 2,890 случаев
   → 350 сложных — на ревью к эксперту

4. Developer workflow:
   → MR/PR: автоматически + патч
   → Accept / Modify / Reject
   → Обратная связь → дообучение DerAI
```

## Датасет и обучение

```python
TRAINING_DATA = {
    "source": "Solar appScreener findings (2018-2025)",
    "size": "85,000+ размеченных находок",
    "languages": ["Java", "Python", "JavaScript", "C#", "Go"],
    "labels": {
        "real_vulnerabilities": 0.31,   # 31% реальные
        "false_positives": 0.69         # 69% ложные
    },
    "annotation": "security engineers (7 лет ревью)",
    "cwe_coverage": "top-25 CWE + специфика appScreener"
}

TRAINING_CONFIG = {
    "base_model": "закрыто (proprietary)",
    "technique": "supervised fine-tuning + RLHF от security engineers",
    "train_test_split": "80/20",
    "validation": "реальные проекты клиентов (с согласия)"
}

# Ключевое преимущество:
# Не просто "код + CWE", а "код + как именно appScreener его нашёл"
# → модель знает паттерны ложных срабатываний конкретного инструмента
```

## Применение к Lorenzo

Lorenzo + SAST паттерн → **LLM-верификация документации**:

```python
# improve_doc_triage.py (паттерн от DerTriage):
# Вместо SAST находок → Lorenzo находит потенциальные проблемы в документах

class DocumentTriage:
    """Классифицирует проблемы в документах: реальная или ложная тревога"""

    def classify_issue(self, issue: ContentIssue) -> TriageResult:
        # Аналог DerTriage: стоит ли беспокоиться о противоречии/дубле?
        verdict = self.llm.generate(f"""
        Проблема в документации: {issue.type}
        Контекст: {issue.context}
        
        Это реальная проблема или ложная тревога?
        (Аналог: improve_contradiction_check.py находит "противоречия",
         но многие — нормальная эволюция взглядов, не ошибка)
        """)
        return TriageResult(verdict=verdict)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **DerAI + Prompt Injection (R23)** | SAST для LLM-приложений: поиск инъекций в промптах как CWE |
| **DerAI + LLM AppSec (R22)** | Defense-in-depth: SAST + runtime LLM защита = два слоя |
| **DerAI + LLM Router (R20)** | Роутинг: DerTriage (fast/cheap) → DerCodeFix только при confirmed |
| **DerAI + Fine-tuning (R24)** | Дистилляция: маленькая узкоспециализированная модель > GPT в задаче |
| **DerAI + CAVM (R26)** | CAVM пайплайн: SAST → Triage → Fix → Report автоматически |

## Контакт

- Статья: https://habr.com/ru/companies/solarsecurity/articles/1031718/ (май 2025)
- Solar appScreener: https://solarsecurity.ru/products/solar_appscreener/
- Смежная (LLM AppSec R22): https://habr.com/ru/companies/solarsecurity/articles/
- Смежная (Semgrep + LLM): статьи о статическом анализе с AI на Хабре

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
