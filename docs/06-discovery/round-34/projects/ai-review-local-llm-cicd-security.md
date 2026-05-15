---
date: 2026-05-15
tags: [memory, orchestration, security, knowledge, ingestion]
state: normalized
---

# AI Review кода: локальная LLM в CI/CD за 30 минут

<!-- toc-auto -->
<!-- tags: ai-review-local-llm-cicd-security, docs -->


<!-- summary -->
> Особенно ценно для регулируемых отраслей и on-premise сред, где исходный код не должен покидать инфраструктуру.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** sound_right (Никита Филонов)  
**Хабр:** https://habr.com/ru/articles/953598/  
**GitHub:** https://github.com/Nikita-Filonov/ai-review  
**GitHub (example workflow):** https://github.com/Nikita-Filonov/test-ai-review  
**Слой:** orchestration / cicd  
**Дата:** октябрь 2025  
**Уникальность:** Полностью локальный AI code review без передачи кода внешним API: Ollama (Mistral/Llama3/CodeLlama/Phi3) интегрирован в GitHub Actions, модель скачивается прямо в runner, итоговые комментарии постятся inline в PR. Особенно ценно для регулируемых отраслей и on-premise сред, где исходный код не должен покидать инфраструктуру.

## Проблема: AI Code Review = утечка кода

```
Стандартный AI code review:
  PR → GitHub Actions → OpenAI/Anthropic API → код уходит за периметр
  → Нарушение NDA / требований compliance / 152-ФЗ

Решение Никиты Филонова:
  PR → GitHub Actions → Ollama (local в runner) → inline PR комментарии
  → Данные не покидают репозиторий
  → Настройка: 30 минут
  → Стоимость: $0 (inference на self-hosted runner)
```

## Архитектура: Ollama + GitHub Actions

```yaml
# .github/workflows/ai-review.yml
# Источник: github.com/Nikita-Filonov/test-ai-review

name: AI Code Review

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  ai-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # нужен diff с base branch

      - name: Install Ollama
        run: |
          curl -fsSL https://ollama.com/install.sh | sh
          ollama serve &

      - name: Pull model
        run: |
          # Выбор модели: mistral (7B) для баланса скорость/качество
          # Альтернативы: codellama, phi3, llama3, deepseek-coder
          ollama pull mistral:7b

      - name: Run AI Review
        uses: Nikita-Filonov/ai-review@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model: mistral:7b
          ollama_url: http://localhost:11434
          # Опционально:
          # max_files: 10           # лимит файлов
          # focus: security         # фокус ревью
          # language: ru            # язык комментариев
```

## Ядро инструмента: diff → Ollama → PR комментарии

```python
# Упрощённая логика ai-review (github.com/Nikita-Filonov/ai-review)

import os
import requests
from github import Github

class AIReviewer:
    """
    1. Получить diff из PR
    2. Разбить на чанки (per-file)
    3. Отправить каждый чанк в Ollama
    4. Постить inline комментарии через GitHub API
    """

    REVIEW_PROMPT = """Ты — опытный senior разработчик, проводишь code review.
Проанализируй следующий diff и дай конкретные замечания:

1. Баги и потенциальные ошибки
2. Проблемы безопасности (SQL injection, XSS, hardcoded secrets и т.д.)
3. Нарушения принципов SOLID/DRY
4. Улучшения производительности

Diff:
{diff}

Файл: {filename}

Отвечай кратко и по делу. Если замечаний нет — скажи "LGTM"."""

    def __init__(self):
        self.ollama_url = os.environ["OLLAMA_URL"]  # http://localhost:11434
        self.model = os.environ["MODEL"]             # mistral:7b
        self.gh = Github(os.environ["GITHUB_TOKEN"])

    def review_pr(self, repo_name: str, pr_number: int):
        repo = self.gh.get_repo(repo_name)
        pr = repo.get_pull(pr_number)

        for file in pr.get_files():
            if not self._should_review(file.filename):
                continue

            # Отправить diff в Ollama
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": self.REVIEW_PROMPT.format(
                        diff=file.patch or "",
                        filename=file.filename
                    ),
                    "stream": False
                }
            )

            comment = response.json()["response"]

            if "LGTM" not in comment:
                # Постить inline комментарий на первую изменённую строку
                pr.create_review_comment(
                    body=f"🤖 **AI Review ({self.model}):**\n\n{comment}",
                    commit=pr.get_commits()[0],
                    path=file.filename,
                    line=file.additions  # последняя добавленная строка
                )

    def _should_review(self, filename: str) -> bool:
        SKIP_PATTERNS = [".lock", ".min.js", "migration", "__pycache__"]
        REVIEW_EXTENSIONS = [".py", ".js", ".ts", ".go", ".java", ".rs"]
        ext = os.path.splitext(filename)[1]
        return (ext in REVIEW_EXTENSIONS and
                not any(p in filename for p in SKIP_PATTERNS))
```

## Сравнение моделей для code review

```python
MODEL_BENCHMARK = {
    # Тестировалось на 50 реальных PR с 200+ изменёнными файлами

    "mistral:7b": {
        "время_запуска": "~45 сек (скачать + прогреть)",
        "скорость": "~15 tok/sec на ubuntu-latest",
        "качество": "хорошее: баги и style issues",
        "размер": "4.1 GB",
        "рекомендовано_для": "общий code review"
    },
    "codellama:7b": {
        "время_запуска": "~50 сек",
        "скорость": "~12 tok/sec",
        "качество": "лучше на алгоритмах и SQL",
        "размер": "3.8 GB",
        "рекомендовано_для": "backend / SQL / алгоритмы"
    },
    "phi3:mini": {
        "время_запуска": "~20 сек",
        "скорость": "~25 tok/sec",
        "качество": "базовое, пропускает сложные баги",
        "размер": "2.3 GB",
        "рекомендовано_для": "быстрые проверки стиля"
    },
    "llama3:8b": {
        "время_запуска": "~55 сек",
        "скорость": "~10 tok/sec",
        "качество": "лучшее из всех по общим знаниям",
        "размер": "4.7 GB",
        "рекомендовано_для": "полный review с контекстом"
    },
    "deepseek-coder:6.7b": {
        "время_запуска": "~40 сек",
        "скорость": "~18 tok/sec",
        "качество": "специализирован на коде, хорош для Python/Go",
        "размер": "3.8 GB",
        "рекомендовано_для": "code-first проекты"
    }
}

# Итог: mistral:7b = лучший баланс для большинства проектов
```

## Self-hosted runner: постоянная модель

```yaml
# Для production: self-hosted runner с предустановленной моделью
# Экономия: не скачивать модель каждый раз (4 GB × N PR/день)

# .github/workflows/ai-review-selfhosted.yml
jobs:
  ai-review:
    runs-on: self-hosted  # свой runner с Ollama уже установленным
    steps:
      - name: Ensure model cached
        run: |
          ollama list | grep -q "mistral:7b" || ollama pull mistral:7b

      - name: Run AI Review
        uses: Nikita-Filonov/ai-review@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          model: mistral:7b
          ollama_url: http://localhost:11434

# Self-hosted runner setup:
# sudo apt install ollama
# ollama pull mistral:7b  # один раз
# ./actions-runner/run.sh  # GitHub Actions runner daemon
```

## Применение к Lorenzo

```python
# Паттерн: AI review для scripts/improve_*.py

class LorenzoAIReview:
    """
    Lorenzo активно генерирует и изменяет Python скрипты.
    ai-review паттерн: автоматический review новых скриптов
    перед добавлением в репозиторий.
    """

    LORENZO_REVIEW_PROMPT = """
Проверь скрипт Lorenzo (scripts/improve_*.py):
1. Наличие --dry-run флага (требование всех Lorenzo скриптов)
2. Обработка отсутствующих файлов (KeyError, FileNotFoundError)
3. Корректная работа с docs/ путями
4. Нет hardcoded путей (должны быть относительные от корня репо)
5. UTF-8 encoding для русскоязычных файлов

{diff}
"""
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **ai-review + LLAMATOR (R33)** | Двойная защита: LLAMATOR тестирует LLM-безопасность, ai-review проверяет код-безопасность |
| **ai-review + Cursor Multi-Agent (R33)** | Reviewer субагент → ai-review как финальная проверка сгенерированного кода |
| **ai-review + DQ LLM (R33)** | ai-review для SQL-кода в DQ пайплайнах: проверка безопасности генерируемых запросов |
| **ai-review + vLLM R32** | vLLM backend вместо Ollama для команд с high-volume PR потоком |
| **ai-review + Cognitive Memory (R31)** | Хранение паттернов ревью в памяти → персонализированные рекомендации по проекту |

## Контакт

- Статья: https://habr.com/ru/articles/953598/ (октябрь 2025)
- GitHub tool: https://github.com/Nikita-Filonov/ai-review
- GitHub example: https://github.com/Nikita-Filonov/test-ai-review
- Смежная (DerAI + Solar appScreener SAST): https://habr.com/ru/companies/solarsecurity/articles/1031718/
- Смежная (вайбкод + DevSecOps pipeline): https://habr.com/ru/companies/ruvds/articles/1017858/
- Ollama: ollama.com

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
