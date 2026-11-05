---
date: 2026-06-05
tags: [orchestration, security, ingestion, architecture, self-improve]
state: normalized
---

# MTS: автоматическое LLM-ревью кода в GitLab CI/CD через n8n + Ollama

<!-- toc-auto -->
<!-- tags: mts-evgzor-llm-code-review-gitlab-n8n-ollama, docs -->


<!-- summary -->
> `mts-evgzor-llm-code-review-gitlab-n8n-ollama` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** evgzor (Евгений Зорин, MTS Future Crew)  
**Хабр:** https://habr.com/ru/companies/ru_mts/articles/876482/  
**GitHub:** нет (архитектура описана детально)  
**Слой:** orchestration  
**Дата:** январь 2025  
**Уникальность:** Production LLM code review интегрированный в GitLab CI/CD через webhooks: n8n (no-code оркестратор) + Ollama (локальный LLM) + GitLab inline comments API. Бенчмарк 4 моделей на реальном enterprise-железе (A100 80GB): Codeqwen:7b, Deepseek-coder:33b, Llama3, ChatGPT. Codeqwen побеждает по quality/speed tradeoff (~5 мин/MR). Прогноз: -20-40% времени ревью, -15-30% ошибок.

## Проблема: код-ревью — узкое место CI/CD

```
Типичный GitLab CI/CD workflow:
  → Разработчик создаёт MR (Merge Request)
  → Ожидает reviewer → 24-48 часов (peak load)
  → Reviewer читает diff вручную → субъективно, устаёт
  → Комментарии: смешано важное и тривиальное
  → 20-40% времени ревью: стиль + именование (автоматизируемо)

MTS контекст:
  → 32 тысячи разработчиков (крупнейший телеком РФ)
  → Тысячи MR в день → bottleneck у senior reviewers
  → Swift (iOS) → Kotlin → Java → большой разнобой языков

Решение: LLM как first-pass reviewer
  → Автоматические комментарии в GitLab на уровне diff
  → Senior reviewer видит уже отфильтрованный MR
  → Экономия: 20-40% времени → senior занимается архитектурой
```

## n8n + GitLab webhook: pipeline без единой строки инфраструктурного кода

```python
# evgzor (MTS): LLM code review в GitLab CI/CD
# habr.com/ru/companies/ru_mts/articles/876482

# Архитектура pipeline описана через n8n workflow (no-code)
# Здесь — Python-эквивалент для понимания логики

from dataclasses import dataclass
from typing import Optional
import httpx
import json

@dataclass
class MergeRequestEvent:
    """Событие GitLab MR (приходит через webhook)."""
    project_id: int
    mr_iid: int          # internal ID в проекте
    source_branch: str
    target_branch: str
    title: str
    author: str

@dataclass
class FileDiff:
    """Изменения одного файла в MR."""
    file_path: str
    language: str
    old_content: str
    new_content: str
    diff: str            # unified diff
    lines_added: int
    lines_removed: int

@dataclass
class ReviewComment:
    """Inline comment к конкретной строке файла."""
    file_path: str
    line: int
    body: str
    severity: str  # "info" | "warning" | "error"


class GitLabLLMReviewer:
    """
    Полный pipeline: GitLab MR → diff → LLM → inline comments.
    Оркестрация: n8n workflow (визуальный, без кода деплоя).
    LLM: Ollama (локальный, данные не покидают инфраструктуру).
    """

    N8N_WORKFLOW_STEPS = [
        "1. GitLab webhook trigger (MR opened/updated)",
        "2. HTTP node: GitLab API → получить diff MR",
        "3. Code node: парсинг diff по файлам",
        "4. HTTP node: Ollama API → LLM анализ каждого файла",
        "5. Code node: парсинг LLM ответа → structured comments",
        "6. HTTP node: GitLab API → post inline comments"
    ]

    def __init__(self, gitlab_url: str, gitlab_token: str,
                  ollama_url: str, model: str = "codeqwen:7b"):
        self.gitlab = httpx.AsyncClient(
            base_url=gitlab_url,
            headers={"PRIVATE-TOKEN": gitlab_token}
        )
        self.ollama_url = ollama_url
        self.model = model

    async def process_merge_request(self, event: MergeRequestEvent) -> list[ReviewComment]:
        """
        Основной pipeline: MR → LLM review → comments.
        """
        # Шаг 1: получить diff
        diffs = await self._fetch_mr_diffs(event.project_id, event.mr_iid)

        # Шаг 2: обогатить контекст (README, .editorconfig, style guide)
        context = await self._fetch_project_context(event.project_id)

        # Шаг 3: анализ каждого файла отдельно (параллельно)
        import asyncio
        review_tasks = [
            self._review_file(diff, context)
            for diff in diffs
            if self._should_review(diff)
        ]
        file_reviews = await asyncio.gather(*review_tasks)

        # Шаг 4: сгладить + дедuplicate comments
        all_comments = [c for review in file_reviews for c in review]
        deduped = self._dedup_comments(all_comments)

        # Шаг 5: опубликовать в GitLab
        await self._post_inline_comments(event.project_id, event.mr_iid, deduped)

        return deduped

    def _should_review(self, diff: FileDiff) -> bool:
        """Фильтровать файлы: не ревьювать generated код, migrations, lock-файлы."""
        skip_patterns = [
            "*.generated.swift", "*.pb.swift",  # protobuf generated
            "Podfile.lock", "Package.resolved",  # lock files
            "*/Migrations/*",                     # DB migrations
        ]
        from fnmatch import fnmatch
        return not any(fnmatch(diff.file_path, p) for p in skip_patterns)

    async def _review_file(self,
                             diff: FileDiff,
                             context: dict) -> list[ReviewComment]:
        """
        LLM ревью одного файла.
        Промпт структурирован под язык (Swift vs Kotlin vs Python).
        """
        prompt = self._build_review_prompt(diff, context)

        response = await httpx.AsyncClient().post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,  # детерминированный → воспроизводимо
                    "num_predict": 2048
                }
            }
        )

        raw_review = response.json()["response"]
        return self._parse_structured_comments(raw_review, diff.file_path)

    def _build_review_prompt(self, diff: FileDiff, context: dict) -> str:
        """
        Промпт для ревью: diff + style guide + правила команды.
        Структурированный output: JSON с комментариями.
        """
        return f"""Ты — опытный {diff.language} разработчик, проводишь code review.

Правила команды: {context.get('style_guide', 'стандартные')}

Diff для ревью:
```diff
{diff.diff}
```

Проверь:
1. Потенциальные баги и ошибки
2. Нарушения style guide команды
3. Производительность и оптимизация
4. Читаемость и maintainability
5. Покрытие тестами (если нужно)

Верни JSON массив комментариев:
[{{"line": <номер_строки>, "severity": "error|warning|info", "comment": "<текст>"}}]

Только конкретные, actionable комментарии. Не хвали хороший код."""
```

## Бенчмарк 4 моделей на A100

```python
MODEL_BENCHMARK = {
    "hardware": {
        "cpu": "32-core",
        "ram": "160 GB",
        "gpu": "NVIDIA A100 80GB",
        "deployment": "On-premise (данные не покидают MTS)"
    },

    "models_tested": {
        "Codeqwen:7b": {
            "avg_time_per_mr": "~5 мин",
            "quality": "Высокое (код-специализированная)",
            "verdict": "✅ WINNER — лучший quality/speed tradeoff"
        },
        "Deepseek-coder:33b": {
            "avg_time_per_mr": "~8.5 мин",
            "quality": "Высокое",
            "verdict": "⚠️ Медленнее, не всегда оправдано"
        },
        "Llama3:latest": {
            "avg_time_per_mr": "~1.5 мин",
            "quality": "Среднее (общая модель)",
            "verdict": "⚠️ Быстрая, но меньше code-специфичных insights"
        },
        "ChatGPT (baseline)": {
            "avg_time_per_mr": "~30 сек (API)",
            "quality": "Высокое",
            "verdict": "📊 Baseline, но данные уходят в облако"
        }
    },

    "projected_metrics": {
        "review_time_reduction": "20-40%",
        "error_detection_improvement": "15-30%",
        "senior_reviewer_time_saved": "На тривиальных замечаниях"
    }
}

N8N_ADVANTAGES = {
    "visual_workflow": "Pipeline виден наглядно, редактируется без кода",
    "no_infra_code": "Нет Airflow/Prefect/Luigi — всё в одном инструменте",
    "webhook_native": "GitLab webhook → trigger из коробки",
    "error_handling": "Retry логика встроена в n8n nodes",
    "observability": "Execution history и logs в n8n UI"
}
```

## Применение к Lorenzo

```python
# Lorenzo: LLM code review паттерн для scripts/ качества

class LorenzoScriptReviewer:
    """
    evgzor паттерн для Lorenzo:
    Автоматический review новых improve_*.py скриптов.
    При git commit → webhook → LLM анализ → comments в PR.
    Проверять: соответствие шаблону скрипта, docstring, main-блок.
    """

    LORENZO_REVIEW_RULES = """
Правила скриптов Lorenzo:
- Каждый скрипт должен иметь if __name__ == '__main__': блок
- Обязателен docstring с описанием функции
- Скрипт должен поддерживать --dry-run флаг (если меняет файлы)
- Нет хардкоженых путей — только относительно docs/
- Логирование через print(), не logging (для согласованности)
"""

    async def review_new_script(self, diff: FileDiff) -> list[ReviewComment]:
        """Проверить новый improve_*.py на соответствие Lorenzo стандартам."""
        reviewer = GitLabLLMReviewer(
            gitlab_url="http://localhost",
            gitlab_token="",
            ollama_url="http://localhost:11434",
            model="codeqwen:7b"
        )
        context = {"style_guide": self.LORENZO_REVIEW_RULES}
        return await reviewer._review_file(diff, context)
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM Code Review + Code MCP (R46)** | EvgeniyRasyuk архитектурный граф + MTS LLM review = понимает зависимости при ревью |
| **LLM Code Review + SENTINEL (R47)** | SENTINEL проверяет промпты ревьювера: нет injection через вредоносный diff |
| **LLM Code Review + LangGraph (R44)** | LangGraph граф: fetch_diff → analyze → comment → re-analyze если score низкий |
| **LLM Code Review + LangFuse (R38)** | Трейсинг каждого ревью: какие правила нарушаются чаще, какая модель точнее |
| **LLM Code Review + SWE-MERA (R41)** | SWE-MERA как benchmark для LLM code reviewer: измерить качество найденных багов |

## Контакт

- Статья: https://habr.com/ru/companies/ru_mts/articles/876482/ (январь 2025)
- Автор: evgzor (Евгений Зорин, MTS Future Crew)
- n8n: n8n.io (open-source workflow automation)
- Ollama: ollama.ai (local LLM runner)
- Codeqwen: huggingface.co/Qwen/CodeQwen1.5-7B
- Смежная (SherlockOps SRE, R42): docs/06-discovery/round-42/projects/sherlockops-llm-alert-investigation-devops.md
- Смежная (LLM DevSecOps, R34): docs/06-discovery/round-34/
- Смежная (Code MCP архитектурное зрение, R46): docs/06-discovery/round-46/projects/evgeniyrasuk-mcp-codebase-architectural-vision.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
