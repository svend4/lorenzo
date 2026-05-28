---
date: 2026-05-28
tags: [rag, knowledge, local-first, architecture, roadmap]
state: normalized
---

# LLM Judge для валидации образовательного контента: CLEV и $0.014 за курс

<!-- toc-auto -->
<!-- tags: maslennikov-llm-judge-educational-content-clev, docs -->


<!-- summary -->
> `maslennikov-llm-judge-educational-content-clev` — раздел документации проекта Lorenzo.


> [!WARNING]
> Документ содержит описание рисков и ограничений. Изучите их перед принятием архитектурных решений.

<!-- alert-added -->

**Автор:** Maslennikovig (Игорь Масленников, DNA IT)  
**Хабр:** https://habr.com/ru/articles/970744/  
**GitHub:** нет (TypeScript примеры в статье)  
**Слой:** analytics / orchestration  
**Дата:** ноябрь 2025  
**Уникальность:** Не генерация образовательного контента, а его автоматическая валидация: cross-model LLM-judge pipeline (Gemini Flash + GPT-4o-mini + Claude Haiku) с алгоритмом CLEV (Consensus with Lazy Evaluation via Voting). Энтропийная детекция галлюцинаций через log-probabilities без RAG для 80-85% контента. $0.00117/урок vs $0.50 бюджет (3400-10300x дешевле ручной экспертной проверки). OSCQR образовательные стандарты как рубрики с VETO-порогами.

## Проблема: валидный промпт → некачественный урок

```
Проблема генерации образовательного контента с LLM:
  → Промпт верный, спецификация правильная
  → Урок всё равно плохой:
    * Галлюцинации ("Пифагор жил в XVI веке")
    * Pedagogical drift: заявлена цель A, реализована цель B
    * Bloom's Taxonomy несоответствие: цель "анализировать" → контент "запомни"
    * Читаемость Flesch-Kincaid не соответствует уровню аудитории

Стандартное решение: человек-эксперт проверяет каждый урок
  → Стоимость: ~$0.50/урок (5-10 мин эксперта)
  → Масштаб: 10K уроков = $5000 + 833 часа
  → Bottleneck: невозможно масштабировать

Решение: автоматическая LLM-валидация с консенсусом моделей
  → Стоимость: $0.00117/урок (→ $0.023 за 20-урочный курс)
  → Масштаб: нет ограничений
  → Качество: 3 модели голосуют, третья — tiebreaker
```

## CLEV: Consensus with Lazy Evaluation via Voting

```typescript
// Maslennikovig: LLM Judge для образовательного контента
// habr.com/ru/articles/970744

interface LessonQualityScore {
  totalScore: number;        // 0-100
  criteriaScores: Record<string, number>;
  vetoViolations: string[];  // критические нарушения → немедленный отказ
  hallucinations: string[];  // обнаруженные галлюцинации
  recommendations: string[];
}

interface CLEVResult {
  consensus: LessonQualityScore;
  judgesUsed: number;          // 2 или 3 (lazy: третий только при несогласии)
  agreement: number;           // 0-1 коэффициент согласия
  escalateToHuman: boolean;
}

async function clevVoting(
  lesson: string,
  rubrics: OSCQRRubrics
): Promise<CLEVResult> {
  /**
   * CLEV (Consensus with Lazy Evaluation via Voting):
   * 1. Judge1 (Gemini Flash) + Judge2 (GPT-4o-mini) оценивают урок
   * 2. Если согласны (agreement > threshold) → финальный результат
   * 3. Если расходятся → Judge3 (Claude Haiku) как tiebreaker
   *
   * Экономия: третий судья вызывается только в 15-30% случаев
   * → 60% экономия токенов vs всегда 3 судьи
   */

  // Шаг 1: два основных судьи
  const [score1, score2] = await Promise.all([
    evaluateWithJudge("gemini-2.0-flash", lesson, rubrics),
    evaluateWithJudge("gpt-4o-mini", lesson, rubrics)
  ]);

  const agreement = computeAgreement(score1, score2);

  // VETO: если хоть один судья видит критическое нарушение → сразу отказ
  const vetoViolations = [
    ...score1.vetoViolations,
    ...score2.vetoViolations
  ];
  if (vetoViolations.length > 0) {
    return {
      consensus: mergeScores(score1, score2),
      judgesUsed: 2,
      agreement,
      escalateToHuman: false
    };
  }

  // Шаг 2: если согласны — готово (экономия Judge3)
  if (agreement > 0.85) {
    return {
      consensus: mergeScores(score1, score2),
      judgesUsed: 2,
      agreement,
      escalateToHuman: false
    };
  }

  // Шаг 3: расхождение → tiebreaker (Claude Haiku дешевле всех)
  const score3 = await evaluateWithJudge("claude-haiku-4-5", lesson, rubrics);
  const finalConsensus = majorityVote(score1, score2, score3);

  // Если и после tiebreaker нет ясности → human escalation
  const finalAgreement = computeAgreement(finalConsensus, score3);

  return {
    consensus: finalConsensus,
    judgesUsed: 3,
    agreement: finalAgreement,
    escalateToHuman: finalAgreement < 0.7
  };
}
```

## Энтропийная детекция галлюцинаций

```typescript
interface EntropyAnalysis {
  overallEntropy: number;
  flaggedSentences: Array<{
    text: string;
    entropy: number;
    requiresRAGCheck: boolean;
  }>;
  ragRequired: boolean;  // только если есть flagged sentences
}

async function detectHallucinationsViaEntropy(
  lesson: string,
  model: string,
  threshold: number = 2.5  // настраивается на calibration датасете
): Promise<EntropyAnalysis> {
  /**
   * Reference-free детекция галлюцинаций через token log-probabilities.
   *
   * Идея: если модель не уверена в токене → высокая энтропия распределения
   * → вероятно, модель "придумывает" (галлюцинирует)
   *
   * Преимущество vs RAG-проверка:
   * - RAG: нужен внешний источник для каждого утверждения
   * - Энтропия: только модель + её уверенность → 0 внешних запросов
   * - Применяем RAG только к flagged (~15-20% контента)
   */

  const sentences = splitIntoSentences(lesson);
  const flagged = [];

  for (const sentence of sentences) {
    const logProbs = await getTokenLogProbabilities(model, sentence);
    const entropy = computeEntropy(logProbs);

    if (entropy > threshold) {
      flagged.push({
        text: sentence,
        entropy,
        requiresRAGCheck: true
      });
    }
  }

  return {
    overallEntropy: average(sentences.map(s => s.entropy || 0)),
    flaggedSentences: flagged,
    ragRequired: flagged.length > 0
  };
}

function computeEntropy(logProbs: number[]): number {
  /**
   * Shannon entropy по распределению вероятностей токенов.
   * H = -Σ p_i * log2(p_i)
   * Высокая H → модель "не знала" что написать → риск галлюцинации.
   */
  const probs = logProbs.map(lp => Math.exp(lp));
  return -probs.reduce((sum, p) => sum + (p > 0 ? p * Math.log2(p) : 0), 0);
}
```

## OSCQR стандарты как машинные рубрики

```typescript
interface OSCQRRubrics {
  /**
   * OSCQR (Open SUNY Course Quality Review): 50 критериев качества
   * онлайн-курсов, адаптированных для AI-генерации.
   *
   * Группы критериев:
   * - Course Overview & Information (Design 1-8)
   * - Course Technology (Technology 1-6)
   * - Design & Layout (Design 9-20)
   * - Content & Activities (Content 1-12)
   * - Interaction (Interaction 1-8)
   * - Assessment & Feedback (Assessment 1-6)
   */
  criteria: Array<{
    id: string;
    description: string;
    weight: number;      // важность критерия (0-1)
    isVeto: boolean;     // VETO = критическое нарушение → немедленный reject
    bloomsLevel?: number; // 1-6 (remember, understand, apply, analyze, evaluate, create)
    readabilityTarget?: { min: number; max: number };  // Flesch-Kincaid range
  }>;
}

const EDUCATIONAL_QUALITY_RUBRICS: OSCQRRubrics = {
  criteria: [
    {
      id: "BLOOM_ALIGNMENT",
      description: "Контент соответствует заявленным целям обучения по таксономии Блума",
      weight: 0.25,
      isVeto: true,  // несоответствие целей → VETO
      bloomsLevel: 3  // целевой уровень (apply)
    },
    {
      id: "READABILITY",
      description: "Читаемость текста соответствует уровню аудитории",
      weight: 0.15,
      isVeto: false,
      readabilityTarget: { min: 60, max: 80 }  // Flesch Reading Ease
    },
    {
      id: "FACTUAL_ACCURACY",
      description: "Нет фактических ошибок и галлюцинаций",
      weight: 0.30,
      isVeto: true  // любая галлюцинация → VETO
    },
    {
      id: "ENGAGEMENT",
      description: "Наличие практических примеров, вопросов для размышления",
      weight: 0.15,
      isVeto: false
    },
    {
      id: "STRUCTURE",
      description: "Чёткая структура: введение → основная часть → резюме",
      weight: 0.15,
      isVeto: false
    }
  ]
};


COST_BENCHMARK = {
  "сравнение": {
    "ручная_проверка_эксперт": {
      "стоимость": "$0.50/урок (5-10 мин × $6/час)",
      "масштаб_10K_уроков": "$5,000 + 833 часа"
    },
    "CLEV_автоматически": {
      "стоимость": "$0.00117/урок",
      "масштаб_10K_уроков": "$11.70",
      "скорость": "< 30 сек/урок",
      "экономия": "3400-10300x дешевле"
    }
  },
  "breakdown_по_моделям": {
    "gemini_flash": "$0.000075/урок",
    "gpt4o_mini": "$0.00042/урок",
    "claude_haiku_tiebreaker": "$0.00068/урок (только 15-30% случаев)"
  },
  "CLEV_savings": "60% экономия vs всегда 3 модели"
}
```

## Circuit Breaker: защита от бесконечного уточнения

```typescript
class RefinementCircuitBreaker {
  /**
   * Паттерн Circuit Breaker для остановки бесконечных refinement циклов.
   *
   * Проблема: LLM пытается улучшить урок → новая версия хуже →
   *            снова улучшает → снова хуже → бесконечный цикл.
   *
   * Решение: максимум 3 итерации, после — human escalation.
   */

  private maxAttempts = 3;
  private scoreHistory: number[] = [];

  shouldContinueRefinement(newScore: number): boolean {
    this.scoreHistory.push(newScore);

    if (this.scoreHistory.length >= this.maxAttempts) {
      return false;  // Circuit OPEN: принудительная остановка
    }

    if (this.scoreHistory.length >= 2) {
      const delta = newScore - this.scoreHistory[this.scoreHistory.length - 2];
      if (delta < 0.01) {
        return false;  // Конвергировали: улучшения < 1%
      }
    }

    return true;  // Продолжать
  }
}
```

## Применение к Lorenzo

```typescript
// Lorenzo: CLEV для валидации карточек проектов

class LorenzoCardValidator {
  /**
   * Maslennikov паттерн для Lorenzo:
   * CLEV-валидация карточек проектов перед добавлением в базу знаний.
   * Рубрики: уникальность, техническая глубина, воспроизводимость.
   * VETO: карточка без метрик или без конкретного кода.
   */

  LORENZO_RUBRICS = {
    criteria: [
      { id: "UNIQUENESS", weight: 0.35, isVeto: false },
      { id: "TECHNICAL_DEPTH", weight: 0.35, isVeto: true },
      { id: "REPRODUCIBILITY", weight: 0.20, isVeto: false },
      { id: "METRICS_PRESENT", weight: 0.10, isVeto: true }
    ]
  };

  async validateCard(cardText: string): Promise<CLEVResult> {
    return clevVoting(cardText, this.LORENZO_RUBRICS);
  }
}
```

## Возможные комбинации

| Комбинация | Новое свойство |
|------------|----------------|
| **LLM Judge + Yandex Eval (R44)** | CLEV как production evaluation pipeline: тот же multi-judge подход для оценки не уроков, а LLM-ответов |
| **LLM Judge + LOCK-R (R43)** | Blind Judge архитектура + CLEV: судья без CoT + консенсус = максимально беспристрастная оценка |
| **LLM Judge + LangGraph (R44)** | CLEV как LangGraph граф: узел judge1 → узел judge2 → conditional tiebreaker → refinement |
| **LLM Judge + LangFuse (R38)** | Трейсинг каждого судьи: какая модель чаще инициирует tiebreaker, где согласие падает |
| **LLM Judge + Lorenzo Gateway** | /api/cards с CLEV-валидацией: только качественные карточки попадают в базу |

## Контакт

- Статья: https://habr.com/ru/articles/970744/ (ноябрь 2025)
- Автор: Maslennikovig (Игорь Масленников, DNA IT)
- OSCQR стандарты: oscqr.suny.edu
- Bloom's Taxonomy: Revised Bloom's Taxonomy (Anderson & Krathwohl 2001)
- Flesch Reading Ease: formulae.mobi/flesch-reading-ease
- Смежная (Yandex LLM Evaluation, R44): docs/06-discovery/round-44/projects/yandex-llm-evaluation-production-pipeline.md
- Смежная (LOCK-R Blind Judge, R43): docs/06-discovery/round-43/projects/lockr-cot-paradox-bayesian-reasoning-benchmark.md

## Смотрите также
- [Главная](../../../README.md)
- [Метрики](../../../METRICS.md)
- [Здоровье](../../../HEALTH.md)
- [Глоссарий](../../../GLOSSARY.md)
- [Сущности](../../../ENTITIES.md)
- [Решения](../../../DECISIONS.md)
