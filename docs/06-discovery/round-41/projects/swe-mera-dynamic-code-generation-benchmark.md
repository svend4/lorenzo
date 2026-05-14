# SWE-MERA: динамический бенчмарк агентной генерации кода

**Автор:** madrugado (ODS community)  
**Хабр:** https://habr.com/ru/companies/ods/articles/948184/  
**GitHub:** https://github.com/MERA-Evaluation/repotest (задачи + запуск), https://github.com/MERA-Evaluation/SWE-MERA-submissions  
**ArXiv:** https://arxiv.org/abs/2507.11059  
**Слой:** analytics / orchestration  
**Дата:** сентябрь 2025  
**Уникальность:** Российский ответ на проблему контаминации статичных бенчмарков: SWE-MERA ежемесячно обновляется ~250 новыми реальными GitHub issues из активных репозиториев, а успех измеряется прохождением юнит-тестов из реального merged PR. Динамический пайплайн исключает temporal overfitting — LLM не может «выучить» задачи из training data. Первый публичный результат: DeepSeek-R1 лидирует с 27.8% pass@1 на 528 задачах.

## Проблема: SWE-bench стареет быстро

```
SWE-bench (статичный, 2310 задач из GitHub):
  → Задачи фиксированы → попадают в training data моделей
  → Temporal contamination: SOTA растёт, но реальное качество нет
  → GPT-4o в 2023: 1.7% → 2025: 49% — реально стало лучше в 28 раз?
  → Нет: частично это меморизация задач

SWE-MERA решает:
  → Каждый месяц: ~250 новых задач из свежих GitHub PR
  → Задачи не были в training data ни одной модели
  → Верификация: тесты должны быть в самом PR (не написаны вручную)
  → Метрика: прошли ли тесты PR после патча агента?
```

## Динамический пайплайн сбора задач

```python
# SWE-MERA: anti-contamination pipeline
# github.com/MERA-Evaluation/repotest

import datetime
from dataclasses import dataclass
from typing import Optional

@dataclass
class SWETask:
    """
    Одна задача = реальный GitHub Issue из merged PR.
    Тесты взяты из самого PR, не написаны вручную.
    """
    repo_url: str          # "github.com/user/project"
    issue_id: int
    pr_id: int             # merged PR с фиксом
    language: str          # "python"
    test_files: list[str]  # тесты из PR (верификация успеха)
    cutoff_date: datetime.date  # дата закрытия PR
    difficulty: str        # "easy" / "medium" / "hard"


class SWEMERACollector:
    """
    Ежемесячный пайплайн: GitHub → фильтрация → верификация → датасет.

    Ключевое отличие от SWE-bench:
    1. Только свежие PR (новее cutoff_date последнего обновления)
    2. Только репозитории с работающим pytest
    3. Только PR где тесты есть в самом PR (не только в основной ветке)
    """

    FILTERS = {
        "min_stars": 100,           # активный проект
        "languages": ["python"],    # первая версия — только Python
        "test_framework": "pytest", # верифицируемые тесты
        "pr_must_have_tests": True, # тесты обязаны быть в PR
        "monthly_refresh": 250      # ~250 новых задач в месяц
    }

    def collect_monthly_batch(self,
                               cutoff_date: datetime.date) -> list[SWETask]:
        """
        1. GitHub Search API: PR merged после cutoff_date
        2. Фильтрация по языку, звёздам, наличию pytest
        3. Проверка: есть ли тесты в PR diff?
        4. Клонирование + запуск тестов в sandbox (должны упасть до патча)
        5. Добавление в датасет с deduplication
        """
        fresh_prs = self._search_github_prs(after=cutoff_date)
        verified = []

        for pr in fresh_prs:
            if self._has_pytest_in_pr(pr) and self._tests_fail_before_patch(pr):
                verified.append(self._create_task(pr))

        return verified[:self.FILTERS["monthly_refresh"]]

    def _tests_fail_before_patch(self, pr: dict) -> bool:
        """
        Антиконтаминационная проверка:
        тесты из PR должны ПАДАТЬ на коде ДО патча.
        Если тесты проходят без патча — это не задача для агента.
        """
        base_sha = pr["base"]["sha"]
        test_result = self._run_pytest_on_sha(base_sha, pr["test_files"])
        return test_result.returncode != 0
```

## Агент-решатель: Aider framework

```python
class SWEMERASolver:
    """
    Решение задач через Aider (AI code editing framework).
    Агент: видит issue → применяет патч → pytest верифицирует.
    """

    def solve_task(self, task: SWETask,
                    model: str = "deepseek-r1") -> dict:
        """
        Стандартный подход (как в SWE-bench):
        1. Клонировать репо на базовый коммит
        2. Показать агенту: issue текст + релевантные файлы
        3. Агент генерирует патч (diff)
        4. Применить патч → запустить pytest
        5. pass@1 = True если все тесты прошли
        """
        repo = self.clone_at_base_commit(task)
        patch = self.aider_agent.solve(
            issue=task.issue_text,
            repo_path=repo,
            model=model
        )
        return self.evaluate_patch(repo, patch, task.test_files)


# Результаты на 528 задачах (сентябрь 2025)
LEADERBOARD = {
    "задач": 528,
    "метрика": "pass@1 (90% confidence interval)",

    "результаты": [
        {"model": "DeepSeek-R1",        "pass1": 0.278, "rank": 1},
        {"model": "Qwen2.5-Coder-32B",  "pass1": 0.129, "rank": 2},
        {"model": "Llama-3.3-70B",      "pass1": 0.087, "rank": 3},
        # ... другие модели
    ],

    "вывод": {
        "DeepSeek-R1": "Лидер: сильное reasoning для понимания issue",
        "Qwen2.5-Coder-32B": "Специализированная coding модель — 2 место",
        "Llama-3.3-70B": "Открытая модель — 3 место",
        "ключевое_наблюдение": "Разрыв между 1 и 2 местом большой (27.8% vs 12.9%)"
    }
}
```

## Динамический бенчмарк: преимущества и ограничения

```python
BENCHMARK_PROFILE = {
    "название": "SWE-MERA (Software Engineering Multiple Evaluation with Refresh)",
    "авторы": "ODS community (madrugado et al.)",
    "arxiv": "https://arxiv.org/abs/2507.11059",

    "преимущества": {
        "anti_contamination": "Задачи всегда новее cutoff любой модели",
        "real_world": "Реальные GitHub issues, не синтетика",
        "автоверификация": "Тесты из PR — не нужна ручная разметка",
        "monthly_refresh": "~250 новых задач каждый месяц",
        "объективность": "pass/fail — бинарная метрика без субъективности"
    },

    "ограничения": {
        "только_python": "Первая версия — Python-only (vs multilingual SWE-bench)",
        "bias_активных_репо": "Только репозитории со звёздами + pytest",
        "сложность_задач": "Реальные PR могут быть проще/сложнее равномерно",
        "aider_зависимость": "Агент-фреймворк — один из многих подходов"
    },

    "сравнение_с_аналогами": {
        "SWE-bench": "Статичный, 2310 задач, Python, засоренный",
        "Doubletapp_multi-SWE": "9 языков, 506 задач, статичный",
        "SWE-MERA": "Динамический, ~250/мес, Python, чистый"
    }
}
```

## Применение к Lorenzo

```python
# Lorenzo: dynamic evaluation паттерн для Q&A качества

class LorenzoDynamicEval:
    """
    SWE-MERA паттерн для Lorenzo:
    Не статичные Q&A тесты, а динамически обновляемый тест-сет
    из реальных вопросов пользователей.

    Аналог anti-contamination: использовать только вопросы,
    поступившие ПОСЛЕ обучения/настройки модели.
    """

    def collect_fresh_eval_cases(self,
                                  cutoff_date: datetime.date) -> list[dict]:
        """
        Вместо статичного Q&A набора:
        → Новые вопросы из Review Queue (review_queue.py)
        → После cutoff_date обновления документации
        → Верификация: есть ли правильный ответ в docs/?
        """
        pass

    def monthly_refresh(self) -> dict:
        """
        Каждый месяц: новые тест-кейсы из реальных запросов.
        Метрика: прошёл ли поиск + LLM ответ проверку рецензента.
        """
        pass
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **SWE-MERA + Agent Distillation (R39)** | Стряска агентных трасс на SWE-MERA → дистилляция coding агента |
| **SWE-MERA + Stryker Testing (R39)** | Mutation testing + SWE-MERA задачи → оценка качества патчей агента |
| **SWE-MERA + LangFuse (R38)** | Трейсинг каждой попытки решения: время, токены, pass/fail |
| **SWE-MERA + Sequential (R38)** | Ансамбль агентов решает SWE-задачи последовательно (панель программистов) |
| **SWE-MERA + Lorenzo Gateway** | /api/code-eval: динамический бенчмарк через Lorenzo API |

## Контакт

- Статья: https://habr.com/ru/companies/ods/articles/948184/ (сентябрь 2025)
- GitHub задачи: https://github.com/MERA-Evaluation/repotest
- GitHub сабмиты: https://github.com/MERA-Evaluation/SWE-MERA-submissions
- ArXiv: https://arxiv.org/abs/2507.11059
- ODS (Open Data Science): ods.ai
- Aider: aider.chat
- Смежная (multilingual SWE-bench, Doubletapp): https://habr.com/ru/companies/doubletapp/articles/916388/
- Смежная (LLM unit-test generation, VK): https://habr.com/ru/companies/vk/articles/921410/
