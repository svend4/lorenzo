# Код без автора: comprehension debt и деградация качества AI-сгенерированного кода

**Автор:** diffnotes-tech (Хабр, апрель 2025)  
**Хабр:** https://habr.com/ru/articles/1021068/  
**GitHub:** не применимо (аналитическая статья)  
**Слой:** orchestration / analytics  
**Дата:** апрель 2025  
**Уникальность:** Эмпирическое исследование деградации качества кода в эпоху AI: GitClear анализировал 211 миллионов строк кода за 2020–2025 — code churn удвоился, рефакторинг упал на 60%. Вводится понятие «comprehension debt» — разрыв между размером кодовой базы и реальным пониманием команды. Практические меры: TDD-принудиловка, domain-specific правила в `.claude/rules/`, хуки автоматизации. Опаснее классического tech debt.

## Данные: что происходит с кодовыми базами

```
GitClear исследование (211M строк, 2020-2025):

Метрика               2020    2022    2024    2025 (прогноз)
──────────────────────────────────────────────────────────
Code churn            100%    118%    187%    210%+
  (изменений/строку)
Рефакторинг            100%    94%     62%     ~50%
  (доля commits)
Copy-paste code        100%    110%    142%    ~160%
  (дублирование)
Документация           100%    97%     71%     ~60%
  (покрытие кода)

Интерпретация:
→ AI пишет код быстро → много кода
→ AI редко рефакторит → нарастает дублирование
→ AI не пишет доктрины → растёт comprehension debt
→ Люди чинят AI-код: churn удваивается
```

## Comprehension Debt: новый вид технического долга

```python
# Классический Technical Debt:
# "Мы знаем что здесь грязно, надо переписать"
# → Видимый, измеримый, можно приоритизировать

# Comprehension Debt (новое понятие):
# "Никто не понимает как это работает"
# → Невидимый, накапливается незаметно, взрывается при онбординге/баге

class ComprehensionDebt:
    """
    Симптомы:
    1. "Лучше переписать с нуля" при любом баге
    2. Bus factor = 1 (только один человек понимает модуль)
    3. Новый разработчик не может онбординговаться без 2+ недель
    4. "Не трогай, работает" — главное правило
    5. Тесты тестируют implementation, не поведение
    """

    def measure(self, codebase: Codebase) -> float:
        """Примерная метрика comprehension debt"""
        return (
            codebase.churn_rate *          # как часто меняется
            codebase.copy_paste_ratio *    # насколько дублирован
            (1 / codebase.test_coverage) * # насколько не покрыт тестами
            (1 / codebase.doc_coverage)    # насколько не документирован
        )

# Почему AI усугубляет:
# AI пишет "рабочий" код → человек принимает MR не читая
# → накапливается код которого никто не понимает
# → при баге: "исправить" = написать ещё AI-кода поверх
```

## Паттерны деградации AI-кода

```python
DEGRADATION_PATTERNS = {
    "copy_paste_amplification": {
        "описание": "AI копирует паттерны без понимания → дублирование растёт",
        "пример": """
        # AI видит в контексте:
        def validate_email(email):
            return re.match(r'[^@]+@[^@]+\.[^@]+', email)

        # И генерирует похожую функцию в другом файле:
        def check_email_format(email):
            return re.match(r'[^@]+@[^@]+\.[^@]+', email)
        # Вместо: импортировать validate_email
        """,
        "решение": "Запрет на генерацию без проверки на дубли"
    },

    "context_hallucination": {
        "описание": "AI предполагает несуществующие зависимости",
        "пример": """
        # AI пишет:
        from utils.validators import validate_user_input
        # Такого модуля не существует → ImportError в prod
        """,
        "решение": "TDD: тест должен пройти перед code review"
    },

    "shallow_error_handling": {
        "описание": "AI добавляет try/except которые скрывают ошибки",
        "пример": """
        try:
            result = complex_operation()
        except Exception:
            return None  # Что пошло не так? Неизвестно
        """,
        "решение": "Линтер: запрет bare except, требовать logging"
    },

    "test_washing": {
        "описание": "AI пишет тесты которые проходят но ничего не тестируют",
        "пример": """
        def test_calculate_price():
            result = calculate_price(100, 0.2)
            assert result is not None  # Проверяет только что не None
            # Не проверяет: result == 80
        """,
        "решение": "Mutation testing (R20 паттерн)"
    }
}
```

## Практические меры: как замедлить деградацию

```python
# Мера 1: domain-specific правила для AI

# .claude/rules/no-duplication.md:
"""
НИКОГДА не создавай новую функцию если похожая существует.
Перед написанием кода: поищи существующие утилиты в utils/, helpers/
Если пишешь похожий код дважды → рефактори в общую функцию.
"""

# .claude/rules/error-handling.md:
"""
ВСЕГДА логируй ошибки перед тем как обработать.
НИКОГДА не используй bare except: или except Exception: без логирования.
При неизвестной ошибке → raise, не return None.
"""

# Мера 2: хуки автоматизации

# pre-commit hook: проверка на дублирование
HOOK_CONFIG = {
    "repos": [{
        "repo": "local",
        "hooks": [{
            "id": "check-duplicates",
            "name": "Detect copy-paste code",
            "entry": "python scripts/detect_duplication.py",
            "language": "python",
            "types": ["python"],
            "args": ["--threshold", "0.85"]  # 85% схожесть = дубль
        }]
    }]
}

# Мера 3: TDD-принудиловка

# Workflow: AI пишет тест → тест падает → AI пишет код → тест проходит
# НЕ: AI пишет код → AI пишет тест → тест проходит (потому что так написан)

class TDDEnforcer:
    def review_ai_output(self, pr: PullRequest) -> ReviewResult:
        # Проверить: тесты написаны ДО кода (по git history)
        test_commit = pr.find_first_test_commit()
        code_commit = pr.find_first_impl_commit()

        if code_commit.timestamp < test_commit.timestamp:
            return ReviewResult(
                approved=False,
                reason="Код написан раньше тестов. Требуется TDD."
            )
```

## Метрики для измерения comprehension debt

```python
COMPREHENSION_DEBT_METRICS = {
    # Структурные
    "churn_rate": "изменений на строку кода за месяц",
    "copy_paste_ratio": "% кода являющегося дублями (PMD CPD)",
    "bus_factor": "min разработчиков знающих модуль (git blame)",
    "cognitive_complexity": "цикломатическая сложность (SonarQube)",

    # AI-специфичные
    "ai_generated_ratio": "% кода написанного AI (watermarking/git stats)",
    "ai_churn_rate": "churn rate AI-кода vs human-кода",
    "hallucination_imports": "% импортов не существующих в проекте",
    "test_meaningfulness": "mutation score (≠ coverage!)"
}

# Алерт: если ai_churn_rate > 2× human_churn_rate → проблема
# Алерт: если mutation_score < 40% → тесты не тестируют
```

## Применение к Lorenzo

Lorenzo генерирует код (improve_self.py). Comprehension Debt паттерн:

```python
# improve_comprehension_audit.py (паттерн):

class LorenzoComprehensionAudit:
    """
    Мониторинг comprehension debt в скриптах Lorenzo
    Аналог GitClear — но для скриптов в scripts/
    """

    def measure_churn(self) -> dict:
        """Какие скрипты меняются чаще всего (и почему?)"""
        return git_log_analysis(
            path="scripts/",
            metric="changes_per_file_per_month"
        )

    def detect_duplicates(self) -> list[DuplicatePair]:
        """Есть ли похожие функции в разных скриптах?"""
        return cpd_analysis(
            path="scripts/improve_*.py",
            threshold=0.80  # 80% схожести = дубль
        )

    def measure_bus_factor(self) -> dict:
        """Скрипты которые понимает только их автор"""
        return {
            script: git_blame_unique_authors(script)
            for script in list_scripts()
        }

    def generate_report(self) -> str:
        return f"""
        # Comprehension Debt Report

        Churn: {self.measure_churn()}
        Дубли: {self.detect_duplicates()}
        Bus factor: {self.measure_bus_factor()}
        """
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **Comprehension Debt + DerAI (R27)** | DerAI находит уязвимости в AI-коде → comprehension debt = вектор атаки |
| **Comprehension Debt + RAG TestGen (R27)** | Тесты к AI-коду как часть борьбы с comprehension debt |
| **Comprehension Debt + Observability (R13)** | Трейсинг AI-кода: где именно накапливается долг в production |
| **Comprehension Debt + LLM Judge (R28)** | LLM Judge оценивает понятность кода, не только корректность |
| **Comprehension Debt + Code Review AI (R15)** | Code review специально ищет признаки comprehension debt |

## Контакт

- Статья: https://habr.com/ru/articles/1021068/ (апрель 2025)
- GitClear research: gitclear.com/research
- Смежная (AI тесты которые ничего не тестируют): https://habr.com/ru/articles/1023532/
- PMD CPD (copy-paste detector): github.com/pmd/pmd
- SonarQube cognitive complexity: sonarqube.org
