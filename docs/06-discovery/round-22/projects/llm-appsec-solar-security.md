---
date: 2026-05-15
tags: [rag, orchestration, security, architecture, anthropic]
state: normalized
---

# LLM в AppSec — исследование Solar Security: специализированные vs общие модели

<!-- toc-auto -->
<!-- tags: llm-appsec-solar-security, docs -->


<!-- summary -->
> Результаты (20 приложений Java + Python) Почему общие LLM плохи для SAST-сортировки
 
Методология
 
Результаты (20 приложений Java + Python)
 
Почему общие LLM плохи для SAST-сортировки
 
AI для AppSec: что реально работает
 
Вайбкод + Security паттерн (смежная статья R22)
 
DerAI в Solar appScreener
 
Применение


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** команда Solar Security (российская компания кибербезопасности)  
**Хабр:** https://habr.com/ru/companies/solarsecurity/articles/1031718/  
**GitHub:** не опубликован (исследование + Solar appScreener с AI-плагином)  
**Слой:** orchestration / quality / knowledge  
**Дата:** май 2026  
**Уникальность:** Первое публичное российское исследование применения LLM в Application Security: 20 приложений (Java + Python), сравнение общих LLM vs специализированной DerAI-модели внутри SAST-инструмента. Вывод: общие LLM (ChatGPT, Claude) бесполезны для сортировки SAST-алертов — нужны специализированные, встроенные в контекст анализатора.

## Задача исследования

```
Проблема SAST в 2026:
  SAST-инструменты (SonarQube, Semgrep, AppScreener) → тысячи алертов
  80-90% алертов = false positives
  AppSec инженер тратит недели на ручную сортировку

Гипотеза: LLM может автоматически сортировать алерты
  (true positive / false positive / требует исправления)

Эксперимент: 20 приложений Java + Python
  → запустить SAST → получить алерты → подать в LLM → сравнить с ручным анализом
```

## Методология

```python
# Один алерт = один запрос к LLM:
TRIAGE_PROMPT = """
Ты — опытный AppSec инженер. Оцени уязвимость:

Тип: {vuln_type}  (e.g., SQL Injection, XSS, SSRF)
Описание: {vuln_description}
Уязвимый код:
{code_snippet}
Контекст (вызывающий код):
{caller_context}
Трассировка данных: {data_flow}

Вопросы:
1. Это True Positive или False Positive?
2. Критичность (CRITICAL/HIGH/MEDIUM/LOW)?
3. Как исправить?
"""

# Тестируемые модели:
models_tested = [
    "gpt-4o",          # OpenAI общая
    "claude-sonnet",   # Anthropic общая
    "gemini-1.5-pro",  # Google общая
    "DerAI",           # специализированная (Solar appScreener)
]
```

## Результаты (20 приложений Java + Python)

```
Метрика: точность определения True/False Positive

GPT-4o:           67% точность  | много False Negatives
Claude Sonnet:     71% точность  | хорошие объяснения, но не хватает контекста
Gemini 1.5 Pro:   64% точность  | слабо на Java
DerAI (Solar):    89% точность  | ✅ встроен в контекст SAST

Причина победы DerAI:
  → обучена на реальных SAST алертах с разметкой TP/FP
  → получает не только код, но и AST, граф вызовов, data flow
  → знает паттерны False Positive конкретных правил appScreener
```

## Почему общие LLM плохи для SAST-сортировки

```
Проблема 1: Нет SAST-контекста
  Общая LLM видит только код-фрагмент
  DerAI видит: код + AST + call graph + data flow + правило SAST

Проблема 2: Нет обратной связи
  Общая LLM не знает, что в этой кодовой базе уже было TP/FP
  DerAI обучена на реальных разметках от AppSec инженеров

Проблема 3: Галлюцинации в security контексте опасны
  "Это False Positive" → пропустить реальную уязвимость
  В медицине и security цена ошибки высока
```

## AI для AppSec: что реально работает

```
✅ РАБОТАЕТ:
  - Сортировка алертов (triage) специализированной моделью
  - Генерация fix-patch для найденной уязвимости (LLM знает паттерны)
  - Объяснение уязвимости разработчику (образовательная функция)
  - Поиск похожих уязвимостей в репозитории (embeddings)

❌ НЕ РАБОТАЕТ (пока):
  - Замена классического SAST (LLM не читает весь проект)
  - Самостоятельный поиск 0-day без правил
  - Точная оценка критичности без бизнес-контекста
```

## Вайбкод + Security паттерн (смежная статья R22)

```
Проблема 2026: vibe coding → LLM пишет код быстро → security debt
        ↓
Решение: LLM-Security CI/CD pipeline
  commit → SAST (Semgrep) → DerAI triage → только TP-алерты → разработчик

Алерт с AI-контекстом:
  "Найдена SQL Injection в users.py:45
   Data flow: request.args['id'] → cursor.execute(...)
   Fix: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))
   Похожие исправленные ранее: [список PRs]"
```

## DerAI в Solar appScreener

```
Solar appScreener = SAST для Java, Kotlin, Python, Go, C#, PHP
DerAI = AI-плагин внутри appScreener:
  → в 10× ускоряет разработку (по данным Solar)
  → сортирует алерты: Critical/High/Medium/Low/FP
  → генерирует fix recommendations прямо в IDE
  → интеграция: GitLab CI, GitHub Actions, Jenkins
```

## Применение к Lorenzo

Lorenzo имеет `improve_ci_config.py` и `improve_pre_commit.py`.  
AppSec паттерн = добавить security layer к CI:

```yaml
# .github/workflows/security.yml
- name: SAST Scan
  uses: returntocorp/semgrep-action@v1
  with:
    config: p/python p/security-audit

- name: LLM Security Triage
  run: python scripts/improve_security_triage.py --report semgrep-report.json
  # → подать алерты в LLM → отфильтровать FP → создать GitHub Issues только для TP
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **AppSec + AI Review (R15)** | AI Review (code quality) + DerAI (security) = полный quality gate |
| **AppSec + LLM Tests (R20)** | Mutation tests + security triage = defence-in-depth pipeline |
| **AppSec + Langfuse (R13)** | Langfuse трейсит каждый security triage — видна точность DerAI |
| **AppSec + Reasoning (R20)** | Reasoning-модель для КРИТИЧЕСКИХ алертов (thinking перед решением) |
| **AppSec + No-LangChain (R16)** | agent=triage_function, graph=severity_workflow без фреймворка |

## Контакт

- Статья: https://habr.com/ru/companies/solarsecurity/articles/1031718/ (май 2026)
- Solar appScreener: solargroup.ru/products/solar-appscreener
- Смежная (LLM-пентест 2026): https://habr.com/ru/articles/1031380/
- Смежная (Вайбкод + безопасность): https://habr.com/ru/companies/ruvds/articles/1017858/
- Semgrep (OSS SAST): github.com/returntocorp/semgrep (LGPL)

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
