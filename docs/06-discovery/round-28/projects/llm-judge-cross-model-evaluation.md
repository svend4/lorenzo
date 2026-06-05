# LLM Judge: кросс-модельная оценка контента за $0.014 — как победить self-preference bias

> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Игорь Масленников (DNA IT, Хабр, ноябрь 2025)  
**Хабр:** https://habr.com/ru/articles/970744/  
**GitHub:** не опубликован (архитектура описана в статье)  
**Слой:** orchestration / analytics  
**Дата:** ноябрь 2025  
**Уникальность:** Обнаружен и решён критический баг LLM evaluation: модели статистически значимо предпочитают outputs своего же семейства (low-perplexity preference). Решение — кросс-модельная оценка (судья из другого семейства). Двухстадийная валидация: Specification Check + Faithfulness Hallucination Check. Архитектура Map-Reduce-Refine. Стоимость: $0.014 за полный курс.

## Открытие: LLM-судья нечестен со своими родственниками

```
Эксперимент:
  Задача: оценить качество автогенерированного образовательного контента
  
  Попытка 1: GPT-5 генерирует → GPT-5 оценивает
    Результат: GPT-5 стабильно даёт высокие оценки своим outputs
    
  Попытка 2: Claude генерирует → Claude оценивает
    Результат: то же самое
    
  Гипотеза: Low-perplexity preference
    Модель воспринимает свои собственные outputs как "знакомые"
    → меньшая перплексия → субъективно "лучше"
    → не реальное качество, а "узнаю свой стиль"

Доказательство (статистика):
  GPT-5 оценивает GPT-outputs:   avg 8.7/10
  GPT-5 оценивает Claude-outputs: avg 7.2/10
  Claude оценивает то же самое:   8.9 vs 7.0 (обратная картина!)
  
  Вывод: single-model self-evaluation = ненадёжно
```

## Решение: кросс-модельная оценка

```python
# Архитектура: генератор и судья из РАЗНЫХ семейств

class CrossModelEvaluator:
    def __init__(self):
        # Генераторы (любые)
        self.generators = {
            "primary": GPT5(),
            "backup": Claude()
        }

        # Судьи: обязательно из другого семейства чем генератор
        self.judges = {
            "for_gpt_outputs":    Claude(),    # Claude судит GPT
            "for_claude_outputs": Gemini(),    # Gemini судит Claude
            "for_any":            Ensemble([Claude(), Gemini()])  # безопаснее
        }

    def evaluate(self, content: str, generator: str) -> EvalResult:
        judge = self.judges[f"for_{generator}_outputs"]
        return judge.evaluate(content, self.rubric)

    # Принцип: никогда не используй тот же LLM-провайдер для оценки
    # что и для генерации в критических сценариях
```

## Двухстадийная валидация: Spec + Faithfulness

```python
# Два типа ошибок в LLM-контенте (образование, как пример)

HALLUCINATION_TAXONOMY = {
    "specification_violation": {
        "описание": "Контент не соответствует ТЗ",
        "пример": "Попросили объяснить для новичков → написали для экспертов",
        "стадия": "Stage 5: Specification Check"
    },
    "faithfulness_hallucination": {
        "описание": "Контент противоречит фактам реального мира",
        "пример": "Правильно структурирован, но содержит неверные факты",
        "стадия": "Stage 6: Faithfulness Check",
        "сложность": "Может пройти Stage 5 и провалить Stage 6!"
    }
}

class TwoStageValidator:
    def validate(self, content: str, spec: Specification) -> ValidationResult:
        # СТАДИЯ 5: Проверка соответствия спецификации
        spec_result = self.check_specification(content, spec)
        if not spec_result.passed:
            return ValidationResult(
                passed=False,
                stage="specification",
                issues=spec_result.violations
            )

        # СТАДИЯ 6: Проверка фактической достоверности
        # Отдельный судья, другой промпт
        faithfulness_result = self.check_faithfulness(content)
        return ValidationResult(
            passed=faithfulness_result.passed,
            stage="faithfulness",
            issues=faithfulness_result.hallucinations
        )

    def check_faithfulness(self, content: str) -> FaithfulnessResult:
        # Судья проверяет каждый факт отдельно
        facts = self.extract_factual_claims(content)
        hallucinations = []
        for fact in facts:
            verification = self.cross_model_judge.verify(
                claim=fact.text,
                rubric=FACTUAL_ACCURACY_RUBRIC
            )
            if not verification.is_accurate:
                hallucinations.append(fact)
        return FaithfulnessResult(hallucinations=hallucinations)
```

## Map-Reduce-Refine: масштабируемая валидация

```python
# Проблема: полный курс = тысячи единиц контента
# Решение: Hybrid Map-Reduce-Refine

class MapReduceRefineEvaluator:
    def evaluate_course(self, course: Course) -> CourseEvaluation:
        # MAP: параллельная оценка каждого урока
        lesson_evaluations = parallel_map(
            fn=self.evaluate_lesson,
            items=course.lessons,
            max_workers=20
        )

        # REDUCE: агрегация по модулям
        module_summaries = []
        for module in course.modules:
            module_lessons = [e for e in lesson_evaluations
                              if e.lesson_id in module.lesson_ids]
            module_summary = self.reduce_to_module(module_lessons)
            module_summaries.append(module_summary)

        # REFINE: финальный LLM проход по агрегированным данным
        # (не по сырым — экономим токены)
        final_report = self.refine(
            module_summaries=module_summaries,
            course_spec=course.specification
        )

        return CourseEvaluation(
            score=final_report.overall_score,
            issues=final_report.critical_issues,
            recommendations=final_report.improvements
        )

# Стоимость:
# Наивный подход: $240 за курс (все токены всех уроков)
# Map-Reduce-Refine: $0.014 за курс
# Экономия: 17,000×
```

## Рубрика LLM-судьи

```python
EVALUATION_RUBRIC = {
    "specification_criteria": [
        {
            "name": "target_audience_match",
            "weight": 0.3,
            "prompt": "Соответствует ли сложность изложения уровню {audience}?",
            "scale": "1-5"
        },
        {
            "name": "completeness",
            "weight": 0.25,
            "prompt": "Охвачены ли все темы из спецификации?",
            "scale": "1-5"
        },
        {
            "name": "structure",
            "weight": 0.2,
            "prompt": "Следует ли контент заданной структуре?",
            "scale": "1-5"
        }
    ],
    "faithfulness_criteria": [
        {
            "name": "factual_accuracy",
            "weight": 0.4,
            "prompt": "Содержит ли текст фактические ошибки? Перечисли каждую.",
            "scale": "binary + list"
        },
        {
            "name": "source_fidelity",
            "weight": 0.3,
            "prompt": "Точно ли отражены факты из источников?",
            "scale": "1-5"
        }
    ]
}
```

## Применение к Lorenzo

Lorenzo генерирует контент (summaries, QA, reports). LLM Judge паттерн:

```python
# improve_llm_judge.py (паттерн):

class LorenzoContentJudge:
    """
    Оценивает качество LLM-генерированного контента в Lorenzo
    Применяет cross-model принцип: Claude генерирует → другая модель оценивает
    """

    def evaluate_summary(self, original: str, summary: str) -> JudgeResult:
        # improve_llm_summary.py генерирует Claude → оцениваем другой моделью
        judge_prompt = f"""
        Оцени качество суммаризации:
        
        Оригинал: {original[:500]}
        Суммаризация: {summary}
        
        Критерии:
        1. Точность: нет ли искажения фактов? (1-5)
        2. Полнота: все ли ключевые идеи? (1-5)
        3. Краткость: нет ли воды? (1-5)
        
        Укажи конкретные Faithfulness Hallucinations если есть.
        """
        return self.cross_model_judge.evaluate(judge_prompt)

    def validate_qa_answers(self, doc: str, qa_pairs: list[QA]) -> list[Issue]:
        """QA-ответы Lorenzo могут содержать Faithfulness Hallucinations"""
        issues = []
        for qa in qa_pairs:
            result = self.evaluate_faithfulness(
                source=doc,
                claim=qa.answer
            )
            if not result.is_accurate:
                issues.append(Issue(qa=qa, type="faithfulness", detail=result.error))
        return issues
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM Judge + RAG eval (R16)** | RAG eval + cross-model judge = честная оценка без self-preference |
| **LLM Judge + CAVM (R26)** | VerificationAgent в CAVM = LLM Judge для цифр в отчёте |
| **LLM Judge + EdTech AI (R24)** | Bloom's taxonomy test gen → LLM Judge оценивает вопросы |
| **LLM Judge + DerAI (R27)** | DerTriage results → LLM Judge независимо верифицирует вердикты |
| **LLM Judge + Normcontrol (R25)** | Нормоконтроль → LLM Judge из другого семейства перепроверяет |

## Контакт

- Статья: https://habr.com/ru/articles/970744/ (ноябрь 2025)
- Смежная (LLM-as-judge Яндекс PR описания): https://habr.com/ru/companies/yandex/articles/907646/
- Смежная (RAG evaluation R16): https://habr.com/ru/companies/
- MT-Bench (multi-turn LLM judge): github.com/lm-sys/FastChat
- LLM-as-a-Judge (оригинальная статья): arxiv.org/abs/2306.05685
